# -*- coding: utf-8 -*-
"""
Created on Mon Dec 27 16:51:13 2021

@author: bezbakri
"""
import nextcord as discord
from nextcord.ext import commands
import json


def return_prefix(guild):
    if guild == None:
        return "$"
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)
    return prefixes.get(str(guild.id), "$")