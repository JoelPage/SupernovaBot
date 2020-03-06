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
    try:
        channel = snBot_Helpers.get_debug_channel()
        await channel.send(message)
    except Exception:
        pass

async def send_debug_embed_async(embed):
    print("Send Debug Embed")
    try:
        channel = snBot_Helpers.get_debug_channel()
        print("Sending Debug Embed")
        await channel.send(embed=embed)
    except Exception:
        print("Exception")
        pass

async def post_announcement_message_async(message):
    try:
        channel = snBot_Helpers.get_announcement_channel()
        await channel.send(message)
    except Exception:
        pass

async def post_log_message_async(message):    
    try:
        nowStr = snHelpers.get_now_time_string()
        channel = snBot_Helpers.get_log_channel()
        embed = discord.Embed(title=f"Signup Log {nowStr}", description=message)
        await channel.send(embed=embed)
    except Exception:
        pass

async def post_heartbeat_async():
    try:
        nowStr = snHelpers.get_now_time_string()
        channel = snBot_Helpers.get_heartbeat_channel()
        await channel.send(f"{nowStr}")
    except Exception:
        pass
