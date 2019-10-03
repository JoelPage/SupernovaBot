def gatherInput():
	#print("gatherInput()")
	return input()

def gatherInputAsync(result):
	#print("gatherInputAsync()")
	result = gatherInput()
	return result