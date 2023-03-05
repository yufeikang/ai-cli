

# AI Tools for chatGPT

This CLI tool allows you to conveniently use chatGPT in the command line. You can chat with it, ask questions, and even have it translate text. It also supports rendering Markdown in the terminal.

[English](README.md) | [中文](README.zh.md) | [日本語](README.ja.md)

## Dependencies

* OPENAI_API_BASE (Optional)

If you're unable to access `https://api.openai.com` due to the Great Firewall of China, you can specify an alternate API endpoint using the `OPENAI_API_BASE` environment variable. We recommend using this method as 
it is more stable than traditional proxies. Here's an article that explains how to set up a Cloudflare Workers proxy: [Using Cloudflare Workers to Proxy OpenAI 
API](https://github.com/noobnooc/noobnooc/discussions/9).

* OPENAI_API_KEY

You can set the `OPENAI_API_KEY` environment variable or specify it using the `--api-key` argument. You can also set it using the `ai setting` command.

## Installation

```bash
pip install py-ai-cli
```

Or install the latest version:

```bash
pip install git+https://github.com/yufeikang/ai-cli.git    
```

## Configuration

You can use the `ai setting` command to set your `api-key` and `api-base`. You can also use environment variables and CLI arguments.

```bash
# view settings
ai setting
# set settings
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

Chatting

```bash
ai chat
```

![](./asset/video/chat.gif)

## Proxy Support

> OPENAI_API_BASE Forward proxy is recommended.

Supports the `HTTP_PROXY` and `HTTPS_PROXY` environment variables, or the `ALL_PROXY` variable. You can also specify a proxy using the `--proxy` argument.

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

SOCKS5 proxies require the installation of `pip install pysocks`

## Additional Information

Use `ai --help` for more commands.