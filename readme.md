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

[0202images.py](src/agents/02images.py) 能运行

##
