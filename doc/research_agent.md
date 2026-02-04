

## 提示词

1. Think like The Agent
- 仔细阅读问题
- 先从宽泛的搜索开始
- 每次搜索完成后，先观察和评估结果
- 再根据评估结果执行详细的搜索

2. Concrete Heuristics（防止过量的循环搜索）
用硬约束来防止LLM Node过度调用搜索工具。
- 当LLM判读能自信的回答问题时，不再调用搜索工具。
- 预算限制：简单的问题2-3词搜索，复杂的问题4-5词搜索。
- 总次数限制：LLM Node调用搜索工具的总次数不能超过5次。

## State 

ResearcherState(TypedDict):
- researcher_messages:消息列表
- tool_call_iterations: 搜索工具调用次数
- research_topic: 研究主题
- compressed_research: 压缩后的研究数据
- raw_notes: 原始研究笔记

ResearcherOutputState(TypedDict)
- compressed_research:压缩后的搜索数据
- raw_notes：原始搜索笔记
- researcher_messages: 消息列表

## Schema

ClarifyWithUser:
need_clarification: 是否需要澄清
question: 澄清问题
verification: 确认信息

ResearchQuestion:
research_brief: 研究问题

Summary:
summary: 研究总结
key_excerpts: 研究中的关键片段

## Research Tool

- 用 tavily 搜索工具
- 去掉url重复的搜索结果
- 使用大模型总结页面结果
- 格式化总结结果
    - 每个页面的总结结果格式为：
        - 页面标题
        - 页面url
        - 页面内容总结

InjectedToolArg:用于标记那些“不需要由大模型（LLM）生成，而是由代码在运行时自动注入”的工具参数

### tavily_search

### think_tool
巧妙之处在于，think_tool利用工具的说明
When to use:
- After receiving search results: What key information did I find?
- Before deciding next steps: Do I have enough to answer comprehensively?
- When assessing research gaps: What specific information am I still missing?
- Before concluding research: Can I provide a complete answer now?
指导大模型在合适的时机使用think_tool，生成反思结果，然后直接返回这个反思结果。
这个tool除了返回反思结果，什么都没有做
如果按照常理，这个实现肯定会被做成一个Node

## Research Agent

### 节点

#### LLM decision node
分析当前状态，并根据当前状态决定下一步是执行工具还是提供研究结果。

#### Tool Execution Node
当LLM Noe觉得需要更多信息时，执行搜索工具，获取研究数据。

#### Research Compression Node
总结和压缩搜索到的研究数据

#### Routing Logic

## Context Engineering Strategy

1. 总结网页信息
- 结构化输出关键信息和片段
- 过滤掉无关信息，保留事实细节
- 长文压缩为焦点总结
- 为之后的验证保留引用
2. 压缩研究总结信息
- 总结多个搜索结合，结合为连贯的信息
- 为之后的细节分析保留原始文本，并且也维护压缩后的总结信息
- 减少后续 LLM 调用所需的token使用量
- 保留报告撰写所需的重要信息
3. 小心的压缩信息
- 在压缩阶段明确重述原始研究主题
- 提醒模型保留与特定问题相关的所有信息
- 强调全面的研究结果对于最终报告的生成至关重要
- 防止在压缩阶段出现任务偏移

4. token输出策略

## 工作流程

llm_call 节点分析当前状态，生成搜索查询。
工具节点执行搜索工具，获取研究数据。
llm_call 节点分析当前状态，生成反思结果。
工具节点执行think_tool，生成反思结果
llm_call 节点分析当前状态，决定进行tool_node或者compress_research。
compress_research节点总结和压缩搜索到的研究数据

## 评估

智能体通过自主调用工具来完成任务。
让我们思考一下工具调用循环调整不当的后果：

- 提前终止：智能体在任务尚未完成时就停止调用工具。
- 无限循环：智能体始终对其信息状态不满意。

第一种故障模式会导致智能体收集的信息不足。在深度研究的背景下，最终结果可能过于浅显。第二种故障模式会导致智能体使用过多的令牌。在深度研究的背景下，无关信息可能会影响结果。
我们已经调整了提示信息以避免这些问题。但是，让我们设置一个玩具评估数据集，以便轻松测试智能体的决策能力。