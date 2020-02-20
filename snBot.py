print("snBot.py")
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

# Setup
bot = commands.Bot(command_prefix='!')

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
    
# Callbacks
@bot.event
async def on_ready():
    snHelpers.debug_print(f'{bot.user.name} has connected to Discord!')
    bot.loop.create_task(update_async())

@bot.event 
async def on_reaction_add(reaction, user):
    if user != bot.user:
        for event in snEvents.events:
            if event.signupMessageID == reaction.message.id:
                # Remove User Reaction
                await reaction.remove(user)
                # Update In Memory Event Reaction
                if event.signups != None:
                    userSignup = None
                    try:
                        userSignup = event.signups[user.id]
                    except KeyError:
                        pass
                    reactionEmoji = snEvents.config.m_reactions[reaction.emoji]
                    if userSignup != reactionEmoji:
                        reactionStr = f"<@{user.id}> reacted to {event.name} with {reaction.emoji}"
                        snHelpers.debug_print(reactionStr)
                        await post_log_message_async(reactionStr)
                        event.signups[user.id] = snEvents.config.m_reactions[reaction.emoji]
                        # Serialise Data
                        snEvents.manager.publish()                        
                # Update Message Embed
                # Collect Embed Data from Event Class
                # Title and Description
                description = event.get_embed_description()
                embed = discord.Embed(title=f"{event.name}", description=description)
                # Thumbnail
                if event.thumbnail != None:
                    embed.set_thumbnail(url=event.thumbnail)
                # Image
                if event.image != None:
                    embed.set_image(url=event.image)
                # ID
                embed.set_footer(text=f"ID:{event.id}")
                # Signups
                splitSignups = {}
                for value in snEvents.config.m_reactions.values():
                    splitSignups[value] = []
                for key, value in event.signups.items():
                    splitSignups[value].append(key)
                for key, value in splitSignups.items():
                    emoji = snEvents.config.findReaction(key)
                    fName = f'**{emoji} {key} {len(value)}**'

                    fValue = ""
                    for userId in value:
                        fValue = f"{fValue}<@{userId}>\n"
                    if fValue == "":
                        fValue = "Nobody"
                    embed.add_field(name=fName, value=fValue, inline=True)                
                # Apply the new Embed
                await reaction.message.edit(embed=embed)

@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f"Hi {member.name}, welcome to Supernova's discord server!\n{snEvents.config.m_welcomeMessage}")

async def on_event_deleted_async(signupMessageID):
    snHelpers.debug_print(f"on_event_deleted_async({signupMessageID})")

    if signupMessageID != None:
        try:
            signupChannel = get_channel(snEvents.config.m_signupChannel)
            message = await signupChannel.fetch_message(signupMessageID)
            await message.delete()
        except Exception:
            pass

# Message Posting
async def send_debug_message_async(message):
    snHelpers.debug_print(f"send_debug_message_async({message})")
    debugChannelID = snEvents.config.m_debugChannel
    if debugChannelID == 0:
        snHelpers.debug_print("Debug channel is not set!")
        return
    try:
        channel = get_channel(debugChannelID)
        await channel.send(message)
    except Exception:
        pass

async def post_announcement_message_async(message):
    snHelpers.debug_print(f"post_announcement_message_async({message})")
    announcementChannelID = snEvents.config.m_announcementChannel
    if announcementChannelID == 0:
        snHelpers.debug_print("Announcements channel is not set!")
        return
    try:
        channel = get_channel(announcementChannelID)
        await channel.send(message)
    except Exception:
        pass

async def post_log_message_async(message):
    snHelpers.debug_print(f"post_log_message_async({message})")
    logsChannelID = snEvents.config.m_logsChannel
    if logsChannelID == 0:
        snHelpers.debug_print("Logs channel is not set!")
        return
    try:
        channel = get_channel(logsChannelID)
        nowStr = snHelpers.get_now_time_string()
        embed = discord.Embed(title=f"Signup Log {nowStr}", description=message)
        await channel.send(embed=embed)
    except Exception:
        pass

# Commands
@bot.command()
@commands.has_role('Officer')
async def publish(ctx, *args):
    print(f"Recieved Discord Command publish({args})")
    snEvents.manager.publish()
    await send_debug_message_async("Publish complete")

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
    await handle_dirty_events_async(force=True)
    snHelpers.debug_print("Command executed")

@bot.command()
@commands.has_role('Officer')
async def skip(ctx, *args):
    print(f"Recieved Discord Command - skip({args})")
    result = snCommands.executeCommand("SKIP", args)
    if result.error != None:
        await ctx.send(result.error)
    else:
        await ctx.send(result.value)

    await check_events_async()
    snHelpers.debug_print("Command executed")

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
    snHelpers.debug_print("Command executed")

@bot.command()
@commands.has_role('Officer')
async def edit(ctx, *args):
    print(f"Recieved Discord Command - edit({args})")
    result = snCommands.executeCommand("EDIT", args)
    if result.error != None:
        await ctx.send(f"```{result.error}```")
    else:
        await ctx.send(f"{result.value[0]}\n```xl\n{result.value[1]}```")

    await handle_dirty_events_async()
    snHelpers.debug_print("Command executed")

@bot.command()
@commands.has_role('Officer')
async def config(ctx, *args):
    snHelpers.debug_print(f"Recieved Discord Command - config({args})")
    result = snCommands.executeCommand("CONFIG", args)
    if result.error:
        await ctx.send(f"```{result.error}```")
    else:
        embed = discord.Embed(title="Configuration")
        for fieldData in result.value:
            embed.add_field(name=fieldData[0], value=fieldData[1], inline=False)
        await ctx.send(embed=embed)
    snHelpers.debug_print("Command executed")

# Update Loop
async def update_async():
    snHelpers.debug_print("update_async()")
    snHelpers.debug_print("Waiting for bot to be ready...")
    nowStr = snHelpers.get_now_time_string()
    # TODO : This could be in the config also
    interval = 5
    await send_debug_message_async(f"Systems Online! {nowStr}\nUpdate ticking every {interval} seconds.")
    await bot.wait_until_ready()
    while True:
        await check_events_async()
        await snHelpers.sleep_async(interval)

async def check_events_async():
    snHelpers.debug_print("check_events_async()")
    # Check for events that have ended
    results = snEvents.check_events()
    # Remove embeds for events that have finished
    for removedEvent in snEvents.manager.m_removedEvents:
        await on_event_deleted_async(removedEvent.signupMessageID)
    snEvents.manager.m_removedEvents.clear()
    # Ending
    if results[0] != None and len(results[0]) > 1:
        await send_debug_message_async(results[0])
    # Starting
    if results[1] != None and len(results[1]) > 1:
        for result in results[1][1:]:
            announcementStr = f"@everyone {result} begins!"
            await post_announcement_message_async(announcementStr)
    # Reminders
    if results[2] != None and len(results[2]) > 1:
        for result in results[2][1:]:
            reminderStr = f"@everyone {result}"
            await post_announcement_message_async(reminderStr)

    await check_reactions_async()
    await handle_dirty_events_async()

async def check_reactions_async():
    snHelpers.debug_print("check_reactions_async()")
    reactionsLogBuffer = ""
    try:        
        for event in snEvents.events:
            if event.signupMessageID != None:
                signupChannel = get_channel(snEvents.config.m_signupChannel)
                sMessage = await fetch_message_async(signupChannel, event.signupMessageID)
                for reaction in sMessage.reactions:
                    for emoji in snEvents.manager.m_config.m_reactions.keys():
                        if reaction.emoji == emoji:
                            users = await reaction.users().flatten()
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
                                            event.isDirty = True
                                            reactionStr = f"<@{user.id}> reacted to {event.name} with {reaction.emoji}"
                                            snHelpers.debug_print(reactionStr)
                                            reactionsLogBuffer = f"{reactionsLogBuffer}{reactionStr}\n"
                                            event.signups[user.id] = snEvents.config.m_reactions[reaction.emoji]

                                    else:
                                        snHelpers.debug_print("event signups was none")
    except Exception as e:
        await send_debug_message_async(f"check_reactions_async() - {e}")

    if reactionsLogBuffer != "":
        await post_log_message_async(reactionsLogBuffer)

async def handle_dirty_events_async(force=False):
    snHelpers.debug_print(f"handle_dirty_events_async({force})")
    try:
        channel = get_channel(snEvents.get_signup_channel_id())

        # force override, flush out all events and recreate them
        if force == True:
            await channel.purge(limit=None, check=lambda msg: not msg.pinned)

        # Create Emoji Dictionary to store users
        splitSignups = {}
        for value in snEvents.config.m_reactions.values():
            splitSignups[value] = []

        hasChanges = False
        eventsList = snEvents.get_events()
        for event in eventsList:
            if event.isDirty == True or force == True:    
                hasChanges = True

                description = event.get_embed_description()
                embed = discord.Embed(title=f"{event.name}", description=description)
                if event.thumbnail != None:
                    embed.set_thumbnail(url=event.thumbnail)
                if event.image != None:
                    embed.set_image(url=event.image)
                embed.set_footer(text=f"ID:{event.id}")

                # Clear Emoji Users Dictionary 
                for value in splitSignups.values():
                    value.clear()

                # Event stores Emoji for each user.
                # We need Users for each emoji
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

                # TODO : Build array of embeds - Then we can delay purge to outside the loop
                
                message = None
                if event.signupMessageID == None or force == True:
                    message = await channel.send(embed=embed)
                    event.signupMessageID = message.id
                else:
                    message = await fetch_message_async(channel, event.signupMessageID)
                    await message.edit(embed=embed)
                    await message.clear_reactions()

                for emoji in snEvents.config.m_reactions.keys():
                    await message.add_reaction(emoji)

                event.isDirty = False

        if force == True or hasChanges == True: 
            snEvents.manager.publish()

    except Exception:
        await send_debug_message_async(f"Discord error not found. Check channel ids in config.")

def get_channel(id):
    channel = bot.get_channel(id)
    if channel == None:
        print(f"get_channel({id}) == None")
        raise Exception(f"Channel with id {id} not found.")
    return channel

async def fetch_message_async(channel, id):
    message = await channel.fetch_message(id)
    if message == None:
        print(f"fetch_message_async({id}) == None")
        raise Exception(f"Channel with id {id} not found.")
    return message