import os
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
client = discord.Client()

win = "🏆"
loss = "🏳️"

players = {}
matches = {}

def testFunc():
    print(f'{client.user} has connected to Discord!')

def cleanAuthor(author):
    return author[:-5]

def save():
    file1 = open("data.txt", "w")
    for key in players:
        file1.write(str(key) + "#" + str(players[key]))
    file1.close()

def load():
    file1 = open("data.txt", "r")
    for line in file1.readlines():
        players[line.split("#")[0]] = int(line.split("#")[1])
    file1.close()

@client.event
async def on_ready():
    testFunc()
    load()
    print("players" + str(players))

@client.event
async def on_message(message):
    author = cleanAuthor(str(message.author))
    messageContent = message.content.lower()
    if author == client.user:
        return

    if messageContent == "!help":
        await message.channel.send(
        "!init \n"
        "!viewWallet \n" +
        "!giveMM (Name of recipient) (amount) \n" +
        "!createBet"
        )
    elif messageContent == "!init":
        if not players.get(author) == None:
            await message.reply("You are already initialized")
            return

        print(str(author) + " has been added")
        players[author] = 10
        save()
    elif messageContent == "!createbet":
        await message.add_reaction(win)
        await message.add_reaction(loss)
        save()
    elif messageContent == "!viewwallet":
        if players.get(author) == None:
            await message.reply("You need to initialize check !help")
            return

        print(str(author) + " has " + str(players[author]) + " monkey money")
        await message.reply(str(author) + " has " + str(players[author]) + " monkey money")  
    elif messageContent.startswith("!givemm"):
        print(message.content)
        splitMessage = message.content.split(" ")
        if len(splitMessage) != 3:
            await message.reply("Not enough arguments check !help")
            return

        recipient = splitMessage[1]

        if not splitMessage[2].isdigit():
            await message.reply("Only positive numbers")
            return
        amount = int(splitMessage[2])

        if players.get(author) == None or players.get(recipient) == None:
            await message.reply("Person does not exist or is not initalized")
            return
        
        if players[author] >= amount:
            await message.reply("You do not have enough monkey money")
            return

        print(str(author) + " lost " + str(amount) + " and " + str(recipient) + " gained " + str(amount))
        await message.reply(str(author) + " lost " + str(amount) + " and " + str(recipient) + " gained " + str(amount))
        players[author] - amount
        players[recipient] + amount
        save()


@client.event
async def on_reaction_add(reaction, user):
    if not user.bot and reaction.message.content.startswith("!createbet"):
        print(user)
        if matches.has_key(reaction.message.content.split(" ")[1]):
            matches[reaction.message.content.split(" ")[1]].append(user)
        else:
            matches[reaction.message.content.split(" ")[1]] = [user]
    

client.run(TOKEN)