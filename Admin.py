import discord
from discord.ext import commands
from discord.ext.commands import Bot

bot = commands.Bot(command_prefix = 'c.')

class Admin():
    print("Admin Loaded")

    @bot.command(pass_context = True)
    async def userinfo(ctx, member : discord.Member):
        """Says when a member joined."""
        user_roles = [r.name.lower() for r in ctx.message.author.roles]

        if "admin" in user_roles:
            em = discord.Embed(color=0x00FFF0) #0xea7938 is the color code
            em.set_thumbnail(url=member.avatar_url)
            em.set_footer(text="Coder Bot v1.0")
            em.add_field(name="Name:", value=member.name)
            em.add_field(name="Discriminator:", value='#{}'.format(member.discriminator))
            em.add_field(name="Nickname:", value=member.nick)
            em.add_field(name="ID:", value=member.id)
            em.add_field(name="Status:", value=member.status)
            em.add_field(name="Game:", value=member.game)
            em.add_field(name='In Voice', value=member.voice_channel)
            em.add_field(name="Account was created at:", value=member.created_at)
            em.add_field(name="Joined this server at:", value=member.joined_at)
            em.add_field(name="Roles:", value='Coming Soon')
            em.add_field(name='Highest Role', value=member.top_role.name)
            await ctx.bot.say(embed=em)
        else:
            msg = ':eyes: | {} Tried to use `userinfo` | ID: {}'.format(ctx.message.author, ctx.message.author.id)
            await ctx.bot.send_message(discord.utils.get(ctx.message.server.channels, name="logs"), msg)
            await ctx.bot.say(":x: | Admin Only! | Action has been logged!")

    @bot.command(pass_context=True)
    async def clear(ctx, number):
        '''Clears The Chat 2-100'''
        user_roles = [r.name.lower() for r in ctx.message.author.roles]

        if "admin" in user_roles:
            mgs = []
            number = int(number)
            async for x in ctx.bot.logs_from(ctx.message.channel, limit = number):
                mgs.append(x)
            await ctx.bot.delete_messages(mgs)
        else:
            msg = ':eyes: | {} Tried to use `clear` | ID: {}'.format(ctx.message.author, ctx.message.author.id)
            await ctx.bot.send_message(discord.utils.get(ctx.message.server.channels, name="logs"), msg)
            await ctx.bot.say(":x: | Admin Only! | Action has been logged!")

def setup(bot):
    bot.add_cog(Admin)
