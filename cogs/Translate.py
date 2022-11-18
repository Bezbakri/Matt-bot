# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 16:07:58 2022

@author: bezbakri
"""

import nextcord as discord
from nextcord.ext import commands
import googletrans

class Translate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
       
    @commands.command(aliases = ["langs", "languages"])
    async def languageList(self, ctx):
        """Gives you all the available languages and their language codes."""
        languages = googletrans.LANGUAGES
        languagesString = "List of languages:\n```"
        for key in languages:
            languagesString += key + ": " + languages[key] + "\n"
        languagesString += "```"
        await ctx.send(languagesString)
    
    @commands.command(aliases = ["englishPls", ])
    async def translateToEnglish(self, ctx, *, text):
        """Translates text to English."""
        # BROKEN LIBRARY, WILL SWITCH TO SOMETHING BETTER LATER
        translator = googletrans.Translator()
        #possibleLang = translator.detect(text)
        #await ctx.send("Detected language")
        #await ctx.send(possibleLang)
        translation = translator.translate(text)
        await ctx.send("Text translated")
        await ctx.send(translation.text)
        #await ctx.send(f"```{possibleLang}\n{translation}```")
    


def setup(bot):
    bot.add_cog(Translate(bot))