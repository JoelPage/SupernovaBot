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
        await snBot.refresh()
        await ctx.send("Refresh Complete")

    @bot.command()
    @commands.has_role('Officer')
    async def create(ctx, *args):
        result = snCommands.executeCommand("CREATE", args)
        if await snBot_Helpers.is_result_valid(ctx, result):
            await ctx.send(f"{result.value[0]}\n```xl\n{result.value[1]}```")
            await snBot.refresh()

    @bot.command()
    @commands.has_role('Officer')
    async def skip(ctx, *args):
        result = snCommands.executeCommand("SKIP", args)
        if await snBot_Helpers.is_result_valid(ctx, result):
            await ctx.send(result.value)
            await snBot.refresh()

    @bot.command()
    @commands.has_role('Officer')
    async def edit(ctx, *args):
        result = snCommands.executeCommand("EDIT", args)
        if await snBot_Helpers.is_result_valid(ctx, result):
            await ctx.send(f"{result.value[0]}\n```xl\n{result.value[1]}```")
            await snBot.refresh()

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
            print("isValid == True")
            embed = discord.Embed(title="Configuration")
            for fieldData in result.value:
                embed.add_field(name=fieldData[0], value=fieldData[1], inline=False)
            print("Sending Embed")
            await ctx.send(embed=embed)