
# chatGPTのAIツール

> このCLIツールを使用すれば、コマンドライン上で簡単にchatGPTを使用できます。AIとチャットをすることができ、質問の回答を支援することもできま
す。また、テキストの翻訳もサポートしています。さらに、マークダウンのテキストも終端でレンダリングすることができます。

[中文](README.zh.md) | [English](README.md) | [日本語](README.ja.md)

## クイックスタート（インストール不要）

```bash
curl https://raw.githubusercontent.com/yufeikang/ai-cli/main/ai.py -L -s | python - ask "こんにちは"
```

## インストール

```bash
curl https://raw.githubusercontent.com/yufeikang/ai-cli/main/ai.py -L -s> /usr/local/bin/ai && chmod +x /usr/local/bin/ai && pip install -U rich 
openai
```

## 使い方

質問する

```bash
ai ask "こんにちは"
# no stream mode
ai --no-stream ask "こんにちは"
# help
ai ask --help
```

 ![]("./_/video/ask.gif")

翻訳

```bash
ai translate "こんにちは"
ai translate "こんにちは" -t japanese
ai translate -t english -f "file.txt"
echo "こんにちは" | ai translate -t english
cat "file.txt" | ai translate -t english
```

 ![]("./_/video/translate.gif")

チャット

```bash
ai chat
```

 ![]("./_/video/chat.gif")

## 必要条件

```bash
pip install rich openai
```

 上記の内容を日本語に翻訳してください。
