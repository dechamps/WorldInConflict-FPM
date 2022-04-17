from serverimports import *
import mapvars

def OnGameStarted():
	if IsSinglePlayer():
		theGame.FadeIn( 1.0 )
	return 1