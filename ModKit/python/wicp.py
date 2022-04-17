""" wicp module interface. These are the functions available to client-side scripts."""


def write():
	"""Writes a string to the ingame console"""
	pass
	
	
def PrintText():
	"""Writes a string to the screen"""
	pass
	

def PrintTextBig():
	"""Writes a string to the screen (large font)"""
	pass

	
def PostScreenMessage():
	"""Writes a text to the screen in screen space"""
	pass
	
def PrintTextLocCatIntInt():
	"""Writes a localized string to the screen with two interger arguments"""
	pass

	
def PrintTextLocCatInt():
	"""Writes a localized string to the screen with one interger argument"""
	pass


def PrintTextLoc():
	"""Writes a localized string to the screen"""
	pass


def ShowMessageBox():
	"""Shows a messagebox to the player. This function is deprecated and is currently doing not working!!!"""
	pass
	
	
def ShowTipText():
	"""Shows a fullscreen tip text screen to the player"""
	pass
	
	
def ActivateGuiHandler():
	"""Activates a GUI handler"""
	pass
	
	
def FlashWidget():
	"""Flashes a GUI widget"""
	pass


def FlashOrderPaletteButton():
	""" Flashes a button in the order palette"""
	pass


def FlashReinforcementButton():
	""" Flashes the reinforcement button"""
	pass
	
def EnableAvailableTANotification( anEnableFlag ):
	pass

def ChooseDropZone():
	""" Enters the choose dropzone mode"""
	pass
	
		
def SetSoundVolumes():
	"""Sets application sound volumes"""
	pass
	
	
def ResetSoundVolumes():
	"""Resets application sound volumes"""
	pass

def ResetSoundVolumesIndividual():
	""" """
	pass


def EnableCommandPointSounds():
	pass


def DisableCommandPointSounds():
	pass


def PlayMusicEvent():
	pass


def AddArea():
	"""Adds a war filter to an area"""
	pass
	
	
def Shake():
	"""Shakes the camera"""
	pass
	
	
def EnableWarFilter():
	"""Enables/disables the war filter"""
	pass
	
	
def FadeIn():
	"""Fades in. Id must be matched with FadeOut() (0x1007, 0xabbaabba taken by system)"""
	pass
	
	
def FadeOut():
	"""Fades out"""
	pass
	
	
def StopFade():
	"""Stops fade"""
	pass
	
	
def GetSelectedUnit():
	"""Returns the id of the selected unit"""
	pass
	
	
def EnableDZModel():
	"""Enables/disables the DZ model for a player"""
	pass


def OverrideGlobalLodFudge():
	pass	


def GetCameraPosition():
	pass


def GetCameraLookAt():
	pass


def GetDistanceToGround():
	pass


def LoadCinematicCamera():
	pass

def StartCinematicCamera():
	pass


def StopCinematicCamera():
	pass


def ShowTutorialHelper():
	pass


def HideAllTutorialHelpers():
	pass


def SetMoodFrame():
	"""Sets the mood frame. If interpolation length is negative, it is not automatically updated (ie is stuck at the start value)"""
	pass
	
	
def EnableAutoMoods():
	"""Enables/disables automatic mood changes based on the world's destruction. Default is on in multiplayer, off in single player."""
	pass
	
	
def SendPlayerAction():
	"""Sends the given player action to the server"""
	pass
	
	
def SetCommandPointVisible():
	"""Sets the visibility state of an commandpoint"""
	pass
	
	
def SetActiveObjectiveInBrowser():
	"""Sets the currently selected objective in the objective browser"""
	pass


def GetInstancePosition():
	pass


def GetInstanceRadius():
	pass


def IsSinglePlayer():
	pass


def CheckMousePressed():
	pass


def CheckKeyPressed():
	pass


def CheckKeyDown():
	pass


def World2Screen():
	pass


def MouseToWorld():
	pass


def SetTutorialMessage():
	pass


def LoadOrderRestrictionMask(aFilePath):
	pass


def EnableOrderRestrictionMask():
	pass


def DisableOrderRestrictionMask():
	pass


def EnableTARestriction(aPositionA, aPositionB):
	pass


def DisableTARestriction():
	pass
