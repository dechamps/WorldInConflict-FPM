"""
    This is the common interface the server and client scripts both have access to. It contains methods 
    for access to things like current game time and the ability to write debugmessages into the WIC debugfile.
"""


def GetCurrentTime():
	""" Returns current time (in seconds) since WIC was started."""
	return 0.0


def GetElapsedTime():
	""" Returns the time (in seconds) of the last frame."""
	return 0.0


def DebugMessage( str ):
	""" Writes a debugmessage to the WIC debugfile."""
	return 1


def StringToInt( str ):
	""" Converts a string to the corresponding Ice hash value."""
	return 1


def write( str ):
	""" Writes a debugmessage to the WIC debugfile. Used to redirect stderr to the debugfile."""
	return 1


def GetHeadingXZ( aFromPos, aToPos ):
	""" Returns the heading between two positions (defined as from, to ) """
	return 1


def GetY():
	pass


def Random():
	pass


def GetRealCurrentTime():
	"""Returns MI_Time::ourRealCurrentTime (time elapsed since application start)."""
	pass
	
	
def GetRealElapsedTime():
	"""Returns MI_Time::ourRealElapsedTime (time elapsed last frame)."""
	pass

	
def StartProfiling():
	"""Starts a profiling instance."""
	pass
	
	
def StopProfiling():
	"""Ends a profiling instance"""
	pass


def DumpToFile():
	pass