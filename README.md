![](https://img.shields.io/badge/python-3.8%20or%20higher-blue)
# 使い方
1. `discord.py`をインストール.
2. `bot.py`と同じ階層に`.token`を用意.
3. `bot.py`を実行.

# コマンド
## ニックネーム変更コマンド  
`/nickname nickname`  
使用したユーザーのサーバーニックネームを変更するコマンドです。

## トリップキー 
`/nickname nickname#tripkey`  
nicknameの後ろに`#`を付けた際は、以降の文字がトリップキーとして扱われます。   
サーバーに存在するテキストチャンネル名と一致している文字列を、トリップキーとして使用することはできません。

# 注意
- 現状、使用しているライブラリの関係でWindowsOSは未対応です。