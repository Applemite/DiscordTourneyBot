import os
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
client = discord.Client()

win = "✔️"
loss = "🏳️"

players = {}
matches = {}

def testFunc():
    print(f'{client.user} has connected to Discord!')

def cleanAuthor(author):
    return author[:-5]

@client.event
async def on_ready():
    testFunc()

@client.event
async def on_message(message):
    author = cleanAuthor(str(message.author))
    if author == client.user:
        return

    if message.content == "!help".lower():
        await message.channel.send(
        "!init \n"
        "!viewWallet \n" +
        "!giveMM \n" +
        "!createBet"
        )
    elif message.content == "!init".lower():
        if players.get(author) == None:
            players[author] = 10
            print(str(author) + " has been added")
    elif message.content == "!createbet".lower():
        await message.add_reaction(win)
        await message.add_reaction(loss)
    elif message.content == "!viewwallet".lower():
        if not players.get(author) == None:
            await message.reply(str(author) + " has " + str(players[author]) + " monkey money")
    elif message.content == "!givemm":
        recipient = message.content.split(" ")[1]
        amount = message.content.split(" ")[2]
        if not players.get(author) == None and not players.get(recipient) == None:
            if players[author] >= amount:
                players[author] - amount
                players[recipient] + amount


@client.event
async def on_reaction_add(reaction, user):
    if not user.bot and reaction.message.content.startswith("!createbet"):
        print(user)
        if matches.has_key(reaction.message.content.split(" ")[1]):
            matches[reaction.message.content.split(" ")[1]].append(user)
        else:
            matches[reaction.message.content.split(" ")[1]] = [user]
    

client.run(TOKEN)