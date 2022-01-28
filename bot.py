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


def extract_trip_key(nickname: str) -> tuple[str, int] | None:
    trip_marker_pos = nickname.find('#')
    if trip_marker_pos == -1:
        return

    # NOTE: 仕様上空白文字はトリップキーとして有効です (`# ` で wqLZLRuzPQ となります)
    # トリップキーが空の場合
    if trip_marker_pos == len(nickname) - 1:
        return

    trip_key = nickname[trip_marker_pos + 1:]

    return (trip_key, trip_marker_pos)

# ニックネームコマンド


@bot.command()
async def nickname(ctx, *, nick: str):
    # メッセージ削除 (トリップキーバレ防止)
    await ctx.message.delete()

    # なりすまし防止
    nick = nick.replace('◆', '◇')

    extracted = extract_trip_key(nick)
    if extracted:
        trip_key, trip_marker_pos = extracted
        if trip_marker_pos > LENGTH_LIMIT_TRIP:
            await ctx.send(length_hint(ctx, trip_marker_pos, LENGTH_LIMIT_TRIP))
            return
        trip = generate_trip(trip_key)
        name = nick[:trip_marker_pos]
        nick = f'{name} ◆{trip}'
        assert len(nick) <= LENGTH_LIMIT_NO_TRIP
    else:
        length = len(nick)
        if length > LENGTH_LIMIT_NO_TRIP:
            await ctx.send(length_hint(ctx, length, LENGTH_LIMIT_NO_TRIP))
            return
    await ctx.author.edit(nick=nick)


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
