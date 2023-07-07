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
    
    def checkIfFloat(self, num) -> bool:
        #Checks if number is a float
        try:
            float(num)
            return True
        except:
            return False
    
    def evaluateOperation(self, left_elem, right_elem, operator):
        #evaluates an expression (horrible code)
        #TODO: FIX MULT, DIV, ETC
        if operator == "+":
            if self.checkIfFloat(left_elem) and self.checkIfFloat(right_elem):
                return float(left_elem) + float(right_elem)
            else:
                return f"{left_elem} + {right_elem}"
        if operator == "-":
            if self.checkIfFloat(left_elem) and self.checkIfFloat(right_elem):
                return float(left_elem) - float(right_elem)
            else:
                return f"{left_elem} - {right_elem}"
        if operator == "%":
            if self.checkIfFloat(left_elem) and self.checkIfFloat(right_elem):
                return float(left_elem) % float(right_elem)
            else:
                return f"Can't find the remainder of {left_elem} divided by {right_elem}"
        if operator == "*":
            if self.checkIfFloat(left_elem) and self.checkIfFloat(right_elem):
                return float(left_elem) * float(right_elem)
            else:
                return "Will add support later"
        if operator == "/":
            if self.checkIfFloat(left_elem) and self.checkIfFloat(right_elem):
                return float(left_elem) / float(right_elem)
            else:
                return "Will add support later"
        if operator == "%":
            if self.checkIfFloat(left_elem) and self.checkIfFloat(right_elem):
                return float(left_elem) % float(right_elem)
            else:
                return "Will add support later"
        if operator == "**" or operator == "^":
            if self.checkIfFloat(left_elem) and self.checkIfFloat(right_elem):
                return float(left_elem) ** float(right_elem)
            else:
                return "Will add support later"
        
        
        
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
                stack.append(str(self.evaluateOperation(left_elem, right_elem, char)))
        return stack.pop()

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
        postfix = self.convertToPostfix(infix)
        await ctx.send(self.evaluatePostfixExpression(postfix))
        
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