# AI Tools for chatGPT

このCLIツールは、コマンドラインでchatGPTまたはnew 
bingを簡単に使用できるようにします。チャットをしたり、質問に答えたり、テキストを翻訳したりすることができます。さらに、ターミナルでのMarkdownのレンダリングをサポートしています。

[![PyPI](https://img.shields.io/pypi/v/py-ai-cli?logo=python&logoColor=%23cccccc)](https://pypi.org/project/py-ai-cli)

 [English](README.md) | [中文](README_zh.md) | [日本語](README_ja.md)

## 必要条件

* OPENAI\_API\_BASE (オプション)

GFWの問題で `https://api.openai.com` にアクセスできない場合は、 `OPENAI_API_BASE` 環境変数で他のAPIアドレスを指定できます。 
これを使用することをお勧めします。この方法は、プロキシを使用するよりも安定しています。Cloudflareのworkersを使用してプロキシを構築する方法については、次の記事を参照してください: [使用Cloudflare 
Workers搭建OpenAI API代理](https://github.com/noobnooc/noobnooc/discussions/9)

* OPENAI\_API\_KEY

環境変数 `OPENAI_API_KEY` または `--api-key` パラメーターを使用して指定するか、`ai setting`命令を使用して指定できます。

* Bing Cookie

Bing Botを使用する場合は、Bing Cookieを設定する必要があります。`ai setting`命令を使用して設定できます。

```bash
ai setting --edit bing_cookie="BING_COOKIE.JSON"
```

Cookie取得方法については、[Bing Bot Cookie获取](https://github.com/acheong08/EdgeGPT#checking-access-required) を参照してください。

## インストール

```bash
pip install py-ai-cli
```

または最新バージョンをインストールします

```bash
pip install git+https://github.com/yufeikang/ai-cli.git    
```

## 設定

現在、APIキーとAPIベースを設定するには、 `ai setting` コマンドを使用できます。これに加えて、環境変数とCLIパラメータも引き続き有効です。

```bash
# 設定を確認する
ai setting
# 設定値を編集する
ai setting --edit
```

## 使用

 `ai -h` コマンドでサポートされているすべてのコマンドを確認できます。

* コミットメッセージ自動生成

```bash
ai commit
```

![](./asset/video/commit.gif)

* 質問する

```bash
ai ask "こんにちは"
# ストリームモードを使用しない場合
ai --no-stream ask "こんにちは"
# ヘルプを表示する
ai ask --help
# プレプロンプトを使用する
curl -s https://raw.githubusercontent.com/yufeikang/ai-cli/main/README.md | ai ask --prompt "summary this, how to install"
```

![](./asset/video/ask.gif)

* 翻訳する

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

> OPENAI_API_BASE 正向代理方式更加稳定，推荐使用。

`HTTP_PROXY` と `HTTPS_PROXY` または `ALL_PROXY` という環境変数をサポートしています。 また、 `--proxy` パラメーターを使用してプロキシを指定することもできます。たとえば：

```bash
export HTTP_PROXY=http://x.x.x.x:xxxx
# or
export HTTPS_PROXY=https://x.x.x.x:xxxx
```

socks5プロキシもサポートしています、例えば：

```bash
export ALL_PROXY=socks5://x.x.x.x:xxxx
```

socks5プロキシを使用するには、 `pip install pysocks` をインストールする必要があります。

## その他

より多くのコマンドを確認するためには `ai --help` を使用してください。