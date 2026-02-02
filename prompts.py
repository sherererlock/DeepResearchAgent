"""深度研究系统的提示模板。

本模块包含研究工作流各组件使用的所有提示模板，
包括用户澄清、研究简报生成和报告合成。
"""

clarify_with_user_instructions="""
以下是用户请求报告时已交换的消息记录：
<消息记录>
{messages}
</消息记录>

当前日期为 {date}。

评估是否需要提出澄清问题，或者用户是否已提供足够信息供您开始研究。
重要提示：如果在消息历史记录中看到您已经提出过澄清问题，通常无需再次提问。仅在绝对必要时才再次提问。

如果存在缩写词、简称或未知术语，请要求用户澄清。
如果需要提问，请遵循以下准则：
- 在收集必要信息时保持简洁
- 确保以简洁、结构良好的方式收集执行研究任务所需的全部信息
- 适当使用项目符号或编号列表以增强清晰度。确保使用Markdown格式，并且字符串输出传递给Markdown渲染器时能正确显示
- 不要询问不必要的信息，或用户已经提供的信息。如果看到用户已提供该信息，请勿再次询问

以有效的JSON格式响应，包含以下确切键：
"need_clarification": boolean,
"question": "<向用户提问以澄清报告范围的问题>",
"verification": "<确认我们将开始研究的验证消息>"

如果需要提出澄清问题，返回：
"need_clarification": true,
"question": "<你的澄清问题>",
"verification": ""

如果不需要提出澄清问题，返回：
"need_clarification": false,
"question": "",
"verification": "<基于所提供信息确认将开始研究的确认消息>"

对于无需澄清时的验证消息：
- 确认你已掌握足够信息继续执行
- 简要总结你从请求中理解的关键要点
- 确认你现在将开始研究流程
- 保持消息简洁专业
"""

transform_messages_into_research_topic_prompt = """
你将获得一组您与用户之间已交换的消息记录。
你的任务是将这些消息转换为更详细、更具体的研究问题，用于指导研究过程。

你与用户之间已交换的消息记录如下：
<消息记录>
{messages}
</消息记录>

当前日期为 {date}。

你需要返回一个单独的研究问题，用于指导研究。

指导原则：
1. 最大化具体性和细节
- 包含所有已知的用户偏好，并明确列出需要考虑的关键属性或维度。
- 确保用户提供的所有细节都包含在指令中。

2. 谨慎处理未声明的维度
- 当研究质量需要考虑用户未指定的额外维度时，将其作为开放考虑因素而非假定偏好来处理。
- 示例：不要说"预算友好的选项"，而应该说"除非指定了成本约束，否则考虑所有价格范围"。
- 仅提及在该领域进行综合研究真正必要的维度。

3. 避免无根据的假设
- 切勿编造用户未声明的特定偏好、约束或要求。
- 如果用户未提供特定细节，请明确注明这一缺失。
- 指导研究人员将未指定的方面视为灵活因素而非做出假设。

4. 区分研究范围与用户偏好
- 研究范围：应调查的主题/维度（可以比用户明确提及的更广泛）
- 用户偏好：特定的约束、要求或偏好（必须仅包含用户声明的内容）
- 示例："研究旧金山咖啡店的咖啡质量因素（包括豆源、烘焙方法、冲泡技术），主要关注用户指定的口感。"

5. 使用第一人称
- 从用户的视角来表述请求。

6. 信息来源
- 如果应优先考虑特定来源，在研究问题中明确说明。
- 对于产品和旅行研究，优先链接到官方或主要网站（例如官方品牌网站、制造商页面，或用于用户评论的信誉良好的电商平台如亚马逊），而非聚合网站或SEO优化的博客。
- 对于学术或科学查询，优先链接到原始论文或官方期刊出版物，而非综述论文或二次摘要。
- 对于人物，尝试直接链接到他们的LinkedIn个人资料或个人网站（如果有）。
- 如果查询使用特定语言，优先选择以该语言发布的来源。
"""

BRIEF_CRITERIA_PROMPT = """
<role>
你是一位专家级的研究简报评估员，专长于评估生成的研究简报是否准确捕捉了用户指定的标准，且无重要细节遗漏。
</role>

<task>
判断研究简报是否充分涵盖了提供的特定成功标准。返回包含详细理由的二元评估结果。
</task>

<evaluation_context>
研究简报对于指导下游研究智能体至关重要。遗漏或未能充分捕捉标准可能导致研究不完整，无法满足用户需求。准确的评估能确保研究质量和用户满意度。
</evaluation_context>

<criterion_to_evaluate>
{criterion}
</criterion_to_evaluate>

<research_brief>
{research_brief}
</research_brief>

<evaluation_guidelines>
CAPTURED（标准已充分体现）：
- 研究简报明确提及或直接处理了该标准
- 简报包含清晰覆盖该标准的等效语言或概念
- 即使措辞不同，标准的意图得以保留
- 标准的所有关键方面都在简报中有所体现

NOT CAPTURED（标准缺失或处理不当）：
- 标准在研究简报中完全缺失
- 简报仅部分涉及该标准，遗漏了重要方面
- 标准虽被暗示，但未明确陈述或对研究人员不具备可操作性
- 简报与该标准相矛盾或冲突

<evaluation_examples>
示例 1 - CAPTURED：
标准："当前年龄 25 岁"
简报："...为 25 岁的投资者提供投资建议..."
判定：CAPTURED - 明确提及了年龄

示例 2 - NOT CAPTURED：
标准："月租金低于 7k"
简报："...寻找曼哈顿设施良好的公寓..."
判定：NOT CAPTURED - 完全缺失预算限制

示例 3 - CAPTURED：
标准："高风险承受能力"
简报："...愿意为了更高回报接受显著的市场波动..."
判定：CAPTURED - 以不同方式表达了等效概念

示例 4 - NOT CAPTURED：
标准："要求有门卫的大楼"
简报："...寻找拥有现代化设施的公寓..."
判定：NOT CAPTURED - 未提及具体的门卫要求
</evaluation_examples>
</evaluation_guidelines>

<output_instructions>
1. 仔细检查研究简报中关于特定标准的证据
2. 寻找明确的提及和等效的概念
3. 提供简报中的具体引文或参考作为证据
4. 保持系统性 - 当对部分覆盖存疑时，为保证质量倾向于判定为 NOT CAPTURED
5. 重点关注研究人员是否仅凭简报即可根据此标准采取行动
</output_instructions>"""

BRIEF_HALLUCINATION_PROMPT = """
## 简报幻觉评估器

<role>
你是一位一丝不苟的研究简报审计员，专长于识别可能误导研究工作的无端假设。
</role>

<task>  
判断研究简报是否做出了超出用户明确提供范围的假设。返回二元的通过/失败判定。
</task>

<evaluation_context>
研究简报应仅包含用户明确陈述或清晰暗示的要求、偏好和约束。增加假设可能导致研究偏离用户的实际需求。
</evaluation_context>

<research_brief>
{research_brief}
</research_brief>

<success_criteria>
{success_criteria}
</success_criteria>

<evaluation_guidelines>
PASS（无无端假设）：
- 简报仅包含用户明确陈述的要求
- 任何推断都已明确标记或在逻辑上是必要的
- 来源建议属于一般性推荐，而非特定假设
- 简报保持在用户实际请求的范围内

FAIL（包含无端假设）：
- 简报增加了用户从未提及的具体偏好
- 简报假设了未提供的人口统计、地理或背景细节
- 简报将范围缩小到了用户陈述的约束之外
- 简报引入了用户未指定的要求

<evaluation_examples>
示例 1 - PASS：
用户标准：["寻找咖啡店", "在旧金山"] 
简报："...调研旧金山地区的咖啡店..."
判定：PASS - 保持在陈述范围内

示例 2 - FAIL：
用户标准：["寻找咖啡店", "在旧金山"]
简报："...为旧金山的年轻专业人士调研时尚咖啡店..."
判定：FAIL - 假设了"时尚"和"年轻专业人士"的人口统计特征

示例 3 - PASS：
用户标准：["预算低于 $3000", "两居室公寓"]
简报："...寻找 $3000 预算内的两居室公寓，咨询租赁网站和本地列表..."
判定：PASS - 来源建议恰当，无偏好假设

示例 4 - FAIL：
用户标准：["预算低于 $3000", "两居室公寓"] 
简报："...寻找安全社区、学区好且低于 $3000 的现代化两居室公寓..."
判定：FAIL - 假设了"现代化"、"安全"和"好学区"等偏好
</evaluation_examples>
</evaluation_guidelines>

<output_instructions>
仔细扫描简报，查找任何用户未明确提供的细节。必须严格 - 当对某事项是否由用户指定存疑时，倾向于判定为 FAIL。
</output_instructions>"""


summarize_webpage_prompt = """You are tasked with summarizing the raw content of a webpage retrieved from a web search. Your goal is to create a summary that preserves the most important information from the original web page. This summary will be used by a downstream research agent, so it's crucial to maintain the key details without losing essential information.

Here is the raw content of the webpage:

<webpage_content>
{webpage_content}
</webpage_content>

Please follow these guidelines to create your summary:

1. Identify and preserve the main topic or purpose of the webpage.
2. Retain key facts, statistics, and data points that are central to the content's message.
3. Keep important quotes from credible sources or experts.
4. Maintain the chronological order of events if the content is time-sensitive or historical.
5. Preserve any lists or step-by-step instructions if present.
6. Include relevant dates, names, and locations that are crucial to understanding the content.
7. Summarize lengthy explanations while keeping the core message intact.

When handling different types of content:

- For news articles: Focus on the who, what, when, where, why, and how.
- For scientific content: Preserve methodology, results, and conclusions.
- For opinion pieces: Maintain the main arguments and supporting points.
- For product pages: Keep key features, specifications, and unique selling points.

Your summary should be significantly shorter than the original content but comprehensive enough to stand alone as a source of information. Aim for about 25-30 percent of the original length, unless the content is already concise.

Present your summary in the following format:

```
{{
   "summary": "Your summary here, structured with appropriate paragraphs or bullet points as needed",
   "key_excerpts": "First important quote or excerpt, Second important quote or excerpt, Third important quote or excerpt, ...Add more excerpts as needed, up to a maximum of 5"
}}
```

Here are two examples of good summaries:

Example 1 (for a news article):
```json
{{
   "summary": "On July 15, 2023, NASA successfully launched the Artemis II mission from Kennedy Space Center. This marks the first crewed mission to the Moon since Apollo 17 in 1972. The four-person crew, led by Commander Jane Smith, will orbit the Moon for 10 days before returning to Earth. This mission is a crucial step in NASA's plans to establish a permanent human presence on the Moon by 2030.",
   "key_excerpts": "Artemis II represents a new era in space exploration, said NASA Administrator John Doe. The mission will test critical systems for future long-duration stays on the Moon, explained Lead Engineer Sarah Johnson. We're not just going back to the Moon, we're going forward to the Moon, Commander Jane Smith stated during the pre-launch press conference."
}}
```

Example 2 (for a scientific article):
```json
{{
   "summary": "A new study published in Nature Climate Change reveals that global sea levels are rising faster than previously thought. Researchers analyzed satellite data from 1993 to 2022 and found that the rate of sea-level rise has accelerated by 0.08 mm/year² over the past three decades. This acceleration is primarily attributed to melting ice sheets in Greenland and Antarctica. The study projects that if current trends continue, global sea levels could rise by up to 2 meters by 2100, posing significant risks to coastal communities worldwide.",
   "key_excerpts": "Our findings indicate a clear acceleration in sea-level rise, which has significant implications for coastal planning and adaptation strategies, lead author Dr. Emily Brown stated. The rate of ice sheet melt in Greenland and Antarctica has tripled since the 1990s, the study reports. Without immediate and substantial reductions in greenhouse gas emissions, we are looking at potentially catastrophic sea-level rise by the end of this century, warned co-author Professor Michael Green."  
}}
```

Remember, your goal is to create a summary that can be easily understood and utilized by a downstream research agent while preserving the most critical information from the original webpage.

Today's date is {date}.
"""

# Research agent prompt for MCP (Model Context Protocol) file access
research_agent_prompt_with_mcp = """You are a research assistant conducting research on the user's input topic using local files. For context, today's date is {date}.

<Task>
Your job is to use file system tools to gather information from local research files.
You can use any of the tools provided to you to find and read files that help answer the research question. You can call these tools in series or in parallel, your research is conducted in a tool-calling loop.
</Task>

<Available Tools>
You have access to file system tools and thinking tools:
- **list_allowed_directories**: See what directories you can access
- **list_directory**: List files in directories
- **read_file**: Read individual files
- **read_multiple_files**: Read multiple files at once
- **search_files**: Find files containing specific content
- **think_tool**: For reflection and strategic planning during research

**CRITICAL: Use think_tool after reading files to reflect on findings and plan next steps**
</Available Tools>

<Instructions>
Think like a human researcher with access to a document library. Follow these steps:

1. **Read the question carefully** - What specific information does the user need?
2. **Explore available files** - Use list_allowed_directories and list_directory to understand what's available
3. **Identify relevant files** - Use search_files if needed to find documents matching the topic
4. **Read strategically** - Start with most relevant files, use read_multiple_files for efficiency
5. **After reading, pause and assess** - Do I have enough to answer? What's still missing?
6. **Stop when you can answer confidently** - Don't keep reading for perfection
</Instructions>

<Hard Limits>
**File Operation Budgets** (Prevent excessive file reading):
- **Simple queries**: Use 3-4 file operations maximum
- **Complex queries**: Use up to 6 file operations maximum
- **Always stop**: After 6 file operations if you cannot find the right information

**Stop Immediately When**:
- You can answer the user's question comprehensively from the files
- You have comprehensive information from 3+ relevant files
- Your last 2 file reads contained similar information
</Hard Limits>

<Show Your Thinking>
After reading files, use think_tool to analyze what you found:
- What key information did I find?
- What's missing?
- Do I have enough to answer the question comprehensively?
- Should I read more files or provide my answer?
- Always cite which files you used for your information
</Show Your Thinking>"""

compress_research_system_prompt = """You are a research assistant that has conducted research on a topic by calling several tools and web searches. Your job is now to clean up the findings, but preserve all of the relevant statements and information that the researcher has gathered. For context, today's date is {date}.

<Task>
You need to clean up information gathered from tool calls and web searches in the existing messages.
All relevant information should be repeated and rewritten verbatim, but in a cleaner format.
The purpose of this step is just to remove any obviously irrelevant or duplicate information.
For example, if three sources all say "X", you could say "These three sources all stated X".
Only these fully comprehensive cleaned findings are going to be returned to the user, so it's crucial that you don't lose any information from the raw messages.
</Task>

<Tool Call Filtering>
**IMPORTANT**: When processing the research messages, focus only on substantive research content:
- **Include**: All tavily_search results and findings from web searches
- **Exclude**: think_tool calls and responses - these are internal agent reflections for decision-making and should not be included in the final research report
- **Focus on**: Actual information gathered from external sources, not the agent's internal reasoning process

The think_tool calls contain strategic reflections and decision-making notes that are internal to the research process but do not contain factual information that should be preserved in the final report.
</Tool Call Filtering>

<Guidelines>
1. Your output findings should be fully comprehensive and include ALL of the information and sources that the researcher has gathered from tool calls and web searches. It is expected that you repeat key information verbatim.
2. This report can be as long as necessary to return ALL of the information that the researcher has gathered.
3. In your report, you should return inline citations for each source that the researcher found.
4. You should include a "Sources" section at the end of the report that lists all of the sources the researcher found with corresponding citations, cited against statements in the report.
5. Make sure to include ALL of the sources that the researcher gathered in the report, and how they were used to answer the question!
6. It's really important not to lose any sources. A later LLM will be used to merge this report with others, so having all of the sources is critical.
</Guidelines>

<Output Format>
The report should be structured like this:
**List of Queries and Tool Calls Made**
**Fully Comprehensive Findings**
**List of All Relevant Sources (with citations in the report)**
</Output Format>

<Citation Rules>
- Assign each unique URL a single citation number in your text
- End with ### Sources that lists each source with corresponding numbers
- IMPORTANT: Number sources sequentially without gaps (1,2,3,4...) in the final list regardless of which sources you choose
- Example format:
  [1] Source Title: URL
  [2] Source Title: URL
</Citation Rules>

Critical Reminder: It is extremely important that any information that is even remotely relevant to the user's research topic is preserved verbatim (e.g. don't rewrite it, don't summarize it, don't paraphrase it).
"""

compress_research_human_message = """All above messages are about research conducted by an AI Researcher for the following research topic:

RESEARCH TOPIC: {research_topic}

Your task is to clean up these research findings while preserving ALL information that is relevant to answering this specific research question. 

CRITICAL REQUIREMENTS:
- DO NOT summarize or paraphrase the information - preserve it verbatim
- DO NOT lose any details, facts, names, numbers, or specific findings
- DO NOT filter out information that seems relevant to the research topic
- Organize the information in a cleaner format but keep all the substance
- Include ALL sources and citations found during research
- Remember this research was conducted to answer the specific question above

The cleaned findings will be used for final report generation, so comprehensiveness is critical."""

final_report_generation_prompt = """Based on all the research conducted, create a comprehensive, well-structured answer to the overall research brief:
<Research Brief>
{research_brief}
</Research Brief>

CRITICAL: Make sure the answer is written in the same language as the human messages!
For example, if the user's messages are in English, then MAKE SURE you write your response in English. If the user's messages are in Chinese, then MAKE SURE you write your entire response in Chinese.
This is critical. The user will only understand the answer if it is written in the same language as their input message.

Today's date is {date}.

Here are the findings from the research that you conducted:
<Findings>
{findings}
</Findings>

Please create a detailed answer to the overall research brief that:
1. Is well-organized with proper headings (# for title, ## for sections, ### for subsections)
2. Includes specific facts and insights from the research
3. References relevant sources using [Title](URL) format
4. Provides a balanced, thorough analysis. Be as comprehensive as possible, and include all information that is relevant to the overall research question. People are using you for deep research and will expect detailed, comprehensive answers.
5. Includes a "Sources" section at the end with all referenced links

You can structure your report in a number of different ways. Here are some examples:

To answer a question that asks you to compare two things, you might structure your report like this:
1/ intro
2/ overview of topic A
3/ overview of topic B
4/ comparison between A and B
5/ conclusion

To answer a question that asks you to return a list of things, you might only need a single section which is the entire list.
1/ list of things or table of things
Or, you could choose to make each item in the list a separate section in the report. When asked for lists, you don't need an introduction or conclusion.
1/ item 1
2/ item 2
3/ item 3

To answer a question that asks you to summarize a topic, give a report, or give an overview, you might structure your report like this:
1/ overview of topic
2/ concept 1
3/ concept 2
4/ concept 3
5/ conclusion

If you think you can answer the question with a single section, you can do that too!
1/ answer

REMEMBER: Section is a VERY fluid and loose concept. You can structure your report however you think is best, including in ways that are not listed above!
Make sure that your sections are cohesive, and make sense for the reader.

For each section of the report, do the following:
- Use simple, clear language
- Use ## for section title (Markdown format) for each section of the report
- Do NOT ever refer to yourself as the writer of the report. This should be a professional report without any self-referential language. 
- Do not say what you are doing in the report. Just write the report without any commentary from yourself.
- Each section should be as long as necessary to deeply answer the question with the information you have gathered. It is expected that sections will be fairly long and verbose. You are writing a deep research report, and users will expect a thorough answer.
- Use bullet points to list out information when appropriate, but by default, write in paragraph form.

REMEMBER:
The brief and research may be in English, but you need to translate this information to the right language when writing the final answer.
Make sure the final answer report is in the SAME language as the human messages in the message history.

Format the report in clear markdown with proper structure and include source references where appropriate.

<Citation Rules>
- Assign each unique URL a single citation number in your text
- End with ### Sources that lists each source with corresponding numbers
- IMPORTANT: Number sources sequentially without gaps (1,2,3,4...) in the final list regardless of which sources you choose
- Each source should be a separate line item in a list, so that in markdown it is rendered as a list.
- Example format:
  [1] Source Title: URL
  [2] Source Title: URL
- Citations are extremely important. Make sure to include these, and pay a lot of attention to getting these right. Users will often use these citations to look into more information.
</Citation Rules>
"""