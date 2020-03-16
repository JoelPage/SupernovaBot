print("snBot_Helpers.py")
import datetime
# Discord
import discord
from discord.ext import commands as commands
# Supernova
import snBot
import snEvents.events as snEvents

def get_signup_channel():
    channelID = snEvents.config.m_signupChannel
    return get_channel(channelID)

def get_debug_channel():
    channelID = snEvents.config.m_debugChannel
    return get_channel(channelID)

def get_announcement_channel():
    channelID = snEvents.config.m_announcementChannel
    return get_channel(channelID)

def get_log_channel():
    channelID = snEvents.config.m_logsChannel
    return get_channel(channelID)

def get_heartbeat_channel():
    channelID = snEvents.config.m_heartbeatChannel
    return get_channel(channelID)

def get_channel(id):
    channel = snBot.bot.get_channel(id)
    if channel == None:
        raise Exception(f"Channel with id {id} not found.")
    return channel

async def fetch_message_async(channel, id):
    message = await channel.fetch_message(id)
    if message == None:
        raise Exception(f"Channel with id {id} not found.")
    return message

async def is_result_valid_async(ctx, result):
    if result.error != None:
        print("Result is invalid")
        print(f"{result.error}")
        await context_send_codeblock_async(ctx, result.error)
        return False
    else:
        return True

async def context_send_codeblock_async(ctx, message):
    await ctx.send(f"```{message}```")

def is_event_locked(event):
    now = snEvents.helpers.get_now_offset()
    if now > event.start:
        return True # already started
    signupLimitDelta = datetime.timedelta(hours=snEvents.config.m_signupLimit)
    lockTime = event.start - signupLimitDelta
    if now > lockTime:
        return True # event isn't locked
    return False
    
