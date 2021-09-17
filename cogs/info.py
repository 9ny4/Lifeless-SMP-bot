import discord
from discord.ext import commands


class information(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Basic Info, Usage '-info'")
    async def info(self, ctx):
        embed = discord.Embed(
            title="Info", description="Welcome To The Lifeless SMP!", color=0xc90808)
        embed.set_author(
            name="Lifeless SMP")
        embed.add_field(name="IP: ", value=LifelessIp, inline=True)
        embed.set_footer(text="Please Enjoy your stay with us! Prefix is -")
        await ctx.send(embed=embed)

    @commands.command(description="Basic Help command, Usage '-help'")
    async def help(self, ctx):
        embed = discord.Embed(
            title="Help", description="A list of some commands", color=0xc90808)
        embed.set_author(
            name="Lifeless SMP")
        embed.add_field(
            name="info", value="Will tell you some basic stuff about the smp", inline=True)
        embed.add_field(
            name="status", value="Shows you the status of the smp can be usefull for checking if the server is online or not", inline=True)
        embed.add_field(
            name="online", value="Will show a list of all online players", inline=True)
        embed.add_field(
            name='fish', value='You can catch a random fish worth a random amount', inline=True)
        embed.add_field(
            name='Balance', value='View you current balance from fishing', inline=True)
        embed.set_footer(text="Please Enjoy your stay with us! Prefix is -")
        await ctx.send(embed=embed)

    @commands.command(description="Sends a list of all commands, Usage '-cmds'", aliases=["cmd", "cmds", "command"])
    async def commands(self, ctx):
        cmdtext = ""
        for command in self.bot.commands:
            cmdtext += f"{command.qualified_name} - {command.description}\n"
        cmdtext += ""
        await ctx.send(
            "```{0}```".format(cmdtext)
        )


def setup(bot):
    bot.add_cog(information(bot))
