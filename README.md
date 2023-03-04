

# AI Tools for chatGPT

This CLI tool allows you to easily use chatGPT in the command line. You can chat with it, ask it questions, and have it translate text for you. It also supports Markdown rendering in the terminal.

[中文](README.zh.md) | [English](README.md) | [日本語](README.ja.md)

## Quickstart (no installation required)

```
curl https://raw.githubusercontent.com/yufeikang/ai-cli/main/ai_cli/cli.py -L -s | python - ask "Hello"
```

## Dependencies

* OPENAI_API_BASE (optional)

If you are unable to access `https://api.openai.com` due to GFW, you can specify another API address using the `OPENAI_API_BASE` environment variable. It is recommended to use this method, as it is more reliable than using a proxy. You
can use Cloudflare Workers to set up a proxy. See [Using Cloudflare Workers to create an OpenAI API proxy](https://github.com/noobnooc/noobnooc/discussions/9) for more information.

* OPENAI_API_KEY

You can set the `OPENAI_API_KEY` environment variable, or specify it using the `--api-key` parameter.

## Installation

```
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

![](./_/video/ask.gif)

Translate

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

## Proxy support

> OPENAI_API_BASE is more reliable using a forward proxy, so it is recommended.

Supports the `HTTP_PROXY` and `HTTPS_PROXY` or `ALL_PROXY` environment variables. You can also specify a proxy using the `--proxy` parameter.

For example:

```bash
export HTTP_PROXY=http://x.x.x.x:xxxx
# or
export HTTPS_PROXY=https://x.x.x.x:xxxx
```

It also supports SOCKS5 proxies, for example:

```bash
export ALL_PROXY=socks5://x.x.x.x:xxxx
```

SOCKS5 proxies require `pip install pysocks`.