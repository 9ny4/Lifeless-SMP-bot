import discord
from discord.ext import commands
from discord.utils import get
from config import token, commandPrefix
import os
import json
import time


client = commands.Bot(command_prefix=commandPrefix, help_command=None, intents=discord.Intents.all(
), status=discord.Status.online, activity=discord.Game(f'{commandPrefix}help | Lifeless SMP'))


@client.event
async def on_ready():
    print(
        f'Alrighty! Im up and going! My current letency is {round(client.latency * 1000)}ms')
    print('The Prefix is ', commandPrefix)


@client.event
async def on_message(message):
    if message.author.bot:
        return
    if "<@!834469368439242873>" in message.content:
        await message.reply("Why did you ping my creator? He will not hesitate to ban you. Be carefull")
    await client.process_commands(message)

@client.event
async def on_member_join(member):
    channel = "883729898533961779"
    await channel.send("Welcome {0} to the lifeless SMP discord! Please verify your minecraft account by running -verify 'Your minecraft username' in this channel! Please enjoy your stay with us!".format(member.mention))


@client.command(name="load", description="Loads a command library")
async def load(ctx, extension):
    if ctx.author.id == 834469368439242873:
        client.load_extension(f'cogs.{extension}')
        await ctx.send('Loaded extension')
        print('{0} Extension loaded by {1}'.format(extension, ctx.author))
    else:
        await ctx.send('Missing Perms')


@client.command(name="Unload", description="Unloads a command library")
async def unload(ctx, extension):
    if ctx.author.id == 834469368439242873:
        client.unload_extension(f'cogs.{extension}')
        await ctx.send('Unloaded extension')
        print('{0} Extension unloaded by {1}'.format(extension, ctx.author))
    else:
        await ctx.send('Missing Perms')


@client.command(name="reload", description="Reloads a command library")
async def reload(ctx, extension):
    if ctx.author.id == 834469368439242873:
        client.unload_extension(f'cogs.{extension}')
        time.sleep(0.2)
        client.load_extension(f'cogs.{extension}')
        await ctx.send('reloaded extension')
        print('{0} Extension reloaded by {1}'.format(extension, ctx.author))
    else:
        await ctx.send('Missing Perms')


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


client.run(token)
