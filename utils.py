import time
import datetime
import discord
import re
import pickle
from discord.utils import get
from dotenv import load_dotenv
from discord.ext.commands import Bot


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


async def handleMessage(ctx, database, guild):
    print(ctx.channel.id)
    if ("<#"+str(ctx.channel.id)+">") in database[guild].channels and any(re.match(c+"[ ].*", ctx.content) or c == ctx.content for c in database[guild].commands):
        await handleMatchPing(ctx, database, guild)


async def handleMatchPing(ctx, database, guild):
    prefix = ""
    for role in database[guild].roles:
        r = int(re.sub("[<>@&]","",role))
        moderator = discord.utils.get(ctx.guild.roles, id=r)
        prefix += moderator.mention+" "

    x = time.mktime(datetime.datetime.now().timetuple()) - \
        database[ctx.guild.name].lastReq
    if x > database[ctx.guild.name].delay:
        database[ctx.guild.name].lastReq = time.mktime(
            datetime.datetime.now().timetuple())
        msg = ctx.content
        for c in database[guild].commands:
            msg = msg.replace(c, "")
        msg = re.sub("[<>@&]","",msg)
        await ctx.channel.send(f'{prefix} {msg}')
    else:

        await ctx.channel.send(f'{database[guild].delay - x} seconds {database[guild].getMessage()}')


def save_obj(obj, name):
    with open('obj/' + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)
