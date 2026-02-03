
## Research Supervisor

- 将研究任务分配给合适数量的子研究代理
- 每个子研究代理负责一个子任务
- 子研究代理有独立分离的上下文窗口
- 分离的上下文窗口更易于代理高质量完成任务

## Prompt 设计

- 指明身份：研究主管
- 指明任务：
  - 使用 ConductResearch 来执行关于用户问题的研究
  - 使用 ResearchComplete 来指出研究完成
- 指明可用工具
  - ConductResearch
  - ResearchComplete
  - think_tool: 反思和计划
     - 关键说明：当发现研究主题可以分解为多个子任务时，必须在一次回复中调用多次ConductResearch来执行并行研究
     - 指明最大的并行研究数量
- 指明思考原则
    - **仔细阅读问题** - 用户需要什么具体信息？  
    - **决定如何委派研究** - 仔细考虑问题并决定如何委派研究。是否有多个可以同时探索的独立方向？  
    - **每次调用 ConductResearch 后，暂停并评估** - 我是否有足够的信息来回答？还缺少什么？ 
- 硬约束
    - 倾向于使用单个代理
    - 当你能自信地回答问题时就停止
    - **限制工具调用** - 如果找不到正确的来源，在 {max_researcher_iterations} 次调用 think_tool 和 ConductResearch 后务必停止

- 展示思考过程

- 扩展规则：给出少量提示

- 善用markdown格式

## State

### SupervisorState
- supervisor_messages
- research_brief
- notes
- research_iterations
- raw_notes

### ConductResearch
这是一个类，被标记为了工具
- research_topic: 研究子主题，必须要被详细描述，至少一段

### ResearchComplete
这是一个类，被标记为了工具



