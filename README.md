

# AI Tools for chatGPT

This CLI tool allows you to easily chat with chatGPT in the command line. You can chat with it, ask questions, and even translate text. It also 
supports Markdown rendering in the terminal.

[中文](README.zh.md) | [English](README.md) | [日本語](README.ja.md)

## Quick test (No installation required)

```bash
curl https://raw.githubusercontent.com/yufeikang/ai-cli/main/ai.py -L -s | python - ask "Hello"
```

## Dependencies

* Install dependencies

```bash
pip install rich openai
```

* OPENAI_API_BASE (optional)

If you can't access `https://api.openai.com` due to GFW in China, you can specify another API address via the `OPENAI_API_BASE` environment 
variable. It's recommended to use this method as it's more stable than using proxy servers. You can refer to 
(https://github.com/noobnooc/noobnooc/discussions/9) for setting up a proxy server using Cloudflare Workers.

* OPENAI_API_KEY

You can set the `OPENAI_API_KEY` environment variable or specify it via the `--api-key` parameter.

## Installation

```bash
curl https://raw.githubusercontent.com/yufeikang/ai-cli/main/ai.py -L -s > /usr/local/bin/ai && chmod +x /usr/local/bin/ai && pip install -U rich 
openai
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

![](./_/video/ask.gif)

Translation

```bash
ai translate "Hello"
ai translate "你好" -t japanese
ai translate -t english -f "file.txt"
echo "Hello" | ai translate -t chinese
cat "file.txt" | ai translate -t chinese
```

![](./_/video/translate.gif)

Chat

```bash
ai chat
```

![](./_/video/chat.gif)

## Proxy support

> OPENAI_API_BASE is more stable for forwarding proxies, it is recommended to use this method.

Supports environment variables `HTTP_PROXY` and `HTTPS_PROXY` or `ALL_PROXY`. You can also specify a proxy via the `--proxy` parameter.

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

socks5 proxies require the installation of `pip install pysocks`.