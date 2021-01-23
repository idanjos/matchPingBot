# bot.py
import os
import random
import subprocess
import discord
from discord.utils import get
from dotenv import load_dotenv
from discord.ext.commands import Bot
import datetime
import time
import re
import utils
from entity import Guild
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
PREFIX = r"\?jb[ ]"
HELP = "?jb"
INIT_ERROR = 'It appears I am not properly set, try ?jb init'


database = dict()
if os.path.isfile("obj/database.pkl"):
	database = utils.load_obj("database")
client = discord.Client()
delay = dict()
lastReq = dict()

@client.event
async def on_ready():
	print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_message(ctx):
	if not (hasattr(ctx,"guild") and hasattr(ctx.guild,"id")):
		c = "?jb sudo service jacbot restart"
		result = subprocess.run(c.split(" ")[1:], stdout=subprocess.PIPE)	
		print("Guild name not found, restarting service")
		return	
	guild = str(ctx.guild.id)
	if ctx.author == client.user:
		return
	if True:
	#if  ctx.author.guild_permissions.administrator:
		if HELP == ctx.content:
			if guild not in database.keys():
				await ctx.channel.send(f'{INIT_ERROR} {guild}')
				return
			await ctx.channel.send(f'Try ?jb help')
			return

		if re.match(PREFIX,ctx.content):
			args = ctx.content.split(" ")
			print(args)

			if "init" == args[1]:
				if guild in database.keys():
					await ctx.channel.send(f'{client.user.name} reset!')
					
				guild = Guild()
				database[guild] = guild
				await ctx.channel.send(f'Thank you for trying {client.user.name}, use the "?jb help" to add command, channels, messages and delay.')
				return



			if guild not in database.keys():
				await ctx.channel.send(f'{INIT_ERROR}')
				return

			if args[1] == "help":
				embed = discord.Embed(title=f"__**JacBot by Jac:**__", color=0x03f8fc)
				embed.add_field(name=f'?jb **[attribute]** [operation] [params]', value=f'> ?jb command (add|del|list) [string] \n> ?jb channel (add|del|list) [string]\n> ?jb message (add|del|list) [strings]\n> ?jb role (add|del|list) [string]\n> ?jb delay set [seconds]',inline=False)
				await ctx.channel.send(embed=embed)

			elif len(args) > 3 or ( len(args)>2 and "list" in args) or  ( len(args)>2 and "get" in args):
				await utils.handleOperation(ctx,database,guild,args)
			else:
				await ctx.channel.send(f'Try ?jb help')
			utils.save_obj(database,"database")		
			return
	#Skip
	if guild not in database.keys():
		return

	
	await utils.handleMessage(ctx,database,guild,client)

	
client.run(TOKEN)
