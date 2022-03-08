import os
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

START_AMOUNT = 10
FUNCTION_PRE = "!"
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
        file1.write(str(key) + "#" + str(players[key]) + "\n")
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
    for guild in client.guilds:
        for member in guild.members:
            cleanedMembers = cleanAuthor(str(member))
            if players.get(cleanedMembers) == None:
                players[cleanedMembers] = START_AMOUNT
                save()
    #print("players" + str(players))

@client.event
async def on_member_join(member):
    cleanedMembers = cleanAuthor(str(member))
    if players.get(cleanedMembers) == None:
        players[cleanedMembers] = START_AMOUNT
        save()

@client.event
async def on_message(message):
    author = cleanAuthor(str(message.author))
    messageContent = message.content.lower()
    if author == client.user:
        return

    if messageContent == FUNCTION_PRE + "help":
        await message.channel.send(
        FUNCTION_PRE + "viewWallet \n" +
        FUNCTION_PRE + "giveMM (Name of recipient) (amount) \n" +
        FUNCTION_PRE + "createBet"
        )
    elif messageContent == FUNCTION_PRE + "createbet":
        await message.add_reaction(win)
        await message.add_reaction(loss)
        save()
    elif messageContent == FUNCTION_PRE + "viewwallet":
        if players.get(author) == None:
            await message.reply("You need to initialize check !help")
            return

        #print(str(author) + " has " + str(players[author]) + " monkey money")
        await message.reply(str(author) + " has " + str(players[author]) + " monkey money")  
    elif messageContent.startswith(FUNCTION_PRE + "givemm"):
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
            await message.reply("Person does not exist")
            return
        
        if author == recipient:
            await message.reply("You can not give yourself monkey money")
            return
        
        if players[author] >= amount:
            await message.reply("You do not have enough monkey money")
            return

        #print(str(author) + " lost " + str(amount) + " and " + str(recipient) + " gained " + str(amount))
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