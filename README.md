# Learn Agent Framework

记录在学习agent framework 时，示例代码的汇总。发现这个文档的示例代码真的是一言难尽。环境变量对不上，包版本对不上，代码根本跑不起来。所以就自己动手写一些示例代码，方便以后回顾。如果我的记录有问题，欢迎指正修复。

## 运行

1. 用 vscode 打开代码根目录
2. F1 选择 rebuild container and open in container
3. 运行 `uv sync` 
4. 运行 `az login` 网页登陆后，选择你的订阅
5. 运行 `uv run src/agents/02images.py` 运行示例代码


## 示例代码

[quick-start.py](src/quick-start.py) 无法运行，import的包和代码里都有问题，无法运行

[01run-a-agent.py](src/agents/01run-a-agent.py) 能运行，但是 image 图片的网站已过期，无法运行图片解析部分

[02images.py](src/agents/02images.py) 能运行

[03multi_turn_conversation.py](src/agents/03multi_turn_conversation.py) 能运行

[04function_tools.py](src/agents/04function_tools.py) 能运行

[05function_tools_approvals.py](src/agents/05function_tools_approvals.py) 将 agent 替换成 04 中的azure agent 后运行成功

[06structured_output.py](src/agents/06structured_output.py) 能运行

[07agent_as_function_tool.py](src/agents/07agent_as_function_tool.py) 能运行

[08agent_as_mcp_tool.py](src/agents/08agent_as_mcp_tool.py) 能运行，但是不知道如何验证运行是否正常

[09chat_with_web_knowledge.py](src/agents/09chat_with_web_knowledge.py) 能运行

[10chat_with_db_knowledge.py](src/agents/10chat_with_db_knowledge.py) 能运行

[11chat_with_vector_store_knowledge.py](src/agents/11chat_with_vector_store_knowledge.py) 能运行

[12custom_prompting.py](src/agents/12custom_prompting.py) 能运行

##
