

# AIツール for chatGPT

このCLIツールを使用すると、コマンドラインで簡単にchatGPTを使用できます。チャットすることも、質問に答えてもらうこともできます。また、テキストを翻訳することもできます。さらに 
でMarkdownをレンダリングすることもできます。

[![PyPI](https://img.shields.io/pypi/v/py-ai-cli?logo=python&logoColor=%23cccccc)](https://pypi.org/project/py-ai-cli)

 [English](README.md)| [中文](README_zh.md) | [日本語](README_ja.md)

## 依存関係

* OPENAI_API_BASE (オプション)

GFWの問題で、`https://api.openai.com`にアクセスできない場合は、`OPENAI_API_BASE`環境変数を使用して、他のAPIアドレスを指定できます。この方法が推奨されます。代理を
使用する方法よりも安定しています。
Cloudflare Workersを使用してプロキシを構築する方法は、[使用Cloudflare Workers搭建OpenAI API代理](https://github.com/noobnooc/noobnooc/discussions/9)をご覧ください。

* OPENAI_API_KEY

環境変数`OPENAI_API_KEY`を設定したり、`--api-key`パラメータを使用したり、`ai setting`コマンドで設定することができます。

## インストール

```bash
pip install py-ai-cli
```

または最新バージョンをインストール

```bash
 pip install git+https://github.com/yufeikang/ai-cli.git    
```

## 設定

現在、`ai setting`コマンドを使用して、APIキーとAPIベースを設定できます。環境変数とCLIパラメータも引き続き有効です。

```bash
# チェックと設定の表示
ai setting
# 設定
ai setting -e
```

## 使用方法

`ai -h`を使用して、サポートされているすべてのコマンドを確認できます。

* コミットメッセージの自動生成

```bash
ai commit
```

![](./asset/video/commit.gif)

* 質問する

```bash
ai ask "こんにちは"
# ストリームモードを無効化
ai --no-stream ask "こんにちは"
# help
ai ask --help
# 事前プロンプトを使用する
curl -s https://raw.githubusercontent.com/yufeikang/ai-cli/main/README.md | ai ask --prompt "summary this, how to install"
```

![](./asset/video/ask.gif)

* 翻訳

```bash
ai translate "こんにちは"
ai translate "こんにちは" -t japanese
ai translate -t english -f "file.txt"
echo "こんにちは" | ai translate -t english
cat "file.txt" | ai translate -t english
```

 ![](./asset/video/translate.gif)

* チャット

```bash
ai chat
```

 ![](./asset/video/chat.gif)

* コードレビュー

```bash
ai review
ai review -t develop
ai review -t HEAD~1
```

## プロキシサポート

> OPENAI_API_BASE 正向きなプロキシの方法が推奨され、使用することをお勧めします。

環境変数`HTTP_PROXY`および`HTTPS_PROXY`または`ALL_PROXY`がサポートされています。また、`--proxy`パラメータを使用してプロキシを指定することもできます。

例：

```bash
export HTTP_PROXY=http://x.x.x.x:xxxx
# もしくは
export HTTPS_PROXY=https://x.x.x.x:xxxx
```

socks5プロキシもサポートされています。例：

```bash
export ALL_PROXY=socks5://x.x.x.x:xxxx
```

socks5プロキシを使用するには、`pip install pysocks`をインストールする必要があります。

## 補足

より多くのコマンドを見るには、`ai --help`を使用してください。