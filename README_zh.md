# chatGPT 的 AI 工具

这个 CLI 工具让你可以轻松地在命令行中使用 chatGPT。你可以和 AI 
聊天或者问它问题。它还可以为你翻译文本，并且支持在终端中渲染 Markdown。

[![PyPI](https://img.shields.io/pypi/v/py-ai-cli?logo=python&logoColor=%23cccccc)](https://pypi.org/proj
ect/py-ai-cli)

[English](README.md) | [中文](README_zh.md) | [日本語](README_ja.md)

## 依赖

* OPENAI_API_BASE（可选）

如果你由于 GFW 的原因无法访问 `https://api.openai.com`，你可以使用 `OPENAI_API_BASE` 环境变量指定不同的 
API 地址。我们建议使用这种方法，因为它比使用代理更加稳定。你可以参考这篇文章了解如何使用 Cloudflare 的 
Workers 来构建一个 OpenAI API 代理：[使用 Cloudflare Workers 构建 OpenAI API 
代理](https://github.com/noobnooc/noobnooc/discussions/9)。

* OPENAI_API_KEY

你可以设置环境变量 `OPENAI_API_KEY` 或者使用 `--api-key` 参数指定它。你还可以使用 `ai setting` 
命令来设置它。

为了构建一个新的可执行文件，你需要安装 (https://pdm.fming.dev/latest/)。

## 安装

`py_ai_cli` 是一个独立的可执行文件。将它添加到你的路径中，就可以从任何地方访问 `ai`。
```bash
ln -s $(pwd)/py_ai_cli /usr/local/bin/ai
```


要应用更新并构建一个新的可执行文件，请运行 `run_build.sh`。

## 配置

现在，你可以使用 `ai setting` 命令设置 API 键和 API base。环境变量和命令行参数仍然有效。 

```bash
# 查看设置
ai setting
# 设置
ai setting -e
```

## 用法

问问题

```bash
ai ask "你好"
# 无流模式
ai --no-stream ask "你好"
# 帮助
ai ask --help
```

![](./asset/video/ask.gif)

翻译

```bash
ai translate "你好"
ai translate "你好" -t english
ai translate -t japanese -f "file.txt"
echo "你好" | ai translate -t english
cat "file.txt" | ai translate -t english
```

![](./asset/video/translate.gif)

聊天

```bash
ai chat
```

![](./asset/video/chat.gif)

代码审查

```bash
ai review
ai review -t develop
ai review -t HEAD~1

```

## 代理支持

> OPENAI_API_BASE 的前向代理更加稳定，推荐使用。

支持 `HTTP_PROXY` 和 `HTTPS_PROXY` 或者 `ALL_PROXY` 环境变量。你还可以使用 `--proxy` 参数指定一个代理。

例如：

```bash
export HTTP_PROXY=http://x.x.x.x:xxxx
# 或者
export HTTPS_PROXY=https://x.x.x.x:xxxx
```

SOCKS5 代理也被支持，例如：

```bash
export ALL_PROXY=socks5://x.x.x.x:xxxx
```

SOCKS5 代理需要 `pip install pysocks`。

## 其他信息

请使用 `ai --help` 查看更多命令。