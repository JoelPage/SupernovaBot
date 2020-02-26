print("snBot_Commands.py")
# Discord
import discord
from discord.ext import commands as commands
# Supernova
import snCommands.commands as snCommands
import snBot
import snBot_Helpers
import snEvents.events as snEvents
# Aliases
snHelpers = snEvents.helpers

# Message Posting
async def send_debug_message_async(message):
    snHelpers.debug_print(f"send_debug_message_async({message})")
    debugChannelID = snEvents.config.m_debugChannel
    if debugChannelID == 0:
        snHelpers.debug_print("Debug channel is not set!")
        return
    try:
        channel = snBot_Helpers.get_channel(debugChannelID)
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
        channel = snBot_Helpers.get_channel(announcementChannelID)
        await channel.send(message)
    except Exception:
        pass

async def post_log_message_async(message):    
    snHelpers.debug_print(f"post_log_message_async({message})")
    logsChannelID = snEvents.config.m_logsChannel
    print(logsChannelID)
    if logsChannelID == 0:
        snHelpers.debug_print("Logs channel is not set!")
        return
    try:
        print("getting channel")
        channel = snBot_Helpers.get_channel(logsChannelID)
        nowStr = snHelpers.get_now_time_string()
        embed = discord.Embed(title=f"Signup Log {nowStr}", description=message)
        await channel.send(embed=embed)
    except Exception:
        pass
