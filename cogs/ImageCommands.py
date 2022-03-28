# -*- coding: utf-8 -*-
"""
Created on Wed Dec 29 21:43:23 2021

@author: bezbakri
"""

import nextcord as discord
from nextcord import Interaction
from nextcord.ext import commands
import requests
from PIL import Image, ImageDraw, ImageFont, ImageSequence
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
import random
from datetime import datetime, timedelta
import textwrap
from string import ascii_letters
import io
from pilmoji import Pilmoji

load_dotenv()

api_key = os.getenv("GOOGLE_CUSTOM_SEARCH_API_TOKEN")
cse_token = os.getenv("SEARCH_ENGINE_ID")
TEST_SERVER_ID = os.getenv("TEST_SERVER_ID") #for testing slash commands

resource = build("customsearch", 'v1', developerKey=api_key).cse()


def member_role_color(member):
    for role in reversed(member.roles): # go top to bottom
        if role.color.value:
            return role.color
        
    return 0xEF8A01

def date_generator():
    d1 = datetime.strptime('1/1/2012 1:30 PM', '%m/%d/%Y %I:%M %p')
    d2 = datetime.strptime('1/6/2021 4:50 AM', '%m/%d/%Y %I:%M %p')
    delta = d2 - d1
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    newdate = d1 + timedelta(seconds=random_second)
    timestamp = newdate.strftime("%I:%M %p").lstrip("0")
    datestamp = newdate.strftime("%d %b %Y").lstrip("0")
    return timestamp, datestamp

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
    

class ImageCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.count = 0
        
    
    
    ascii_help = """Returns ascii image of the argument.
    Usage:
        $ascii me    Returns ascii art of your avatar
        $ascii <image_link>    Returns ascii art of image link
        $ascii (attach an image to your message)    Returns ascii art of attached image
    
    
    """
    
    async def get_asset_from_user(self, ctx, image_link = None, allow_static_image = True, allow_gif = False):
         
        try:
            extra_text = ""
            if len(ctx.message.attachments) > 0:
                    extra_text = image_link
                    image_link = ctx.message.attachments[0].url
            if image_link.lower() == "me":
                image_link = ctx.author.avatar.url
            response = requests.get(image_link, stream=True).raw
            img = Image.open(response)
            #fh = open(image_name, "wb")
            #fh.write(response.content)
            #fh.close()
            await ctx.channel.send("Successful image")
            if allow_gif == False and img.format == "GIF":
                mypalette = img.getpalette()
                img.putpalette(mypalette)
                static_img = Image.new("RGBA", img.size)
                static_img.paste(img)
                return static_img, extra_text
                    
                
            else:
                return img, extra_text
        except:
            await ctx.channel.send("fucker gimme an image link")
    
    
    @commands.command(
        name = "ascii",
        help = ascii_help,
        brief = "Ascii art of images"        
    )
    async def ascii_art(self, ctx, image_link = None):
        #image_name = "assets/image_to_ascii.png"
        
        
        #Note to self: PLEASE FIX THE ERROR HANDLING
        #Note to self: Fixed, somehow
        #Note to self: with rev's thing AND MY SHITTY ERROR HANDLING SKILLS
        
        
       
        #now image manipulation, my most hated part
        #img = Image.open(image_name)
        img = await self.get_asset_from_user(ctx, image_link)
        img = img[0]
        
        #resizing
        width, height = img.size
        aspect_ratio = height/width #RATIO LOL
        new_width = 52
        new_height = aspect_ratio * new_width *0.5
        img = img.resize((new_width, int(new_height)))
        #await ctx.channel.send(img.size)
        
        #image to grayscale (image takes an L)
        
        img = img.convert("L")
        pixels = img.getdata()
        #await ctx.channel.send(pixels)
        
        
        #replace pixels with ascii character
        ASCII_CHARS = ["@", "#", "$", "%", "?", "*", "+", ";", ":", ",", "."]
        
        new_pixels = [ASCII_CHARS[pixel//25] for pixel in pixels]
        new_pixels = "".join(new_pixels)
        
        
        #now make them into a list of strings with length = new width
        new_pixels_count = len(new_pixels)
        ascii_image = [new_pixels[index:index + new_width] for index in range(0, new_pixels_count, new_width)]
        ascii_image = "\n".join(ascii_image)
        try:
        
            #send it
            #with open("assets/ascii_art.txt", "w") as f:
                #f.write(ascii_image)
            await ctx.channel.send(f"```{ascii_image}```")
        except:
            await ctx.channel.send("Discord is being a poopoohead and won't let me send the final product.")
    
            
        
       
        
    @commands.command(
        name = "backtoformula",
        aliases = ["BezBeingACodeMonkey"],
        help = "Back to formula",
        brief = "back to formula"
        
    )    
        
    async def backtoformula(self, ctx):
        await ctx.reply("https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fi.redd.it%2Fy3f2yhe3ywsy.jpg&f=1&nofb=1")
    
    
    @commands.command(
        name = "image",
        aliases = ["img", "i"],
        help = "Searches for images. Aliases are img and i.",
        brief = "Image search command"
    )
    
    async def only_100_queries_a_day(self, ctx, *search_query):
        
        
        embed_color = member_role_color(ctx.author)
        
        
        search_query = " ".join(search_query)
        
        await ctx.channel.send(f"Starting search for {search_query}...")
        
        #image_name = "assets/search_result.png"
        
        result = resource.list(q=search_query, cx=cse_token, searchType='image').execute()
        await ctx.channel.send("Search done!")
        result_to_show_index = random.randint(0, len(result['items']))
        result_to_show = result['items'][result_to_show_index]
        image_link = result_to_show['link']
        
        #response = requests.get(image_link)
        #fh = open(image_name, "wb")
        #fh.write(response.content)
        #fh.close()
        #await ctx.channel.send("Successful image")
        
        embed_url = result_to_show['image']['contextLink']
        embed = discord.Embed(title = f"{search_query}", url = embed_url, color = embed_color)
        embed.set_image(url = image_link)
        embed.set_footer(text = f"Requested by {ctx.author.display_name}", icon_url = ctx.author.avatar.url)
        embed.timestamp = datetime.utcnow()
        
        await ctx.channel.send(embed = embed)
        
        
    @commands.command(
        name = "trumptweet",
        aliases = ['trump', 'trumpet'],
        help = "Trump tweets whatever you say.",
        brief = "Trumpify your words"        
    )
    async def djtj(self, ctx, *, text = None):
        
        text = "".join(text)
        #await ctx.channel.send("Text converted to string")
        
        
        
        
        
        font = ImageFont.truetype("assets/HelveticaNeueLight.ttf", size = 58)
        
        # Calculate the average length of a single character of our font.
        # Note: this takes into account the specific font and font size.
        avg_char_width = sum(font.getsize(char)[0] for char in ascii_letters) / len(ascii_letters)
        # Translate this average length into a character count
        max_char_count = int(1050/ avg_char_width)
        # Create a wrapped text object using scaled character count
        text = textwrap.fill(text=text, width=max_char_count).replace("\\n", "\n")
        
        text_image_y_dimension = 100
        for i in text:
            if i == "\n":
                text_image_y_dimension+=60
        
        mode = "RGB"
        size = (1094, text_image_y_dimension)
        color = (255, 255, 255)
        text_image = Image.new(mode, size, color)
        
        #writing_text = ImageDraw.Draw(text_image)
        writing_text = Pilmoji(text_image)
        writing_text.text(xy=(0, 0), text=text, font=font, fill='#000000')
        
        
        
        
        trump_tweet_header_path = "assets/trump_tweet_header.png"
        trump_tweet_footer_path = "assets/trump_tweet_footer.png"
        
        
        trump_tweet_footer = Image.open(trump_tweet_footer_path)
        font_ratio = ImageFont.truetype("assets/HelveticaNeueBold.ttf", size = 36)
        font_datestamp = ImageFont.truetype("assets/ArialMdm.ttf", size = 26)
        retweets = retweets_and_likes_generator(8000, 100000)
        likes = retweets_and_likes_generator(10000, 250000)
        trump_tweet_ratio = ImageDraw.Draw(trump_tweet_footer)
        
        #the retweets-likes
        trump_tweet_ratio.text(xy = (42, 45), text = retweets, font = font_ratio, fill = "#438DCB")
        trump_tweet_ratio.text(xy = (210, 45), text = likes, font = font_ratio, fill = "#438DCB")
        
        
        
        #the datestamp
        
        timestamp, datestamp = date_generator()
        trump_tweet_ratio.text(xy = (42, 134), text = timestamp, font = font_datestamp, fill = "#6E777E")
        trump_tweet_ratio.text(xy = (170, 134), text = datestamp, font = font_datestamp, fill = "#6E777E")
        
        
        trump_tweet_header = Image.open(trump_tweet_header_path)
        
        
        
        trump_tweet_y_dimension = text_image_y_dimension + 338
        mode = "RGB"
        size = (1200, trump_tweet_y_dimension)
        color = (255, 255, 255)
        trump_tweet = Image.new(mode, size, color)
        
        trump_tweet.paste(trump_tweet_header)
        trump_tweet.paste(text_image, (42, 150))
        trump_tweet.paste(trump_tweet_footer, (0, text_image_y_dimension+151))
        
        
        
        
        with io.BytesIO() as image_binary:
             trump_tweet.save(image_binary, 'PNG')
             image_binary.seek(0)
             await ctx.send(file=discord.File(fp=image_binary, filename='trump_says.png'))
        
        
        
        #trump_tweet_path = "assets/trump_tweet.png"
        
        #trump_tweet.save(trump_tweet_path)
        
        #with open(trump_tweet_path, "rb") as fh:
            #f = discord.File(fh, filename = "Trump_says.png")
        #await ctx.channel.send(file = f)
        
        
        #old version of doing this shit
        #keeping it just because
        
        '''
        
        
        mode = "RGB"
        size = (1094, 283)
        color = (255, 255, 255)
        text_image = Image.new(mode, size, color)
        
        
        font = ImageFont.truetype("assets/HelveticaNeueLight.ttf", size = 58)
        
        
        writing_text = ImageDraw.Draw(text_image)
        
        # Calculate the average length of a single character of our font.
        # Note: this takes into account the specific font and font size.
        avg_char_width = sum(font.getsize(char)[0] for char in ascii_letters) / len(ascii_letters)
        # Translate this average length into a character count
        max_char_count = int(text_image.size[0] * 1.2/ avg_char_width)
        # Create a wrapped text object using scaled character count
        text = textwrap.fill(text=text, width=max_char_count)
        # Add text to the image
        writing_text.text(xy=(0, 0), text=text, font=font, fill='#000000')
                
        
        #text_image.save(text_image_path)
        #await ctx.channel.send("Text image created.")
        
        trump_template = Image.open("assets/trump_tweet_template.png")
        
        trump_tweet = trump_template.copy()
        trump_tweet.paste(text_image, (42, 150))
        
        font_ratio = ImageFont.truetype("assets/HelveticaNeueBold.ttf", size = 36)
        retweets = retweets_and_likes_generator(8000, 100000)
        likes = retweets_and_likes_generator(10000, 250000)
        trump_tweet_ratio = ImageDraw.Draw(trump_tweet)
        trump_tweet_ratio.text(xy = (42, 490), text = retweets, font = font_ratio, fill = "#438DCB")
        trump_tweet_ratio.text(xy = (210, 490), text = likes, font = font_ratio, fill = "#438DCB")
        
        
        trump_tweet_path = "assets/trump_tweet.png"
        
        trump_tweet.save(trump_tweet_path)
        
        with open(trump_tweet_path, "rb") as fh:
            f = discord.File(fh, filename = "Trump_says.png")
        await ctx.channel.send(file = f)
        '''
        
    @commands.command(
        name = "caption",
        help = "Captions your image like a meme."
    )
    async def meme_caption(self, ctx, image_link = None, *, caption = None):
        if caption:
            caption = "".join(caption)
        meme_format = await self.get_asset_from_user(ctx, image_link, allow_gif = True)
        if caption:
            caption = meme_format[1]+ " " + caption
        else:
            caption = meme_format[1]
        caption = caption.strip()
        meme_format = meme_format[0]
        meme_format_type = meme_format.format
        meme_format_x_dimension, meme_format_y_dimension = meme_format.size
        aspect_ratio = meme_format_y_dimension/meme_format_x_dimension
        meme_width = 600
        meme_format_height = int(meme_width*aspect_ratio)

        font = ImageFont.truetype("assets/caption.ttf", size = 54)
        
        avg_char_width = sum(font.getsize(char)[0] for char in ascii_letters) / len(ascii_letters)
        max_char_count = int(625/avg_char_width)
        caption = textwrap.fill(text = caption, width = max_char_count).replace("\\n", "\n")
        
        caption_y_dimension = 100
        for i in caption:
            if i == "\n":
                caption_y_dimension+=60
        mode = "RGB"
        size = (meme_width, caption_y_dimension)
        color = (255, 255, 255)
        caption_image = Image.new(mode, size, color)
        
        writing_text = Pilmoji(caption_image)
        writing_text.text(xy = (300, 25), text = caption, font = font, fill = '#000000', anchor = "ma", align= "center",)
        del writing_text
        
        meme_size = (meme_width, caption_y_dimension + meme_format_height)
        
        
        
        if meme_format_type != "GIF":
            meme_format = meme_format.resize((meme_width, meme_format_height))
            meme = Image.new(mode, meme_size, color)
            meme.paste(caption_image)
            meme.paste(meme_format, (0, caption_y_dimension))
            
            with io.BytesIO() as image_binary:
                 meme.save(image_binary, 'PNG')
                 image_binary.seek(0)
                 await ctx.send(file=discord.File(fp=image_binary, filename='caption.png'))
            
        else:
            frames = []
            
            for frame in ImageSequence.Iterator(meme_format):
                meme_frame = Image.new(mode, meme_size, color)
                frame = frame.resize((meme_width, meme_format_height))
                meme_frame.paste(caption_image)
                meme_frame.paste(frame, (0, caption_y_dimension))
                meme_frame_byte_stream = io.BytesIO()
                meme_frame.save(meme_frame_byte_stream, "GIF")
                meme_frame = Image.open(meme_frame_byte_stream)
                frames.append(meme_frame)
            avg_duration = meme_format.info['duration']
            meme_first_frame = frames[0]
            with io.BytesIO() as image_binary:
                 meme_first_frame.save(image_binary, format = 'GIF', append_images = frames[1:], save_all = True, loop=0, duration = avg_duration)
                 image_binary.seek(0)
                 await ctx.send(file=discord.File(fp=image_binary, filename='caption.gif'))
    
    @commands.command(
        name = "motivation",
        help = "Captions your image like a demotivational poster. Separate the title and the rest of the text with | ."
    )
    async def meme_demotivation(self, ctx, image_link = None, *, caption = None):
        if caption:
            caption = "".join(caption)
        meme_format = await self.get_asset_from_user(ctx, image_link, allow_gif = True)
        if caption:
            caption = meme_format[1]+ " " + caption
        else:
            caption = meme_format[1]
        caption = caption.strip()
        meme_format = meme_format[0]
        meme_format_type = meme_format.format
        meme_format_x_dimension, meme_format_y_dimension = meme_format.size
        aspect_ratio = meme_format_y_dimension/meme_format_x_dimension
        meme_width = 600
        meme_format_height = int(meme_width*aspect_ratio)
        
        caption = caption.partition(" | ")
        title = caption[0]
        subtitle = caption[2]

        title_font = ImageFont.truetype("assets/motivation.ttf", size = 64)
        subtitle_font = ImageFont.truetype("assets/motivation.ttf", size = 36)
        #title
        avg_char_width = sum(title_font.getsize(char)[0] for char in ascii_letters) / len(ascii_letters)
        max_char_count_title = int(550/avg_char_width)
        title = textwrap.fill(text = title, width = max_char_count_title).replace("\\n", "\n")
        #subtitle
        avg_char_width = sum(subtitle_font.getsize(char)[0] for char in ascii_letters) / len(ascii_letters)
        max_char_count = int(650/avg_char_width)
        subtitle = textwrap.fill(text = subtitle, width = max_char_count).replace("\\n", "\n")
        
        poster_y_dimension = meme_format_height + 250
        subtitle_y_pos = meme_format_height + 170
        for i in title:
            if i == "\n":
                poster_y_dimension+=70
                subtitle_y_pos+=70
        for i in subtitle:
            if i == "\n":
                poster_y_dimension+=40
        mode = "RGB"
        size = (meme_width + 100, poster_y_dimension)
        color = (0, 0, 0)
        poster = Image.new(mode, size, color)
        
        writing_text = Pilmoji(poster)
        writing_text.text(xy = (350, meme_format_height + 100), text = title, font = title_font, fill = '#FFFFFF', anchor = "ma", align= "center",)
        writing_text.text(xy = (350,  subtitle_y_pos), text = subtitle, font = subtitle_font, fill = '#FFFFFF', anchor = "ma", align= "center",)
        del writing_text
        
        meme_size = (meme_width+100, poster_y_dimension)
        
        
        
        if meme_format_type != "GIF":
            meme_format = meme_format.resize((meme_width, meme_format_height))
            meme = Image.new(mode, meme_size, color)
            meme.paste(poster)
            meme.paste(meme_format, (50, 50))
            addons = ImageDraw.Draw(meme)
            addons.rectangle((40, 40, meme_width+60, meme_format_height+60), outline = '#FFFFFF', width = 2)
            del addons
            
            with io.BytesIO() as image_binary:
                 meme.save(image_binary, 'PNG')
                 image_binary.seek(0)
                 await ctx.send(file=discord.File(fp=image_binary, filename='motivation.png'))
            
        else:
            frames = []
            
            for frame in ImageSequence.Iterator(meme_format):
                meme_frame = Image.new(mode, meme_size, color)
                frame = frame.resize((meme_width, meme_format_height))
                meme_frame.paste(poster)
                meme_frame.paste(frame, (50, 50))
                meme_frame_byte_stream = io.BytesIO()
                meme_frame.save(meme_frame_byte_stream, "GIF")
                meme_frame = Image.open(meme_frame_byte_stream)
                addons = ImageDraw.Draw(meme_frame)
                addons.rectangle((40, 40, meme_width+60, meme_format_height+60), outline = '#FFFFFF', width = 2)
                del addons
                frames.append(meme_frame)
            avg_duration = meme_format.info['duration']
            meme_first_frame = frames[0]
            with io.BytesIO() as image_binary:
                 meme_first_frame.save(image_binary, format = 'GIF', append_images = frames[1:], save_all = True, loop=0, duration = avg_duration)
                 image_binary.seek(0)
                 await ctx.send(file=discord.File(fp=image_binary, filename='motivation.gif'))
    
    #slash version of trump command
    @discord.slash_command(name = "trumptwit", description = "Trump tweets what you say!")
    async def slash_command_cog(self, 
                                interaction:Interaction,
                                text:str 
                                ):
        
                    
        font = ImageFont.truetype("assets/HelveticaNeueLight.ttf", size = 58)
        
        # Calculate the average length of a single character of our font.
        # Note: this takes into account the specific font and font size.
        avg_char_width = sum(font.getsize(char)[0] for char in ascii_letters) / len(ascii_letters)
        # Translate this average length into a character count
        max_char_count = int(1050/ avg_char_width)
        # Create a wrapped text object using scaled character count
        text = textwrap.fill(text=text, width=max_char_count).replace("\\n", "\n")
        
        text_image_y_dimension = 100
        for i in text:
            if i == "\n":
                text_image_y_dimension+=60
        
        mode = "RGB"
        size = (1094, text_image_y_dimension)
        color = (255, 255, 255)
        text_image = Image.new(mode, size, color)
        
        #writing_text = ImageDraw.Draw(text_image)
        writing_text = Pilmoji(text_image)
        writing_text.text(xy=(0, 0), text=text, font=font, fill='#000000')
        
        
        
        
        trump_tweet_header_path = "assets/trump_tweet_header.png"
        trump_tweet_footer_path = "assets/trump_tweet_footer.png"
        
        
        trump_tweet_footer = Image.open(trump_tweet_footer_path)
        font_ratio = ImageFont.truetype("assets/HelveticaNeueBold.ttf", size = 36)
        font_datestamp = ImageFont.truetype("assets/ArialMdm.ttf", size = 26)
        retweets = retweets_and_likes_generator(8000, 100000)
        likes = retweets_and_likes_generator(10000, 250000)
        trump_tweet_ratio = ImageDraw.Draw(trump_tweet_footer)
        
        #the retweets-likes
        trump_tweet_ratio.text(xy = (42, 45), text = retweets, font = font_ratio, fill = "#438DCB")
        trump_tweet_ratio.text(xy = (210, 45), text = likes, font = font_ratio, fill = "#438DCB")
        
        
        
        #the datestamp
        
        timestamp, datestamp = date_generator()
        trump_tweet_ratio.text(xy = (42, 134), text = timestamp, font = font_datestamp, fill = "#6E777E")
        trump_tweet_ratio.text(xy = (170, 134), text = datestamp, font = font_datestamp, fill = "#6E777E")
        
        
        trump_tweet_header = Image.open(trump_tweet_header_path)
        
        
        
        trump_tweet_y_dimension = text_image_y_dimension + 338
        mode = "RGB"
        size = (1200, trump_tweet_y_dimension)
        color = (255, 255, 255)
        trump_tweet = Image.new(mode, size, color)
        
        trump_tweet.paste(trump_tweet_header)
        trump_tweet.paste(text_image, (42, 150))
        trump_tweet.paste(trump_tweet_footer, (0, text_image_y_dimension+151))
        
        
        
        
        with io.BytesIO() as image_binary:
             trump_tweet.save(image_binary, 'PNG')
             image_binary.seek(0)
             await interaction.response.send_message(file=discord.File(fp=image_binary, filename='trump_says.png'))
    
    
        


def setup(bot):
    bot.add_cog(ImageCommands(bot))