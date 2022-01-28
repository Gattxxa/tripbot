# -*- coding: utf-8 -*-
from crypt import crypt
import discord
from discord.ext import commands
import re

# 文字数制限
LENGTH_LIMIT_TRIP: int = 20
LENGTH_LIMIT_NO_TRIP: int = 32


# トリップの生成
# https://itasuke.hatenadiary.org/entry/20071224/p1
def generate_trip(trip_key):
    salt: str = (trip_key + 'H.')[1:3]
    salt = re.sub(r'[^\.-z]', '.', salt)
    salt = salt.translate(str.maketrans(':;<=>?@[\\]^_`', 'ABCDEFGabcdef'))
    trip: str = crypt(trip_key, salt)
    trip = trip[-10:]
    return trip


# 文字数制限ヒント
def length_hint(ctx, length: int, limit: int):
    return f'<@{str(ctx.author.id)}> 名前が長すぎます。({str(length)}/{str(limit)}文字)'


# ボット設定
bot = commands.Bot(command_prefix='/')
bot.remove_command('help')


# ボットステータス
@bot.event
async def on_ready():
    print('online')
    status = '/nickname nickname#tripkey '
    await bot.change_presence(activity=discord.Game(name=status, type=1))


# ニックネームコマンド
@bot.command()
async def nickname(ctx, *, nick):
    # メッセージ削除 (トリップキーバレ防止)
    await ctx.message.delete()

    # なりすまし防止
    sharp = nick.find('#')
    dia = nick.find('◆')

    # ニックネームの変更(トリップキー有り)
    if sharp != dia:

        # 名前が受け入れられる長さである場合
        if sharp <= LENGTH_LIMIT_TRIP and dia <= LENGTH_LIMIT_TRIP:

            # 本物
            if sharp != -1 and (dia == -1 or dia > sharp):
                split_icon = '◆'
                split = sharp
                trip = generate_trip(nick[split + 1:])

            # なりすまし
            # if dia != -1 and (sharp == -1 or sharp > dia):
            else:
                split_icon = '◇'
                split = dia
                trip = nick[split + 1:]

            name = nick[:split]
            nick_n_trip = f'{name} {split_icon}{trip}'
            await ctx.author.edit(nick=nick_n_trip)

        # 名前が受け入れられない長さである場合
        else:
            length = max(sharp, dia)
            await ctx.send(length_hint(ctx, length, LENGTH_LIMIT_TRIP))

    # ニックネームの変更(トリップキー無し)
    else:
        length = len(nick)

        # 名前が受け入れられる長さである場合
        if length <= LENGTH_LIMIT_NO_TRIP:
            await ctx.author.edit(nick=nick)

        # 名前が受け入れられない長さである場合
        else:
            await ctx.send(length_hint(ctx, length, LENGTH_LIMIT_NO_TRIP))


# bot.pyが直接起動されている場合
if __name__ == '__main__':
    # トークンを開く
    try:
        with open('.token', 'r') as t:
            # ボットを起動
            bot.run(t.read())

    # ファイルが存在しない場合
    except FileNotFoundError:
        print('エラー: .token ファイルが見つかりませんでした。')
