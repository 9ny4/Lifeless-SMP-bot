import discord
from discord.ext import commands
import json
from mojang import MojangAPI


async def get_data(ctx, member, users):
    if str(member.id) in users:
        bal = users[str(member.id)]["purse"]
        hasvip = "User does not have vip"
        vip = discord.utils.find(
            lambda r: r.name == '-V.I.P-', ctx.message.guild.roles)
        vipPluss = discord.utils.find(
            lambda r: r.name == 'VIP+', ctx.message.guild.roles)
        if vip in member.roles:
            hasvip = "User has vip"
        if vipPluss in member.roles:
            hasvip = "User has vip"
        roles = member.roles
        roles.reverse()
        highest = roles[0]
        highestRole = discord.utils.find(
            lambda r: r.name == str(highest), ctx.message.guild.roles)
        if "." in member.display_name:
            nickname = member.display_name[:-1]
        if not "." in member.display_name:
            nickname = member.display_name
        embed = discord.Embed(
            title="Lookup", description="Veiw basic stats of  this user.", color=0xed1212)
        embed.set_author(name="Lifeless SMP")
        embed.add_field(name="Does member have vip",
                        value=hasvip, inline=False)
        embed.add_field(name="Balance", value=bal, inline=False)
        embed.add_field(name="Highest role", value=highestRole, inline=False)
        embed.add_field(name="Discord id", value=member.id)
        embed.add_field(name="Minecraft Name",
                        value=nickname, inline=False)
        embed.add_field(name="UUID", value=MojangAPI.get_uuid(nickname))
        embed.set_footer(text="Enjoy your stay with us! The prfix is -")
        await ctx.send(embed=embed)


class misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="For sus people, Usage '-sus'")
    async def sus(self, ctx):
        embed = discord.Embed(title="Cought🎥In📷4K📸", color=0xc90808)
        await ctx.send(embed=embed)

    @commands.command(description="Lookup a user with their id or mention")
    async def lookup(self, ctx, member: discord.Member):
        with open("Economy.json", "r") as f:
            users = json.load(f)
        await get_data(ctx, member, users)

    @lookup.error
    async def lookup_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You didnt specify a user to lookup")
        else:
            print(error)
            await ctx.send("Something happend dm xbtq")


def setup(bot):
    bot.add_cog(misc(bot))
