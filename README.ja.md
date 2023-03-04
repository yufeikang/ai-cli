

# AIツールのチャットGPT

このCLIツールは、コマンドラインでchatGPTを簡単に使用できるようにするものです。チャットすることも、質問に答えてもらうこともできます。また、
テキストの翻訳も手伝ってくれます。そして、ターミナルでのマークダウンのレンダリングもサポートしています。

[中国語](README.zh.md) | [英語](README.md) | [日本語](README.ja.md)

## クイックスタート（インストールなし）

```bash
curl https://raw.githubusercontent.com/yufeikang/ai-cli/main/ai.py -L -s | python - ask "こんにちは"
```

## インストール

```bash
curl https://raw.githubusercontent.com/yufeikang/ai-cli/main/ai.py -L -s> /usr/local/bin/ai && chmod +x /usr/local/bin/ai && pip install -U rich 
openai
```

## 使用法

質問する

```bash
ai ask "こんにちは"
# サポートされていないストリームモード
ai --no-stream ask "こんにちは"
# ヘルプ
ai ask --help
```

![](./_/video/ask.gif)

翻訳

```bash
ai translate "こんにちは"
ai translate "こんにちは" -t japanese
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

## 必要条件

```bash
pip install rich openai
```

* プロキシサポート

環境変数`HTTP_PROXY`および`HTTPS_PROXY`または`ALL_PROXY`をサポートしています。`--proxy`パラメータを使用してプロキシを指定することもできます。

たとえば：

```bash
export HTTP_PROXY=http://x.x.x.x:xxxx
export HTTPS_PROXY=http://x.x.x.x:xxxx
export ALL_PROXY=http://x.x.x.x:xxxx
```

SOCKS5プロキシもサポートしています。たとえば：

```bash
export ALL_PROXY=socks5://x.x.x.x:xxxx
```

SOCKS5プロキシを使用するには、 `pip install pysocks`をインストールする必要があります。

* OPENAI_API_KEY

環境変数`OPENAI_API_KEY`を設定することができます。また、`--api-key`パラメータを使用して指定することもできます。