import discord
import random
import asyncio
import logging
import urllib.request
from discord.ext import commands

bot = commands.Bot(command_prefix='nep ', description= "Nep Nep")
counter = 0
countTask = None

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
#    print(bot.user.id)
    print('------')

@bot.command()
async def nep(ctx):
    await ctx.send("NEP NEP")

@bot.command(pass_context = True)
async def guessWhat(ctx):
    await ctx.send(str(ctx.message.author.display_name) + " officially learned how to code a Discord bot")

async def countdown(channel):
    global counter
    while not bot.is_closed():
        counter += 1
        await channel.send("Count is at " + str(counter))
        await asyncio.sleep(3)

@bot.command(pass_context = True, aliases = ["collect"])
async def sc(ctx):
    global countTask
    await ctx.send("Countdown Started!")
    countTask = bot.loop.create_task(countdown(ctx.message.channel))

@bot.command(pass_context = True, aliases = ["cancel", "stop"])
async def cc(ctx):
    global countTask
    await ctx.send("Countdown Cancelled!")
    countTask.cancel()

@bot.command(pass_context = True)
async def pm(ctx, *content):
    if ctx.author.dm_channel is not None:
        await ctx.author.dm_channel.send(content)
    else:
        await ctx.author.create_dm()
        sendString = ''
        for c in content:
            sendString += c + ' '
        await ctx.author.dm_channel.send(sendString)

@bot.command(aliases = ['nh'])
async def nhentai(ctx):
    rurl = "https://nhentai.net/random/"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    accessHurl = urllib.request.urlopen(urllib.request.Request(rurl, headers = headers))
    await ctx.send(accessHurl.geturl())

token = "insert token here"

bot.run(token)