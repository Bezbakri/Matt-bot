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
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f"with {len(bot.guilds)} war criminal bunkers"))
    channel = bot.get_channel(924331444661284914)
    await channel.send("I am alive")
    '''
    for i in initial_extensions:
        bot.add_cog(i)
    await channel.send(f"Added {len(initial_extensions)} cogs {initial_extensions})"'''
       



    
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
    

initial_extensions = ['cogs.FunCommands', 'cogs.ImageCommands', 'cogs.error_handling']



if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)





async def is_owner(ctx):
    return ctx.author.id == 316125981725425666

@bot.command(
    name = "addcog",
    help = f"Adding cogs. List of cogs is: {initial_extensions}",
    brief = "command for adding cogs"
)
@commands.check(is_owner)
async def adding_pog(ctx, cog):
    if cog.lower() == "all":
        for i in initial_extensions:
            bot.add_cog(i)
        await ctx.channel.send(f"Added {len(initial_extensions)} cogs {initial_extensions}")
    '''else:
        bot.add_cog(str_to_class(cog))
        await ctx.channel.send(f"Added 1 cog {cog}")'''


@bot.command(
    name = "removecog",
    help = f"Removing cogs. List of cogs is: {initial_extensions}",
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
    
    if message.content.lower() == "i live in canada":
        prev_msg =await message.channel.history(limit = 2).flatten()
        if prev_msg[1].content.lower() == "wrong":
            await message.reply("https://en.wikipedia.org/wiki/Kaneda_Castle")
    
    
    
    await bot.process_commands(message)    
 




    
bot.run(DISCORD_TOKEN)