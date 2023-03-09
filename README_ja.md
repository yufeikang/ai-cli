

# チャットGPTのためのAIツール

このCLIツールを使うと、簡単にコマンドラインでチャットGPTを使用できます。人工知能とチャットしたり、質問し
りすることができます。また、テキストを翻訳したり、ターミナルでMarkdownをレンダリングすることもできます
。

[![PyPI](https://img.shields.io/pypi/v/py-ai-cli?logo=python&logoColor=%23cccccc)](https://pypi.org/proj
ect/py-ai-cli)

 [英語](README.md)| [中文](README_zh.md) | [日本語](README_ja.md)

## 依存関係

* OPENAI_API_BASE (オプション)

GFWのために`https://api.openai.com`にアクセスできない場合は、`OPENAI_
API_BASE`環境変数で別のAPIアドレスを指定できます。プロキシを使用するよりも安定しているため、この方法を使
OpenAI APIプロキシを構築するための手順については、この記事を参照してください。[Build an OpenAI API Proxy
with Cloudflare 
Workers](https://github.com/noobnooc/noobnooc/discussions/9).

* OPENAI_API_KEY

環境変数`OPENAI_API_KEY`を設定するか、`--api-key`パラメータを介して指定することができます。また、`ai 
setting`コマンドを介して設定することもできます。

新しい実行ファイルをビルドするには、(https://pdm.fming.dev/latest/)をインストールする必要があります。

## インストール

`py_ai_cli`は、スタンドアロンの実行可能ファイルです。`ai`にアクセスするために、パスに追加してください。
```bash
ln -s $(pwd)/py_ai_cli /usr/local/bin/ai
```


アップデートを適用して新しい実行可能ファイルをビルドするには、`run_build.sh`を実行してください。

## 設定

APIキーとAPIベースを`ai setting`コマンドで設定できます。環境変数とCLI引数は引き続き有効です。

```bash
# 設定を表示する
ai setting
# 設定する
ai setting -e
```

## 使用法

質問する

```bash
ai ask "Hello"
# stream modeオフ
ai --no-stream ask "Hello"
# help
ai ask --help
```

![](./asset/video/ask.gif)

翻訳

```bash
ai translate "Hello"
ai translate "Hello" -t japanese
ai translate -t english -f "file.txt"
echo "Hello" | ai translate -t english
cat "file.txt" | ai translate -t english
```

 ![](./asset/video/translate.gif)

チャット

```bash
ai chat
```

 ![](./asset/video/chat.gif)

コードレビュー

```bash
ai review
ai review -t develop
ai review -t HEAD~1

```

## Proxyサポート

> OPENAI_API_BASE Forward proxy is more stable and recommended.

`HTTP_PROXY`、`HTTPS_PROXY`、または`ALL_PROXY`環境変数をサポートしています。また、`--
proxy`パラメータでプロキシを指定することもできます。

例えば：

```bash
export HTTP_PROXY=http://x.x.x.x:xxxx
# または
export HTTPS_PROXY=https://x.x.x.x:xxxx
```

SOCKS5プロキシもサポートされています。例えば：

```bash
export ALL_PROXY=socks5://x.x.x.x:xxxx
```

SOCKS5プロキシを使用するには、`pip install pysocks`が必要です。

## 追加情報

`ai --help`を使用して、より多くのコマンドを表示してください。