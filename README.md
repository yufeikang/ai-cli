

# AI Tools for chatGPT

This CLI tool allows you to easily use chatGPT in the command line. You can chat with it, ask it questions, and use it to translate text. It also supports rendering Markdown
in the terminal.

[![PyPI](https://img.shields.io/pypi/v/py-ai-cli?logo=python&logoColor=%23cccccc)](https://pypi.org/project/py-ai-cli)

[English](README.md) | [中文](README_zh.md) | [日本語](README_ja.md)

## Dependencies

* OPENAI_API_BASE (optional)

If you are unable to access `https://api.openai.com` because of the GFW, you can specify a different API address using the `OPENAI_API_BASE` environment variable. We 
recommend using this method, as it is more stable than using a proxy. You can find instructions for using Cloudflare Workers to set up a proxy at 
(https://github.com/noobnooc/noobnooc/discussions/9).

* OPENAI_API_KEY

You can set the `OPENAI_API_KEY` environment variable, or specify it using the `--api-key` argument. You can also set it using the `ai setting` command.

## Installation

```bash
pip install py-ai-cli
```

or install the latest version:

```bash
 pip install git+https://github.com/yufeikang/ai-cli.git    
```

## Configuration

You can now use the `ai setting` command to set the API key and API base. Environment variables and command-line arguments also work.

```bash
# view settings
ai setting
# set
ai setting -e
```

## Usage

Use `ai -h` to view all the supported commands.

* Generate commit messages

```bash
ai commit
```

 ![](./asset/video/commit.gif)

* Ask a question

```bash
ai ask "你好"
# no stream mode
ai --no-stream ask "你好"
# help
ai ask --help
# use pre prompt
curl -s https://raw.githubusercontent.com/yufeikang/ai-cli/main/README.md | ai ask --prompt "summary this, how to install"
```

![](./asset/video/ask.gif)

* Translate

```bash
ai translate "你好"
ai translate "你好" -t japanese
ai translate -t english -f "file.txt"
echo "你好" | ai translate -t english
cat "file.txt" | ai translate -t english
```

 ![](./asset/video/translate.gif)

* Chat

```bash
ai chat
```

 ![](./asset/video/chat.gif)

* Code review

```bash
ai review
ai review -t develop
ai review -t HEAD~1

```

## Proxy Support

> OPENAI_API_BASE Using a forward proxy is more stable, we recommend using it.

Supports the `HTTP_PROXY` and `HTTPS_PROXY` or `ALL_PROXY` environment variables. You can also specify a proxy using the `--proxy` parameter.

For example:

```bash
export HTTP_PROXY=http://x.x.x.x:xxxx
# or
export HTTPS_PROXY=https://x.x.x.x:xxxx
```

Also supports SOCKS5 proxies, for example:

```bash
export ALL_PROXY=socks5://x.x.x.x:xxxx
```

SOCKS5 proxies require `pip install pysocks`

## Additional Information

Please use `ai --help` to view more commands.