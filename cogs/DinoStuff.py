# -*- coding: utf-8 -*-
"""
Created on Wed May 24 17:06:12 2023

@author: bezbakri
"""

import nextcord as discord
from nextcord import Interaction
from nextcord.ext import commands
import requests
from bs4 import BeautifulSoup
from random import choice

class DinoStuff(commands.Cog):
    def GetDinoFacts(self) -> list:
        facts_list = []
        dino_site = "https://www.thefactsite.com/dinosaur-facts/"

        response = requests.get(dino_site)
        soup = BeautifulSoup(response.text, "html.parser")
        dino_text_whole = soup.find('div', attrs = {"class": "content-area"})
        dino_text_facts_entire = dino_text_whole.find("ul")
        dino_text_headers = dino_text_facts_entire.find_all("h2")

        for header in dino_text_headers:
            fact = [header.text, ]
            image_tag = header.nextSibling
            cur_tag = image_tag.nextSibling
            fact_text = ""
            while True:
                
                if cur_tag is not None and cur_tag.name == "p" and cur_tag.text.strip() != "":
                    fact_text += cur_tag.text
                    fact_text += "\n"
                    cur_tag = cur_tag.nextSibling
                    
                else:
                    break
            fact.append(fact_text)
            facts_list.append(fact)
        return facts_list
    
    def GetDinoList(self) -> list:
        dino_list = []
        base_site = "https://www.nhm.ac.uk"
        dino_site = base_site + "/discover/dino-directory/name/name-az-all.html"
        response = requests.get(dino_site)
        soup = BeautifulSoup(response.text, "html.parser")
        dino_text_raw = soup.find("div", attrs={"class" : "dinosaurfilter section"})
        all_dinos_raw = dino_text_raw.find("ul")
        all_dinos = all_dinos_raw.find_all("li")
        for dino in all_dinos:
            dino_set = {}
            dino_set["name"] = dino.text.strip().split()[0]
            dino_set["url"] = dino.find("a")["href"]
            dino_list.append(dino_set)
        return dino_list
    
    def __init__(self, bot):
        self.bot = bot
        self.facts_list = self.GetDinoFacts() #add the sue fact to the footer of an embed
        self.dino_list = self.GetDinoList()
        
    @commands.command()
    async def RandomDinoFact(self, ctx):
        """Gives you a random dino fact!"""
        fact = choice(self.facts_list)
        await ctx.send(f"**{fact[0]}**\n\n{fact[1]}\n*Did you know? The largest T-Rex skeleton ever discovered was named Sue*")
        
    @commands.command()
    async def RandomDino(self, ctx):
        """Gives you the name of one of the 315 odd non-avian dinosaur genera!"""
        dino = choice(self.dino_list)
        wikipedia_main_link = "https://en.wikipedia.org/wiki/"
        nhm_main_link = "https://www.nhm.ac.uk"
        await ctx.send(f"# {dino['name']}\n\n**Wikipedia link:** <{wikipedia_main_link + dino['name']}>\n**Additional link from the NHM UK:** {nhm_main_link + dino['url']}")
        
    @discord.slash_command(name = "RandomDinoFact")
    async def RandomDinoFactSlash(self, interaction:Interaction):
        """Gives you a random dino fact!"""
        fact = choice(self.facts_list)
        await interaction.response.send_message(f"**{fact[0]}**\n\n{fact[1]}\n*Did you know? The largest T-Rex skeleton ever discovered was named Sue*")
      
    
def setup(bot):
    bot.add_cog(DinoStuff(bot))