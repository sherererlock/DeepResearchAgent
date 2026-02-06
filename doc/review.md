# Review

## Scope
确认研究范围

输入：AgentInputState（消息列表）
中间状态：AgentState
输出：research_brief

## Supervisor
发起研究

子研究主题可并行研究

## Reseach Agent 
搜索，总结，输出研究结果

输入：研究主题消息
中间状态：ResearcherState
输出：研究结果消息



## 提示词技巧

1. 提示大模型今天的日期
2. 结构化输出，json输出
3. 用markdown语法输入输出
4. 提示大模型首先查询官方网站
5. 提示词需要良好的结构
6. XML 标签隔离与模块化 (XML Tagging & Modularity)
7. 显式思维链引导 (Explicit Chain of Thought)
8. 硬性预算与停止条件 (Hard Constraints & Budgeting)
9. 少样本学习与反例教学 (Few-Shot & Negative Prompting)
10. 跨语言一致性强制 (Cross-Language Consistency)
11. 角色沉浸 (Role Immersion)


## 新的认识

1. research_agent_scope中clarify_with_user会在澄清用户问题时走向End,需要用InMemorySaver在内存中保存之前信息

### 流程图

```mermaid
graph TD
    %% 定义样式
    classDef scope fill:#e1f5fe,stroke:#01579b,stroke-width:2px;
    classDef supervisor fill:#f3e5f5,stroke:#4a148c,stroke-width:2px;
    classDef researcher fill:#fff3e0,stroke:#e65100,stroke-width:2px;
    classDef report fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px;
    classDef startend fill:#fafafa,stroke:#333,stroke-width:2px;

    %% 节点定义
    Start((Start))
    End((End))

    subgraph Scope_Phase [Scope Phase]
        direction TB
        ClarifyNode[Clarify With User]
        UserCheck{"Need Clarification?"}
        BriefNode[Write Research Brief]
    end

    subgraph Supervisor_Phase [Supervisor Phase]
        direction TB
        SupNode[Supervisor Decision]
        SupTools[Supervisor Tools]
        CheckSup{"Action?"}
    end

    subgraph Research_Phase [Research Phase Parallel]
        direction TB
        LLMCall[LLM Call]
        ResCheck{"Action?"}
        ToolNode[Execute Search Tools]
        Compress[Compress Findings]
    end

    subgraph Report_Phase [Report Phase]
        GenReport[Generate Final Report]
    end

    %% 流程连接
    Start --> ClarifyNode
    ClarifyNode --> UserCheck
    
    UserCheck -- Yes --> End
    UserCheck -- No --> BriefNode
    
    BriefNode --> SupNode
    
    SupNode --> CheckSup
    CheckSup -- "ConductResearch (Parallel)" --> LLMCall
    CheckSup -- "Think Tool" --> SupTools
    CheckSup -- "ResearchComplete" --> GenReport
    
    SupTools --> SupNode

    %% Researcher 内部循环
    LLMCall --> ResCheck
    ResCheck -- "Tool Call" --> ToolNode
    ResCheck -- "Done" --> Compress
    ToolNode --> LLMCall
    
    %% Researcher 返回结果给 Supervisor
    Compress -- "ToolMessage (Findings)" --> SupTools

    GenReport --> End

    %% 统一应用样式
    class Start,End startend;
    class ClarifyNode,UserCheck,BriefNode scope;
    class SupNode,SupTools,CheckSup supervisor;
    class LLMCall,ResCheck,ToolNode,Compress researcher;
    class GenReport report;
```

