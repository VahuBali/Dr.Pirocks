import discord
from discord.ext import commands
import json
import os
import random
import time

os.chdir("/app")

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

    await ctx.send(f"Dr.Pirocks felt generous for you and gave you {earnings} moolah!!")
    users[str(user.id)]["wallet"] += earnings

    with open("mainbank.json", "w") as f:
        json.dump(users,f)

@client.command()
async def withdraw(ctx, change, amount = None):
    await open_account(ctx.author)

    bal = await update_bank(ctx.author, change)

    amount = int(amount)

    if amount>bal[1]:
        await ctx.send("You don't have enough money")
        return

    if amount<0:
        await ctx.send("YOU CAN'T WITHDRAW A NEGATIVE AMOUNT")
        return

    if amount == None:
        await ctx.send("Please enter the amount")
        return

    await update_bank(ctx.author,amount)
    await update_bank(ctx.author,-1*amount, "bank")

    await ctx.send(f"You deposited {amount} coins!")


@client.command()
async def deposit(ctx, change, amount = None):
    await open_account(ctx.author)

    bal = await update_bank(ctx.author, change)

    amount = int(amount)

    if amount>bal[0]:
        await ctx.send("")
        return

    if amount<0:
        await ctx.send("YOU CAN'T WITHDRAW A NEGATIVE AMOUNT")
        return

    if amount == None:
        await ctx.send("Please enter the amount")
        return

    await update_bank(ctx.author,-1*amount)
    await update_bank(ctx.author,amount, "bank")

    await ctx.send(f"You withdrew {amount} coins!")


@client.command()
async def send(ctx,change, member:discord.Member, amount):
    await open_account(ctx.author)
    await open_account(member)

    bal = await update_bank(ctx.author, change)
    if amount == "all":
        amount = bal[0]
        
    amount = int(amount)

    if amount>bal[1]:
        await ctx.send("")
        return

    if amount<0:
        await ctx.send("YOU CAN'T WITHDRAW A NEGATIVE AMOUNT")
        return

    if amount == None:
        await ctx.send("Please enter the amount")
        return

    await update_bank(ctx.author,-1*amount, "bank")
    await update_bank(ctx.author,amount, "bank")

    await ctx.send(f"You gave {amount} coins!")


@client.command()
async def slots(ctx,change, amount):
    await open_account(ctx.author)

    bal = await update_bank(ctx.author,change)

    amount = int(amount)

    if amount>bal[0]:
        await ctx.send("")
        return

    if amount<0:
        await ctx.send("YOU CAN'T WITHDRAW A NEGATIVE AMOUNT")
        return

    if amount == None:
        await ctx.send("Please enter the amount")
        return

    final = []
    for i in range(3):
        a = random.choice(["X","O","Q"])

        final.append(a)

    await ctx.send(str(final))

    if final[0] == final[1] or final[0] == final[2] or final[1] == final[2]:
        await update_bank(ctx.author,2*amount)
        await ctx.send("CONGRATS FOR WINNING")
    else:
        await update_bank(ctx.author,-3*amount)
        await ctx.send("Welcome to Poverty")


@client.command()
async def rob(ctx, change, member:discord.Member):
    await open_account(ctx.author)
    await open_account(member)

    bal = await update_bank(member,change)

    if bal[0]<100:
        await ctx.send("Come on man why would you rob a peasent")
        return

    earnings = random.randrange(0,bal[0])

    await update_bank(ctx.author,earnings)
    await update_bank(ctx.author,-1*earnings, "wallet")

    await ctx.send(f"You stole {earnings} coins!")
    

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
    return True

async def get_bank_data():
    with open("mainbank.json","r") as f:
        users = json.load(f)
    return users

async def update_bank(user, change, mode = "wallet"):
    users = await get_bank_data()


    users[str(user.id)][mode] += change

    with open("mainbank.json", "w") as f:
        json.dump(users,f)

    bal = [users[str(user.id)]["wallet"],  users[str(user.id)]["bank"]]
    return bal
    

env = os.environ.get("BOT_TOKEN")

client.run(env)
