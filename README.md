

# AI Tools for chatGPT

This CLI tool allows you to easily use chatGPT in the command line. You can chat with it, ask it questions and get answers. It can also help you translate text and supports markdown rendering in the terminal.

 [English](README.md)| [中文](README_zh.md) | [日本語](README_ja.md)

## Dependencies

* OPENAI_API_BASE (optional)

If you cannot access `https://api.openai.com` because of the GFW, you can specify another API address through the `OPENAI_API_BASE` environment variable. It is recommended to use this method, which is more stable 
than using a proxy. You can refer to this article on how to use Cloudflare Workers to set up an OpenAI API proxy: [Using Cloudflare Workers build OpenAI API proxy](https://github.com/noobnooc/noobnooc/discussions/9)

* OPENAI_API_KEY

You can set the `OPENAI_API_KEY` environment variable or specify it through the `--api-key` parameter. You can also set it through the `ai setting` command.

## Installation

```bash
pip install py-ai-cli
```

Or install the latest version.

```bash
pip install git+https://github.com/yufeikang/ai-cli.git    
```

## Configuration

You can now set the API key and API base through the `ai setting` command. Environment variables and CLI parameters are still valid.

```bash
# view setting
ai setting
# set
ai setting -e
```

## Usage

Ask a question

```bash
ai ask "你好"
# no stream mode
ai --no-stream ask "你好"
# help
ai ask --help
```

![](./asset/video/ask.gif)

Translation

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


> Using OPENAI_API_BASE for forward proxy is more stable, which is recommended.

Support `HTTP_PROXY` and `HTTPS_PROXY` or `ALL_PROXY` environment variable. You can also specify a proxy through the `--proxy` parameter.

For example:

```bash
export HTTP_PROXY=http://x.x.x.x:xxxx
# or
export HTTPS_PROXY=https://x.x.x.x:xxxx
```

socks5 proxy is also supported, for example:

```bash
export ALL_PROXY=socks5://x.x.x.x:xxxx
```

Socks5 proxy requires `pip install pysocks`.

## Supplement

Please use `ai --help` to see more commands.