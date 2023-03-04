# AIツール for chatGPT

このCLIツールを使うと、コマンドラインでchatGPTを簡単に使用できます。チャットをすることも、質問に答えてもらうこともできます。また、テキスト
を翻訳することもできます。さらに、ターミナルでのマークダウンのレンダリングをサポートしています。

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

![](./_/video/ask.gif)

翻訳する

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

## 依存関係

```bash
pip install rich openai
```

* プロキシサポート

環境変数`HTTP_PROXY`と`HTTPS_PROXY`または`ALL_PROXY`をサポートしています。`--proxy`パラメーターを使用してプロキシを指定することもできます。

例：

```bash
export HTTP_PROXY=http://x.x.x.x:xxxx
# or
export HTTPS_PROXY=https://x.x.x.x:xxxx
```

socks5プロキシもサポートしています。例：

```bash
export ALL_PROXY=socks5://x.x.x.x:xxxx
```

socks5プロキシを使用するには、`pip install pysocks`をインストールする必要があります。

* OPENAI_API_BASE（オプション）
もしGFWのせいで 
`https://api.openai.com`にアクセスできない場合は、`OPENAI_API_BASE`環境変数を別のAPIアドレスに指定することができます。この方
法を推奨します。これは、プロキシを使用する方法よりも安定しています。
Cloudflareのworkersを使用してプロキシを構築する方法は、次の記事を参照してください：[使用Cloudflare Workers搭建OpenAI 
API代理](https://github.com/noobnooc/noobnooc/discussions/9)

* OPENAI_API_KEY
`OPENAI_API_KEY`環境変数を設定することができます。また、`--api-key`パラメーターを使用して指定することもできます。