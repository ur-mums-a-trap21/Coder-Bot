import discord
from discord.ext import commands
from discord.ext.commands import Bot
import random
from random import randint
import time
import datetime
import lists
from lists import insults
import os

bot = commands.Bot(command_prefix = 'c.')
bot_request = "442450720751353857"
verif = discord.Object("398961598145888266")

class startup():
    @bot.event
    async def on_ready():
        print("===================================")
        print("Logged in as")
        print("Username: %s"%bot.user.name)
        print("ID: %s"%bot.user.id)
        print('Server count:', str(len(bot.servers)))
        print('User Count:',len(set(bot.get_all_members())))
        print("Py Lib Version: %s"%discord.__version__)
        print("===================================")

    @bot.command(pass_context=True)
    async def ping(ctx):
        """Check The Bots Response Time"""
        t1 = time.perf_counter()
        await bot.send_typing(ctx.message.channel)
        t2 = time.perf_counter()
        thedata = (":ping_pong: **Pong.**\nTime: " + str(round((t2 - t1) * 1000)) + "ms")
        color = ''.join([random.choice('0123456789ABCDEF') for x in range(6)])
        color = int(color, 16)
        data = discord.Embed(description = thedata, colour=discord.Colour(value = color))
        await bot.say(embed = data)

 

      
    @bot.event
    async def on_message(message):
        if message.channel.id == bot_request:
            if message.author.id != bot.user.id:
                if len(message.content) == 18:
                    invite = "https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=104123457".format(message.content)
                    embed = discord.Embed(title="Bot Added! | Please Wait For Mods To Verify The Bot!", description="'[{}]({})'".format("Bot invite", invite), color = 0x00ff00)
                    embed.add_field(name="Bot Lister", value=message.author, inline= True)
                    await bot.delete_message(message)
                    await bot.send_message(message.channel, embed=embed)
                    await bot.send_message(verif, embed=embed)
                else:
                    await bot.delete_message(message)
                    await bot.send_message(message.author, ":x: Please only paste your bot's ID in #bot-requests")
        await bot.process_commands(message)

if not os.environ.get('TOKEN'):
        print("No Token Found")
bot.run(os.environ.get('TOKEN').strip('\"'))
