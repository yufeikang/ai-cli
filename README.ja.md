

# AIツールfor chatGPT

このCLIツールは、chatGPTをコマンドラインで簡単に使用できるようにします。チャットすることができ、質問に答えてもらうこともできます。また、テキストの翻訳もサポートしています。そして、端末でのマークダウンのレンダ
リングもサポートしています。

 [English](README.md)| [中文](README.zh.md) | [日本語](README.ja.md)

## 必要なもの

* OPENAI_API_BASE (オプション)

もしGFWの問題で、`https://api.openai.com`にアクセスできない場合は、他のapiアドレスを`OPENAI_API_BASE`環境変数で指定できます。こちらの方法をお勧めします。プロキシを使うよりも、より安定しています。
Cloudflare workersを使用してプロキシを構築する方法は、この記事を参考にしてください：[使用Cloudflare Workers搭建OpenAI API代理](https://github.com/noobnooc/noobnooc/discussions/9)

* OPENAI_API_KEY

`OPENAI_API_KEY`環境変数を設定するか、`--api-key`パラメータを使用して指定することができます。または、`ai setting`コマンドを使用して設定することもできます。

## インストール

```bash
pip install py-ai-cli
```

または、最新バージョンをインストールするには

```bash
 pip install git+https://github.com/yufeikang/ai-cli.git    
```

## 設定

`ai setting`コマンドを使用してAPIキーとAPIベースを設定できるようになりました。環境変数とCLIパラメータも引き続き有効です。

```bash
# settingを確認
ai setting
# 設定
ai setting -e
```

## 利用

質問する

```bash
ai ask "こんにちは"
# no streamモード
ai --no-stream ask "こんにちは"
# help
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

チャットする

```bash
ai chat
```

 ![](./asset/video/chat.gif)

## プロキシサポート

> OPENAI_API_BASEを使用する正向きなプロキシ方法がより安定しているため、お勧めします。

`HTTP_PROXY`、`HTTPS_PROXY`または`ALL_PROXY`の環境変数をサポートしています。また、`--proxy`パラメーターでプロキシを指定することもできます。

例：

```bash
export HTTP_PROXY=http://x.x.x.x:xxxx
# または
export HTTPS_PROXY=https://x.x.x.x:xxxx
```

また、socks5プロキシもサポートしています。

```bash
export ALL_PROXY=socks5://x.x.x.x:xxxx
```

socks5プロキシを使用するには、`pip install pysocks`をインストールする必要があります。

## 追加情報

より多くのコマンドを確認するには、`ai --help`を使用してください。