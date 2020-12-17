import discord
from discord.ext import commands
import json
import os
import random
import time

os.chdir("/Users/vasu/Desktop/DiscordBot/")

client = commands.Bot(command_prefix="vb ")

@client.event
async def on_ready():
    print("Bot is ready")

@client.command()
async def hello(ctx):
    await ctx.send("hey")

@client.command()
async def balance(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    wallet_amt = users[str(user.id)]["wallet"]
    bank_amt = users[str(user.id)]["bank"]



    em = discord.Embed(title = f"{ctx.author.name}'s balance", color = discord.Color.red())
    em.add_field(name = "Wallet", value = wallet_amt)
    em.add_field(name = "Bank Balance", value = bank_amt)
    await ctx.send(embed = em)


@client.command()
async def beg(ctx):
    await open_account(ctx.author)
    
    users = await get_bank_data()

    user = ctx.author

    earnings = random.randrange(0,101)

    await ctx.send(f"Dr.Pirocks felt generous for you and gave you {earnings} coins!!")
    users[str(user.id)]["wallet"] += earnings

    with open("mainbank.json", "w") as f:
        json.dump(users,f)

async def open_account(user):
    with open("mainbank.json", "r") as f:
         users = json.load(f)

    if str(user.id) in users:
        return False

    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0

    with open("mainbank.json", "w") as f:
        json.dump(users,f)

async def get_bank_data():
    with open("mainbank.json","r") as f:
        users = json.load(f)
    return users



client.run(process.env.Nzg4ODk1NjI4NTExMjgxMTgy.X9qKTg.C8GU8Bt9SyV_AtqHzAXkXNoVSAg)