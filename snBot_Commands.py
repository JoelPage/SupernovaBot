print("snBot_Commands.py")
# Discord
import discord
from discord.ext import commands as commands
# Supernova
import snCommands.commands as snCommands
import snBot
import snBot_Output
import snEvents.events as snEvents
# Aliases
snHelpers = snEvents.helpers

def initialise(bot):
    print("Initialise Discord Bot Commands")

    @bot.command()
    @commands.has_role('Officer')
    async def publish(ctx, *args):
        print(f"Recieved Discord Command publish({args})")
        snEvents.manager.publish()
        await snBot_Output.send_debug_message_async("Publish complete")

    @bot.command()
    @commands.has_role('Officer')
    async def create(ctx, *args):
        print(f"Recieved Discord Command create({args})")
        result = snCommands.executeCommand("CREATE", args)
        if result.error != None:
            await ctx.send(f"```{result.error}```")
        else:
            await ctx.send(f"{result.value[0]}\n```xl\n{result.value[1]}```")

        await snBot.check_events_async()
        await snBot.handle_dirty_events_async(force=True)
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

        await snBot.check_events_async()
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

        await snBot.handle_dirty_events_async()
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