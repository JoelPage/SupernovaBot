print("threading_helpers.py")
import threading

def CreateThread(func, args=None):
	print("Multi-threading Helpers - Creating Thread")
	if args:
		return threading.Thread(target=func, args=args)
	else:
		return threading.Thread(target=func)
	
async def CreateThreadAsync(func, args=None):
	print("Multi-threading Helpers - Creating Thread")
	if args:
		return await threading.Thread(target=func, args=args)
	else:
		return await threading.Thread(target=func)