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

def run():
    #print("run()")
    print("Connecting bot to discord...")
    bot.run(TOKEN)

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

@bot.command()
@commands.has_role('Officer')
async def create(ctx, *args):
    print(f"Recieved command 'CREATE' with args {args}")
    result = i_commands.CommandManager.executeCommand("CREATE", args)
    print(result)
    createResultStr = f"New event created :id: {result.uid} on #<Chat Channel>\n```css\nTitle: '{result.name}'\nStart: {result.start}\nEnd: {result.end}\nRepeat: <Repeat>\nDescription: <Description>```"
    await ctx.send(createResultStr)

@bot.command()
@commands.has_role('Officer')
async def skip(ctx, *args):
    print(f"Recieved command 'SKIP' with args {args}")
    result = i_commands.CommandManager.executeCommand("SKIP", args)
    await ctx.send(result)

@bot.command()
@commands.has_role('Officer')
async def events(ctx):
    eventsStr = ""
    now = i_datetime.datetime.now()
    for event in i_events.Events:
        timeDelta = event.start - now
        timeStr = getTimeUntilStringFromTimeDelta(timeDelta)
        eventsStr = f"{eventsStr}:id:`{event.uid}` ~ **{event.name}** {timeStr}\n" 

    embed = discord.Embed(title="Upcoming Events", description=eventsStr)
    embed.set_footer(text=f"{len(i_events.Events)} event(s)")
    
    await ctx.send(embed=embed)

def getTimeUntilStringFromTimeDelta(td):
        tdDays = td.days
        tdHours = td.seconds//3600
        tdMinutes = (td.seconds//60)%60
        timeStr = "begins in "

        if tdDays > 0 : 
            timeStr = f"{timeStr}{tdDays} day(s) "

        if tdHours > 0 :
             timeStr = f"{timeStr}{tdHours} hour(s) "

        if tdMinutes > 0 :
             timeStr = f"{timeStr}{tdMinutes} minute(s) "

        return timeStr

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