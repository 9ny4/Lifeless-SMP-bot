import discord
import json
import random
import os
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
from operator import attrgetter, itemgetter


async def update_data_fish(users, user):
    if not str(user.id) in users:
        users[str(user.id)] = {}
        users[str(user.id)]['purse'] = 0


async def add_money(users, cash, user):
    users[str(user.id)]['purse'] += cash


async def get_data_fish(users, user, ctx):
    if not str(user.id) in users:
        await ctx.send('User has no data in the current system.')
    if str(user.id) in users:
        balance = users[str(user.id)]['purse']
        embed = discord.Embed(
            title="Balance", description=f"View {user.mention} current points earned from fishing", color=0xed1212)
        embed.set_author(name="Lifeless SMP")
        embed.add_field(
            name="Balance", value='{0} points'.format(balance), inline=True)
        embed.set_footer(
            text="Please enjoy your stay with us! The prefix is -")
        await ctx.send(embed=embed)


async def buy_revive(users, user, ctx):
    if not str(user.id) in users:
        await ctx.send('Your not in our systems. Run the fish command at least once!')
    if str(user.id) in users:
        if users[str(user.id)]['purse'] >= 2500:
            vip = discord.utils.find(
                lambda r: r.name == '-V.I.P-', ctx.message.guild.roles)
            vipPluss = discord.utils.find(
                lambda r: r.name == 'VIP+', ctx.message.guild.roles)
            if vip or vipPluss in user.roles:
                users[str(user.id)]['purse'] -= 2250
                await ctx.send('Since you have VIP you paid 10% less<3')
            else:
                users[str(user.id)]["purse"] -= 2500
        else:
            await ctx.send('You dont have the points needed to buy a revive! you need {0}'.format(2500 - users[str(user.id)]['purse']))


async def add_points(users, ctx, member, points):
    if str(member.id) in users:
        users[str(member.id)]['purse'] += int(points)
    if not str(member.id) in users:
        users[str(member.id)] = {}
        users[str(member.id)]['purse'] = 0
        users[str(member.id)]['purse'] += int(points)


async def remove_points(users, ctx, member, points):
    if str(member.id) in users:
        users[str(member.id)]['purse'] -= int(points)
    if not str(member.id) in users:
        users[str(member.id)] = {}
        users[str(member.id)]['purse'] = 0
        users[str(member.id)]['purse'] -= int(points)


async def buy_vip(users, user, ctx):
    if not str(user.id) in users:
        users[str(user.id)] = {}
        users[str(user.id)]['purse'] = 0
        await ctx.send('You didnt have any data in our system so i added you <3 run the -fish command to get points!')
    if str(user.id) in users:
        if users[str(user.id)]['purse'] >= 5000:
            role = discord.utils.find(
                lambda r: r.name == '-V.I.P-', ctx.message.guild.roles)
            if role in user.roles:
                await ctx.send('You already have vip!')
            elif not role in user.roles:
                users[str(user.id)]['purse'] -= 5000
                users[str(user.id)]['purse'] += 2250
                await user.add_roles(role)
                await ctx.send('You bought VIP! I added 2250 to your balance for a free revive!')
        else:
            await ctx.send('You dont seem to have the requierd points! Your missing {0} points to buy VIP!'.format(5000 - users[str(user.id)]['purse']))


async def GiveAllPoints(ctx, users, points):
    for member in ctx.guild.members:
        if not str(member.id) in users:
            users[str(member.id)] = {}
            users[str(member.id)]['purse'] = 0
            print("{0} not is our system adding them".format(member))
        if str(member.id) in users:
            users[str(member.id)]['purse'] += int(points)
            print("Added {0} points to {1} balance from giveall".format(
                points, member))


async def pay_points(ctx, users, member, points):
    if not str(member.id) in users:
        users[str(member.id)] = {}
        users[str(member.id)]['purse'] = 0
        await ctx.send('User wasnt in our system so I added him. Please run command again')
    if str(member.id) in users:
        if str(member.id) == str(ctx.author.id):
            await ctx.send('Cant send money to yourself!')
        if not str(member.id) == str(ctx.author.id):
            if users[str(ctx.author.id)]['purse'] > int(points):
                users[str(ctx.author.id)]['purse'] -= int(points)
                users[str(member.id)]['purse'] += int(points)
                await ctx.send('Gave {0} {1} points from {2} blance'.format(member, points, ctx.author))
            else:
                await ctx.send('Your missing some points there bud!')


class economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Adds points to your balance, Usage '-fish'", aliases=['2+2'])
    @commands.cooldown(2, 3600, commands.BucketType.user)
    async def fish(self, ctx):
        if not ctx.author.bot:
            if random.random() < 0.65:
                fishes = ['Salmon', 'Tropical Fish', 'Cod', 'Pufferfish']
                fish = random.choice(fishes)
                money = random.randrange(5, 100)

                with open('Economy.json', 'r') as f:
                    users = json.load(f)
                vip = discord.utils.find(
                    lambda r: r.name == '-V.I.P-', ctx.message.guild.roles)
                vipPluss = discord.utils.find(
                    lambda r: r.name == 'VIP+', ctx.message.guild.roles)
                if vip in ctx.author.roles:
                    money = random.randrange(75, 250)
                if vipPluss in ctx.author.roles:
                    money = random.randrange(125, 350)
                print('{0} got a {1} worth {2}'.format(
                    ctx.author, fish, money))

                await update_data_fish(users, ctx.author)
                await add_money(users, money, ctx.author)

                with open('Economy.json', 'w') as f:
                    json.dump(users, f)

                embed = discord.Embed(
                    title='Fish', description='Congrats you cought a fish! Read  below to see what you cauth and how much its worth', color=0xed1212)
                embed.set_author(name='Lifeless SMP')
                embed.add_field(name='You cauth a {0}'.format(fish),
                                value='Worth {0} points'.format(money), inline=True)
                embed.set_footer(
                    text='Please enjoy your stay with us! The prefix is -')
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    title="Fish", description="Sorry you didnt catch anything this time!", color=0xed1212)
                embed.set_author(name="Lifeless SMP")
                embed.set_footer(
                    text="Please enjoy your stay with us! The prefix is -")
                await ctx.send(embed=embed)

    @fish.error
    async def fish_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            em = discord.Embed(title=f"Slow it down bro!",
                               description=f"This command is on cooldown! Try again later.", color=0xc90808)
            await ctx.send(embed=em)
        else:
            print(error)

    @commands.command(description="Gets your balance or another members balance, Usage '-bal', '-bal @xbtq'", aliases=["bal", "bank"])
    async def balance(self, ctx, member: discord.Member = None):
        with open('Economy.json', 'r') as f:
            users = json.load(f)

        if not member:
            await get_data_fish(users, ctx.author, ctx)
        if member:
            await get_data_fish(users, member, ctx)

    @commands.command(description="Sends a revive request to the admins, usage '-revive xbtq'")
    async def revive(self, ctx):
        with open('Economy.json', 'r') as f:
            users = json.load(f)

        if str(ctx.author.id) in users:
            if users[str(ctx.author.id)]['purse'] >= 2500:
                await buy_revive(users, ctx.author, ctx)
                await ctx.send('{0} You bought a revive, ive sent a request to the admins and they will review it when they can!'.format(ctx.author.mention))
                channel = self.bot.get_channel(885548723214631022)
                await channel.send('{0} bought a revive! Their username is __{1}__ react with a checkmark to this when its completed <@&883728118769156157>'.format(ctx.author.mention, ctx.author.nick))
            else:
                await ctx.send('You seem to be missing some points! you need {0} more points to buy a revive.'.format(2500 - users[str(ctx.author.id)]['purse']))
        else:
            await ctx.send('You have no data in the current system.')

        with open('Economy.json', 'w') as f:
            json.dump(users, f)

    @commands.command(description="Add points to a user, Usage '-ap @xbq 1000'")
    @commands.has_permissions(administrator=True)
    async def ap(self, ctx, member: discord.Member, points):
        with open('Economy.json', 'r') as f:
            users = json.load(f)

        await add_points(users, ctx, member, points)
        await ctx.send('Added {0} points to {1}'.format(points, member))

        with open('Economy.json', 'w') as f:
            json.dump(users, f)

    @ap.error
    async def ap_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Missing permission")

    @commands.command(description="Removes ponits from a user, Usage '-rp @xbtq 1000'")
    @commands.has_permissions(administrator=True)
    async def rp(self, ctx, member: discord.Member, points):
        with open('Economy.json', 'r') as f:
            users = json.load(f)

        await remove_points(users, ctx, member, points)
        await ctx.send('Removed {0} points from {1}'.format(points, member))

        with open('Economy.json', 'w') as f:
            json.dump(users, f)

    @rp.error
    async def rp_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Missing permission")

    @commands.command(description="Force revives a player. Does not take ponits from your balance, Usage '-frevive xbtq'")
    @commands.has_permissions(administrator=True)
    async def frevive(self, ctx, username):
        await ctx.send('{0} You force revived {1}'.format(ctx.author.mention, username))
        channel = self.bot.get_channel(883732690128498688)
        await channel.send('{0} force revived __{1}__ react with a checkmark to this when its completed'.format(ctx.author.mention, username))

    @frevive.error
    async def frevive_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('You didnt specify a username to revive! Example ``-frevive xbtq``')

    @commands.command(description="Buy vip on the smp for points, usage '-buyvip xbtq'")
    async def buyvip(self, ctx):
        with open('Economy.json', 'r') as f:
            users = json.load(f)

        await ctx.send('Attepting to buy vip...')
        await buy_vip(users, ctx.author, ctx)

        role = discord.utils.find(
            lambda r: r.name == 'VIP', ctx.message.guild.roles)
        if role in ctx.author.roles:
            channel = self.bot.get_channel(872495121269162004)
            await channel.send('{0} bought vip! The name under the perchase is __{1}__'.format(
                ctx.author.mention, ctx.author.nick))

        with open('Economy.json', 'w') as f:
            json.dump(users, f)

    @buyvip.error
    async def buyvip_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('You didnt specify a username to give vip to')
        else:
            print(error)

    @commands.command(description="Give a user vip, Usage '-givevip @xbtq xbtq'")
    @commands.has_permissions(administrator=True)
    async def givevip(self, ctx, member: discord.Member):
        role = discord.utils.find(
            lambda r: r.name == '-V.I.P-', ctx.message.guild.roles)
        if role in member.roles:
            await ctx.send("That member already have vip!")
        else:
            with open('Economy.json', 'r') as f:
                users = json.load(f)

            await add_points(users, ctx, member, 2250)
            await member.add_roles(role)
            await ctx.send('Gave {0} vip.'.format(member.nick))
            channel = self.bot.get_channel(872495121269162004)
            await channel.send('{0} was given vip by {1}! The name is __{2}__'.format(member.mention, ctx.author.mention, member.nick))

            with open('Economy.json', 'w') as f:
                json.dump(users, f)

    @commands.command(description="Gives everyone points")
    async def giveall(self, ctx, points):
        if ctx.author.id == 834469368439242873:
            with open('Economy.json', 'r') as f:
                users = json.load(f)

            await GiveAllPoints(ctx, users, points)

            with open('Economy.json', 'w') as f:
                json.dump(users, f)

            await ctx.send("Gave everyone {0} points".format(points))
        else:
            await ctx.send("Good try")

    @commands.command(description='Give someone your points! usage "-pay @xbtq 2500"', aliases=['give'])
    async def pay(self, ctx, member: discord.Member, points):
        role = discord.utils.find(
            lambda r: r.name == '-V.I.P-', ctx.message.guild.roles)
        if role in ctx.author.roles:
            with open('Economy.json', 'r') as f:
                users = json.load(f)

            await pay_points(ctx, users, member, points)

            with open('Economy.json', 'w') as f:
                json.dump(users, f)
        else:
            await ctx.send('Your not vip!')

    @pay.error
    async def pay_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('You didnt specify a username or points to give')
        else:
            print(error)

    @commands.command(description='Tells you how to buy vip+')
    async def vipp(self, ctx):
        await ctx.send("Wanna buy vip+? Send 5 usd or 44 nok to <https://paypal.me/xbtq>")


def setup(bot):
    bot.add_cog(economy(bot))
