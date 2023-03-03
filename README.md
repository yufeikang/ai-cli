

# AI Tools for chatGPT

> This CLI tool allows you to easily use chatGPT in the command line. You can chat with it, ask it to answer questions and translate text. It also 
supports markdown rendering in the terminal.

[中文](README.zh.md) | [English](README.md) | [日本語](README.ja.md)

## Quick Start ( No Installation Required )

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

 ![]("./_/video/ask.gif")
 
Translation

```bash
ai translate "Hello"
ai translate "Hello" -t japanese
ai translate -t english -f "file.txt"
echo "Hello" | ai translate -t english
cat "file.txt" | ai translate -t english
```

 ![]("./_/video/translate.gif")

Chat

```bash
ai chat
```

 ![]("./_/video/chat.gif")

## Dependencies

```bash
pip install rich openai
```
