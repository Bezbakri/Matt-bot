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
wiki_cse_token = os.getenv("WIKIPEDIA_SEARCH_ENGINE_ID")
resource = build("customsearch", 'v1', developerKey=api_key).cse()

def wikisearch(query):
    search_result = resource.list(q=query, cx=wiki_cse_token).execute()['items']
    wiki_link =  search_result[0]['link']

    response = requests.get(wiki_link)
    soup = BeautifulSoup(response.text, 'html.parser')
    wiki_text_whole = soup.find('div', attrs = {"class": "mw-parser-output"})
    wiki_text_tags = wiki_text_whole.find_all("p")
    wiki_text = f"<{wiki_link}>\n```"
    i = 0
    for line in wiki_text_tags:
        if i <5:
            wiki_text = wiki_text + line.text
            i+=1
        else:
            break
    if len(wiki_text) > 1825:
        wiki_text = wiki_text[:1825] + "..."
    
    try:
        image_link = search_result[0]['pagemap']['metatags'][0]['og:image']
        wiki_text = wiki_text + "```\n" + image_link
    except:
        wiki_text = wiki_text + "```"
    return wiki_text
    
    

class WikiCommands(commands.Cog):
    def __init(self, bot):
        self.bot = bot
        
    @commands.command(aliases = ['wiki', ])
    async def discordwikisearch(self, ctx, *, query):
        "Returns the summary of a wikipedia article"
        await ctx.send(wikisearch(query))
        
def setup(bot):
    bot.add_cog(WikiCommands(bot))