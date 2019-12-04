# Returns a unique identifier
# TODO : Create a more reliable unique identifier
import time

def get():
	return format(int(time.time()), 'X')