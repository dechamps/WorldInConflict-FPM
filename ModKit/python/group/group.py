import wicg
import wicg_common as common
import debug
import unit
import instance
import base

## group imports
from globals import *
import behavior
import command

import serverimports

## math imports
import random
import math
from wicmath import wicmath
from position import Position
from wicmath.vector import Vector


class GroupException( Exception ): pass
class UnknownGroupException( GroupException ): pass
class CreateUnitException( GroupException ): pass
class EmptyGroupException( GroupException ): pass
class NoneGroupException( GroupException ): pass
class SquadSizeException( GroupException ): pass
class GroupNameException( GroupException ): pass
class GroupToBigException( GroupException ): pass



class Groups (object):
	""" A manager class that handles multiple Groups
	"""

	__GroupCounter = 0
	__SpawnCounter = 0

	def __init__( self ):

		self.__Groups = {}
		self.__GroupCounter = 0
		self.__SpawnCounter = 0
		self.__UpdateList = []
		self.__CurrentUpdateIndex = 0
		self.__UpdateCounter = 0

		self.__UpdateNrGroups = UPDATE_NR_GROUPS
		
		self.__LastAverageUpdateTime = 0.0
		self.__UpdateAverage = 0.0
		self.__CurrentUpdateAverage = 0.0


	@classmethod
	def GetCounter( groups ):
		
		groups.__GroupCounter += 1
		return groups.__GroupCounter

	@classmethod
	def GetNextUniqueSpawnKey( groups ):
		groups.__SpawnCounter += 1
		return groups.__SpawnCounter

	@classmethod
	def PeekCounter( groups ):
		
		return groups.__GroupCounter
	
		
	def __getGroups( self ):
		
		return self.__Groups
		
	myGroups = property( __getGroups )

	
	def GetAverageUpdateDelay( self, aUpdateTime = 0.0 ):
		
		if len( self.__Groups.values() ) == 0:
			return self.__CurrentUpdateAverage

		average = 0.0
		for grp in self.__Groups.values():
			average += grp.GetUpdateDelay()
		
		average /= len( self.__Groups.values() )
		self.__UpdateAverage += average
		self.__UpdateAverage /= 2
		
		if (self.__LastAverageUpdateTime + aUpdateTime) < serverimports.GetCurrentTime():
			self.__CurrentUpdateAverage = self.__UpdateAverage
			self.__LastAverageUpdateTime = serverimports.GetCurrentTime()
			
		return self.__CurrentUpdateAverage
	
	
	def GetLastUpdateAverage( self ):
		
		if len( self.__Groups.values() ) == 0:
			return 0.0
		
		average = 0.0
		for grp in self.__Groups.values():
			average += grp.GetUpdateDelay()
		
		average /= len( self.__Groups.values() )
		
		return average
		
		

	def Update( self ):
		
		if len( self.__Groups ) == 0:
			return
		
		totalUpdateCost = 0
		
		while totalUpdateCost < MAX_GROUP_UPDATE_COST:
			if self.__CurrentUpdateIndex >= len( self.__Groups ):
				self.__CurrentUpdateIndex = 0
			
			currGroup = self.__Groups.values()[self.__CurrentUpdateIndex]
			
			if currGroup:
				totalUpdateCost += currGroup.Update()
			else:
				totalUpdateCost += GROUP_UPDATE_COST_LOW
			
			self.__CurrentUpdateIndex += 1


	def AddGroup( self, aGroup, aGroupName = None ):
		""" Adds a new group
		"""
		
		self.__GroupCounter += 1

		if aGroupName is None:
			aGroupName = 'Group%d' % ( self.__GroupCounter )

		aGroup.myName = aGroupName
		
		## if its already added it could be a hash collision
		if aGroupName in self.__Groups:
			raise GroupNameException( 'Bad Group name (%s)! Group already added or hash collision. Try different groupname.' % aGroupName )
		
		self.__Groups[aGroupName] = aGroup
		
		if __debug__:
			debug.DebugMessage( 'Groups::AddGroup - A group was added to theGroups %s' % aGroupName )

		return aGroup


	def RemoveGroup( self, aGroup ):
		""" Removes a group

		Args:
		 aGroup - (Group) The group to remove

		Returns:
		 Nothing
		"""
		
		if aGroup is None:
			debug.DebugMessage( 'Groups::RemoveGroup Warning! Trying to remove group of type None.', debug.NONE )
			return
		
		if isinstance( aGroup, str ):
			try:
				del self.__Groups[aGroup]
				return
			except KeyError:
				debug.DebugMessage( 'Groups::RemoveGroup(%s) Warning! Group already removed or never added' % aGroup, debug.NONE )
		elif isinstance( aGroup, Group ):
			for key in self.__Groups:
				if self.__Groups[key] == aGroup:
					del self.__Groups[key]
					return
			debug.DebugMessage( 'Groups::RemoveGroup(%s) Warning! Group already removed or never added' % aGroup, debug.NONE )

		debug.DebugMessage( 'Groups::RemoveGroup Warning! Trying to remove a none-group object from Groups', debug.NONE )

	
	def RemoveAllGroups( self ):
		self.__Groups.clear()


	def DestroyAllGroups( self ):
		
		for grp in self.__Groups.values():
			grp.DeactivateRefillMode( True )
		for grp in self.__Groups.values():
			grp.DestroyGroup()


	def DestroyUnitById( self, aUnitId, aShouldExplode = 0 ):
		
		if not isinstance( aUnitId, int ):
			raise TypeError( 'DestroyUnitById failed. An integer is required as unit id.' )
		
		try:
			unit.theUnits[ aUnitId ]
		except unit.UnknownUnitException:
			return False
		
		for grp in self.__Groups.values():
			if grp.IsUnitInGroup( aUnitId ):
				grp.DestroyUnitById( aUnitId, aShouldExplode )
				return True
		return False

	
	def RemoveUnitById( self, aUnitId ):
		
		if not isinstance( aUnitId, int ):
			raise TypeError( 'RemoveUnitById failed. An integer is required.' )
		
		for grp in self.__Groups.values():
			if grp.IsUnitInGroup( aUnitId ):
				grp.RemoveUnitById( aUnitId )
				return True
		return False
	
	
	def IsGroup( self, aGroup ):
		
		return (aGroup in self.__Groups.values())
	

	def IsGroupByName( self, aGroupName ):
		
		return (aGroupName in self.__Groups)

	
	def ValidateAllGroupUnits( self, aUpdateGroups = False ):
		
		debug.DebugMessage( 'ValidateAllGroupUnits' )
		
		allOk = True
		
		## validate and fix all units
		for grp in self.__Groups.values()[:]:
			allOk = grp.ValidateUnits( aUpdateGroups )
			
		## update all refills
		if aUpdateGroups:
			for grp in self.__Groups.values()[:]:
				grp.TestForRefill()
			
		return allOk
		
	
	def SetUpdateNrGroups( self, aUpdateNrGroups ):
		
		self.__UpdateNrGroups = aUpdateNrGroups


	def GetGroupByUnit( self, aUnitId ):

		for i in self.__Groups.values():
			if i.IsUnitInGroup( aUnitId ):
				return i

		return None


	def GetNameByUnit( self, aUnitId ):
		
		g = self.GetGroupByUnit(aUnitId)

		for i in self.__Groups.keys():
			if self.__Groups[i] is g:
				return i

		return None


	def GetCurrentNumberOfGroups( self ):
		
		return len(self)


	def GetCurrentNumberOfRefillerGroups( self ):
		
		totalNr = 0
		for grp in self.__Groups.values():
			if grp.CheckState( 'RefillGroup' ):
				totalNr += 1
		
		return totalNr
		

	def GetCurrentNumberOfUnits( self ):
		
		totalNr = 0
		for grp in self.__Groups.values():
			totalNr += grp.Size()
		
		return totalNr		
	
	
	def CancelAllAirDrops( self ):
	
		for grp in self.__Groups.values():
			grp.CancelAirDrops()
	

	def CancelAllSquadReactions( self ):
	
		for grp in self.__Groups.values():
			grp.CancelSquadReactions()

	
	def __getitem__( self, aKey ):
		
		return self.__Groups[aKey]


	def __len__( self ):
		
		return self.__Groups.__len__()


class GroupUnit( object ):
	"""
	"""
	
	def __init__( self, aUnitId ):
		
		self.__UnitId = aUnitId
		self.__TargetPos = None
		self.__TargetHeading = 0.0
		self.__TargetSpeed = 0.0
		self.__DestroyedReaction = None
		self.__InCombatReaction = None
		
		self.__Active = True
	
	
	def __del__( self ):
		
		self.Shutdown( None )


	def __str__( self ):

		return ("%d" % self.__UnitId)


	def __pos__( self ):

		x = unit.theUnits[self.__UnitId].myPos.myX
		y = unit.theUnits[self.__UnitId].myPos.myY
		z = unit.theUnits[self.__UnitId].myPos.myZ
		return Position(x, y, z)


	def __getUnit( self ):

		return unit.theUnits[self.__UnitId]

	myUnit = property( __getUnit )


	def __getUnitId( self ):

		return self.__UnitId

	myUnitId = property( __getUnitId )


	def __getTargetPos( self ):

		return self.__TargetPos

	def __setTargetPos( self, aTargetPos ):

		self.__TargetPos = Position(aTargetPos.myX, aTargetPos.myY, aTargetPos.myZ)

	myTargetPos = property( __getTargetPos, __setTargetPos )


	def __getPos( self ):

		unit_pos = Position()
		unit_pos.myX = self.myUnit.myPos.myX
		unit_pos.myY = self.myUnit.myPos.myY
		unit_pos.myZ = self.myUnit.myPos.myZ

		return unit_pos


	myPos = property( __getPos )

	
	def __getTargetHeading( self ):
		
		return self.__TargetHeading
	
	
	def __setTargetHeading( self, aTargetHeading ):
		
		self.__TargetHeading = aTargetHeading

	myTargetHeading = property( __getTargetHeading, __setTargetHeading )
	
	
	def __getTargetSpeed( self ):
		
		return self.__TargetSpeed
	
	
	def __setTargetSpeed( self, aTargetSpeed ):
		
		self.__TargetSpeed = aTargetSpeed
	
	myTargetSpeed = property( __getTargetSpeed, __setTargetSpeed )
	
	
	def GetTargetPosition( self, aGroup ):
				
		if aGroup.IsTransporterGroup():
			containerId = wicg.GetContainerId( self.__UnitId )
			
			if containerId != -1:
				containerUnit = aGroup.GetUnitById( containerId )
				
				if containerUnit is None:
					debug.DebugMessage( 'GroupUnit::GetTargetPosition Warning! Bad use of TransporterGroup. Container and passenger not in same Group ', debug.NONE )
					return self.__TargetPos
				else:
					return containerUnit.myTargetPos
			else:
				return self.__TargetPos

		else:
			return self.__TargetPos
	
	
	def Reset( self, aGroup ):
		
		self.__TargetPos = unit.theUnits[self.__UnitId].myPos
		self.__TargetHeading = unit.theUnits[self.__UnitId].myHeading
		self.__TargetSpeed = unit.theUnits[self.__UnitId].myMaxSpeed
		
		self.__DestroyedReaction = serverimports.RE_OnUnitDestroyed( self.__UnitId, serverimports.Action( aGroup.OnUnitDestroyed, self ) )
		
		if not aGroup.IsPassive():
			self.__Active = True
			self.__InCombatReaction = serverimports.RE_OnUnitInCombat( self.__UnitId, serverimports.Action( aGroup.OnInCombat, self ) )
			self.__InCombatReaction.myRepeating = True
			wicg.TrackUnit( self.__UnitId )
		else:
			self.__Active = False

		
	def Shutdown( self, aGroup ):
		
		if self.__DestroyedReaction:
			serverimports.RemoveReaction( self.__DestroyedReaction )
			self.__DestroyedReaction = None
			
		if self.__InCombatReaction:
			serverimports.RemoveReaction( self.__InCombatReaction )
			self.__InCombatReaction = None

			
	def MakePassive( self ):
		
		if not self.__Active:
			return
		
		self.__Active = False
		
		if self.__InCombatReaction:
			serverimports.RemoveReaction( self.__InCombatReaction )
			self.__InCombatReaction = None


	def MakeActive( self, aGroup ):
		
		if self.__Active:
			return
		
		self.__Active = True
		
		if self.__InCombatReaction:
			serverimports.RemoveReaction( self.__InCombatReaction )
			self.__InCombatReaction = None

		self.__InCombatReaction = serverimports.RE_OnUnitInCombat( self.__UnitId, serverimports.Action( aGroup.OnInCombat, self ) )
		self.__InCombatReaction.myRepeating = True
		wicg.TrackUnit( self.__UnitId )



class Group( object ):


	def __init__( self, aUnits = [], aTarget = None, aOwner = 0, aTeam = 0 ):
		
		self.__Units = []

		self.__Name = 'NoName'
		
		self.__Id = Groups.GetCounter()

		self.__Owner = aOwner
		self.__Team = aTeam

		self.__Formation = FORMATION_LINE
		self.__FormationDistance = DEFAULT_FORMATION_DISTANCE
		self.__FormationOffset = 0.0
		self.__FormationWidthOffset = 0.0
		
		self.__UnifiedSpeed = False
		self.__HoldFire = False
		self.__Speed = -1
		self.__State = 'NoState'
		self.__UseSquadCreation = True
		self.__IsPassive = False
		
		self.__UseAirDrop = False
		self.__AirDropReactions = []
		self.__NrUnitsInAir = 0
		
		self.__SquadReactions = []
		
		self.__IsTransporter = False

		self.__PrimaryCommands = []
		self.__AttackCommands = []
		self.__BaseCommands = []
		
		self.__LastExecutedCommandType = None

		self.__BehaviorManager = behavior.BehaviorManager( self )
		self.SetAttackBehavior( behavior.BHA_Fearless() )

		self.__CombatExceptionGroups = []

		self.__RefillMode = False
		self.__RefillLimit = 0
		self.__RefillAmount = 0
		self.__RefillUnits = []
		self.__RefillCounter = 0
		self.__RefillSpawnTarget = None
		self.__RefillMoveTarget = None
		self.__RefillMoveRadius = None
		self.__RefillLastLeaderPos = None
		self.__RefillDelay = 0.0
		self.__RefillPendingRefill = False
		self.__RefillPendingReaction = None
		self.__RefillGroups = []
		self.__RefillCommandQueue = []
				
		self.__ParentGroup = None
		
		self.__Platoons = []
		
		self.__AI = None
		
		self.__LastUpdate = 0.0
		self.__LastUpdateDelay = 0.0
		
		self.__NrOfBadMoveOrdersThisUpdate = 0
		
		self.__DropShipDirection = Position( -1, -1, -1 )
		
		if len( aUnits ):
			self.CreateGroup( aUnits, aTarget, aOwner, aTeam )
	
	
	def __del__( self ):
		
		self.Purge()

	def __str__( self ):

		return self.__Name


	def __pos__( self ):
		
		return self.GetPosition()
		

	def Purge( self, aDestroyUnits = False ):
		
		self.DeactivateRefillMode( True )

		if self.__BehaviorManager:
			self.__BehaviorManager.Shutdown( )
			self.__BehaviorManager = None
			
		self.__BehaviorManager = behavior.BehaviorManager( self )
		self.SetAttackBehavior( behavior.BHA_Fearless() )
		
		self.__CombatExceptionGroups = []
		
		self.__ParentGroup = None
		
		if aDestroyUnits:
			self.DestroyGroup()
			
		self.ClearCommands( CMD_PRIMARY )
		self.ClearCommands( CMD_BASE )
		self.ClearCommands( CMD_ATTACK )
		

	def Update( self ):

		## used for debug purposes only
		if __debug__:
			self.__LastUpdateDelay = serverimports.GetCurrentTime() - self.__LastUpdate
			self.__LastUpdate = self.__LastUpdate + self.__LastUpdateDelay
		
		self.__NrOfBadMoveOrdersThisUpdate = 0

		if self.__IsPassive:
			return GROUP_UPDATE_COST_LOW

		activeCommandList = None

		if len( self.__AttackCommands ):
			activeCommandList = self.__AttackCommands
			self.RestartCommand( CMD_PRIMARY )
			self.ClearCommands( CMD_BASE )
			self.__LastExecutedCommandType = CMD_ATTACK
		elif len( self.__PrimaryCommands ):
			activeCommandList = self.__PrimaryCommands
			self.ClearCommands( CMD_BASE )
			self.__LastExecutedCommandType = CMD_PRIMARY
		elif len( self.__BaseCommands ):
			activeCommandList = self.__BaseCommands
			self.__LastExecutedCommandType = CMD_BASE

		if activeCommandList:
			commandCost = 0.0
			currCommand = activeCommandList[0]

			if not currCommand.IsActive():
				commandCost += currCommand.Start()

			commandCost += currCommand.Update()

			if currCommand.IsDone():
				activeCommandList.pop( activeCommandList.index( currCommand ) )
			
			self.__NrOfBadMoveOrdersThisUpdate = 0
			
			return commandCost
		else:
			return GROUP_UPDATE_COST_LOW


	def __getId( self ):

		return self.__Id

	myId = property( __getId )
	
	
	def __getOwner( self ):

		return self.__Owner

	myOwner = property( __getOwner )


	def __getTeam( self ):

		return self.__Team

	myTeam = property( __getTeam )


	def __getUnits( self ):

		return self.__Units

	myUnits = property( __getUnits )


	def __getParentGroup( self ):

		return self.__ParentGroup

	myParentGroup = property( __getParentGroup )

	def __getRefillGroups( self ):
		
		return self.__RefillGroups
		
	myRefillGroups = property( __getRefillGroups )


	def __getName( self ):
		"""
		"""
		
		return self.__Name


	def __setName( self, aName ):
		"""
		"""
		
		self.__Name = aName

	myName = property( __getName, __setName )
	

	def __getBehaviorManager( self ):
		"""
		"""

		return self.__BehaviorManager

	myBehaviorManager = property( __getBehaviorManager )
	
	
	def __getRefillMode( self ):

		return self.__RefillMode

	myRefillMode = property( __getRefillMode )


	def __getPlatoons( self ):

		return self.__Platoons

	myPlatoons = property( __getPlatoons )


	def GetUpdateDelay( self ):
		
		return self.__LastUpdateDelay


	def GetLastExecutedCommandType( self ):
		return self.__LastExecutedCommandType


	def SetFormation( self, aFormation, aDistance = DEFAULT_FORMATION_DISTANCE ):

		self.__Formation = aFormation
		self.__FormationDistance = aDistance

	def SetFormationEx( self, aFormation, aDistance = DEFAULT_FORMATION_DISTANCE, anOffset = 3, anWidthOffset = 2 ):

		self.__Formation = aFormation
		self.__FormationDistance = aDistance
		self.__FormationOffset = anOffset
		self.__FormationWidthOffset = anWidthOffset
	
	def SetFormationOffset( self, anOffset ):
		
		self.__FormationOffset = anOffset

	
	def SetFormationWidthOffset( self, anOffset ):
		
		self.__FormationWidthOffset = anOffset

	
	def CalculateOffsetPositions( self, somePositions, aDirection, anOffset ):
				
		c = 0
		for p in somePositions:
			offset = random.uniform( -anOffset, anOffset )
			p = p + (aDirection * offset)
			somePositions[c] = p
			c += 1
		
	
	def GetFormation( self ):

		return self.__Formation


	def GetFormationDistance( self ):

		return self.__FormationDistance


	def GetAI( self ):
		
		return self.__AI


	def SetAI( self, anAI ):
		
		self.__AI = anAI


	def SetSquadCreation( self, aSquadCreation ):
		
		self.__UseSquadCreation = aSquadCreation

		
	def SetUseAirDrop( self, aUseAirDrop, aDirection = None ):
		
		self.__UseAirDrop = aUseAirDrop
		
		if aDirection:
			self.SetDropshipDirection( aDirection )
		

	
	def GetNrUnitsInAir( self ):
		
		return self.__NrUnitsInAir

	
	def SetUnifiedSpeed( self, aUnifiedSpeed ):

		self.__UnifiedSpeed = aUnifiedSpeed


	def SetOwner( self, aNewOwner ):

		self.__Owner = aNewOwner

		for groupUnit in self.__Units:
			if groupUnit.myUnit.myOwner == serverimports.PLAYER_SCRIPT:
				groupUnit.myUnit.myOwner = aNewOwner


	def SetTeam( self, aNewTeam ):

		self.__Team = aNewTeam

		for groupUnit in self.__Units:
			if groupUnit.myUnit.myOwner == serverimports.PLAYER_SCRIPT:
				groupUnit.myUnit.myTeam = aNewTeam


	def UpdateOwner( self ):

		for groupUnit in self.__Units:
			if groupUnit.myUnit.myOwner == serverimports.PLAYER_SCRIPT:
				groupUnit.myUnit.myOwner = self.__Owner
	
	
	def UpdateTeam( self ):

		for groupUnit in self.__Units:
			if groupUnit.myUnit.myOwner == serverimports.PLAYER_SCRIPT:
				groupUnit.myUnit.myTeam = self.__Team
	
	
	def SetGroupApOwner( self, anOwner ):
		
		for groupUnit in self.__Units:
			wicg.SetUnitApOwner( groupUnit.myUnitId, anOwner )

	
	def UpdateGroupApOwner( self ):

		for groupUnit in self.__Units:
			wicg.SetUnitApOwner( groupUnit.myUnitId, self.__Owner )
	
	
	def SetHealth( self, aNewHealth ):

		for groupUnit in self.__Units:
			groupUnit.myUnit.SetHealth( aNewHealth )
		

	def SetHealthByScale( self, aHealthScale ):

		for groupUnit in self.__Units:
			curHealth = groupUnit.myUnit.myHealth
			curHealth = curHealth * aHealthScale
			groupUnit.myUnit.ChangeHealth( -int( curHealth ) )
		
		
	def SetRandomHealth( self, aMinHealth, aMaxHealth ):

		for groupUnit in self.__Units:
			curHealth = groupUnit.myUnit.myHealth
			curHealth = curHealth * random.uniform( aMinHealth, aMaxHealth )
			groupUnit.myUnit.ChangeHealth( -int(curHealth) )

	
	def SetInvulnerable( self, anInvulnerableFlag ):
		
		for groupUnit in self.__Units:
			groupUnit.myUnit.myInvulnerable = anInvulnerableFlag
	
	
	def Size( self, aCountRefillUnits = False ):

		refill_units = 0
		
		if aCountRefillUnits:
			for grp in self.__RefillGroups:
				refill_units += grp.Size( aCountRefillUnits )
			
			## units in air, we need to count them when testing for a refill
			refill_units += self.__NrUnitsInAir

		return len( self.__Units ) + refill_units


	def GetLeader( self ):

		if self.IsEmpty():
			return None
		
		return self.__Units[0]


	def GetUnitById( self, aUnitId ):

		if self.IsEmpty():
			return None
		
		for u in self.__Units:
			if u.myUnitId == aUnitId:
				return u
		return None


	def GetPosition( self ):

		if self.IsEmpty():
			raise EmptyGroupException( 'Empty group has no position %s' % self.__Name )
		
		leader = self.GetLeader()
		return leader.myUnit.myPos


	def GetHeading( self ):

		if self.IsEmpty():
			return None
		
		leader = self.GetLeader()
		return leader.myUnit.myHeading

	
	def GetGroupHealth( self ):
		'''Returns the total health of all units in the group'''
		
		GroupTotalHealth = 0
		for u in self.myUnits:
			GroupTotalHealth += u.myUnit.myHealth

		return GroupTotalHealth
	
	
	def SetSpeed( self, aNewSpeed ):

		self.__Speed = aNewSpeed


	def RestoreSpeed( self ):

		self.__Speed = -1


	def GetSpeed( self ):

		speed = self.__Speed

		if self.__UnifiedSpeed:

			if self.__Speed == -1:
				speed = 999

			for groupUnit in self.__Units:
				if groupUnit.myUnit.myMaxSpeed < speed:
					speed = groupUnit.myUnit.myMaxSpeed
		else:
			if self.__Speed != -1:
				return self.__Speed
			else:
				for groupUnit in self.__Units:
					if groupUnit.myUnit.myMaxSpeed > speed:
						speed = groupUnit.myUnit.myMaxSpeed

		return speed


	def SetAttackBehavior( self, aBehavior ):

		if isinstance( aBehavior, behavior.AttackBehavior ):
			self.__BehaviorManager.ActivateAttackBehavior( aBehavior )
			self.TrackGroup()
		else:
			raise TypeError( 'SetAttackBehavior requires an AttackBehavior, was given a %s. %s' % (type( aBehavior ), self ) )


	def SetBaseBehavior( self, aBehavior ):

		if isinstance( aBehavior, behavior.BaseBehavior ):
			self.__BehaviorManager.ActivateBaseBehavior( aBehavior )
		else:
			raise TypeError( 'SetBaseBehavior requires a BaseBehavior, was given a %s. %s' % (type( aBehavior ), self ) )


	def AddPlatoon( self, aPlatoon ):
		self.__Platoons.append( aPlatoon )
	
	
	def RemovePlatoon( self, aPlatoon ):
		
		if aPlatoon in self.__Platoons:
			self.__Platoons.remove( aPlatoon )


	def UpdatePlatoonSize( self ):
		
		for plt in self.__Platoons:
			plt.OnSize()
		

	def SetState( self, aState ):

		self.__State = aState


	def GetState( self ):

		return self.__State


	def CheckState( self, aState ):

		return (self.__State == aState)


	def IsPassive( self ):

		return self.__IsPassive


	def IsTransporterGroup( self ):

		return self.__IsTransporter


	def IsEmpty( self ):

		return (not len(self.__Units))


	def IsUnitInGroup( self, aUnitId ):
		
		for groupUnit in self.__Units:
			if aUnitId == groupUnit.myUnitId:
				return True
		return False
		
	
	def IsUnitInCombatExceptionGroup( self, aUnitId ):

		for grp in self.__CombatExceptionGroups:
			if grp.IsUnitInGroup(aUnitId):
				return True
		return False


	def IsCloseTo(self, aTarget, aLimit = CLOSE_TO_LIMIT):

		if self.IsEmpty():
			return True
		
		try:
			targetPos = common.GetPosition( aTarget )
		except EmptyGroupException:
			debug.DebugMessage( 'Group(%s)::IsCloseTo Failed! Invalid Target EmptyGroup(%s)' % (self.__Name, aTarget), debug.NONE )
			return True
		except unit.UnknownUnitException:
			debug.DebugMessage( 'Group(%s)::IsCloseTo Failed! Invalid Target (Unit)' % (self.__Name, aTarget), debug.NONE )
			return True
			

		for groupUnit in self.__Units:
			distance = wicmath.Distance( groupUnit.myUnit.myPos, targetPos )
			if (distance < aLimit):
				return True
		return False


	def IsUnitCloseTo( self, aIndex, aTarget, aLimit = CLOSE_TO_LIMIT ):

		if self.IsEmpty():
			return True

		try:
			targetPos = common.GetPosition( aTarget )
		except EmptyGroupException:
			debug.DebugMessage( 'Group(%s)::IsUnitCloseTo Failed! Invalid Target EmptyGroup(%s)' % (self.__Name, aTarget), debug.NONE )
			return True
		except unit.UnknownUnitException:
			debug.DebugMessage( 'Group(%s)::IsUnitCloseTo Failed! Invalid Target Unit(%d)' % (self.__Name, aTarget), debug.NONE )
			return True

		groupUnit = self.__Units[aIndex]

		distance = wicmath.Distance( groupUnit.myUnit.myPos, targetPos )

		if (distance < aLimit):
			return True

		return False


	def IsAllCloseTo( self, aTarget, aLimit = CLOSE_TO_LIMIT ):

		try:
			targetPos = common.GetPosition( aTarget )
		except EmptyGroupException:
			debug.DebugMessage( 'Group(%s)::IsUnitCloseTo Failed! Invalid Target EmptyGroup(%s)' % (self.__Name, aTarget), debug.NONE )
			return True
		except unit.UnknownUnitException:
			debug.DebugMessage( 'Group(%s)::IsUnitCloseTo Failed! Invalid Target Unit(%d)' % (self.__Name, aTarget), debug.NONE )
			return True

		for groupUnit in self.__Units:
			distance = wicmath.Distance( groupUnit.myUnit.myPos, targetPos )
			if (distance > aLimit):
				return False
		return True


	def IsSubgroupCloseTo( self, aStartIndex, aStopIndex, aTarget, aLimit = CLOSE_TO_LIMIT ):
				
		try:
			targetPos = common.GetPosition( aTarget )
		except EmptyGroupException:
			debug.DebugMessage( 'Group(%s)::IsSubgroupCloseTo Failed! Invalid Target EmptyGroup(%s)' % (self.__Name, aTarget), debug.NONE )
			return True
		except unit.UnknownUnitException:
			debug.DebugMessage( 'Group(%s)::IsSubgroupCloseTo Failed! Invalid Target Unit(%d)' % (self.__Name, aTarget), debug.NONE )
			return True

		if aStartIndex < 0 or aStopIndex >= self.Size() or aStartIndex > aStopIndex:
			return False

		for groupUnit in self.__Units[aStartIndex:(aStopIndex + 1)]:
			distance = wicmath.Distance( groupUnit.myUnit.myPos, targetPos )
			if (distance > aLimit):
				return False
		return True

		
	def IsMultipleUnitsCloseTo( self, someUnits, aTarget, aLimit = CLOSE_TO_LIMIT ):
				
		try:
			targetPos = common.GetPosition( aTarget )
		except EmptyGroupException:
			debug.DebugMessage( 'Group(%s)::IsMultipleUnitsCloseTo Failed! Invalid Target EmptyGroup(%s)' % (self.__Name, aTarget), debug.NONE )
			return True
		except unit.UnknownUnitException:
			debug.DebugMessage( 'Group(%s)::IsMultipleUnitsCloseTo Failed! Invalid Target Unit(%d)' % (self.__Name, aTarget), debug.NONE )
			return True

		for groupUnit in someUnits:
			distance = wicmath.Distance( groupUnit.myUnit.myPos, targetPos )
			if (distance > aLimit):
				return False
		return True
		

	def IsAtTarget( self, aLimit = CLOSE_TO_LIMIT ):

		if self.IsEmpty():
			return True

		for groupUnit in self.__Units:
			distance = wicmath.Distance( groupUnit.myUnit.myPos, groupUnit.GetTargetPosition( self ) )
			if (distance < aLimit):
				return True
		return False


	def IsLeaderAtTarget( self, aLimit = CLOSE_TO_LIMIT ):

		if self.IsEmpty():
			return True

		distance = wicmath.Distance( self.GetPosition(), self.GetLeader().GetTargetPosition( self ) )
		
		if (distance < aLimit):
			return True
		return False


	def IsUnitAtTarget( self, aIndex, aLimit = CLOSE_TO_LIMIT ):

		if self.IsEmpty():
			return True

		groupUnit = self.__Units[aIndex]

		distance = wicmath.Distance( groupUnit.myUnit.myPos, groupUnit.GetTargetPosition( self ) )
		
		if (distance < aLimit):
			return True
		return False


	def IsAllAtTarget( self, aLimit = CLOSE_TO_LIMIT ):

		if self.IsEmpty():
			return True

		for groupUnit in self.__Units:
			distance = wicmath.Distance( groupUnit.myUnit.myPos, groupUnit.GetTargetPosition( self ) )
			if (distance > aLimit):
				return False
		return True


	def CreateGroup( self, aUnits, aTarget, aOwner, aTeam ):

		if not self.IsEmpty():
			return

		self.__Owner = aOwner
		self.__Team = aTeam
		self.CreateUnitsAtPosition( aUnits, aTarget, aOwner, aTeam, NO_SQUAD_ID, self.__UseAirDrop )


	def CreateUnits( self, aUnits ):

		if self.IsEmpty():
			return

		pos = self.GetPosition()
		owner = self.GetLeader().myUnit.myOwner
		team = self.GetLeader().myUnit.myTeam
		self.CreateUnitsAtPosition( aUnits, pos, owner, team, NO_SQUAD_ID, self.__UseAirDrop )


	def CreateUnitFromInstance( self, anInstance ):
		
		returnInstance = instance.theInstances[anInstance]
		newUnitId = wicg.CreateUnit( base.StringToInt( returnInstance.myType ), returnInstance.myPos, returnInstance.myOri.x, self.__Owner, self.__Team, NO_SQUAD_ID, 0 )
		newGroupUnit = GroupUnit(newUnitId)
		self.AddUnit(newGroupUnit)

	
	def DecrUnitsInAir( self, anAmount ):
		
		self.__NrUnitsInAir -= anAmount
		
	
	def CancelAirDrops( self ):
				
		## remove all reactions listening for units to be created
		for react in self.__AirDropReactions:
			serverimports.RemoveReaction( react )
		self.__AirDropReactions = []
		
		##check for units in air
		for grp in self.__RefillGroups[:]:
			if grp.GetNrUnitsInAir() > 0:
				serverimports.RemoveGroup( grp, True )
				self.__RefillGroups.remove( grp )

	
	def DropUnitsAtPosition( self, aUnits, aTarget, aOwner = -1, aTeam = -1, aSquadId = NO_SQUAD_ID, aDirection = None ):
		
		self.CreateUnitsAtPosition( aUnits, aTarget, aOwner, aTeam, aSquadId, True, aDirection )
		
	
	def CreateUnitsAtPosition( self, someUnits, aTarget, aOwner = -1, aTeam = -1, aSquadId = NO_SQUAD_ID, aUseAirDrop = False, aDirection = None ):
		
		if __debug__:
			debug.DebugMessage( 'Group::CreateUnitsAtPosition(%s) - aOwner=%d aTeam=%d aSquadId=%d aUseAirDrop=%s' %\
			( self, aOwner, aTeam, aSquadId, aUseAirDrop ) )
		
		try:
			targetPos = common.GetPosition( aTarget )
		except EmptyGroupException:
			debug.DebugMessage( 'Group(%s)::CreateUnitsAtPosition Failed! Invalid Target EmptyGroup(%s)' % (self.__Name, aTarget), debug.NONE )
			return
		except unit.UnknownUnitException:
			debug.DebugMessage( 'Group(%s)::CreateUnitsAtPosition Failed! Invalid Target Unit(%d)' % (self.__Name, aTarget), debug.NONE )
			return

		if aOwner == -1:
			aOwner = self.__Owner
		if aTeam == -1:
			aTeam = self.__Team

		if aUseAirDrop:
						
			key = Groups.GetNextUniqueSpawnKey()
			
			squadCreation = False
			
			## check if its a squad spawner unit
			if len( someUnits ) == 1 and common.IsSquadUnitType( someUnits[0] ):
				nrOfUnits = MAX_SQUAD_SIZE
				squadCreation = True
			else:
				nrOfUnits = len( someUnits )
			
			self.__NrUnitsInAir += nrOfUnits
			
			if squadCreation:
				airDropReaction = serverimports.RE_OnUnitCreatedWithKey( key, serverimports.Action( self.DecrUnitsInAir, nrOfUnits ) )
				airDropReaction.myNrOfExecutions = 1
			else:
				airDropReaction = serverimports.RE_OnUnitCreatedWithKey( key, [serverimports.Action( self.DecrUnitsInAir, 1 ), serverimports.Action( self.AddUnitFromEventData )] )
				airDropReaction.myNrOfExecutions = nrOfUnits

			airDropReaction.AddEndAction( serverimports.Action( self.__AirDropReactions.remove, airDropReaction ) )
			airDropReaction.AddEndAction( serverimports.Action( serverimports.PostEvent, 'UnitsDropped', self ) )
			self.__AirDropReactions.append( airDropReaction )
									
			if aDirection == None:
				if hasattr(self, "_Group__DropShipDirection"):
					dropDirection = self.__DropShipDirection
				else:
					dropDirection = Position( -1, -1, -1 )
			else:
				dropDirection = aDirection
			
			## start the dropship
			wicg.CreateUnitsWithSpawner( someUnits, targetPos, aOwner, aTeam, key, 0, dropDirection )

						
			if __debug__:
				debug.DebugMessage( 'Group::CreateUnitsAtPosition(%s) - Using AirDrop Owner=%d Team=%d NrOfUnit=%d Key=%d' % \
				 ( self, aOwner, aTeam, len( someUnits ), key ) )
			
			return
		
			
		for unitType in someUnits:
			## if unit is an infantry and it should be added to current squads
			if common.IsInfantryType( unitType ) and self.__UseSquadCreation and aSquadId == NO_SQUAD_ID:
				squadId = self.FindFreeSquad()
				
				if squadId == NO_SQUAD_ID:
					squadId = wicg.GetAndIncNextFreeSquadId()
				else:
					squadSize = wicg.GetSquadSize( squadId )
					if squadSize >= MAX_SQUAD_SIZE:
						raise SquadSizeException( 'Group(%s)::CreateUnitsAtPosition Warning Squad Bug!!! squadSize=%d, squadId=%d' % (self, squadSize, squadId) )
						#squadId = wicg.GetAndIncNextFreeSquadId()

				newUnitId = wicg.CreateUnit( unitType, targetPos, 0.0, aOwner, aTeam, squadId, 0 )
			else:
				newUnitId = wicg.CreateUnit( unitType, targetPos, 0.0, aOwner, aTeam, aSquadId, 0 )
			
			if newUnitId == INVALID_UNIT_ID:
				raise CreateUnitException( 'Group::CreateUnitsAtPosition(%s) Failed to create unit! (id=%d) Target=%s Type=%d' % (self.__Name, INVALID_UNIT_ID, aTarget, unitType) )
			
			## squad units will be added through the squad reaction
			if not common.IsSquadUnitType( unitType ):
				self.AddUnit( GroupUnit( newUnitId ) )
	

	def FindFreeSquad( self ):
		
		squadIds = {}
						
		for grpUnit in self.__Units:
			
			## update unit to prevent squadsize bug
			grpUnit.myUnit.Update( True, True )
		
			if common.IsInfantry( grpUnit.myUnitId ):
				squadIds[grpUnit.myUnit.mySquadId] = 0


		for grpUnit in self.__Units:
			if common.IsInfantry( grpUnit.myUnitId ):
				squadIds[grpUnit.myUnit.mySquadId] += 1
				
		bestSquadId = 0
		bestSquadSize = 6
		
		for squadId in squadIds.keys():
			if squadIds[squadId] > 0 and squadIds[squadId] < MAX_SQUAD_SIZE and squadIds[squadId] < bestSquadSize:
				bestSquadId = squadId
				bestSquadSize = squadIds[squadId]
		
		return bestSquadId


	def CreateUnitsAtPositionEx( self, aUnits, aTarget, aHeading, aOwner, aTeam, aSquadId = NO_SQUAD_ID ):
		"""
		"""

		try:
			targetPos = common.GetPosition( aTarget )
		except EmptyGroupException:
			debug.DebugMessage( 'Group(%s)::CreateUnitsAtPositionEx Failed! Invalid Target EmptyGroup(%s)' % (self.__Name, aTarget), debug.NONE )
			return
		except unit.UnknownUnitException:
			debug.DebugMessage( 'Group(%s)::CreateUnitsAtPositionEx Failed! Invalid Target Unit(%d)' % (self.__Name, aTarget), debug.NONE )
			return
		
		
		if not isinstance( aHeading, float ) and not isinstance( aHeading, int ):
			try:
				headingTargetPos = common.GetPosition( aHeading )
			except EmptyGroupException:
				debug.DebugMessage( 'Group(%s)::CreateUnitsAtPositionEx Failed! Invalid Heading Target EmptyGroup(%s)' % (self.__Name, aHeading), debug.NONE )
				return
			except unit.UnknownUnitException:
				debug.DebugMessage( 'Group(%s)::CreateUnitsAtPositionEx Failed! Invalid Heading Target Unit(%d)' % (self.__Name, aHeading), debug.NONE )
				return

			aHeading = wicmath.Vector2Heading( wicmath.GetVector( targetPos, headingTargetPos ) )
			
		
		for unitType in aUnits:
			if common.IsInfantryType( unitType ) and self.__UseSquadCreation and aSquadId == NO_SQUAD_ID:
				squadId = self.FindFreeSquad()
				
				if squadId == NO_SQUAD_ID:
					squadId = wicg.GetAndIncNextFreeSquadId()

				newUnitId = wicg.CreateUnit( unitType, targetPos, aHeading, aOwner, aTeam, squadId, 0 )
			else:
				newUnitId = wicg.CreateUnit( unitType, targetPos, aHeading, aOwner, aTeam, aSquadId, 0 )
			
			if newUnitId == INVALID_UNIT_ID:
				raise CreateUnitException( 'Group::CreateUnitsAtPositionEx(%s) Failed to create unit! (id=%d)' % (self.__Name, INVALID_UNIT_ID) )
			
			newGroupUnit = GroupUnit( newUnitId )
			self.AddUnit( newGroupUnit )


	def CreateSquad( self, aUnits, aTarget, aOwner = -1, aTeam = -1 ):

		try:
			targetPos = common.GetPosition( aTarget )
		except EmptyGroupException:
			debug.DebugMessage( 'Group(%s)::CreateSquad Failed! Invalid Target EmptyGroup(%s)' % (self.__Name, aTarget), debug.NONE )
			return
		except unit.UnknownUnitException:
			debug.DebugMessage( 'Group(%s)::CreateSquad Failed! Invalid Target Unit(%d)' % (self.__Name, aTarget), debug.NONE )
			return
		
		if aOwner == -1:
			aOwner = self.__Owner
		if aTeam == -1:
			aTeam = self.__Team

		if self.IsEmpty():
			self.__Owner = aOwner
			self.__Team = aTeam

		if len( aUnits ) > MAX_SQUAD_SIZE:
			raise SquadSizeException( 'Group::CreateSquad To many units in squad (%d)' % len( aUnits ) )
		
		squadId = wicg.GetAndIncNextFreeSquadId()
		self.CreateUnitsAtPosition( aUnits, aTarget, aOwner, aTeam, squadId, self.__UseAirDrop )

	
	def CancelSquadReactions( self ):
		
		for squadReaction in self.__SquadReactions:
			serverimports.RemoveReaction( squadReaction )
		self.__SquadReactions = []
	
	
	def CreateSquadEx( self, aSquadUnitType, aTarget ):
		
		## we dont want any infantry units to join this squad
		self.__UseSquadCreation = False
		
		squadId = wicg.GetNextFreeSquadId()
		
		if self.__UseAirDrop:
			key = self.CreateUnitsAtPosition( [aSquadUnitType], aTarget, -1, -1, squadId, self.__UseAirDrop )
			
			squadReaction = serverimports.RE_OnUnitCreatedWithKey( key, serverimports.Action( self.AddUnitFromEventData ) )
			squadReaction.myRepeating = True
			self.__SquadReactions.append( squadReaction )
		
		else:
			## units created and migration, listen for new units in the squad
			squadReaction = serverimports.RE_OnUnitCreatedInSquad( squadId, serverimports.Action( self.AddUnitFromEventData ) )
			squadReaction.myRepeating = True
			self.__SquadReactions.append( squadReaction )
			
			self.CreateUnitsAtPosition( [aSquadUnitType], aTarget, -1, -1, squadId, self.__UseAirDrop )
		
	
	def AddUnitFromEventData( self ):
		
		## this units has just been created and we got a callback from the reaction system
		## a UnitCreated was posted so the unit id is saved in the first element of the event data list
		unitId = serverimports.theReactions.myEventData[0]
		self.AddUnit( GroupUnit( unitId ) )
		
		## special spawned infantry units will have neutral team when spawned to script player
		unit.theUnits[unitId].myTeam = self.__Team
		
	
	def AddUnits( self, someGroupUnits ):

		for groupUnit in someGroupUnits:
			self.AddUnit( groupUnit )


	def AddUnitsById( self, someUnitIds ):

		for unitId in someUnitIds:
			self.AddUnit( GroupUnit( unitId ) )


	def AddUnit( self, aGroupUnit ):

		try:
			unit.theUnits[aGroupUnit.myUnitId]
		except unit.UnknownUnitException:
			debug.DebugMessage( 'Group(%s)::AddUnit Warning! Invalid Unit(%d) ' % ( self.__Name, aGroupUnit.myUnitId ), debug.NONE )
			raise unit.UnknownUnitException
		
		## check size of group
		if __debug__:
			size = self.Size()
			if size >= MAX_GROUP_SIZE:
				raise GroupToBigException( 'Group(%s) has too many units(%d). Max nr of units in group is %d.' % (self, size, MAX_GROUP_SIZE) )
		
		newGroupUnit = GroupUnit( aGroupUnit.myUnitId )
		newGroupUnit.Reset( self )
		self.__Units.append( newGroupUnit )
			
		serverimports.PostEvent( 'GroupSize', self, self.Size( True ) )
		
		self.UpdatePlatoonSize()

	
	def DestroyGroup( self, aShouldExplode = 0, aDestroyRefillGroups = False ):
		self.ValidateUnits( False )

		for groupUnit in self.__Units[:]:
			self.DestroyUnit( groupUnit, aShouldExplode )
			
		if aDestroyRefillGroups:
			for g in self.__RefillGroups:
				g.DestroyGroup( aShouldExplode )


	def DestroyUnits( self, aStartIndex, aStopIndex, aShouldExplode = 0 ):

		if self.IsEmpty() or aStopIndex < aStartIndex or aStartIndex < 0 or aStopIndex >= self.Size():
			return

		for groupUnit in self.__Units[aStartIndex:aStopIndex+1]:
			self.DestroyUnit( groupUnit, aShouldExplode )


	def DestroyUnit( self, aGroupUnit, aShouldExplode = 0 ):

		if aGroupUnit in self.__Units:
			if aGroupUnit.myUnit.myOwner == serverimports.PLAYER_HUMAN:
				wicg.RemovePlayerUnit( aGroupUnit.myUnitId, aShouldExplode )
			else:
				wicg.RemoveUnit( aGroupUnit.myUnitId, aShouldExplode )
	

	def DestroyUnitById( self, aUnitId, aShouldExplode = 0 ):

		UnitToDestroy = None
		for grpUnit in self.__Units:
			if grpUnit.myUnitId == aUnitId:
				UnitToDestroy = grpUnit
				break
		
		if UnitToDestroy:
			self.DestroyUnit( UnitToDestroy, aShouldExplode )
			return True
		
		return False


	def RemoveAllUnits( self ):

		if self.IsEmpty():
			return

		for groupUnit in self.__Units[:]:
			self.RemoveUnit( groupUnit )


	def RemoveUnits( self, aStartIndex, aStopIndex ):

		if self.IsEmpty() or aStopIndex < aStartIndex or aStartIndex < 0 or aStopIndex >= self.Size():
			return

		for groupUnit in self.__Units[aStartIndex:aStopIndex+1]:
			self.RemoveUnit( groupUnit )


	def RemoveUnit( self, aGroupUnit ):

		if aGroupUnit in self.__Units:
			aGroupUnit.Shutdown( self )
			self.__Units.remove( aGroupUnit )
		else:
			debug.DebugMessage( 'Group(%s)::RemoveUnit Failed! Unit not in group(%s)' % (self.__Name, aGroupUnit), debug.BRIEF )
			return

		serverimports.PostEvent( 'GroupSize', self, self.Size( True ) )
		
		self.UpdatePlatoonSize()
		
		self.TestForRefill()
		
		if self.__ParentGroup:
			self.__ParentGroup.TestForRefill()
	
	
	def RemoveUnitById( self, aUnitId ):
		
		UnitToRemove = None
		for grpUnit in self.__Units:
			if grpUnit.myUnitId == aUnitId:
				UnitToRemove = grpUnit
				break
		
		if UnitToRemove:
			self.RemoveUnit( UnitToRemove )
			return True
		
		return False


	def ValidateUnits( self, aUpdateGroups ):
		
		debug.DebugMessage( 'ValidateUnits (%s)' % self )		
		toBeRemoved = []
		
		allOk = True
		for grpUnit in self.__Units[:]:
			try:
				grpUnit.myUnit.myHealth
			except unit.UnknownUnitException:
				debug.DebugMessage( 'ValidateUnits Bad Unit (%d)' % grpUnit.myUnitId )
				if aUpdateGroups:
					grpUnit.Shutdown( self )
					toBeRemoved.append( grpUnit )					
				else:
					allOk =  False
		
		for grpUnit in toBeRemoved:
			self.__Units.remove( grpUnit )
		
		return allOk
		

	def MergeGroup( self, aGroup, aRefillerGroupsTo = False ):
		## Added the possibility to merge aGroups refiller units to the new group. davidh 080720.
		if aRefillerGroupsTo:
			for refillGrp in aGroup.myRefillGroups:
				refillGrp.Purge() 
				aGroup.MergeGroup( refillGrp )			
		
		self.AddUnits( aGroup.myUnits )
		aGroup.RemoveAllUnits()

		return aGroup


	def MakePassive( self ):
		
		if self.__IsPassive:
			return
		
		self.__IsPassive = True
		
		self.UnTrackGroup()
		
		for grpUnit in self.__Units:
			grpUnit.MakePassive()
		
		self.__BehaviorManager.Pause()

		
	def MakeActive( self ):
		
		if not self.__IsPassive:
			return
		
		self.__IsPassive = False
		
		self.TrackGroup()
		
		for grpUnit in self.__Units:
			grpUnit.MakeActive( self )
		
		self.__BehaviorManager.UnPause()
		

	def OnUnitDestroyed( self, aGroupUnit ):
		
		self.RemoveUnit( aGroupUnit )


	def OnInCombat( self, aGroupUnit ):
		
		if aGroupUnit.myUnitId == serverimports.theReactions.myEventData[0]:
			aAttackerId = serverimports.theReactions.myEventData[1]
		else:
			aAttackerId = serverimports.theReactions.myEventData[0]

		
		for grp in self.__CombatExceptionGroups:
			if grp.IsUnitInGroup( aAttackerId ):
				return

		self.UnTrackGroup()
		
		serverimports.PostEvent( 'GroupInCombat', self, aGroupUnit.myUnitId, aAttackerId )
		serverimports.Delay( COMBAT_DELAY, serverimports.Action( self.TrackGroup ) )
		
		## handle platoon updates
		for plt in self.__Platoons:
			plt.OnInCombat( self, aGroupUnit.myUnitId, aAttackerId )


	def TrackGroup( self ):
		
		if self.__IsPassive:
			return
		
		for groupUnit in self.__Units:
			wicg.TrackUnit( groupUnit.myUnitId )


	def UnTrackGroup( self ):
				
		for groupUnit in self.__Units:
			wicg.UnTrackUnit( groupUnit.myUnitId )


	def LookAt( self, aTarget ):

		try:
			targetPos = common.GetPosition( aTarget )
		except EmptyGroupException:
			debug.DebugMessage("Group(%s)::LookAt Failed! Invalid Target EmptyGroup(%s)" % (self.__Name, aTarget), debug.NONE)
			return
		except unit.UnknownUnitException:
			debug.DebugMessage("Group(%s)::LookAt Failed! Invalid Target Unit(%d)" % (self.__Name, aTarget), debug.NONE)
			return

		for groupUnit in self.__Units:
			groupUnit.myUnit.LookAt( targetPos )


	def FaceDirection( self, aDirection ):

		debug.DebugMessage( 'Group(%s)::FaceDirection - %s' % (self, aDirection) )

		direction = None

		if isinstance( aDirection, float ) or isinstance( aDirection, int ):
			direction = wicmath.Heading2Vector( aDirection )
		elif isinstance( aDirection, Position ):
			direction = wicmath.Position2Vector( aDirection )
		elif isinstance( aDirection, Vector ):
			direction = aDirection
		else:
			return

		for groupUnit in self.__Units:
			u = groupUnit.myUnit
			pos = wicmath.Position2Vector( u.myPos )
			vtarget = pos + direction
			ptarget = wicmath.Vector2Position( vtarget )
			u.LookAt( ptarget )


	def TeleportUnit( self, aGroupUnit, aTarget, aDirection = None ):

		if self.__IsTransporter and wicg.GetContainerId( aGroupUnit.myUnitId ) != -1:
			return True

		try:
			targetPos = common.GetPosition( aTarget )
		except EmptyGroupException:
			debug.DebugMessage( 'Group(%s)::TeleportUnit Failed! Invalid Target EmptyGroup(%s)' % ( self.__Name, aTarget ), debug.NONE )
			return False
		except unit.UnknownUnitException:
			debug.DebugMessage( 'Group(%s)::TeleportUnit Failed! Invalid Target Unit(%d)' % ( self.__Name, aTarget ), debug.NONE )
			return False
		
		if aGroupUnit.myUnit.myOwner == serverimports.PLAYER_HUMAN:
			wicg.PlayerStopUnit( aGroupUnit.myUnitId )
			wicg.TeleportPlayerUnit( aGroupUnit.myUnitId, targetPos )
		else:
			wicg.SetUnitData( aGroupUnit.myUnitId , 'position', targetPos )
		
		aGroupUnit.myTargetPos = targetPos
		
		if aDirection != None and aGroupUnit.myUnit.myOwner != serverimports.PLAYER_HUMAN:
			heading = wicmath.Vector2Heading( wicmath.Position2Vector( aDirection ) )
			wicg.SetUnitData( aGroupUnit.myUnitId, 'heading', heading )

		return True


	def TeleportGroup( self, aTarget, aDirection = None ):
		
		return self.MoveGroup( aTarget, aDirection, None, True )

	
	def MoveUnit( self, aGroupUnit, aTarget, aHeading = None, aSpeed = None, aBackwards = False ):
		
		if self.__IsTransporter and wicg.GetContainerId( aGroupUnit.myUnitId ) != -1:
			return True
		
		try:
			tempPos = common.GetPosition(aTarget)
		except EmptyGroupException:
			debug.DebugMessage( 'Group(%s)::MoveUnit Failed! Invalid Target EmptyGroup(%s)' % (self.__Name, aTarget), debug.NONE )
			return
		except unit.UnknownUnitException:
			debug.DebugMessage( 'Group(%s)::MoveUnit Failed! Invalid Target Unit(%d)' % (self.__Name, aTarget), debug.NONE )
			return

		targetPos = Position( tempPos.myX, tempPos.myY, tempPos.myZ )

		original_pos = Position()
		original_pos.myX = targetPos.myX
		original_pos.myZ = targetPos.myZ
	
		if aSpeed is None:
			speed = self.GetSpeed()
		else:
			speed = aSpeed
		
		counter = 0
		step = 0
		move_ok = False
		while counter < POSITION_TEST_LIMIT and not move_ok and self.__NrOfBadMoveOrdersThisUpdate < MAX_MOVE_ORDERS_PER_UPDATE:
			mod = counter % 5
		
			if mod == 0:
				step += 1
			elif mod == 1:
				targetPos.myX = original_pos.myX + step * POSITION_TEST_STEP_SIZE
				targetPos.myZ = original_pos.myZ + step * POSITION_TEST_STEP_SIZE
			elif mod == 2:
				targetPos.myX = original_pos.myX - step * POSITION_TEST_STEP_SIZE
				targetPos.myZ = original_pos.myZ - step * POSITION_TEST_STEP_SIZE
			elif mod == 3:
				targetPos.myX = original_pos.myX + step * POSITION_TEST_STEP_SIZE
				targetPos.myZ = original_pos.myZ - step * POSITION_TEST_STEP_SIZE
			elif mod == 4:
				targetPos.myX = original_pos.myX - step * POSITION_TEST_STEP_SIZE
				targetPos.myZ = original_pos.myZ + step * POSITION_TEST_STEP_SIZE

			counter += 1
			move_ok = aGroupUnit.myUnit.MoveTo( targetPos, aHeading, speed, aBackwards )

			##count the number of move orders this update
			self.__NrOfBadMoveOrdersThisUpdate += 1


		if counter == POSITION_TEST_LIMIT and not move_ok:
			debug.DebugMessage( 'Group(%s)::MoveUnit Failed! No valid position in range!' % (self.__Name), debug.NONE )
			return False
		
		if move_ok:
			aGroupUnit.myTargetPos = targetPos
			aGroupUnit.myTargetHeading = aHeading
			aGroupUnit.myTargetSpeed = speed
			return True
		else:
			debug.DebugMessage( 'Group(%s)::MoveUnit Failed!' % (self.__Name), debug.NONE )
			return False


	def MoveUnitCover( self, aGroupUnit, aTarget, aHeading = None, aSpeed = None ):
		
		if self.__IsTransporter and wicg.GetContainerId( aGroupUnit.myUnitId ) != -1:
			return True

		try:
			tempPos = common.GetPosition(aTarget)
		except EmptyGroupException:
			debug.DebugMessage( 'Group(%s)::MoveUnitCover Failed! Invalid Target EmptyGroup(%s)' % (self.__Name, aTarget), debug.NONE )
			return
		except unit.UnknownUnitException:
			debug.DebugMessage( 'Group(%s)::MoveUnitCover Failed! Invalid Target Unit(%d)' % (self.__Name, aTarget), debug.NONE )
			return

		targetPos = Position( tempPos.myX, tempPos.myY, tempPos.myZ )

		original_pos = Position()
		original_pos.myX = targetPos.myX
		original_pos.myZ = targetPos.myZ
	
		if aSpeed is None:
			speed = self.GetSpeed()
		else:
			speed = aSpeed
		
		counter = 0
		step = 0
		move_ok = False
		while counter < POSITION_TEST_LIMIT and not move_ok and self.__NrOfBadMoveOrdersThisUpdate < MAX_MOVE_ORDERS_PER_UPDATE:
			mod = counter % 5
		
			if mod == 0:
				step += 1
			elif mod == 1:
				targetPos.myX = original_pos.myX + step * POSITION_TEST_STEP_SIZE
				targetPos.myZ = original_pos.myZ + step * POSITION_TEST_STEP_SIZE
			elif mod == 2:
				targetPos.myX = original_pos.myX - step * POSITION_TEST_STEP_SIZE
				targetPos.myZ = original_pos.myZ - step * POSITION_TEST_STEP_SIZE
			elif mod == 3:
				targetPos.myX = original_pos.myX + step * POSITION_TEST_STEP_SIZE
				targetPos.myZ = original_pos.myZ - step * POSITION_TEST_STEP_SIZE
			elif mod == 4:
				targetPos.myX = original_pos.myX - step * POSITION_TEST_STEP_SIZE
				targetPos.myZ = original_pos.myZ + step * POSITION_TEST_STEP_SIZE

			counter += 1

			dist2Target = wicmath.Distance( aGroupUnit.myUnit.myPos, targetPos )
			movePos = wicg.MoveUnitsCover( [aGroupUnit.myUnitId], targetPos, dist2Target + DEFAULT_COVER_DISTANCE_FORWARD )
			move_ok = aGroupUnit.myUnit.MoveTo( movePos[0], aHeading, speed )
			
			##count the number of move orders this update
			self.__NrOfBadMoveOrdersThisUpdate += 1

		if counter == POSITION_TEST_LIMIT and not move_ok:
			debug.DebugMessage( 'Group(%s)::MoveUnitCover Failed! No valid position in range!' % (self.__Name), debug.VERBOSE )
			return False
		
		if move_ok:
			aGroupUnit.myTargetPos = targetPos
			aGroupUnit.myTargetHeading = aHeading
			aGroupUnit.myTargetSpeed = speed
			return True
		else:
			debug.DebugMessage( 'Group(%s)::MoveUnitCover Failed!' % (self.__Name), debug.VERBOSE )
			return False


	def MoveGroup( self, aTarget, aDirection = None, aHeading = None, aTeleport = False, aBackwards = False ):
		
		if self.IsEmpty():
			debug.DebugMessage( "Group(%s)::MoveGroup Failed! EmptyGroup(%s)" % (self.__Name, self.__Name), debug.VERBOSE )
			return False

		try:
			targetPos = common.GetPosition( aTarget )
		except EmptyGroupException:
			debug.DebugMessage("Group(%s)::MoveGroup Failed! EmptyGroup(%s)" % (self.__Name, aTarget), debug.BRIEF)
			return False
		except unit.UnknownUnitException:
			debug.DebugMessage("Group(%s)::MoveGroup Failed! Invalid Unit(%d)" % (self.__Name, aTarget), debug.BRIEF)
			return False

		if aDirection is None:
			Direction = wicmath.Vector2Position( wicmath.GetVector( self.GetPosition(), targetPos ) )
		else:
			Direction = aDirection

		if Direction.myX == 0 and Direction.myZ == 0:
			debug.DebugMessage("Group(%s)::MoveGroup Failed! Invalid Direction(%s)" % (self.__Name, Direction), debug.VERBOSE)
			return False

		## fetch all units to move
		units = []
		groupUnits = []
		for groupUnit in self.__Units:
			if self.__IsTransporter:
				if wicg.GetContainerId( groupUnit.myUnitId ) == -1:
					units.append( groupUnit.myUnitId )
					groupUnits.append( groupUnit )
				else:
					continue
			else:
				units.append( groupUnit.myUnitId )
				groupUnits.append( groupUnit )

		## calculate all positions
		positions = []

		if self.__Formation == FORMATION_COVER:
			dist2Target = wicmath.Distance( self.GetPosition(), targetPos )
			positions = wicg.MoveUnitsCover( units, targetPos, dist2Target + DEFAULT_COVER_DISTANCE_FORWARD )
		else:		
			positions = wicg.MoveUnits( units, targetPos, Direction, self.__Formation, self.__FormationDistance )
			
		
		## calculate offset
		if self.__FormationOffset > 0.0 and self.__Formation != FORMATION_COVER:
			self.CalculateOffsetPositions( positions, Direction, self.__FormationOffset )
		if self.__FormationWidthOffset > 0.0 and self.__Formation != FORMATION_COVER:
			offsetDirection = wicmath.Vector2Position( wicmath.RotateVector( wicmath.Position2Vector( Direction ), (math.pi / 2) ) )
			self.CalculateOffsetPositions( positions, offsetDirection, self.__FormationWidthOffset )
		
		
		## calculate speed
		speed = self.GetSpeed()
		
		self.__NrOfBadMoveOrdersThisUpdate = 0
		
		## move units
		pos_counter = 0
		all_ok = True
		for groupUnit in groupUnits:
			if aTeleport:
				if self.TeleportUnit( groupUnit, positions[pos_counter], Direction ):
					all_ok = False
			else:
				if not self.MoveUnit( groupUnit, positions[pos_counter], aHeading, speed, aBackwards ):
					all_ok = False
			pos_counter += 1
	
		return all_ok


	def MoveSubgroup(self, aStartIndex, aStopIndex, aTarget):

		if self.IsEmpty():
			return False
		
		try:
			targetPos = common.GetPosition(aTarget)
		except EmptyGroupException:
			debug.DebugMessage("Group(%s)::MoveSubgroup Failed! EmptyGroup(%s)" % (self.__Name, aTarget), debug.NONE)
			return False
		except unit.UnknownUnitException:
			debug.DebugMessage("Group(%s)::MoveSubgroup Failed! Invalid Unit(%d)" % (self.__Name, aTarget), debug.NONE)
			return False


		all_ok = True

		if aStartIndex >= 0 and aStopIndex < self.Size():

			Direction = wicmath.Vector2Position(wicmath.GetVector(self.GetPosition(), targetPos))
			
			if Direction.myX == 0 and Direction.myZ == 0:
				debug.DebugMessage("Group(%s)::MoveSubgroup Failed! Invalid Direction(%s)" % (self.__Name, Direction), debug.VERBOSE)
				return False
			
			## fetch all units to move
			units = []
			groupUnits = []
			for groupUnit in self.__Units[aStartIndex:(aStopIndex + 1)]:
				if self.__IsTransporter:
					if wicg.GetContainerId( groupUnit.myUnitId ) == -1:
						units.append( groupUnit.myUnitId )
						groupUnits.append( groupUnit )
					else:
						continue
				else:
					units.append( groupUnit.myUnitId )
					groupUnits.append( groupUnit )
			
			## calculate positions
			positions = []
			if self.__Formation == FORMATION_COVER:
				dist2Target = wicmath.Distance(self.GetPosition(), targetPos)
				positions = wicg.MoveUnitsCover( units, targetPos, self.__FormationDistance + DEFAULT_COVER_DISTANCE_FORWARD )
			else:
				positions = wicg.MoveUnits(units, targetPos, Direction, self.__Formation, self.__FormationDistance)
			
			## calculate offset
			if self.__FormationOffset > 0.0 and self.__Formation != FORMATION_COVER:
				self.CalculateOffsetPositions( positions, Direction, self.__FormationOffset )
			
			## calculate speed
			speed = self.GetSpeed()
			
			self.__NrOfBadMoveOrdersThisUpdate = 0
			
			## move units
			counter = 0
			for groupUnit in groupUnits:
				if not self.MoveUnit( groupUnit, positions[counter], None, speed ):
					all_ok = False
				counter += 1
		return all_ok

	
	def MoveMultipleUnits( self, someUnits, aTarget ):
		
		if self.IsEmpty():
			return False
		
		try:
			targetPos = common.GetPosition(aTarget)
		except EmptyGroupException:
			debug.DebugMessage("Group(%s)::MoveMultipleUnits Failed! EmptyGroup(%s)" % (self.__Name, aTarget), debug.NONE)
			return False
		except unit.UnknownUnitException:
			debug.DebugMessage("Group(%s)::MoveMultipleUnits Failed! Invalid Unit(%d)" % (self.__Name, aTarget), debug.NONE)
			return False

		## fetch all units to move
		units = []
		groupUnits = []
		for u in someUnits:
			if self.__IsTransporter:
				if wicg.GetContainerId( u.myUnitId ) == -1:
					units.append( u.myUnitId )
					groupUnits.append( u )
				else:
					continue
			else:
				units.append( u.myUnitId )
				groupUnits.append( u )


		Direction = wicmath.Vector2Position( wicmath.GetVector( self.GetPosition(), targetPos ) )
			
		if Direction.myX == 0 and Direction.myZ == 0:
			debug.DebugMessage( 'Group(%s)::MoveMultipleUnits Failed! Invalid Direction(%s)' % (self.__Name, Direction), debug.VERBOSE )
			return False

		if self.__Formation == FORMATION_COVER:
			dist2Target = wicmath.Distance(self.GetPosition(), targetPos)
			positions = wicg.MoveUnitsCover( units, targetPos, self.__FormationDistance + DEFAULT_COVER_DISTANCE_FORWARD )
		else:
			positions = wicg.MoveUnits( units, targetPos, Direction, self.__Formation, self.__FormationDistance )
		
		## calculate offset
		if self.__FormationOffset > 0.0 and self.__Formation != FORMATION_COVER:
			self.CalculateOffsetPositions( positions, Direction, self.__FormationOffset )

		speed = self.GetSpeed()

		all_ok = True
		
		self.__NrOfBadMoveOrdersThisUpdate = 0
		
		c = 0
		for u in groupUnits:
			if not self.MoveUnit( u, positions[c], None, speed ):
				all_ok = False
			c += 1
			
		return all_ok



	def MoveMultipleTargets(self, aTargets, aLimit = CLOSE_TO_LIMIT):

		if not len(aTargets) or self.IsEmpty():
			return False
		
		allUnitsToMove = []
		
		if self.__IsTransporter:
			for u in self.__Units:
				if wicg.GetContainerId( u.myUnitId ) == -1:
					allUnitsToMove.append( u )
		else:
			allUnitsToMove = self.__Units
			
		unitsPerPosition = len(allUnitsToMove) / len(aTargets)
		unitsOver = len(allUnitsToMove) % len(aTargets)

		unitCounter = 0
		
		for i in aTargets:
			if unitCounter >= len(allUnitsToMove):
				return
			else:
				unitsToMove = []
				j = 0
				while j < unitsPerPosition:
					unitsToMove.append( allUnitsToMove[unitCounter] )
					unitCounter += 1
					j += 1

				if unitsOver > 0:
					unitsToMove.append( allUnitsToMove[unitCounter] )
					unitCounter += 1
					j += 1
					unitsOver -= 1

				if not self.IsMultipleUnitsCloseTo( unitsToMove, i, aLimit ):
					self.MoveMultipleUnits( unitsToMove, i )


	def StopGroup( self ):

		self.__NrOfBadMoveOrdersThisUpdate = 0
		speed = self.GetSpeed()
		for i in self.__Units:
			self.StopUnit( i, speed )


	def StopUnit( self, aGroupUnit, aSpeed = None ):
		
		self.MoveUnit( aGroupUnit, aGroupUnit.myUnit.myPos, None, aSpeed )


	def TakeCover( self ):
		
		if self.IsEmpty():
			return

		leaderPos = self.GetPosition()
		direction = wicmath.Vector2Position( wicmath.Heading2Vector( self.GetHeading() ) )
		
		oldFormation = self.__Formation
		self.__Formation = FORMATION_COVER
		self.MoveGroup( leaderPos, direction )
		self.__Formation = oldFormation


	def Regroup( self, aTarget = None ):
		
		if self.IsEmpty():
			return

		direction = None
		heading = None

		leaderPos = self.GetPosition()

		if aTarget:
			
			try:		
				targetPos = common.GetPosition( aTarget )
			except EmptyGroupException:
				debug.DebugMessage( 'Group(%s)::Regroup Failed! EmptyGroup(%s)' % (self.__Name, aTarget), debug.NONE )
				return False
			except unit.UnknownUnitException:
				debug.DebugMessage( 'Group(%s)::Regroup Failed! Invalid Target Unit(%d)' % (self.__Name, aTarget), debug.NONE )
				return False

			
			direction = wicmath.Vector2Position( wicmath.GetVector(leaderPos, targetPos) )
			heading = wicmath.GetHeading( wicmath.Position2Vector(leaderPos), wicmath.Position2Vector(targetPos) )
		else:
			direction = wicmath.Vector2Position( wicmath.Heading2Vector( self.GetHeading() ) )

		return self.MoveGroup( leaderPos, direction, heading )


	def RegroupAt( self, aPosition, aTarget = None ):

		if self.IsEmpty():
			return

		direction = None
		heading = None

		try:
			position = common.GetPosition( aPosition )
		except EmptyGroupException:
			debug.DebugMessage( 'Group(%s)::RegroupAt Failed! Invalid Position EmptyGroup(%s)' % (self.__Name, aPosition), debug.NONE )
			return False
		except unit.UnknownUnitException:
			debug.DebugMessage( 'Group(%s)::RegroupAt Failed! Invalid Position Unit(%d)' % (self.__Name, aPosition), debug.NONE )
			return False


		if aTarget:
			try:
				targetPos = common.GetPosition( aTarget )
			except EmptyGroupException:
				debug.DebugMessage( 'Group(%s)::RegroupAt Failed! Invalid Target EmptyGroup(%s)' % (self.__Name, aTarget), debug.NONE )
				return False
			except unit.UnknownUnitException:
				debug.DebugMessage( 'Group(%s)::RegroupAt Failed! Invalid Target Unit(%d)' % (self.__Name, aTarget), debug.NONE )
				return False

			direction = wicmath.Vector2Position( wicmath.GetVector( position, targetPos ) )
			heading = wicmath.GetHeading( wicmath.Position2Vector( position ), wicmath.Position2Vector( targetPos ) )
		else:
			direction = wicmath.Vector2Position( wicmath.Heading2Vector( self.GetHeading() ) )

		return self.MoveGroup( position, direction, heading )


	def EnterContainer( self, aContainer, aInstantEnter = False ):
		
		if isinstance( aContainer, str ):
			self.EnterBuilding( aContainer, aInstantEnter )
		else:
			for groupUnit in self.__Units:
				groupUnit.myUnit.EnterContainer( aContainer, aInstantEnter )


	def EnterBuilding( self, aBuilding, aInstantEnter = False ):
		
		squadIds = []

		for groupUnit in self.__Units:
			u = groupUnit.myUnit
			if common.IsInfantry( groupUnit.myUnitId ) and not u.mySquadId in squadIds:
				squadIds.append(u.mySquadId)

		if len(squadIds) == 0:
			return

		if isinstance(aBuilding, list):
			for currBuilding in aBuilding:
				currSquadId = squadIds[0]
				squadIds.pop(0)

				for groupUnit in self.__Units:
					u = groupUnit.myUnit
					if u.mySquadId == currSquadId:
						u.EnterBuilding(currBuilding, aInstantEnter)

				if len(squadIds) == 0:
					return
		else:
			currSquadId = squadIds[0]
			for groupUnit in self.__Units:
				u = groupUnit.myUnit
				if u.mySquadId == currSquadId:
					u.EnterBuilding(aBuilding, aInstantEnter)


	def UnitsEnterContainer( self, aStartIndex, aStopIndex, aContainerId, aInstantEnter = False ):

		if self.IsEmpty() or aStopIndex < aStartIndex or aStartIndex < 0 or aStopIndex >= self.Size():
			return

		for groupUnit in self.__Units[aStartIndex:aStopIndex+1]:
			u = groupUnit.myUnit
			u.EnterContainer( aContainerId, aInstantEnter )


	def UnitEnterContainer( self, aGroupUnit, aContainerId, aInstantEnter = False ):

		if aGroupUnit in self.__Units:
			u = aGroupUnit.myUnit
			u.EnterContainer( aContainerId, aInstantEnter )


	def EnterGroup( self, aGroupToEnter = None, aInstantFlag = False ):	
		
		debug.DebugMessage( 'Group(%s)::EnterGroup(%s)' % ( self.__Name, aGroupToEnter ), debug.EXCESSIVE )
		
		if aGroupToEnter is None:
			aGroupToEnter = self
		
		containers = []
		squadIds = []

		for groupUnit in aGroupToEnter.myUnits:
			if common.IsContainer( groupUnit.myUnitId ):
				containers.append( groupUnit.myUnitId )

		for groupUnit in self.__Units:
			if common.IsInfantry( groupUnit.myUnitId ) and not groupUnit.myUnit.mySquadId in squadIds:
				squadIds.append( groupUnit.myUnit.mySquadId )

		if len( squadIds ) == 0:
			return

		for c in containers:
			currentSquadId = squadIds[0]
			squadIds.pop(0)

			for groupUnit in self.__Units:
				if groupUnit.myUnit.mySquadId == currentSquadId:
					groupUnit.myUnit.EnterContainer( c, aInstantFlag )

			if len( squadIds ) == 0:
				return


	def UnloadAll( self ):
	
		for groupUnit in self.__Units:
			groupUnit.myUnit.UnloadAll()


	def UnloadFrom( self, aIndex ):

		if aIndex >= 0 and aIndex < self.Size():
			self.__Units[aIndex].myUnit.UnloadAll()


	def AttackTarget( self, aTarget ):
		
		try:
			targetPos = common.GetPosition( aTarget )
		except EmptyGroupException:
			debug.DebugMessage( 'Group(%s)::AttackTarget Failed! Invalid Target EmptyGroup(%s)' % (self.__Name, aTarget), debug.NONE )
			return False
		except unit.UnknownUnitException:
			debug.DebugMessage( 'Group(%s)::AttackTarget Failed! Invalid Target Unit(%d)' % (self.__Name, aTarget), debug.NONE )
			return False


		for groupUnit in self.__Units:
			groupUnit.myUnit.AttackPosition( targetPos )
			

	def AttackUnit( self, aUnitId ):

		for groupUnit in self.__Units:
			groupUnit.myUnit.AttackUnit( aUnitId )


	def AddCombatExceptionGroup( self, someGroups ):

		if isinstance( someGroups, list ):
			self.__CombatExceptionGroups.extend( someGroups )
		elif isinstance( someGroups, Group ):
			self.__CombatExceptionGroups.append( someGroups )
		else:
			raise NoneGroupException( 'Group(%s)::AddCombatExceptionGroup Warning! Trying to add a none-group object.' % self )

		
	def RemoveCombatExceptionGroup( self, someGroups ):
		
		if isinstance( someGroups, list ):
			for grp in someGroups:
				self.__CombatExceptionGroups.remove( grp )
		elif isinstance(someGroups, Group):
			self.__CombatExceptionGroups.remove( someGroups )
		else:
			raise NoneGroupException( 'Group(%s)::RemoveCombatExceptionGroup Warning! Trying to add a none-group object.' % self )


	def HoldFire( self, aFlag ):

		self.__HoldFire = aFlag

		for groupUnit in self.__Units:
			groupUnit.myUnit.myIsHoldingFire = self.__HoldFire


	def SetTransporterGroup( self, aFlag ):

		self.__IsTransporter = aFlag


	def ActivateRefillMode( self, aRefillLimit, aRefillAmount, aUnits, aSpawnTarget, aMoveRadius, aMoveTarget = None, aDelay = 0.0 ):

		self.__RefillMode = True
		self.__RefillLimit = aRefillLimit
		self.__RefillAmount = aRefillAmount
		self.__RefillUnits = aUnits
		self.__RefillSpawnTarget = aSpawnTarget
		self.__RefillMoveTarget = aMoveTarget
		self.__RefillMoveRadius = aMoveRadius
		self.__RefillDelay = aDelay
		self.__RefillCounter = 0

		try:
			self.__RefillLastLeaderPos = self.GetPosition()
		except EmptyGroupException:
			debug.DebugMessage( 'Group(%s)::ActivateRefillMode No Last Leader Position, EmptyGroup' % self.__Name, debug.NONE )
			self.__RefillLastLeaderPos = common.GetPosition( aSpawnTarget )

		self.TestForRefill()


	def UpdateRefillMode( self, aRefillLimit, aRefillAmount, aUnits, aSpawnTarget, aMoveRadius, aMoveTarget = None, aDelay = 0.0, aRemovePendingRefill = False ):
		
		self.DeactivateRefillMode( aRemovePendingRefill )
		self.ActivateRefillMode( aRefillLimit, aRefillAmount, aUnits, aSpawnTarget, aMoveRadius, aMoveTarget, aDelay )


	def UpdateRefillModeEx( self, aRefillLimit = None, aRefillAmount = None, aUnits = None, aSpawnTarget = None, aMoveRadius = None, aMoveTarget = None, aDelay = None, aRemovePendingRefill = False ):

		self.DeactivateRefillMode( aRemovePendingRefill )
		
		self.__RefillMode = True
		
		if aRefillLimit != None:
			self.__RefillLimit = aRefillLimit
		if aRefillAmount != None:
			self.__RefillAmount = aRefillAmount
		if aUnits != None:
			self.__RefillUnits = aUnits
		if aSpawnTarget != None:
			self.__RefillSpawnTarget = aSpawnTarget
		if aMoveTarget != None:
			self.__RefillMoveTarget = aMoveTarget
		if aMoveRadius != None:
			self.__RefillMoveRadius = aMoveRadius
		if aDelay != None:
			self.__RefillDelay = aDelay
		
		try:
			self.__RefillLastLeaderPos = self.GetPosition()
		except EmptyGroupException:
			debug.DebugMessage( 'Group(%s)::ActivateRefillMode No Last Leader Position, EmptyGroup' % self.__Name, debug.NONE )
			self.__RefillLastLeaderPos = common.GetPosition( self.__RefillSpawnTarget )
		
		self.TestForRefill()
		

	def DeactivateRefillMode( self, aRemovePendingRefill = False ):

		self.__RefillMode = False
		self.__RefillCounter = 0
		
		if aRemovePendingRefill:
			serverimports.RemoveReaction( self.__RefillPendingReaction )
			self.__RefillPendingRefill = False


	def PauseRefillMode( self, aPauseFlag ):
		
		self.__RefillMode = aPauseFlag
		
		if aPauseFlag:
			self.TestForRefill()
	
	
	def TestForRefill( self ):
		
		if self.__RefillMode and self.Size( True ) <= self.__RefillLimit and not self.__RefillPendingRefill:
			if self.__RefillDelay > 0.0:
				self.__RefillPendingRefill = True
				self.__RefillPendingReaction = serverimports.Delay( self.__RefillDelay, serverimports.Action( self.Refill ) )
			else:
				self.Refill()
		
		
	def Refill( self ):
		
		self.__RefillPendingRefill = False
		
		if self.__RefillAmount < 1 or len( self.__RefillUnits ) < 1:
			return

		unit_list = []
		for i in range( 0, self.__RefillAmount ):
			if self.__RefillCounter >= len( self.__RefillUnits ):
				self.__RefillCounter = 0
			unit_list.append( self.__RefillUnits[self.__RefillCounter] )
			self.__RefillCounter += 1

		if not self.__RefillMoveTarget is None:
			try:
				our_pos = common.GetPosition( self.__RefillMoveTarget )
			except EmptyGroupException:
				debug.DebugMessage( 'Group(%s)::Refill Failed! Invalid Target EmptyGroup(%s)' % ( self.__Name, aTarget ), debug.BRIEF )
				return
			except unit.UnknownUnitException:
				debug.DebugMessage( 'Group(%s)::Refill Failed! Invalid Target Unit(%d)' % ( self.__Name, aTarget ), debug.BRIEF )
				return

		else:
			try:
				our_pos = self.GetPosition()
			except EmptyGroupException:
				our_pos = self.__RefillLastLeaderPos
			except unit.UnknownUnitException:
				our_pos = self.__RefillLastLeaderPos
		
		self.__RefillLastLeaderPos = common.GetCopy( our_pos )


		tempGroup = serverimports.CreateGroup( None, [], self.__RefillSpawnTarget, serverimports.PLAYER_SCRIPT, self.__Team )
		tempGroup.SetParentGroup( self )
		if hasattr(self, "_Group__DropShipDirection"):
			tempGroup.SetDropshipDirection( self.__DropShipDirection )
		
		if self.__UseAirDrop:
			tempGroup.SetUseAirDrop( True )
		
		tempGroup.CreateGroup( unit_list, self.__RefillSpawnTarget, serverimports.PLAYER_SCRIPT, self.__Team )
		tempGroup.SetState( 'RefillGroup' )
		self.__RefillGroups.append( tempGroup )

		if len( self.__RefillCommandQueue ) == 0 and not self.__UseAirDrop:
			tempGroup.MoveGroup( wicmath.CalculateRandomPosition( our_pos, self.__RefillMoveRadius ) )
			self.AddUnits( tempGroup.myUnits )
			
			self.SetOwner( self.__Owner )
			self.SetTeam( self.__Team )
			
			tempGroup.RemoveAllUnits()
			self.__RefillGroups.remove( tempGroup )
			serverimports.RemoveGroup( tempGroup )
			serverimports.PostEvent( 'Refill', self )
		else:
			if self.__UseAirDrop:
				tempGroup.PostCommand( command.CMD_WaitUntilNextDrop() )
				
			for cmd_action in self.__RefillCommandQueue[:]:
				refill_cmd = cmd_action()
				tempGroup.PostCommand( refill_cmd )
		
			actAddUnits = serverimports.Action( self.AddUnits, tempGroup.myUnits )
			
			actSetOwner = serverimports.Action( self.SetOwner, self.__Owner )
			actSetTeam = serverimports.Action( self.SetTeam, self.__Team )

			actRemoveUnits = serverimports.Action( tempGroup.RemoveAllUnits )
			actRefillRemove = serverimports.Action( self.__RefillGroups.remove, tempGroup )
			actRemoveGroup = serverimports.Action( serverimports.RemoveGroup, tempGroup )
			actPostEvent = serverimports.Action( serverimports.PostEvent, 'Refill', self )
			
			tempGroup.PostCommand( command.CMD_CustomCommand( [actAddUnits, actSetOwner, actSetTeam, actRemoveUnits, actRefillRemove, actRemoveGroup, actPostEvent] ) )
		
	
	def SetParentGroup( self, aGroup ):
		
		self.__ParentGroup = aGroup
		
		
	def PostRefillCommand( self, aAction ):
		
		self.__RefillCommandQueue.append( aAction )


	def GetRefillCommands( self ):
		
		return self.__RefillCommandQueue


	def ClearRefillCommands( self ):
		
		self.__RefillCommandQueue = []


	def PostCommand( self, aCommand, aType = CMD_PRIMARY ):

		aCommand.SetGroup( self )

		if aType == CMD_PRIMARY:
			self.__PrimaryCommands.append( aCommand )
		elif aType == CMD_ATTACK:
			self.__AttackCommands.append( aCommand )
		elif aType == CMD_BASE:
			self.__BaseCommands.append( aCommand )

		return aCommand


	def PushCommand( self, aCommand, aType = CMD_PRIMARY ):

		self.RestartCommand( aType )

		aCommand.SetGroup( self )

		if aType == CMD_PRIMARY:
			self.__PrimaryCommands.insert( 0, aCommand )
		elif aType == CMD_ATTACK:
			self.__AttackCommands.insert( 0, aCommand )
		elif aType == CMD_BASE:
			self.__BaseCommands.insert( 0, aCommand )

		return aCommand


	def InsertCommand( self, aCommand, aIndex, aType = CMD_PRIMARY ):

		aCommand.SetGroup( self )

		if aType == CMD_PRIMARY:
			self.__PrimaryCommands.insert( aIndex, aCommand )
		elif aType == CMD_ATTACK:
			self.__AttackCommands.insert( aIndex, aCommand )
		elif aType == CMD_BASE:
			self.__BaseCommands.insert( aIndex, aCommand )

		return aCommand


	def PopCommand( self, aType = CMD_PRIMARY ):

		if aType == CMD_PRIMARY and len( self.__PrimaryCommands ):
			self.__PrimaryCommands.pop( 0 )
		elif aType == CMD_ATTACK and len( self.__AttackCommands ):
			self.__AttackCommands.pop( 0 )
		elif aType == CMD_BASE and len( self.__BaseCommands ):
			self.__BaseCommands.pop( 0 )


	def PeekCommand( self, aType = CMD_PRIMARY ):

		if aType == CMD_PRIMARY and len( self.__PrimaryCommands ):
			return self.__PrimaryCommands[0]
		elif aType == CMD_ATTACK and len( self.__AttackCommands ):
			return self.__AttackCommands[0]
		elif aType == CMD_BASE and len( self.__BaseCommands ):
			return self.__BaseCommands[0]

		return None


	def ClearCommands( self, aType = CMD_PRIMARY ):

		if aType == CMD_PRIMARY:
			self.__PrimaryCommands = []
		elif aType == CMD_ATTACK:
			self.__AttackCommands = []
		elif aType == CMD_BASE:
			self.__BaseCommands = []


	def RestartCommand( self, aType = CMD_PRIMARY ):

		if aType == CMD_PRIMARY and len( self.__PrimaryCommands ):
			self.__PrimaryCommands[0].Restart()
		elif aType == CMD_ATTACK and len( self.__AttackCommands ):
			self.__AttackCommands[0].Restart()
		elif aType == CMD_BASE and len( self.__BaseCommands ):
			self.__BaseCommands[0].Restart()


	def GetCommands( self, aType = CMD_PRIMARY ):

		if aType == CMD_PRIMARY:
			return self.__PrimaryCommands
		elif aType == CMD_ATTACK:
			return self.__AttackCommands
		elif aType == CMD_BASE:
			return self.__BaseCommands
			
			
	def SetExperienceLevel( self, aLevel ):
		for groupUnit in self.__Units:
			wicg.SetExperienceLevel( groupUnit.myUnitId, aLevel )


	def SetMaxExperienceLevel( self ):
		for groupUnit in self.__Units:
			wicg.SetExperienceLevel( groupUnit.myUnitId, 4 )	
			
	
	def SetDropshipDirection( self, aDirection ):	
		
		if not isinstance( aDirection, Position ):
			debug.DebugMessage( 'Groups::SetDropshipDirection on %s, aDirection need to be a Position.' % aGroupName )
		
		self.__DropShipDirection = aDirection
			
			

