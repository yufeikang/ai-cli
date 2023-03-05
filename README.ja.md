# chatGPT用のAIツール

このCLIツールを使うと、コマンドラインで簡単にchatGPTを使用できます。チャットのやり取りをしたり、質問への回答のお手伝いをしたり、テキストの翻訳をしたりすることができます。また、ターミナルでのmarkdownのレンダリングもサポー
トしています。

[中文版](README.zh.md) | [英文版](README.md) | [日本語版](README.ja.md)

## クイックスタート（インストールが必要なし）

```bash
curl https://raw.githubusercontent.com/yufeikang/ai-cli/main/src/ai_cli/cli.py -L -s | python - ask "こんにちは"
```

## 依存関係

* OPENAI_API_BASE（オプション）

GFWの制限のために`https://api.openai.com` にアクセスできない場合は、 `OPENAI_API_BASE`環境変数を使用して他のAPIアドレスを指定できます。使用をお勧めします。これは、代理を使用するよりもより安定した方法です。 
cloudflareのworkersを使用して代理を構築する方法については、次の記事を参照してください。：[使用Cloudflare Workers搭建OpenAI API代理](https://github.com/noobnooc/noobnooc/discussions/9)

* OPENAI_API_KEY

環境変数`OPENAI_API_KEY`を設定できます。または、 `--api-key` パラメータを指定できます。

## インストール

```bash
pip install https://github.com/yufeikang/ai-cli/releases/download/v0.0.1/ai_cli-0.0.1-py3-none-any.whl
```

## 使用方法

質問をする

```bash
ai ask "こんにちは"
# no stream mode
ai --no-stream ask "こんにちは"
# ヘルプ
ai ask --help
```

![](./asset/video/ask.gif)

翻訳

```bash
ai translate "こんにちは"
ai translate "こんにちは" -t japanese
ai translate -t english -f "file.txt"
echo "こんにちは" | ai translate -t english
cat "file.txt" | ai translate -t english
```

 ![](./asset/video/translate.gif)

チャット

```bash
ai chat
```

 ![](./asset/video/chat.gif)

## プロキシ対応

> OPENAI_API_BASE 正向代理方式更加稳定，推荐使用。

`HTTP_PROXY`、 `HTTPS_PROXY` または `ALL_PROXY` の環境変数をサポートしています。または、 `--proxy` パラメータを使用してプロキシを指定することもできます。

例：

```bash
export HTTP_PROXY=http://x.x.x.x:xxxx
# または
export HTTPS_PROXY=https://x.x.x.x:xxxx
```

また、socks5プロキシもサポートしています。

例：

```bash
export ALL_PROXY=socks5://x.x.x.x:xxxx
```

socks5プロキシを使用する場合は、 `pip install pysocks` をインストールする必要があります。