# -*- coding: utf-8 -*-
"""
Created on Sat Dec 25 18:42:42 2021

@author: bezbakri
"""

import nextcord as discord
from nextcord import Interaction, Message
from datetime import datetime, timezone
import pytz
import os
from os.path import join, isfile
from dotenv import load_dotenv
from nextcord.ext import commands
import sys, traceback
import json


load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
TEST_SERVER_ID = os.getenv("TEST_SERVER_ID") #for testing slash commands

def get_prefix(client, message):
    guild = message.guild
    if guild == None:
        return "$"
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)
    return prefixes.get(str(guild.id), "$")

intents = discord.Intents.default()
intents.members = True
#intents.message_content = True


bot = commands.Bot(command_prefix = (get_prefix), intents = intents)



cog_dir = "cogs"

"""initial_extensions = ['cogs.FunCommands', 
                      'cogs.ImageCommands', 
                      'cogs.error_handling', 
                      'cogs.AutoResponder',
                      'cogs.owner',
                      'cogs.WikiCommands',
                      'cogs.Translate']"""
initial_extensions = [f.replace(".py", "") for f in os.listdir(cog_dir) if isfile(join(cog_dir, f))]


if __name__ == '__main__':
    global cogs_added
    cogs_added = 0
    for extension in initial_extensions:
        bot.load_extension(cog_dir + "." + extension)
        cogs_added+=1


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    GMT = pytz.timezone("Etc/GMT")
    start_time = datetime.now(GMT)
    utc_start_time = start_time.replace(tzinfo=timezone.utc)
    global utc_start_timestamp
    utc_start_timestamp = str(utc_start_time.timestamp()).partition(".")[0]
    global display_time
    display_time = start_time.strftime("%Y/%m/%d %H:%M:%S")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f"with {len(bot.guilds)} war criminal bunkers"))
    channel = bot.get_channel(924331444661284914)
    await channel.send("I am alive <:hellofriends:943005593566838794>")
    await channel.send(f"Added {cogs_added} out of {len(initial_extensions)} cogs")


@bot.command(
    name = "test",
    help = "Tells you how long the bot's been running for. In GMT format.",
    brief = "Is the bot working?"
)        
async def pls_respond(ctx):
    
    await ctx.channel.send(f"<:20hype:924951455343968296> Meheheheh. Running since {display_time} GMT (<t:{utc_start_timestamp}:R> or <t:{utc_start_timestamp}>).")
    

    

@bot.command(
    name = "ping",
    help = "Pongs back at ya. That's all.",
    brief = "pong"
)
async def finally_work_pls(ctx):
    await ctx.channel.send(f"pong :ping_pong:\nMy latency is **{round(bot.latency*1000)} ms**")

@bot.slash_command(name = "peeng", description = "Pongs back at ya. That's all.")
async def slash_test(interaction:Interaction):
    await interaction.response.send_message(f"pong :ping_pong:\nMy latency is **{round(bot.latency*1000)} ms**")

@bot.slash_command(name = "say", description = "Repeats whatever you say.")
async def say(interaction: Interaction, message: str):
    await interaction.response.send_message(message)
    

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


class NewHelpCommand(commands.MinimalHelpCommand):
    async def help(self):
        """Attempt at rewriting the default help command. Will finish this later"""
        destination = self.get_destination()
        for page in self.paginator.pages:
            emby = discord.Embed(description=page)
            await destination.send(embed=emby)
    
bot.help_command = NewHelpCommand()

@bot.event
async def on_guild_join(guild):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = "$"
    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f"with {len(bot.guilds)} war criminal bunkers"))

@bot.event
async def on_guild_remove(guild):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))
    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f"with {len(bot.guilds)} war criminal bunkers"))

    
bot.run(DISCORD_TOKEN)