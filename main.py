# Supernova Bot
import snBot

def main():
	# offline mode could be an executable parameter instead of hard coded
	offlineMode = False
	if offlineMode == True:
		# Offline mode does not work yet.
		print("Offline Mode")
		snBot.run_offline()
	else:
		print("Online Mode")
		snBot.run_online()

main()