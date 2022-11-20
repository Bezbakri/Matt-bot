# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 16:07:58 2022

@author: bezbakri
"""

import nextcord as discord
from nextcord.ext import commands
import googletrans
import deep_translator
import os
from dotenv import load_dotenv

load_dotenv()

TRANSLATION_API_KEY = os.getenv("TRANSLATION_API_KEY")

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
        
        detectedLang = deep_translator.single_detection(text, api_key = TRANSLATION_API_KEY)
        await ctx.send(f"Possible language = {detectedLang}")
        
        translatedText = deep_translator.GoogleTranslator(source = "auto", target = "en").translate(text)
        await ctx.send(translatedText)
        
        # BROKEN LIBRARY, WILL SWITCH TO SOMETHING BETTER LATER
        #translator = googletrans.Translator()
        #possibleLang = translator.detect(text)
        #await ctx.send("Detected language")
        #await ctx.send(possibleLang)
        #translation = translator.translate(text)
        #await ctx.send("Text translated")
        #await ctx.send(translation.text)
        #await ctx.send(f"```{possibleLang}\n{translation}```")
        
    @commands.command()
    async def translate(self, ctx, target, *, text):
        """Translate text to the specified language."""
        try:
            translatedText = deep_translator.GoogleTranslator(source = "auto", target = target).translate(text)
            await ctx.send(translatedText)
        except:
            await ctx.send("Mofo gimme a valid language code.")
    


def setup(bot):
    bot.add_cog(Translate(bot))