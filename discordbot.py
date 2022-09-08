import discord
import traceback
import requests
import re
from discord.ext import commands
from discord.ext import tasks
from os import getenv
from bs4 import BeautifulSoup
from datetime import datetime, timezone, timedelta, time

bot = commands.Bot(command_prefix="/",intents=discord.Intents.all())

URL = r"https://"
url = re.compile(URL)
pattern = pattern = re.compile(r"https?://[\w/:%#\$&\?\(\)~\.=\+\-]+")

# その送信者のIDを辞書に入れる
is_matched = {}
is_text = {}


async def _check_url(message: discord.Message):
    role = discord.utils.get(message.guild.roles, name="kagi")
    if message.author.bot:
        return
    # メッセージからURLを抽出
    url_list = re.findall(pattern, message.content)
    # もしメッセージにURLが含まれていたら
    if url_list:
        print("#" * 50)
        print("1時間以内に同じURLを送信したら削除する")
        # もし辞書にURLが登録されていたら(含まれていなかったらNoneが返る)
        if is_text.get(url_list[0], None) is not None:
            # 送信されていた時間を取り出す
            _sent_date = is_text[url_list[0]]
            print("辞書に登録されている発言時間は" + str(_sent_date))
            # もし差分が3600秒以上(1h)なら
            if (datetime.now() - _sent_date).seconds >= 3600:
                # 辞書のURLが持つ発言時間を更新して終了
                print("辞書のURL(" + url_list[0] + ")が持つ発言時間を更新")
                is_text[url_list[0]] = datetime.now()
                return
            else:
                # 1h以内に投稿されていた場合削除
                print(url_list[0])
                print("そのURL(" + url_list[0] + ")が入ったメッセージが1時間以内に投稿されています。削除します。")
                alert_msg = await message.channel.send("そのURLが入ったメッセージが1時間以内に投稿されています。削除します。")
                await message.delete(delay=1)
                await alert_msg.delete(delay=3)
                return
        else:
            # 辞書にURLが登録されていなかったのでURLと発言時間を登録する
            print("辞書にURLと発言時間を登録")
            is_text[url_list[0]] = datetime.now()
            print(is_text)
    else:
        print("メッセージにURLはない")

'''
async def _check_url(message: discord.Message):
    # もしメッセージにURLが含まれていたら
    if url.search(message.content) is not None:
        print(is_matched)
        # もし辞書に送信者のIDが含まれていたら(含まれていなかったらNoneが返る)
        if is_matched.get(message.author.id, None) is not None:
            # 送信されていた時間を取り出す
            _sent_date = is_matched[message.author.id]
            # もし差分が3600秒以上(1h)なら、送信された時間を更新して終了
            if (datetime.datetime.now() - _sent_date).seconds >= 3600:
                is_matched[message.author.id] = datetime.datetime.now()
                return

            else:
                # 1h以内に投稿されていた場合削除
                alert_msg = await message.channel.send("そのURLが入ったメッセージが1時間以内に投稿されています。削除します。")
                await message.delete(delay=1)
                await alert_msg.delete(delay=3)

        else:
            # 再起動時など、辞書が空の時に送信された場合、辞書を更新
            is_matched[message.author.id] = datetime.datetime.now()
            print(is_matched)
'''


@bot.event
async def on_ready():
    print(bot.user.name)


@bot.event
async def on_message(message: discord.Message):
    await _check_url(message)

token = getenv('DISCORD_BOT_TOKEN')
bot.run(token)
