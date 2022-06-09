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
wookiee_cse_token = os.getenv("WOOKIEEPEDIA_SEARCH_ENGINE_ID")
resource = build("customsearch", 'v1', developerKey=api_key).cse()

def member_role_color(member):
    for role in reversed(member.roles): # go top to bottom
        if role.color.value:
            return role.color
        
    return 0xEF8A01

def wikisearch(query):
    search_result = resource.list(q=query, cx=wiki_cse_token).execute()['items']
    wiki_link =  search_result[0]['link']

    response = requests.get(wiki_link)
    soup = BeautifulSoup(response.text, 'html.parser')
    wiki_text_whole = soup.find('div', attrs = {"class": "mw-parser-output"})
    wiki_text_tags = wiki_text_whole.find_all("p")
    wiki_text = f"<{wiki_link}>\n```"
    for line in wiki_text_tags:
        wiki_text = wiki_text + line.text
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
    
    @commands.command(aliases = ['wookiee', "starwars"])
    async def discordwookieesearch(self, ctx, *, query):
        "Returns the summary of a wookieepedia article"
        search_result = resource.list(q=query, cx=wookiee_cse_token).execute()['items']
        wookiee_link =  search_result[0]['link']
        wookiee_title = search_result[0]['title']
        
        response = requests.get(wookiee_link)
        soup = BeautifulSoup(response.text, 'html.parser')
        wookiee_text_whole = soup.find('div', attrs = {"class": "mw-parser-output"})
        wookiee_text_tags = wookiee_text_whole.find_all("p")
        wookiee_text = ""
        for line in wookiee_text_tags:
            wookiee_text = wookiee_text + line.text
        
        if len(wookiee_text)>1500:
            wookiee_text = wookiee_text[:1500] + "..."
        
        embed_color = member_role_color(ctx.author)
        
        wookiee_embed = discord.Embed(title=wookiee_title, url=wookiee_link, description=wookiee_text, color=embed_color)
        wookiee_embed.set_footer(text = f"Requested by {ctx.author.display_name}", icon_url = ctx.author.avatar.url)
        
        try:
            image_link = search_result[0]['pagemap']['metatags'][0]['og:image']
            wookiee_embed.set_image(url=image_link)
        except:
            pass
        await ctx.send(embed=wookiee_embed)
        
def setup(bot):
    bot.add_cog(WikiCommands(bot))