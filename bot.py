# bot.py
import os
import discord
import helpers
import asyncio

from discord.ext import commands
from dotenv import load_dotenv

import commands as i_commands
import events as i_events

import datetime as i_datetime
import time as i_time

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='!')

async def sendDebugMessage(message):
    debugChannelID = 640834927981494276
    channel = bot.get_channel(debugChannelID)
    await channel.send(message)

async def postAnnouncementMessage(message):
    announcementChannelID = 641202921324937218
    channel = bot.get_channel(announcementChannelID)
    await channel.send(message)

def run():
    #print("run()")
    print("Connecting bot to discord...")
    bot.run(TOKEN)

async def update():
    interval = 30
    print("Waiting for bot to be ready...")
    await sendDebugMessage(f"Systems Online! {i_time.time()}\nUpdate ticking every {interval} seconds.")
    await bot.wait_until_ready()
    print(f"Bot now checking events every {interval} seconds")
    while True:
        await check_events()
        await asyncio.sleep(interval)

async def check_events():
    print(f"Checking Events : {i_time.time()}")
    results = i_events.EventManager.check_events()

    # We need to do different things with each result
    # Detect End do nothing
    # Detect Start post to Announcements
    # Detect Reminder post to Announcements
    # Reminder structure
    #   - Time
    #   - Message
    #   - hasBeenPosted

    # Ending
    if results[0] != None and len(results[0]) > 1:
        await sendDebugMessage(results[0])

    # Starting
    if results[1] != None and len(results[1]) > 1:
        for result in results[1][1:]:
            announcementStr = f"@everyone Event {result} begins!"
            await postAnnouncementMessage(announcementStr)
        
        

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    bot.loop.create_task(update())

@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f"""Hi {member.name}, welcome to Supernova's discord server! 
Please set your nickname to be your in-game character name and leave us a message in #new-arrivals and we will get back to you!"""
    )

@bot.command()
@commands.has_role('Officer')
async def create(ctx, *args):
    print(f"Recieved Discord Command create({args})")
    result = i_commands.CommandManager.executeCommand("CREATE", args)

    if result.error != None:
        await ctx.send(f"```{result.error}```")
    else:
        await ctx.send(f"{result.value[0]}\n```xl\n{result.value[1]}```")

@bot.command()
@commands.has_role('Officer')
async def skip(ctx, *args):
    print(f"Recieved Discord Command - skip({args})")
    result = i_commands.CommandManager.executeCommand("SKIP", args)
    
    if result.error != None:
        await ctx.send(result.error)
    else:
        await ctx.send(result.value)

@bot.command()
@commands.has_role('Officer')
async def events(ctx, *args):
    print(f"Recieved Discord Command - events({args})")
    result = i_commands.CommandManager.executeCommand("EVENTS", args)
    
    if result.error != None:
        await ctx.send(result.error)
    else:
        embed = discord.Embed(title="Upcoming Events", description=result.value[1])
        embed.set_footer(text=result.value[0])
        await ctx.send(embed=embed)

@bot.command()
@commands.has_role('Officer')
async def edit(ctx, *args):
    print(f"Recieved Discord Command - edit({args})")
    result = i_commands.CommandManager.executeCommand("EDIT", args)
    
    if result.error != None:
        await ctx.send(f"```{result.error}```")
    else:
        await ctx.send(f"{result.value[0]}\n```xl\n{result.value[1]}```")


# Helper function
#@bot.command(name='create-channel')
#@commands.has_role('Officer')
#async def create_channel(ctx, channel_name=f"new-channel-{helpers.getTimeInMilliseconds()}"):
#    guild = ctx.guild
#    existing_channel = discord.utils.get(guild.channels, name=channel_name)
#    if not existing_channel:
#        print(f'Creating a new channel: {channel_name}')
#        await guild.create_text_channel(channel_name)


#async def start():
#	print("Starting Discord Bot")
#	await bot.start(TOKEN)
#	print("Started Discord Bot")
#	
#async def exit():
#	await logout()
#	
#async def logout():
#	print("Logging out of Discord Bot")
#	await bot.logout()