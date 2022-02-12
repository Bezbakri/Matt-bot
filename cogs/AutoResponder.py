# -*- coding: utf-8 -*-
"""
Created on Thu Feb  3 22:11:01 2022

@author: bezbakri
"""

import nextcord as discord
import os
from nextcord.ext import commands
from dotenv import load_dotenv
import prefix

load_dotenv()
BOT_USER_ID=os.getenv("BOT_USER_ID")

class AutoResponder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_message(self,message):
        if message.author == BOT_USER_ID:
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
        mention_comp = f"<@!{BOT_USER_ID}>"
        mention_mobile = f"<@{BOT_USER_ID}>"
        if mention_comp in message.content or mention_mobile in message.content:
            if "fuck you" in message.content.lower():
                await message.channel.send(f"Fuck you {message.author.mention}")
            else:
                await message.channel.send(f"Hello, my prefix for this server is ``{prefix.return_prefix(message.guild)}``")
        
        
        #await self.bot.process_commands(message)    
def setup(bot):
    bot.add_cog(AutoResponder(bot))