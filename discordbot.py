import discord
import traceback
import requests
from discord.ext import commands
from discord.ext import tasks
from os import getenv
from datetime import datetime, timezone, timedelta, time
from bs4 import BeautifulSoup

bot = commands.Bot(command_prefix="/",intents=discord.Intents.all())


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
"""

is_pc4u = {}
#PC4Uからグラボの商品名と価格を取得
def main():
    url = requests.get(
        "https://www.pc4u.co.jp/shopbrand/pciexpress4/page1/price/").content
    soup = BeautifulSoup(url)
    #print(url)
    for item in soup.find_all(class_="innerBox"): #商品の親要素divをクラス名で取得
        print("#" * 50)
        title = item.find(class_="name").text #itemからクラス名で商品名を取得
        price = item.find(class_="price").text #itemからクラス名で価格を取得
        is_pc4u[title] = price
        print(str(is_pc4u[title].keys()) + ":" + is_pc4u[title])
        if title is None:
            continue
    #print(is_pc4u)



if __name__ == "__main__":
    main()


@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)
    

@bot.command()
async def ping(ctx):
    main()
    
    

token = getenv('DISCORD_BOT_TOKEN')
bot.run(token)

