print("snBot_Commands.py")
# Discord
import discord
from discord.ext import commands as commands
# Supernova
import snCommands.commands as snCommands
import snBot
import snBot_Output
import snBot_Helpers
import snEvents.events as snEvents
# Aliases
snHelpers = snEvents.helpers

def initialise(bot):

    @bot.command()
    @commands.has_role('Officer')
    async def version(ctx, *args):
        await ctx.send("Supernova Bot v0.1.2")

    @bot.command()
    @commands.has_role('Officer')
    async def refresh(ctx, *args):
        await snBot.refresh_async()
        await ctx.send("Refresh Complete")

    @bot.command()
    @commands.has_role('Officer')
    async def create(ctx, *args):
        result = snCommands.executeCommand("CREATE", args)
        if await snBot_Helpers.is_result_valid(ctx, result):
            await ctx.send(f"{result.value[0]}\n```xl\n{result.value[1]}```")
            await snBot.refresh_async()

    @bot.command()
    @commands.has_role('Officer')
    async def skip(ctx, *args):
        result = snCommands.executeCommand("SKIP", args)
        if await snBot_Helpers.is_result_valid(ctx, result):
            await ctx.send(result.value)
            await snBot.refresh_async()

    @bot.command()
    @commands.has_role('Officer')
    async def edit(ctx, *args):
        result = snCommands.executeCommand("EDIT", args)
        print("Result recieved")
        if await snBot_Helpers.is_result_valid(ctx, result):
            # This command has a subcommand for editing the signups for an event.
            # WARNING : This is a hack to make add/remove work without refactoring
            # commands to be async or changing how commands and results work in general!
            if result.value.subname == "signup":
                # Validate Event
                event = snEvents.manager.find_event_by_id(result.value.UID)
                if event == None:
                    await snBot_Helpers.context_send_codeblock(ctx, f"Event with ID {result.value.UID} not found!")
                    return
                # Validate user
                userID = result.value.user
                user = snBot.bot.get_user(userID)
                if user == None:
                    await snBot_Helpers.context_send_codeblock(ctx, f"User with ID {userID} not found!")
                    return
                reaction = result.value.reaction
                # Add or Remove
                if result.value.addremove == "add":
                    # If a reaction wasn't provided, assume Yes
                    if reaction == None:
                        reaction = "Yes"
                    # Validate Reaction
                    if reaction not in snEvents.config.m_reactions.values():
                        await snBot_Helpers.context_send_codeblock(ctx, f"Reaction of type {reaction} not found!")
                        return
                    
                    event.signups[userID] = reaction            
                    print(f"Reaction {reaction} set for User <@!{userID}>")
                    await snBot.refresh_async()
                else:
                    # If a reaction wasn't provided, remove the users existing reaction
                    if reaction == None:
                        event.signups.pop(userID)
                        print(f"Reaction removed for User <@!{userID}>")
                        await snBot.refresh_async()
                    else:
                        if reaction == event.signups[userID]:
                            event.signups.pop(userID)                
                            print(f"Reaction {reaction} removed for User <@!{userID}>")
                            await snBot.refresh_async()
            else:
                await ctx.send(f"{result.value[0]}\n```xl\n{result.value[1]}```")
                await snBot.refresh_async()

    @bot.command()
    @commands.has_role('Officer')
    async def events(ctx, *args):
        result = snCommands.executeCommand("EVENTS", args)
        if await snBot_Helpers.is_result_valid(ctx, result):
            embed = discord.Embed(title="Upcoming Events", description=result.value[1])
            embed.set_footer(text=result.value[0])
            await ctx.send(embed=embed)

    @bot.command()
    @commands.has_role('Officer')
    async def config(ctx, *args):
        result = snCommands.executeCommand("CONFIG", args)
        if await snBot_Helpers.is_result_valid(ctx, result):
            embed = discord.Embed(title="Configuration")
            for fieldData in result.value:
                embed.add_field(name=fieldData[0], value=fieldData[1], inline=False)
            await ctx.send(embed=embed)