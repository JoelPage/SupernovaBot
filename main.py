# python libraries
import sys
import queue
import asyncio

# local libraries
import helpers
import events
import bot
import input

import threading

def main():
	print("main()")
	#initBotThread()
			
def onStart():
	print("onStart")

def onUpdate():
	print("onUpdate")

def initBotThread():
	print("initBotThread()")
	bot.run()

async def runBotAsync(runLoop):
	print("Creating Run Bot Async Task")
	runBotTask = runLoop.create_task(bot.run())
	print("Waiting for Run Bot Async Task")
	await asyncio.wait([runBotTask])

def exitBot():
	exitLoop = asyncio.new_event_loop()	
	asyncio.set_event_loop(exitLoop)
	try:
		exitLoop.run_until_complete(exitBotAsync(exitLoop))
	except Exception as e:
		print(e)
		pass
	finally:
		exitLoop.close()
	
async def exitBotAsync(exitLoop):
	print("Creating Exit Bot Async Task")
	exitBotTask = exitLoop.create_task(bot.exit())
	print("Waiting for Bot Exit Async Task")
	await asyncio.wait([exitBotTask])

def readInput():
	while True:
		print("Waiting for input...")
		if input.gatherInput() == "exit":
			exitBot()
			sys.exit()

main()

