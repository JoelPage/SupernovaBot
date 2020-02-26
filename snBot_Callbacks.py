print("snBot_Callbacks.py")
# Discord
import discord
from discord.ext import commands as commands
# Supernova
import snBot
import snBot_Output
import snEvents.events as snEvents
# Aliases
snHelpers = snEvents.helpers

def initialise(bot):
    print("Init Discord Callbacks")

    @bot.event
    async def on_ready():
        snHelpers.debug_print(f'{bot.user.name} has connected to Discord!')
        bot.loop.create_task(snBot.start_async())

    @bot.event
    async def on_member_join(member):
        await member.create_dm()
        await member.dm_channel.send(f"Hi {member.name}, welcome to Supernova's discord server!\n{snEvents.config.m_welcomeMessage}")

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
                            await snBot_Output.post_log_message_async(reactionStr)
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

