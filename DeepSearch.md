
## 数据类

### State类
AgentInputState:
保存meesages数据

AgentState:

research_brief: 研究简要报告
supervisor_messages: 与监督智能体交换的消息
raw_notes: 原始研究笔记
notes: 结构化研究笔记
final_report: 最终研究报告

### 结构化输出类

ClarifyWithUser:
need_clarification: 是否需要澄清
question: 澄清问题
verification: 确认信息

ResearchQuestion:
research_brief: 研究问题


## 工作图

### 节点clarify_with_user:
主要用来与用户交互，询问是否需要澄清问题，以及需要澄清的问题。
结构化输出为ClarifyWithUser
两个分支：
1. need_clarification为True时，暂时直接去END。
2. need_clarification为False时，write_research_brief。
更新AgentState的research_brief。

### 节点research_question:
主要用来生成研究问题。
结构化输出为ResearchQuestion

### 分支

START -> clarify_with_user
clarify_with_user -> research_question
research_question -> END
