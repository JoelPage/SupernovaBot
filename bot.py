# bot.py
import os
import discord
import helpers
import asyncio

from discord.ext import commands
from dotenv import load_dotenv

def run():
	bot.run(TOKEN)

async def start():
	print("Starting Discord Bot")
	await bot.start(TOKEN)
	print("Started Discord Bot")
	
async def exit():
	await logout()
	
async def logout():
	print("Logging out of Discord Bot")
	await bot.logout()

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f"""Hi {member.name}, welcome to Supernova's discord server! 
Please set your nickname to be your in-game character name and leave us a message in #new-arrivals and we will get back to you!"""
    )

@bot.command(name='create-event')
@commands.has_role('Officer')
async def create_event(ctx, event_name=f"new-event-{helpers.getTimeInMilliseconds()}"):
	print(f"Creating event at {event_name}.xml")
	helpers.CreateDummyEvent(f"{event_name}.xml")

@bot.command(name='create-channel')
@commands.has_role('Officer')
async def create_channel(ctx, channel_name=f"new-channel-{helpers.getTimeInMilliseconds()}"):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        print(f'Creating a new channel: {channel_name}')
        await guild.create_text_channel(channel_name)