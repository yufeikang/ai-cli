

# chatGPTのAIツール

このCLIツールを使用すると、コマンドラインで簡単にchatGPTを使用できます。会話したり、質問に答えてもらったり、テキストを翻訳したりできます。また、ター
ミナルでのMarkdownのレンダリングをサポートしています。

[中文](README.zh.md) | [English](README.md) | [日本語](README.ja.md)

## クイックスタート（インストール不要）

```bash
curl https://raw.githubusercontent.com/yufeikang/ai-cli/main/ai.py -L -s | python - ask "Hello"
```

## インストール

```bash
curl https://raw.githubusercontent.com/yufeikang/ai-cli/main/ai.py -L -s> /usr/local/bin/ai && chmod +x /usr/local/bin/ai && pip install -U rich 
openai
```

## 使い方

質問する

```bash
ai ask "Hello"
# no stream mode
ai --no-stream ask "Hello"
# help
ai ask --help
```

![](./_/video/ask.gif)

翻訳

```bash
ai translate "こんにちは"
ai translate "こんにちは" -t chinese
ai translate -t english -f "file.txt"
echo "こんにちは" | ai translate -t english
cat "file.txt" | ai translate -t english
```

 ![](./_/video/translate.gif)

チャット

```bash
ai chat
```

 ![](./_/video/chat.gif)

## 依存関係

```bash
pip install rich openai
```

* プロキシーサポート

環境変数`HTTP_PROXY`および`HTTPS_PROXY`または`ALL_PROXY`がサポートされています。プロキシを指定するには、`--proxy`パラメーターを使用できます。

例：

```bash
export HTTP_PROXY=http://x.x.x.x:xxxx
export HTTPS_PROXY=http://x.x.x.x:xxxx
export ALL_PROXY=http://x.x.x.x:xxxx
```

SOCKS5プロキシもサポートされています。例えば：

```bash
export ALL_PROXY=socks5://x.x.x.x:xxxx
```

SOCKS5プロキシを使用するには、`pip install pysocks`をインストールする必要があります。