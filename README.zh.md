# AI Tools for chatGPT

这个cli工具可以让你方便的在命令行中使用chatGPT。你可以和他聊天，也可以让他帮你回答问题。也可以帮你翻译文本。并且支持markdown在终端中的渲染。

[中文](README.zh.md) | [English](README.md) | [日本語](README.ja.md)

## 快速体验(无需安装)

```bash
curl https://raw.githubusercontent.com/yufeikang/ai-cli/main/ai.py -L -s | python - ask "你好"
```

## 安装

```bash
curl https://raw.githubusercontent.com/yufeikang/ai-cli/main/ai.py -L -s> /usr/local/bin/ai && chmod +x /usr/local/bin/ai && pip install -U rich openai
```

## 使用

问问题

```bash
ai ask "你好"
# no stream mode
ai --no-stream ask "你好"
# help
ai ask --help
```

![](./_/video/ask.gif)

翻译

```bash
ai translate "你好"
ai translate "你好" -t japanese
ai translate -t english -f "file.txt"
echo "你好" | ai translate -t english
cat "file.txt" | ai translate -t english
```

 ![](./_/video/translate.gif)

聊天

```bash
ai chat
```

 ![](./_/video/chat.gif)

## 依赖

```bash
pip install rich openai
```

* 代理支持

支持环境变量`HTTP_PROXY`和`HTTPS_PROXY` 或者 `ALL_PROXY`。也可以通过`--proxy`参数指定代理。

例如：

```bash
export HTTP_PROXY=http://x.x.x.x:xxxx
export HTTPS_PROXY=http://x.x.x.x:xxxx
export ALL_PROXY=http://x.x.x.x:xxxx
```

也支持socks5代理，例如：

```bash
export ALL_PROXY=socks5://x.x.x.x:xxxx
```

socks5代理需要安装`pip install pysocks`
