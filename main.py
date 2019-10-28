import shlex as i_shlex
import event_globals as i_event_globals # Should use generic globals for exit

import commands as i_commands # CommandManager.executeCommand
import event_commands as i_event_commands # Init event commands

def main():
	#print("main()")
	while i_event_globals.exit == False:
	    print("Waiting for command...")
	    args = i_shlex.split(input())
	    commandName = args[0]
	    i_commands.CommandManager.executeCommand(commandName, args[1:])

main()

# python libraries
#import sys
#import queue
#import asyncio

# local libraries
#import helpers
#import events
#import bot
#import input

#import threading

#def onStart():
#	print("onStart")
#
#def onUpdate():
#	print("onUpdate")
#
#def initBotThread():
#	print("initBotThread()")
#	bot.run()
#
#async def runBotAsync(runLoop):
#	print("Creating Run Bot Async Task")
#	runBotTask = runLoop.create_task(bot.run())
#	print("Waiting for Run Bot Async Task")
#	await asyncio.wait([runBotTask])
#
#def exitBot():
#	exitLoop = asyncio.new_event_loop()	
#	asyncio.set_event_loop(exitLoop)
#	try:
#		exitLoop.run_until_complete(exitBotAsync(exitLoop))
#	except Exception as e:
#		print(e)
#		pass
#	finally:
#		exitLoop.close()
#	
#async def exitBotAsync(exitLoop):
#	print("Creating Exit Bot Async Task")
#	exitBotTask = exitLoop.create_task(bot.exit())
#	print("Waiting for Bot Exit Async Task")
#	await asyncio.wait([exitBotTask])
