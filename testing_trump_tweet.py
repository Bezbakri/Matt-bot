# -*- coding: utf-8 -*-
"""
Created on Fri Jan  7 19:13:43 2022

@author: bezbakri
"""

from PIL import Image, ImageDraw, ImageFont
import random

def retweets_and_likes_generator(lower_limit, upper_limit):
    raw_number = random.randint(lower_limit, upper_limit)
    list_for_raw_number = []
    for i in str(raw_number):
        list_for_raw_number.append(i)
    list_for_raw_number.insert(-3, ",")
    ratio = ""
    for i in list_for_raw_number:
        ratio+= i
    return ratio
    


trump_template = Image.open("assets/trump_tweet_footer.png")
        
trump_tweet = trump_template.copy()

font_ratio = ImageFont.truetype("assets/HelveticaNeueBold.ttf", size = 36)
retweets = retweets_and_likes_generator(8000, 100000)
likes = retweets_and_likes_generator(10000, 250000)
trump_tweet_ratio = ImageDraw.Draw(trump_tweet)
trump_tweet_ratio.text(xy = (42, 45), text = retweets, font = font_ratio, fill = "#438DCB")
trump_tweet_ratio.text(xy = (210, 45), text = likes, font = font_ratio, fill = "#438DCB")


trump_tweet_path = "assets/trump_tweet.png"

trump_tweet.save(trump_tweet_path)

