# Supernova Bot
print("main.py")
import snBot

def main():
	# offline mode could be an executable parameter instead of hard coded
	offlineMode = False
	if offlineMode == True:
		print("Offline Mode")
		progress = True
		while progress:
			snBot.run_offline()
	else:
		print("Online Mode")
		snBot.run_online()

main()