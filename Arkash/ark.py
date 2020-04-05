#Convite pro bot: https://discordapp.com/api/oauth2/authorize?client_id=560206824205189130&permissions=2013654128&scope=bot

import discord
import random
import asyncio
import logging
import urllib.request
import json
import os
from discord.ext import commands

bot = commands.Bot(command_prefix='ark ', description= "Nep Nep")
counter = 0
resetInterval = 120
countTask = None

memberPath = lambda ctx : "members/" + str(ctx.message.author.id) + '.json'

def createMember(ctx):
    user = {
        "name": str(ctx.message.author),
        "rolls": 5,
        "battlers": {},
        "inventory": {}
        }
    with open(memberPath(ctx), 'w') as file:
        json.dump(user, file)
        file.close()

def getMemberData(ctx):
    with open(memberPath(ctx), 'r') as file:
        user = json.load(file)
        file.close()
        return user

def updateName(ctx, *content):
    user = getMemberData(ctx)
    newName = ''
    for c in content:
        newName += c + ' '
    user["name"] = newName
    with open(memberPath(ctx), 'w') as file:
        json.dump(user, file)

def updateRolls(ctx, increment):
    user = getMemberData(ctx)
    user["rolls"] += increment
    with open(memberPath(ctx), 'w') as file:
        json.dump(user, file)

def updateBattlers(ctx, battlerName, increment):
    user = getMemberData(ctx)
    if battlerName in user["battlers"].keys():
        user["battlers"][battlerName] += increment
    else:
        user["battlers"][battlerName] = increment
    if user["battlers"][battlerName] == 0:
        user["battlers"].pop(battlerName)
    with open(memberPath(ctx), 'w') as file:
        json.dump(user, file)
    
def updateInventory(ctx, item, increment):
    user = getMemberData(ctx)
    if item in user["inventory"].keys():
        user["inventory"][item] += increment
    else:
        user["inventory"][item] = increment
    user["inventory"][item] += increment
    if user["inventory"][item] == 0:
        user["inventory"].pop(item)
    with open(memberPath(ctx), 'w') as file:
        json.dump(user, file)

def increaseAllRolls():
    for filename in os.listdir("members"):
        with open("members/" + filename + ".json", "r+") as file:
            user = json.load(file)
            user["rolls"] += 1
            json.dump(user, "members/" + filename + ".json")
            file.close()

def rollRarity(box):
    with open("droprates.json", "r") as file:
        data = json.load(file)
        boxData = data[box]
        file.close()
    randomGen = random.random()
    probability = 0
    for drop in boxData:
        if probability <= randomGen <= probability + drop["droprate"]:
            return drop["battler"]
        else:
            probability += drop["droprate"]

def randomBattler(rarity):
    with open("battlers/battlers.json", "r") as file:
        data = json.load(file)
        selected = random.choice(list(data[rarity].keys()))
        return (selected, data[rarity][selected])

def getBattler(battlerName):
    with open("battlers/battlers.json", "r") as file:
        data = json.load(file)
        for rarities in data.values():
            for battler in rarities.keys():
                if battlerName.lower() == battler.lower():
                    return (battler, rarities[battler])
    return None

def battlerData(battlerName):
    battler = getBattler(battlerName)
    if battler == None:
        return None
    else:
        return [battlerName.upper(), discord.File("battlers/images/" + battler[1]["image"] + ".png", battler[1]["image"] + ".png" ), "STATS" + '\n' + "-----" + '\n' + "ATTACK: " + str(battler[1]["attack"]) + '\n' + "HEALTH: " + str(battler[1]["health"]) + '\n' + "FORGE POINTS: " + str(battler[1]["forgePoints"]) + '\n' + "RARITY: " + battler[1]["rarity"].upper() + '\n' + "-----"]


def battlerEmbed(battlerName):
    battler = getBattler(battlerName)
    battlerImage = "https://i.imgur.com/" + battler[1]["image"] + ".png"
    embed=discord.Embed(title=battler[0], description=battler[1]["rarity"], color=0x289393)
    embed.set_author(name="Battler", icon_url="https://www.inova.com.br/wp-content/uploads/2017/03/ubuntu-icon.png")
    #embed.set_thumbnail(url=battlerImage)
    embed.add_field(name="attack", value=battler[1]["attack"])
    embed.add_field(name="health", value=battler[1]["health"], inline=False)
    embed.add_field(name="forge points", value=battler[1]["forgePoints"], inline=False)
    embed.set_image(url = battlerImage)
    embed.set_footer(text=battler[1]["box"])
    return embed

def addToMarket():
    pass

def removeFromMarket():
    pass

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
#    print(bot.user.id)
    print('------')

@bot.command(pass_context = True)
async def start(ctx):
    createMember(ctx)
    await ctx.send("User created with Success!")

'''
@bot.command(pass_context = True)
async def prefix(ctx, prefix):
    bot.command_prefix = prefix
    await ctx.send("Prefix successfully updated to " + bot.command_prefix)
'''

@bot.command(aliases = ["rr", "rollr"])
async def rollreset(ctx):
    if counter >= resetInterval:
        await ctx.send("The rolls for this server are already reset")
    else:
        await ctx.send("You must wait " + str(resetInterval - counter) + " minutes before rolling again")

async def rollCounter(channel):
    global counter
    while not bot.is_closed():
        counter += 1
        await channel.send("Count is at " + str(counter))
        await asyncio.sleep(60)
        if counter >= resetInterval:
            increaseAllRolls()
            counter -= resetInterval
            await channel.send("Rolls have been added for all players!")

@bot.command(pass_context = True)
async def gamestart(ctx):
    global countTask
    await ctx.send("Countdown Started!")
    countTask = bot.loop.create_task(rollCounter(ctx.message.channel))

@bot.command(pass_context = True, aliases = ["cancel", "stop"])
async def cc(ctx):
    global countTask
    await ctx.send("Countdown Cancelled!")
    countTask.cancel()

@bot.command(pass_context = True)
async def roll(ctx, box):
    user = getMemberData(ctx)
    if user["rolls"] >= 1:
        rarity = rollRarity(box.lower())
        result = randomBattler(rarity)
        battlerName = result[0]
        battler = getBattler(battlerName)
        if battler == None:
            await ctx.send("Battler not found. Are you sure you typed its name correctly?")
        else:
            await ctx.send(embed = battlerEmbed(battlerName))
            updateBattlers(ctx, battlerName, 1)
            updateRolls(ctx, -1)
            await ctx.send("Battler successfully added to your inventory! You now have " + str(user["rolls"] - 1) + " rolls available.")
    else:
        await ctx.send("You do not have available rolls")

@bot.command(pass_context = True)
async def battler(ctx, *content):
    battlerName = ""
    for x in content:
        battlerName += x + " "
    battlerName = battlerName[:len(battlerName) - 1]
    battler = getBattler(battlerName)
    if battler == None:
        await ctx.send("Battler not found. Are you sure you typed its name correctly?")
    else:
        await ctx.send(embed = battlerEmbed(battlerName))

token = "insert token here"

bot.run(token)