# Discord
import discord
from discord.ext import commands as commands
# Supernova Commands
import snCommands.commands as snCommands
# Supernova Events
import snEvents.events as snEvents
import snEvents.helpers as snHelpers

# Setup
bot = commands.Bot(command_prefix='!')

# Run
def run_offline():
    snHelpers.debug_print("Bot running in offline mode!")
    # TODO : Create async task 
    #while True:
        #snHelpers.debug_print("Offline bot async loop.")
        #snHelpers.sleep_async(30)

def run_online():
    snHelpers.debug_print("Connecting bot to discord...")
    token = snHelpers.get_discord_bot_token()
    bot.run(token)
    
# Callbacks
@bot.event
async def on_ready():
    snHelpers.debug_print(f'{bot.user.name} has connected to Discord!')
    bot.loop.create_task(update_async())

# Message Posting
async def send_debug_message_async(message):
    snHelpers.debug_print(f"send_debug_message_async({message})")
    # TODO : Should get channel from config
    #debugChannelID = 640834927981494276 # Test
    debugChannelID = 648954586614202381 # Local
    channel = bot.get_channel(debugChannelID)
    await channel.send(message)

async def post_announcement_message_async(message):
    announcementChannelID = int(snEvents.config.m_announcementChannel)
    channel = bot.get_channel(announcementChannelID)
    await channel.send(message)

async def postSignupMessageAsync(message):
    signupChannelID = int(snEvents.config.m_signupChannel)
    channel = bot.get_channel(signupChannelID)
    await channel.send(message)

async def post_log_message_async(message):
    logsChannelID = int(snEvents.config.m_logsChannel)
    channel = bot.get_channel(logsChannelID)
    await channel.send(message)

# Callbacks
@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f"""Hi {member.name}, welcome to Supernova's discord server! 
Please set your nickname to be your in-game character name and leave us a message in #new-arrivals and we will get back to you!"""
    )

async def on_event_deleted_async(signupMessageID):
    snHelpers.debug_print(f"on_event_deleted_async({signupMessageID})")

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

    await check_events_async()

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

    await handle_dirty_events_async()

@bot.command()
@commands.has_role('Officer')
async def config(ctx, *args):
    snHelpers.debug_print(f"Recieved Discord Command - config({args})")
    result = snCommands.executeCommand("CONFIG", args)
    if result.error != None:
        await ctx.send(f"```{result.error}```")
    else:
        await ctx.send(f"{result.value}")

# Update Loop
async def update_async():
    snHelpers.debug_print("update_async()")
    snHelpers.debug_print("Waiting for bot to be ready...")
    nowStr = snHelpers.get_now_time_string()
    # TODO : This could be in the config also
    interval = 30
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
            announcementStr = f"@ everyone {result} begins!"
            await post_announcement_message_async(announcementStr)
    # Reminders
    if results[2] != None and len(results[2]) > 1:
        for result in results[2][1:]:
            reminderStr = f"@ everyone {result}"
            await post_announcement_message_async(reminderStr)

    await check_reactions_async()
    await handle_dirty_events_async()

async def check_reactions_async():
    snHelpers.debug_print("check_reactions_async()")
    reactionsLogBuffer = ""
    for event in snEvents.events:
        if event.signupMessageID != None:
            signupChannel = bot.get_channel(int(snEvents.config.m_signupChannel))
            try:
                sMessage = await signupChannel.fetch_message(event.signupMessageID)
                for reaction in sMessage.reactions:
                    for emoji in snEvents.manager.m_config.m_reactions.keys():
                        if reaction.emoji == emoji:
                            users = await reaction.users().flatten()
                            for user in users:
                                if user != bot.user:
                                    event.isDirty = True
                                    reactionStr = f"@{user} reacted to {event.name} with {snEvents.config.m_reactions[reaction.emoji]}"
                                    snHelpers.debug_print(reactionStr)
                                    reactionsLogBuffer = f"{reactionsLogBuffer}{reactionStr}\n"
                                    event.signups[user.id] = snEvents.config.m_reactions[reaction.emoji]

            except discord.errors.NotFound:
                pass

    if reactionsLogBuffer != "":
        await post_log_message_async(reactionsLogBuffer)

async def handle_dirty_events_async(allDirty=False):
    snHelpers.debug_print(f"handle_dirty_events_async({allDirty})")
    sChannel = bot.get_channel(int(snEvents.config.m_signupChannel))

    # allDirty override, flush out all events and recreate them
    if allDirty == True:
        await sChannel.purge(limit=None, check=lambda msg: not msg.pinned)

    eventsList = None
    if snEvents.config.m_isAscendingSort == True:
        eventsList = reversed(snEvents.events)
    else:
        eventsList = snEvents.events

    eventWasDirty = False
    for event in eventsList:
        if event.isDirty == True or allDirty == True:    
            eventWasDirty = True
            print(f"{event.name} is dirty!")
            splitSignups = {}
            for key, value in snEvents.config.m_reactions.items():
                splitSignups[value] = []

            for key, value in event.signups.items():
                splitSignups[value].append(key) 

            # Date Time
            day = event.start.day
            month = event.start.month
            monthStr = snHelpers.get_month_as_string_abbr(month)
            hours = event.start.hour
            minutes = event.start.minute

            sDateTime = ""
            sDateTime = f"<{monthStr} {day}, {hours:02d}:{minutes:02d}"
            if event.end != None:
                endDay = event.end.day
                endMonth = event.end.month
                endMonthStr = snHelpers.get_month_as_string_abbr(endMonth)
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

            for emoji in snEvents.manager.m_config.m_reactions.keys():
                await sMessage.add_reaction(emoji)

            event.isDirty = False

    if allDirty == True or eventWasDirty == True: 
        snEvents.manager.publish()