print("snBot_Helpers.py")
# Discord
import discord
from discord.ext import commands as commands
# Supernova
import snBot
import snEvents.events as snEvents

def get_channel(id):
    channel = snBot.bot.get_channel(id)
    if channel == None:
        print(f"get_channel({id}) == None")
        raise Exception(f"Channel with id {id} not found.")
    return channel

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

async def fetch_message_async(channel, id):
    message = await channel.fetch_message(id)
    if message == None:
        print(f"fetch_message_async({id}) == None")
        raise Exception(f"Channel with id {id} not found.")
    return message

