import wicg
import wicg_common as common
import debug
import unit
import group

## math imports
import random
import math
from wicmath import *
import position

## group imports
from command import *
from globals import *

import serverimports


class BehaviorManager( object ):
	"""
	"""
	
	def __init__( self, aGroup ):
		"""
		"""
		
		self.__BaseBehavior = None
		self.__AttackBehavior = None
		self.__BaseReaction = None
		self.__AttackReaction = None
		self.__StartAttackReaction = None
		self.__Group = aGroup


	def Shutdown( self ):
		
		if self.__BaseReaction:
			serverimports.RemoveReaction( self.__BaseReaction )
			self.__BaseReaction = None
			
		if self.__AttackReaction:
			serverimports.RemoveReaction( self.__AttackReaction )
			self.__AttackReaction = None

		if self.__StartAttackReaction:
			serverimports.RemoveReaction( self.__StartAttackReaction )
			self.__StartAttackReaction = None


	def __str__( self ):
		"""
		"""
		
		if self.__Group:
			groupName = self.__Group.myName
		else:
			groupName = 'NoGroup'
		
		return '%s(%s)' % (self.__class__.__name__, groupName)


	def __getBaseBehavior( self ):
		"""
		"""
		
		return self.__BaseBehavior
		
	myBaseBehavior = property( __getBaseBehavior )


	def __getAttackBehavior( self ):
		"""
		"""
		
		return self.__AttackBehavior

	myAttackBehavior = property( __getAttackBehavior )


	def ActivateBaseBehavior( self, aNewBehavior ):
				
		if not aNewBehavior:
			return
		
		self.__BaseBehavior = aNewBehavior
		self.__BaseBehavior.SetGroup( self.__Group )
		self.__BaseBehavior.Start()
		
		if self.__BaseReaction:
			serverimports.RemoveReaction( self.__BaseReaction )
			self.__BaseReaction = None
		
		## add a small random value to prevent multiple updates at the same frame
		r = random.random()
		self.__BaseReaction = serverimports.Repeat( self.__BaseBehavior.GetUpdateTime() + r, serverimports.Action( self.UpdateBaseBehavior ) )
		
	
	def UpdateBaseBehavior( self ):
		
		if not self.__BaseBehavior:
			return
		
		self.__BaseBehavior.Update()


	def ActivateAttackBehavior( self, aNewBehavior ):
		
		self.__AttackBehavior = aNewBehavior
		self.__AttackBehavior.SetGroup( self.__Group )
		
		self.StartAttackReaction()


	def UpdateAttackBehavior( self, anUnitId = -1, anAttackerId = -1 ):
		
		if self.__AttackBehavior is None:
			return
		
		## if ids are -1 we have been called by a reaction ( GroupInCombat )
		if anUnitId == -1:
			anUnitId = serverimports.theReactions.myEventData[1]
		if anAttackerId == -1:
			anAttackerId = serverimports.theReactions.myEventData[2]
		
		doExecute = True
		
		try:
			unit.theUnits[anUnitId]
			unit.theUnits[anAttackerId]
		except unit.UnknownUnitException:
			debug.DebugMessage( 'Behaviors(%s)::UpdateAttackBehavior (%d, %d) Warning! unknown unit' % (self.__Group, anUnitId, anAttackerId), debug.NONE )
			doExecute = False
		
		
		if doExecute:
			self.__AttackBehavior.Execute( anUnitId, anAttackerId )
		
		self.__AttackReaction = None
		self.__StartAttackReaction = serverimports.Delay( self.__AttackBehavior.GetUpdateTime(), serverimports.Action( self.StartAttackReaction ) )


	def StartAttackReaction( self ):

		if self.__AttackReaction:
			serverimports.RemoveReaction( self.__AttackReaction )
			self.__AttackReaction = None

		self.__AttackReaction = serverimports.RE_OnGroupInCombat( self.__Group, serverimports.Action( self.UpdateAttackBehavior ) )
		
	
	def Pause( self ):
		
		if self.__BaseReaction:
			serverimports.RemoveReaction( self.__BaseReaction )
			self.__BaseReaction = None
			
		if self.__AttackReaction:
			serverimports.RemoveReaction( self.__AttackReaction )
			self.__AttackReaction = None

		if self.__StartAttackReaction:
			serverimports.RemoveReaction( self.__StartAttackReaction )
			self.__StartAttackReaction = None

		
	
	def UnPause( self ):
		
		if self.__BaseReaction:
			serverimports.RemoveReaction( self.__BaseReaction )
			self.__BaseReaction = None
		
		if self.__BaseBehavior:
			self.__BaseReaction = serverimports.Repeat( self.__BaseBehavior.GetUpdateTime(), serverimports.Action( self.UpdateBaseBehavior ) )
		
		self.StartAttackReaction()



class Behavior( object ):
	

	def __init__( self ):
		
		self.myGroup = None
		self.myUpdateTime = 1.0


	def __str__( self ):
		
		return "%s(%s)" % ( self.__class__.__name__, self.myGroup )

		
	
	def SetGroup( self, aGroup ):
		
		self.myGroup = aGroup


	def GetUpdateTime( self ):

		return self.myUpdateTime


""" Base behaviors """
class BaseBehavior( Behavior ):

	
	def __init__( self ):
		
		Behavior.__init__( self )


	def Start( self ):
		
		pass


	def Update( self ):
		
		pass
	

class BHB_Idle( BaseBehavior ):

	
	def __init__( self ):
		
		BaseBehavior.__init__( self )
		self.myUpdateTime = 60.0

	
class BHB_Artillery( BaseBehavior ):

	
	def __init__( self, aDelay = 6.0, aOffset = 0.0, aExcludeList = None ):
		
		BaseBehavior.__init__( self )
		self.myUpdateTime = aDelay
		self.__Offset = aOffset
		self.__ExcludeList = aExcludeList
	
	
	def Start( self ):

		BaseBehavior.Start( self )
		
		self.Update()

	
	def Update( self ):
		
		BaseBehavior.Update( self )
		
		if self.myGroup.IsEmpty():
			return
		
		target = self.FindTarget()
		
		self.myGroup.ClearCommands( CMD_BASE )
		
		if target is None:
			self.myGroup.PostCommand( CMD_StopGroup( ), CMD_BASE )
		else:
			self.myGroup.PostCommand( CMD_AttackArea( unit.theUnits[target].myPos, self.__Offset ), CMD_BASE )
	
	
	def FindTarget( self ):
		
		if self.myGroup.IsEmpty():
			return None

		leaderUnit = self.myGroup.GetLeader().myUnit
		
		enemies = wicg.GetVisibleEnemyUnitsInArea( leaderUnit.myTeam, self.myGroup.GetPosition(), leaderUnit.myMaxRange )

		if not len( enemies ):
			return None
		
		exludedUnit = False
		
		while len( enemies ):
			exludedUnit = False
			targetUnitId = random.choice( enemies )
			enemies.remove( targetUnitId )
			
			# if the unit is in the exclude area list its not a valid target
			if self.__ExcludeList:
				for area in self.__ExcludeList:
					if wicmath.Distance( unit.theUnits[targetUnitId].myPos, area.myPos ) < area.myRadius:
						exludedUnit = True
			
			if exludedUnit:
				continue
			
			if not self.myGroup.IsUnitInCombatExceptionGroup( targetUnitId ):
				if wicmath.Distance( leaderUnit.myPos, unit.theUnits[targetUnitId].myPos ) >= leaderUnit.myMinRange:
					return targetUnitId

		return None


class BHB_AreaArtillery( BaseBehavior ):
	
	def __init__( self, someAreas, aDelay, aSpreadFire = False, aShootDelay = 0.0 ):
		
		BaseBehavior.__init__( self )
		
		self.myUpdateTime = aDelay
		
		if isinstance( someAreas, list ):
			self.__Areas = someAreas
		else:
			self.__Areas = [someAreas]
			
		self.__SpreadFire = aSpreadFire
		self.__ShootDelay = aShootDelay
	
	
	def Start( self ):

		BaseBehavior.Start( self )
		
		self.Update()

	
	def Update( self ):
		
		BaseBehavior.Update( self )
		
		if self.myGroup.IsEmpty() or len( self.__Areas ) == 0:
			return
		
		
		attackArea = None
		
		if self.__SpreadFire:
			attackArea = random.choice( self.__Areas )
			
		for groupUnit in self.myGroup.myUnits:
			
			if not self.__SpreadFire:
				attackArea = random.choice( self.__Areas )
			
			targetPosition = position.Position( attackArea.myPosition.myX, attackArea.myPosition.myY, attackArea.myPosition.myZ )
			targetPosition.myX += random.randint(-int(attackArea.myRadius), int(attackArea.myRadius))
			targetPosition.myZ += random.randint(-int(attackArea.myRadius), int(attackArea.myRadius))
			
			if self.__ShootDelay > 0.0:
				shootDelay = random.uniform( 0.0, self.__ShootDelay )
				serverimports.Delay( shootDelay, serverimports.Action( self.Fire, groupUnit, targetPosition ) )
			else:
				self.Fire( groupUnit, targetPosition )
				
				
	def Fire( self, aGroupUnit, aTargetPos ):
		
		try:
			if self.myGroup.myOwner == 0: # script
				aGroupUnit.myUnit.AttackPosition( aTargetPos )
				#this would be more correct
				#self.myGroup.PostCommand( CMD_AttackTarget( aTargetPos ) )
		except unit.UnknownUnitException:
			pass



class BHB_Patrol( BaseBehavior ):

	def __init__( self, aWayPoints, aDelayMode = BHB_PATROL_NO_DELAY, aDelayTime = 0.0, aPatrolMode = BHB_PATROL_NORMAL, aAllAtTarget = False, aLimit = CLOSE_TO_LIMIT ):

		BaseBehavior.__init__(self)
		self.myUpdateTime = 2.5
		self.__WayPoints = aWayPoints
		self.__Limit = aLimit
	
		self.__PatrolMode = aPatrolMode
	
		self.__DelayMode = aDelayMode
		self.__DelayTime = aDelayTime
		
		self.__CurrentWayPoint = -1
		self.__CounterModifier = 1
		
		self.__AllAtTarget = aAllAtTarget
		

	def Start( self ):

		BaseBehavior.Start( self )

		self.Update()
		
		self.myGroup.ClearCommands( CMD_BASE )


	def Update( self ):

		BaseBehavior.Update( self )

		if self.myGroup.IsEmpty():
			return

		if len( self.myGroup.GetCommands( CMD_BASE ) ) or len( self.myGroup.GetCommands( CMD_PRIMARY ) ) or len( self.myGroup.GetCommands( CMD_ATTACK ) ):
			return

		useDelay = False

		serverimports.PostEvent( 'PatrolAtTarget', self.myGroup )

		if self.__DelayMode == BHB_PATROL_ALLPOINTS_DELAY:
			useDelay = True

		if self.__PatrolMode == BHB_PATROL_RANDOM:
			nrOfWayPoints = len( self.__WayPoints )
			self.__CurrentWayPoint = random.randint( 0, nrOfWayPoints - 1 )
		else:
			self.__CurrentWayPoint += self.__CounterModifier
			
			if self.__PatrolMode == BHB_PATROL_CIRCULAR:
				if self.__CurrentWayPoint >= len( self.__WayPoints ):
					self.__CurrentWayPoint = 0
					
					if self.__DelayMode == BHB_PATROL_ENDPOINTS_DELAY:
						useDelay = True
			else:
				if self.__CurrentWayPoint >= len( self.__WayPoints ):
					self.__CurrentWayPoint -= 2
					self.__CounterModifier = -1
					
					if self.__DelayMode == BHB_PATROL_ENDPOINTS_DELAY:
						useDelay = True
	
				if self.__CurrentWayPoint <= -1:
					self.__CurrentWayPoint = 1
					self.__CounterModifier = 1
					
					if self.__DelayMode == BHB_PATROL_ENDPOINTS_DELAY:
						useDelay = True
	
				if self.__CurrentWayPoint >= len( self.__WayPoints ):
					self.__CurrentWayPoint = 0
					self.__CounterModifier = 1
	
					if self.__DelayMode == BHB_PATROL_ENDPOINTS_DELAY:
						useDelay = True
			
		self.myGroup.ClearCommands( CMD_BASE )
			
		if useDelay and self.__DelayTime > 0.0:
			self.myGroup.PostCommand( CMD_Wait( self.__DelayTime ), CMD_BASE )
			
		self.myGroup.PostCommand( CMD_MoveGroup( self.__WayPoints[self.__CurrentWayPoint], self.__Limit, None, None, (not self.__AllAtTarget) ), CMD_BASE )


class BHB_MoveRandomly( BaseBehavior ):
	"""
	"""
	
	def __init__( self, aDelay = 24.0, aMoveDistance = 36, aTarget = None, aRegroup = False, aRegroupTarget = None ):
		"""
		"""
		
		BaseBehavior.__init__( self )
		self.myUpdateTime = aDelay
		self.__MoveDistance = aMoveDistance
		self.__Target = aTarget
		self.__Regroup = aRegroup
		self.__RegroupTarget = aRegroupTarget
	
	def Start( self ):
		"""
		"""
		BaseBehavior.Start( self )
		
		self.Update()

	
	def Update( self ):
		"""
		"""
		
		BaseBehavior.Update( self )
		
		if self.myGroup.IsEmpty():
			return
		
		if self.__Target:
			move_pos = common.GetPosition( self.__Target )
		else:
			move_pos = self.myGroup.GetPosition()
			
		move_pos = common.GetCopy( move_pos )
		
		move_pos.myX += random.uniform( -self.__MoveDistance, self.__MoveDistance )
		move_pos.myZ += random.uniform( -self.__MoveDistance, self.__MoveDistance )
		
		self.myGroup.ClearCommands( CMD_BASE )
		self.myGroup.PostCommand( CMD_MoveGroup( move_pos ), CMD_BASE )
		
		if self.__Regroup:
			self.myGroup.PostCommand( CMD_RegroupAt( move_pos, self.__RegroupTarget ), CMD_BASE )
	

class BHB_GroupHealer( BaseBehavior ):
	
	def __init__( self, someGroupsToHeal, aDistanceImpact = 1.0 ):
		
		BaseBehavior.__init__( self )
		self.myUpdateTime = 3.0
		
		
		if not isinstance( someGroupsToHeal ,list ):
			self.__GroupsToHeal = [someGroupsToHeal]
		else:
			self.__GroupsToHeal = someGroupsToHeal
		
		
		self.__DistanceImpact = aDistanceImpact

		
	def Start( self ):
		
		BaseBehavior.Start( self )


	def Update( self ):
		
		HEAL_DISTANCE = 6
		SPLIT_LIMIT = 2
		
		BaseBehavior.Update( self )
		
		unitsToHeal = []
		
		
		if self.myGroup.IsEmpty():
			return
		
		
		for grp in self.__GroupsToHeal:
			if not grp.IsEmpty():
				unitsToHeal.extend( grp.myUnits )
		
		if len( unitsToHeal ) == 0:
			return
		
		## we have already done an empty group check above
		ourPos = self.myGroup.GetPosition()
		
		bestUnit = 0
		bestValue = -1
		nextBestUnit = 0
		nextBestValue = 0
		
		for grpUnit in unitsToHeal:
			
			try:
				u = grpUnit.myUnit
			except unit.UnknownUnitException:
				debug.DebugMessage( 'BHV_GroupHealer::Update Error(A)! (no such unit) %s' % self.myGroup.myName, debug.NONE )
				return
			
			health_ratio = 1.0 / (((float(u.myHealth) + 1.0) / (float(u.myMaxHealth) + 1.0)) + 0.001)			
			distance_ratio = (float(self.__DistanceImpact)) / (wicmath.Distance( ourPos, u.myPos ) + 1.0)

			if health_ratio < 1.0:
				health_ratio = 0.0

			current_value = health_ratio * distance_ratio

			if current_value > bestValue:
				bestUnit = u
				bestValue = current_value
			elif current_value > nextBestValue:
				nextBestUnit = u
				nextBestValue = current_value
		
		
		try:		
			targetPos = bestUnit.myPos
		except unit.UnknownUnitException:
			debug.DebugMessage( 'BHV_GroupHealer::Update Error(B)! (no such unit) %s' % self.myGroup.myName, debug.NONE )
			return

		targetPos = wicmath.NearPosition( self.myGroup.GetPosition(), targetPos, HEAL_DISTANCE )
		self.myGroup.ClearCommands( CMD_BASE )
		self.myGroup.PostCommand( CMD_MoveGroup( targetPos, 64 ), CMD_BASE )
		
		if self.myGroup.Size() > SPLIT_LIMIT and nextBestValue > 0.0:
			try:
				secondTargetPos = nextBestUnit.myPos
			except unit.UnknownUnitException:
				debug.DebugMessage( 'BHV_GroupHealer::Update Error(C)! (no such unit) %s' % self.myGroup.myName, debug.NONE )
				return
			
			secondTargetPos = wicmath.NearPosition( self.myGroup.GetPosition(), secondTargetPos, HEAL_DISTANCE )
			
			try:
				self.myGroup.PostCommand( CMD_MoveUnit( self.myGroup.myUnits[-1], secondTargetPos ), CMD_BASE )
			except unit.UnknownUnitException:
				debug.DebugMessage( 'BHV_GroupHealer::Update Error(D)! (no such unit) %s' % self.myGroup.myName, debug.NONE )
				return


class BHB_RepairInAreas( BaseBehavior ): 

	def __init__( self, someAreas ):
		BaseBehavior.__init__( self )
		self.myUpdateTime = 3.0
		
		if not isinstance( someAreas ,list ):
			self.__AreasToRepairIn = [someAreas]
		else:
			self.__AreasToRepairIn = someAreas		
			
	
	def Start( self ):
		
		BaseBehavior.Start( self )


	def Update( self ):
		debug.DebugMessage( 'BHB_Repair' )
		BaseBehavior.Update( self )
		
		if self.myGroup.IsEmpty():
			return		
		
		RepairUnits = [ ]

		for aUnit in self.myGroup.myUnits:
			if common.IsRepairUnit( aUnit.myUnitId ):
				RepairUnits.append( aUnit.myUnitId )				  
		
		if len( RepairUnits ) == 0:
			return
		
		unitsToHeal = [ ]
				
		for area in self.__AreasToRepairIn:			
			for unitId in area.myUnits:
				if unit.theUnits[unitId].myTeam == self.myGroup.myTeam:
					if unit.theUnits[unitId].myHealth != unit.theUnits[unitId].myMaxHealth:
						if unit.theUnits[unitId].myOwner == serverimports.PLAYER_HUMAN:
							unitsToHeal.insert( 0, unitId )
						else:
							unitsToHeal.append( unitId )			

		if len( unitsToHeal ) == 0:
			return

		counter = 0			
		for repairer in RepairUnits:
			if len( unitsToHeal ) > counter:
				wicg.UnitRepair( repairer, unitsToHeal[ counter ] )
				counter +=1
		

	
		

class BHB_IdleUnits( BaseBehavior ):

	def __init__( self, aWantedPosition = None, aDistanceLimit = CLOSE_TO_LIMIT * 2, aShortMoveDistance = 8, aShortMoveChance = 0.25, aLongMoveDistance = 18, aLongMoveChance = 0.2, aOnlyMoveInfantry = False, aUseCover = False ):
		
		BaseBehavior.__init__( self )
		self.myUpdateTime = 6.5
		
		self.__ShortMoveDistance = aShortMoveDistance
		self.__ShortMoveChance = aShortMoveChance
		self.__LongMoveDistance = aLongMoveDistance
		self.__LongMoveChance = aLongMoveChance
		self.__WantedPosition = aWantedPosition
		self.__DistanceLimit = aDistanceLimit
		self.__OnlyMoveInfantry = aOnlyMoveInfantry
		self.__UseCover = aUseCover


	def Start( self ):
		BaseBehavior.Start( self )
		self.Update()


	def Update( self ):
		BaseBehavior.Update( self )
		
		if len( self.myGroup.GetCommands( CMD_BASE ) ):
			return
		
		self.myGroup.ClearCommands( CMD_BASE )
		self.myGroup.PushCommand( CMD_CustomCommand( self.MoveUnits ), CMD_BASE )


	def MoveUnits( self ):
		
		if self.myGroup.Size() == 0:
			return
		
		if self.__WantedPosition:
			try:
				target_pos = common.GetCopy( common.GetPosition( self.__WantedPosition ) )
			except group.EmptyGroupException:
				target_pos = common.GetCopy( self.myGroup.GetPosition() )
			except unit.UnknownUnitException:
				target_pos = common.GetCopy( self.myGroup.GetPosition() )
		else:
			target_pos = common.GetCopy( self.myGroup.GetPosition() )

		
		if self.__WantedPosition is None:			
			if self.myGroup.Size() < 2:
				return
			units = self.myGroup.myUnits[1:]
		else:
			units = self.myGroup.myUnits[:]
		
		if random.random() < self.__LongMoveChance:
			
			u = random.choice( units )
			
			## no long move order if we are outside perimeter
			if wicmath.Distance( u.myUnit.myPos, target_pos ) <= self.__DistanceLimit:			
				unit_pos = u.myUnit.myPos
				long_move_dir = wicmath.GetVector( target_pos, unit_pos )
				target_pos_vec = wicmath.Position2Vector( target_pos )
				long_move_vec = target_pos_vec + ( long_move_dir * self.__LongMoveDistance )
				long_move_pos = wicmath.Vector2Position( long_move_vec )
				
				if self.__OnlyMoveInfantry:
					if common.IsInfantry( u.myUnitId ):
						if self.__UseCover:
							self.myGroup.MoveUnitCover( u, long_move_pos )
						else:
							self.myGroup.MoveUnit( u, long_move_pos )
				else:
					if self.__UseCover:
						self.myGroup.MoveUnitCover( u, long_move_pos )
					else:
						self.myGroup.MoveUnit( u, long_move_pos )
				
				units.pop( units.index( u ) )
		

		for u in units:
							
			my_pos = common.GetCopy( u.myUnit.myPos )
			
			if wicmath.Distance( my_pos, target_pos ) > self.__DistanceLimit:
				direction = my_pos - target_pos
				direction.Normalize()
				l = self.__DistanceLimit * random.random()
				
				move_pos = target_pos + ( direction * l )
				
				if self.__OnlyMoveInfantry:
					if common.IsInfantry( u.myUnitId ):
						if self.__UseCover:
							self.myGroup.MoveUnitCover( u, move_pos )
						else:
							self.myGroup.MoveUnit( u, move_pos )
				else:
					if self.__UseCover:
						self.myGroup.MoveUnitCover( u, move_pos )
					else:
						self.myGroup.MoveUnit( u, move_pos )
			else:
				if random.random() < self.__ShortMoveChance:
					move_pos = common.GetCopy( target_pos )
					move_pos.myX += random.uniform( -self.__ShortMoveDistance, self.__ShortMoveDistance )
					move_pos.myZ += random.uniform( -self.__ShortMoveDistance, self.__ShortMoveDistance )
					
					if self.__OnlyMoveInfantry:
						if common.IsInfantry( u.myUnitId ):
							if self.__UseCover:
								self.myGroup.MoveUnitCover( u, move_pos )
							else:
								self.myGroup.MoveUnit( u, move_pos )
					else:
						if self.__UseCover:
							self.myGroup.MoveUnitCover( u, move_pos )
						else:
							self.myGroup.MoveUnit( u, move_pos )


class BHB_IdleInfantry( BHB_IdleUnits ):
	
	def __init__( self, aWantedPosition = None, aDistanceLimit = CLOSE_TO_LIMIT * 2, aShortMoveDistance = 8, aShortMoveChance = 0.25, aLongMoveDistance = 18, aLongMoveChance = 0.2 ):
		
		BHB_IdleUnits.__init__( self, aWantedPosition, aDistanceLimit, aShortMoveDistance, aShortMoveChance, aLongMoveDistance, aLongMoveChance, True )
		self.__OnlyMoveInfantry = True


class BHB_IdleInfantryCover( BHB_IdleUnits ):
	
	def __init__( self, aWantedPosition = None, aDistanceLimit = CLOSE_TO_LIMIT * 2, aShortMoveDistance = 8, aShortMoveChance = 0.25, aLongMoveDistance = 18, aLongMoveChance = 0.2 ):
		
		BHB_IdleUnits.__init__( self, aWantedPosition, aDistanceLimit, aShortMoveDistance, aShortMoveChance, aLongMoveDistance, aLongMoveChance, True, True )
	

class BHB_CaptureCommandPoint( BaseBehavior ):

	def __init__( self, somePerimeterPoints ):
		
		BaseBehavior.__init__( self )
		self.myUpdateTime = 12.0
		
		if isinstance( somePerimeterPoints, list ):
			self.__PerimeterPoints = somePerimeterPoints
		else:
			self.__PerimeterPoints = [somePerimeterPoints]


	def Start( self ):
		BaseBehavior.Start( self )
		self.Update()


	def Update( self ):
		BaseBehavior.Update( self )
	
		self.myGroup.ClearCommands( CMD_BASE )
		self.myGroup.PushCommand( CMD_MoveMultipleTargets( self.__PerimeterPoints ), CMD_BASE )


class BHB_HoldPosition( BaseBehavior ):
	"""
	"""

	def __init__( self, aTarget, aLimit = CLOSE_TO_LIMIT ):
		
		BaseBehavior.__init__( self )
		self.myUpdateTime = 8.0
		self.__Target = aTarget
		self.__Limit = aLimit


	def Start( self ):
		BaseBehavior.Start( self )
		self.Update()


	def Update( self ):
		BaseBehavior.Update( self )
	
		if self.myGroup.Size() == 0:
			return
		
		self.myGroup.ClearCommands( CMD_BASE )
		
		grpPos = self.myGroup.GetPosition()
		
		try:
			targetPos = common.GetPosition( self.__Target )
		except group.EmptyGroupException:
			debug.DebugMessage( 'BHB_HoldPosition Failed! Invalid Target EmptyGroup(%s)' % (self.__Target), debug.NONE )
			return
		except unit.UnknownUnitException:
			debug.DebugMessage( 'BHB_HoldPosition Failed! Invalid Target Unit(%d)' % (self.__Target), debug.NONE )
			return
			
		if wicmath.Distance( grpPos, targetPos ) < self.__Limit:
			return
	
		self.myGroup.PushCommand( CMD_MoveGroup( self.__Target ), CMD_BASE )






### davidh 080707.
class BHB_RegroupAt( BaseBehavior ):
	"""
	"""

	def __init__( self, aTarget, aLookAtTarget, aLimit = CLOSE_TO_LIMIT  ):
		
		BaseBehavior.__init__( self )
		self.myUpdateTime = 8.0
		self.__Target = aTarget
		self.__LookAt = aLookAtTarget
		self.__Limit = aLimit


	def Start( self ):
		BaseBehavior.Start( self )
		self.Update()


	def Update( self ):
		BaseBehavior.Update( self )
	
		if self.myGroup.Size() == 0:
			return
		
		self.myGroup.ClearCommands( CMD_BASE )
		
		grpPos = self.myGroup.GetPosition()

		try:
			targetPos = common.GetPosition( self.__Target )
		except group.EmptyGroupException:
			debug.DebugMessage( 'BHB_HoldPosition Failed! Invalid Target EmptyGroup(%s)' % (self.__Target), debug.NONE )
			return			
		except unit.UnknownUnitException:
			debug.DebugMessage( 'BHB_HoldPosition Failed! Invalid Target Unit(%d)' % (self.__Target), debug.NONE )
			return

		Regroup = False
		for aUnit in self.myGroup.myUnits:
			dist = wicmath.Distance( common.GetPosition( self.__Target ), aUnit.myPos )
			
			if dist > self.__Limit:
				self.myGroup.PushCommand( CMD_RegroupAt( self.__Target, self.__LookAt ), CMD_BASE )     
				return  
	












""" Attack behaviors """
class AttackBehavior( Behavior ):

	
	def __init__( self ):
		
		Behavior.__init__( self )


	def Execute( self, aUnitId, aAttackerId ):
		
		pass
			
	
	def Defend( self, aUnitId, aAttackerId, aDistance ):
		
		if self.myGroup.IsEmpty():
			return
		
		WAIT_TIME = 6.5
		
		our_pos = self.myGroup.GetPosition()
		our_vec = wicmath.Position2Vector( our_pos )
		
		target = unit.theUnits[aAttackerId].myPos
		
		distance = wicmath.Distance( self.myGroup.GetPosition(), target )
		
		direction_vec = wicmath.GetVector( our_pos, target )
		direction_pos = wicmath.Vector2Position( direction_vec )
		
		heading = wicmath.GetHeading( wicmath.Position2Vector( our_pos ), wicmath.Position2Vector( target ) )
		
		move_pos = wicmath.Vector2Position(our_vec + (direction_vec * (distance - aDistance)))

		self.myGroup.PushCommand( CMD_Wait( WAIT_TIME ), CMD_ATTACK )
		self.myGroup.PushCommand( CMD_LookAt( target ), CMD_ATTACK )
		self.myGroup.PushCommand( CMD_Wait( 1.0 ), CMD_ATTACK )
		
		move_distance = wicmath.Distance( our_pos, move_pos )
		
		if distance >= (aDistance / random.randint(2, 4)) and move_distance >= 8:
			self.myGroup.PushCommand( CMD_MoveGroup( move_pos, CLOSE_TO_LIMIT, None, heading ), CMD_ATTACK )
		

	def Flee( self, aUnitId, aAttackerId, aFleeDistance ):

		if self.myGroup.IsEmpty():
			return

		RANDOM_DISTANCE = 24
		WAIT_TIME = 2
		
		attacker_pos = unit.theUnits[aAttackerId].myPos
		pos = self.myGroup.GetPosition()
		pos_vec = wicmath.Position2Vector( pos )
		
		move_pos = wicmath.Vector2Position( pos_vec + ( wicmath.GetVector( attacker_pos, pos ) * aFleeDistance ) )

		offset_x = random.randint( -RANDOM_DISTANCE, RANDOM_DISTANCE )
		offset_z = random.randint( -RANDOM_DISTANCE, RANDOM_DISTANCE )
		
		move_pos.myX += offset_x
		move_pos.myZ += offset_z
		
		self.myGroup.PushCommand( CMD_Wait( WAIT_TIME ), CMD_ATTACK )
		self.myGroup.PushCommand( CMD_MoveGroup( move_pos ), CMD_ATTACK )


	def Flank( self, aUnitId, aAttackerId, aDistanceScale, aAllFlank = False, aBehindFlank = True ):
		
		FLANK_DISTANCE = 92 * aDistanceScale
		BEHIND_DISTANCE = 58 * aDistanceScale
		WAIT_TIME = 6
		FRONT_DISTANCE = 52 * aDistanceScale

		if self.myGroup.IsEmpty():
			return

		if self.myGroup.Size() < 2:
			return

		half_group = self.myGroup.Size() / 2

		our_pos = self.myGroup.GetPosition()
		target_pos = unit.theUnits[aAttackerId].myPos
		
		if random.randint(0, 1):
			flank_pos = wicmath.CalculateFlankPosition( our_pos, target_pos, math.pi / 2.5, FLANK_DISTANCE )
		else:
			flank_pos = wicmath.CalculateFlankPosition( our_pos, target_pos, math.pi / 2.5, FLANK_DISTANCE, True )
		
		if aBehindFlank:
			behind_pos = wicmath.CalculateBehindPosition( our_pos, target_pos, BEHIND_DISTANCE )

		near_pos = wicmath.NearPosition( our_pos, target_pos, FRONT_DISTANCE )

		
		self.myGroup.PushCommand( CMD_Wait( WAIT_TIME ), CMD_ATTACK )
		self.myGroup.PushCommand( CMD_LookAt( target_pos ), CMD_ATTACK )
		
		if aAllFlank:
			if aBehindFlank:
				self.myGroup.PushCommand( CMD_MoveGroup( behind_pos ), CMD_ATTACK )
			self.myGroup.PushCommand( CMD_MoveGroup( flank_pos, 24 ), CMD_ATTACK )
		else:
			if aBehindFlank:
				self.myGroup.PushCommand( CMD_MoveSubgroup( 0, half_group, behind_pos), CMD_ATTACK )
			self.myGroup.PushCommand( CMD_MoveSubgroup( 0, half_group, flank_pos, 24 ), CMD_ATTACK )

		self.myGroup.PushCommand( CMD_MoveGroup( near_pos, 64 ), CMD_ATTACK )
		self.myGroup.PushCommand( CMD_LookAt( target_pos ), CMD_ATTACK )
		self.myGroup.PushCommand( CMD_StopGroup(), CMD_ATTACK )

		
	def Blitz( self, aUnitId, aAttackerId ):
		
		if self.myGroup.IsEmpty():
			return
		
		WAIT_TIME = 2
		
		if common.IsInfantry( aAttackerId ):
			move_pos = unit.theUnits[aAttackerId].myPos
			self.myGroup.PushCommand( CMD_Wait( WAIT_TIME ), CMD_ATTACK )
			self.myGroup.PushCommand( CMD_MoveGroup( move_pos, 4 ), CMD_ATTACK )


	def Surround( self, aUnitId, aAttackerId, aRadius ):
		
		if self.myGroup.IsEmpty():
			return
		
		WAIT_TIME = 3.0
	
		target = unit.theUnits[aAttackerId].myPos
	
		self.myGroup.PushCommand( CMD_Wait( WAIT_TIME ), CMD_ATTACK )
		self.myGroup.PushCommand( CMD_SurroundTarget( target, aRadius, SURROUND_IN ), CMD_ATTACK )

		
	def StandFast(self, aUnitId, aAttackerId, aThreshold = 0.0):
		"""
		"""
		
		if self.myGroup.IsEmpty():
			return
		
		WAIT_TIME = 7.5
	
		target = unit.theUnits[aAttackerId].myPos
		
		doRegroup = True
		
		if aThreshold > 0.0:
			ourPos = unit.theUnits[aUnitId].myPos
			
			attackerDir = wicmath.GetVector( ourPos, target )
			headingDir = wicmath.Heading2Vector( unit.theUnits[aUnitId].myHeading )
			
			d = wicmath.Dot( attackerDir, headingDir )
			
			## make sure that acos doesn't get a bad value
			d = max( d, -1.0 )
			d = min( d, 1.0 )
			
			angle = math.acos( d )

			if angle < aThreshold:
				doRegroup = False

		self.myGroup.PushCommand( CMD_Wait(WAIT_TIME), CMD_ATTACK )
			
		if doRegroup or self.myGroup.GetLastExecutedCommandType() != CMD_ATTACK:
			self.myGroup.PushCommand( CMD_Regroup( target ), CMD_ATTACK )
		

class BHA_Fearless( AttackBehavior ):
	
	def __init__( self ):
		
		AttackBehavior.__init__( self )
		self.myUpdateTime = 60.0


class BHA_Defensive( AttackBehavior ):

	
	def __init__( self, aDistance = 38 ):
		
		AttackBehavior.__init__( self )
		self.myUpdateTime = 3.5
		self.__Distance = aDistance
		
	
	def Execute( self, aUnitId, aAttackerId ):

		AttackBehavior.Execute( self, aUnitId, aAttackerId )
		
		if common.IsArtillery( aAttackerId ):
			return
		
		self.myGroup.ClearCommands( CMD_ATTACK )
		self.Defend( aUnitId, aAttackerId, self.__Distance )


class BHA_Chicken( AttackBehavior ):

	
	def __init__( self, aFleeDistance = 128 ):
		
		AttackBehavior.__init__(self)
		self.myUpdateTime = 3.0
		self.__FleeDistance = aFleeDistance
		
	
	def Execute( self, aUnitId, aAttackerId ):

		AttackBehavior.Execute( self, aUnitId, aAttackerId )
		
		if common.IsArtillery( aAttackerId ):
			return

		self.myGroup.ClearCommands( CMD_ATTACK )
		self.Flee( aUnitId, aAttackerId, self.__FleeDistance )


class BHA_Flanker( AttackBehavior ):

	
	def __init__( self, aDistanceScale = 1.0, aAllFlank = False, aBehindFlank = True ):
		
		AttackBehavior.__init__( self )
		
		self.myUpdateTime = 26.0
		self.__DistanceScale = aDistanceScale
		self.__AllFlank = aAllFlank
		self.__BehindFlank = aBehindFlank
		
	
	def Execute( self, aUnitId, aAttackerId ):
		
		AttackBehavior.Execute( self, aUnitId, aAttackerId )
		
		if common.IsArtillery( aAttackerId ):
			return

		self.myGroup.ClearCommands( CMD_ATTACK )
		self.Flank( aUnitId, aAttackerId, self.__DistanceScale, self.__AllFlank, self.__BehindFlank )


class BHA_CautiousFlanker( AttackBehavior ):

	
	def __init__( self ):
		
		AttackBehavior.__init__( self )
		self.myUpdateTime = 28.0
		self.__Health = 0
		self.__UpdateHealth = True
		
	
	def Execute( self, aUnitId, aAttackerId ):
		
		AttackBehavior.Execute( self, aUnitId, aAttackerId )
		
		if common.IsArtillery( aAttackerId ):
			return

		if self.__UpdateHealth:
			self.__Health = self.myGroup.Size()
			self.__UpdateHealth = False

		self.myGroup.ClearCommands( CMD_ATTACK )
		
		if self.myGroup.Size() <= (self.__Health / 2):
			self.Flee( aUnitId, aAttackerId, 128 )
			self.__UpdateHealth = True
		else:
			self.Flank( aUnitId, aAttackerId, 1.0 )
		
		
class BHA_Blitzer( AttackBehavior ):
	
	def __init__( self ):
		"""
		"""
		
		AttackBehavior.__init__( self )
		self.myUpdateTime = 3.0
		self.__DefendDistance = 24
		
	
	def Execute( self, aUnitId, aAttackerId ):
		
		AttackBehavior.Execute( self, aUnitId, aAttackerId )
		
		if common.IsArtillery( aAttackerId ):
			return

		self.myGroup.ClearCommands( CMD_ATTACK )
		
		if common.IsInfantry( aAttackerId ):
			self.Blitz( aUnitId, aAttackerId )
		else:
			self.Defend( aUnitId, aAttackerId, self.__DefendDistance )
		
			
class BHA_Aggressive( AttackBehavior ):

	
	def __init__( self, aRadius = 36 ):
		
		AttackBehavior.__init__( self )
		self.myUpdateTime = 2.0
		self.__Radius = aRadius
		
	
	def Execute( self, aUnitId, aAttackerId ):
		
		AttackBehavior.Execute( self, aUnitId, aAttackerId )
		
		if common.IsArtillery( aAttackerId ):
			return

		self.myGroup.ClearCommands( CMD_ATTACK )
		self.Surround( aUnitId, aAttackerId, self.__Radius )
		

class BHA_StandFast( AttackBehavior ):

	
	def __init__( self, aAngleThreshold = 0.0 ):
		
		AttackBehavior.__init__( self )
		self.myUpdateTime = 2.5
		
		self.__AngleThreshold = aAngleThreshold
		
		
	def Execute( self, aUnitId, aAttackerId ):
		
		AttackBehavior.Execute( self, aUnitId, aAttackerId )
		
		if common.IsArtillery( aAttackerId ):
			return

		self.myGroup.ClearCommands( CMD_ATTACK )
		self.StandFast( aUnitId, aAttackerId, self.__AngleThreshold )



class BHA_StandFastEx( AttackBehavior ):

	
	def __init__( self, aOnlyTriggerOnPlayer = False, aAngleThreshold = 0.0 ):
		
		AttackBehavior.__init__( self )
		self.myUpdateTime = 2.5
		self.__TriggerOnPlayer = aOnlyTriggerOnPlayer
		
		self.__AngleThreshold = aAngleThreshold
		
		
	def Execute( self, aUnitId, aAttackerId ):
		
		AttackBehavior.Execute( self, aUnitId, aAttackerId )
		
		if self.__TriggerOnPlayer:
			if not unit.theUnits[ aAttackerId ].myOwner == serverimports.PLAYER_HUMAN:
				return
				
		if common.IsArtillery( aAttackerId ):
			return

		self.myGroup.ClearCommands( CMD_ATTACK )

		if self.myGroup.IsEmpty():
			return
		
		WAIT_TIME = 7.5
	
		regroupPos = unit.theUnits[aUnitId].myPos
		target = unit.theUnits[aAttackerId].myPos
		
		doRegroup = True
		aThreshold = self.__AngleThreshold
		
		if aThreshold > 0.0:
			ourPos = unit.theUnits[aUnitId].myPos
			
			attackerDir = wicmath.GetVector( ourPos, target )
			headingDir = wicmath.Heading2Vector( unit.theUnits[aUnitId].myHeading )
			
			d = wicmath.Dot( attackerDir, headingDir )
			
			## make sure that acos doesn't get a bad value
			d = max( d, -1.0 )
			d = min( d, 1.0 )
			
			angle = math.acos( d )

			if angle < aThreshold:
				doRegroup = False

		self.myGroup.StopGroup()
		self.myGroup.PushCommand( CMD_Wait(WAIT_TIME), CMD_ATTACK )
			
		if doRegroup or self.myGroup.GetLastExecutedCommandType() != CMD_ATTACK:
			self.myGroup.PushCommand( CMD_RegroupAt( regroupPos, target ), CMD_ATTACK )