# chatGPT的AI工具

このCLIツールは、コマンドラインでchatGPTを簡単に使用できます。チャットしたり、質問に答えたり、テキストを翻訳したりすることができます。ターミナルで
のMarkdownのレンダリングをサポートしています。

[中文](README.zh.md) | [English](README.md) | [日本語](README.ja.md)

## クイックスタート(インストール不要)

```bash
curl https://raw.githubusercontent.com/yufeikang/ai-cli/main/ai.py -L -s | python - ask "こんにちは"
```

## 依存関係

* 依存関係のインストール

```bash
pip install rich openai
```

* OPENAI_API_BASE(オプション)

GFWの原因により`https://api.openai.com`にアクセスできない場合、他のAPIアドレスを`OPENAI_API_BASE`環境変数で指定できます。
この方法を使用することをお勧めします。これは、プロキシを使用する方法よりも安定しています。
Cloudflare Workersを使用してプロキシを作成する方法については、次の記事を参照してください：[使用Cloudflare Workers搭建OpenAI 
API代理](https://github.com/noobnooc/noobnooc/discussions/9)

* OPENAI_API_KEY

環境変数`OPENAI_API_KEY`を設定することができます。`--api-key`パラメータを指定することもできます。

## インストール

```bash
curl https://raw.githubusercontent.com/yufeikang/ai-cli/main/ai.py -L -s> /usr/local/bin/ai && chmod +x /usr/local/bin/ai && pip install -U rich 
openai
```

## 使用方法

質問する

```bash
ai ask "こんにちは"
# ノーストリームモード
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

環境変数`HTTP_PROXY`および`HTTPS_PROXY`または`ALL_PROXY`をサポートしています。`--proxy`パラメータでプロキシを指定することもできます。

例：

```bash
export HTTP_PROXY=http://x.x.x.x:xxxx
# または
export HTTPS_PROXY=https://x.x.x.x:xxxx
```

また、socks5プロキシをサポートしています。

```bash
export ALL_PROXY=socks5://x.x.x.x:xxxx
```

socks5プロキシを使用する場合は、`pip install pysocks`をインストールする必要があります。