print("snBot.py")
# Python
import threading
# Discord
import discord
from discord.ext import commands as commands
# Input
import input
# Supernova Commands
import snCommands.commands as snCommands
# Supernova Events
import snEvents.events as snEvents
# Aliases
snHelpers = snEvents.helpers

import snBot_Callbacks
import snBot_Commands
import snBot_Output
import snBot_Helpers

# Setup
bot = commands.Bot(command_prefix='!')
snBot_Callbacks.initialise(bot)
snBot_Commands.initialise(bot)

isAlive = False

# Offline Mode - Debugging Only
def run_offline():
    command = input.gatherInput()
    splitCommand = command.split(' ')
    result = snCommands.executeCommand(splitCommand[0], splitCommand[1:])
    for v1 in result.value:
        for v2 in v1:
            print(v2)

def run_online():
    snHelpers.debug_print("Retrieving token!")
    token = snHelpers.get_discord_bot_token()
    snHelpers.debug_print("Connecting bot to discord...")
    bot.run(token)
    snHelpers.debug_print("Finished running bot!")

# Start - This function is called when the bot is ready
async def start_async():
    # WARNING : HARD CODE INTERVAL OF 5 SECONDS
    interval = 5
    heartbeat = 900
    nowStr = snHelpers.get_now_time_string()
    await snBot_Output.send_debug_message_async(f"Systems Online! {nowStr}\nUpdate ticking every {interval} seconds.\nHeart beating every {heartbeat} seconds.")
    await bot.wait_until_ready()
    # Re-initialise from an offline state
    # - Read and reactions that may have occured while offline
    await check_reactions_async()
    # - Refresh Embeds so they are present in the message cache
    await refresh_embeds_async()
    # - Setup Heartbeat Loop
    start_heartbeat(heartbeat)
    while True:
        await update_async()
        await snHelpers.sleep_async(interval)

def start_heartbeat(heartbeat):
    threading.Timer(heartbeat, start_heartbeat, [heartbeat]).start()
    global isAlive 
    isAlive = True

# Update
async def update_async():
    await check_heartbeat_async()
    await check_events_async()

async def check_heartbeat_async():
    global isAlive
    if isAlive == True:
        await snBot_Output.post_heartbeat_async()
        isAlive = False

async def check_events_async():
    # Check for events that have ended
    results = snEvents.check_events()
    # Remove embeds for events that have finished
    for removedEvent in snEvents.manager.m_removedEvents:
        await on_event_deleted_async(removedEvent.signupMessageID)
    snEvents.manager.m_removedEvents.clear()
    # Ending
    if results[0] != None and len(results[0]) > 1:
        embed = discord.Embed(title=results[0][0], description=results[0][1:])
        await snBot_Output.send_debug_embed_async(embed)
    # Starting
    if results[1] != None and len(results[1]) > 1:
        for result in results[1][1:]:
            announcementStr = f"@everyone {result} begins!"
            await snBot_Output.post_announcement_message_async(announcementStr)
    # Reminders
    if results[2] != None and len(results[2]) > 1:
        for result in results[2][1:]:
            reminderStr = f"@everyone {result}"
            await snBot_Output.post_announcement_message_async(reminderStr)

# TODO : Clean up this function, it's ugly AF
async def check_reactions_async():
    reactionsLogBuffer = ""
    try:        
        # For Each Message
        for event in snEvents.get_events():
            if snBot_Helpers.is_event_locked(event):
                continue
            if event.signupMessageID != None:
                sChannel = snBot_Helpers.get_channel(snEvents.config.m_signupChannel)
                sMessage = await snBot_Helpers.fetch_message_async(sChannel, event.signupMessageID)
                # If the reaction is a recognised RVSP option
                for reaction in sMessage.reactions:
                    for emoji in snEvents.manager.m_config.m_reactions.keys():
                        if reaction.emoji == emoji:
                            users = await reaction.users().flatten()
                            # RVSP the users that have selected that option
                            for user in users:
                                if user != bot.user:
                                    if event.signups != None:
                                        userSignup = None
                                        try:
                                            userSignup = event.signups[user.id]
                                        except KeyError:
                                            pass
                                        reactionEmoji = snEvents.config.m_reactions[reaction.emoji]
                                        if userSignup != reactionEmoji:
                                            reactionStr = f"<@{user.id}> reacted to {event.name} with {reaction.emoji}"
                                            reactionsLogBuffer = f"{reactionsLogBuffer}{reactionStr}\n"
                                            event.signups[user.id] = snEvents.config.m_reactions[reaction.emoji]
    except Exception as e:
        await snBot_Output.send_debug_message_async(f"check_reactions_async() - {e}")
    if reactionsLogBuffer != "":
        await snBot_Output.post_log_message_async(reactionsLogBuffer)

async def refresh_embeds_async():
    try:
        sChannel = snBot_Helpers.get_channel(snEvents.get_signup_channel_id())
        await sChannel.purge(limit=None, check=lambda msg: not msg.pinned)
        splitSignups = {}
        for value in snEvents.config.m_reactions.values():
            splitSignups[value] = []

        eventEmbeds = {}
        eventsList = snEvents.get_events()
        for event in eventsList:
            # TODO : This code is duplicated, it could be a single function on an event to construct an Embed
            description = event.get_embed_description()
            embed = discord.Embed(title=f"{event.name}", description=description)
            if event.thumbnail != None:
                embed.set_thumbnail(url=event.thumbnail)
            if event.image != None:
                embed.set_image(url=event.image)
            embed.set_footer(text=f"ID:{event.id}")

            for value in splitSignups.values():
                value.clear()

            # Events store Emoji for each user.
            # We need Users for each emoji to display counts
            # User, Emoji
            for key, value in event.signups.items():
                splitSignups[value].append(key)

            # Add a field for each emoji
            # Emoji, Users
            for key, value in splitSignups.items():
                emoji = snEvents.config.findReaction(key)
                fName = f'**{emoji} {key} {len(value)}**'

                fValue = ""
                for userId in value:
                    fValue = f"{fValue}<@{userId}>\n"
                if fValue == "":
                    fValue = "Nobody"
                embed.add_field(name=fName, value=fValue, inline=True)
                eventEmbeds[event] = embed

        messages = []
        for key, value in eventEmbeds.items():
            message = await sChannel.send(embed=value)
            key.signupMessageID = message.id
            if snBot_Helpers.is_event_locked(key):
                continue
            messages.append(message)
        for message in messages:
            for emoji in snEvents.config.m_reactions.keys():
                await message.add_reaction(emoji)

        snEvents.manager.publish()

    except Exception:
        await snBot_Output.send_debug_message_async(f"Discord error not found. Check channel ids in config.")

# Callbacks
async def on_event_deleted_async(signupMessageID):
    snHelpers.debug_print(f"on_event_deleted_async({signupMessageID})")

    if signupMessageID != None:
        try:
            signupChannel = snBot_Helpers.get_channel(snEvents.config.m_signupChannel)
            message = await signupChannel.fetch_message(signupMessageID)
            await message.delete()
        except Exception:
            pass

async def refresh_async():
    await check_events_async()
    await check_reactions_async()
    await refresh_embeds_async()
    publish()

def publish():
    snEvents.manager.publish()