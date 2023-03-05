# chatGPTのAIツール

このCLIツールは、コマンドラインでchatGPTを簡単に使用できるようにするためのものです。他の人とチャットすることも、質問に答えてもらうこともできます。また、テキストを翻訳することもできます。さらに、ターミナル
でのマークダウンのレンダリングをサポートしています。

[中文](README.zh.md) | [English](README.md) | [日本語](README.ja.md)

## 依存関係

- OPENAI_API_BASE（オプション）

GFWの問題があるため「https://api.openai.com」にアクセスできない場合は、`OPENAI_API_BASE`環境変数で他のAPIのアドレスを指定できます。推奨方法です。これにより、プロキシを使用するよりも安定した状態にすることができます。
dflare Workersを使用してプロキシを構築する方法は、[使用Cloudflare Workers搭建OpenAI API代理](https://github.com/noobnooc/noobnooc/discussions/9)の記事を参照してください。

- OPENAI_API_KEY

`OPENAI_API_KEY`環境変数を設定することができます。また、`--api-key`パラメータで指定することもできます。`ai setting`コマンドを使用して設定することもできます。

## インストール

```bash
pip install https://github.com/yufeikang/ai-cli/releases/download/v0.0.1/ai_cli-0.0.1-py3-none-any.whl
```

## 設定

現在、`ai setting`コマンドを使用して、APIキーとAPIベースを設定できます。環境変数とCLIパラメーターもまだ有効です。

```bash
# settingを確認
ai setting
# 設定
ai setting -e
```

## 使用方法

### 質問をする

```bash
ai ask "こんにちは"
# no stream mode
ai --no-stream ask "こんにちは"
# help
ai ask --help
```

![](./asset/video/ask.gif)

### 翻訳する

```bash
ai translate "こんにちは"
ai translate "こんにちは" -t japanese
ai translate -t english -f "file.txt"
echo "こんにちは" | ai translate -t english
cat "file.txt" | ai translate -t english
```

![](./asset/video/translate.gif)

### チャットする

```bash
ai chat
```

![](./asset/video/chat.gif)

## プロキシサポート

> OPENAI_API_BASE 正向代理方式更加稳定，推荐使用。

環境変数`HTTP_PROXY`および`HTTPS_PROXY`または`ALL_PROXY`をサポートしています。また、`--proxy`パラメータを使用してプロキシを指定することもできます。

例：

```bash
export HTTP_PROXY=http://x.x.x.x:xxxx
# or
export HTTPS_PROXY=https://x.x.x.x:xxxx
```

関数也支持Socks5代理，例如：

```bash
export ALL_PROXY=socks5://x.x.x.x:xxxx
```

Socks5プロキシを使用するには、`pip install pysocks`をインストールする必要があります。

## 追加情報

他のコマンドを確認するには、`ai --help`を使用してください。