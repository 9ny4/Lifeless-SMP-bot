import discord
from discord.ext import commands


class moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Kicks a user from the discord server, Usage '-kick @xbtq'")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        if not member.bot:
            await member.kick(reason=reason)
            await ctx.send('{0} has been kicked form the server. Reason: {1}').format(member, reason)
        else:
            await ctx.send('Cant kick bots.', delete_after=5)

    @commands.command(description="Bans a user from the discord server, Usage '-ban @xbtq'")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        if not member.bot:
            await member.ban(reason=reason)
            await ctx.send('{0} has been banned form the server. Reason: {1}').format(member, reason)
        else:
            await ctx.send('Cant ban bots.', delete_after=5)

    @commands.command(description="Clears a amount of messages, Usage '-clear 100'", aliases=["purge"])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        try:
            if amount > 11:
                await ctx.channel.purge(limit=amount)
                await ctx.send(f'Removed {amount} messages', delete_after=5)
            else:
                await ctx.channel.purge(limit=amount)
                await ctx.send(f'Went with default {amount - 1}', delete_after=5)
        except:
            await ctx.send('If you put number as a argument its not gonna work.. if you didnt contact xbtq#0001')

    @commands.command(description="Deletes a specific message, Usage '-del <message id>'", aliases=["del"])
    @commands.has_permissions(manage_messages=True)
    async def delete(self, ctx, msgID: int):
        await ctx.send("Fetching message", delete_after=5)
        try:
            msg = await ctx.fetch_message(msgID)
            await msg.delete()
            await ctx.send("deleted message", delete_after=5)
        except:
            await ctx.send("Couldnt find message.", delete_after=5)


def setup(bot):
    bot.add_cog(moderation(bot))
