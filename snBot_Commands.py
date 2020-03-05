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

# Permission Roles
roles = ['Officer', 'Classleader', 'Servant']

def check_valid_users(ctx):
    # Extend to loop if more than pipini.
    # TODO expose in config 
    return ctx.message.author.id == 367675059243974656

def initialise(bot):

    @bot.command()
    @commands.check(check_valid_users)
    @commands.has_any_role(*roles)
    async def version(ctx, *args):
        await ctx.send("Supernova Bot v0.1.3")

    @bot.command()
    @commands.check(check_valid_users)
    @commands.has_any_role(*roles)
    async def refresh(ctx, *args):
        await snBot.refresh_async()
        await ctx.send("Refresh Complete")

    @bot.command()
    @commands.check(check_valid_users)
    @commands.has_any_role(*roles)
    async def create(ctx, *args):
        result = snCommands.executeCommand("CREATE", args)
        if await snBot_Helpers.is_result_valid(ctx, result):
            await ctx.send(f"{result.value[0]}\n```xl\n{result.value[1]}```")
            await snBot.refresh_async()

    @bot.command()
    @commands.check(check_valid_users)
    @commands.has_any_role(*roles)
    async def skip(ctx, *args):
        result = snCommands.executeCommand("SKIP", args)
        if await snBot_Helpers.is_result_valid(ctx, result):
            await ctx.send(result.value)
            await snBot.refresh_async()

    @bot.command()
    @commands.check(check_valid_users)
    @commands.has_any_role(*roles)
    async def edit(ctx, *args):
        result = snCommands.executeCommand("EDIT", args)

        if await snBot_Helpers.is_result_valid(ctx, result):
            # This command has a subcommand for editing the signups for an event.
            # WARNING : This is a hack to make add/remove work without refactoring
            # commands to be async or changing how commands and results work in general!
                    
            isSubCommand = False
            try:
                isSubCommand = (result.value.subname == "signup")
            except Exception:
                pass

            if isSubCommand:
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
                    await snBot_Helpers.context_send_codeblock(ctx, f"Reaction {reaction} set for User <@!{userID}>")
                    await snBot.refresh_async()
                else:
                    # If a reaction wasn't provided, remove the users existing reaction
                    if reaction == None:
                        event.signups.pop(userID)
                        await snBot_Helpers.context_send_codeblock(ctx, f"Reaction removed for User <@!{userID}>")
                        await snBot.refresh_async()
                    else:
                        if reaction == event.signups[userID]:
                            event.signups.pop(userID)                
                            await snBot_Helpers.context_send_codeblock(ctx, f"Reaction {reaction} removed for User <@!{userID}>")
                            await snBot.refresh_async()
            else:
                await ctx.send(f"{result.value[0]}\n```xl\n{result.value[1]}```")
                await snBot.refresh_async()

    @bot.command()
    @commands.check(check_valid_users)
    @commands.has_any_role(*roles)
    async def events(ctx, *args):
        result = snCommands.executeCommand("EVENTS", args)
        if await snBot_Helpers.is_result_valid(ctx, result):
            embed = discord.Embed(title="Upcoming Events", description=result.value[1])
            embed.set_footer(text=result.value[0])
            await ctx.send(embed=embed)

    @bot.command()
    @commands.check(check_valid_users)
    @commands.has_any_role(*roles)
    async def config(ctx, *args):
        result = snCommands.executeCommand("CONFIG", args)
        if await snBot_Helpers.is_result_valid(ctx, result):
            embed = discord.Embed(title="Configuration")
            for fieldData in result.value:
                embed.add_field(name=fieldData[0], value=fieldData[1], inline=False)
            await ctx.send(embed=embed)