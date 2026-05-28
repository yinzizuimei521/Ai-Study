# AI Partner

一个基于 Streamlit 和大模型 API 的本地 AI 伴侣聊天应用。项目支持自定义伴侣昵称、年龄、性格，支持历史会话保存，也可以加载不同角色的 `skill` 资料，让模型按照指定角色风格进行对话。

## 功能特点

- 使用 Streamlit 构建网页聊天界面
- 通过 OpenAI SDK 调用 DeepSeek 兼容接口
- 支持流式输出回复
- 支持创建、切换和删除历史会话
- 支持保存会话记录到本地 JSON 文件
- 支持自定义伴侣昵称、年龄和性格
- 支持加载本地角色 `skill` Markdown 资料
- 支持设置聊天背景图和侧边栏 Logo

## 项目结构

```text
ai_stduy/
├── ai_partners.py          # Streamlit 主程序
├── README.md               # 项目说明文档
├── background/             # 建议存放聊天背景图片
├── logo/                   # 建议存放 Logo 图片
├── sessions/               # 建议存放本地会话记录
└── skills/                 # 建议存放角色 skill 资料
```

## 环境要求

- Python 3.10 或更高版本
- DeepSeek API Key
- Windows、macOS 或 Linux 均可运行

## 安装依赖

建议先创建虚拟环境：

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

macOS / Linux:

```bash
source .venv/bin/activate
```

安装依赖：

```bash
pip install streamlit openai
```

也可以新建 `requirements.txt`：

```txt
streamlit
openai
```

然后运行：

```bash
pip install -r requirements.txt
```

## 配置 API Key

程序通过环境变量 `DEEPSEEK_API_KEY` 读取 API Key。

Windows PowerShell:

```powershell
$env:DEEPSEEK_API_KEY="你的 DeepSeek API Key"
```

macOS / Linux:

```bash
export DEEPSEEK_API_KEY="你的 DeepSeek API Key"
```

如果希望长期生效，可以把环境变量配置到系统环境变量或 shell 配置文件中。

## 运行项目

在项目根目录执行：

```bash
streamlit run ai_partners.py
```

启动后，浏览器会自动打开本地页面。如果没有自动打开，可以访问终端中显示的本地地址，一般是：

```text
http://localhost:8501
```

## 使用说明

1. 在侧边栏填写伴侣昵称、年龄和性格。
2. 在聊天输入框中输入内容并发送。
3. 点击“新建对话”可以开启新的聊天记录。
4. 在“历史会话”区域可以切换或删除过往会话。
5. 在“角色 skill 加载”区域可以加载指定角色资料，让模型按该角色设定回复。

## 注意事项

- 本项目默认调用 DeepSeek 兼容 OpenAI SDK 的接口。
- 如果更换其他模型服务，需要同步修改 `base_url`、`api_key` 和 `model`。
- 角色 `skill` 内容来自本地 Markdown 文件，请确认相关资料有权公开后再上传。
- 如果背景图、Logo 或角色资料涉及版权，请不要直接公开发布。

