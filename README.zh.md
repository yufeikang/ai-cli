# AI Tools for chatGPT

这个cli工具可以让你方便的在命令行中使用chatGPT。你可以和他聊天，也可以让他帮你回答问题。也可以帮你翻译文本。并且支持markdown在终端中的渲染。

[中文](README.zh.md) | [English](README.md) | [日本語](README.ja.md)

## 依赖

* OPENAI_API_BASE (可选)

如果因为GFW的原因，你无法访问`https://api.openai.com`，你可以通过`OPENAI_API_BASE`环境变量指定其他的api地址。建议使用这种方式。它比使用代理的方式更加稳定。
如何使用cloudflare的workers来搭建代理，可以参考这篇文章：[使用Cloudflare Workers搭建OpenAI API代理](https://github.com/noobnooc/noobnooc/discussions/9)

* OPENAI_API_KEY

可以设定环境变量`OPENAI_API_KEY`，也可以通过`--api-key`参数指定。也可通过`ai setting`命令来设置。

## 安装

```bash
pip install https://github.com/yufeikang/ai-cli/releases/download/v0.0.1/ai_cli-0.0.1-py3-none-any.whl
```

或者安装最新版本

```bash
 pip install git+https://github.com/yufeikang/ai-cli.git    
```

## 设定

现在你可以通过`ai setting`命令来设置api key和api base了。同时环境变量和cli参数依然有效。

```bash
# 查看setting
ai setting
# 设置
ai setting -e
```

## 使用

问一个问题

```bash
ai ask "你好"
# no stream mode
ai --no-stream ask "你好"
# help
ai ask --help
```

![](./asset/video/ask.gif)

翻译

```bash
ai translate "你好"
ai translate "你好" -t japanese
ai translate -t english -f "file.txt"
echo "你好" | ai translate -t english
cat "file.txt" | ai translate -t english
```

 ![](./asset/video/translate.gif)

聊天

```bash
ai chat
```

 ![](./asset/video/chat.gif)

## 代理支持

> OPENAI_API_BASE 正向代理方式更加稳定，推荐使用。

支持环境变量`HTTP_PROXY`和`HTTPS_PROXY` 或者 `ALL_PROXY`。也可以通过`--proxy`参数指定代理。

例如：

```bash
export HTTP_PROXY=http://x.x.x.x:xxxx
# or
export HTTPS_PROXY=https://x.x.x.x:xxxx
```

也支持socks5代理，例如：

```bash
export ALL_PROXY=socks5://x.x.x.x:xxxx
```

socks5代理需要安装`pip install pysocks`

## 补充

请用`ai --help`来查看更多命令。
