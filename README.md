

# AI Tools for chatGPT

This CLI tool allows you to easily use chatGPT in the command line. You can chat with it, ask it questions, and also have it 
translate text. It also supports markdown rendering in the terminal.

[![PyPI](https://img.shields.io/pypi/v/py-ai-cli?logo=python&logoColor=%23cccccc)](https://pypi.org/project/py-ai-ali)

[English](README.md) | [中文](README_zh.md) | [日本語](README_ja.md)

## Dependencies

* OPENAI_API_BASE (Optional)

If you are unable to access `https://api.openai.com` due to the Great Firewall of China, you can specify an alternative API address 
via the `OPENAI_API_BASE` environment variable. This is the recommended method as it is more stable compared to using proxies. You 
can refer to this article on how to set up an OpenAI API proxy using Cloudflare workers: [Using Cloudflare Workers to Setup a OpenAI 
API Proxy](https://github.com/noobnooc/noobnooc/discussions/9)

* OPENAI_API_KEY

You can set the `OPENAI_API_KEY` environment variable, or use the `--api-key` argument to specify it. You can also use the `ai 
setting` command to set it.

## Installation

```bash
pip install py-ai-cli
```

Or install the latest version

```bash
 pip install git+https://github.com/yufeikang/ai-cli.git    
```

## Configuration

Now you can use the `ai setting` command to set your API key and API base. Environmental variables and CLI arguments are still valid.

```bash
# show current setting
ai setting
# set it up
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

![](./assets/video/ask.gif)

Translation

```bash
ai translate "你好"
ai translate "你好" -t japanese
ai translate -t english -f "file.txt"
echo "你好" | ai translate -t english
cat "file.txt" | ai translate -t english
```

![](./assets/video/translate.gif)

Chat

```bash
ai chat
```

![](./assets/video/chat.gif)

## Proxy Support

> OPENAI_API_BASE with forwarding proxy is recommended.

It supports the `HTTP_PROXY` and `HTTPS_PROXY`, or `ALL_PROXY` environment variables. You can also specify the proxy via the 
`--proxy` argument.

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

SOCKS5 proxies require an installation of `pip install pysocks`.

## Additional Information

Please refer to `ai --help` for more commands.