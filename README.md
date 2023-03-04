# AI Tools for chatGPT

This CLI tool allows you to easily use chatGPT in the command line. You can chat with it and have it help you answer questions. It can also 
translate text for you, and supports rendering markdown in the terminal.

[中文](README.zh.md) | [English](README.md) | [日本語](README.ja.md)

## Quick Start (No installation required)

```bash
curl https://raw.githubusercontent.com/yufeikang/ai-cli/main/ai.py -L -s | python - ask "Hello"
```

## Installation

```bash
curl https://raw.githubusercontent.com/yufeikang/ai-cli/main/ai.py -L -s> /usr/local/bin/ai && chmod +x /usr/local/bin/ai && pip install -U rich 
openai
```

## Usage

Ask questions

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
ai translate "Hello" -t japanese
ai translate -t english -f "file.txt"
echo "Hello" | ai translate -t english
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

Supports the `HTTP_PROXY` and `HTTPS_PROXY` environment variables or `ALL_PROXY`. You can also specify a proxy using the `--proxy` parameter.

For example:

```bash
export HTTP_PROXY=http://x.x.x.x:xxxx
export HTTPS_PROXY=http://x.x.x.x:xxxx
export ALL_PROXY=http://x.x.x.x:xxxx
```

Also, supports SOCKS5 proxy, for example:

```bash
export ALL_PROXY=socks5://x.x.x.x:xxxx
```

SOCKS5 proxy requires `pip install pysocks`.