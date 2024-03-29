# -*- coding: utf-8 -*-
"""
Created on Mon Dec 27 16:26:15 2021

@author: bezbakri
"""
import nextcord as discord
from nextcord import Interaction
import random
from nextcord.ext import commands
import prefix
from datetime import datetime
import csv
import asyncio

def member_role_color(member):
    for role in reversed(member.roles): # go top to bottom
        if role.color.value:
            return role.color
        
    return 0xEF8A01

def talking_ben_simulator():
    response_list = ["Yes.", "No.", "**No.**", "Hohoho!", "*Hohoho!*", "Bleugh!"]
    choice = random.randint(0,5)
    return response_list[choice]


async def is_owner(ctx):
    return ctx.author.id == 316125981725425666        
        
class FunCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    
    
    copypasta_help = """Gives you a random copyapsta from the list of stored copypastas.
    Usage (with default prefix):
        $copypasta random    Gives you a random copypasta
        $copypasta [title]    Gives you a copypasta with that title.
        $copypasta list    Shows the titles of all the copypastas.
        $copypasta count    Shows the number of available copypastas.
    """
    
    
    @commands.command(
        name = "addcopypasta",
        help = "Adding copypastas to the copypasta csv file (yes i am using a csv for this). remember,          $addcopypasta [title] [copypasta]",
        brief = "Add copypastas to library"
        
    )
    @commands.check(is_owner)
    async def addcopypasta(self, ctx, title, copypasta):
        f = open("assets/copypastas.csv", "a")
        fwriter = csv.writer(f)
        fwriter.writerow([title, copypasta])
        await ctx.channel.send(f"added copypasta {title}")
        f.close()
    
    
    
    @commands.command(
        name = "copypasta",
        help = copypasta_help,
        brief = "gives you a copypasta",
        aliases = ["tag", ]
    )
    async def copypasta(self, ctx, *arg):
        
        best_copypasta_desc = "I cannot do this copypasta justice. So please click on the title for the whole thing."
        best_copypasta = """I was thinking about why so many in the radical left participate in "speedrunning"

The reason is the left's lack of work ethic ('go fast' rather than 'do it right') and, in a Petersonian sense, to elevate alternative sexual archetypes in the marketplace ('fastest mario') 1/14
        """
        embed_color = member_role_color(ctx.author)
        
        #best copypastas embed
        petersonian_url = "https://twitter.com/bronzeswords/status/1449345260207828995"
        petersonian_url_author = "https://twitter.com/bronzeswords"
        embed_petersonian = discord.Embed(title = "Please read the full thing here", url = petersonian_url, description = best_copypasta_desc, color = embed_color)
        embed_petersonian.set_author(name = "Petersonian", url = petersonian_url_author, icon_url= "https://pbs.twimg.com/profile_images/1243738424118358017/AQdB0Ze0_400x400.jpg")
        embed_petersonian.set_thumbnail(url = "https://i.kym-cdn.com/entries/icons/original/000/038/621/Screen_Shot_2021-10-20_at_11.21.05_AM.png")
        embed_petersonian.add_field(name = "The 1/14 (actually more)", value=best_copypasta)
        embed_petersonian.timestamp = datetime.utcnow()
        
        
        copypasta_titles = []
        copypasta_titles_lowercase = []
        copypastas = "assets/copypastas.csv"
        
        with open(copypastas, "r", newline = '\r\n', encoding = "cp1251", errors='ignore') as f:
            freader = csv.reader(f)
            for row in freader:
                if row[0]:
                    copypasta_titles.append(row[0])
                    copypasta_titles_lowercase.append(row[0].lower())
        copypasta_titles.pop(0)
        number_of_copypastas = len(copypasta_titles)
        list_of_copypastas = ", ".join(copypasta_titles)
        
        #testing to see if my csv method worked
        '''copypasta_titles_string = ""
        
        for i in copypasta_titles:
            copypasta_titles_string += i
            copypasta_titles_string += ", "
        await ctx.channel.send(f"List of copypastas is {copypasta_titles_string}")'''
        
        embed_list_of_copypastas = discord.Embed(title = f"All copypastas saved ({number_of_copypastas})", description=list_of_copypastas, color= embed_color)
        
        #real code
        
        arg = " ".join(arg)
        
        
        
        if arg.lower() == "random":
            i = random.randint(0,number_of_copypastas-1)
            if i ==13:
                await ctx.channel.send(embed = embed_petersonian)
            else:
                with open(copypastas, "r", newline = '\r\n', encoding = "cp1251", errors='ignore') as f:
                    freader = csv.reader(f)
                    for row in freader:
                        if row[0] == copypasta_titles[i]:
                            copypasta_title = row[0]
                            copypasta_to_send = row[1].replace("\\n", "\n")
                await ctx.channel.send(f"**{copypasta_title}**\n{copypasta_to_send}")
        
        elif arg.lower() in copypasta_titles_lowercase:
            if arg.lower() == "petersonian":
                await ctx.channel.send(embed = embed_petersonian)
            else:
                with open(copypastas, "r", newline = '\r\n', encoding = "cp1251", errors='ignore') as f:
                    freader = csv.reader(f)
                    for row in freader:
                        if row[0].lower() == arg.lower():
                            copypasta_to_send = row[1]
                await ctx.channel.send(copypasta_to_send.replace("\\n", "\n"))
        
        elif arg.lower() == "list":
            
            await ctx.channel.send(embed = embed_list_of_copypastas)
        
        elif arg.lower() == "count":
            copypasta_count = "There are currently " + str(number_of_copypastas) + " copypastas stored in my library. Dm Bezbakri#2637 for more copypastas."
            await ctx.channel.send(copypasta_count)
        
        
        
        else:
            await ctx.channel.send(f"**{arg}** copypasta does not exist")
        
        #code from when this was a .txt file
        #now i'm using a csv file
        #leaving it here for when i might need it again
        """
        with open("copypastas.txt", "r") as f:
            copypasta_directory = f.readlines()
        number_of_copypastas = len(copypasta_directory)
        
        
        #terrible way of writing titles, please do NOT do this
        #i hated this idea so much, i scraped it before finishing it
        #still leaving it here so that i can laugh at myself
        #this was when this was still a .txt file
        '''
        copypasta_titles = []
        copypasta_titles[0] = "Speedrunning"
        copypasta_titles[1] = "Kosovo"
        copypasta_titles[2] = "Hololive dating"
        copypasta_titles[3] = "shit sponge"
        copypasta_titles[4] = "Speedrunning"
        copypasta_titles[5] = "Speedrunning"
        copypasta_titles[6] = "Speedrunning"
        copypasta_titles[7] = "Speedrunning"
        copypasta_titles[8] = "Speedrunning"
        copypasta_titles[9] = "Speedrunning"
        copypasta_titles[10] = "Speedrunning"
        copypasta_titles[11] = "Speedrunning"
        copypasta_titles[12] = "Speedrunning"
        copypasta_titles[13] = "Speedrunning"
        copypasta_titles[14] = "Speedrunning"
        copypasta_titles[15] = "Speedrunning"
        '''
        
       
        #list of copypastas embed
        backward_emoji = "\u2B05"
        forward_emoji = "\u27A1"
        
        emoji_list_movement = [backward_emoji, forward_emoji]
        
        if arg != None:
            if arg.isdigit():
                index = int(arg)
                if index > number_of_copypastas or index <0:
                    await ctx.channel.send(f"Index out of bonds! Please note that the max index is {number_of_copypastas-1}")
                elif index == 14:
                    
                    await ctx.channel.send(embed = embed_petersonian)
                else:
                    await ctx.channel.send(copypasta_directory[index-1].replace("\\n", "\n"))
            
            
            else:
                if arg.lower() == "list":
                    #old version pls ignore
                    '''
                    copypasta_preview = ""
                    for i in range(number_of_copypastas):
                        copypasta_preview += str(i+1)
                        copypasta_preview += ". "
                        copypasta_preview += copypasta_directory[i][:32]
                        copypasta_preview += ", "
                    msg = await ctx.channel.send(copypasta_preview)
                    for i in emoji_list_movement:
                        await msg.add_reaction(i)
                    '''
                    
                    
                    
                
                elif arg.lower() == "count":
                    copypasta_count = "There are currently " + str(number_of_copypastas) + " copypastas stored in my directory. DM Bezbakri#2637 for adding more copypastas."
                    await ctx.channel.send(copypasta_count)
                else:
                    await ctx.channel.send("Wrong usage! Type ``$help copypasta`` for the right usage.")
                   
        else:
            
            
            i = random.randint(0,number_of_copypastas-1)
            if i ==13:
                await ctx.channel.send(embed = embed_petersonian)
            else:
                copypasta_to_send = copypasta_directory[i]
                await ctx.channel.send(copypasta_to_send.replace("\\n", "\n"))
    
    """
    @commands.command(
        name = "hicutie~",
        help = """Replies with a password like a filthy bottom. :pleading_face:
            If you want to know why this bot has this command, type in \"$hicutie~ why\".""",
        brief = "Password generator"
    )
    async def bottom_emoji(self, ctx):
        bottom_emoji = "\U0001F97A"
        sobbing_emoji = "\U0001F62D"
        heart_emoji = "\u2764"
        emoji_list = [bottom_emoji, sobbing_emoji, heart_emoji]
        await ctx.message.add_reaction(bottom_emoji)
        if "why" in ctx.message.content.lower():
            with open("assets/hicutie.png", "rb") as fh:
                f = discord.File(fh, filename = "The_Reason.png")
            await ctx.reply(file = f, mention_author = False)
        else:
            number_of_passwords = random.randint(1, 4)
            password_ = ""
            for i in range(number_of_passwords):
                pass_length = random.randint(8,16)
                
                for j in range(pass_length):
                    case = random.randint(0,1)
                    if case == 0:
                        l_ord = random.randint(65,90)
            
                    else:
                        l_ord = random.randint(97,122)
                    l_chr = chr(l_ord)
                    password_ += l_chr
                password_ += " "
            number_of_emojis = random.randint(0,5)
            for i in range(number_of_emojis):
                emoji_index = random.randint(0, 2)
                password_ += emoji_list[emoji_index]
            await ctx.channel.send(password_)
    @commands.command(
    name = "botlore",
    help = "Tells you about itself",
    brief = "Bot lore"
)
    async def bruh(self, ctx):
        await ctx.channel.send("Bruh I'm a furry bottom who watches vtubers")

    @commands.command(
     name = "send"
  )
    @commands.has_permissions(manage_messages = True)
    async def troll_from_another_channel(self, ctx, channel_from_user, *message):
        """Sends a message to the specified channel from another channel"""
        message = " ".join(message)
        channel_from_user = channel_from_user.lstrip("<#")
        channel_from_user = channel_from_user.rstrip(">")
        channel_to_send = self.bot.get_channel(int(channel_from_user))
        await channel_to_send.send(message)
        await ctx.channel.send(f"Sent message to #{channel_to_send}")
        
    
    
    @discord.slash_command(name = "decide", description = "Decides whether you should do it or not.")
    async def decide(self, interaction: Interaction):
        response_list = ["Yes!", "No!"]
        choice = random.randint(0,1)
        await interaction.response.send_message(response_list[choice])
        
    @commands.command()
    async def joinpos(self, ctx, member: discord.Member = None):
        """Calculates your join position."""
        member = member if member else ctx.author
        order = sorted(ctx.guild.members, key=lambda m: m.joined_at)
        join_pos = order.index(member) + 1
        await ctx.send(join_pos)
    
    @commands.command(
        name = "telephone",
        help = "Talk to Mattbot. Similar to Talking Ben's phone calls. \
            \n$stop (default prefix) stops the call",
        brief = "Talk to Mattbot. Similar to Talking Ben's phone calls."
    )
    async def hohoho(self, ctx):
        await ctx.channel.send("*Connecting to Mattbot...*")
        await ctx.channel.send("sup")
        while True:
            
            try:
                msg = await self.bot.wait_for("message", timeout = 60.0)
            except asyncio.TimeoutError:
                await ctx.channel.send("No response, call ended.")
                break
            
            if msg.content != f"{prefix.return_prefix(ctx.guild)}stop" and msg.channel == ctx.channel:
                if msg.author == self.bot.user:
                    return
                chance = random.randint(0,100)
                if chance in range(13):
                    await ctx.channel.send("*Matt has hung up on you!*")
                    break
                else:
                    response = talking_ben_simulator()
                    await ctx.channel.send(response)
            else:
                await ctx.channel.send("Call stopped.")
                break

    
def setup(bot):
    bot.add_cog(FunCommands(bot))
