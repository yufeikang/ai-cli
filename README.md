

# AI Tools for chatGPT

This CLI tool allows you to easily use chatGPT in the command line. You can chat with it, ask it questions, and even have it translate text. It also supports markdown rendering in the terminal.

[中文](README.zh.md) | [English](README.md) | [日本語](README.ja.md)

## Quick Start (No installation required)

```bash
curl https://raw.githubusercontent.com/yufeikang/ai-cli/main/src/ai_cli/cli.py -L -s | python - ask "Hello"
```

## Dependencies

* OPENAI_API_BASE (optional)

If you are unable to access `https://api.openai.com` due to the Great Firewall of China, you can specify another API address via the `OPENAI_API_BASE` environment variable. This is recommended over using a proxy for 
stability.
To use Cloudflare Workers to set up a proxy, you can refer to this article: [Using Cloudflare Workers as an OpenAI API proxy](https://github.com/noobnooc/noobnooc/discussions/9)

* OPENAI_API_KEY

You can set the `OPENAI_API_KEY` environment variable, or pass it in as a `--api-key` argument.

## Installation

```bash
pip install https://github.com/yufeikang/ai-cli/releases/download/v0.0.1/ai_cli-0.0.1-py3-none-any.whl
```

## Usage

Ask a question

```bash
ai ask "Hello"
# no stream mode
ai --no-stream ask "Hello"
# help
ai ask --help
```

![](./asset/video/ask.gif)

Translation

```bash
ai translate "Hello"
ai translate "Hello" -t japanese
ai translate -t english -f "file.txt"
echo "Hello" | ai translate -t english
cat "file.txt" | ai translate -t english
```

 ![](./asset/video/translate.gif)

Chat

```bash
ai chat
```

 ![](./asset/video/chat.gif)

## Proxy Support

> OPENAI_API_BASE is recommended over using a reverse proxy.

Support for `HTTP_PROXY` and `HTTPS_PROXY` or `ALL_PROXY` environment variables. You can also specify a proxy via the `--proxy` argument.

For example:

```bash
export HTTP_PROXY=http://x.x.x.x:xxxx
# or
export HTTPS_PROXY=https://x.x.x.x:xxxx
```

It also supports socks5 proxies, for example:

```bash
export ALL_PROXY=socks5://x.x.x.x:xxxx
```

socks5 proxies require `pip install pysocks`