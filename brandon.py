#!/usr/bin/python3
import logging
import requests
import asyncio
import re
from asyncio import CancelledError
from discord.ext import commands
from discord.ext.commands import Context, MissingRequiredArgument
from datetime import datetime


import credentials  # Make your own credentials file
from util import util
from util import content_mapping as cm

description = """A man so great we had to somehow imitate his life."""

# Set up logger for this class and discord
logger = logging.getLogger('brandon')
logger.setLevel(logging.INFO)
loggerd = logging.getLogger('discord')
loggerd.setLevel(logging.INFO)

# Set up file handler
handler = logging.FileHandler(filename='logs/brandon.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('[brandon] %(levelname)s %(asctime)s:%(name)s: %(message)s'))

# Add file handler to loggers
logger.addHandler(handler)
loggerd.addHandler(handler)
util.util_logger.addHandler(handler)

# Set up bot with ? command prefix
bot = commands.Bot(command_prefix='!', description=description)

# Specify Wednesday discord channel
brandon_channel = None

async def respond_to(message, responses, mentioned):
    channel = message.channel
    for a in responses:
        if a[1] != '':
            await bot.add_reaction(message, a[1])
        if a[0] != '':
            await bot.send_message(channel, a[0])
        if a[2]:  # Stop processing results
            return
    if len(responses) == 0 and mentioned:
        await bot.add_reaction(message, '👀')  # :eyes:


@bot.event
async def on_ready():
    logger.info('-+-+-+-+-+-+-')
    logger.info(bot.user.name)
    logger.info('is alive...')
    logger.info(bot.user.id)
    logger.info('-+-+-+-+-+-+-')


"""

@bot.command(pass_context=True)
async def day(ctx):

    #Prints a helpful, friendly message to let you know which day of the week it is.
    #Also provides a helpful visual, in case you are still confused.

    channel = ctx.message.channel
    today = datetime.today().weekday()
    await bot.say(util.my_dudes(today))
    await bot.send_file(channel, util.image(today))
    
"""

@bot.event
async def on_message(message):
    if not message.author.id == bot.user.id:  # don't reply to your own messages
        if message.channel.is_private:
            if not persistence.is_dude(message.author.id):
                await bot.send_message(message.channel, 'Hey there. Slidin in the DMs are we?')
                await bot.send_message(message.channel, ':wink:')
        if bot.user.mentioned_in(message) and message.mention_everyone is False:
            if util.thanked(message.content.lower()):
                await bot.send_message(message.channel, 'You\'re welcome, my dude')
                await bot.add_reaction(message, '❤')  # :heart:
                return
            await respond_to(message, cm.mentioned_in(message.content.lower()), True)
            return
        await respond_to(message, cm.listen_to(message.content.lower()), False)
        if len(message.attachments) > 0:
            logger.info(str(message.author) + " sent " + str(message.attachments) + " attachments.")
            return
    await bot.process_commands(message)


@bot.event
async def on_command_error(error, ctx):
    if error == MissingRequiredArgument:
        logger.error(str(ctx.message) + " : not enough arguments\n" + str(error))
    if error == CancelledError:
        logger.error(str(error))


if __name__ == "__main__":
    # This MUST be the final function call that runs
    bot.run(credentials.get_creds('token'))
