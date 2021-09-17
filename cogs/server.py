import discord
from discord.ext import commands
import requests
from mcstatus import MinecraftServer
from config import LifelessIp, LifelessIPQuery
import datetime
from datetime import datetime
from mojang import MojangAPI


class Server(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Gets the status of the server, Usage '-status'")
    @commands.cooldown(2, 600, commands.BucketType.guild)
    async def status(self, ctx):
        await ctx.send('Getting Status! Please allow up to 10 seconds')
        try:
            server = MinecraftServer.lookup(
                "{0}".format(LifelessIp))
            status = server.status()
            print("Connected! The server has {0} players and replied in {1} ms".format(
                status.players.online, status.latency))
            embed = discord.Embed(
                title="Status", description="This is the status of the smp, it will include the amount of players online and the current ping for the server. To  get a list of all online players use the online command!", color=0xc90808)
            embed.set_author(
                name="Lifeless SMP")
            embed.add_field(name="Online Players",
                            value=status.players.online, inline=True)
            embed.add_field(name="Server Ping",
                            value=status.latency, inline=True)
            embed.add_field(name="Server IP", value=LifelessIp, inline=True)
            embed.set_footer(
                text="Please Enjoy your stay with us! Prefix is -")
            await ctx.send(embed=embed)
        except:
            print("Something happend")
            await ctx.send("Failed to connect! Server might be offline")

    @status.error
    async def status_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            em = discord.Embed(title=f"Slow it down bro!",
                               description=f"This command is on cooldown! Try again later. This is to prevent mass pining the server.", color=0xc90808)
            await ctx.send(embed=em)
        else:
            print(error)

    @commands.command(description="Gives a list of online players, Usage '-online'")
    @commands.cooldown(2, 600, commands.BucketType.guild)
    async def online(self, ctx):
        await ctx.send('Getting Players! Please allow up to 10 seconds')
        try:
            server = MinecraftServer.lookup(LifelessIPQuery)
            status = server.status()
            print("Connected! The server has {0} players and replied in {1} ms".format(
                status.players.online, status.latency))
            query = server.query()
            print("The server has the following players online: {0}".format(
                ", ".join(query.players.names)))

            embed = discord.Embed(title="Current Online players", description="{0}".format(
                ", ".join(query.players.names)), color=0xc90808)
            await ctx.send(embed=embed)
        except:
            print("Something happend")
            await ctx.send("Failed to connect! Server might be offline")

    @commands.command(description="Report a user, usage '-report xbtq was killing people'")
    @commands.cooldown(1 , 600)
    async def report(self, ctx, username):
        channel = self.bot.get_channel(887683453758341181)
        await ctx.send("Ive sent your report to the staff!")
        await channel.send("{0} has reported __**{1}**__ for __**{2}**__".format(
            ctx.author.mention, username, ctx.message.content.split(' ', 2)[2]))
            

    @report.error
    async def report_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('You didnt specify a username to report! Example ``-report xbtq Killing me``')
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(" You can only report once every 10 minute")

    @commands.command(aliases=['sug', 'sugg'], description="Suggest a new feature for the smp or the discord! Example '-suggest a new kit'")
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def suggest(self, ctx):
        channel = self.bot.get_channel(883732909993898085)
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        try:
            embed = discord.Embed(title="New suggestion by {0}".format(
                ctx.author), description="{0}".format(ctx.message.content.split(' ', 1)[1]), color=0xc90808)
            embed.set_footer(text="Suggested at {0}".format(dt_string))
            msg_embed = await channel.send(embed=embed)
            await msg_embed.add_reaction("✅")
            await msg_embed.add_reaction("❌")
            await ctx.send('You suggested ``{0}`` check the suggestion channel if its appeard!'.format(ctx.message.content.split(' ', 1)[1]))
        except:
            await ctx.send("A error occurred while trying to suggest a new feature. Please dm xbtq")

    @suggest.error
    async def suggest_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('You didnt suggest anything!')
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send('You can only suggest something every hour!')
        else:
            print(error)

    @commands.command(description="Verify yourself")
    async def verify(self, ctx, username):
        member = discord.utils.find(
            lambda r: r.name == 'People', ctx.message.guild.roles)
        if member not in ctx.author.roles:
            uuid = MojangAPI.get_uuid(username)
            if uuid == None:
                await ctx.author.send("The username you entered dosent exist! Please try again...")
            if not uuid == None:
                profile = MojangAPI.get_profile(uuid)
                await ctx.author.edit(nick=f"{username}.")
                await ctx.author.add_roles(member)
                await ctx.author.send("Verification successful! Your current account linked is {0} If you buy vip this is the account that gets vip! Dm xbtq to change it. Your current skin is {1}".format(username, profile.skin_url))
                await channel.send("{0} Verified themself as __{1}__ with uuid of **{2}**".format(ctx.author.mention, username, uuid))
        else:
            await ctx.send("Your already verifed! If you wanna change nickname dm xbtq", delete_after=5)
        await ctx.message.delete()
        channel = self.bot.get_channel(883732690128498688)

    @verify.error
    async def verify_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('You need to specify your minecraft username! If you buy vip the username you give now is what gets vip.', delete_after=10)
            await ctx.message.delete()
        else:
            print(error)


def setup(bot):
    bot.add_cog(Server(bot))
