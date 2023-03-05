

# AIツール chatGPT

このCLIツールは、コマンドラインでchatGPTを簡単に使用できます。 彼とチャットすることも、質問に答えてもらうこともできます。 
また、テキストの翻訳を行うこともできます。そして、ターミナルでマークダウンをレンダリングすることもできます。

[English](README.md) | [中文](README_zh.md) | [日本語](README_ja.md)

## 依存関係

* OPENAI_API_BASE (オプション)

GFWのために `https://api.openai.com`にアクセスできない場合は、 
`OPENAI_API_BASE`環境変数を使用して別のapiアドレスを指定できます。この方法を使用することをお勧めします。これは、プロキシを使用する方法よりも安定しています。
Cloudflare Workersを使用してプロキシを設定する方法については、[Using Cloudflare Workers to Set Up OpenAI API Proxy](https://github.com/noobnooc/noobnooc/discussions/9)を参照してください。

* OPENAI_API_KEY

`OPENAI_API_KEY`環境変数を設定し、 `--api-key`でパラメータを指定するか、 `ai setting`コマンドを使用して設定できます。

## インストール

```bash
pip install py-ai-cli
```

または最新バージョンをインストールする

```bash
 pip install git+https://github.com/yufeikang/ai-cli.git    
```

## 設定

今、 `ai setting`コマンドを使用して API キーと API ベースを設定できます。環境変数とCLIパラメータも引き続き有効です。

```bash
# 設定の確認
ai setting
# 設定する
ai setting -e
```

## 使用方法

質問をする：

```bash
ai ask "こんにちは"
# ノーストリームモード
ai --no-stream ask "こんにちは"
# ヘルプ
ai ask --help
```

![](./asset/video/ask.gif)

翻訳する：

```bash
ai translate "こんにちは"
ai translate "こんにちは" -t japanese
ai translate -t english -f "file.txt"
echo "こんにちは" | ai translate -t english
cat "file.txt" | ai translate -t english
```

![](./asset/video/translate.gif)

おしゃべり

```bash
ai chat
```

![](./asset/video/chat.gif)

## 代理サポート

> OPENAI_API_BASE 正しいプロキシ方法はより安定しているため、お勧めします。

環境変数 `HTTP_PROXY` と `HTTPS_PROXY`または `ALL_PROXY`がサポートされています。 `--proxy`パラメータを使用してプロキシを指定することもできます。

例：

```bash
export HTTP_PROXY=http://x.x.x.x:xxxx
# または
export HTTPS_PROXY=https://x.x.x.x:xxxx
```

また、socks5プロキシもサポートされています。

```bash
export ALL_PROXY=socks5://x.x.x.x:xxxx
```

socks5プロキシには、 `pip install pysocks`をインストールする必要があります。

## 追加情報

より多くのコマンドを表示するには、 `ai --help`を使用してください。