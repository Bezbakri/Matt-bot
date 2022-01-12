"""
Rev's command handling cog, repurposed from Ouranos.

Error handling event from Ouranos class: https://github.com/nwunderly/ouranos/blob/master/ouranos/bot.py
Custom error classes from errors.py: https://github.com/nwunderly/ouranos/blob/master/ouranos/utils/errors.py

Note: this code is untested but should help with implementing custom error handling for something like command responses.
"""

from discord.ext import commands
import discord

TICK_RED = "❌"

"""
# my custom errors, copy pasted from errors.py
# useful for killing a command execution and returning a message for the user.

class OuranosCommandError(commands.CommandError):
    def __init__(self, message):
        self._msg = message
        super().__init__(message)

# this one just has a different response. works the same way
class UnexpectedError(OuranosCommandError):
    pass
"""

class ErrorHandler(commands.Cog):
    """A cog that adds some basic command error handling to your bot."""
    '''def __init__(self, bot):
        self.bot = bot'''

    async def _respond_to_error(self, ctx, error):
        """Function containing my normal error responses for command errors."""
        # UserInputError is the user using the command wrong, for example missing an argument.
        # we just return the message discord.py gives us since that's usually helpful.
        if isinstance(error, commands.UserInputError):
            await ctx.send(f"{TICK_RED} {str(error).capitalize()}")
        
        # These are just my custom errors. When I want to tell the user "hey you can't do this" I raise OuranosCommandError.
        # If I want to make a note about "hey this shouldn't have happened" I raise UnexpectedError.
        # Commented these out since they're not going to happen normally. but left it here for an explanation.
        # elif isinstance(error, UnexpectedError):
        #     await ctx.send(f'{TICK_RED} An unexpected error occurred:```\n{error}\n```')
        # elif isinstance(error, OuranosCommandError):
        #     await ctx.send(f"{TICK_RED} {error}")
            
        # The bot tried to do something (send a message, ban someone, etc) but doesnt have the permissions.
        elif isinstance(error, discord.Forbidden):
            await ctx.send(f'{TICK_RED} I do not have permission to execute this action.')
            
        # sometimes discord.py wraps an error in CommandInvokeError.
        # I dont need to handle Forbidden twice but I forget which is the one we need.
        elif isinstance(error, commands.CommandInvokeError):
            # CommandInvokeError *should* wrap another error.
            # This just pulls that error out since it's the one we want.
            error = error.original or error
            
            # discord permissions error on an action that's not allowed. same as above.
            if isinstance(error, discord.Forbidden):
                await ctx.send(f'{TICK_RED} I do not have permission to execute this action.')
                
            # self-explanatory. Not found. Something like trying to bot.fetch_guild(id) with a guild it's not in,
            # or bot.fetch_user(id) for a user that doesnt exist.
            elif isinstance(error, discord.NotFound):
                await ctx.send(f"{TICK_RED} Not found: {error.text.lower().capitalize()}.")
                
            # discord complaining about a request we made. this isn't expected and should rarely happen,
            # but this will make the bot reply to your command telling you what went wrong.
            elif isinstance(error, discord.HTTPException):
                await ctx.send(f'{TICK_RED} An unexpected error occurred:```\n{error.__class__.__name__}: {error.text}\n```')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, exception):
        """This is the event. I removed the logging since discord.py should log it anyway.
        
        It's still in its own function so logging and responding can be separated easily.
        """
        try:
            await self._respond_to_error(ctx, exception)
        except discord.DiscordException:
            # if we can't send a message when trying to tell the user what went wrong,
            # let's just skip it since at that point it's not my problem.
            pass


'''def setup(bot):
    bot.add_command(ErrorHandler(bot))'''
