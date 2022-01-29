![](https://img.shields.io/badge/python-3.10.x-blue?style=for-the-badge&logo=python)  
![](https://i.imgur.com/Fx5vRFC.gif)

# 使い方

1. `discord.py`をインストール.
   1. `python -m pip install -r requirements.txt`を実行.
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
`#` 以降の文字がトリップキーとして扱われ、トリップ付きのニックネームに変更できます。  
トリップ付きのニックネーム変更を行う場合は、 `nickname` を20文字以下にしなければなりません。  
サーバーに存在するテキストチャンネル名と一致する文字列をトリップキーとして使用することは非推奨です。

## 成りすまし防止

`/nickname nickname◆trip`  
`◆` が `◇` に置き換わる形でニックネームが変更されます。

# 注意点

- **サーバーオーナーのニックネームはDiscordの仕様上Botによる変更ができません。**
  - こればかりはどうしようもない。
