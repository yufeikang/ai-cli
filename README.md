

# AI Tools for chatGPT

This CLI tool allows you to easily use chatGPT in the command line. You can chat with it, ask it questions, and even translate text. It 
also supports rendering Markdown in the terminal.

[![PyPI](https://img.shields.io/pypi/v/py-ai-cli?logo=python&logoColor=%23cccccc)](https://pypi.org/project/py-ai-cli)

[English](README.md)| [中文](README_zh.md) | [日本語](README_ja.md)

## Dependencies

* OPENAI_API_BASE (optional)

If you cannot access `https://api.openai.com` due to GFW, you can specify an alternative API endpoint through the `OPENAI_API_BASE` 
environment variable. We recommend this approach since it is more stable than using proxies. You can follow this article to learn how to 
use Cloudflare Workers to set up a proxy: [Using Cloudflare Workers to proxy OpenAI 
API](https://github.com/noobnooc/noobnooc/discussions/9).

* OPENAI_API_KEY

You can set the `OPENAI_API_KEY` environment variable, or use the `--api-key` parameter. You can also use the `ai setting` command to set
it.

## Installation

```bash
pip install py-ai-cli
```

Or install the latest version

```bash
 pip install git+https://github.com/yufeikang/ai-cli.git    
```

## Configuration

You can use the `ai setting` command to set your API key and API endpoint. The environment variables and command-line arguments still 
work.

```bash
# Check settings
ai setting
# Set settings
ai setting -e
```

## Usage

Ask a question:

```bash
ai ask "Hello"
# no stream mode
ai --no-stream ask "Hello"
# help
ai ask --help
```

![](./asset/video/ask.gif)

Translation:

```bash
ai translate "Hello"
ai translate "Hello" -t japanese
ai translate -t english -f "file.txt"
echo "Hello" | ai translate -t english
cat "file.txt" | ai translate -t english
```

 ![](./asset/video/translate.gif)

Chat:

```bash
ai chat
```

 ![](./asset/video/chat.gif)

## Proxy Support

> OPENAI_API_BASE Using a forward proxy is more stable, and we recommend it.

Supports the `HTTP_PROXY` and `HTTPS_PROXY` environment variables or `ALL_PROXY`. You can also use the `--proxy` parameter to specify a 
proxy.

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

Use `ai --help` to view more commands.