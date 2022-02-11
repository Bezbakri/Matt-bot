# -*- coding: utf-8 -*-
"""
Created on Sat Dec 25 18:42:42 2021

@author: bezbakri
"""

import nextcord as discord
from datetime import datetime
import pytz
import os
from dotenv import load_dotenv
from nextcord.ext import commands
import sys, traceback
import prefix
import json


load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

def get_prefix(client, message):
    guild = message.guild
    if guild == None:
        return "$"
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)
    return prefixes.get(str(guild.id), "$")


bot = commands.AutoShardedBot(command_prefix = (get_prefix), )




initial_extensions = ['cogs.FunCommands', 
                      'cogs.ImageCommands', 
                      'cogs.error_handling', 
                      'cogs.AutoResponder',
                      'cogs.owner']



if __name__ == '__main__':
    global cogs_added
    cogs_added = 0
    for extension in initial_extensions:
        bot.load_extension(extension)
        
        cogs_added+=1


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    GMT = pytz.timezone("Etc/GMT")
    start_time = datetime.now(GMT)
    global display_time
    display_time = start_time.strftime("%Y/%m/%d %H:%M:%S")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f"with {len(bot.guilds)} war criminal bunkers"))
    channel = bot.get_channel(924331444661284914)
    await channel.send("I am alive")
    await channel.send(f"Added {cogs_added} out of {len(initial_extensions)} cogs")
       



    
@bot.command(
    name = "test",
    help = "Tells you how long the bot's been running for. In GMT format.",
    brief = "Is the bot working?"
)        
async def pls_respond(ctx):
    
    await ctx.channel.send(f"<:20hype:924951455343968296> Meheheheh. Running since {display_time} GMT.")
    

    

@bot.command(
    name = "ping",
    help = "Pongs back at ya. That's all.",
    brief = "pong"
)
async def finally_work_pls(ctx):
    await ctx.channel.send("pong")

@bot.command()
@commands.has_permissions(administrator=True)
async def setprefix(ctx, prefix):
    """Command for setting a prefix
    Ping the bot for the current prefix"""
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
        prefixes[str(ctx.guild.id)] = prefix
        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)
            await ctx.send(f'Prefix is now: {prefix}')
            bot.unload_extension("cogs.AutoResponder")
            bot.load_extension("cogs.AutoResponder")

@bot.event
async def on_guild_join(guild):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = "$"
    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)


@bot.event
async def on_guild_remove(guild):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))
    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)

    
bot.run(DISCORD_TOKEN)