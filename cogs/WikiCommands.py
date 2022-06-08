# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 19:37:32 2022

@author: bezbakri
"""

import nextcord as discord
from nextcord.ext import commands
import requests
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
from bs4 import BeautifulSoup

load_dotenv()

api_key = os.getenv("GOOGLE_CUSTOM_SEARCH_API_TOKEN")
cse_token = os.getenv("WIKIPEDIA_SEARCH_ENGINE_ID")
resource = build("customsearch", 'v1', developerKey=api_key).cse()

def wikisearch(query):
    search_result = resource.list(q=query, cx=cse_token).execute()['items']
    wiki_link =  search_result[0]['link']
    image_link = search_result[0]['pagemap']['metatags'][0]['og:image']
    response = requests.get(wiki_link)
    soup = BeautifulSoup(response.text, 'html.parser')
    wiki_text_whole = soup.findAll('div', attrs = {"class": "mw-parser-output"})
    wiki_text = wiki_text_whole.find("p")
    
    print(wiki_text)
    return image_link
    
    

class WikiCommands(commands.Cog):
    def __init(self, bot):
        self.bot = bot
        
    @commands.command(aliases = ['wiki', ])
    async def discordwikisearch(self, ctx, *, query):
        "Returns the summary of a wikipedia article"
        await ctx.send(wikisearch(query))
        
def setup(bot):
    bot.add_cog(WikiCommands(bot))