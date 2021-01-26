import discord
from discord.ext import commands
import json
import os
import math
import random
import praw
import datetime
import asyncio
import youtube_dl
from discord.ext.commands import command, cooldown
from discord.ext.commands import Cog, BucketType
from enum import Enum
import typing as t
import re
import wavelink
from discord import Intents


from PIL import Image
from io import BytesIO

intent = discord.Intents.all()

f = open("rules2.txt","r")
rules = f.readlines()

filtered_words = ["dick", "fuck", "bitch", "ass", "shit", "motherfucker"]


reddit = praw.Reddit(client_id = "AjkL0nqGEdPZYw",
                     client_secret = "5kVlWhM_E7Jm2ZijsOmSCJyg79p6lg",
                     username = "Vahu-Bali",
                     password = "Vasu@5950",
                     user_agent = "pythonmemepraw")


client = commands.Bot(command_prefix="vb ")

client.remove_command("help")

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
discord.Intents.all()

@client.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.channels, name='general')
    await channel.send(f'Welcome {member.mention}!  Ready to jam out? See `?help` command for details!')
        
@client.command(name='ping', help='This command returns the latency')
async def ping(ctx):
    await ctx.send(f'**Pong!** Latency: {round(client.latency * 1000)}ms')

@client.command(name='hello', help='This command returns a random welcome message')
async def hello(ctx):
    responses = ['***grumble*** Why did you wake me up?', 'Top of the morning to you lad!', 'Hello, how are you?', 'Hi', '**Wasssuup!**']
    await ctx.send(choice(responses))

@client.command(name='die', help='This command returns a random last words')
async def die(ctx):
    responses = ['why have you brought my short life to an end', 'i could have done so much more', 'i have a family, kill them instead']
    await ctx.send(choice(responses))

@client.group(invoke_without_command=True)
async def help(ctx):
    em = discord.Embed(title = "Help", description = "Use **vb help** <command> for extended information on a command.",color = ctx.author.colour)

    em.add_field(name = "Moderation", value = "```help moderation```")
    em.add_field(name = "Fun", value = "```help fun````")
    em.add_field(name = "Economy", value = "bal, beg, withdraw, dep, pay, slots, rob, shop, bag")

    await ctx.send(embed = em)

@client.group(invoke_without_command=True, aliases=['help moderation'])
async def help_moderation(ctx):
    em = discord.Embed(title = "Moderation", description = "Moderation Commands",color = ctx.author.colour)

    em.add_field(name="kick", value = "Admin can kick members")
    em.add_field(name="ban", value="Bans members from servers")
    em.add_field(name="unban", value="unbans members allowing them to join back to the server")
    em.add_field(name="mute", value = "mutes members so that they can't talk")
    em.add_field(name="unmute", value = "unmutes members so that they can start talking again")
    em.addfield(name = "clear", value="clears messages from value provided, Ex: vb clear 300, <-- this will clear 300 messages")

@client.group(invoke_without_command=True, aliases=['help fun'])
async def help_fun(ctx):
    em = discord.Embed(title = "Fun", description= 'Fun commands', color = ctx.author.colour)

    em.add_field(name="trash", value = "you can trash anybody's picture in the fire just by doing vb trash @mention")
    em.add_field(name = "meme", value = "you can ask Dr.Pirocks to give you a meme to laugh at")
    em.add_field(name = "cleanmeme", value = "you can ask Dr.Pirocks to give you a meme to laugh at that is appropriate and doens't have any bad words or vulgar refrences")
    em.add_field(name='tictactoe', value = "mention two people (yourself and somebody else) to play tic tac toe with, to place your marker somewhere then you have to type vb place (and then number location like the top left would be 1 and the top right would be 3")

@client.group(invoke_without_command=True, aliases=['help economy'])
async def help_economy(ctx):
    em = discord.Embed(title = "Fun", description= 'Fun commands', color = ctx.author.colour)

    em.add_field(name="bal", value = "find the amount of moolah you have in your wallet and bank")
    em.add_field(name="beg", value = "don't deny it you are a poor man but don't worry just type in vb beg and Dr.Pirocks will give you some cash")
    em.add_field(name = "withdraw", value = "You can withdraw your moolah from your bank to use to pay people or something like that")
    em.add_field(name="dep", value = "deposit moolah from wallet to bank so you can't get robbed")
    em.add_field(name="pay", value = "pay people moolah")
    em.add_field(name = "slots", value = "gamble your moolah for the chance of winning double but also the chance of losing that amount")
    em.add_field(name="rob", value = "rob those people and live the life of fortunes")
    em.add_field(name = "shop", value = "shop for items using your moolah")
    em.add_field(name="bag", value = "check all the items you have bought from the shop in your bag")


@client.event
async def on_message2(msg):
    for word in filtered_words:
        if word in msg.content:
            await msg.delete()

    await client.process_commands(msg)

@client.command(aliasess=['rules'])
async def rule(ctx,*,number):
    await ctx.send(rules[int(number)-1])



@client.command(aliases=['c'])
@commands.has_permissions(manage_messages = True)
async def clear(ctx,amount=2):
    await ctx.channel.purge(limit = amount)

@client.command(aliases=['k'])
@commands.has_permissions(manage_messages = True)
async def kick(ctx,member : discord.Member,*,reason= "No reason provided"):
    await member.send("You have been kicked from the server, Because:"+reason)
    await member.kick(reason=reason)

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
async def cleanmeme(ctx):

    subreddit = reddit.subreddit("cleanmemes")
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
async def youtube(ctx):
    embed=discord.Embed(title="Vasu Bansal YouTube", url="https://www.youtube.com/channel/UCCzfHZSA8nEnx_QTFlq6mHA", description="This is the link to the Vasu Bansal YouTube channel go subscribe", color=0xFF5733)
    await ctx.send(embed=embed)

@client.command()
async def podcast(ctx):
    embed=discord.Embed(title="Talk Tech Teen Tech Podcast", url="https://redcircle.com/talk-tech-teen-tech", description="This is the link to the podcast that was created by Vasu Bansal and in this podcast we talk about tech through the prespective of school going teenagers", color=0xFF5733)
    await ctx.send(embed=embed)

@client.command()
async def joindis(ctx):
    embed=discord.Embed(title="Discord Support", url="https://discord.gg/G2KgVtyaR5", description="This is the link to the Vasu Bansal Discord and support server for this bot", color=0xFF5733)
    await ctx.send(embed=embed)

@client.command()
async def inv(ctx):
    embed=discord.Embed(title="Invite to server", url="https://discord.com/api/oauth2/authorize?client_id=788895628511281182&permissions=8&scope=bot", description="Add this bot to your server with this link ", color=0xFF5733)
    await ctx.send(embed=embed)

@client.command(aliases=['b'])
@commands.has_permissions(ban_members = True)
async def ban(ctx,member : discord.Member, *, reason = "No reason provided"):
    await ctx.send(member.name + " has been banned from the server")
    await member.ban(reason=reason)

@client.command(aliases=['ub'])
@commands.has_permissions(ban_members = True)
async def unban(ctx, *,member):
    banned_users = await ctx.guild.bans()
    member_name, member_disc = member.split('#')

    for banned_entry in banned_users:
        user = banned_entry.users

        if(user.name, user.discrimator)==(member_name, member_disc):

            await ctx.guild.unban(user)
            await ctx.send(member_name +" has been unbanned!")
            return
    
    await ctx.send(member+" was not found")


@client.command(aliases=['m'])
@commands.has_permissions(kick_members = True)
async def mute(ctx,member : discord.Member):
    muted_role = ctx.guild.get_role(799700181913698371)

    await member.add_roles(muted_role)

    await ctx.send(member.mention + " has been muted")

@client.command(aliases=['um'])
@commands.has_permissions(kick_members = True)
async def unmute(ctx,member : discord.Member):
    muted_role = ctx.guild.get_role(799700181913698371)

    await member.remove_roles(muted_role)

    await ctx.send(member.mention + " has been unmuted")



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
@cooldown(1, 15, BucketType.user)
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

@client.command()
async def imbetter(ctx, user: discord.Member = None):

    myself = ctx.author

    if user == None:
        user = ctx.author()

    imbetter = Image.open("DrakeMeme.jpg")

    asset = user.avatar_url_as(size = 128)

    data = BytesIO(await asset.read())
    pfp = Image.open(data)

    pfp = pfp.resize((430,430))
    imbetter.paste(pfp, (659, 79))

    asset2 = myself.avatar_url_as(size = 128)

    data2 = BytesIO(await asset2.read())
    pfp2 = Image.open(data2)

    pfp2 = pfp2.resize((435,435))
    imbetter.paste(pfp2, (662,683))

    imbetter.save("profile.jpg")

    await ctx.send (file = discord.File("profile.jpg"))



youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)



queue = []





@client.command(name='join', help='This command makes the bot join the voice channel')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("You are not connected to a voice channel")
        return
    
    else:
        channel = ctx.message.author.voice.channel

    await channel.connect()

@client.command(name='queue', help='This command adds a song to the queue')
async def queue_(ctx, url):
    global queue

    queue.append(url)
    await ctx.send(f'`{url}` added to queue!')

@client.command(name='remove', help='This command removes an item from the list')
async def remove(ctx, number):
    global queue

    try:
        del(queue[int(number)])
        await ctx.send(f'Your queue is now `{queue}!`')
    
    except:
        await ctx.send('Your queue is either **empty** or the index is **out of range**')
        
@client.command(name='play', help='This command plays songs')
async def play(ctx):
    global queue

    server = ctx.message.guild
    voice_channel = server.voice_client

    async with ctx.typing():
        player = await YTDLSource.from_url(queue[0], loop=client.loop)
        voice_channel.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

    await ctx.send('**Now playing:** {}'.format(player.title))
    del(queue[0])

@client.command(name='pause', help='This command pauses the song')
async def pause(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client

    voice_channel.pause()

@client.command(name='resume', help='This command resumes the song!')
async def resume(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client

    voice_channel.resume()

@client.command(name='view', help='This command shows the queue')
async def view(ctx):
    await ctx.send(f'Your queue is now `{queue}!`')

@client.command(name='leave', help='This command stops makes the bot leave the voice channel')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    await voice_client.disconnect()

@client.command(name='stop', help='This command stops the song!')
async def stop(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client

    voice_channel.stop()



player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]

@client.command()
async def tictactoe(ctx, p1: discord.Member, p2: discord.Member):
    global count
    global player1
    global player2
    global turn
    global gameOver

    if gameOver:
        global board
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:"]
        turn = ""
        gameOver = False
        count = 0

        player1 = p1
        player2 = p2

        # print the board
        line = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[x]

        # determine who goes first
        num = random.randint(1, 2)
        if num == 1:
            turn = player1
            await ctx.send("It is <@" + str(player1.id) + ">'s turn.")
        elif num == 2:
            turn = player2
            await ctx.send("It is <@" + str(player2.id) + ">'s turn.")
    else:
        await ctx.send("A game is already in progress! Finish it before starting a new one.")

@client.command()
async def place(ctx, pos: int):
    global turn
    global player1
    global player2
    global board
    global count
    global gameOver

    if not gameOver:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"
            elif turn == player2:
                mark = ":o2:"
            if 0 < pos < 10 and board[pos - 1] == ":white_large_square:" :
                board[pos - 1] = mark
                count += 1

                # print the board
                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]

                checkWinner(winningConditions, mark)
                print(count)
                if gameOver == True:
                    await ctx.send(mark + " wins!")
                elif count >= 9:
                    gameOver = True
                    await ctx.send("It's a tie!")

                # switch turns
                if turn == player1:
                    turn = player2
                elif turn == player2:
                    turn = player1
            else:
                await ctx.send("Be sure to choose an integer between 1 and 9 (inclusive) and an unmarked tile.")
        else:
            await ctx.send("It is not your turn.")
    else:
        await ctx.send("Please start a new game using the !tictactoe command.")


def checkWinner(winningConditions, mark):
    global game0ver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True

@tictactoe.error
async def tictactoe_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention 2 players for this command.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to mention/ping players (ie. <@688534433879556134>).")

@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please enter a position you would like to mark.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to enter an integer.")


@client.event
async def on_message(message):
    empty_array = []
    modmail_channel = discord.utils.get(client.get_all_channels(), name="mod-mail")

    if message.author == client.user:
        return
    if str(message.channel.type) == "private":
        if message.attachments != empty_array:
            files = message.attachments
            await modmail_channel.send("[" + message.author.display_name + "]")

            for file in files:
                await modmail_channel.send(file.url)
        else:
            await modmail_channel.send("[" + message.author.display_name + "] " + message.content)

    elif str(message.channel) == "mod-mail" and message.content.startswith("<"):
        member_object = message.mentions[0]
        if message.attachments != empty_array:
            files = message.attachments
            await member_object.send("[" + message.author.display_name + "]")

            for file in files:
                await member_object.send(file.url)
        else:
            index = message.content.index(" ")
            string = message.content
            mod_message = string[index:]
            await member_object.send("[" + message.author.display_name + "]" + mod_message)

    await client.process_commands(message)

@commands.command()
async def randgrame(self, ctx):
    number = random.randint(0, 100)
    for i in range(0, 5):
        await ctx.send('guess')
        response = await self.bot.wait_for('message')
        guess = int(response.content)
        if guess > number:
            await ctx.send('bigger')
        elif guess < number:
            await ctx.send('smaller')
        else:
            await ctx.send('true')


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
