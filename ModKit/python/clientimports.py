##game imports
import wicp
from wicp import *
from base import *

## common imports
import wicp_common as common

##wicmath imports
from wicmath.wicmath import *
from position import *

##reaction imports
from reaction.reaction import *
from reaction.action import *
from reaction.test import *
from reaction.globals import *

##camera and sound imports
from camera.objectivecamera import ObjectiveCameraEx
from camera.objectivecamera import Helicopter
from camera.camera import *
from cmovieplayer import *
from csound import *

##gui imports
from gui_widget_names import *


theReactions = Reactions()
theOldReactions = None

isInAlternativeMode = False
timeInAlternativeMode = 0.0


reactSweepReaction = None


class SPCameraDefault( CameraType ):
	
	def __init__( self ):
		
		CameraType.__init__( self )
		
		self.myMaxSpeed			= 55.0
		self.myMaxAcceleration		= 25.0
		self.myAngularElasticity	= 4.0
		self.myAngularDrag		= 15.0
		self.myPositionalElasticity	= 4.0
		self.myPositionalDrag		= 15.0
		self.myZoomElasticity		= 30.0
		self.myZoomDrag			= 10.0	


class MPCameraDefault( CameraType ):
	
	def __init__( self ):
		
		CameraType.__init__( self )
		
		self.myMaxSpeed			= 55.0
		self.myMaxAcceleration		= 25.0
		self.myAngularElasticity	= 4.0
		self.myAngularDrag		= 15.0
		self.myPositionalElasticity	= 4.0
		self.myPositionalDrag		= 15.0
		self.myZoomElasticity		= 30.0
		self.myZoomDrag			= 10.0

mySweepPositions =[Position(1300, 150, 200), Position(1300, 150, 1300), Position(200, 150, 1300), Position(200, 150, 200)]
myCurrentPosition = 0

def MPCameraSweep():
	global myCurrentPosition
	import random
##	LookAt( 750, 10, 750 )
	LookAt( 750 + random.randint( -150, 150 ), random.randint( 20, 40 ), 750 + random.randint( -150, 150 ) )
##	GoTo( 600 + random.randint( -320, 320 ), random.randint( 92, 132 ), 600 + random.randint( -320, 320 ) )
	GoTo( mySweepPositions[myCurrentPosition].myX, mySweepPositions[myCurrentPosition].myY, mySweepPositions[myCurrentPosition].myZ)
	myCurrentPosition += 1
	if myCurrentPosition >= len(mySweepPositions):
		myCurrentPosition = 0

def SPCameraSweep():
	global myCurrentPosition
	import random
	LookAt( 750 + random.randint( -150, 150 ), random.randint( 20, 40 ), 750 + random.randint( -150, 150 ) )
	GoTo( mySweepPositions[myCurrentPosition].myX, mySweepPositions[myCurrentPosition].myY, mySweepPositions[myCurrentPosition].myZ)
	myCurrentPosition += 1
	if myCurrentPosition >= len(mySweepPositions):
		myCurrentPosition = 0


## ----- CALLBACKS -----

def OnStartCameraSweepScript( aSweepStart ):
	global reactSweepReaction
	
	##uncomment this for multiplayer camera sweep
	if not aSweepStart:
		reactSweepReaction.myRepeating = False
		RemoveReaction( reactSweepReaction )
		reactSweepReaction = None
		ReleaseCamera()
	else:
		GrabCamera( 0 )
		SetCameraType( MPCameraDefault() )
		reactSweepReaction = Repeat( 16, Action( MPCameraSweep ) )
		GoToNow( 200, 400, 200 )
		MPCameraSweep()
	
	return 1



def StartEndCamScript( ):
	global reactSweepReaction
	
	GrabCamera( 0 )
	SetCameraType( SPCameraDefault() )
	reactSweepReaction = Repeat( 16, Action( SPCameraSweep ) )
	SPCameraSweep()
	
	return 1


def OnUpdate():
	PostEvent( 'Update', GetElapsedTime(), GetCurrentTime() )
	return 1


def OnInit():
	if wicp.IsSinglePlayer():
		PostEvent( 'Init' )
		
	return 1
	
def OnCameraAtTarget( aX, aY, aZ ):
	PostEvent( 'CameraAtTarget', aX, aY, aZ )
	return 1

def OnScriptCameraAtPosition( aX, aY, aZ ):
	PostEvent( 'ScriptCameraAtPosition', aX, aY, aZ )
	return 1
	
def OnScriptCameraDone( ):
	PostEvent( 'ScriptCameraDone' )
	return 1


## ----- REACTIONS -----

def UseAlternativeReactionSystem():
	global theReactions
	theReactions.AddLastAction( Action( SwitchToAlternativeSystem ) )


def SwitchToAlternativeSystem():
	global theReactions, theOldReactions
	global isInAlternativeMode
	global timeInAlternativeMode
	
	debug.DebugMessage( 'SwitchToAlternativeSystem(%s) - client' % isInAlternativeMode, debug.VERBOSE )
	
	if isInAlternativeMode:
		debug.DebugMessage( 'SwitchToAlternativeSystem Warning! Trying to switch to alternative mode when already in alternative mode', debug.BRIEF )
		return
	
	theOldReactions = theReactions
	theReactions = Reactions()
	
	theReactions.Activate()
	isInAlternativeMode = True
	
	theOldReactions.PostEvent( 'SystemSwitched' )
	theOldReactions.Deactivate()
	
	timeInAlternativeMode = GetCurrentTime()


def UsePrimaryReactionSystem():
	global theReactions
	theReactions.AddLastAction( Action( SwitchToPrimarySystem ) )


def SwitchToPrimarySystem():
	global theReactions, theOldReactions
	global isInAlternativeMode
	global timeInAlternativeMode
	
	debug.DebugMessage( 'SwitchToPrimarySystem(%s) - client' % isInAlternativeMode, debug.VERBOSE )
	
	if not isInAlternativeMode:
		debug.DebugMessage( 'SwitchToPrimarySystem Warning! Trying to switch to primary mode when already in primary mode', debug.BRIEF )
		return

	tempAlternative = theReactions
	theReactions = theOldReactions
	
	timeInAlternativeMode = GetCurrentTime() - timeInAlternativeMode
	theReactions.AddTimeToTimers( timeInAlternativeMode )
	
	theReactions.Activate()
	isInAlternativeMode = False
	
	tempAlternative.PostEvent( 'SystemSwitched' )
	tempAlternative = None


def PostEvent( anEventString, *someArguments ):
	global theReactions
	theReactions.PostEvent(anEventString, *someArguments)


def RegisterReaction( aReaction ):
	global theReactions
	theReactions.RegisterReaction( aReaction )
	

def RemoveReaction( aReaction ):
	global theReactions
	theReactions.RemoveReaction( aReaction )


def PurgeReactions( aRestartGroups = True ):
	global theReactions
	
	theReactions.RemoveAllReactions()
	
	if aRestartGroups:
		theReactions.RegisterReaction( Reaction( 'Update', Action( theGroups.Update ), None ) ).myRepeating = True


def RemoveAllTimers( ):
	global theReactions
	
	theReactions.RemoveAllTimers()


def At( aDelay, aFunction, *someArguments):
	global theReactions
	
	newAction = Action( aFunction, *someArguments )
	newReaction = Reaction( 'Update', newAction, TimeTest ( aDelay ) )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction


def Delay( aDelay, someActions ):
	global theReactions
	
	my_time = GetCurrentTime() + aDelay
	newTimer = TimerReaction( someActions, my_time )
	theReactions.AddTimer( newTimer )

	return newTimer


def Repeat( aDelay, someActions ):
	global theReactions

	newTimer = TimerReaction( someActions, GetCurrentTime() + aDelay, aDelay )
	theReactions.AddTimer( newTimer )
	return newTimer


def RE_OnSystemSwitched( someActions ):
	global theReactions
	
	newReaction = Reaction( 'SystemSwitched', someActions )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction


def RE_OnCustomEvent( anEventString, someActions, someTestFunctions = None):
	global theReactions

	newReaction = Reaction( anEventString, someActions, someTestFunctions )
	theReactions.RegisterReaction( newReaction )

	return newReaction


## GUI

def ShowTipText( aTipText ):
	wicp.ShowTipText( *aTipText )

def ActivateGuiHandler( aGuiComponent ):
	wicp.ActivateGuiHandler( aGuiComponent )

def ActivateObjectiveBrowser( aObjectiveHashName ):
	wicp.SetActiveObjectiveInBrowser( aObjectiveHashName )
	wicp.ActivateGuiHandler( 'ObjectiveBrowser' )

def FlashObjectivesButton():
	wicp.FlashWidget('ObjectivesButton', 'MiniMap', 3.5)

def ActivateReinforcements():
	wicp.ActivateGuiHandler( 'Reinforcements_Menu' )

def ActivateSupport():
	wicp.ActivateGuiHandler( 'TacticalAids' )
	
def HideAllDropZones(): 
	for i in range( 0, 16 ): ## loop to player16 so that all DropZones are hidden. davidh 090126.
		try:
			EnableDZModel( i, False )
		except Exception:
			pass
			
			
def ShowPlayerDropZone():
	EnableDZModel( 0, True )


## CAMERA

def ObjectiveCameraRelease( ):
	ReleaseCamera()

def SetDefaultCameraType():
	SetCameraType( DefaultCamera() )

def GameOverCam( ):
	GrabCamera( True )	

##map specific cinematics import
try:
	if IsSinglePlayer( ):
		from clientplay import *
except ImportError:
	pass
