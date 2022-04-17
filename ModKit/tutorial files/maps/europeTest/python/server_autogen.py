# Autogenerated script "server_autogen.py" for map "europeTest"
# Created on ME512 by carll at Thu Jul 26 15:07:35 2007
# !!!! DO NOT EDIT MANUALLY !!!!

import wicg
from position import *

glbWasLoading = 0

def SpawnCommonAgents():
	""" This method can be called when you from other python function want to respawn all agents in common division """
	if glbWasLoading == 0 and not wicg.IsSinglePlayer():
 	# Adding agents for multiplayer
		wicg.CreateUnit(1560086671, Position( 981.81024, 109.24805, 956.11554 ), -3.112, 0, 0, 0 )
		wicg.CreateUnit(1271007140, Position( 1101.21912, 106.52333, 525.35938 ), 0.000, 0, 0, 0 )
		pass
 
	return 1

def SpawnSinglePlayerAgents():
	""" This method can be called when you from other python function want to respawn all agents in single player division """
	if glbWasLoading == 0 and wicg.IsSinglePlayer():
 	# Adding agents for singeplayer
		pass
 
	return 1

def OnLoad( someLoadData ):
	""" Takes care of singleplayer loading. """
	import persistence
	global glbWasLoading
 
	glbWasLoading = 1
	persistence.Load( someLoadData )
 
	return 1
 

def OnSave():
	""" Takes care of singleplayer saving. """
	import persistence
	return persistence.Save()
 

def OnGameStarted():
	""" This method will be run as soon as the first player is fully loaded and connected """
	if glbWasLoading == 0 and not wicg.IsSinglePlayer():
		""" Will not be run from a persisted game """
 
		# Adding commandpoint "CommandPoint__2" and its perimeter and defensive fortification points
		wicg.CreateCommandPointEx("CommandPoint__2", 0, 1)
		wicg.CreatePerimeterPointEx("PerimeterPoint__5", "CommandPoint__2")
		wicg.CreateFortificationPointEx("PerimeterPoint__5_DefFort1", "PerimeterPoint__5", "CommandPoint__2")
		wicg.CreateFortificationPointEx("PerimeterPoint__5_DefFort2", "PerimeterPoint__5", "CommandPoint__2")
		wicg.CreateFortificationPointEx("PerimeterPoint__5_DefFort3", "PerimeterPoint__5", "CommandPoint__2")
		wicg.CreatePerimeterPointEx("PerimeterPoint__6", "CommandPoint__2")
		wicg.CreateFortificationPointEx("PerimeterPoint__6_DefFort1", "PerimeterPoint__6", "CommandPoint__2")
		wicg.CreateFortificationPointEx("PerimeterPoint__6_DefFort2", "PerimeterPoint__6", "CommandPoint__2")
		wicg.CreateFortificationPointEx("PerimeterPoint__6_DefFort3", "PerimeterPoint__6", "CommandPoint__2")
		wicg.CreatePerimeterPointEx("PerimeterPoint__7", "CommandPoint__2")
		wicg.CreateFortificationPointEx("PerimeterPoint__7_DefFort1", "PerimeterPoint__7", "CommandPoint__2")
		wicg.CreateFortificationPointEx("PerimeterPoint__7_DefFort2", "PerimeterPoint__7", "CommandPoint__2")
		wicg.CreateFortificationPointEx("PerimeterPoint__7_DefFort3", "PerimeterPoint__7", "CommandPoint__2")
 
		# Adding commandpoint "CommandPoint__0" and its perimeter and defensive fortification points
		wicg.CreateCommandPointEx("CommandPoint__0", 0, 1)
		wicg.CreatePerimeterPointEx("PerimeterPoint__0", "CommandPoint__0")
		wicg.CreateFortificationPointEx("PerimeterPoint__0_DefFort1", "PerimeterPoint__0", "CommandPoint__0")
		wicg.CreateFortificationPointEx("PerimeterPoint__0_DefFort2", "PerimeterPoint__0", "CommandPoint__0")
		wicg.CreateFortificationPointEx("PerimeterPoint__0_DefFort3", "PerimeterPoint__0", "CommandPoint__0")
		wicg.CreatePerimeterPointEx("PerimeterPoint__1", "CommandPoint__0")
		wicg.CreateFortificationPointEx("PerimeterPoint__1_DefFort1", "PerimeterPoint__1", "CommandPoint__0")
		wicg.CreateFortificationPointEx("PerimeterPoint__1_DefFort2", "PerimeterPoint__1", "CommandPoint__0")
		wicg.CreateFortificationPointEx("PerimeterPoint__1_DefFort3", "PerimeterPoint__1", "CommandPoint__0")
 
		# Adding commandpoint "CommandPoint__1" and its perimeter and defensive fortification points
		wicg.CreateCommandPointEx("CommandPoint__1", 0, 1)
		wicg.CreatePerimeterPointEx("PerimeterPoint__2", "CommandPoint__1")
		wicg.CreateFortificationPointEx("PerimeterPoint__2_DefFort1", "PerimeterPoint__2", "CommandPoint__1")
		wicg.CreateFortificationPointEx("PerimeterPoint__2_DefFort2", "PerimeterPoint__2", "CommandPoint__1")
		wicg.CreateFortificationPointEx("PerimeterPoint__2_DefFort3", "PerimeterPoint__2", "CommandPoint__1")
		wicg.CreatePerimeterPointEx("PerimeterPoint__3", "CommandPoint__1")
		wicg.CreateFortificationPointEx("PerimeterPoint__3_DefFort1", "PerimeterPoint__3", "CommandPoint__1")
		wicg.CreateFortificationPointEx("PerimeterPoint__3_DefFort2", "PerimeterPoint__3", "CommandPoint__1")
		wicg.CreateFortificationPointEx("PerimeterPoint__3_DefFort3", "PerimeterPoint__3", "CommandPoint__1")
 
		# Adding commandpoint "CommandPoint__2x" and its perimeter and defensive fortification points
		wicg.CreateCommandPointEx("CommandPoint__2x", 0, 1)
		wicg.CreatePerimeterPointEx("PerimeterPoint__6z", "CommandPoint__2x")
		wicg.CreateFortificationPointEx("PerimeterPoint__6z_DefFort1", "PerimeterPoint__6z", "CommandPoint__2x")
		wicg.CreateFortificationPointEx("PerimeterPoint__6z_DefFort2", "PerimeterPoint__6z", "CommandPoint__2x")
		wicg.CreateFortificationPointEx("PerimeterPoint__6z_DefFort3", "PerimeterPoint__6z", "CommandPoint__2x")
		wicg.CreatePerimeterPointEx("PerimeterPoint__7k", "CommandPoint__2x")
		wicg.CreateFortificationPointEx("PerimeterPoint__7k_DefFort1", "PerimeterPoint__7k", "CommandPoint__2x")
		wicg.CreateFortificationPointEx("PerimeterPoint__7k_DefFort2", "PerimeterPoint__7k", "CommandPoint__2x")
		wicg.CreateFortificationPointEx("PerimeterPoint__7k_DefFort3", "PerimeterPoint__7k", "CommandPoint__2x")
		pass
	return 1
	
