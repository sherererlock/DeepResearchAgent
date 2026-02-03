
## 节点

### LLM decision node
分析当前状态，并根据当前状态决定下一步是执行工具还是提供研究结果。

### Tool Execution Node
当LLM Noe觉得需要更多信息时，执行搜索工具，获取研究数据。

### Research Compression Node
总结和压缩搜索到的研究数据

### Routing Logic


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

