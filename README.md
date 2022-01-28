![](https://img.shields.io/badge/python-3.8%20or%20higher-blue)
![](https://i.imgur.com/Fx5vRFC.gif)

# 使い方

1. `discord.py`をインストール.
   1. `python -m pip -r requirements.txt`を実行.
1. `bot.py`と同じ階層に`.token`を用意.
1. `bot.py`を実行.

※現状、使用しているライブラリの関係でWindowsOSは未対応です。

# コマンド

## ニックネーム変更コマンド

`/nickname nickname`  
使用したユーザーのサーバーニックネームを変更するコマンドです。  
使用後はメッセージが自動的に削除されます。

## トリップキー

`/nickname nickname#tripkey`  
nicknameの後ろに `#` を付けた際は、以降の文字がトリップキーとして扱われます。  
サーバーに存在するテキストチャンネル名と一致する文字列をトリップキーとして使用することは非推奨です。

## 成りすまし防止

`/nickname nickname◆trip`  
最初の `◆` が `◇` としてニックネームが変更されます。

# 注意点

- **サーバーオーナーのニックネームはDiscordの仕様上Botによる変更ができません。**
  - こればかりはどうしようもない。
- **ニックネームに空白を使用することはできません。**
  - 作る段階で想定し忘れていました。
    - 元々身内用のBotなので必要があれば直します。
