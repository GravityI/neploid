import discord, json, asyncio, random, logging
from discord.ext import commands
import lib.ydkToJSON as ydk

bot = commands.Bot(command_prefix='ark ', description= "Nep Nep")

#get player file path for the player whom sent the message
playerFile = lambda ctx : "data/players/" + str(ctx.message.author.id) + '.json'

#checks if deck exists for the player whom sent the message
deckExists = lambda ctx, deckName : deckName in json.load(open(playerFile(ctx), "r"))["decks"].keys()

#joins all strings from given list, separating them by spaces
composeString = lambda words : "".join(list(map(lambda x : x + " ", words)))[:-1]

def compoundString(words):
    string = ""
    for word in words:
        string += str(word) + " "
    return string[:-1]

def createDeck(ctx, deckName):
    with open(playerFile(ctx), "r") as file:
        data = json.load(file)
        data["decks"][deckName] = {}
        json.dump(data, open(playerFile(ctx), "w"))
        file.close()


#print something when the bot is connected
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print('------')

#initialize player data
@bot.command(aliases = ["reset"], pass_context = True)
async def start(ctx):
    player = {
    "trunk": {},
    "decks": {"starter": {"main":{}}},
    "coins": 0,
    "wins": 0,
    "losses": 0,
    "draws": 0,
    "score": 0}
    
    with open(playerFile(ctx), 'w') as file:
        json.dump(player, file)
        file.close() 
    await ctx.send("Player created with success!")

@bot.command(aliases = ["d"], pass_context = True)
async def deck(ctx, *args):
    await ctx.send(args)
    deckName = composeString(args[1:])
    if args[0] in ["create", "c"] and len(args) >= 2:
        if deckExists(ctx, deckName):
            await ctx.send("There's already a deck named " + deckName + "!")
        else:
            createDeck(ctx, deckName)
            await ctx.send("Deck " + deckName + " created successfully!")
    elif args[0] in ["clear", "cl"] and len(args) >= 2:
        if deckExists(ctx, deckName):
            createDeck(ctx, deckName)
            await ctx.send("Deck" + deckName + " cleared sucessfully")
        else:
            await ctx.send("There's no deck named " + deckName + "!")

#To create a starter deck:
#Store a Card Pool
#Randomize 40 cards from given pool
#Add those 40 random cards to the player's main deck


#define bot token and run it
token = "insert token here"
bot.run(token)