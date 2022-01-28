# -*- coding: utf-8 -*-
from email import message
import discord
from discord.ext import commands

import re
from crypt import crypt

# 文字数制限
LENGTH_LIMIT_TRIP = 21
LENGTH_LIMIT_NO_TRIP = 32

# トリップの生成
# https://itasuke.hatenadiary.org/entry/20071224/p1
def generate_trip(tripkey):
    salt = (tripkey + 'H.')[1:3]
    salt = re.sub('[^\.-z]', '.', salt)
    salt = salt.translate(str.maketrans(':;<=>?@[\\]^_`', 'ABCDEFGabcdef'))
    trip = crypt(tripkey, salt)
    trip = trip[-10:]
    return trip

# 文字数制限ヒント
def length_hint(ctx, length, limit):
    mention = '<@' + str(ctx.author.id) +'> '
    hint = mention + '名前が長すぎます。(' + str(length) + '/' + str(limit) + '文字)'
    return hint

# bot settings
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
async def nickname(ctx, nickname):
    # メッセージ削除 (トリップキーバレ防止)
    await ctx.message.delete()

    # なりすまし防止
    sharp = nickname.find('#')
    dia = nickname.find('◆')
  
    # ニックネームの変更(トリップキー有り)
    if sharp != dia:
        # 名前が受け入れられる長さであること
        if sharp < 22 and dia < 22:
            # 本物
            if sharp != -1 and (dia == -1 or dia > sharp):
                split_icon = '◆'
                split = sharp
            # なりすまし
            elif dia != -1 and (sharp == -1 or sharp > dia):
                split_icon = '◇'
                split = dia
            name = nickname[:split]
            trip = generate_trip(nickname[split+1:])
            nickname_n_trip = name + split_icon + trip
            await ctx.author.edit(nick=nickname_n_trip)
        else:
            length = max(sharp, dia)
            await ctx.send(length_hint(ctx, length, LENGTH_LIMIT_TRIP))
    # ニックネームの変更(トリップキー無し)
    else:
        # 名前が受け入れられる長さであること
        length = len(nickname)
        if length < 33:
            await ctx.author.edit(nick=nickname)
        else:
            await ctx.send(length_hint(ctx, length, LENGTH_LIMIT_NO_TRIP))  

# トークン
with open('.token') as t:
    bot.run(t.read())