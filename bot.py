import discord
from discord.ext import commands
import json
import os
import math
import random
import praw
import datetime
import asyncio

from PIL import Image
from io import BytesIO


reddit = praw.Reddit(client_id = "AjkL0nqGEdPZYw",
                     client_secret = "5kVlWhM_E7Jm2ZijsOmSCJyg79p6lg",
                     username = "Vahu-Bali",
                     password = "Vasu@5950",
                     user_agent = "pythonmemepraw")

os.chdir("/app")


client = commands.Bot(command_prefix = "vb ")


mainshop = [{"name":"Watch", "price": 1000, "description": "Check Time"},
            {"name":"Laptop", "price": 3000, "description": "Google Things"},
            {"name":"Phone", "price": 7000, "description": "Call"}]



@client.event
async def on_ready():
    # Setting `Playing ` status
    await client.change_presence(activity=discord.Game(name=f"on {len(client.guilds)} servers | vb "))

    # Setting `Streaming ` status
    await client.change_presence(activity=discord.Streaming(name="My YouTube", url="https://www.youtube.com/channel/UCCzfHZSA8nEnx_QTFlq6mHA"))

    # Setting `Listening ` status
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Talk Tech Teen Tech"))

    # Setting `Watching ` status
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="M1 Mac Buyers Guide | Vasu Bansal"))
    print("Bot is ready")

async def ch_pr():
    await client.wait_until_ready()

    statuses = [f"on {len(client.guilds)} servers | vb ", "Check out the Talk Tech Teen Tech podcast", "Subscribe to the Vasu Bansal YouTube at bit.do/vasuyt"]

    while not client.is_closed():

        status = random.choice(statuses)

        await client.change_presence(activity = discord.Game(name = status))

        await asyncio.sleep(10)

client.loop.create_task(ch_pr())

@client.command()
async def meme(ctx):

    subreddit = reddit.subreddit("memes")
    all_subs = []
    top = subreddit.top(limit = 50)

    for submission in top:
        all_subs.append(submission)

    random_sub = random.choice(all_subs)

    name = random_sub.title
    url = random_sub.url

    em = discord.Embed(title = name)

    em.set_image(url = url)

    await ctx.send(embed = em)


@client.command()
async def hello(ctx):
    await ctx.send("hey")

@client.command()
async def youtube(ctx):
    await ctx.send("Vasu Bansal's YouTube channel can be found at https://www.youtube.com/channel/UCCzfHZSA8nEnx_QTFlq6mHA")

@client.command()
async def podcast(ctx):
    await ctx.send("Vasu Bansal's Podcast can be found at https://redcircle.com/talk-tech-teen-tech or on Spotify, Apple Podcasts, or anywhere you listen to your podcasts!")

@client.command()
async def joindis(ctx):
    await ctx.send("Join the vbYT discord where you can also ask any questions about this bot using this link https://discord.gg/npzKUsG9PS")

@client.command()
async def inv(ctx):
    await ctx.send("Get the Admins to click this link to add this bot https://discord.com/api/oauth2/authorize?client_id=788895628511281182&permissions=8&scope=bot")

@client.command(pass_context=True)
async def bal(ctx, member: discord.Member = None):
    await open_account(ctx.author)

    user = ctx.author

    users = await get_bank_data()

    wallet_amt = users[str(user.id)]["wallet"]

    bank_amt = users[str(user.id)]["bank"]

    embed = discord.Embed(title=f"{ctx.author.name}'s balance", color=0xFF69B4)

    embed.add_field(name= "Wallet Balance", value= wallet_amt,inline = False)
    embed.add_field(name= "Bank Balance", value= bank_amt,inline = False)

    await ctx.send(embed = embed)

@client.command(pass_context=True)
async def beg(ctx):
    await open_account(ctx.author)

    user = ctx.author

    users = await get_bank_data()

    


    earnings = random.randrange(101)

    await ctx.send(f"**Dr.Pirocks gave you {earnings} moolah now use this money to do something good for the planet!!**")

    users[str(user.id)]["wallet"] += earnings

    with open("mainbank.json", "w") as f:
        json.dump(users,f)

@client.command(pass_context=True)
async def withdraw(ctx,amount = None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send("**Please enter the amount**")
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)

    if amount>bal[1]:
        await ctx.send("**You dont have that much money!!**")
        return
    if amount<0:
        await ctx.send("**Amount must be positive**")
        return

    await update_bank(ctx.author,amount)
    await update_bank(ctx.author,-1*amount,"bank")

    await ctx.send(f"**you withdrew {amount} moolah!**")

@client.command(pass_context=True)
async def dep(ctx,amount = None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send("**Please enter the amount**")
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)

    if amount>bal[0]:
        await ctx.send("**You dont have that much money!!**")
        return
    if amount<0:
        await ctx.send("**Amount must be positive**")
        return

    await update_bank(ctx.author,-1*amount)
    await update_bank(ctx.author,amount,"bank")

    await ctx.send(f"**you deposited {amount} moolah!**")


@client.command(pass_context=True)
async def pay(ctx,member: discord.Member, amount = None):
    await open_account(ctx.author)
    await open_account(member)
    if amount == None:
        await ctx.send("**Please enter the amount**")
        return

    bal = await update_bank(ctx.author)

    if amount == "all":
        amount = bal[0]




    amount = int(amount)

    if amount>bal[1]:
        await ctx.send("**You dont have that much money!!**")
        return
    if amount<0:
        await ctx.send("**Amount must be positive**")
        return

    await update_bank(ctx.author,-1*amount,"bank")
    await update_bank(member,amount,"bank")

    await ctx.send(f"**you paid {amount} moolah!**")

@client.command(pass_context=True)
async def rob(ctx,member: discord.Member):
    await open_account(ctx.author)
    await open_account(member)
   
    bal = await update_bank(member)

    

    if bal[0]<100:
        await ctx.send("It's not worth it")
        return

    earnings = random.randrange(0, bal[0])
  

    await update_bank(ctx.author,earnings)
    await update_bank(member,-1*earnings)

    await ctx.send(f"you robbed and got {earnings} moolah!")


@client.command(pass_context=True)
async def slots(ctx, amount = None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send("Please enter the amount")
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)

    if amount>bal[0]:
        await ctx.send("You dont have that much money!!")
        return
    if amount<0:
        await ctx.send("Amount must be positive")
        return

    final = []
    for i in range(3):
        a = random.choice([":poop:", ":smile:", ":cherry_blossom:"])

        final.append(a)

    await ctx.send(str(final))

    if final[0] == final[1] or final[0] == final[2] or final[2] == final[1]:
         await update_bank(ctx.author,2*amount)
         await ctx.send("**you won!**")

    else:
        await update_bank(ctx.author,-1*amount)
        await ctx.send("**you lost!**")

@client.command()
async def shop(ctx):
    em = discord.Embed(title = "Shop")

    for item in mainshop:
        name = item["name"]
        price = item["price"]
        desc = item["description"]
        em.add_field(name = name, value = f"{price} | {desc}")

    await ctx.send(embed = em)

@client.command(pass_context =True)
async def buy(ctx, item, amount = 1):
    await open_account(ctx.author)

    res = await buy_this(ctx.author, item, amount)

    if not res [0]:
        if res[1] == 1:
            await ctx.send("Thathobject isn't there!")
            return
        if res[1] == 2:
            await ctx.send(f"You don't have that much Moolah in your wallet to buy {amount}")
            return
        
    await ctx.send(f"You just bought {amount} {item}")


@client.command()
async def bag(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    try:
        bag = users[str(user.id)]["bag"]
    except:
        bag = []


    em = discord.Embed(title = "Bag")
    for item in bag:
        name = item["item"]
        amount = item["amount"]

        em.add_field(name = name, value = amount)    

    await ctx.send(embed = em)  


async def buy_this(user,item_name,amount):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            price = item["price"]
            break

    if name_ == None:
        return [False,1]

    cost = price*amount

    users = await get_bank_data()

    bal = await update_bank(user)

    if bal[0]<cost:
        return [False,2]


    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt + amount
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index+=1 
        if t == None:
            obj = {"item":item_name , "amount" : amount}
            users[str(user.id)]["bag"].append(obj)
    except:
        obj = {"item":item_name , "amount" : amount}
        users[str(user.id)]["bag"] = [obj]        

    with open("mainbank.json","w") as f:
        json.dump(users,f)

    await update_bank(user,cost*-1,"wallet")

    return [True,"Worked"]

@client.command(pass_context=True)
async def sell(ctx,item,amount = 1):
    await open_account(ctx.author)

    res = await sell_this(ctx.author,item,amount)

    if not res[0]:
        if res[1]==1:
            await ctx.send("That Object isn't there!")
            return
        if res[1]==2:
            await ctx.send(f"You don't have {amount} {item} in your bag.")
            return
        if res[1]==3:
            await ctx.send(f"You don't have {item} in your bag.")
            return

    await ctx.send(f"You just sold {amount} {item}.")

async def sell_this(user,item_name,amount,price = None):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            if price==None:
                price = 0.9* item["price"]
            break

    if name_ == None:
        return [False,1]

    cost = price*amount

    users = await get_bank_data()

    bal = await update_bank(user)


    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt - amount
                if new_amt < 0:
                    return [False,2]
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index+=1 
        if t == None:
            return [False,3]
    except:
        return [False,3]    

    with open("mainbank.json","w") as f:
        json.dump(users,f)

    await update_bank(user,cost,"wallet")

    return [True,"Worked"]


@client.command(aliases = ["lb"])
async def leaderboard(ctx,x = 5):
    users = await get_bank_data()
    leader_board = {}
    total = []
    for user in users:
        name = int(user)
        total_amount = users[user]["wallet"] + users[user]["bank"]
        leader_board[total_amount] = name
        total.append(total_amount)

    total = sorted(total,reverse=True)    

    em = discord.Embed(title = f"Top {x} Richest People" , description = "This is decided on the basis of raw money in the bank and wallet",color = discord.Color(0xfa43ee))
    index = 5
    for amt in total:
        id_ = leader_board[amt]
        member = client.get_user(id_)
        name = member.name
        em.add_field(name = f"{index}. {name}" , value = f"{amt}",  inline = False)
        if index == x:
            break
        else:
            index += 1

    await ctx.send(embed = em)


@client.command()
@commands.has_role("Giveaways")
async def gstart(ctx, mins : int, * , prize: str):
    embed = discord.Embed(title = "Giveaway!", description = f"{prize}", color = ctx.author.color)

    end = datetime.datetime.utcnow() + datetime.timedelta(seconds = mins*60) 

    embed.add_field(name = "Ends At:", value = f"{end} UTC")
    embed.set_footer(text = f"Ends {mins} mintues from now!")

    my_msg = await ctx.send(embed = embed)


    await my_msg.add_reaction("🎉")


    await asyncio.sleep(mins*60)


    new_msg = await ctx.channel.fetch_message(my_msg.id)


    users = await new_msg.reactions[0].users().flatten()
    users.pop(users.index(client.user))

    winner = random.choice(users)

    await ctx.send(f"Congratulations! {winner.mention} won {prize}!")


def convert(time):
    pos = ["s","m","h","d"]

    time_dict = {"s" : 1, "m" : 60, "h" : 3600 , "d" : 3600*24}

    unit = time[-1]

    if unit not in pos:
        return -1
    try:
        val = int(time[:-1])
    except:
        return -2


    return val * time_dict[unit]

@client.command()
@commands.has_role("Owner")
async def giveaway(ctx):
    await ctx.send("Let's start with this giveaway! Answer these questions within 15 seconds!")

    questions = ["Which channel should it be hosted in?", 
                "What should be the duration of the giveaway? (s|m|h|d)",
                "What is the prize of the giveaway?"]

    answers = []

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel 

    for i in questions:
        await ctx.send(i)

        try:
            msg = await client.wait_for('message', timeout=15.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send('You didn\'t answer in time, please be quicker next time!')
            return
        else:
            answers.append(msg.content)

    try:
        c_id = int(answers[0][2:-1])
    except:
        await ctx.send(f"You didn't mention a channel properly. Do it like this {ctx.channel.mention} next time.")
        return

    channel = client.get_channel(c_id)

    time = convert(answers[1])
    if time == -1:
        await ctx.send(f"You didn't answer the time with a proper unit. Use (s|m|h|d) next time!")
        return
    elif time == -2:
        await ctx.send(f"The time must be an integer. Please enter an integer next time")
        return            

    prize = answers[2]

    await ctx.send(f"The Giveaway will be in {channel.mention} and will last {answers[1]}!")


    embed = discord.Embed(title = "Giveaway!", description = f"{prize}", color = ctx.author.color)

    embed.add_field(name = "Hosted by:", value = ctx.author.mention)

    embed.set_footer(text = f"Ends {answers[1]} from now!")

    my_msg = await channel.send(embed = embed)


    await my_msg.add_reaction(":tada:")


    await asyncio.sleep(time)


    new_msg = await channel.fetch_message(my_msg.id)


    users = await new_msg.reactions[0].users().flatten()
    users.pop(users.index(client.user))

    winner = random.choice(users)

    await channel.send(f"Congratulations! {winner.mention} won {prize}!")

@client.command()
@commands.has_role("Owner")
async def reroll(ctx, channel : discord.TextChannel, id_ : int):
    try:
        new_msg = await channel.fetch_message(id_)
    except:
        await ctx.send("The id was entered incorrectly.")
        return
    
    users = await new_msg.reactions[0].users().flatten()
    users.pop(users.index(client.user))

    winner = random.choice(users)

    await channel.send(f"Congratulations! The new winner is {winner.mention}.!")   



@client.command()
async def trash(ctx, user: discord.Member = None):

    if user == None:
        user = ctx.author()

    trash = Image.open("SpongeBurn.jpg")

    asset = user.avatar_url_as(size = 128)

    data = BytesIO(await asset.read())
    pfp = Image.open(data)

    pfp = pfp.resize((176,176))
    trash.paste(pfp, (82, 143))

    trash.save("profile.jpg")

    await ctx.send (file = discord.File("profile.jpg"))







async def open_account(user):

    users = await get_bank_data()
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
    with open("mainbank.json", "r") as f:
        users = json.load(f)

    return users



async def update_bank(user, change=0,mode = 'wallet'):

    users = await get_bank_data()

    users[str(user.id)][mode] += change

    with open("mainbank.json", "w") as f:
        json.dump(users,f)

    bal = users[str(user.id)]["wallet"],users[str(user.id)]["bank"]


    return bal


env = os.environ.get("BOT_TOKEN")


client.run(env)
