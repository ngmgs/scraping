import discord
import traceback
# import requests
import asyncio
import aiohttp
import async_timeout
import time as t
import csv
import os
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
        
with open('is_pc4u_amd.csv', 'w') as f:  
    writer = csv.writer(f)            
    for k, v in is_pc4u_amd.items():
       writer.writerow([k, v])

        
async def fetch(session, url, dic):
    print("{} start".format(url))
    while True:
        async with async_timeout.timeout(100):
            async with session.get(url) as response:
                html = await response.text()
                soup = BeautifulSoup(html, "html.parser")
                
                url = await next_page(session, soup)
                '''
                if dic == False:
                    promises = [get_items(item, dic) for item in soup.find_all(class_="innerBox")]
                    await asyncio.gather(*promises)
                    return
                ''' 
                promises = [get_items(item, dic) for item in soup.find_all(class_="innerBox")]
                await asyncio.gather(*promises)
                
                if url is None:
                    break

                await asyncio.sleep(5)
                    
    return

async def get_items(item, dic):
    
    title = item.select_one('p.name').text  # itemからクラス名で商品名を取得
    price = item.select_one('p.price').text  # itemからクラス名で価格を取得
    stock = item.select_one('div.btnWrap > img')  #itemからクラス名で品切れ情報を取得
    
    
    dic[title] = {'price': price, 'stock': stock}

    print("#" * 50)
    print(title)
    print(dic[title]['price'])
    print(dic[title]['stock'])

    
    


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
    


              
'''     
        async with session.get(url) as response:
            html = await response.text()
            soup = BeautifulSoup(html, "html.parser")
            
            try:
                url_next = soup.select_one('li.next > a[href]:-soup-contains("次の50件")').get('href')
            except AttributeError:
                print("最後のページです")
            print(url_next)
            print(url)
    

    async with aiohttp.ClientSession() as session:

        async with session.get(url) as res:

            soup = BeautifulSoup(res, 'html.parser')
            try:
                url_next = soup.select_one('li.next > a[href]:-soup-contains("次の50件")').get('href')
            except AttributeError:
                print("最後のページです")
            print(url_next)
        
'''

    
"""
@tasks.loop(minutes=1)
async def send_message_every():
    channel_sent = bot.get_channel(1019194136349392916)
    t_delta = timedelta(hours=9)
    JST = timezone(t_delta, 'JST')
    now = datetime.now(JST).strftime('%A/%H:%M')
    url = "https://www.pc4u.co.jp/shopbrand/pciexpress4/page1/price/"
    print(now)
    await pc4u_get_vga(url, is_pc4u_amd)
    print(list(is_pc4u_amd.items())[0])
    await asyncio.sleep(5)
    url = "https://www.pc4u.co.jp/shopbrand/ct1850/page1/price/"
    await pc4u_get_vga(url, is_pc4u_nvidia)
    print(list(is_pc4u_nvidia.items())[0])
    
    # await pc4u_nvidia()


@bot.event
async def on_ready():
    send_message_every.start()  # ループ処理開始



#PC4Uからamdグラボの商品名と価格を取得
async def pc4u_get_vga(url, is_pc4u):
    channel_sent = bot.get_channel(1019194136349392916)
    session = requests.Session()
    res = session.get(url).content
    soup = BeautifulSoup(res, 'html.parser')
    # await channel_sent.send("pc4u")
    for item in soup.find_all(class_="innerBox"): #商品の親要素divをクラス名で取得
        title = item.find(class_="name").text #itemからクラス名で商品名を取得
        price = item.find(class_="price").text #itemからクラス名で価格を取得
        stock = item.find(class_="btnWrap").find('img') #itemからクラス名で品切れ情報を取得
        url_temp = item.find('a') #itemからクラス名で価格を取得
        url = "https://www.pc4u.co.jp" + url_temp.get('href')


        # もし辞書に商品が登録されていたら(含まれていなかったらNoneが返る)
        if is_pc4u.get(title, None) is not None:
            # 辞書に登録されている価格を取得
            _sent_price = is_pc4u[title]['price']
            # もし辞書と現在の価格が違えば更新
            if price != _sent_price:
                is_pc4u[title]['price'] = price
                print("#" * 50)
                print("価格が変更!!")
                print(title)
                print(is_pc4u[title])
                print(url)
                await channel_sent.send(title)
                await channel_sent.send(is_pc4u[title])
                await channel_sent.send(url)
            # 価格が同じ場合
            '''
            else:
                print("価格に変更はない")
                print(title)
                print(is_pc4u[title])
                print(url)
            '''
        # 辞書に商品が登録されていなかったので価格を登録する
        else:            
            is_pc4u[title] = {'price': price, 'stock': stock}

            '''
            print("#" * 50)
            print("初回登録")
            print(title)
            print(is_pc4u[title])
            print(url)
            print(stock)
            '''

        if title is None:
            continue
    #print(is_pc4u)
    #return is_pc4u

    while True:
        print(session)
        try:
            url_next = soup.select_one('li.next > a[href]:-soup-contains("次の50件")').get('href')
        except AttributeError:
            print("最後のページです")
            break
        url_next = soup.select_one('li.next > a[href]:-soup-contains("次の50件")').get('href')
        url = "https://www.pc4u.co.jp" + url_next
        print("次のページは")
        print(url)
        await asyncio.sleep(5)
        res = session.get(url).content
        soup = BeautifulSoup(res, 'html.parser')
    print("ブレイクしたよ")
'''
    t.sleep(5)
    res = requests.get(url).content
    soup = BeautifulSoup(res, 'html.parser')
    url_next = soup.select_one('li.next > a[href]:-soup-contains("次の50件")').get('href')
    url = "https://www.pc4u.co.jp" + url_next
    print(url)
    if url_next is None:
        print("2:次のページはない")
    else:
        print("2:次のページある")

    t.sleep(5)
    res = requests.get(url).content
    soup = BeautifulSoup(res, 'html.parser')
    try:
        url_next = soup.select_one('li.next > a[href]:-soup-contains("次の50件")').get('href')
    except AttributeError:
        print("最後のページです")
        return
    url = "https://www.pc4u.co.jp" + url_next
    print(url)
    if url_next is None:
        print("3次のページはない")
    else:
        print("3:次のページある")
'''
        

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
"""

@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)


@bot.command()
async def ping(ctx):
    url = "https://www.pc4u.co.jp/shopbrand/pciexpress4/page1/price/"
    await main()

@bot.command()
async def pank(ctx):
    my_dict = { 'Apple': 4, 'Banana': 2, 'Orange': 6, 'Grapes': 11}

    tf = open("myDictionary.json", "w")
    json.dump(my_dict,tf)
    tf.close()
    
@bot.command()
async def penk(ctx):
    tf = open("myDictionary.json", "r")
    new_dict = json.load(tf)
    print(new_dict)
    
token = getenv('DISCORD_BOT_TOKEN')
bot.run(token)
