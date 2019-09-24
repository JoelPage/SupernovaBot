# bot.py
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

import helpers

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='create-channel')
@commands.has_role('Officer')
async def create_channel(ctx, channel_name='new-channel-' + str(helpers.getTimeInMilliseconds())):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        print(f'Creating a new channel: {channel_name}')
        await guild.create_text_channel(channel_name)

bot.run(TOKEN)
