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
from FunCommands import FunCommands
import prefix
from ImageCommands import ImageCommands
from error_handling import ErrorHandler

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")



bot = commands.Bot(command_prefix = prefix.prefix)

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    GMT = pytz.timezone("Etc/GMT")
    start_time = datetime.now(GMT)
    global display_time
    display_time = start_time.strftime("%Y/%m/%d %H:%M:%S")
    channel = bot.get_channel(924331444661284914)
    for i in coglist:
        bot.add_cog(i)
    await channel.send(f"Added {len(coglist)} cogs {coglist}")    




    
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
    

coglist = [FunCommands(), ImageCommands(), ErrorHandler()]



import sys

def str_to_class(classname):
    return getattr(sys.modules[__name__], classname)



async def is_owner(ctx):
    return ctx.author.id == 316125981725425666

@bot.command(
    name = "addcog",
    help = f"Adding cogs. List of cogs is: {coglist}",
    brief = "command for adding cogs"
)
@commands.check(is_owner)
async def adding_pog(ctx, cog):
    if cog.lower() == "all":
        for i in coglist:
            bot.add_cog(i)
        await ctx.channel.send(f"Added {len(coglist)} cogs {coglist}")
    '''else:
        bot.add_cog(str_to_class(cog))
        await ctx.channel.send(f"Added 1 cog {cog}")'''


@bot.command(
    name = "removecog",
    help = f"Removing cogs. List of cogs is: {coglist}",
    brief = "command for removing cogs"
)
@commands.check(is_owner)
async def removing_pog(ctx, cog):
    
    bot.remove_cog(cog)
    await ctx.channel.send(f"Removed {cog}")
    '''else:
        bot.add_cog(str_to_class(cog))
        await ctx.channel.send(f"Added 1 cog {cog}")'''


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.author.id == 316125981725425666:
        if "gaymers" in message.content.lower():
            if "morning" in message.content.lower():
                await message.channel.send(f"<#{message.channel.id}> is online")
                if "good" in message.content.lower():
                    await message.reply('Good morning furry', mention_author=False)
                else:
                    await message.reply('Morning furry', mention_author=False)
                with open("assets/greetings.png", "rb") as fh:
                    f = discord.File(fh, filename = "greetings.png")
                await message.channel.send("*greetings bi furry", file = f)
                await message.channel.send(f"{message.author.mention} what's up you meme loving fuck")
                await message.channel.send("https://cdn.discordapp.com/attachments/528925999602204681/910120622007418880/video0.mp4")
            
            elif "goodnight" in message.content.lower():
                await message.channel.send(f"<#{message.channel.id}> is offline")
    
    await bot.process_commands(message)    
 




    
bot.run(DISCORD_TOKEN)