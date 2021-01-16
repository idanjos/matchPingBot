import time
import datetime
import subprocess
import discord
import re
import random
import pickle
from discord.utils import get
from dotenv import load_dotenv
from discord.ext.commands import Bot
from datetime import date

images = [
    "https://i.pinimg.com/originals/7b/8b/9c/7b8b9cbc22da0f51cc6710d470a70abd.png",
   "https://i.pinimg.com/originals/d9/c9/e4/d9c9e4be3c2968c4b0884fbd3372d4ee.png",
    "https://i.pinimg.com/originals/ee/0b/83/ee0b8322db7fb7939469a67e889318d4.png",
    "https://clipart.world/wp-content/uploads/2020/10/Light-Green-Among-Us-clipart-transparent.png"
]

types = [
    "Trash Can",
    "3rd Impostor",
    "Throw Lobby",
    "Cringe Crew",
    "Jungle Fumble"
]

async def handleOperation(ctx,database,guild,args):
    if args[1] == "sudo":
        #c = "?jb sudo service ssh restart"
        result = subprocess.run(args[1:], stdout=subprocess.PIPE).stdout
        await ctx.channel.send(f'{result}')
    elif args[1] == "channel":
        if args[2] == "add":
            if database[guild].addChannel(args[3]):
                await ctx.channel.send(f'Channel {args[3]} added')
                return
        elif args[2] == "del":
            if database[guild].delChannel(args[3]):
                await ctx.channel.send(f'Channel {args[3]} deleted')
                return
        elif args[2] == "list":
            await listArray(ctx, database[guild].channels, args[1])
            return
        await ctx.channel.send(f'?jb channel [add|del|list] [string]')
        return
    elif args[1] == "command":
        if args[2] == "add":
            if database[guild].addCommand(args[3]):
                await ctx.channel.send(f'Command {args[3]} added')
                return
        elif args[2] == "del":
            if database[guild].delCommand(args[3]):
                await ctx.channel.send(f'Command {args[3]} deleted')
                return
        elif args[2] == "list":
            await listArray(ctx, database[guild].commands, args[1])
            return
        await ctx.channel.send(f'?jb command [add|del|list] [string]')
        return
    elif args[1] == "message":
        if args[2] == "add":
            if database[guild].addMessage(' '.join(args[3:])):
                await ctx.channel.send(f'Message added')
                return
        elif args[2] == "del":
            if database[guild].delMessage(' '.join(args[3:])):
                await ctx.channel.send(f'Message deleted')
                return
        elif args[2] == "list":
            await listArray(ctx, database[guild].messages, args[1])
            return
        await ctx.channel.send(f'?jb message [add|del|list] [strings]')
        return
    elif args[1] == "role":
        if args[2] == "add":
            if database[guild].addRole(' '.join(args[3:])):
                await ctx.channel.send(f'Role added')
                return
        elif args[2] == "del":
            if database[guild].delRole(' '.join(args[3:])):
                await ctx.channel.send(f'Role {args[3]} deleted')
                return
        elif args[2] == "list":
            await listArray(ctx, database[guild].roles, args[1])
            return
        await ctx.channel.send(f'?jb role [add|del|list] [string]')
        return
    elif args[1] == "delay":
        if args[2] == "set" and args[3].isnumeric():
            if database[guild].setDelay(int(args[3])):
                await ctx.channel.send(f'Delay set to {args[3]} seconds')
                return
        elif args[2] == "get":
            await listArray(ctx, [str(database[guild].delay) + " seconds"], args[1])
            return
        await ctx.channel.send(f'?jb delay set [seconds]')
        return


async def listArray(ctx, array, title):
    embed = discord.Embed(title=f"__**JacBot by Jac:**__", color=0x03f8fc)
    nl = '\n'
    embed.add_field(name=f'{title}s', value=f'{nl.join(array)}', inline=False)
    await ctx.channel.send(embed=embed)


async def handleMessage(ctx, database, guild,client):
    print(ctx.channel.id)
    if ("<#"+str(ctx.channel.id)+">") in database[guild].channels and any(re.match(c+"[ ].*", ctx.content) or c == ctx.content for c in database[guild].commands):
        await ctx.delete()
        await handleMatchPing(ctx, database, guild,client)


async def handleMatchPing(ctx, database, guild,client):
    prefix = ""
    if not ctx.author.voice:
            await ctx.channel.send(f'You are not in a Voice channel', delete_after=10)
            return
    for role in database[guild].roles:
        r = int(re.sub("[<>@&]","",role))
        moderator = discord.utils.get(ctx.guild.roles, id=r)
        prefix += moderator.mention+" "

    x = time.mktime(datetime.datetime.now().timetuple()) - \
        database[ctx.guild.name].lastReq
    if x > database[ctx.guild.name].delay:
        database[ctx.guild.name].lastReq = time.mktime(
            datetime.datetime.now().timetuple())
        
        # await ctx.channel.send(f'{prefix} Please visit something for information on the current list information!')
        # msg = {"embed": {"color": 3447003,"title": "**SERVER NAME** Welcome Bot!","url": "WEBSITE URL","description": "Welcome ** to the **Server name** discord server!","fields": [{"name": "Information","value": "Some info on the server"}],"footer": {"text": "© NAME OF SERVER 2018 - 2019"}}}
        
        
        channel = ctx.author.voice.channel
        n_members = len(channel.members)
        link = await channel.create_invite(max_age = 300)
        # invitelinknew = await client.create_invite(destination = channel, xkcd = True, max_age = 100)
        # print(channel.members)
    # await ctx.send("Here is an instant invite to your server: " + link)
        embed=discord.Embed(title=f'{channel.name} is looking for players!', description=f'[Click here to Join!]({link})', color=0x2dd28b)
        
        
        embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
        embed.set_thumbnail(url=random.choice(images))
        embed.add_field(name="Current size:", value=f'{n_members}/{channel.user_limit}', inline=True)
        embed.add_field(name="Type:", value="Normal", inline=True)
        embed.set_footer(text=f'Created by {ctx.author.name} {str(date.today())}')
        # await ctx.channel.send(link)
        await ctx.channel.send(prefix,embed=embed)

    else:
        await ctx.channel.send(f'{database[guild].delay - x} seconds {database[guild].getMessage()}', delete_after=10)
        


def save_obj(obj, name):
    with open('obj/' + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)
