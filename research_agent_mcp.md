
## 主要思想
用mcp工具来替换之前的tailvy工具


## Filesystem MCP Server

- 文件操作
- 目录管理
- 搜索能力
- 元数据访问

### 工具
- 文件操作：`read_file`, `write_file`, `edit_file`, `read_multiple_files`
- 目录管理：`create_directory`, `list_directory`, `move_file`
- 搜索 & 发现：`search_files`, `get_file_info`, `list_allowed_directories`

## prompt

- 指定角色
- 指定任务
- 工具介绍
- 怎么更好的完成任务
- 硬约束
- 反思指引

## Research Tool

- langchain中mcp工具都是异步执行的
- JSON RPC 协议 
- MultiServerMCPClient
- mcp server在子进程里运行，通过stdio/http交互


## Agent