import wicg
import unit
import debug
import base
import wicg_common as common
import group
import serverimports

from globals import *

class AIException( Exception ): pass
class BadAIZoneException( AIException ): pass


AI_SPECIAL_ABILITY_FACTOR_EASY 		= 100.0
AI_SPECIAL_ABILITY_FACTOR_NORMAL 	= 100.0
AI_SPECIAL_ABILITY_FACTOR_HARD 		= 100.0


class AI( object ):
	
	
	def __init__( self, anAIPlayerId ):
		
		self.__Id = anAIPlayerId
		self.__Groups = []
		self.__JoinGroup = None
		self.__CurrentCommand = 'NoCommand'
		self.__IsEnabled = False

		if wicg.GetDifficultyLevel() == EASY:
			wicg.SetAISpecialAbilityOffensiveFactor( self.__Id, 1.0 - (AI_SPECIAL_ABILITY_FACTOR_EASY / 100.0) )
		elif wicg.GetDifficultyLevel() == NORMAL:
			wicg.SetAISpecialAbilityOffensiveFactor( self.__Id, 1.0 - (AI_SPECIAL_ABILITY_FACTOR_NORMAL / 100.0) )
		elif wicg.GetDifficultyLevel() == HARD:
			wicg.SetAISpecialAbilityOffensiveFactor( self.__Id, 1.0 - (AI_SPECIAL_ABILITY_FACTOR_HARD / 100.0) )
		
	
	def __getId( self ):
		
		return self.__Id
		
	myId = property( __getId )
	

	def __getCurrentCommand( self ):
		
		return self.__CurrentCommand
		
	myCurrentCommand = property( __getCurrentCommand )


	def __getGroups( self ):
		
		return self.__Groups
		
	myGroups = property( __getGroups )


	def __getIsEnabled( self ):
		
		return self.__IsEnabled
		
	myIsEnabled = property( __getIsEnabled )

	
	def Enable( self ):
		""" Enables this AI player. If an AI player isnt enabled it wont issue any orders to its units.
		"""
		
		wicg.EnableAI( self.__Id, True )
		self.__IsEnabled = True
	
	
	def Disable( self ):
		
		wicg.EnableAI( self.__Id, False )
		self.__IsEnabled = False
		
	
	def IsEnabled( self ):
		
		return wicg.IsAIEnabled( self._Id )
	
	
	def SetJoinGroup( self, aGroup ):
		""" When calling RemoveAllUnits units that doesnt belong to a group will join this group (aGroup).
		"""
		
		self.__JoinGroup = aGroup

	
	def AddGroup( self, aGroup ):
		""" Adds a Group to this AI. The Group will automatically change owner (to the AI player) and be a passive Group.
		"""
		
		aGroup.SetOwner( self.__Id + 1 )
		aGroup.MakePassive()
		aGroup.SetAI( self )
		
		if not aGroup in self.__Groups:
			self.__Groups.append( aGroup )
	
	
	def RemoveAllUnits( self ):
		""" Remove all units from this AI. All groups in this AI will become active. All units will get the groups owner as new owner. 
		    Units that doesnt belong to any group will join the first group or a group specified with SetJoinGroup.
		"""
		
		aiUnits = wicg.ChangeUnitsOwner( self.__Id, PLAYER_SCRIPT )
		
		if aiUnits is None:
			return

		for grp in self.__Groups:
			grp.SetOwner( PLAYER_SCRIPT )
			grp.MakeActive()
			grp.SetAI( None )
		
		joinGrp = None
		
		if len( self.__Groups ):
			if self.__JoinGroup:
				joinGrp = self.__JoinGroup
			else:
				joinGrp = self.__Groups[0]

		if joinGrp:
			for unitId in aiUnits:
				if not serverimports.IsUnitGroupUnit( unitId ):
					joinGrp.AddUnitsById( [unitId] )
			joinGrp.UpdateOwner()
		
			for u in aiUnits:
				unit.theUnits[u].myTeam = joinGrp.myTeam
		
		self.__Groups = []
		
	
	def HideCommandPoint( self, aCommandPoint ):
		
		if not isinstance( aCommandPoint, str ):
			raise ValueError('HideCommandPoint(): Second argument must be a string')
	
		zone = base.StringToInt( aCommandPoint )
		wicg.HideAIZone( self.__Id, zone, True )
	
	
	def ShowCommandPoint( self, aCommandPoint ):
		
		if not isinstance( aCommandPoint, str ):
			raise ValueError('HideCommandPoint(): Second argument must be a string')

		zone = base.StringToInt( aCommandPoint )
		wicg.HideAIZone( self.__Id, zone, False)

	
	def HoldCommandPoint( self, aCommandPoint, aStance = AI_STANCE_DEFENSIVE ):
		""" The AI will move and take a command point close to aCommandPoint. aCommandPoint is just a Position. 
		If aCommandPoint isnt close to a perimeter point the AI will do a HoldZone order instead.
		"""
		
		cpCenterPos = common.GetPosition( aCommandPoint )
		wicg.HoldAICommandPointArea( self.__Id, cpCenterPos, aStance )
		self.__CurrentCommand = 'HoldCommandPoint(%s)' % aCommandPoint
		
		
	def HoldZone( self, aMoveZoneCenter, aMoveZoneRadius, someKillZones, aStance = AI_STANCE_DEFENSIVE ):
		
		if someKillZones is None:
			someKillZones = []
			
		if not len(someKillZones) and aMoveZoneCenter is None:
			raise BadAIZoneException( 'HoldZone(): Both move area and killzones are None' )
	
		moveZoneCenterPos = None
		
		if aMoveZoneCenter:
			moveZoneCenterPos = common.GetPosition( aMoveZoneCenter )
		
		wicg.HoldAIZone( self.__Id, moveZoneCenterPos, aMoveZoneRadius, someKillZones, aStance)
		self.__CurrentCommand = 'HoldZone'
	
	
	def HoldZoneLine( self, someMoveStripes, aWidth, someKillZones, aUseFlanking = False, aUseSpreadOut = False, aUseHeight = True, aStance = AI_STANCE_DEFENSIVE ):
		
		if someKillZones is None or len( someKillZones ) == 0:
			raise BadAIZoneException( 'HoldZoneLine(): You must specify at least one killzone.' )
		
		wicg.HoldAIZoneLine( self.__Id, someMoveStripes, aWidth, someKillZones, aUseFlanking, aUseSpreadOut, aUseHeight, aStance )
		self.__CurrentCommand = 'HoldZoneLine'
	
	
	def EnableBuy( self ):
		
		wicg.EnableAIBuy( self.__Id, True )
	
	
	def DisableBuy( self ):
		
		wicg.EnableAIBuy( self.__Id, False )
	
	
	def EnableTA( self ):
		
		wicg.EnableAITAUse( self.__Id, True )
	
	
	def DisableTA( self ):
		
		wicg.EnableAITAUse( self.__Id, False )
	
	
	def SetTAZones( self, someZones ):
		
		wicg.SetAITAZones( self.__Id, someZones )
		
	
	def DropTAUsingMeAsHost( self, taName, aPosition, aDirection ):
		
		## make sure the AI has enough TA points
		serverimports.thePlayers[self.__Id + 1].myTacticalAid = 500
		## add the TA to the AI player
		serverimports.AddSupportWeapon( self.__Id + 1, taName )
		
		try:
			wicg.DropTAUsingMeAsHost( self.__Id, base.StringToInt( taName ), aPosition, aDirection )
		except Exception:
			debug.DebugMessage( 'AI::DropTAUsingMeAsHost Failed to use TA (%s)' % taName )
	

	def SetArtilleryZones( self, someZones ):
		
		wicg.SetAIArtilleryZones( self.__Id, someZones )

	
	def EnableSpecialAbilities( self ):
		
		wicg.EnableAISpecialAbilities( self.__Id, True, True )
	
	
	def DisableSpecialAbilities( self ):
		
		wicg.EnableAISpecialAbilities( self.__Id, False, False )
		
		
	def SetSpecialAbilityOffensiveFactor( self, anOffensiveFactor ):
		
		wicg.SetAISpecialAbilityOffensiveFactor( self.__Id, anOffensiveFactor )
		
		
	def EnableInfantryEnterBuildings( self ):
		
		wicg.EnableAIInfantryEnterBuildings( self.__Id, True )
	
	
	def DisableInfantryEnterBuildings( self ):
		
		wicg.EnableAIInfantryEnterBuildings( self.__Id, False )
				
	
	def EnableDebugOutput( self ):
		
		if not wicg.IsScriptDebugOutputAIEnable( self.__Id ):
			wicg.ScriptDebugOutputAIEnable( self.__Id )


	def DisableDebugOutput( self ):
		
		if wicg.IsScriptDebugOutputAIEnable( self.__Id ):
			wicg.ScriptDebugOutputAIDisable( self.__Id )
	
	
	def ToggleDebugOutput( self ):
		
		if wicg.IsScriptDebugOutputAIEnable( self.__Id ):
			wicg.ScriptDebugOutputAIDisable( self.__Id )
		else:
			wicg.ScriptDebugOutputAIEnable( self.__Id )


	def IsDebugOutputEnabled( self ):
		
		return wicg.IsScriptDebugOutputAIEnable( self.__Id )


	def DisableBlockForArtillery( self ):
  
		wicg.SetShouldBlockForIncomingArtillery( self.__Id, False )
 
 
	def EnableBlockForArtillery( self ):
  
		wicg.SetShouldBlockForIncomingArtillery( self.__Id, True )
		
