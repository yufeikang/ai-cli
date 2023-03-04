

# chatGPT用のAIツール

このCLIツールは、コマンドラインでchatGPTを簡単に使用できるようにします。チャットをしたり、質問に答えたり、テキストを翻訳したりすることができます。また、ターミナルでのMarkdownのレンダリングをサポートしています。

[中文](README.zh.md) | [English](README.md) | [日本語](README.ja.md)

## クイック体験（インストール不要）

```bash
curl https://raw.githubusercontent.com/yufeikang/ai-cli/main/ai_cli/cli.py -L -s | python - ask "こんにちは"
```

## 依存関係

* OPENAI_API_BASE（オプション）

GFWの問題により、`https://api.openai.com`にアクセスできない場合は、`OPENAI_API_BASE`環境変数を使用して別のAPIアドレスを指定できます。この方法をお勧めします。プロキシを使用する方法よりも安定しています。 

Cloudflare Workersを使用して代理を構築する方法については、次の記事を参照してください：[使用Cloudflare Workers搭建OpenAI API代理](https://github.com/noobnooc/noobnooc/discussions/9)

* OPENAI_API_KEY

`OPENAI_API_KEY`環境変数を設定するか、`--api-key`パラメーターを使用して指定できます。

## インストール

```bash
pip install https://github.com/yufeikang/ai-cli/releases/download/v0.0.1/ai_cli-0.0.1-py3-none-any.whl
```

## 使い方

質問する

```bash
ai ask "こんにちは"
# ストリームモードではありません
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

## プロキシサポート

> OPENAI_API_BASE 正向代理方式更加稳定，推荐使用。

`HTTP_PROXY`および`HTTPS_PROXY`環境変数または`ALL_PROXY`をサポートしています。また、`--proxy`パラメーターを使用して代理を指定することもできます。

例：

```bash
export HTTP_PROXY=http://x.x.x.x:xxxx
# or
export HTTPS_PROXY=https://x.x.x.x:xxxx
```

また、socks5プロキシもサポートしています。

```bash
export ALL_PROXY=socks5://x.x.x.x:xxxx
```

socks5プロキシを使用するには、`pip install pysocks`を実行する必要があります。