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
        #wookiee_text_tags = wookiee_text_whole.find_all("p")
        wookiee_text = ""
        #for line in wookiee_text_tags:
        #    wookiee_text = wookiee_text + line.text
        if wookiee_text_whole.find('div', attrs = {"class": "quote"}):
            for div in wookiee_text_whole.find('div', attrs = {"class": "quote"}):
                next_node = div.parent
                next_node_sibling = next_node.find_next_sibling("p")
            wookiee_text = wookiee_text + next_node_sibling.text
        elif wookiee_text_whole.find('aside'):
            for div in wookiee_text_whole.find('aside'):
                next_node = div.parent
                next_node_sibling = next_node.find_next_sibling("p")
            wookiee_text = wookiee_text + next_node_sibling.text
        else:
            wookiee_text_tags = wookiee_text_whole.find_all("p")
            for line in wookiee_text_tags:
                wookiee_text = wookiee_text + line.text
        
        

        
        if len(wookiee_text)>1250:
            wookiee_text = wookiee_text[:1250] + "..."
        
        embed_color = member_role_color(ctx.author)
        
        wookiee_embed = discord.Embed(title=wookiee_title, url=wookiee_link, description=wookiee_text, color=embed_color)
        if wookiee_text_whole.find('aside'):
            aside_content =  wookiee_text_whole.find('aside').strings
            sub_text = ""
            for line in aside_content:
                if line[0] == "[":
                    pass
                elif wookiee_title.partition("|")[0].strip() in line:
                    pass
                else:
                    sub_text = sub_text + line
            if len(sub_text) > 1021:
                sub_text = sub_text[:1021] + "..."
            wookiee_embed.add_field(name = "Some Information", value = sub_text)
        if wookiee_text_whole.find('table', attrs = {"class": "scrollbox"}) and wookiee_text_whole.find('table', attrs = {"class": "scrollbox"}).parent.find_previous_sibling("h2").text == "Appearances[]":
            table = wookiee_text_whole.find('table', attrs = {"class": "scrollbox"})
            ul = table.find("ul")
            appearances = ul.find_all("li")
            number_of_appearances = len(appearances)
            wookiee_embed.add_field(name = "Number of Appearances", value = number_of_appearances)
        elif wookiee_text_whole.find('span', text = "Appearances"):
            first_appearance = wookiee_text_whole.find('small', text = "(First appearance)")
            ul = first_appearance.parent.parent
            appearances = ul.find_all("li")
            number_of_appearances = len(appearances)
            wookiee_embed.add_field(name = "Number of Appearances", value = number_of_appearances)
            
        wookiee_embed.set_footer(text = f"Requested by {ctx.author.display_name}", icon_url = ctx.author.avatar.url)
        
        try:
            image_link = search_result[0]['pagemap']['metatags'][0]['og:image']
            wookiee_embed.set_image(url=image_link)
        except:
            pass
        await ctx.send(embed=wookiee_embed)
    @commands.command()
    async def wookie(self, ctx):
        "Respect the double E."
        await ctx.reply("Respect the double E.")
    @commands.command(aliases = ['wikifind', ])
    async def specificwikisearch(self, ctx, article, keyword):
        "Searches for a certain header in the wikipedia article you want to search up. CURRENTLY ONLY WORKS WITH h3."
        search_result = resource.list(q=article, cx=wiki_cse_token).execute()['items']
        wiki_link =  search_result[0]['link']
        await ctx.send(f"<{wiki_link}>")
        
        response = requests.get(wiki_link)
        soup = BeautifulSoup(response.text, 'html.parser')
        wiki_text = soup.find('div', attrs = {"class": "mw-parser-output"})
        
        try:
            for header in wiki_text.find_all('h3'): 
                if keyword.lower() == header.text.lower():
                    next_node = header
                    while True:
                        next_node = next_node.nextSibling
                        if next_node == None:
                            break
                        if next_node.name is not None:
                            if next_node.name != "p":
                                break
                            
                            text_to_send =next_node.get_text(strip = True)
                            await ctx.send(f"```{text_to_send}```")
                    break
                else:
                    pass
            else:
                await ctx.send("The topic you were looking for wasn't found.")
        except:
            await ctx.send("Some error occurred idk bru 🤓")
        
        
def setup(bot):
    bot.add_cog(WikiCommands(bot))