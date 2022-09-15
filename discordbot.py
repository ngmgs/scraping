import discord
import traceback
import requests
from discord.ext import commands
from discord.ext import tasks
from os import getenv
from datetime import datetime, timezone, timedelta, time
from bs4 import BeautifulSoup

bot = commands.Bot(command_prefix="/",intents=discord.Intents.all())
is_pc4u_amd = {}
is_pc4u_nvidia = {}


is_message = {}
@bot.event
async def on_message(message):
    t_delta = timedelta(hours=9)
    JST = timezone(t_delta, 'JST')
    now = datetime.now(JST).strftime('%A/%H:%M')
    is_message[message] = now
    print(is_message)

    user = message.author.username
    print(user)

    
@tasks.loop(minutes=1)
async def send_message_every():
    channel_sent = bot.get_channel(1019194136349392916)
    t_delta = timedelta(hours=9)
    JST = timezone(t_delta, 'JST')
    now = datetime.now(JST).strftime('%A/%H:%M')
    await pc4u_amd()
    await pc4u_nvidia()


@bot.event
async def on_ready():
    send_message_every.start()



#PC4Uからamdグラボの商品名と価格を取得
async def pc4u_amd():
    channel_sent = bot.get_channel(1019194136349392916)
    url = requests.get(
        "https://www.pc4u.co.jp/shopbrand/pciexpress4/page1/price/").content
    soup = BeautifulSoup(url, 'html.parser')
    #print(url)
    # await channel_sent.send("pc4u")
    for item in soup.find_all(class_="innerBox"): #商品の親要素divをクラス名で取得
        title = item.find(class_="name").text #itemからクラス名で商品名を取得
        price = item.find(class_="price").text #itemからクラス名で価格を取得
        url_temp = item.find('a') #itemからクラス名で価格を取得
        url = "https://www.pc4u.co.jp" + url_temp.get('href')


        # もし辞書に商品が登録されていたら(含まれていなかったらNoneが返る)
        if is_pc4u_amd.get(title, None) is not None:
            # 辞書に登録されている価格を取得
            _sent_price = is_pc4u_amd[title]
            # もし辞書と現在の価格が違えば更新
            if price != _sent_price:
                is_pc4u_amd[title] = price
                print("#" * 50)
                print("価格が変更!!")
                print(title)
                print(is_pc4u_amd[title])
                print(url)
                await channel_sent.send(title)
                await channel_sent.send(is_pc4u_amd[title])
                await channel_sent.send(url)
            # 価格が同じ場合
            '''
            else:
                print("価格に変更はない")
                print(title)
                print(is_pc4u_amd[title])
                print(url)
            '''
        # 辞書に商品が登録されていなかったので価格を登録する
        else:            
            is_pc4u_amd[title] = price
            '''
            print("#" * 50)
            print("初回登録")
            print(title)
            print(is_pc4u_amd[title])
            print(url)
            '''

        if title is None:
            continue
    #print(is_pc4u_amd)

#PC4Uからnvidiaグラボの商品名と価格を取得
async def pc4u_nvidia():
    channel_sent = bot.get_channel(1019194136349392916)
    url = requests.get(
        "https://www.pc4u.co.jp/shopbrand/ct1850/page1/price/").content
    soup = BeautifulSoup(url, 'html.parser')
    #print(url)
    # await channel_sent.send("pc4u")
    for item in soup.find_all(class_="innerBox"): #商品の親要素divをクラス名で取得
        title = item.find(class_="name").text #itemからクラス名で商品名を取得
        price = item.find(class_="price").text #itemからクラス名で価格を取得
        url_temp = item.find('a') #itemからクラス名で価格を取得
        url = "https://www.pc4u.co.jp" + url_temp.get('href')


        # もし辞書に商品が登録されていたら(含まれていなかったらNoneが返る)
        if is_pc4u_nvidia.get(title, None) is not None:
            # 辞書に登録されている価格を取得
            _sent_price = is_pc4u_nvidia[title]
            # もし辞書と現在の価格が違えば更新
            if price != _sent_price:
                is_pc4u_nvidia[title] = price
                print("#" * 50)
                print("価格が変更!!")
                print(title)
                print(is_pc4u_nvidia[title])
                print(url)
                await channel_sent.send(title)
                await channel_sent.send(is_pc4u_nvidia[title])
                await channel_sent.send(url)
            # 価格が同じ場合
            '''
            else:
                print("価格に変更はない")
                print(title)
                print(is_pc4u_nvidia[title])
                print(url)
            '''
        # 辞書に商品が登録されていなかったので価格を登録する
        else:
            is_pc4u_nvidia[title] = price
            '''
            print("#" * 50)
            print("初回登録")
            print(title)
            print(is_pc4u_nvidia[title])
            print(url)
            '''


        if title is None:
            continue
    #print(is_pc4u_nvidia)


@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)


@bot.command()
async def ping(ctx):
    await pc4u_amd()
    await pc4u_nvidia()


token = getenv('DISCORD_BOT_TOKEN')
bot.run(token)

