import discord
import traceback
from discord.ext import commands
from discord.ext import tasks
from os import getenv
from datetime import datetime, timezone, timedelta, time


bot = commands.Bot(command_prefix="/",intents=discord.Intents.all())






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
