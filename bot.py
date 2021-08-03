""" * * * * * * * * * * * * * * *
*                               *
*     discord.py Rewrite DM     *
*        Author: Invader        *
*     Discord: IПVΛDΣЯ#0006     *
*                               *
* * * * * * * * * * * * * * * """

# Ik most of you guys will just remove the credits stuff. Well, you're free to do so, idec anymore xd.
# If anyone gets any error or anything unusual, join the discord server or add me IПVΛDΣЯ#1195, we'll figure it out.
# Enjoy <3
# -invader

# Modules
import discord
from discord.ext import commands
from discord.ext.commands import MemberConverter
import json
import asyncio
import os
import sys

# Loading config
with open(os.path.join(sys.path[0], "config.json"), "r") as f:
	config = json.load(f)
token = config["token"]
prefix = config["prefix"]
delay = int(config["delay"])
log_dms = config["log_dms"]

# Bot Instance(s) & Settings
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(
	command_prefix=prefix,
	case_insensitive=True, # Remove this line to make your bot command sensitive
	intents=intents)
client.remove_command("help") # Coz default help sucks

# Events
@client.event
async def on_ready():
	print(f"Logged in as {client.user.name}")

# Commands
@client.command(aliases=["dmall"]) # You can add more aliases here
async def send(ctx, *, args:str=None):
	if args.strip() == None or args.strip() == "":
		return
	else:
		if log_dms.strip().lower() in ["on","enabled","true","enable"]:
			member_count = 0
			for member in ctx.guild.members:
				member_count += 1
			await ctx.send(f"{member_count} members detected, this might take a while")
			for member in ctx.guild.members:
				if member == client.user:
					await ctx.send(f":x: {member.name} is self, cannot message self")
					member_count -= 1
					pass
				elif member.bot == True:
					await ctx.send(f":x: {member.name} is a bot, cannot message a bot")
					member_count -= 1
					pass
				else:
					try:
						await member.send(args.strip())
						await ctx.send(f":white_check_mark: Sent message to {member.name}")
						await asyncio.sleep(delay)
					except discord.errors.Forbidden:
						await ctx.send(f":white_check_mark: Could not send message to {member.name}, probably DMs off")
						member_count -= 1
						pass
					except commands.CommandInvokeError:
						await ctx.send(f":x: Could not send message to {member.name}, probably DMs off")
						member_count -= 1
						pass
			await ctx.send(f":white_check_mark: DM sent to {member_count} members")
			return
		else:
			member_count = 0
			for member in ctx.guild.members:
				member_count += 1
			await ctx.send(f"{member_count} members detected, this might take a while")
			for member in ctx.guild.members:
				if member == client.user or member.bot == True:
					member_count -= 1
					pass
				else:
					try:
						await member.send(args.strip())
						await asyncio.sleep(delay)
					except discord.errors.Forbidden:
						member_count -= 1
						pass
					except commands.CommandInvokeError:
						member_count -= 1
						pass

			await ctx.send(f":white_check_mark: DM sent to {member_count} members")
			return

@client.command(aliases=["idm"]) # You can add more aliases here
async def dm(ctx, user:MemberConverter=None, *, args=None):
	while args != None and args != "" and not args.isspace():
		try:
			await user.send(args.replace(user.mention, ""))
			await ctx.send(f"Message sent to {user.name}#{user.discriminator} :white_check_mark:")
		except discord.errors.Forbidden:
			await ctx.send(f"Could not send messsage to {user.name}#{user.discriminator} :x:")
			pass
		except commands.CommandInvokeError:
			await ctx.send(f"Could not send messsage to {user.name}#{user.discriminator} :x:")
			pass
		return
	await ctx.send(f"Please enter a message with the command\nUsage : `{client.command_prefix}dm <member> <message>`")
	return

@client.command(aliases=["ping","ltc"]) # You can add more aliases here
async def latency(ctx):
	if int(round(client.latency * 1000)) <= 50:
		color=0x000000
	elif int(round(client.latency * 1000)) <= 100:
		color=0x00FF00
	elif int(round(client.latency * 1000)) <= 300:
		color=0x00FFFF
	else:
		color=0xFF0000
	if ctx.message.content.lower().startswith(f"{client.command_prefix}latency"):
		title="Latency"
	elif ctx.message.content.lower().startswith(f"{client.command_prefix}ping"):
		title="Ping"
	else:
		title="Latency"
	hehe = discord.Embed(title=title,description=f"Latency : {str(round(client.latency * 1000))}ms", color=color)
	await ctx.send(embed=hehe)

@client.command(aliases=["helpme","how"])
async def help(ctx, command_name:str=None):
	while command_name == None or command_name.isspace() or command_name == "":
		xd = discord.Embed(title=f"{client.user.name}", description="", color=0x00FFFF)
		xd.add_field(name="Send", value=f"DMs all members with a delay\nUsage : `{client.command_prefix}send <message>`", inline=False)
		xd.add_field(name="DM", value=f"DMs specific member\nUsage : `{client.command_prefix}dm <user> <message>`", inline=False)
		xd.add_field(name="Latency", value=f"Displays the latency/ping of the bot in ms\nUsage : `{client.command_prefix}latency`", inline=False)
		xd.add_field(name="Help", value=f"Shows all available commands\nUsage : `{client.command_prefix}help`", inline=False)
		xd.add_field(value=f"You can do `{client.command_prefix}help <command-name>` for more info on command", name="More Info", inline=False)
		xd.set_footer(text="Made by IПVΛDΣЯ <3", icon_url="https://cdn.discordapp.com/avatars/559227438224375828/95f57511cebe80102e73a50eb892506e.webp?size=1024")
		await ctx.send(embed=xd)
		return
	if command_name.strip().lower() == "send" or command_name.strip().lower() in commands.Bot.get_command(client, "send").aliases:
		send_aliases = commands.Bot.get_command(client, "send").aliases
		send_aliases_str = ""
		for element in send_aliases:
			if len(send_aliases) == 0:
				send_aliases_str += " `None`"
			else:
				send_aliases_str += f" `{element}`"
		xdd = discord.Embed(
			title="Send - Help",
			description=f"DMs the members in the server with a delay (changeable)\nYou can change ***delay*** in ***config.json***\nYou can stop the ***bot's logging after each DM*** in ***config.json***\n`(By setting log_dms to \"off\" or \"disabled\")`\nUsage : `{client.command_prefix}send <message>`\nAliases :{send_aliases_str}",
			color=0x00FF00)
	elif command_name.strip().lower() == "dm":
		dm_aliases = commands.Bot.get_command(client, "dm").aliases
		dm_aliases_str = ""
		for element in dm_aliases:
			if len(dm_aliases) == 0:
				dm_aliases_str += " `None`"
			else:
				dm_aliases_str += f" `{element}`"
		xdd = discord.Embed(
			title="DM - Help",
			description=f"DMs a specific member in the server\nUsage : `{client.command_prefix}dm <message>`\nAliases :{dm_aliases_str}",
			color=0x00FF00)
	elif command_name.strip().lower() == "latency":
		latency_aliases = commands.Bot.get_command(client, "latency").aliases
		latency_aliases_str = ""
		for element in latency_aliases:
			if len(latency_aliases) == 0:
				latency_aliases_str += " `None`"
			else:
				latency_aliases_str += f" `{element}`"
		xdd = discord.Embed(
			title="Latency - Help",
			description=f"Displays the latency/ping of the bot in milliseconds\nUsage : `{client.command_prefix}latency`\nAliases :{latency_aliases_str}",
			color=0x00FF00)
	elif command_name.strip().lower() == "help":
		help_aliases = commands.Bot.get_command(client, "help").aliases
		help_aliases_str = ""
		for element in help_aliases:
			if len(help_aliases) == 0:
				help_aliases_str += " `None`"
			else:
				help_aliases_str += f" `{element}`"
		xdd = discord.Embed(
			title="Help - Help",
			description=f"Displays all available commands\nUsage : `{client.command_prefix}help`\nAliases :{help_aliases_str}",
			color=0x00FF00)
	else:
		xdd = discord.Embed(name="Invalid Command", description=f"No command found matching \"{command_name.strip()}\"", color=0xFF0000)
	xdd.set_footer(text="Made By IПVΛDΣЯ <3", icon_url="https://cdn.discordapp.com/avatars/559227438224375828/95f57511cebe80102e73a50eb892506e.webp?size=1024")
	await ctx.send(embed=xdd)

# Catch MemberConveter Error
@dm.error
async def resolve(ctx, error):
	if isinstance(error, commands.MemberNotFound):
		await ctx.send("Please Mention/Enter A Valid Member")
		return

# Run Client - duh!
client.run(token)
