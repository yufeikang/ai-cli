

# AIツール for chatGPT

このCLIツールを使用すると、コマンドラインでchatGPTを簡単に使用できます。チャットをしたり、質問に答えたり、テキストを翻訳したりでき
ます。また、ターミナルでのMarkdownのレンダリングをサポートしています。

[![PyPI](https://img.shields.io/pypi/v/py-ai-cli?logo=python&logoColor=%23cccccc)](https://pypi.org/project/py-ai-cli)

[English](README.md)| [中文](README_zh.md) | [日本語](README_ja.md)

## 依存関係

* OPENAI_API_BASE (オプション)

GFWの制限のために`https://api.openai.com`にアクセスできない場合は、`OPENAI_API_BASE`環境変数を使
用して別のAPIアドレスを指定できます。これは推奨されます。これにより、プロキシを使用する場合よりも安定性が向上します。
Cloudflareのワーカーを使用してプロキシを構築する方法については、[Cloudflare WorkersでOpenAI 
APIプロキシを構築する方法](https://github.com/noobnooc/noobnooc/discussions/9)を参照してください。

* OPENAI_API_KEY

環境変数`OPENAI_API_KEY`を設定するか、`--api-key`パラメーターを使用して指定することができます。この他、`ai 
setting`コマンドを使用して設定することもできます。

## インストール

```bash
pip install py-ai-cli
```

または最新バージョンをインストールするには

```bash
 pip install git+https://github.com/yufeikang/ai-cli.git    
```

## 設定

`ai setting`コマンドを使用して、APIキーとAPIベースを設定できます。環境変数とCLIパラメーターも引き続き使用できます。

```bash
# 設定の確認
ai setting
# 設定
ai setting -e
```

## 使用法

質問する

```bash
ai ask "こんにちは"
# ストリームモードを無効にする
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

## プロキシサポート

> OPENAI_API_BASE 正向代理方式更加稳定，推荐使用。

環境変数`HTTP_PROXY`と`HTTPS_PROXY`または`ALL_PROXY`をサポートしています。また、`--proxy`パラメーターを使用してプロキシを指定する
こともできます。

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

詳細なコマンドは、`ai --help`を使用してください。