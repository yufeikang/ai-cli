

# AI Tools for chatGPT

This CLI tool allows you to easily use chatGPT in the command line. You can chat with it, ask it questions, and get text translations. It also 
supports rendering Markdown in the terminal.

[中文](README.zh.md) | [English](README.md) | [日本語](README.ja.md)

## Quick Start (No Installation Required)

```bash
curl https://raw.githubusercontent.com/yufeikang/ai-cli/main/ai.py -L -s | python - ask "hello"
```

## Installation

```bash
curl https://raw.githubusercontent.com/yufeikang/ai-cli/main/ai.py -L -s> /usr/local/bin/ai && chmod +x /usr/local/bin/ai && pip install -U rich 
openai
```

## Usage

Ask Questions

```bash
ai ask "hello"
# no stream mode
ai --no-stream ask "hello"
# help
ai ask --help
```

![](./_/video/ask.gif)

Translation

```bash
ai translate "hello"
ai translate "hello" -t japanese
ai translate -t english -f "file.txt"
echo "hello" | ai translate -t english
cat "file.txt" | ai translate -t english
```

 ![](./_/video/translate.gif)

Chat

```bash
ai chat
```

 ![](./_/video/chat.gif)

## Dependencies

```bash
pip install rich openai
```

* Proxy Support

Supports `HTTP_PROXY` and `HTTPS_PROXY` or `ALL_PROXY` environment variables. You can also specify a proxy with the `--proxy` parameter.

For example:

```bash
export HTTP_PROXY=http://x.x.x.x:xxxx
export HTTPS_PROXY=http://x.x.x.x:xxxx
export ALL_PROXY=http://x.x.x.x:xxxx
```

SOCKS5 proxies are also supported, for example:

```bash
export ALL_PROXY=socks5://x.x.x.x:xxxx
```

SOCKS5 proxies require `pip install pysocks`.

* OPENAI_API_KEY

You can set the `OPENAI_API_KEY` environment variable, or pass it in with the `--api-key` parameter.