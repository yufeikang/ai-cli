

# AI Tools for chatGPT

このCLIツールは、chatGPTを簡単にコマンドラインで使用できるようにします。チャットしたり、質問に答えたり、テキストを翻訳したりすることが
できます。また、ターミナルでのMarkdownのレンダリングをサポートしています。

[![PyPI](https://img.shields.io/pypi/v/py-ai-cli?logo=python&logoColor=%23cccccc)](https://pypi.org/project/py-ai-cli)

 [English](README.md)| [中文](README_zh.md) | [日本語](README_ja.md)

## 必要なもの

* OPENAI_API_BASE (オプション)

GFWの影響で `https://api.openai.com` 
にアクセスすることができない場合は、`OPENAI_API_BASE`環境変数を使用して他のAPIアドレスを指定できます。高度なプロキシの使用よりも安定した
方法です。
Cloudflare 
Workersを使用してプロキシを構成する方法については、[こちらの記事](https://github.com/noobnooc/noobnooc/discussions/9)を参照してください。

* OPENAI_API_KEY

`OPENAI_API_KEY` 環境変数を設定するか、 `--api-key` パラメーターを使用してAPIキーを指定できます。 `ai 
setting`コマンドを使用しても指定できます。

## インストール

```bash
pip install py-ai-cli
```

または最新バージョンをインストールすることもできます

```bash
 pip install git+https://github.com/yufeikang/ai-cli.git    
```

## 設定

現在、`ai setting`コマンドを使用して、APIキーとAPIベースを設定できます。環境変数やCLIパラメータも引き続き有効です。

```bash
# 設定を確認する
ai setting
# 設定変更
ai setting -e
```

## 使い方

質問する

```bash
ai ask "こんにちは"
# ストリームモードを無効化する場合
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

## プロキシーサポート

> OPENAI_API_BASE 正向代理方式更加稳定，推荐使用。

環境変数 `HTTP_PROXY`および`HTTPS_PROXY`または`ALL_PROXY` 
をサポートしています。また、「--proxy」パラメーターを使用してプロキシを指定することもできます。

例：

```bash
export HTTP_PROXY=http://x.x.x.x:xxxx
# or
export HTTPS_PROXY=https://x.x.x.x:xxxx
```

socks5プロキシもサポートされています。例：

```bash
export ALL_PROXY=socks5://x.x.x.x:xxxx
```

socks5プロキシには、 `pip install pysocks` をインストールする必要があります。

## 補足

`ai --help`を使用して、より多くのコマンドを表示します。