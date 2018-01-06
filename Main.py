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
bot_request = "398983251101745182"
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
        await bot.change_presence(game = discord.Game(name='Coders Server'))
        bot.load_extension("Admin")
        bot.load_extension("NSFW")

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

    @bot.command(pass_context = True)
    async def gbans(ctx):
        '''Gets A List Of Users Who Are No Longer With us'''
        x = await bot.get_bans(ctx.message.server)
        x = '\n'.join([y.name for y in x])
        embed = discord.Embed(title = "List of The Forgotten", description = x, color = 0xFFFFF)
        embed.set_footer(text="Coder Bot v1.0")
        return await bot.say(embed = embed)

    @bot.command(pass_context = True)
    async def iamrewrite(ctx):
        role = discord.utils.get(ctx.message.server.roles, name="Discord.py Rewrite")
        if "Discord.py Rewrite" in [role.name for role in ctx.message.author.roles]:
            await bot.remove_roles(ctx.message.author, role)
            await bot.say(":x:  | You already had the `Discord.py Rewrite` role added, so I removed it")
        else:
            await bot.add_roles(ctx.message.author, role)
            await bot.say(":white_check_mark: | I've Given You The `Discord.py Rewrite` Role")

    @bot.command(pass_context = True)
    async def iamasync(ctx):
        role = discord.utils.get(ctx.message.server.roles, name="Discord.py Async")
        if "Discord.py Async" in [role.name for role in ctx.message.author.roles]:
            await bot.remove_roles(ctx.message.author, role)
            await bot.say(":x:  | You already had the `Discord.py Async` role added, so I removed it")
            msg = '{} removed their role `Discord.py Asyc`'.format(ctx.message.author)
            await bot.send_message(discord.utils.get(ctx.message.server.channels, name="logs"), msg)
        else:
            await bot.add_roles(ctx.message.author, role)
            await bot.say(":white_check_mark: | I've Given You The `Discord.py Async` Role")
            msg = '{} gave themself the role `Discord.py Async`'.format(ctx.message.author)
            await bot.send_message(discord.utils.get(ctx.message.server.channels, name="logs"), msg)

    @bot.command(pass_context = True)
    async def ownerbday():
        now=datetime.datetime.utcnow()
        bday1 = now.year + 1
        bday=datetime.datetime(bday1, 9, 16)
        if bday<now:
            bday=bday.replace(year=now.year+1)
        delta=bday-now
        y, remainder4 = divmod(int(delta.total_seconds()), 31536025)
        months, remainder5 = divmod(remainder4, 2592000)
        weeks, remainder = divmod(remainder5, 604800)
        days, remainder2 = divmod(remainder, 86400)
        hours, remainder3=divmod(remainder2, 3600)
        minutes, seconds=divmod(remainder3, 60)

        embed=discord.Embed(colour = discord.Colour(0xA522B3))
        embed.add_field(name=":gift::wrench::gift: Time left until Bot Owner's Birthday :gift::wrench::gift:",
            value=f"{y} year, {months} months, {weeks} weeks, {days} days, {hours} hours, {minutes} minutes.")
        await bot.say(embed=embed)
    @bot.command()
    async def roast(member : discord.Member = None):
        color = ''.join([random.choice('0123456789ABCDEF') for x in range(6)])
        color = int(color, 16)
        embed = discord.Embed(colour=discord.Colour(value=color))
        choice = random.choice(insults)
        embed.add_field(name = "Roast", value = member.mention +" , "+ (choice))
        embed.set_footer(text="You just got Roasted, You need some ice?")
        await bot.say(embed = embed)

    @bot.command(pass_context=True)
    async def verify(ctx, member: discord.Member = None):
        user_roles = [r.name.lower() for r in ctx.message.author.roles]

        if "admin" in user_roles:
            if member is None:
                await bot.say(":x: | Please Tag a Users Bot!")
            else:
                oldrole = discord.utils.get(member.server.roles, name="Not Yet Verified")
                role = discord.utils.get(member.server.roles, name="Verified Bot")
                await bot.remove_roles(member, oldrole)
                await bot.add_roles(member, role)
                await bot.say(":white_check_mark: Succesfully verified {}".format(member))
        else:
            msg = ':eyes: | {} Tried to use `verify` | ID: {}'.format(ctx.message.author, ctx.message.author.id)
            await bot.send_message(discord.utils.get(ctx.message.server.channels, name="logs"), msg)
            await bot.say(":x: | Admin Only! | Action has been logged!")

    @bot.event
    async def on_member_join(member):
        if member.bot is True:
            role = discord.utils.get(member.server.roles, name="Not Yet Verified")
            await bot.add_roles(member, role)
      
    @bot.event
    async def on_message(message):
        if message.channel.id == bot_request:
            if len(message.content) == 18:
                invite = "https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=0".format(message.content)
                embed = discord.Embed(title="Bot added", description="'[{}]({})'".format("Bot invite", invite), color = 0x00ff00)
                embed.add_field(name="Bot Lister", value=message.author, inline=False)
                await bot.delete_message(message)
                await bot.say(embed = embed)
                await bot.send_message(verif, embed=embed)
            else:
                await bot.delete_message(message)
                await bot.send_message(message.author, ":x: Please only paste your bot's ID in #bot-requests")
        await bot.process_commands(message)

if not os.environ.get('TOKEN'):
        print("No Token Found")
bot.run(os.environ.get('TOKEN').strip('\"'))
