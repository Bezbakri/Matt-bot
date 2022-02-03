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




initial_extensions = ['cogs.FunCommands', 
                      'cogs.ImageCommands', 
                      'cogs.error_handling', 
                      'cogs.AutoResponder']



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



 




    
bot.run(DISCORD_TOKEN)