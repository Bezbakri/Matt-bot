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
        self.precedence = {"(" : 0, ")" : 0, "+" : 1, "-" : 1, "*" : 2, "/" : 2, "%" : 2, "**" : 3, "^" : 3}
        
    def isOperand(self, op) -> bool:
        list_of_ops = ["+", "-", "*", "/", "%", "^", "**", "(", ")"]
        return op not in list_of_ops
        
    def convertToPostfix(self, infix) -> list:
        """Convert infix expression (taken as a list) to a postfix expression"""
        stack = []
        postfix = []
        for char in infix:
            if self.isOperand(char):
                postfix.append(char)
            else:
                if char == "(":
                    stack.append("(")
                elif char == ")":
                    operator = stack.pop()
                    while operator != "(":
                        postfix.append(operator)
                        operator = stack.pop()
                else:
                    while (len(stack) != 0 and self.precedence[char] <= self.precedence[stack[-1]]):
                        postfix.append(stack.pop())
                    stack.append(char)
        while (len(stack) != 0):
            postfix.append(stack.pop())
        return postfix
    
    def evaluatePostfixExpression(self, postfix) -> float:
        stack = []
        for char in postfix:
            if self.isOperand(char):
                stack.append(char)
            else:
                right_elem = stack.pop()
                left_elem = stack.pop()
                #will write a function to evaluate this properly tomorrow

    @commands.command()
    async def simpleCalc(self, ctx, *, exp):
        """Simple arithmetic calculator. Converts shit to postfix, then solves it."""
        exp = "".join(exp)
        exp_spaced = ""
        for char in exp:
            if not self.isOperand(char):
                exp_spaced += " " + char + " "
            else:
                exp_spaced += char
        infix = exp_spaced.split()
        for i, element in enumerate(infix):
            if element == "(" and i > 0 and self.isOperand(infix[i - 1]):
                infix.insert(i, "*")
        await ctx.send(self.convertToPostfix(infix))
        
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