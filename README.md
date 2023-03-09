

# AI Tools for chatGPT

This CLI tool allows you to easily use chatGPT in the command line. You can chat with the AI or ask it questions. It can also translate texts for you, and supports rendering Markdown in the terminal.

[![PyPI](https://img.shields.io/pypi/v/py-ai-cli?logo=python&logoColor=%23cccccc)](https://pypi.org/project/py-ai-cli)

 [English](README.md)| [中文](README_zh.md) | [日本語](README_ja.md)

## Dependencies

* OPENAI_API_BASE (optional)

If you are unable to access `https://api.openai.com` due to the GFW, you can specify a different API address with the `OPENAI_API_BASE` environment variable. We recommend using this method as it is more 
stable than using a proxy.
You can refer to this article for instructions on how to use Cloudflare workers to build an OpenAI API proxy: [Build an OpenAI API Proxy with Cloudflare 
Workers](https://github.com/noobnooc/noobnooc/discussions/9).

* OPENAI_API_KEY

You can set the environment variable `OPENAI_API_KEY`, or specify it through the `--api-key` parameter. You can also set it through the `ai setting` command.

## Installation

```bash
pip install py-ai-cli
```

Or install the latest version

```bash
 pip install git+https://github.com/yufeikang/ai-cli.git    
```

## Configuration

Now you can set the API key and API base with the `ai setting` command. Environment variables and CLI arguments are still valid.

```bash
# View settings
ai setting
# Set
ai setting -e
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

![](./asset/video/ask.gif)

Translation

```bash
ai translate "Hello"
ai translate "Hello" -t japanese
ai translate -t english -f "file.txt"
echo "Hello" | ai translate -t english
cat "file.txt" | ai translate -t english
```

 ![](./asset/video/translate.gif)

Chat

```bash
ai chat
```

 ![](./asset/video/chat.gif)

Code Review

```bash
ai review
ai review -t develop
ai review -t HEAD~1

```

## Chat Presets

You can add custom chat or ask presets that will be included along with your messages. This can be useful to set a different context for different chats or commands.

e.g. you can have a 'unix' preset 
```python
ChatPreset(
            name="unix",
            role="system",
            stream=False,
            no_markdown=True,
            temperature=0.15,
            instruction=f"""
            I want you to act as an experienced devops engineer, software engineer, and unix expert. You are an expert in devops, systems design, unix, linux, vim, shell scripts, python, and more.
            I will ask you to write unix commands and code snippets for me.
            I want you to only reply with the terminal command or code, and nothing else. Do not use markdown. Do not write explanations. Your response should be executable verbatim.
            """,
        ),
```

```
$ ai ask --preset unix "write a bash script that contains an if block, where the true condition is only if an environmental variable is set"

#!/bin/bash

if [ -z "$ENV_VAR" ]; then
  echo "ENV_VAR is not set"
else
  echo "ENV_VAR is set to $ENV_VAR"
fi


Note: Replace ENV_VAR with the name of the environmental variable you want to check.
```

To add your own presets, add a new prompt and model to `models` inside the `Presets` class in `chat_presets.py`


## Proxy Support

> OPENAI_API_BASE Forward proxy is more stable and recommended.

Support the `HTTP_PROXY` and `HTTPS_PROXY` or `ALL_PROXY` environment variables. You can also specify a proxy with the `--proxy` parameter.

For example:

```bash
export HTTP_PROXY=http://x.x.x.x:xxxx
# or
export HTTPS_PROXY=https://x.x.x.x:xxxx
```

SOCKS5 proxies are also supported, for example:

```bash
export ALL_PROXY=socks5://x.x.x.x:xxxx
```

SOCKS5 proxies require `pip install pysocks`.

## Additional Information

Please use `ai --help` to view more commands.