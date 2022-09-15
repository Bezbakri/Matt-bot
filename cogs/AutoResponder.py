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
import re
import json

load_dotenv()
BOT_USER_ID=os.getenv("BOT_USER_ID")
SQUILL_USER_ID=int(os.getenv("SQUILL_USER_ID")) 
with open('im_response_config.json', 'r') as f:
    im_response_config = json.load(f)

start_line_dad_expression = re.compile("[Ii]'*([( a)( A)])*[Mm] ")

def rest_of_message_function(message):
    if message.startswith("I'm"):
        return message.lstrip("I'm")
    elif message.startswith("i'm"):
        return message.lstrip("i'm")
    elif message.startswith("im"):
        return message.lstrip("im")
    elif message.startswith("Im"):
        return message.lstrip("Im")
    elif message.startswith("I am"):
        return message.lstrip("I a").lstrip("m")
    elif message.startswith("i am"):
        return message.lstrip("i a").lstrip("m")
    elif message.startswith("I AM"):
        return message.lstrip("I A").lstrip("M")
    elif message.startswith("IM"):
        return message.lstrip("IM")
    elif message.startswith("I'M"):
        return message.lstrip("I'M")
    elif message.startswith("iM"):
        return message.lstrip("iM")

class AutoResponder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.bad_words_list = ["kys", "kill yourself"]
        self.bot.hello_friends_emoji = "<:hellofriends:943005593566838794>"
        self.bot.upvote = "<:upvote:944219796554252429>"
        self.bot.downvote = "<:downvote:944219797162459136>"
        self.bot.amogus_emoji = "\U0001F237"
        
        
    @commands.Cog.listener()
    async def on_message(self,message):
        im_response_enabled = bool(im_response_config.get(str(message.author.id), True))
        if message.author == self.bot.user:
            return
        else:
            for i in self.bot.bad_words_list:
                if i in message.content.lower():
                    await message.channel.send("you should love yourself now")
                    return
            if "hello friends" in message.content.lower():
                await message.add_reaction(self.bot.hello_friends_emoji)
            if "sus" in message.content.lower():
                await message.add_reaction(self.bot.amogus_emoji)
            if "ratio" in message.content.lower():
                await message.add_reaction(self.bot.upvote)
                await message.add_reaction(self.bot.downvote)
            if "🥺" in message.content:
                await message.reply(">bottom emoji\n\nHi, cutie~")
            if message.author.id == 316125981725425666 or message.author.id == SQUILL_USER_ID:
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
            if start_line_dad_expression.match(message.content, 0, 5) and im_response_enabled:
                rest_of_message = rest_of_message_function(message.clean_content).strip()
                display_name = await message.guild.fetch_member(BOT_USER_ID)
                display_name = display_name.display_name
                await message.reply(f"Hi {rest_of_message}, \nI'm {display_name}.")
            mention_comp = f"<@!{BOT_USER_ID}>"
            mention_mobile = f"<@{BOT_USER_ID}>"
            if mention_comp in message.content or mention_mobile in message.content:
                if "fuck you" in message.content.lower():
                    await message.channel.send(f"Fuck you {message.author.mention}")
                else:
                    await message.channel.send(f"Hello, my prefix for this server is ``{prefix.return_prefix(message.guild)}``")
            
        
        #await self.bot.process_commands(message)
    @commands.command()
    async def im_toggle(self, ctx):
        """Toggles the option for the bot to respond to you a classic dad response."""
        if not im_response_config.get(str(ctx.author.id)):
            im_response_config[str(ctx.author.id)] = "False"
        else:
            im_response_config[str(ctx.author.id)] = str(not bool(im_response_config.get(str(ctx.author.id))))
        
        with open('im_response_config.json', 'w') as f:
            json.dump(im_response_config, f)
        await ctx.send(f'"im" response toggled to {im_response_config.get(str(ctx.author.id))}')


def setup(bot):
    bot.add_cog(AutoResponder(bot))