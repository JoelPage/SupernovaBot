# Python
import os
import asyncio
import datetime
import time
import calendar
from dotenv import load_dotenv
# Discord
import discord
from discord.ext import commands as commands
# Supernova Commands
import snCommands.commands as snCommands
# Supernova Events
import snEvents.events as snEvents
import snEvents.helpers as snHelpers

yesEmoji = "✅"
noEmoji = "❌"
unsureEmoji = "❔"
defaultReactionEmojis = [ yesEmoji, noEmoji, unsureEmoji]
reactionToRSVP = { 
    yesEmoji : "Yes",
    noEmoji : "No",
    unsureEmoji : "Unsure" 
    }

# Setup
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='!')

# Run
def run():
    print("Connecting bot to discord...")
    bot.run(TOKEN)

def initialise():
    print("Initialise Bot")
    snEvents.manager.m_onEventDeletedAsync = onEventDeletedAsync
    snEvents.manager.m_signupEmojis = defaultReactionEmojis
    
# Message Posting
async def sendDebugMessageAsync(message):
    #debugChannelID = 640834927981494276
    debugChannelID = 648954586614202381
    channel = bot.get_channel(debugChannelID)
    await channel.send(message)

async def postAnnouncementMessageAsync(message):
    announcementChannelID = int(snEvents.config.m_announcementChannel)
    channel = bot.get_channel(announcementChannelID)
    await channel.send(message)

async def postSignupMessageAsync(message):
    signupChannelID = snEvents.config.m_signupChannel
    channel = bot.get_channel(signupChannelID)
    await channel.send(message)

# Callbacks
@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f"""Hi {member.name}, welcome to Supernova's discord server! 
Please set your nickname to be your in-game character name and leave us a message in #new-arrivals and we will get back to you!"""
    )

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    initialise()
    bot.loop.create_task(updateAsync())

async def onEventDeletedAsync(signupMessageID, rosterMessageID):
    print(f"onEventDeleted({signupMessageID},{rosterMessageID})")

    # Signups
    if signupMessageID != None:
        signupChannel = bot.get_channel(int(snEvents.config.m_signupChannel))
        try:
            sMessage = await signupChannel.fetch_message(signupMessageID)
            await sMessage.delete()
        except discord.errors.NotFound:
            pass

# Commands
@bot.command()
@commands.has_role('Officer')
async def emoji(ctx, *args):
    print(f"{args}")

@bot.command()
@commands.has_role('Officer')
async def create(ctx, *args):
    print(f"Recieved Discord Command create({args})")
    result = snCommands.executeCommand("CREATE", args)
    if result.error != None:
        await ctx.send(f"```{result.error}```")
    else:
        await ctx.send(f"{result.value[0]}\n```xl\n{result.value[1]}```")

    await check_events_async()
    await handle_dirty_events_async(allDirty=True)

@bot.command()
@commands.has_role('Officer')
async def skip(ctx, *args):
    print(f"Recieved Discord Command - skip({args})")
    result = snCommands.executeCommand("SKIP", args)
    if result.error != None:
        await ctx.send(result.error)
    else:
        await ctx.send(result.value)

@bot.command()
@commands.has_role('Officer')
async def events(ctx, *args):
    print(f"Recieved Discord Command - events({args})")
    result = snCommands.executeCommand("EVENTS", args)
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
    result = snCommands.executeCommand("EDIT", args)
    if result.error != None:
        await ctx.send(f"```{result.error}```")
    else:
        await ctx.send(f"{result.value[0]}\n```xl\n{result.value[1]}```")

@bot.command()
@commands.has_role('Officer')
async def config(ctx, *args):
    print(f"Recieved Discord Command - config({args})")
    result = snCommands.executeCommand("CONFIG", args)
    if result.error != None:
        await ctx.send(f"```{result.error}```")
    else:
        # Always send result.value as a single formatted string
        await ctx.send(f"{result.value}")

# Update Loop
async def updateAsync():
    interval = 30
    print("Waiting for bot to be ready...")
    nowStr = snHelpers.getNowTimeStr()
    await sendDebugMessageAsync(f"Systems Online! {nowStr}\nUpdate ticking every {interval} seconds.")
    await bot.wait_until_ready()
    while True:
        await check_events_async()
        await asyncio.sleep(interval)

async def check_events_async():
    nowStr = snHelpers.getNowTimeStr()
    print(f"Checking Events : {nowStr}")
    
    results = await snEvents.checkEventsAsync()
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
        await sendDebugMessageAsync(results[0])
    # Starting
    if results[1] != None and len(results[1]) > 1:
        for result in results[1][1:]:
            announcementStr = f"@ everyone {result} begins!"
            await postAnnouncementMessageAsync(announcementStr)
    # Reminders
    if results[2] != None and len(results[2]) > 1:
        for result in results[2][1:]:
            reminderStr = f"@ everyone {result}"
            await postAnnouncementMessageAsync(reminderStr)

    await check_reactions_async()
    await handle_dirty_events_async()

async def check_reactions_async():
    for event in snEvents.events:
        if event.signupMessageID != None:
            signupChannel = bot.get_channel(int(snEvents.config.m_signupChannel))
            try:
                sMessage = await signupChannel.fetch_message(event.signupMessageID)
                for reaction in sMessage.reactions:
                    for emoji in defaultReactionEmojis:
                        if reaction.emoji == emoji:
                            users = await reaction.users().flatten()
                            for user in users:
                                if user != bot.user:
                                    event.isDirty = True
                                    print(f"{user} reacted to {event.name} with {snEvents.config.m_reactions[reaction.emoji]}")
                                    event.signups[user.id] = snEvents.config.m_reactions[reaction.emoji]

            except discord.errors.NotFound:
                pass

async def handle_dirty_events_async(allDirty=False):
    sChannel = bot.get_channel(int(snEvents.config.m_signupChannel))

    if allDirty == True:
        await sChannel.purge(limit=None, check=lambda msg: not msg.pinned)

    eventsList = None
    if snEvents.config.m_isAscendingSort == True:
        eventsList = snEvents.events
    else:
        eventsList = reversed(snEvents.events)

    for event in eventsList:
        if event.isDirty == True or allDirty == True:    
            print(f"{event.name} is dirty!")
            splitSignups = {}
            for key, value in snEvents.config.m_reactions.items():
                splitSignups[value] = []

            for key, value in event.signups.items():
                splitSignups[value].append(key) 

            # Date Time
            day = event.start.day
            month = event.start.month
            monthStr = calendar.month_abbr[month]
            hours = event.start.hour
            minutes = event.start.minute

            sDateTime = ""
            sDateTime = f"<{monthStr} {day}, {hours:02d}:{minutes:02d}"
            if event.end != None:
                endDay = event.end.day
                endMonth = event.end.month
                endMonthStr = calendar.month_abbr[endMonth]
                endHours = event.end.hour
                endMinutes = event.end.minute
                monthStr = ""
                if event.end.day != event.start.day or event.end.month != event.start.month:
                    monthStr = f"{endMonthStr} {endDay}, "
                sDateTime = f"{sDateTime} - {monthStr}{endHours:02d}:{endMinutes:02d}>"
            else:
                sDateTime = f"{sDateTime}>"
            sDateTime = f"```xl\n{sDateTime}```"

            # Description
            sDescription = f"{sDateTime}\n{event.description}"

            sEmbed = discord.Embed(title=f"{event.name}", description=sDescription)
            if event.thumbnail:
                sEmbed.set_thumbnail(url=event.thumbnail)
            if event.image:
                sEmbed.set_image(url=event.image)            
            sEmbed.set_footer(text=f"ID:{event.id}")
            
            # Edit Roster Field
            for key, value in splitSignups.items():
                fName = f'**{key} {len(value)}\n========**'
                
                fValue = ""
                for userId in value:
                    fValue = f"{fValue}<@{userId}>\n"
                if fValue == "":
                    fValue = "Nobody"
                sEmbed.add_field(name=fName, value=fValue)

            # Edit Signup Embed
            sDescription = f"{sDateTime}{event.description}"

            # Build array of embeds - Then we can delay purge to outside the loop
            sMessage = None
            if event.signupMessageID == None or allDirty == True:
                sMessage = await sChannel.send(embed=sEmbed)
                event.signupMessageID = sMessage.id
            else:
                sMessage = await sChannel.fetch_message(event.signupMessageID)
                await sMessage.edit(embed=sEmbed)
                await sMessage.clear_reactions()

            for emoji in defaultReactionEmojis:
                await sMessage.add_reaction(emoji)

            event.isDirty = False
            snEvents.manager.publish()