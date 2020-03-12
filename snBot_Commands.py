print("snBot_Commands.py")
# Discord
import discord
import snBot
import snBot_Helpers
import snBot_Output
# Supernova
import snCommands.commands as snCommands
import snEvents.events as snEvents
from discord.ext import commands as commands

# Aliases
snHelpers = snEvents.helpers

# Permission Roles
# TODO : Make these defininable in the config.
roles = ['Officer', 'Classleader', 'Servant']
# TODO : Make these definable in the config.
validUserIDs = [ 367675059243974656 ]

def check_valid_users(ctx):
    # TODO expose in config 
    isValidRole = False
    for validRole in roles:
        for userRole in ctx.message.author.roles:
            if userRole.name == validRole:
                isValidRole = True
    isValidUser = ctx.message.author.id in validUserIDs
    return isValidUser or isValidRole

def initialise(bot):

    @bot.command()
    @commands.check(check_valid_users)
    async def version(ctx, *args):
        await ctx.send("This command is deprecated, use !info instead.")

    @bot.command()
    @commands.check(check_valid_users)
    async def info(ctx, *args):
        title = "Info"
        desc = "Supernova Bot v0.1.4\n"
        embed = discord.Embed(title=title, description=desc)
        await ctx.send(embed=embed)

    @bot.command()
    @commands.check(check_valid_users)
    async def refresh(ctx, *args):
        await snBot.refresh_async()
        await ctx.send("Refresh Complete")

    @bot.command()
    @commands.check(check_valid_users)
    async def create(ctx, *args):
        result = snCommands.executeCommand("CREATE", args)
        if await snBot_Helpers.is_result_valid_async(ctx, result):
            await ctx.send(f"{result.value[0]}\n```xl\n{result.value[1]}```")
            await snBot.refresh_async()

    @bot.command()
    @commands.check(check_valid_users)
    async def skip(ctx, *args):
        result = snCommands.executeCommand("SKIP", args)
        if await snBot_Helpers.is_result_valid_async(ctx, result):
            await ctx.send(result.value)
            await snBot.refresh_async()

    @bot.command()
    @commands.check(check_valid_users)
    async def edit(ctx, *args):
        result = snCommands.executeCommand("EDIT", args)

        if await snBot_Helpers.is_result_valid_async(ctx, result):
            # This command has a subcommand for editing the signups for an event.
            # WARNING : This is a hack to make add/remove work without refactoring
            # commands to be async or changing how commands and results work in general!
                    
            isSubCommand = False
            try:
                isSubCommand = (result.value.subname == "signup")
            except Exception:
                pass

            if isSubCommand:
                print("SubCommand")
                # Validate Event
                event = snEvents.manager.find_event_by_id(result.value.UID)
                if event == None:
                    await snBot_Helpers.context_send_codeblock_async(ctx, f"Event with ID {result.value.UID} not found!")
                    return
                # Validate user
                userID = result.value.user
                user = snBot.bot.get_user(userID)
                if user == None:
                    await snBot_Helpers.context_send_codeblock_async(ctx, f"User with ID {userID} not found!")
                    return
                reaction = result.value.reaction
                # Add or Remove
                if result.value.addremove == "add":
                    # If a reaction wasn't provided, assume Yes
                    if reaction == None:
                        reaction = "Yes"
                    # Validate Reaction
                    if reaction not in snEvents.config.m_reactions.values():
                        await snBot_Helpers.context_send_codeblock_async(ctx, f"Reaction of type {reaction} not found!")
                        return
                    
                    event.signups[userID] = reaction            
                    await snBot_Helpers.context_send_codeblock_async(ctx, f"Reaction {reaction} set for User <@!{userID}>")
                    await snBot.refresh_async()
                else:
                    # If a reaction wasn't provided, remove the users existing reaction
                    if reaction == None:
                        event.signups.pop(userID)
                        await snBot_Helpers.context_send_codeblock_async(ctx, f"Reaction removed for User <@!{userID}>")
                        await snBot.refresh_async()
                    else:
                        if reaction == event.signups[userID]:
                            event.signups.pop(userID)                
                            await snBot_Helpers.context_send_codeblock_async(ctx, f"Reaction {reaction} removed for User <@!{userID}>")
                            await snBot.refresh_async()
            else:
                await ctx.send(f"{result.value[0]}\n```xl\n{result.value[1]}```")
                await snBot.refresh_async()
        else:
            print("Error")
            await snBot_Output.send_debug_message_async(f"{result.error}")

    @bot.command()
    @commands.check(check_valid_users)
    async def events(ctx, *args):
        result = snCommands.executeCommand("EVENTS", args)
        if await snBot_Helpers.is_result_valid_async(ctx, result):
            embed = discord.Embed(title="Upcoming Events", description=result.value[1])
            embed.set_footer(text=result.value[0])
            await ctx.send(embed=embed)

    @bot.command()
    @commands.check(check_valid_users)
    async def config(ctx, *args):
        result = snCommands.executeCommand("CONFIG", args)
        if await snBot_Helpers.is_result_valid_async(ctx, result):
            embed = discord.Embed(title="Configuration")
            for fieldData in result.value:
                embed.add_field(name=fieldData[0], value=fieldData[1], inline=False)
            await ctx.send(embed=embed)
