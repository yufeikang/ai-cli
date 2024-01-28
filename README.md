# AI Tools for chatGPT

This CLI tool allows you to conveniently use chatGPT or new bing in the command line interface. You can chat with it or ask it questions. It can also help you translate text and supports rendering 
markdown in the terminal.

[![PyPI](https://img.shields.io/pypi/v/py-ai-cli?logo=python&logoColor=%23cccccc)](https://pypi.org/project/py-ai-cli)

 [English](README.md) | [中文](README_zh.md) | [日本語](README_ja.md)

## Dependencies

* OPENAI_API_BASE (optional)

If you are unable to access `https://api.openai.com` due to GFW, you can specify another API address using the `OPENAI_API_BASE` environment variable. It is recommended to use this method as it is 
more stable than using a proxy. For information on how to use Cloudflare Workers to set up a proxy, see [Setting up an OpenAI API Proxy with Cloudflare 
Workers](https://github.com/noobnooc/noobnooc/discussions/9).

* OPENAI_API_KEY

You can set the `OPENAI_API_KEY` environment variable or specify it using the `--api-key` parameter. You can also set it using the `ai setting` command.

If you use Azure OpenAI, you can set the `AZURE_OPENAI_API_KEY` or `AZURE_OPENAI_AD_TOKEN` environment variable. and `AZURE_OPENAI_ENDPOINT` for Azure OpenAI endpoint.

* Bard Support

If you use the Bard Bot, you must be logged into Google Bard on at least one browser, which will automatically be detected.

* Bing Cookie

If you use the Bing Bot, you need to set the Bing Cookie. You can set it using the `ai setting` command.

```bash
ai setting --edit bing_cookie="BING_COOKIE.JSON"
```

For information on how to get the cookie, see [Checking Access Required for Bing Bot](https://github.com/acheong08/EdgeGPT#checking-access-required).

## Installation

```bash
pip install py-ai-cli
```

Alternatively, install the latest version:

```bash
pip install git+https://github.com/yufeikang/ai-cli.git    
```

## Configuration

You can now set the API key and API base using the `ai setting` command. Environmental variables and CLI parameters are still valid.

```bash
# View settings
ai setting
# Set settings
ai setting -e
```

## Usage

Use `ai -h` to view all supported commands.

* Automatic Commit Messages

```bash
ai commit
```

![](./asset/video/commit.gif)

* Ask a Question

```bash
ai ask "Hello"
# no stream mode
ai --no-stream ask "Hello"
# help
ai ask --help
# use pre prompt
curl -s https://raw.githubusercontent.com/yufeikang/ai-cli/main/README.md | ai ask --prompt "summary this, how to install"
```

![](./asset/video/ask.gif)

* Translation

```bash
ai translate "Hello"
ai translate "Hello" -t japanese
ai translate -t english -f "file.txt"
echo "Hello" | ai translate -t english
cat "file.txt" | ai translate -t english
```

 ![](./asset/video/translate.gif)

* Chatting

```bash
ai chat
```

 ![](./asset/video/chat.gif)

* Code Review

```bash
ai review
ai review -t develop
ai review -t HEAD~1

```

## Proxy Support

> OPENAI_API_BASE is more stable with a forward proxy. It is recommended.

Support environment variables `HTTP_PROXY` and `HTTPS_PROXY`, or `ALL_PROXY`. You can also specify a proxy using the `--proxy` parameter.

For example:

```bash
export HTTP_PROXY=http://x.x.x.x:xxxx
# or
export HTTPS_PROXY=https://x.x.x.x:xxxx
```

SOCKS5 proxy is also supported, for example:

```bash
export ALL_PROXY=socks5://x.x.x.x:xxxx
```

SOCKS5 proxy requires `pip install pysocks`.

## Additional Information

Please use `ai --help` to view more commands.

## Thanks

![JetBrains Logo (Main) logo](https://resources.jetbrains.com/storage/products/company/brand/logos/jb_beam.svg)

This project is developed using [JetBrains](https://www.jetbrains.com/) products.
