# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 23:13:06 2023

@author: bezbakri
"""

import nextcord as discord
from nextcord.ext import commands

class Math(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        self.precedence = {"+" : 1, "-" : 1, "*" : 2, "/" : 2, "%" : 2, "**" : 3, "^" : 3}
        
        self.array = [] #stack that I'll be using for some commands
        self.postfix = []
        
    def isOperand(self, op):
        list_of_ops = ["+", "-", "*", "/", "%", "^", "**"]
        return op in list_of_ops
        
    def convertToPostfix(self, infix):
        return
    
    @commands.command()
    async def simpleCalc(self, ctx, *, exp):
        """Simple arithmetic calculator. Converts shit to postfix, then solves it."""
        exp = "".join(exp)
        await ctx.send(exp)
        
    @commands.command()
    async def add(self, ctx, num1, num2):
        """Adds two numbers. Lazy command I added to make this cog."""
        ans = None
        try:
            ans = float(num1) + float(num2)
        except:
            await ctx.send("Please enter a valid floating point number")
            return
        await ctx.send(f"{ans}")
        
def setup(bot):
    bot.add_cog(Math(bot))