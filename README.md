

# AI Tools for chatGPT

This CLI tool allows you to conveniently use chatGPT in the command line. You can chat with it, ask it questions, and translate text. It also supports rendering Markdown in the terminal.

[中文](README.zh.md) | [English](README.md) | [日本語](README.ja.md)

## Dependencies

* OPENAI_API_BASE (optional)

If you cannot access `https://api.openai.com` due to the GFW, you can specify an alternative API address using the `OPENAI_API_BASE` environment variable. It is recommended to use this method, which is more reliable
than using proxies. Please refer to this article for how to use Cloudflare Workers to set up a proxy: [使用Cloudflare Workers搭建OpenAI API代理](https://github.com/noobnooc/noobnooc/discussions/9).

* OPENAI_API_KEY

You can set the `OPENAI_API_KEY` environment variable, or specify it using the `--api-key` parameter. You can also set it using the `ai setting` command.

## Installation

```bash
pip install https://github.com/yufeikang/ai-cli/releases/download/v0.0.1/ai_cli-0.0.1-py3-none-any.whl
```

## Setup

Now you can use the `ai setting` command to set your API key and API base. Environment variables and CLI parameters are still valid.

```bash
# view settings
ai setting
# set settings
ai setting -e
```

## Usage

Ask questions

```bash
ai ask "你好"
# no stream mode
ai --no-stream ask "你好"
# help
ai ask --help
```

![](./asset/video/ask.gif)

Translate

```bash
ai translate "你好"
ai translate "你好" -t japanese
ai translate -t english -f "file.txt"
echo "你好" | ai translate -t english
cat "file.txt" | ai translate -t english
```

 ![](./asset/video/translate.gif)

Chat

```bash
ai chat
```

 ![](./asset/video/chat.gif)

## Proxy Support

> Using a forward proxy for `OPENAI_API_BASE` is more stable, and recommended.

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

You need to install `pip install pysocks` for SOCKS5 proxies.

## Additional Information

Please use `ai --help` to see more commands.