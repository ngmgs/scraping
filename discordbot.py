import discord
import traceback
import requests
import re
import datetime
from discord.ext import commands
from discord.ext import tasks
from os import getenv
from bs4 import BeautifulSoup

bot = commands.Bot(command_prefix="/",intents=discord.Intents.all())

URL = r"https://"
url = re.compile(URL)
pattern = "https?://[\w/:%#\$&\?\(\)~\.=\+\-]+"

# その送信者のIDを辞書に入れる
is_matched = {}
is_text = {}


async def _check_url(message: discord.Message):
    if any(is_text):
        print(message.content)
        url_list = re.findall(pattern, message.content)
        print(url_list)
        is_text[url_list[0]] = datetime.datetime.now()
        print(is_text)
    else:
    print("空である")


'''
async def _check_url(message: discord.Message):
    # もしメッセージにURLが含まれていたら
    if url.search(message.content) is not None:
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
'''


@bot.event
async def on_ready():
    print(bot.user.name)


@bot.event
async def on_message(message: discord.Message):
    await _check_url(message)

token = getenv('DISCORD_BOT_TOKEN')
bot.run(token)
