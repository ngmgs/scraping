import discord
import traceback
# import requests
import asyncio
import aiohttp
import async_timeout
import time as t
import json
from discord.ext import commands
from discord.ext import tasks
from os import getenv
from datetime import datetime, timezone, timedelta, time
from bs4 import BeautifulSoup

bot = commands.Bot(command_prefix="/",intents=discord.Intents.all())


is_pc4u_amd = {}
is_pc4u_nvidia = {}


async def main():
    
    async with aiohttp.ClientSession() as session:
        urls = {
            'https://www.pc4u.co.jp/shopbrand/pciexpress4/page1/price/': is_pc4u_amd,
            # 'https://www.pc4u.co.jp/shopbrand/ct1850/page1/price/': is_nvidia,
        }
        promises = [fetch(session, url, dic) for url, dic in urls.items()]
        print(promises)
        await asyncio.gather(*promises)


async def fetch(session, url, dic):
    print("{} start".format(url))


    while True:
        async with async_timeout.timeout(100):
            async with session.get(url) as response:
                html = await response.text()
                soup = BeautifulSoup(html, "html.parser")

                # もし辞書が空の時（再起動等で辞書が空のとき）
                if any(dic) == False:
                    while True:                        
                        promises = [first_items(item, dic) for item in soup.find_all(class_="innerBox")]
                        await asyncio.gather(*promises)

                        url = await next_page(session, soup)

                        if url is None:
                            break

                        await asyncio.sleep(5)
                        async with session.get(url) as response:
                            html = await response.text()
                            soup = BeautifulSoup(html, "html.parser")
                            
                        print("辞書に全アイテム登録完了")
                    return

                promises = [get_items(item, dic) for item in soup.find_all(class_="innerBox")]
                await asyncio.gather(*promises)


                url = await next_page(session, soup)

                if url is None:
                    break

                await asyncio.sleep(5)

    return

async def first_items(item, dic):

    title = item.select_one('p.name').text  # itemからクラス名で商品名を取得
    price = item.select_one('p.price').text  # itemからクラス名で価格を取得
    stock = item.select_one('div.btnWrap > img')  #itemからクラス名で品切れ情報を取得

    dic[title] = {'price': price, 'stock': stock}


async def get_items(item, dic):
    channel_sent = bot.get_channel(1019194136349392916)
    title = item.select_one('p.name').text  # itemからクラス名で商品名を取得
    price = item.select_one('p.price').text  # itemからクラス名で価格を取得
    stock = item.select_one('div.btnWrap > img')  #itemからクラス名で品切れ情報を取得


    # もし辞書に商品が登録されていたら(含まれていなかったらNoneが返る)
    if dic.get(title, None) is not None:
        # 辞書に登録されている価格を取得
        _sent_price = dic[title]['price']
        # もし現在の価格と辞書の価格が違えば更新
        if price != _sent_price:
            dic[title]['price'] = price
            print("#" * 50)
            print("価格が変更!!")
            print(title)
            print(_sent_price + " ⇒ " + dic[title]['price'])
            print(url)
            await channel_sent.send("価格変更")
            await channel_sent.send(title)
            await channel_sent.send(_sent_price + " ⇒ " + dic[title]['price'])
            await channel_sent.send(url)
        # 価格が同じ場合
        '''
        else:
            print("価格に変更はない")
            print(title)
            print(dic[title])
            print(url)
        '''
    # 辞書に商品が登録されていなかったので価格を登録する
    else:
        dic[title] = {'price': price, 'stock': stock}

        print("新規登録")

        await channel_sent.send("新規登録")
        await channel_sent.send(title)
        await channel_sent.send(dic[title]['price'])
        await channel_sent.send(url)




async def next_page(session, soup):
    try:
        url_next = soup.select_one('li.next > a[href]:-soup-contains("次の50件")').get('href')
    except AttributeError:
        print("最後のページです")
        return
    url_next = soup.select_one('li.next > a[href]:-soup-contains("次の50件")').get('href')
    url = "https://www.pc4u.co.jp" + url_next
    print("次のページは")
    print(url)
    return url


@bot.command()
async def ping(ctx):
    await main()

@bot.command()
async def pank(ctx):
    my_dict = { 'Apple': 4, 'Banana': 2, 'Orange': 6, 'Grapes': 11}

    tf = open("/tmp/myDictionary.json", "w")
    json.dump(my_dict,tf)
    tf.close()
    
@bot.command()
async def penk(ctx):
    tf = open("/tmp/myDictionary.json", "r")
    new_dict = json.load(tf)
    print(new_dict)
    
token = getenv('DISCORD_BOT_TOKEN')
bot.run(token)
