import time
import xml_helpers
import threading_helpers

def CreateFunctionThread(func, args=None):
	#print("Helpers - Creating Function Thread")
	if args:
		return threading_helpers.CreateThread(func, args)
	else:
		return threading_helpers.CreateThread(func)

def CreateAndRunFunctionThread(func, args=None):
	if args:
		thread = CreateFunctionThread(func, args)
	else:
		thread = CreateFunctionThread(func)
		
	#print("Helpers - Starting Function Thread")
	thread.start()
	return thread
	
async def CreateFunctionThreadAsync(func, args=None):
	#print("Helpers - Creating Function Thread")
	if args:
		return await threading_helpers.CreateThread(func, args)
	else:
		return await threading_helpers.CreateThread(func)

async def CreateAndRunFunctionThreadAsync(func, args=None):
	if args:
		thread = await CreateFunctionThreadAsync(func, args)
	else:
		thread = await CreateFunctionThreadAsync(func)
		
	#print("Helpers - Starting Function Thread")
	await thread.start()
	return thread

getTimeInMilliseconds = lambda: int(round(time.time() * 1000))
