import discord
import traceback
import requests
from discord.ext import commands
from discord.ext import tasks
from os import getenv
from datetime import datetime, timezone, timedelta, time
from bs4 import BeautifulSoup

bot = commands.Bot(command_prefix="/",intents=discord.Intents.all())



def main():
    url = requests.get(
        "https://search.rakuten.co.jp/search/mall/%E3%83%9F%E3%83%83%E3%82%AF%E3%82%B9%E3%83%8A%E3%83%83%E3%83%84/").content
    soup = BeautifulSoup(url)
    #print(url)
    for item in soup.find_all(class_="dui-card searchresultitem"):
        print("#" * 50)
        print(item)
        print(item.text)
        title = item.get("title")
        if title is None:
            continue
        print("-" * 50)
        print(title)


if __name__ == "__main__":
    main()



@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)
    

@bot.command()
async def ping(ctx):
    await ctx.send(discord.__version__)
    
    

token = getenv('DISCORD_BOT_TOKEN')
bot.run(token)
