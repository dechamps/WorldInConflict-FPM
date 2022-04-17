##wicmath imports
import position
from position import *
from wicmath.wicmath import *

## common inports
import wicg_common as common
from wicg_common import *

##game imports
import wicg
import game
import unit
import base
import building
import unittypes
from wicg import *
from base import *
from game import *
from player import *
from gameobject import *
from building import *
from building import theBuildings
from unit import *
from area import *
from unittypes import *
from wicgame.globals import *
import wicgame.cinematic
from wicgame.cinematic import Cinematic
from wicgame.cinematic import LuddeCinematic
from wicgame.cinematic import SplineCinematic
from wicgame.ai import *
import wicgame.ai
import wicgame.ai as ai
import wicgame.los
from wicgame.los import LOSCircle
from wicgame.los import LOSRectangle
import wicgame.timer
from wicgame.timer import *
import wicgame.actionqueue
from wicgame.actionqueue import *
from wicgame.objective import Objective
import wicgame.feedback
from wicgame.feedback import CommandPointFeedbackRuFortif
from wicgame.feedback import CommandPointFeedbackCPLost
import wicgame.tacticalaid
from wicgame.tacticalaid import TA_Wrapper
from wicgame.tacticalaid import TA_Position
from wicgame.tacticalaid import TA_DestroyObject
from wicgame.tacticalaid import TA_DestroyBuilding
from wicgame.tacticalaid import TA_Wrapper as TAWrapper
import wicgame.disobey
from wicgame.disobey import Disobey
from wicgame.civilians import SpawnCiviliansInClump

##reaction imports
from reaction.reaction import *
from reaction.action import *
from reaction.test import *
from reaction.globals import *

##group imports
from group.group import *
from group.command import *
from group.behavior import *
from group.platoon import *
from group.globals import *


##misc imports
from debug import *
import debug
import profiler


##gamesettings
import gamesettings


theReactions	= Reactions()
theOldReactions = None

theGroups	= Groups()
theOldGroups	= None

theTime = 0.0

enabledAIs = []

dualEvents = 	['FortificationCreated', 'FortificationDestroyed', 'BuildingDestroyed', 'EventStringDone', \
		'CommandPointTaken', 'PerimeterPointTaken', 'MessageBoxClosed', 'UnitEnterBuilding', 'UnitEnterContainer' ]

isInAlternativeMode = False
timeInAlternativeMode = 0.0

theReactions.RegisterReaction( Reaction( 'Update', Action( theGroups.Update ), TimeTest( UPDATE_FREQUENCY ) ) ).myRepeating = True

theMessageboxCounter = 0
lastShownMessageBoxId = INVALID_MSG_BOX_ID

lastShownFeedBackMessageBoxId = 10002

inMegamap = False

## action queue
theExecutionQueue = []
theExpressList = []
theNameCounter = 0

## gui chunk names
theGUIChunks = {
	'minimap'	: False,
	'support'	: False,
	'reinforcements': False
}


##buy menu items
theBuyMenu = {}


## ta menu items
theTAs = {}

## ----- EXCEPTIONS -----

class BadSystemException( Exception ): pass
class BadReactionArgumentException( Exception ): pass


## ----- CALLBACKS -----

def OnFPMModeStarted():
	
	debug.DebugMessage( 'OnFPMModeStarted' )
	
	## setup few player mode
	numPlayers = wicg.GetMaxNumPlayers()
	
	if numPlayers == 2:
		wicg.SetMaxAP( gamesettings.FPM_MAX_AP_1V1, TEAM_USA )
		wicg.SetMaxAP( gamesettings.FPM_MAX_AP_1V1, TEAM_NATO )
		wicg.SetMaxAP( gamesettings.FPM_MAX_AP_1V1, TEAM_USSR )
		wicg.SetStartingAP( gamesettings.FPM_STARTING_AP_1V1, TEAM_USA )
		wicg.SetStartingAP( gamesettings.FPM_STARTING_AP_1V1, TEAM_NATO )
		wicg.SetStartingAP( gamesettings.FPM_STARTING_AP_1V1, TEAM_USSR )
		wicg.SetApRegrowthRate( gamesettings.FPM_TRICKLE_RATE_1V1 )
		wicg.SetUnitScoreToTAMultiplier( gamesettings.FPM_BATTLE_HONOR_MULTIPLIER_1V1 )
		wicg.SetDomTotalDominationFactor( gamesettings.FPM_TOTAL_DOMINATION_FACTOR_1V1 )
	
	if numPlayers == 4:
		wicg.SetMaxAP( gamesettings.FPM_MAX_AP_2V2, TEAM_USA )
		wicg.SetMaxAP( gamesettings.FPM_MAX_AP_2V2, TEAM_NATO )
		wicg.SetMaxAP( gamesettings.FPM_MAX_AP_2V2, TEAM_USSR )
		wicg.SetStartingAP( gamesettings.FPM_STARTING_AP_2V2, TEAM_USA )
		wicg.SetStartingAP( gamesettings.FPM_STARTING_AP_2V2, TEAM_NATO )
		wicg.SetStartingAP( gamesettings.FPM_STARTING_AP_2V2, TEAM_USSR )
		wicg.SetApRegrowthRate( gamesettings.FPM_TRICKLE_RATE_2V2 )
		wicg.SetUnitScoreToTAMultiplier( gamesettings.FPM_BATTLE_HONOR_MULTIPLIER_2V2 )
		wicg.SetDomTotalDominationFactor( gamesettings.FPM_TOTAL_DOMINATION_FACTOR_2V2 )
		
	return 1


def OnUpdate():
	if wicg.IsSinglePlayer() or wicg.IsMoviebox():
		global theReactions
		theReactions.ResetEventDepth()
		PostEvent( 'Update', GetElapsedTime(), GetCurrentTime() )
	return 1
 
def OnInit():
	if wicg.IsSinglePlayer():
		PostEvent( 'Init' )		
	return 1

def OnUnitDestroyed( aUnitID, aKillerID ):
	if wicg.IsSinglePlayer() or wicg.IsMoviebox():
		PostEvent( 'UnitDestroyed', aUnitID, aKillerID )
	return 1

def OnUnitUnderAttack( aUnitID, anAttackerID ):
	if wicg.IsSinglePlayer():
		PostEvent( 'UnitInCombat', aUnitID, anAttackerID )
	return 1

def OnUnitCreated( aUnitID, aSquadId, aKey ):
	if wicg.IsSinglePlayer() or wicg.IsMoviebox():
		PostEvent( 'UnitCreated', aUnitID, aSquadId, aKey )
	return 1

def OnZoneTaken( aZone, aTeam ):
	if wicg.IsSinglePlayer( ):
		PostEvent( 'CommandPointTaken', aZone, aTeam )
	return 1

def OnMessageBoxClosed( aMessageBoxID ):
	if wicg.IsSinglePlayer():
		PostEvent( 'MessageBoxClosed', aMessageBoxID )
	return 1

def OnEventStringDone( anEventStringId ):
	if wicg.IsSinglePlayer():
		PostEvent( 'EventStringDone', anEventStringId )
	return 1

def OnPerimeterPointCaptured( aPPoint, aTeam ):
	if wicg.IsSinglePlayer():
		PostEvent( 'PerimeterPointTaken', aPPoint, aTeam )
	return 1

def OnFortificationCreated( aPPoint, aTeam, aLevel ):
	if wicg.IsSinglePlayer():
		PostEvent( 'FortificationCreated', aPPoint, aTeam, aLevel )
	return 1

def OnFortificationDestroyed( aPPoint, aTeam, aLevel ):
	if wicg.IsSinglePlayer():
		PostEvent( 'FortificationDestroyed', aPPoint, aTeam, aLevel )
	return 1

def OnBuildingDestroyed( aBuilding ):
	if wicg.IsSinglePlayer():
		PostEvent( 'BuildingDestroyed', aBuilding )
	return 1

def OnBridgeDestroyed( aDestroyedBridge ):
	
	if wicg.IsSinglePlayer():
		PostEvent( 'BridgeDestroyed', aDestroyedBridge )
	return 1	

def OnUnitEnterBuilding( aUnitId, aBuilding ):
	if wicg.IsSinglePlayer():
		PostEvent( 'UnitEnterBuilding', aUnitId, aBuilding )
	return 1

def OnUnitEnterContainer( aUnitId, aContainerId ):
	if wicg.IsSinglePlayer():
		PostEvent( 'UnitEnterContainer', aUnitId, aContainerId )
	return 1


def OnUnitExitContainer( aUnitId, aContainerId ):
	if wicg.IsSinglePlayer():
		PostEvent( 'UnitExitContainer', aUnitId, aContainerId )
	return 1


def OnTASpawned( aTrackingName ):
	if wicg.IsSinglePlayer():
		PostEvent( 'TASpawned', aTrackingName )
	return 1


def OnTAProjectile( aTrackingName, aTrackingId ):
	if wicg.IsSinglePlayer():
		PostEvent( 'TAProjectile', aTrackingName, aTrackingId )
	return 1


def OnTAProjectileDestroyed( aTrackingName, aTrackingId ):
	if wicg.IsSinglePlayer():
		PostEvent( 'TAProjectileDestroyed', aTrackingName, aTrackingId )
	return 1


def OnPlayerConnected( aPlayerId, aTeam ):
	if wicg.IsSinglePlayer():
		PostEvent( 'PlayerConnected' )
		
		if aPlayerId+1 == PLAYER_HUMAN:
			## set default Player name to Parker
			thePlayers[ PLAYER_HUMAN ].myName = 'parker'
			
	return 1


def OnPlayerLeave( aPlayerId, aTeam ):
	global theReactions
	
	if wicg.IsSinglePlayer():
		PostEvent( 'PlayerLeave', aPlayerId, aTeam )
		
		## pause the reaction system when the player leaves
		## the server will keep getting updates after the player leaves,
		## so we do this to ensure that no python code is running after player leaves
		if aPlayerId == 0:
			theReactions.Pause()
		
	return 1


def OnGameStarted():
	if wicg.IsSinglePlayer():
		PostEvent( 'GameStarted' )
	return 1

def OnPlayerAction( aPlayerID, anActionString ):
	if wicg.IsSinglePlayer( ):
		## post player action on client, so we can quit objective cameras on ESC
		## this must be called before PostEvent (otherwise objectivecameras and ESC can be messed up)
		ClientCommand( 'PostEvent', anActionString )

		PostEvent( anActionString )		
	return 1


def OnTAExecuted( aPlayerId, aTAId ):   
	if wicg.IsSinglePlayer( ):
		PostEvent( 'TAExecuted', aPlayerId, aTAId )
	return 1
	

def OnSpecialAbilityFired( anAbility, aUsingUnitId ):
	if wicg.IsSinglePlayer( ):
		PostEvent( "FIRED_SPECIAL_ABILITY", anAbility.Id, aUsingUnitId, anAbility.Type )
	return 1
	



## ----- TESTS -----

class SpecialAbilityFiredTest( BaseTest ):
	
	def __init__( self, anAbility, aUsingUnitId ):
		
		self.__Ability = base.StringToInt( anAbility )
		self.__UserUnitId = aUsingUnitId

	
	def Test( self, someEventData ):
		
		if self.__Ability == someEventData[ 0 ]:
			if not self.__UserUnitId:
				return True
			
		return False
		



class PlayerHoldFire( BaseTest ):
	
	def __init__( self, aPlayerId, aAllUnits = True, aHoldingFire = False ):
		
		self.__PlayerId = aPlayerId
		self.__AllUnits = aAllUnits
		self.__HoldingFire = aHoldingFire

	def Test( self, someEventData ):
		
		numOfUnits = 0
		numOfHoldFire = 0
		unit_owner = 0
		isholdingfire = False
		
		for unitId in range( MAX_NUMBER_OF_UNITS ):
			try:
				#aUnit = Unit( unitId )
				unit_owner = wicg.GetUnitMember( unitId, 'owner' )
				if unit_owner == self.__PlayerId:
					numOfUnits += 1
					isholdingfire = wicg.GetUnitMember( unitId, 'isholdingfire' )
					if isholdingfire == self.__HoldingFire:
						numOfHoldFire += 1 
					
			except unit.UnknownUnitException:
				pass  

		if self.__AllUnits:
			if numOfUnits == numOfHoldFire and numOfHoldFire != 0:
				return True
		else:
			if numOfHoldFire != 0:
				return True
		
		return False


class PlayerInForestTest( BaseTest ):
	
	def __init__( self, aPlayerId ):
		
		self.__PlayerId = aPlayerId

	def Test( self, someEventData ):
		for unitId in range( MAX_NUMBER_OF_UNITS ):
			try:
				#aUnit = Unit( unitId )
				unit_owner = wicg.GetUnitMember( unitId, 'owner' )
				if unit_owner == self.__PlayerId:
					if wicg.IsUnitInForest( unitId ):
						return True
					
			except unit.UnknownUnitException:
				pass  

		return False
class UnitInAreaTest( BaseTest ):
	
	def __init__( self, someUnitIds, someAreas ):
		
		self.__UnitIds = someUnitIds

		if isinstance( someAreas, list ):
			self.__Areas = someAreas
		else:
			self.__Areas = [someAreas]


	def Test( self, someEventData ):
		
		for a in self.__Areas:
			if a.HaveUnits( self.__UnitIds ) != None:
				return True
		return False


class UnitNotInAreaTest( BaseTest ):
	
	def __init__( self, someUnitIds, someAreas ):
		
		self.__UnitIds = someUnitIds

		if isinstance( someAreas, list ):
			self.__Areas = someAreas
		else:
			self.__Areas = [someAreas]


	def Test( self, someEventData ):
		
		for a in self.__Areas:
			if a.HaveUnits( self.__UnitIds ) != None:
				return False
		return True


class PlayerInAreaTest( BaseTest ):
	
	def __init__( self, aPlayer, someAreas ):
		
		self.__Player = aPlayer
		
		if isinstance( someAreas, list ):
			self.__Areas = someAreas
		else:
			self.__Areas = [someAreas]


	def Test( self, someEventData ):
		
		for a in self.__Areas:
			if a.HavePlayerUnit( self.__Player ):
				return True
		return False


class PlayerInAreaTestNotChoppers( BaseTest ):
	
	def __init__( self, aPlayer, someAreas ):
		
		self.__Player = aPlayer
		
		if isinstance( someAreas, list ):
			self.__Areas = someAreas
		else:
			self.__Areas = [someAreas]


	def Test( self, someEventData ):
		
		for a in self.__Areas:
			if a.HavePlayerUnitNotChopper( self.__Player ):
				return True
		return False


class RadarScanInAreaTest( BaseTest ):
	
	def __init__( self, aPlayer, someAreas ):
		
		self.__Player = aPlayer
		
		if isinstance( someAreas, list ):
			self.__Areas = someAreas
		else:
			self.__Areas = [someAreas]


	def Test( self, someEventData ):
		
		for a in self.__Areas:
			if a.HaveRadarScanUnit( self.__Player ):
				return True
		return False


class TeamInAreaTest( BaseTest ):
	
	def __init__( self, aTeam, someAreas ):
		
		self.__Team = aTeam

		if isinstance( someAreas, list ):
			self.__Areas = someAreas
		else:
			self.__Areas = [someAreas]


	def Test( self, someEventData ):
		
		for a in self.__Areas:
			if a.HaveTeamUnit( self.__Team ):
				return True
		return False


class GroupInAreaTest( BaseTest ):
	
	def __init__( self, aGroup, someAreas, aAllIn = False ):
		
		self.__Group = aGroup
		self.__AllIn = aAllIn

		if isinstance( someAreas, list ):
			self.__Areas = someAreas
		else:
			self.__Areas = [someAreas]


	def Test( self, someEventData ):
		
		for a in self.__Areas:
			if self.__AllIn:
				if not a.HaveGroup( self.__Group ):
					return False
			else:
				if a.HaveGroupUnit( self.__Group ):
					return True
		
		if self.__AllIn:
			return True
			
		return False


class GroupNotInAreaTest( BaseTest ):
	
	def __init__( self, aGroup, someAreas, aAllOut = False ):
		
		self.__Group = aGroup
		self.__AllOut = aAllOut

		if isinstance( someAreas, list ):
			self.__Areas = someAreas
		else:
			self.__Areas = [someAreas]


	def Test( self, someEventData ):
		
		for a in self.__Areas:
			if self.__AllOut:
				if a.HaveGroupUnit( self.__Group ):
					return False
			else:
				if not a.HaveGroup( self.__Group ):
					return True
		if self.__AllOut:
			return True
		
		return False



class PlatoonInAreaTest( BaseTest ):
	
	def __init__( self, aPlatoon, someAreas, aAllIn = False ):
		
		self.__Platoon = aPlatoon
		self.__AllIn = aAllIn

		if isinstance( someAreas, list ):
			self.__Areas = someAreas
		else:
			self.__Areas = [someAreas]


	def Test( self, someEventData ):
		
		testGroups = []
		testGroups = self.__Platoon.myGroups
		
		
		for g in self.__Platoon.myGroups:
			for u in g.myUnits:
				area_counter = 0
				for a in self.__Areas:
					if self.__AllIn:
						if a.HaveUnit( u.myUnitId ) is None:
							area_counter += 1
					else:
						if a.HaveUnit( u.myUnitId ) != None:
							return True
				
				if self.__AllIn and area_counter >= len(self.__Areas):
					return False
		
		if self.__AllIn:
			return True
			
		return False

class PlatoonNotInAreaTest( BaseTest ):
	
	def __init__( self, aPlatoon, someAreas, aAllOut = False ):
		
		self.__Platoon = aPlatoon
		self.__AllOut = aAllOut

		if isinstance( someAreas, list ):
			self.__Areas = someAreas
		else:
			self.__Areas = [someAreas]


	def Test( self, someEventData ):
		
		for g in self.__Platoon.myGroups:
			for u in g.myUnits:
				area_counter = 0
				for a in self.__Areas:
					if self.__AllOut:
						if a.HaveUnit( u.myUnitId ) is None:
							return False
					else:
						if not a.HaveUnit( u.myUnitId ) != None:
							return True
				
				if self.__AllOut and area_counter >= len(self.__Areas):
					return False
		
		if self.__AllOut:
			return True
			
		return False



class GroupHealthTest( BaseTest ):
	
	def __init__( self, aGroup, aHealth, aUseMaxHealth, aNrOfUnits ):
		
		self.__Group = aGroup
		self.__Health = aHealth
		self.__UseMaxHealth = aUseMaxHealth
		self.__NrOfUnits = aNrOfUnits


	def Test( self, someEventData ):
		
		nrUnits = 0
		limit = self.__NrOfUnits
		
		if self.__NrOfUnits == -1:
			limit = self.__Group.Size()
		
		for grpUnit in self.__Group.myUnits:
			if self.__UseMaxHealth:
				if grpUnit.myUnit.myHealth >= grpUnit.myUnit.myMaxHealth:
					nrUnits += 1
			else:
				if grpUnit.myUnit.myHealth >= self.__Health:
					nrUnits += 1
					
			if nrUnits >= limit:
				return True

		return False


class PlatoonHealthTest( BaseTest ):
	
	def __init__( self, aPlatoon, aHealth, aUseMaxHealth, aNrOfUnits ):
		
		self.__Platoon = aPlatoon
		self.__Health = aHealth
		self.__UseMaxHealth = aUseMaxHealth
		self.__NrOfUnits = aNrOfUnits


	def Test( self, someEventData ):
		
		nrUnits = 0
		limit = self.__NrOfUnits
		
		if self.__NrOfUnits == -1:
			limit = self.__Platoon.Size()
		
		for grp in self.__Platoon.myGroups:
			for grpUnit in grp.myUnits:
				if self.__UseMaxHealth:
					if grpUnit.myUnit.myHealth == grpUnit.myUnit.myMaxHealth:
						nrUnits += 1
				else:
					if grpUnit.myUnit.myHealth >= self.__Health:
						nrUnits += 1
						
				if nrUnits >= limit:
					return True

		return False


class UnitOwnerTest( BaseTest ):
	
	def __init__( self, aPlayerId, anIndex = 0 ):
		
		self.__PlayerId = aPlayerId
		self.__Index = anIndex


	def Test( self, someEventData ):
		
		if someEventData[self.__Index] == -1:
			return False
		
		if self.__PlayerId == unit.theUnits[someEventData[self.__Index]].myOwner:
			return True

		return False


class UnitTypesTest( BaseTest ):
	
	def __init__( self, someTypes, anIndex = 0 ):
		
		self.__Types = someTypes
		self.__Index = anIndex


	def Test( self, someEventData ):
		
		if someEventData[self.__Index] == -1:
			return False
		
		if unit.theUnits[someEventData[self.__Index]].myType in self.__Types:
			return True

		return False


class UnitInGroupsTest( BaseTest ):
	
	def __init__( self, someGroups, anIndex = 0 ):
		
		self.__Groups = someGroups
		self.__Index = anIndex


	def Test( self, someEventData ):
		
		for grp in self.__Groups:
			if grp and grp.IsUnitInGroup( someEventData[self.__Index] ):
				return True
		return False


class NrOfPlayerUnitsTest( BaseTest ):
	
	def __init__( self, aNrOfUnits = 0 ):
		
		self.__NrOfUnits = aNrOfUnits
	
	
	def Test( self, someEventData ):
		
		unitCounter = 0
		
		for i in range( 512 ):
			try:
				if theUnits[i].myOwner == PLAYER_HUMAN or (i != someEventData[0] and theUnits[i].myOwner == PLAYER_HUMAN):
					unitCounter += 1
			except Exception:
				continue
			
			if unitCounter > self.__NrOfUnits:
				return False
		return True
		
	

class GroupInCombatUnitOwnerTest( BaseTest ):
	
	def __init__( self, aPlayerId ):
		
		self.__PlayerId = aPlayerId


	def Test( self, someEventData ):
		
		if self.__PlayerId == unit.theUnits[someEventData[1]].myOwner or self.__PlayerId == unit.theUnits[someEventData[2]].myOwner:
			return True

		return False


class GroupInPlatoonTest( BaseTest ):
	
	def __init__( self, aPlatoon ):
		
		self.__Platoon = aPlatoon


	def Test( self, someEventData ):
				
		if someEventData[0] in self.__Platoon.myGroups:
			return True

		return False


class APLimitTest( BaseTest ):
	
	def __init__( self, anAPLimit = 0 ):
		
		self.__APLimit = anAPLimit


	def Test( self, someEventData ):
		
		if thePlayers[PLAYER_HUMAN].myCurrentAP <= self.__APLimit:
			return True

		return False


class NotInMegamapTest( BaseTest ):
	
	def __init__( self ):
		pass		
	
	def Test( self, someEventData ):
		global inMegamap

		return (not inMegamap)


class CameraInAreaTest( BaseTest ):
	
	def __init__( self, anArea ):
		
		self.__Area = anArea
		
	
	def Test( self, someEventData ):

		currentCameraPosition = wicg.GetCameraPosition( PLAYER_HUMAN )
		
		if wicmath.Distance( self.__Area.myPos, currentCameraPosition ) < self.__Area.myRadius:
			return True

		return False


class CameraMoveForwardTest( BaseTest ):
	
	def __init__( self ):
		
		self.__LastCameraPosition = None
		self.__LastCameraLookAt = None
		self.__AccumulatedLength = 0.0
		self.Update()
	
	
	def Update( self ):
		
		self.__LastCameraPosition = wicg.GetCameraPosition( PLAYER_HUMAN )
		self.__LastCameraPosition.myY = 0.0

		## camera direction
		self.__LastCameraLookAt = wicmath.Angles2Direction( wicg.GetCameraRotation( PLAYER_HUMAN ) )
		self.__LastCameraLookAt.myY = 0.0
		self.__LastCameraLookAt.Normalize()
		
	
	def Test( self, someEventData ):

		## current position
		currentCameraPosition = wicg.GetCameraPosition( PLAYER_HUMAN )
		currentCameraPosition.myY = 0.0
		
		## move direction
		moveDirection = currentCameraPosition - self.__LastCameraPosition
		moveDirection.myY = 0.0
		moveLength = moveDirection.Length()
		moveDirection.Normalize()

		
		## angle between camDirection and moveDirection
		d = PosDot( moveDirection, self.__LastCameraLookAt )
		
		## use this for debugging
		#debug.DebugMessage( 'CameraMoveForwardTest d=%f moveDirection=%s moveLength=%f accumulatedLength=%f' % (d, moveDirection, moveLength, self.__AccumulatedLength) )

		## angle threshold (we must be moving forward)
		if d > 0.98:
			
			self.__AccumulatedLength += moveLength
		
			## length threshold (we must have moved a certain length)
			if self.__AccumulatedLength > 4.0:
				self.Update()
				return True
			else:
				self.Update()
				return False
				
		self.__AccumulatedLength = 0.0
		self.Update()
		return False


class CameraMoveBackwardTest( BaseTest ):
	
	def __init__( self ):
		
		self.__LastCameraPosition = None
		self.__LastCameraLookAt = None
		self.__AccumulatedLength = 0.0
		self.Update()
	
	
	def Update( self ):
		
		self.__LastCameraPosition = wicg.GetCameraPosition( PLAYER_HUMAN )
		self.__LastCameraPosition.myY = 0.0

		## camera direction
		self.__LastCameraLookAt = wicmath.Angles2Direction( wicg.GetCameraRotation( PLAYER_HUMAN ) )
		self.__LastCameraLookAt.myY = 0.0
		self.__LastCameraLookAt.Normalize()
		
	
	def Test( self, someEventData ):

		## current position
		currentCameraPosition = wicg.GetCameraPosition( PLAYER_HUMAN )
		currentCameraPosition.myY = 0.0
		
		## move direction
		moveDirection = currentCameraPosition - self.__LastCameraPosition
		moveDirection.myY = 0.0
		moveLength = moveDirection.Length()
		moveDirection.Normalize()

		
		## angle between camDirection and moveDirection
		d = PosDot( moveDirection, self.__LastCameraLookAt )
		
		## use this for debugging
		#debug.DebugMessage( 'CameraMoveBackwardTest d=%f moveDirection=%s moveLength=%f accumulatedLength=%f' % (d, moveDirection, moveLength, self.__AccumulatedLength) )

		## angle threshold (we must be moving backwards)
		if d < -0.98:
			
			self.__AccumulatedLength += moveLength
		
			## length threshold (we must have moved a certain length)
			if self.__AccumulatedLength > 4.0:
				self.Update()
				return True
			else:
				self.Update()
				return False
				
		self.__AccumulatedLength = 0.0
		self.Update()
		return False
		

class CameraMoveLeftTest( BaseTest ):
	
	def __init__( self ):
		
		self.__LastCameraPosition = None
		self.__LastCameraLookAt = None
		self.__AccumulatedLength = 0.0
		self.Update()
	
	
	def Update( self ):
		
		self.__LastCameraPosition = wicg.GetCameraPosition( PLAYER_HUMAN )
		self.__LastCameraPosition.myY = 0.0

		## camera direction
		self.__LastCameraLookAt = wicmath.Angles2Direction( wicg.GetCameraRotation( PLAYER_HUMAN ) )
		self.__LastCameraLookAt.myY = 0.0
		self.__LastCameraLookAt.Normalize()
		
	
	def Test( self, someEventData ):

		## current position
		currentCameraPosition = wicg.GetCameraPosition( PLAYER_HUMAN )
		currentCameraPosition.myY = 0.0
		
		## move direction
		moveDirection = currentCameraPosition - self.__LastCameraPosition
		moveDirection.myY = 0.0
		moveLength = moveDirection.Length()
		moveDirection.Normalize()
		moveDirection = RotatePosition( moveDirection, -(math.pi/2.0) )
		moveDirection.myY = 0.0

		
		## angle between camDirection and moveDirection
		d = PosDot( moveDirection, self.__LastCameraLookAt )
		
		## use this for debugging
		#debug.DebugMessage( 'CameraMoveLeftTest d=%f moveDirection=%s moveLength=%f accumulatedLength=%f' % (d, moveDirection, moveLength, self.__AccumulatedLength) )

		## angle threshold (we must be moving backwards)
		if d < -0.98:
			
			self.__AccumulatedLength += moveLength
		
			## length threshold (we must have moved a certain length)
			if self.__AccumulatedLength > 4.0:
				self.Update()
				return True
			else:
				self.Update()
				return False
				
		self.__AccumulatedLength = 0.0
		self.Update()
		return False


class CameraMoveRightTest( BaseTest ):
	
	def __init__( self ):
		
		self.__LastCameraPosition = None
		self.__LastCameraLookAt = None
		self.__AccumulatedLength = 0.0
		self.Update()
	
	
	def Update( self ):
		
		self.__LastCameraPosition = wicg.GetCameraPosition( PLAYER_HUMAN )
		self.__LastCameraPosition.myY = 0.0

		## camera direction
		self.__LastCameraLookAt = wicmath.Angles2Direction( wicg.GetCameraRotation( PLAYER_HUMAN ) )
		self.__LastCameraLookAt.myY = 0.0
		self.__LastCameraLookAt.Normalize()
		
	
	def Test( self, someEventData ):

		## current position
		currentCameraPosition = wicg.GetCameraPosition( PLAYER_HUMAN )
		currentCameraPosition.myY = 0.0
		
		## move direction
		moveDirection = currentCameraPosition - self.__LastCameraPosition
		moveDirection.myY = 0.0
		moveLength = moveDirection.Length()
		moveDirection.Normalize()
		moveDirection = RotatePosition( moveDirection, (math.pi/2.0) )

		
		## angle between camDirection and moveDirection
		d = PosDot( moveDirection, self.__LastCameraLookAt )
		
		## use this for debugging
		#debug.DebugMessage( 'CameraMoveRightTest d=%f moveDirection=%s moveLength=%f accumulatedLength=%f' % (d, moveDirection, moveLength, self.__AccumulatedLength) )

		## angle threshold (we must be moving backwards)
		if d < -0.98:
			
			self.__AccumulatedLength += moveLength
		
			## length threshold (we must have moved a certain length)
			if self.__AccumulatedLength > 4.0:
				self.Update()
				return True
			else:
				self.Update()
				return False
				
		self.__AccumulatedLength = 0.0
		self.Update()
		return False



class CameraPanDownTest( BaseTest ):
	
	def __init__( self ):
		
		self.__CameraXRotation = wicg.GetCameraRotation( PLAYER_HUMAN ).myX
	
	
	def Test( self, someEventData ):
		
		currentXRotation = wicg.GetCameraRotation( PLAYER_HUMAN ).myX
		
		if currentXRotation > self.__CameraXRotation:
			self.__CameraXRotation = wicg.GetCameraRotation( PLAYER_HUMAN ).myX
			return True
		
		self.__CameraXRotation = wicg.GetCameraRotation( PLAYER_HUMAN ).myX
		return False



class CameraPanUpTest( BaseTest ):
	
	def __init__( self ):
		
		self.__CameraXRotation = wicg.GetCameraRotation( PLAYER_HUMAN ).myX
	
	
	def Test( self, someEventData ):
		
		currentXRotation = wicg.GetCameraRotation( PLAYER_HUMAN ).myX
		
		if currentXRotation < self.__CameraXRotation:
			self.__CameraXRotation = wicg.GetCameraRotation( PLAYER_HUMAN ).myX
			return True
		
		self.__CameraXRotation = wicg.GetCameraRotation( PLAYER_HUMAN ).myX
		return False


class CameraPanLeftTest( BaseTest ):
	
	def __init__( self ):
		
		self.__CameraYRotation = wicg.GetCameraRotation( PLAYER_HUMAN ).myY
	
	
	def Test( self, someEventData ):
		
		currentYRotation = wicg.GetCameraRotation( PLAYER_HUMAN ).myY
		
		if currentYRotation < self.__CameraYRotation:
			self.__CameraYRotation = wicg.GetCameraRotation( PLAYER_HUMAN ).myY
			return True
		
		self.__CameraYRotation = wicg.GetCameraRotation( PLAYER_HUMAN ).myY
		return False


class CameraPanRightTest( BaseTest ):
	
	def __init__( self ):
		
		self.__CameraYRotation = wicg.GetCameraRotation( PLAYER_HUMAN ).myY
	
	
	def Test( self, someEventData ):
		
		currentYRotation = wicg.GetCameraRotation( PLAYER_HUMAN ).myY
		
		if currentYRotation > self.__CameraYRotation:
			self.__CameraYRotation = wicg.GetCameraRotation( PLAYER_HUMAN ).myY
			return True
		
		self.__CameraYRotation = wicg.GetCameraRotation( PLAYER_HUMAN ).myY
		return False


class CameraMoveUpTest( BaseTest ):
	
	def __init__( self ):
		
		self.__CameraDistanceToGround = wicg.GetCameraHeightToGround( PLAYER_HUMAN )
	
	
	def Test( self, someEventData ):
		
		currentDistanceToGround = wicg.GetCameraHeightToGround( PLAYER_HUMAN )
		
		if currentDistanceToGround > self.__CameraDistanceToGround:
			self.__CameraDistanceToGround = wicg.GetCameraHeightToGround( PLAYER_HUMAN )
			return True
		
		self.__CameraDistanceToGround = wicg.GetCameraHeightToGround( PLAYER_HUMAN )
		return False


class CameraMoveDownTest( BaseTest ):
	
	def __init__( self ):
		
		self.__CameraDistanceToGround = wicg.GetCameraHeightToGround( PLAYER_HUMAN )
	
	
	def Test( self, someEventData ):
		
		currentDistanceToGround = wicg.GetCameraHeightToGround( PLAYER_HUMAN )
		
		if currentDistanceToGround < self.__CameraDistanceToGround:
			self.__CameraDistanceToGround = wicg.GetCameraHeightToGround( PLAYER_HUMAN )
			return True
		
		self.__CameraDistanceToGround = wicg.GetCameraHeightToGround( PLAYER_HUMAN )
		return False


class CameraIntersectCircleTest( BaseTest ):
	
	def __init__( self, aCenter, aRadius, aNormal ):
		
		self.__Center = common.GetPosition( aCenter )
		self.__Radius = aRadius
		self.__Normal = common.GetPosition( aNormal )
		self.__Normal.Normalize()
		
		self.__LastCameraPosition = wicg.GetCameraPosition( PLAYER_HUMAN )
		
	
	def Test( self, someEventData ):
		
		currentCameraPosition = wicg.GetCameraPosition( PLAYER_HUMAN )
		
		lastPosVector = self.__LastCameraPosition - self.__Center
		currPosVector = currentCameraPosition - self.__Center
		
		intPoint = (self.__LastCameraPosition + currentCameraPosition) * 0.5
		
		lastPosVector.Normalize()
		currPosVector.Normalize()
		
		## test for intersection
		lastDot = PosDot( lastPosVector, self.__Normal )
		currDot = PosDot( currPosVector, self.__Normal )
		
		## check for different signs
		if (lastDot < 0.0 and currDot > 0.0) or (lastDot > 0.0 and currDot < 0.0):
			
			if Distance3D( intPoint, self.__Center ) < self.__Radius:
				self.__LastCameraPosition = currentCameraPosition
				return True
			
		self.__LastCameraPosition = common.GetCopy( currentCameraPosition )
		return False



## ----- REACTIONS -----

def ValidateAllGroupUnitsEx():
	global theGroups
	
	theGroups.ValidateAllGroupUnits( True )


def UseAlternativeReactionSystem():
	global theReactions
	theReactions.AddLastAction( Action( SwitchToAlternativeSystem ) )
	
def SwitchToAlternativeSystem():
	global theReactions, theOldReactions
	global theGroups, theOldGroups
	global isInAlternativeMode
	global timeInAlternativeMode
	
	debug.DebugMessage( 'SwitchToAlternativeSystem(%s) - server' % isInAlternativeMode, debug.NONE )
	
	if isInAlternativeMode:
		common.StackTrace()
		debug.DebugMessage( 'SwitchToAlternativeSystem Warning! Trying to switch to alternative mode when already in alternative mode', debug.NONE )
		return
	
	theOldReactions = theReactions
	theReactions = Reactions()

	theOldGroups = theGroups
	theGroups = Groups()
	
	theReactions.RegisterReaction( Reaction( 'Update', Action( theGroups.Update ), TimeTest( UPDATE_FREQUENCY ) ) ).myRepeating = True
	
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
	global theGroups, theOldGroups
	global isInAlternativeMode
	global timeInAlternativeMode
	
	debug.DebugMessage( 'SwitchToPrimarySystem(%s) - server' % isInAlternativeMode, debug.NONE )
	
	if not isInAlternativeMode:
		debug.DebugMessage( 'SwitchToPrimarySystem Warning! Trying to switch to primary mode when already in primary mode', debug.NONE )
		return
	
	tempAlternative = theReactions
	theReactions = theOldReactions
	theGroups = theOldGroups
	
	timeInAlternativeMode = GetCurrentTime() - timeInAlternativeMode
	theReactions.AddTimeToTimers( timeInAlternativeMode )

	## we now validates and fixes all units in the primary system
	## this call will also do a refill test for each group ( could be a preformance peak )
	theGroups.ValidateAllGroupUnits( True )
	
	## process all cached events
	theReactions.Activate()
	isInAlternativeMode = False
	
	## we now check if all groups in the primary system are ok
	if not theGroups.ValidateAllGroupUnits( ):
		raise BadSystemException( 'SwitchToPrimarySystem Failed! There are invalid units in the system.' )
	
	tempAlternative.PostEvent( 'SystemSwitched' )
	tempAlternative = None
		

def PostEvent( anEventString, *someArguments ):
	global theReactions, isInAlternativeMode, theOldReactions, dualEvents

	theReactions.PostEvent( anEventString, *someArguments )
	
	if isInAlternativeMode and anEventString in dualEvents:
		theOldReactions.PostEvent( anEventString, *someArguments )

def RegisterReaction( aReaction, aFirstInList = False ):
	global theReactions
	theReactions.RegisterReaction( aReaction, aFirstInList )
	

def RemoveReaction( aReaction ):
	global theReactions
	theReactions.RemoveReaction( aReaction )


def RemoveReactionFromPrimary( aReaction ):
	global theReactions, theOldReactions
	
	if isInAlternativeMode:
		theOldReactions.RemoveReaction( aReaction )
	else:
		theReactions.RemoveReaction( aReaction )


def PurgeReactions( aRestartGroups = True ):
	global theReactions
	
	theReactions.RemoveAllReactions()
	
	if aRestartGroups:
		theReactions.RegisterReaction( Reaction( 'Update', Action( theGroups.Update ), None ) ).myRepeating = True


def StartGroupUpdate( ):
	global theReactions
	
	theReactions.RegisterReaction( Reaction( 'Update', Action( theGroups.Update ), None ) ).myRepeating = True


def ClearSystem():
	global theReactions
	theReactions.AddLastAction( Action( ExecuteClearSystem ) )


def ExecuteClearSystem():
	global theGroups, theReactions
	
	debug.DebugMessage( 'ExecuteClearSystem' )
	
	theReactions.Pause()
	
	theGroups.DestroyAllGroups()
	del theGroups
	theGroups = Groups()
	
	del theReactions
	theReactions = Reactions()
	
	theReactions.RegisterReaction( Reaction( 'Update', Action( theGroups.Update ), TimeTest( UPDATE_FREQUENCY ) ) ).myRepeating = True
	

def PauseReactions( aPauseFlag = True ):
	global theReactions

	theReactions.Pause( aPauseFlag )


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


def RE_OnGameStarted( someActions ):
	global theReactions
	
	newReaction = Reaction( 'GameStarted', someActions )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction


def RE_OnSystemSwitched( someActions ):
	global theReactions
	
	newReaction = Reaction( 'SystemSwitched', someActions )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction


def RE_OnUnitDestroyed( aUnitId, someActions ):
	global theReactions
	
	newReaction = UnitDestroyedReaction( someActions, aUnitId )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction


def RE_OnUnitCreatedWithKey( aKey, someActions ):
	global theReactions
	
	newReaction = Reaction( 'UnitCreated', someActions, SimpleTest( aKey, 2 ) )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction


def RE_OnUnitCreatedToPlayer( aPlayer, someActions ):
	global theReactions
	
	newReaction = Reaction( 'UnitCreated', someActions, UnitOwnerTest( aPlayer ) )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction


def RE_OnUnitTypesCreatedToPlayer( anOwner, someUnitTypes, nrOfUnits, someActions ):
	global theReactions
	
	newReaction = Reaction( 'UnitCreated', someActions, [UnitOwnerTest( anOwner ), UnitTypesTest( someUnitTypes ), CounterTest( nrOfUnits )] )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction	
	

def RE_OnUnitCreatedInSquad( aSquadId, someActions ):
	global theReactions
	
	newReaction = Reaction( 'UnitCreated', someActions, SimpleTest( aSquadId, 1 ) )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction


def RE_OnEmptyGroup( aGroup, someActions ):
	global theReactions
	
	if aGroup is None:
		raise BadReactionArgumentException( 'First argument aGroup is NoneType. Group must not be None!' )
	
	newReaction = Reaction( 'GroupSize', someActions, ComplexTest( aGroup, 0 ) )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction


def RE_OnEmptyPlatoon( aPlatoon, someActions ):
	global theReactions

	if aPlatoon is None:
		raise BadReactionArgumentException( 'First argument aPlatoon is NoneType. Platoon must not be None!' )
	
	newReaction = Reaction( 'PlatoonSize', someActions, ComplexTest( aPlatoon, 0 ) )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction


def RE_OnGroupRefill( aGroup, someActions ):
	global theReactions

	if aGroup is None:
		raise BadReactionArgumentException( 'First argument aGroup is NoneType. Group must not be None!' )
		
	newReaction = Reaction( 'Refill', someActions, SimpleTest( aGroup ) )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction


def RE_OnGroupUnitsDropped( aGroup, someActions ):
	global theReactions

	if aGroup is None:
		raise BadReactionArgumentException( 'First argument aGroup is NoneType. Group must not be None!' )
	
	newReaction = Reaction( 'UnitsDropped', someActions, SimpleTest( aGroup ) )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction


def RE_OnGroupSize( aGroup, aSize, someActions ):
	global theReactions
	
	if aGroup is None:
		raise BadReactionArgumentException( 'First argument aGroup is NoneType. Group must not be None!' )

	newReaction = GroupSizeReaction( someActions, aGroup, aSize )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction


def RE_OnPlatoonSize( aPlatoon, aSize, someActions ):
	global theReactions
	
	if aPlatoon is None:
		raise BadReactionArgumentException( 'First argument aPlatoon is NoneType. Platoon must not be None!' )

	newReaction = Reaction( 'PlatoonSize', someActions, ComplexTest( aPlatoon, aSize ) )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction


def RE_OnGroupHealth( aGroup, someActions, aHealth = 0, aUseMaxHealth = True, aNrOfUnits = -1 ):
	global theReactions

	if aGroup is None:
		raise BadReactionArgumentException( 'First argument aGroup is NoneType. Group must not be None!' )
	
	newReaction = Reaction( 'UpdateOne', someActions, GroupHealthTest( aGroup, aHealth, aUseMaxHealth, aNrOfUnits ) )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction


def RE_OnPlatoonHealth( aPlatoon, someActions, aHealth = 0, aUseMaxHealth = True, aNrOfUnits = -1 ):
	global theReactions

	if aPlatoon is None:
		raise BadReactionArgumentException( 'First argument aPlatoon is NoneType. Platoon must not be None!' )
	
	newReaction = Reaction( 'UpdateOne', someActions, PlatoonHealthTest( aPlatoon, aHealth, aUseMaxHealth, aNrOfUnits ) )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction


def RE_OnPlayerEnterContainer( aPlayer, aContainerId, someActions ):
	global theReactions
		
	newReaction = Reaction( 'UnitEnterContainer', someActions, [UnitOwnerTest( aPlayer ), SimpleTest( aContainerId, 1 )] )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction


def RE_OnPlayerEnterContainerEx( aPlayer, aContainerId, aNrOfUnits, someActions ):
	global theReactions
		
	newReaction = Reaction( 'UnitEnterContainer', someActions, [UnitOwnerTest( aPlayer ), SimpleTest( aContainerId, 1 ), CounterTest( aNrOfUnits )] )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction


def RE_OnPlayerExitContainer( aPlayer, aContainerId, someActions ):
	global theReactions
		
	newReaction = Reaction( 'UnitExitContainer', someActions, [UnitOwnerTest( aPlayer ), SimpleTest( aContainerId, 1 )] )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction


def RE_OnPlayerEnterBuilding( aPlayerId, aBuilding, someActions ):
	global theReactions
	
	newReaction = Reaction( 'UnitEnterBuilding', someActions, [ UnitOwnerTest( aPlayerId ), SimpleTest( StringToInt( aBuilding ), 1 ) ] )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction


def RE_OnGroupsEnterBuilding( someGroups, aBuilding, someActions ):
	global theReactions
	
	if not isinstance( someGroups, list ):
		someGroups = [someGroups]
	
	c = 0
	for grp in someGroups:
		if grp is None:
			raise BadReactionArgumentException( 'Group at index %d is NoneType. Group must not be None!' % c )
		c += 1
	
	newReaction = Reaction( 'UnitEnterBuilding', someActions, [ UnitInGroupsTest( someGroups ), SimpleTest( StringToInt( aBuilding ), 1 ) ] )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction


def RE_OnPlatoonEnterBuilding( aPlatoon, aBuilding, someActions ):
	global theReactions

	if aPlatoon is None:
		raise BadReactionArgumentException( 'First argument aPlatoon is NoneType. Platoon must not be None!' )

	newReaction = Reaction( 'UnitEnterBuilding', someActions, [ GroupInPlatoonTest( aPlatoon ), SimpleTest( StringToInt( aBuilding ), 1 ) ] )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction


def RE_OnUnitInCombat( aUnitId, someActions ):
	global theReactions
		
	newReaction = UnitInCombatReaction( someActions, aUnitId )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction


def RE_OnGroupInCombat( aGroup, someActions ):
	global theReactions
	
	if aGroup is None:
		raise BadReactionArgumentException( 'First argument aGroup is NoneType. Group must not be None!' )
	
	newReaction = GroupInCombatReaction( someActions, aGroup )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction


def RE_OnPlayerInCombatWithGroup( aPlayerId, aGroup, someActions ):
	global theReactions
	
	if aGroup is None:
		raise BadReactionArgumentException( 'Second argument aGroup is NoneType. Group must not be None!' )

	newReaction = Reaction( 'GroupInCombat', someActions, [SimpleTest( aGroup ), GroupInCombatUnitOwnerTest( aPlayerId )] )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction


def RE_OnPlayerInCombatWithPlatoon( aPlayerId, aPlatoon, someActions ):
	global theReactions
	
	if aPlatoon is None:
		raise BadReactionArgumentException( 'Second argument aPlatoon is NoneType. Platoon must not be None!' )

	newReaction = Reaction( 'GroupInCombat', someActions, [GroupInPlatoonTest( aPlatoon ), GroupInCombatUnitOwnerTest( aPlayerId )] )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction


def RE_OnPlayerKilledUnitsInGroups( aPlayerId, someGroups, aNrOfUnits, someActions ):
	global theReactions
	
	if not isinstance( someGroups, list ):
		someGroups = [someGroups]
	
	c = 0
	for grp in someGroups:
		if grp is None:
			raise BadReactionArgumentException( 'Second argument someGroups contains NoneType Group at index %d. All Groups must be valid!' % c )
		c += 1
	
	newReaction = Reaction( 'UnitDestroyed', someActions, [UnitOwnerTest( aPlayerId, 1 ), UnitInGroupsTest( someGroups ), CounterTest( aNrOfUnits )] )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction


def RE_OnPlayerInAreasKillsUnitsInGroups( aPlayerId, someAreas, someGroups, someActions ):
	global theReactions
	
	if not isinstance( someGroups, list ):
		someGroups = [someGroups]
	
	c = 0
	for grp in someGroups:
		if grp is None:
			raise BadReactionArgumentException( 'Second argument someGroups contains NoneType Group at index %d. All Groups must be valid!' % c )
		c += 1
	
	newReaction = Reaction( 'UnitDestroyed', someActions, [UnitOwnerTest( aPlayerId, 1 ), PlayerInAreaTest( aPlayerId, someAreas ), UnitInGroupsTest( someGroups )] )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction				


def RE_OnPlayerKilledPlayerUnits( aKillerPlayerId, aKilledPlayerId, aNrOfUnits, someActions ):
	global theReactions
		
	newReaction = Reaction( 'UnitDestroyed', someActions, [UnitOwnerTest( aKillerPlayerId, 1 ), UnitOwnerTest( aKilledPlayerId ), CounterTest( aNrOfUnits )] )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction


def RE_OnPatrolAtTarget( aGroup, someActions ):
	global theReactions
	
	if aGroup is None:
		raise BadReactionArgumentException( 'First argument aGroup is NoneType. Group must not be None!' )

	newReaction = Reaction( 'PatrolAtTarget', someActions, SimpleTest( aGroup ) )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction


def RE_OnPlayerAttackedByUnit( aPlayerId, aUnitId, someActions ):
	global theReactions
	
	newReaction = Reaction( 'UnitInCombat', someActions, [UnitOwnerTest( aPlayerId ), SimpleTest( aUnitId, 1 )] )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction


def RE_OnPlatoonInCombat( aPlatoon, someActions ):
	global theReactions

	if aPlatoon is None:
		raise BadReactionArgumentException( 'First argument aPlatoon is NoneType. Platoon must not be None!' )
	
	newReaction = Reaction( 'PlatoonInCombat', someActions, SimpleTest( aPlatoon ) )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction


def RE_OnUnitInArea( someUnitIds, someAreas, someActions ):
	global theReactions
	
	newReaction = Reaction( 'UpdateOne', someActions, UnitInAreaTest( someUnitIds, someAreas ) )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction


def RE_OnUnitNotInArea( someUnitIds, someAreas, someActions ):
	global theReactions
	
	newReaction = Reaction( 'UpdateOne', someActions, UnitNotInAreaTest( someUnitIds, someAreas ) )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction


def RE_OnUnitsInArea( someUnitIds, someAreas, someActions ):
	global theReactions
	
	newReaction = Reaction( 'UpdateOne', someActions, UnitNotInAreaTest( someUnitIds, someAreas ) )
	newReaction.myTestType = REACTION_TEST_NOT
	theReactions.RegisterReaction( newReaction )
	
	return newReaction


def RE_OnUnitsNotInArea( someUnitIds, someAreas, someActions ):
	global theReactions
	
	newReaction = Reaction( 'UpdateOne', someActions, UnitInAreaTest( someUnitIds, someAreas ) )
	newReaction.myTestType = REACTION_TEST_NOT
	theReactions.RegisterReaction( newReaction )
	
	return newReaction


def RE_OnPlayerInArea( aPlayer, someAreas, someActions ):
	global theReactions
	
	newReaction = Reaction( 'UpdateOne', someActions, PlayerInAreaTest( aPlayer, someAreas ) )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction


def RE_OnPlayerInAreaNotChoppers( aPlayer, someAreas, someActions ):
	global theReactions
	
	newReaction = Reaction( 'UpdateOne', someActions, PlayerInAreaTestNotChoppers( aPlayer, someAreas ) )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction


def RE_OnPlayerNotInArea( aPlayer, someAreas, someActions ):
	global theReactions
	
	newReaction = Reaction( 'UpdateOne', someActions, PlayerInAreaTest( aPlayer, someAreas ) )
	newReaction.myTestType = REACTION_TEST_NOT
	theReactions.RegisterReaction( newReaction )
	
	return newReaction


def RE_OnRadarScanInArea( aPlayer, someAreas, someActions ):
	global theReactions
	
	newReaction = Reaction( 'UpdateOne', someActions, RadarScanInAreaTest( aPlayer, someAreas ) )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction


def RE_OnTeamInArea( aTeam, someAreas, someActions ):
	global theReactions
	
	newReaction = Reaction( 'UpdateOne', someActions, TeamInAreaTest( aTeam, someAreas ) )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction


def RE_OnTeamNotInArea( aTeam, someAreas, someActions ):
	global theReactions
	
	newReaction = Reaction( 'UpdateOne', someActions, TeamInAreaTest( aTeam, someAreas ) )
	newReaction.myTestType = REACTION_TEST_NOT
	theReactions.RegisterReaction( newReaction )
	
	return newReaction


def RE_OnGroupInArea( aGroup, someAreas, someActions, aAllIn = False ):
	global theReactions
	
	if aGroup is None:
		raise BadReactionArgumentException( 'First argument aGroup is NoneType. Group must not be None!' )

	newReaction = Reaction( 'UpdateOne', someActions, GroupInAreaTest( aGroup, someAreas, aAllIn ) )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction


def RE_OnGroupNotInArea( aGroup, someAreas, someActions, aAllOut = True ):
	global theReactions
	
	if aGroup is None:
		raise BadReactionArgumentException( 'First argument aGroup is NoneType. Group must not be None!' )

	newReaction = Reaction( 'UpdateOne', someActions, GroupNotInAreaTest( aGroup, someAreas, aAllOut ) )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction


def RE_OnPlatoonInArea( aPlatoon, someAreas, someActions, aAllIn = False ):
	global theReactions

	if aPlatoon is None:
		raise BadReactionArgumentException( 'First argument aPlatoon is NoneType. Platoon must not be None!' )
	
	newReaction = Reaction( 'UpdateOne', someActions, PlatoonInAreaTest( aPlatoon, someAreas, aAllIn ) )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction


def RE_OnNotPlatoonInArea( aPlatoon, someAreas, someActions, aAllOut = False ):
	global theReactions

	if aPlatoon is None:
		raise BadReactionArgumentException( 'First argument aPlatoon is NoneType. Platoon must not be None!' )
	
	newReaction = Reaction( 'UpdateOne', someActions, PlatoonNotInAreaTest( aPlatoon, someAreas, aAllOut ) )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction


def RE_OnCommandPointTaken( aCommandPoint, aTeam, someActions ):
	global theReactions

	newReaction = Reaction( 'CommandPointTaken', someActions, ComplexTest( StringToInt( aCommandPoint ), aTeam ) )
	theReactions.RegisterReaction( newReaction )

	return newReaction


def RE_OnPerimeterPointTaken( aPerimeterPoint, aTeam, someActions ):
	global theReactions

	newReaction = Reaction( 'PerimeterPointTaken', someActions, ComplexTest( StringToInt( aPerimeterPoint ), aTeam ) )
	theReactions.RegisterReaction( newReaction )

	return newReaction


def RE_OnFortificationCreated( aPerimeterPoint, aTeam, aLevel, someActions ):
	global theReactions

	newReaction = Reaction( 'FortificationCreated', someActions, ComplexTest( StringToInt( aPerimeterPoint ), aTeam, aLevel ) )
	theReactions.RegisterReaction( newReaction )

	return newReaction


def RE_OnCustomFortificationCreated( aPerimeterPoint, aTeam, someActions ):
	global theReactions

	newReaction = Reaction( 'FortificationCreated', someActions, [ComplexTest( StringToInt( aPerimeterPoint ), aTeam ), ComplexTest( StringToInt( aPerimeterPoint ), 0 )] )
	newReaction.myTestType = REACTION_TEST_OR
	theReactions.RegisterReaction( newReaction )

	return newReaction


def RE_OnFortificationDestroyed( aPerimeterPoint, aTeam, aLevel, someActions ):
	global theReactions

	newReaction = Reaction( 'FortificationDestroyed', someActions, ComplexTest( StringToInt( aPerimeterPoint ), aTeam, aLevel ) )
	theReactions.RegisterReaction( newReaction )

	return newReaction


def RE_OnCustomFortificationDestroyed( aPerimeterPoint, aTeam, someActions ):
	global theReactions

	newReaction = Reaction( 'FortificationDestroyed', someActions, [ComplexTest( StringToInt( aPerimeterPoint ), aTeam ), ComplexTest( StringToInt( aPerimeterPoint ), 0 )] )
	newReaction.myTestType = REACTION_TEST_OR
	theReactions.RegisterReaction( newReaction )

	return newReaction


def RE_OnBuildingDestroyed( aBuildingName, someActions ):
	global theReactions

	newReaction = Reaction( 'BuildingDestroyed', someActions, SimpleTest( StringToInt( aBuildingName ) ) )
	theReactions.RegisterReaction( newReaction )

	return newReaction


def RE_OnBridgeDestroyed( aBridgeName, someActions ):
	global theReactions

	newReaction = Reaction( 'BridgeDestroyed', someActions, SimpleTest( StringToInt( aBridgeName ) ) )
	theReactions.RegisterReaction( newReaction )

	return newReaction

	
def RE_OnDestroyableObjectDestroyed( aDestroyableObjectName, someActions ):
	global theReactions

	newReaction = Reaction( 'DestroyableObjectDestroyed', someActions, SimpleTest( StringToInt( aDestroyableObjectName ) ) )
	theReactions.RegisterReaction( newReaction )

	return newReaction

	
def RE_OnMessageBoxClosed( aMessageBoxId, someActions ):
	global theReactions

	newReaction = Reaction( 'MessageBoxClosed', someActions, SimpleTest( aMessageBoxId ) )
	theReactions.RegisterReaction( newReaction )

	return newReaction


def RE_OnEventStringDone( anEventString, someActions ):
	global theReactions
	
	newReaction = Reaction( 'EventStringDone', someActions, SimpleTest( StringToInt( anEventString ) ) )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction


def RE_OnAPLimitReached( anAPLimit, someActions ):
	global theReactions
	
	newReaction = Reaction( 'Update', someActions, APLimitTest( anAPLimit ) )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction


def RE_OnUnitSelected( someActions ):
	global theReactions
	
	newReaction = Reaction( 'AGENT_SELECTED', someActions )
	theReactions.RegisterReaction( newReaction )

	return newReaction


def RE_OnMultipleUnitsSelected( someActions ):
	global theReactions
	
	newReaction = Reaction( 'AGENT_SELECTED_MULTIPLE', someActions )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction


def RE_OnUnitBought( someActions ):
	global theReactions
	
	newReaction = Reaction( 'SPAWNER_DEPLOY', someActions )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction


def RE_OnSpawnerDeployed( someActions ):
	global theReactions
	
	newReaction = Reaction( 'SPAWNER_DEPLOY', someActions )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction


def RE_OnMiniMapClicked( someActions ):
	global theReactions
	
	newReaction = Reaction( 'CLICKED_MINIMAP', someActions )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction
	

def RE_OnTAClicked( someActions ):
	global theReactions
	
	newReaction = Reaction( 'TACTICAL_AID_SCREEN_PRESSED', someActions )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction


def RE_OnReinforcementsMenuClicked( someActions ):
	global theReactions
	
	newReaction = Reaction( 'REINFORCEMENTS_SCREEN_PRESSED', someActions )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction


def RE_OnTAChoosen( someActions ):
	global theReactions
	
	newReaction = Reaction( 'TACTICAL_AID_CHOOSEN', someActions )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction

def RE_OnTAExecuted( someActions ):
	global theReactions
	
	newReaction = Reaction( 'TAExecuted', someActions )		
	#newReaction.myRepeating = True
	
	theReactions.RegisterReaction( newReaction )
	
	return newReaction	

def RE_OnTASpawned( aTrackingName, someActions ):
	global theReactions
	
	newReaction = Reaction( 'TASpawned', someActions, SimpleTest( aTrackingName ) )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction

def RE_OnTAProjectile( aTrackingName, aTrackingId, someActions ):
	global theReactions
	
	newReaction = Reaction( 'TAProjectile', someActions, [ SimpleTest( aTrackingName, 0 ), SimpleTest( aTrackingId, 1 ) ] )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction


def RE_OnTAProjectileDestroyed( aTrackingName, aTrackingId, someActions ):
	global theReactions
	
	newReaction = Reaction( 'TAProjectileDestroyed', someActions, [ SimpleTest( aTrackingName, 0 ), SimpleTest( aTrackingId, 1 ) ] )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction


def RE_OnSpecialAbilityClicked( someActions ):
	global theReactions
	
	newReaction = Reaction( 'CLICKED_SPECIAL_ABILITY', someActions )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction


def RE_OnSpecialAbilityUsed( someActions ):
	global theReactions
	
	newReaction = Reaction( 'USED_SPECIAL_ABILITY', someActions )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction
	

def RE_OnObjectiveBrowserActivated( someActions ):
	global theReactions
	
	newReaction = Reaction( 'OBJECTIVE_BROWSER_ACTIVATED', someActions )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction
	

def RE_OnObjectiveBrowserDeactivated( someActions ):
	global theReactions
	
	newReaction = Reaction( 'OBJECTIVE_BROWSER_DEACTIVATED', someActions )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction


def RE_OnEnterMegaMap( someActions ):
	global theReactions
	
	newReaction = Reaction( 'MEGAMAP_PRESSED', someActions )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction


def RE_OnExitMegaMap( someActions ):
	global theReactions
	
	newReaction = Reaction( 'MEGAMAP_CLOSED', someActions )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction


def RE_OnEnterDropZoneMode( someActions ):
	global theReactions
	
	newReaction = Reaction( 'ENTER_DROPZONE_MODE', someActions )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction

def RE_OnDropZonePlaced( someActions ):
	global theReactions
	
	newReaction = Reaction( 'DROPZONE_PLACED', someActions )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction


def RE_OnLessonRestart( someActions ):
	global theReactions
	
	newReaction = Reaction( 'CLICKED_RESTARTLESSION', someActions )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction


def RE_OnNextLesson( someActions ):
	global theReactions
	
	newReaction = Reaction( 'CLICKED_NEXTLESSION', someActions )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction


def RE_OnSkipMessageBoxButtonClicked( someActions ):
	global theReactions
	
	newReaction = Reaction( 'CLICKED_SKIPLESSION', someActions )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction


def RE_OnLessonFinished( someActions ):
	global theReactions
	
	newReaction = Reaction( 'CLICKED_FINISHLESSION', someActions )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction


def RE_OnCameraInArea( anArea, someActions ):
	global theReactions
	
	newReaction = Reaction( 'UpdateOne', someActions, CameraInAreaTest( anArea ) )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction


def RE_OnCameraIntersectCircle( aCenter, aRadius, aNormal, someActions ):
	global theReactions
	
	newReaction = Reaction( 'Update', someActions, [TimeTest( 0.5 ), CameraIntersectCircleTest( aCenter, aRadius, aNormal )] )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction


def RE_OnCameraMoveForward( someActions ):
	global theReactions
	
	newReaction = Reaction( 'Update', someActions, [TimeTest(0.1), CameraMoveForwardTest(), NotInMegamapTest()] )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction


def RE_OnCameraMoveBackward( someActions ):
	global theReactions
	
	newReaction = Reaction( 'Update', someActions, [TimeTest(0.1), CameraMoveBackwardTest(), NotInMegamapTest()] )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction


def RE_OnCameraMoveLeft( someActions ):
	global theReactions
	
	newReaction = Reaction( 'Update', someActions, [TimeTest(0.1), CameraMoveLeftTest(), NotInMegamapTest()] )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction


def RE_OnCameraMoveRight( someActions ):
	global theReactions
	
	newReaction = Reaction( 'Update', someActions, [TimeTest(0.1), CameraMoveRightTest(), NotInMegamapTest()] )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction

	
def RE_OnCameraPanDown( someActions ):
	global theReactions
	
	newReaction = Reaction( 'Update', someActions, [CameraPanDownTest(), NotInMegamapTest()] )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction


def RE_OnCameraPanUp( someActions ):
	global theReactions
	
	newReaction = Reaction( 'Update', someActions, [CameraPanUpTest(), NotInMegamapTest()] )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction


def RE_OnCameraPanLeft( someActions ):
	global theReactions
	
	newReaction = Reaction( 'Update', someActions, [CameraPanLeftTest(), NotInMegamapTest()] )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction


def RE_OnCameraPanRight( someActions ):
	global theReactions
	
	newReaction = Reaction( 'Update', someActions, [CameraPanRightTest(), NotInMegamapTest()] )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction


def RE_OnCameraMoveUp( someActions ):
	global theReactions
	
	newReaction = Reaction( 'Update', someActions, [CameraMoveUpTest(), NotInMegamapTest()] )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction


def RE_OnCameraMoveDown( someActions ):
	global theReactions
	
	newReaction = Reaction( 'Update', someActions, [CameraMoveDownTest(), NotInMegamapTest()] )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction


def RE_OnCustomEvent( anEventString, someActions, someTestFunctions = None):
	global theReactions

	newReaction = Reaction( anEventString, someActions, someTestFunctions )
	theReactions.RegisterReaction( newReaction )

	return newReaction


def RE_OnCameraMove( someActions ):
	global theReactions

	newReaction = Reaction( 'CAMERA_MOVE', someActions )
	theReactions.RegisterReaction( newReaction )

	return newReaction


def RE_OnCameraZoomIn( someActions ):
	global theReactions

	newReaction = Reaction( 'CAMERA_ZOOM_IN', someActions )
	theReactions.RegisterReaction( newReaction )

	return newReaction


def RE_OnCameraZoomOut( someActions ):
	global theReactions

	newReaction = Reaction( 'CAMERA_ZOOM_OUT', someActions )
	theReactions.RegisterReaction( newReaction )

	return newReaction


def RE_OnGroupSelect( someActions ):
	global theReactions

	newReaction = Reaction( 'GROUP_SELECT', someActions )
	theReactions.RegisterReaction( newReaction )

	return newReaction


def RE_OnSingleSelect( someActions ):
	global theReactions

	newReaction = Reaction( 'SINGLE_SELECT', someActions )
	theReactions.RegisterReaction( newReaction )

	return newReaction


def RE_OnCompanyCreated( someActions ):
	global theReactions

	newReaction = Reaction( 'COMPANY_CREATED', someActions )
	theReactions.RegisterReaction( newReaction )

	return newReaction


def RE_OnUnitpaneActivated( someActions ):
	global theReactions

	newReaction = Reaction( 'UNITPANE_ACTIVATED', someActions )
	theReactions.RegisterReaction( newReaction )

	return newReaction


def RE_OnUnitpaneSelected( someActions ):
	global theReactions

	newReaction = Reaction( 'UNITPANE_SELECTED', someActions )
	theReactions.RegisterReaction( newReaction )

	return newReaction


def RE_OnConsoleUnitSelected( someActions ):
	global theReactions

	newReaction = Reaction( 'UNIT_SELECTED', someActions )
	theReactions.RegisterReaction( newReaction )

	return newReaction


def RE_OnEnterVehicle( someActions ):
	global theReactions

	newReaction = Reaction( 'ENTER_VEHICLE', someActions )
	theReactions.RegisterReaction( newReaction )

	return newReaction


def RE_OnExitVehicle( someActions ):
	global theReactions

	newReaction = Reaction( 'EXIT_VEHICLE', someActions )
	theReactions.RegisterReaction( newReaction )

	return newReaction


def RE_OnEnterBuilding( someActions ):
	global theReactions

	newReaction = Reaction( 'ENTER_BUILDING', someActions )
	theReactions.RegisterReaction( newReaction )

	return newReaction


def RE_OnExitBuilding( someActions ):
	global theReactions

	newReaction = Reaction( 'EXIT_BUILDING', someActions )
	theReactions.RegisterReaction( newReaction )

	return newReaction


def RE_OnDefenseActivated( someActions ):
	global theReactions

	newReaction = Reaction( 'DEFENSE_ACTIVATED', someActions )
	theReactions.RegisterReaction( newReaction )

	return newReaction


def RE_OnViewedObjectives( someActions ):
	global theReactions

	newReaction = Reaction( 'VIEWED_OBJECTIVES', someActions )
	theReactions.RegisterReaction( newReaction )

	return newReaction


def RE_OnReinforcementsMenuActivated( someActions ):
	global theReactions

	newReaction = Reaction( 'REINF_ACTIVATED', someActions )
	theReactions.RegisterReaction( newReaction )

	return newReaction


def RE_OnSetFirstDropZone( someActions ):
	global theReactions

	newReaction = Reaction( 'DZ_POSITION', someActions )
	theReactions.RegisterReaction( newReaction )

	return newReaction


def RE_OnSetDropZone( someActions ):
	global theReactions

	newReaction = Reaction( 'DZ_MOVE', someActions )
	theReactions.RegisterReaction( newReaction )

	return newReaction


def RE_OnCancelDropZone( someActions ):
	global theReactions

	newReaction = Reaction( 'DZ_CANCEL', someActions )
	theReactions.RegisterReaction( newReaction )

	return newReaction


def RE_OnPlacedDropZone( someActions ):
	global theReactions

	newReaction = Reaction( 'DZ_SET', someActions )
	theReactions.RegisterReaction( newReaction )

	return newReaction


def RE_OnTAMenuActivated( someActions ):
	global theReactions

	newReaction = Reaction( 'TA_ACTIVATED', someActions )
	theReactions.RegisterReaction( newReaction )

	return newReaction


def RE_OnOrderOutsideRestrictionMask( someActions ):
	global theReactions

	newReaction = Reaction( 'ORDER_OUTSIDE_RESTRICTION_MASK', someActions )
	theReactions.RegisterReaction( newReaction )

	return newReaction
	
def RE_OnTAOutsideRestrictedArea( someActions ):
	global theReactions

	newReaction = Reaction( 'TA_OUTSIDE_RESTRICTED_AREA', someActions )
	theReactions.RegisterReaction( newReaction )

	return newReaction
	
def RE_OnAttackGround( someActions ):
	global theReactions

	newReaction = Reaction( 'ATTACK_GROUND', someActions )
	theReactions.RegisterReaction( newReaction )

	return newReaction
def RE_OnPlayerInForest( aPlayerId, someActions ):
	global theReactions
	
	newReaction = Reaction( 'UpdateOne', someActions, PlayerInForestTest( aPlayerId ) )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction	



def RE_OnPlayerHoldFire( aPlayerId, someActions, aAllUnits = True, aHoldingFire = True ):
	global theReactions
	
	newReaction = Reaction( 'UpdateOne', someActions, PlayerHoldFire( aPlayerId, aAllUnits, aHoldingFire ) )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction	


def RE_OnSpecialAbilityFired( anAbility, someActions, aUsingUnitId = None ):
	global theReactions
	
	newReaction = Reaction( 'FIRED_SPECIAL_ABILITY', someActions, SpecialAbilityFiredTest( anAbility, aUsingUnitId ) )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction

def OnTutorialMessageBoxClosed( aMessageBoxNameHash ):		
	PostEvent( "OnTutorialMessageBoxClosed", aMessageBoxNameHash )
	return 1

def RE_OnTutorialMessageBoxClosed( aMessageBoxNameHash, someActions ):
	global theReactions
			
	newReaction = Reaction( 'OnTutorialMessageBoxClosed', someActions, SimpleTest( aMessageBoxNameHash ) )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction


def RE_OnOffensiveSpecialAbilityFired( someActions ):
	global theReactions
	
	newReaction = Reaction( 'FIRED_SPECIAL_ABILITY', someActions, SimpleTest( 0, 2 ) )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction	


def RE_OnDefensiveSpecialAbilityFired( someActions ):
	global theReactions
	
	newReaction = Reaction( 'FIRED_SPECIAL_ABILITY', someActions, SimpleTest( 1, 2 ) )
	theReactions.RegisterReaction( newReaction )
	
	return newReaction	
	
	
# COMPLEX REACTIONS
class RE_OnCommandPointFortifiedEx( ComplexReaction ):
	
	
	def __init__ ( self, somePerimeterPoints, aTeam, aLevel, someActions, aExactLevelCheck = False, aTestAtInit = False ):
		
		ComplexReaction.__init__(self, someActions)
		
		self.__Reactions = []
		self.__Counters = {}
		self.__Level = aLevel
		self.__ExactLevelCheck = aExactLevelCheck
		
		self.myRepeating = False
				
		if isinstance( somePerimeterPoints, list ):
			for per in somePerimeterPoints:
				reactCreate = RE_OnCustomFortificationCreated( per, aTeam, Action( self.FortificationCreated, per ) )
				reactDestroy = RE_OnCustomFortificationDestroyed( per, aTeam, Action( self.FortificationDestroyed, per ) )
				
				reactCreate.myRepeating = True
				reactDestroy.myRepeating = True
				
				self.__Reactions.append( reactCreate )
				self.__Reactions.append( reactDestroy )
				
				self.__Counters[per] = 0
		else:
			reactCreate = RE_OnCustomFortificationCreated( somePerimeterPoints, aTeam, Action( self.FortificationCreated, somePerimeterPoints ) )
			reactDestroy = RE_OnCustomFortificationDestroyed( somePerimeterPoints, aTeam, Action( self.FortificationDestroyed, somePerimeterPoints ) )
			
			reactCreate.myRepeating = True
			reactDestroy.myRepeating = True
			
			self.__Reactions.append( reactCreate )
			self.__Reactions.append( reactDestroy )
			
			self.__Counters[somePerimeterPoints] = 0

		
		for p in self.__Counters:
			try:
				## we always check neutral perimeter points
				
				if CheckFortificationLevel( p, 1, aTeam ) or CheckFortificationLevel( p, 1, TEAM_NEUTRAL ):
					self.__Counters[p] += 1
				if CheckFortificationLevel( p, 2, aTeam ) or CheckFortificationLevel( p, 2, TEAM_NEUTRAL ):
					self.__Counters[p] += 1
				if CheckFortificationLevel( p, 3, aTeam ) or CheckFortificationLevel( p, 3, TEAM_NEUTRAL ):
					self.__Counters[p] += 1
			except Exception:
				debug.DebugMessage( 'OnCommandPointFortifiedEx Warning! No such perimeter point or perimeter point not created, %s' % p, debug.NONE )
		
		if aTestAtInit:
			self.TestForExecution()
			

	def __del__( self ):
		self.Shutdown()

	def Shutdown( self ):
		global theReactions
		
		if self.myRepeating:
			return
		
		for react in self.__Reactions:
			theReactions.RemoveReaction( react )
			
		self.__Reactions = []


	def FortificationCreated( self, aPerimeterPoint ):
		self.__Counters[aPerimeterPoint] += 1
		self.TestForExecution()

		
	def FortificationDestroyed( self, aPerimeterPoint ):
		if self.__Counters[aPerimeterPoint] > 0:
			self.__Counters[aPerimeterPoint] -= 1
		else:
			debug.DebugMessage('OnCommandPointFortifiedEx::FortificationDestroyed Warning! none existing fortification destroyed', debug.BRIEF)
		self.TestForExecution()

	
	def TestForExecution( self ):
		for counter in self.__Counters.values():
			if self.__ExactLevelCheck:
				if counter != self.__Level:
					return
			else:
				if counter < self.__Level:
					return
		
		self.Execute()
		self.Shutdown()


class RE_OnCommandPointTakenEx( ComplexReaction ):
	
	
	def __init__ ( self, someCommandPoints, aTeam, someActions, aTestAtInit = False ):
		
		ComplexReaction.__init__(self, someActions)
		
		self.__Reactions = []
		self.__CommandPoints = {}
		
		self.myRepeating = False
				
		if isinstance( someCommandPoints, list ):
			for c in someCommandPoints:
				reactTaken = RE_OnCommandPointTaken( c, aTeam, Action( self.CommandPointTaken, c ) )
				reactLost = RE_OnCommandPointTaken( c, aTeam, Action( self.CommandPointLost, c ) )
				reactLost.myTestType = REACTION_TEST_NOT
				
				reactTaken.myRepeating = True
				reactLost.myRepeating = True
				
				self.__Reactions.append( reactTaken )
				self.__Reactions.append( reactLost )
				
				self.__CommandPoints[c] = False
		else:
			raise BadReactionArgumentException( 'RE_OnCommandPointTakenEx requires a list with commandpoints. Use RE_OnCommandPointTaken?' )
		
		
		## update the commandpoints information				
		for c in self.__CommandPoints:
			if wicg.GetCommandPointOwner(c) == aTeam:
				self.__CommandPoints[c] = True
		
		## test if we already owns the commandpoints
		if aTestAtInit:
			self.TestForExecution()
			

	def __del__( self ):
		self.Shutdown()

	def Shutdown( self ):
		global theReactions
		
		if self.myRepeating:
			return
		
		for react in self.__Reactions:
			theReactions.RemoveReaction( react )
			
		self.__Reactions = []


	def CommandPointTaken( self, aCommandPoint ):
		self.__CommandPoints[aCommandPoint] = True
		self.TestForExecution()

		
	def CommandPointLost( self, aCommandPoint ):
		self.__CommandPoints[aCommandPoint] = False
		self.TestForExecution()

	
	def TestForExecution( self ):
		
		for c in self.__CommandPoints:
			if not self.__CommandPoints[c]:
				return
		
		self.Execute()
		self.Shutdown()


class RE_OnCustomEventEx( ComplexReaction ):
	
	
	def __init__ ( self, someEvents, someActions, someTests = None, aTestType = COMPLEX_TEST_AND, aAddFirst = False ):
		
		ComplexReaction.__init__(self, someActions)
		
		self.__Reactions = []
		self.__TestType = aTestType
		self.__Counter = 0
		
		if isinstance( someEvents, list ):
			c = 0
			for event in someEvents:
				if someTests is None:
					react = RE_OnCustomEvent(event, Action(self.Update))
					
					## should this reaction be added first in the reaction list, this is only used by the invulnerable obj camera code
					if aAddFirst:
						RemoveReaction( react )
						RegisterReaction( react, True )
					
					self.__Reactions.append(react)
				else:
					if isinstance( someTests, list ):
						self.__Reactions.append(RE_OnCustomEvent(event, Action(self.Update), someTests[c]))
					else:
						self.__Reactions.append(RE_OnCustomEvent(event, Action(self.Update), someTests))
				c += 1
		else:
			if someTests is None:
				self.__Reactions.append(RE_OnCustomEvent(someEvents, Action(self.Update)))
			else:
				self.__Reactions.append(RE_OnCustomEvent(someEvents, Action(self.Update), someTests))
			

	def __del__( self ):
		self.Shutdown()

	def Shutdown( self ):
		global theReactions
		
		for react in self.__Reactions:
			theReactions.RemoveReaction( react )
			
		self.__Reactions = []


	def Update( self ):
		
		self.__Counter += 1
		
		if self.__TestType == COMPLEX_TEST_OR:
			self.Execute()
			self.Shutdown()
			return
		elif self.__TestType == COMPLEX_TEST_AND and self.__Counter == len( self.__Reactions ):
			self.Execute()
			self.Shutdown()
			return
			


## ----- GROUP -----

def CreateGroup( aName = None, aUnits = [], aTarget = None, aOwner = 0, aTeam = 0):
	global theGroups
	
	return theGroups.AddGroup( Group( aUnits, aTarget, aOwner, aTeam ), aName )

def RemoveGroup( aGroup, aDestroy = False, aShouldExplode = False ):
	global theGroups

	if aGroup is None:
		return
	
	if aDestroy:
		aGroup.DestroyGroup( aShouldExplode )

	theGroups.RemoveGroup( aGroup )


def CancelAllActiveAirDrops():
	global theGroups
	
	theGroups.CancelAllAirDrops()
	wicg.CancelAllSpawners()


def IsGroup( aGroup ):
	global theGroups
	
	return theGroups.IsGroup( aGroup )


def IsGroupByName( aGroupName ):
	global theGroups
	
	return theGroups.IsGroupByName( aGroupName )


def IsUnitGroupUnit( aUnitId ):
	global theGroups
	
	grp = theGroups.GetGroupByUnit( aUnitId )
	return grp
	

def DestroyAllGroups():
	global theGroups
	
	theGroups.DestroyAllGroups()

def RemoveAllGroups():
	global theGroups
	
	theGroups.RemoveAllGroups()
	

def GetGroupsInArea( anArea ):
	global theGroups
	
	units = GetUnitsInAreaXZ( anArea.myPosition, anArea.myRadius )
	groups = []
	
	for unitId in units:
		grp = theGroups.GetGroupByUnit( unitId )
		if grp:
			groups.append( grp )
	
	return groups

def SpeedRPTrickle( ):
	wicg.SetApRegrowthRate( 1 )
	Delay( 2, Action( wicg.SetApRegrowthRate, 40 ) )


def AddAPToPlayer( anApAmount ):
	
	thePlayers[PLAYER_HUMAN].myMaxAP = thePlayers[PLAYER_HUMAN].myMaxAP + anApAmount
	thePlayers[PLAYER_HUMAN].myCurrentAP = thePlayers[PLAYER_HUMAN].myCurrentAP + anApAmount


def AddTAToPlayer( anTAAmount ):
	
	thePlayers[PLAYER_HUMAN].myMaxTacticalAid = thePlayers[PLAYER_HUMAN].myMaxTacticalAid + anTAAmount


def AddToSPReinforcement( aUnitType, aNrOfUnitsIfLimited = -1, anOverrideCost = -1 ):
	
	if not isinstance( aUnitType, str ):
		raise ValueError( 'unit type should be a string' )
	
	if aNrOfUnitsIfLimited > 0:
		rebate = 'REBATE_LIMITED'
	else:
		rebate = 'REBATE_REBATED'
		
	if anOverrideCost != -1:
		cost = anOverrideCost
	else:
		cost = unittypes.unitCosts[aUnitType]
	
	SetUnitCostForSPRole( aUnitType, cost, rebate )
	
	if aNrOfUnitsIfLimited != -1:
		SetUnitNumLimitedPurchasable( aUnitType, aNrOfUnitsIfLimited )


def AddDeploymentZoneToTeam( aDeploymentAreaMask, aTeam ):
	wicg.AddDeploymentZoneToTeam( aDeploymentAreaMask, aTeam )
	wicg.ForceNewDeploymentPosition( )			
	

def GetUnitCost( someUnitTypes ):
	cost = 0
	if isinstance( someUnitTypes, list ) or isinstance( someUnitTypes, tuple ):
		for unitType in someUnitTypes:
			cost += unittypes.unitCosts[unitType]
	else:
		cost = unittypes.unitCosts[someUnitTypes]
		
	return cost


def DifficultyLevelValue( aValue, aMediumModifier, aEasyModifier ):
	
	if wicg.GetDifficultyLevel() == EASY:
		return aValue + aEasyModifier
	elif wicg.GetDifficultyLevel() == NORMAL:
		return aValue + aMediumModifier
	elif wicg.GetDifficultyLevel() == HARD:
		return aValue


def RemoveSupportWeaponFromAllPlayers( taName ):
	
	for i in range( 16 ):
		RemoveSupportWeapon( i, taName )


def SetInMegamapFlag( aValue ):
	global inMegamap
	
	inMegamap = aValue


def DisableAllUnits( aFlag ):
	global enabledAIs
	
	if __debug__:
		debug.DebugMessage( 'serverimports::DisableAllUnits(%s)' % aFlag )
	
	## disable all AI:s
	if aFlag:
		enabledAIs = []
		
		for i in range( 16 ):
			if wicg.IsAIEnabled( i ):
				enabledAIs.append( i )
				wicg.EnableAI( i, False )
	##enable all AI:S
	else:
		for i in range( 16 ):
			if i in enabledAIs:
				wicg.EnableAI( i, True )

	
	wicg.DisableAllUnits( aFlag )


def MakeAllUnitsInvulnerable( aFlag = True ):
	
	for i in range( 512 ):
		try:
			unit.theUnits[i].myHealth
		except unit.UnknownUnitException:
			pass
		else:
			if unit.theUnits[i].myOwner == PLAYER_HUMAN:
				unit.theUnits[i].myInvulnerable = aFlag


def StartClientCamera( aClientFunctionAsString, *someArgs ):

	# make sure that the units is vulnerable when the camera ends	
	RE_OnCustomEventEx( ['END_OF_CUTSCENE', 'SKIP_CUTSCENE'], Action( MakeAllUnitsInvulnerable, False ), None, COMPLEX_TEST_OR, True )
		
	# make all units invulnerable
	MakeAllUnitsInvulnerable( True )
	
	# start the camera
	ClientCommand( aClientFunctionAsString, *someArgs )


## ----- AI -----

def DisableAllAIs():
	for i in range( 0, 16 ):
		try:
			wicg.IsScriptDebugOutputAIEnable( i )
		except Exception, e:
			continue
		
		wicg.EnableAI( i, False )


## ----- FORTIFICATIONS -----

def RemoveAllFortifications( aPerimeterPoint, aExplodeFlag = False ):
	
	try:
		RemoveFortification( aPerimeterPoint, 1, aExplodeFlag )
	except Exception:
		pass
	try:
		RemoveFortification( aPerimeterPoint, 2, aExplodeFlag )
	except Exception:
		pass
	try:
		RemoveFortification( aPerimeterPoint, 3, aExplodeFlag )
	except Exception:
		pass

def CheckIfFortified( aPerimeterPoint, aTeam ):

	if CheckFortificationLevel( aPerimeterPoint, 1, aTeam ):
		return True
	if CheckFortificationLevel( aPerimeterPoint, 2, aTeam ):
		return True
	if CheckFortificationLevel( aPerimeterPoint, 3, aTeam ):
		return True
 
	return False


## ----- MESSAGEBOX -----

def ShowMessageBox( aMessageboxName, aMessageBoxId = -1, aUnitId = -1, aWorldPos = Position(), aBlinkFlag = False ):
	global theMessageboxCounter
	
	if __debug__:
		debug.DebugMessage( 'ShowMessageBox - %s' % aMessageboxName )
	
	if aMessageBoxId == -1:
		theMessageboxCounter += 1
		messageBoxId = theMessageboxCounter
	else:
		messageBoxId = aMessageBoxId
	
	thePlayers[PLAYER_HUMAN].ShowMessageBox( aMessageboxName, messageBoxId, aUnitId, aWorldPos, aBlinkFlag )
	
	return messageBoxId


def HideMessageBox( aFadeTime = 0.0 ):
	
	thePlayers[PLAYER_HUMAN].HideMessageBox( aFadeTime )


def PushMessageBox( aMessageboxName, aMessageBoxId, aDelay = 0.0, aUnitId = -1, aWorldPos = Position(), aBlinkFlag = False ):
	global lastShownMessageBoxId
	
	if lastShownMessageBoxId == INVALID_MSG_BOX_ID:
		if aDelay == 0.0:
			ShowMessageBox( aMessageboxName, aMessageBoxId, aUnitId, aWorldPos, aBlinkFlag )
		else:
			Delay( aDelay, Action( ShowMessageBox, aMessageboxName, aMessageBoxId, aUnitId, aWorldPos, aBlinkFlag ) )
	else:
		if aDelay == 0.0:
			RE_OnMessageBoxClosed( lastShownMessageBoxId, Action( ShowMessageBox, aMessageboxName, aMessageBoxId, aUnitId, aWorldPos, aBlinkFlag ) )
		else:
			RE_OnMessageBoxClosed( lastShownMessageBoxId, Action( Delay, aDelay, Action( ShowMessageBox, aMessageboxName, aMessageBoxId, aUnitId, aWorldPos, aBlinkFlag ) ) )
			
	lastShownMessageBoxId = aMessageBoxId


## ----- CLIENT -----

def ClientCommand( aCommand, *someArgs ):
	thePlayers[1].ClientPythonCommand( aCommand, *someArgs )
	

## ----- OBJECTIVES -----

def AddObjective( aName, aTarget = -1, aType = 'primary', aTotalObjectiveCount = 0 ):
	thePlayers[1].AddObjective( aName, aTarget, aType, aTotalObjectiveCount )
	ClientCommand('FlashObjectivesButton')

def SetObjective( aName, aState, aType = 'primary' ):
	thePlayers[1].SetObjective( aName, aState, aType )

def UpdateObjective( aCurrentObjective, aTarget = -1, aType = 'primary', anObjectiveCounter = 0, aNewObjective = None ):
	thePlayers[1].UpdateObjective( aCurrentObjective, aTarget, aType, anObjectiveCounter, aNewObjective )


##map specific cinematics import
try:
	if IsSinglePlayer():
		import serverplay
except ImportError:
	pass



#------------------------------ Victory ---------------------------------------


# this overrides the native function EndGame, this is the global function beeing used when completing a mission
# only use this function for Victory!!!
def EndGame( aTeam, aPlayVictoryMusic = True ):
	global theReactions
	
	if __debug__:
		debug.DebugMessage( 'Victory! - serverimports::EndGame(%d)' % aTeam )
	
	if aPlayVictoryMusic:
		ClientCommand( 'PlayMusicEvent', 'Global_OnMissionCompleted' )
	
	ClientCommand( 'StartEndCamScript' )
	
	## no more reactions this frame or any other frame
	theReactions.DoEarlyOut()
	theReactions.Pause()
	
	wicg.EndGame( aTeam )

#------------------------------ Game Over ---------------------------------------

def GameOver( aObjective, aMessageboxList = [] ):
	global theReactions
	
	PurgeAllActionQueues( )
	PurgeMessageBoxQueue( 'all' )

	queGameOver = ActionQueue( 'GameOver' )
	if aObjective:
		queGameOver.AddFunction( aObjective.Failed )
	
	queGameOver.AddFunction( ClientCommand, 'PlayMusicEvent', 'Global_OnMissionFailed' )
	queGameOver.AddDelay( 3 )
	queGameOver.AddFunction( theGame.HideGUIChunk, 'reinforcements' )
	queGameOver.AddFunction( theGame.HideGUIChunk, 'support' )
	
	if len( aMessageboxList ) == 2:
		queGameOver.AddMessageBox( aMessageboxList[ 0 ], aMessageboxList[ 1 ] )
	
	if len( aMessageboxList ) == 4:
		queGameOver.AddMessageBox( aMessageboxList[ 0 ], aMessageboxList[ 1 ] )
		queGameOver.AddMessageBox( aMessageboxList[ 2 ], aMessageboxList[ 3 ] )
	
	if len( aMessageboxList ) == 6:
		queGameOver.AddMessageBox( aMessageboxList[ 0 ], aMessageboxList[ 1 ] )
		queGameOver.AddMessageBox( aMessageboxList[ 2 ], aMessageboxList[ 3 ] )
		queGameOver.AddMessageBox( aMessageboxList[ 4 ], aMessageboxList[ 5 ] )
		
	queGameOver.AddFunction( ClientCommand, 'StartEndCamScript' )
	
	## no more reactions this frame or any other frame
	queGameOver.AddFunction( theReactions.DoEarlyOut )
	queGameOver.AddFunction( theReactions.Pause )
	
	queGameOver.AddFunction( MissionFailed )
	queGameOver.Execute( )


def StartMaxUnitTracker( ):
	MaxUnitNumberList = []
	MaxUnitNumberList.append( 'MaxUnits: ' )
	MaxUnitNumberList.append( str(0) )
	MaxUnitNumberList.append( '\n' )
	MaxUnitNumberList.append( 'Time\tUnits\n' )
	RunMaxUnitNumberTracker( MaxUnitNumberList )


def RunMaxUnitNumberTracker( MaxUnitNumberList ):
	nrOfUnitsCounter = 0
	for i in range(512):
		try:
			unit.theUnits[i].myHealth
			nrOfUnitsCounter += 1
		except Exception:
			continue
	
	if nrOfUnitsCounter > int(MaxUnitNumberList[1]):
		MaxUnitNumberList[1] = str(nrOfUnitsCounter)
	
	newstring = '%-.3f\t%-d\n' % ( GetCurrentTime( ), nrOfUnitsCounter )
	filePath = 'maps\\_UnitCount_\\%s' % wicg.GetMapName()
	f = file( filePath + '_UnitCount.txt', 'w' )
	MaxUnitNumberList.append( newstring )
	f.writelines( MaxUnitNumberList )
	f.close( )
	Delay( 5, Action( RunMaxUnitNumberTracker, MaxUnitNumberList ) )


def ActionQueue( aName = 'Queue', aUseQueueSystemFlag = True ):
	global theExecutionQueue
	global theExpressList
	global theNameCounter
	
	if aName == 'Queue':
		aName = '%s%d' % ( aName, theNameCounter )
		theNameCounter += 1

	if aUseQueueSystemFlag:
		return wicgame.actionqueue.ActionQueue( theExecutionQueue, aName, aUseQueueSystemFlag )
	
	return wicgame.actionqueue.ActionQueue( theExpressList, aName, aUseQueueSystemFlag )


def PurgeAllActionQueues():
	global theExecutionQueue
	global theExpressList
	
	wicgame.actionqueue.PurgeActionQueues( theExecutionQueue )
	wicgame.actionqueue.PurgeActionQueues( theExpressList )


def SetCoreSystemState( aGuiChunk, aState ):
	global theGUIChunks
	
	wicg.SetCoreSystemState( aGuiChunk, aState )
	
	if aState == 'enabled':
		theGUIChunks[aGuiChunk] = True
	else:
		theGUIChunks[aGuiChunk] = False


def RestoreGUIState():
	global theGUIChunks

	for chunk in theGUIChunks:
		if theGUIChunks[chunk]:
			SetCoreSystemState( chunk, 'enabled' )
		else:
			SetCoreSystemState( chunk, 'hidden' )

def SetupShowPlayerDropZoneReaction():
	
	RE_OnDropZonePlaced( Action( ClientCommand, 'ShowPlayerDropZone' ) )


def SetUnitCostForSPRole( aUnitType, aCost, aRebate ):
	global theBuyMenu
	
	theBuyMenu[aUnitType] = [ aCost, aRebate, -1 ]
	
	wicg.SetUnitCostForSPRole( aUnitType, aCost, aRebate )
	
	if __debug__:
		debug.DebugMessage( "Added %s to the buy menu" % aUnitType, debug.NONE )


def SetUnitNumLimitedPurchasable( aUnitType, aNrOfUnitsIfLimited ):
	global theBuyMenu
	
	#theBuyMenu[aUnitType][2] = aNrOfUnitsIfLimited
	wicg.SetUnitNumLimitedPurchasable( aUnitType, aNrOfUnitsIfLimited )


def RestoreBuyMenu():
	global theBuyMenu
	
	if __debug__:
		debug.DebugMessage( "Restoring the buy menu", debug.NONE )

	for unitType in theBuyMenu:
		wicg.SetUnitCostForSPRole( unitType, theBuyMenu[unitType][0], theBuyMenu[unitType][1] )
		
		if theBuyMenu[unitType][2] != -1:
			wicg.SetUnitNumLimitedPurchasable( unitType, theBuyMenu[unitType][2] )
		
		if __debug__:
			debug.DebugMessage( "Readded %s to the buy menu" % unitType, debug.NONE )


def AddSupportWeapon( aPlayer, aSupportWeapon ):
	global theTAs
	
	wicg.AddSupportWeapon( aPlayer, aSupportWeapon, 1 )
	
	if not aPlayer in theTAs:
		theTAs[aPlayer] = []
	
	theTAs[aPlayer].append( aSupportWeapon )
	
	debug.DebugMessage( 'Adding TA "%s" to player #%d' % ( aSupportWeapon, aPlayer ), debug.NONE )


def RemoveSupportWeapon( aPlayer, aSupportWeapon ):
	global theTAs
	
	wicg.RemoveSupportWeapon( aPlayer, aSupportWeapon )
	
	if aPlayer in theTAs:
		if aSupportWeapon in theTAs[aPlayer]:
			theTAs[aPlayer].remove( aSupportWeapon )

	debug.DebugMessage( 'Removing TA "%s" from player #%d' % ( aSupportWeapon, aPlayer ), debug.NONE )


def ClearSupportWeapons( aPlayer ):
	global theTAs
	
	wicg.ClearSupportWeapons( aPlayer )
	
	theTAs[ aPlayer ] = []

	debug.DebugMessage( 'Purging TAs for player #%d' % ( aPlayer ), debug.NONE )


def RestoreTAs():
	global theTAs
	
	for player in theTAs:
		wicg.ClearSupportWeapons( player )
		for ta in theTAs[player]:
			# Bugfix: Added a delay so that the player dont have to wait for the recharge time after loading a game. DavidH 16/6
			Delay( 0.15, Action( wicg.AddSupportWeapon, player, ta, 1 ) )

	thePlayers[PLAYER_HUMAN].myTacticalAid = thePlayers[PLAYER_HUMAN].myTacticalAid # TA bugfix DavidH 9/6					
			
def RestoreAfterLoad():
	global theReactions, theTime
	
	RestoreGUIState()
	RestoreBuyMenu()	
	theReactions.AddTimeToTimers( wic.common.GetCurrentTime() - theTime )
	theReactions.Pause( False )
	RestoreTAs() # Bugfix: Run RestoreTAs after AddTimeToTimers so that the delay work. DavidH 16/6	
	
	## Update theGroups and remove units that dont exist any more. BugId 111. davidh 090205.
	global theGroups
	theGroups.ValidateAllGroupUnits( True ) 
	
	FadeIn( 4.0 )
	
	debug.DebugMessage( "RestoredAfterLoad", debug.NONE )

