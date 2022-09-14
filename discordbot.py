import discord
import traceback
import requests
from discord.ext import commands
from discord.ext import tasks
from os import getenv
from datetime import datetime, timezone, timedelta, time
from bs4 import BeautifulSoup

bot = commands.Bot(command_prefix="/",intents=discord.Intents.all())

@tasks.loop(minutes=1)
async def send_message_every():
    channel_sent = bot.get_channel(1019194136349392916)
    t_delta = timedelta(hours=9)
    JST = timezone(t_delta, 'JST')
    now = datetime.now(JST).strftime('%A/%H:%M')
    await main()
    # await channel_sent.send("1分タスク" + now)
    if now == 'Friday/19:00':
        await channel_sent.send(now + "時間だよ")

@bot.event
async def on_ready():
    send_message_every.start()


"""楽天から商品名と価格を取得
def main():
    url = requests.get(
        "https://search.rakuten.co.jp/search/mall/%E3%83%9F%E3%83%83%E3%82%AF%E3%82%B9%E3%83%8A%E3%83%83%E3%83%84/").content
    soup = BeautifulSoup(url)
    #print(url)
    for item in soup.find_all(class_="dui-card searchresultitem"): #商品の親要素divをクラス名で取得
        print("#" * 50)
        #print(item.find("a", attrs={"data-track-trigger": "title", "target": "_top"}).text)
        #print(item.find(class_="important").text)
        title = item.find("a", attrs={"data-track-trigger": "title", "target": "_top"}).get("title") #itemからaタグのtitleで商品名を取得
        price = item.find(class_="important").text #itemからクラス名で価格を取得
        if title is None:
            continue
        print("-" * 50)
        print(title)
        print("-" * 50)
        print(price)
        


#PC4Uからグラボの商品名と価格を取得
def main():
    url = requests.get(
        "https://www.pc4u.co.jp/shopbrand/pciexpress4/page1/price/").content
    soup = BeautifulSoup(url)
    #print(url)
    for item in soup.find_all(class_="innerBox"): #商品の親要素divをクラス名で取得
        print("#" * 50)
        #print(item.find("a", attrs={"data-track-trigger": "title", "target": "_top"}).text)
        #print(item.find(class_="important").text)
        title = item.find(class_="name").text #itemからクラス名で商品名を取得
        price = item.find(class_="price").text #itemからクラス名で価格を取得
        if title is None:
            continue
        print("-" * 50)
        print(title)
        print("-" * 50)
        print(price)


if __name__ == "__main__":
    main()


is_pc4u = {}
#PC4Uからグラボの商品名と価格を取得
def main():
    channel_sent = bot.get_channel(1019194136349392916)
    url = requests.get(
        "https://www.pc4u.co.jp/shopbrand/pciexpress4/page1/price/").content
    soup = BeautifulSoup(url)
    #print(url)
    await channel_sent.send("a")
    for item in soup.find_all(class_="innerBox"): #商品の親要素divをクラス名で取得
        title = item.find(class_="name").text #itemからクラス名で商品名を取得
        price = item.find(class_="price").text #itemからクラス名で価格を取得
        url_temp = item.find('a') #itemからクラス名で価格を取得
        url = "https://www.pc4u.co.jp" + url_temp.get('href')
        print("#" * 50)
        
        # もし辞書に商品が登録されていたら(含まれていなかったらNoneが返る)
        if is_pc4u.get(title, None) is not None:
            # 辞書に登録されている価格を取得
            _sent_price = is_pc4u[title]
            # もし辞書と現在の価格が違えば更新
            if price != _sent_price:
                is_pc4u[title] = price
                print("価格が変更!!")
                print(title)
                print(is_pc4u[title])
            # 価格が同じ場合
            else:
                print("価格に変更はない")
                print(title)
                print(is_pc4u[title])
        # 辞書に商品が登録されていなかったので価格を登録する
        else:
            print("初回登録")
            is_pc4u[title] = price
            print(title)
            print(is_pc4u[title])
            print(url)

        
        if title is None:
            continue
    #print(is_pc4u)



if __name__ == "__main__":
    main()
"""

is_pc4u = {}
#PC4Uからグラボの商品名と価格を取得
async def main():
    channel_sent = bot.get_channel(1019194136349392916)
    url = requests.get(
        "https://www.pc4u.co.jp/shopbrand/pciexpress4/page1/price/").content
    soup = BeautifulSoup(url)
    #print(url)
    await channel_sent.send("pc4u")
    for item in soup.find_all(class_="innerBox"): #商品の親要素divをクラス名で取得
        title = item.find(class_="name").text #itemからクラス名で商品名を取得
        price = item.find(class_="price").text #itemからクラス名で価格を取得
        url_temp = item.find('a') #itemからクラス名で価格を取得
        url = "https://www.pc4u.co.jp" + url_temp.get('href')
        print("#" * 50)
        
        # もし辞書に商品が登録されていたら(含まれていなかったらNoneが返る)
        if is_pc4u.get(title, None) is not None:
            # 辞書に登録されている価格を取得
            _sent_price = is_pc4u[title]
            # もし辞書と現在の価格が違えば更新
            if price != _sent_price:
                is_pc4u[title] = price
                print("価格が変更!!")
                print(title)
                print(is_pc4u[title])
            # 価格が同じ場合
            else:
                print("価格に変更はない")
                print(title)
                print(is_pc4u[title])
        # 辞書に商品が登録されていなかったので価格を登録する
        else:
            print("初回登録")            
            is_pc4u[title] = price
            print(title)
            print(is_pc4u[title])
            print(url)

        
        if title is None:
            continue
    #print(is_pc4u)


@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)
    

@bot.command()
async def ping(ctx):
    await main()
    
    

token = getenv('DISCORD_BOT_TOKEN')
bot.run(token)

