import base
import wicg_common as common
import debug
import unit

## math imports
import math
from wicmath import *
import position

## group imports
from globals import *
import group


class Command( object ):


	def __init__( self ):

		self.Active = False
		self.Done = False
		self.Group = None

	
	def __str__( self ):
		
		if self.Group:
			groupName = self.Group.myName
		else:
			groupName = 'NoGroup'
		
		return '%s(%s)' % (self.__class__.__name__, groupName)
		
	
	def Start( self ):

		if __debug__:
			debug.DebugMessage( '%s::Start' % self )

		self.Active = True
		return GROUP_UPDATE_COST_LOW


	def Restart( self ):

		self.Active = False
		self.Done = False


	def Update( self ):
		return GROUP_UPDATE_COST_LOW

	def IsActive( self ):

		return self.Active


	def IsDone( self ):

		return self.Done


	def SetGroup( self, aGroup ):

		self.Group = aGroup


class CMD_MoveUnit( Command ):

	def __init__( self, aGroupUnit, aTarget, aDistance = CLOSE_TO_LIMIT, aHeading = None ):

		Command.__init__( self )
		self.__GroupUnit = aGroupUnit
		self.__Target = aTarget
		self.__Distance = aDistance
		self.__Heading = aHeading


	def Start( self ):
		
		Command.Start( self )
		
		self.Group.MoveUnit( self.__GroupUnit, self.__Target, self.__Heading )
		
		return GROUP_UPDATE_COST_HIGH


	def Update( self ):
		
		Command.Update( self )

		
		if (self.Group == None or self.Group.IsEmpty() or not self.Group.IsUnitInGroup( self.__GroupUnit.myUnitId ) ):
			self.Active = False
			self.Done = True
			return GROUP_UPDATE_COST_LOW
		
		try:
			ourPos = common.GetPosition( self.__GroupUnit )
		except unit.UnknownUnitException:
			self.Active = False
			self.Done = True
			return GROUP_UPDATE_COST_MEDIUM

		
		if wicmath.Distance( self.__GroupUnit.myTargetPos, ourPos ) < self.__Distance:
			self.Active = False
			self.Done = True
			return GROUP_UPDATE_COST_MEDIUM
		
		return GROUP_UPDATE_COST_MEDIUM


class CMD_MoveGroup( Command ):

	def __init__( self, aTarget, aDistance = CLOSE_TO_LIMIT, aDirection = None, aHeading = None, aOneAtTarget = False ):

		Command.__init__( self )
		self.__Target = aTarget
		self.__Distance = aDistance
		self.__Direction = aDirection
		self.__Heading = aHeading
		self.__OneAtTarget = aOneAtTarget


	def Start( self ):
		
		Command.Start( self )
		
		self.Group.MoveGroup( self.__Target, self.__Direction, self.__Heading )
		
		return GROUP_UPDATE_COST_HIGH


	def Update( self ):
		
		Command.Update( self )

		
		if (self.Group == None or self.Group.IsEmpty()):
			self.Active = False
			self.Done = True
			return GROUP_UPDATE_COST_LOW

		if self.__OneAtTarget and self.Group.IsAtTarget( self.__Distance ):
			self.Active = False
			self.Done = True
			return GROUP_UPDATE_COST_MEDIUM

		if self.Group.IsAllAtTarget( self.__Distance ):
			self.Active = False
			self.Done = True
			return GROUP_UPDATE_COST_MEDIUM
		
		return GROUP_UPDATE_COST_MEDIUM
			

class CMD_MoveGroupBackwards( Command ):

	def __init__( self, aTarget, aDistance = CLOSE_TO_LIMIT, aDirection = None, aHeading = None ):

		Command.__init__( self )
		self.__Target = aTarget
		self.__Distance = aDistance
		self.__Direction = aDirection
		self.__Heading = aHeading


	def Start( self ):
		
		Command.Start( self )
		
		self.Group.MoveGroup( self.__Target, self.__Direction, self.__Heading, False, True )
		
		return GROUP_UPDATE_COST_HIGH


	def Update( self ):
		
		Command.Update( self )

		if (self.Group == None or self.Group.IsEmpty()):
			self.Active = False
			self.Done = True
			return GROUP_UPDATE_COST_LOW

		if self.Group.IsAllAtTarget(self.__Distance):
			self.Active = False
			self.Done = True
			return GROUP_UPDATE_COST_MEDIUM
			
		return GROUP_UPDATE_COST_MEDIUM

			
class CMD_TeleportGroup( Command ):

	def __init__( self, aTarget, aDirection = None ):

		Command.__init__( self )
		self.__Target = aTarget
		self.__Direction = aDirection


	def Start( self ):
		
		Command.Start( self )
		
		self.Group.MoveGroup( self.__Target, self.__Direction, None, True )
		
		return GROUP_UPDATE_COST_HIGH


	def Update( self ):
		
		Command.Update( self )

		if ( self.Group == None or self.Group.IsEmpty() ):
			self.Active = False
			self.Done = True
			return GROUP_UPDATE_COST_LOW

		if self.Group.IsAllAtTarget( CLOSE_TO_LIMIT ):
			self.Active = False
			self.Done = True
			return GROUP_UPDATE_COST_MEDIUM
		
		return GROUP_UPDATE_COST_MEDIUM


class CMD_MoveForward( Command ):

	def __init__( self, aDistance ):

		Command.__init__( self )
		self.__Distance = aDistance
		self.__Target = None


	def Start( self ):

		Command.Start( self )
		
		if self.Group.IsEmpty():
			return GROUP_UPDATE_COST_LOW

		dir_vec = wicmath.Heading2Vector( self.Group.GetHeading() )
		pos_vec = wicmath.Position2Vector( self.Group.GetPosition() )
		target_vec = pos_vec + ( dir_vec * self.__Distance )

		self.__Target = wicmath.Vector2Position( target_vec )

		self.Group.MoveGroup( self.__Target )
		
		return GROUP_UPDATE_COST_HIGH


	def Update( self ):
		
		Command.Update( self )

		if ( self.Group == None or self.Group.IsEmpty() ):
			self.Active = False
			self.Done = True
			return GROUP_UPDATE_COST_LOW

		if self.Group.IsAllAtTarget():
			self.Active = False
			self.Done = True
			return GROUP_UPDATE_COST_MEDIUM

		return GROUP_UPDATE_COST_MEDIUM


class CMD_MoveSubgroup(Command):


	def __init__( self, aStartIndex, aStopIndex, aTarget, aDistance = CLOSE_TO_LIMIT ):

		Command.__init__( self )
		self.__StartIndex = aStartIndex
		self.__StopIndex = aStopIndex
		self.__Target = aTarget
		self.__Distance = aDistance
		self.__Subgroup = []

	def Start( self ):

		Command.Start( self )

		if self.__StartIndex >= 0 and self.__StopIndex < self.Group.Size():
			
			self.__Subgroup = self.Group.myUnits[self.__StartIndex:(self.__StopIndex + 1)]	
			self.Group.MoveSubgroup( self.__StartIndex, self.__StopIndex, self.__Target )
			return GROUP_UPDATE_COST_HIGH
		else:
			self.Active = False
			self.Done = True
			return GROUP_UPDATE_COST_MEDIUM

	def Update( self ):
		
		Command.Update( self )

		if ( self.Group == None or self.Group.IsEmpty() ):
			self.Active = False
			self.Done = True
			return GROUP_UPDATE_COST_LOW

		if self.IsAtTarget():
			self.Active = False
			self.Done = True
			return GROUP_UPDATE_COST_HIGH
		
		return GROUP_UPDATE_COST_MEDIUM


	def IsAtTarget( self ):
		
		for grpUnit in self.__Subgroup:
			if self.Group.IsUnitInGroup( grpUnit.myUnitId ):
				distance = wicmath.Distance( grpUnit.myUnit.myPos, grpUnit.myTargetPos )
				if ( distance > self.__Distance ):
					return False
		return True


class CMD_MoveMultipleTargets( Command ):


	def __init__( self, someTargets, aDistance = CLOSE_TO_LIMIT ):
		
		Command.__init__( self )
		
		if isinstance( someTargets, list ):
			self.__Targets = someTargets
		else:
			self.__Targets = [someTargets]
		
		self.__Distance = aDistance


	def Start( self ):
		
		Command.Start(self)

		self.Active = True
		self.Group.MoveMultipleTargets( self.__Targets )
		
		return GROUP_UPDATE_COST_HIGH


	def Update( self ):
		
		Command.Update( self )

		if ( self.Group == None or self.Group.IsEmpty() ):
			self.Active = False
			self.Done = True
			return GROUP_UPDATE_COST_LOW

		if self.Group.IsAllAtTarget( self.__Distance ):
			self.Active = False
			self.Done = True
			return GROUP_UPDATE_COST_MEDIUM
		
		return GROUP_UPDATE_COST_MEDIUM


class CMD_StopGroup( Command ):


	def __init__( self ):
		"""
		"""

		Command.__init__( self )


	def Start( self ):
		"""
		"""
		
		Command.Start( self )

		self.Group.StopGroup()
		
		self.Active = False
		self.Done = True
		
		return GROUP_UPDATE_COST_HIGH


class CMD_AttackUnit( Command ):


	def __init__( self, aUnitId  ):

		Command.__init__( self )
		self.__UnitId = aUnitId


	def Start( self ):
		
		Command.Start( self )

		self.Group.AttackUnit( self.__UnitId )

		self.Active = False
		self.Done = True
		
		return GROUP_UPDATE_COST_HIGH


class CMD_AttackTarget( Command ):


	def __init__( self, aTarget ):
		"""
		"""

		Command.__init__( self )
		self.__Target = aTarget


	def Start( self ):
		"""
		"""

		Command.Start( self )

		self.Group.AttackTarget( self.__Target )

		self.Active = False
		self.Done = True
		
		return GROUP_UPDATE_COST_HIGH


class CMD_AttackArea( Command ):

	def __init__( self, aCenter, aRadius ):

		Command.__init__( self )
		self.__Center = aCenter
		self.__Radius = aRadius


	def Start( self ):
		
		Command.Start( self )

		self.Active = False
		self.Done = True
		
		try:
			center_pos = common.GetPosition( self.__Center )
		except group.EmptyGroupException:
			debug.DebugMessage( 'CMD_AttackArea(%s)::Start Failed! Invalid Area Center, Empty Group' % ( self.Group ), debug.BRIEF )
			return GROUP_UPDATE_COST_MEDIUM
		except unit.UnknownUnitException:
			debug.DebugMessage( 'CMD_AttackArea(%s)::Start Failed! Invalid Area Center, Unknown Unit' % ( self.Group ), debug.BRIEF )
			return GROUP_UPDATE_COST_MEDIUM

		new_pos = wicmath.CalculateRandomPosition( center_pos, self.__Radius )
		self.Group.AttackTarget( new_pos )
		
		return GROUP_UPDATE_COST_HIGH


class CMD_UnloadAll( Command ):
	"""
	"""


	def __init__( self ):
		"""
		"""

		Command.__init__( self )


	def Start( self ):
		"""
		"""
		
		Command.Start( self )

		self.Active = False
		self.Done = True

		self.Group.UnloadAll()
		
		return GROUP_UPDATE_COST_HIGH


class CMD_UnloadFrom( Command ):
	"""
	"""


	def __init__( self, aIndex ):
		"""
		"""

		Command.__init__( self )
		self.__Index = aIndex


	def Start( self ):
		"""
		"""
		Command.Start( self )

		self.Active = False
		self.Done = True

		self.Group.UnloadFrom( self.__Index )
		
		return GROUP_UPDATE_COST_HIGH


class CMD_EnterContainer( Command ):
	"""
	"""


	def __init__( self, aContainerId, aFlag = False ):
		"""
		"""

		Command.__init__( self )
		self.__ContainerId = aContainerId
		self.__Flag = aFlag


	def Start( self ):
		"""
		"""
		Command.Start( self )

		self.Active = False
		self.Done = True

		self.Group.EnterContainer( self.__ContainerId, self.__Flag )
		
		return GROUP_UPDATE_COST_HIGH


class CMD_EnterGroup( Command ):
	"""
	"""


	def __init__( self, aGroupToEnter = None, aInstantFlag = False ):
		"""
		"""

		Command.__init__( self )
		self.__GroupToEnter = aGroupToEnter
		self.__InstantFlag = aInstantFlag


	def Start( self ):
		"""
		"""
		Command.Start( self )

		self.Active = False
		self.Done = True

		self.Group.EnterGroup( self.__GroupToEnter, self.__InstantFlag )
		
		return GROUP_UPDATE_COST_HIGH


class CMD_UnitsEnterContainer( Command ):
	"""
	"""


	def __init__( self, aStartIndex, aStopIndex, aContainerId, aFlag = False ):
		"""
		"""

		Command.__init__( self )
		self.__ContainerId = aContainerId
		self.__Flag = aFlag
		self.__StartIndex = aStartIndex
		self.__StopIndex = aStopIndex


	def Start( self ):
		"""
		"""
		Command.Start( self )

		self.Active = False
		self.Done = True

		self.Group.UnitsEnterContainer( self.__StartIndex, self.__StopIndex, self.__ContainerId, self.__Flag )
		
		return GROUP_UPDATE_COST_HIGH


class CMD_UnitEnterContainer( Command ):
	"""
	"""


	def __init__( self, aGroupUnit, aContainerId, aFlag = False ):
		"""
		"""

		Command.__init__( self )
		self.__ContainerId = aContainerId
		self.__Flag = aFlag
		self.__GroupUnit = aGroupUnit


	def Start( self ):
		"""
		"""
		Command.Start( self )

		self.Active = False
		self.Done = True

		self.Group.UnitEnterContainer( self.__GroupUnit, self.__ContainerId, self.__Flag )
		
		return GROUP_UPDATE_COST_HIGH


class CMD_EnterBuilding( Command ):
	"""
	"""


	def __init__( self, aBuilding, aInstantEnter = False ):
		"""
		"""

		Command.__init__( self )
		self.__Building = aBuilding
		self.__InstantEnter = aInstantEnter


	def Start( self ):
		"""
		"""
		Command.Start( self )

		self.Active = False
		self.Done = True

		self.Group.EnterBuilding( self.__Building, self.__InstantEnter )
		
		return GROUP_UPDATE_COST_HIGH


class CMD_FollowPath( Command ):


	def __init__( self, aWayPoints, aDelay = 0.0, aLoop = False, aLimit = CLOSE_TO_LIMIT ):
		"""
		"""

		Command.__init__( self )
		self.__WayPoints = aWayPoints[:]
		self.__CurrentPos = 0
		self.__Delay = aDelay
		self.__Loop = aLoop
		self.__Limit = aLimit
		self.__DoMove = False
		self.__LastUpdatTime = 0.0


	def Start( self ):
		"""
		"""
		Command.Start( self )

		self.Group.MoveGroup( self.__WayPoints[self.__CurrentPos] )

		self.__LastUpdatTime = base.GetCurrentTime()
		
		return GROUP_UPDATE_COST_HIGH


	def Update( self ):
		"""
		"""
		Command.Update( self )

		if (self.Group == None or self.Group.IsEmpty() or not len( self.__WayPoints )):
			self.Active = False
			self.Done = True
			return GROUP_UPDATE_COST_MEDIUM

		if self.Group.IsLeaderAtTarget( self.__Limit ):
			if ( base.GetCurrentTime() - self.__LastUpdatTime ) > self.__Delay:
				self.__CurrentPos += 1
				self.__DoMove = True

				if self.__CurrentPos >= len( self.__WayPoints ):
					if self.__Loop:
						self.__CurrentPos = 0
					else:
						self.Active = False
						self.Done = True
						return GROUP_UPDATE_COST_HIGH
			
		if self.__DoMove:
			self.__LastUpdatTime = base.GetCurrentTime()
			self.__DoMove = False
			self.Group.MoveGroup( self.__WayPoints[self.__CurrentPos] )
		
		return GROUP_UPDATE_COST_HIGH


class CMD_Follow( Command ):


	def __init__( self, aTarget, aDistance = 0.0, aForever = True, aUpdateFreq = 16.0 ):
		"""
		"""

		Command.__init__( self )

		self.__Target = aTarget
		self.__Distance = aDistance
		self.__Forever = aForever
		
		self.__LastUpdateTime = 0.0
		if aUpdateFreq < 1.0:
			aUpdateFreq = 1.0
		self.__UpdateFrequency = aUpdateFreq


	def Start( self ):
		"""
		"""
		Command.Start( self )

		if ( self.Group.IsEmpty() ):
			self.Active = False
			self.Done = True
		
		return GROUP_UPDATE_COST_MEDIUM


	def Update( self ):
		"""
		"""
		Command.Update( self )

		if ( self.Group.IsEmpty() ):
			self.Active = False
			self.Done = True
			return GROUP_UPDATE_COST_MEDIUM

		currentTime = base.GetCurrentTime()
		if currentTime > (self.__LastUpdateTime + self.__UpdateFrequency):
			try:
				target = common.GetPosition( self.__Target )
			except group.EmptyGroupException:
				debug.DebugMessage( 'CMD_Follow(%s)::Update Failed! Target Invalid - EmptyGroup(%s)' % ( self.Group, self.__Target ), debug.NONE )
				self.Active = False
				self.Done = True
				return GROUP_UPDATE_COST_HIGH
			except unit.UnknownUnitException:
				debug.DebugMessage( 'CMD_Follow(%s)::Update Failed! Target Invalid - Bad Unit' % ( self.Group ), debug.NONE )
				self.Active = False
				self.Done = True
				return GROUP_UPDATE_COST_HIGH
				
	
			if not self.__Forever and self.Group.IsCloseTo(target, self.__Distance + 2):
				self.Active = False
				self.Done = True
				return GROUP_UPDATE_COST_HIGH
	
			Unit2Group = wicmath.GetVector(target, self.Group.GetPosition())
			UnitPosVector = wicmath.Position2Vector(target)
	
			FollowPos = wicmath.Vector2Position(UnitPosVector + Unit2Group * self.__Distance)
			
			self.Group.MoveGroup( FollowPos )
				
			self.__LastUpdateTime = currentTime
		
		return GROUP_UPDATE_COST_HIGH


class CMD_SurroundTarget( Command ):


	def __init__( self, aTarget, aDistance, aHeading = SURROUND_NORMAL ):
		"""
		"""

		Command.__init__(self )

		self.__Target = aTarget
		self.__Distance = float( aDistance )
		self.__Heading = aHeading


	def Start( self ):
		"""
		"""
		Command.Start( self )
					
		self.DoMove()
		
		return GROUP_UPDATE_COST_HIGH


	def Update( self ):
		"""
		"""
		Command.Update( self )

		if self.Group == None or self.Group.IsEmpty():
			self.Active = False
			self.Done = True
			return GROUP_UPDATE_COST_LOW

		if self.Group.IsAllAtTarget():
			self.Active = False
			self.Done = True
		
		return GROUP_UPDATE_COST_HIGH


	def DoMove( self ):
		"""
		"""

		if self.Group.IsEmpty():
			self.Active = False
			self.Done = True
			return

		radiansPerUnit = float(math.pi * 2.0) / float(self.Group.Size())
		currentAngle = 0.0

		try:
			targetPos = common.GetPosition( self.__Target )
		except group.EmptyGroupException:
			debug.DebugMessage( 'CMD_SurroundTarget(%s)::DoMove Failed! Invalid Target - EmptyGroup(%s)' % ( self.Group, self.__Target ), debug.NONE )
			self.Active = False
			self.Done = True
			return
		except unit.UnknownUnitException:
			debug.DebugMessage( 'CMD_SurroundTarget(%s)::DoMove Failed! Invalid Target - Bad Unit' % ( self.Group ), debug.NONE )
			self.Active = False
			self.Done = True
			return
			
		movePos = position.Position()

		for groupUnit in self.Group.myUnits:
				movePos.myX = targetPos.myX
				movePos.myZ = 0.0
				movePos.myZ = targetPos.myZ

				movePos.myX += ( self.__Distance * math.cos( currentAngle ) )
				movePos.myZ += ( self.__Distance * math.sin( currentAngle ) )
				currentAngle += radiansPerUnit

				if self.__Heading == SURROUND_NORMAL:
					self.Group.MoveUnit( groupUnit, movePos )
				elif self.__Heading == SURROUND_OUT:
					self.Group.MoveUnit( groupUnit, movePos, wicmath.GetHeading( wicmath.Position2Vector( targetPos ), wicmath.Position2Vector( movePos ) ) )
				elif self.__Heading == SURROUND_IN:
					self.Group.MoveUnit( groupUnit, movePos, wicmath.GetHeading( wicmath.Position2Vector( movePos ), wicmath.Position2Vector( targetPos ) ) )


class CMD_TakeCover( Command ):


	def __init__( self ):
		"""
		"""

		Command.__init__( self )


	def Start( self ):
		"""
		"""
		Command.Start( self )

		self.Group.TakeCover()
		
		return GROUP_UPDATE_COST_HIGH


	def Update( self ):
		"""
		"""
		Command.Update( self )

		if self.Group == None or self.Group.IsEmpty():
			self.Active = False
			self.Done = True
			return GROUP_UPDATE_COST_LOW

		if self.Group.IsAllAtTarget():
			self.Active = False
			self.Done = True
		
		return GROUP_UPDATE_COST_HIGH


class CMD_Regroup( Command ):


	def __init__( self, aTarget = None ):
		"""
		"""

		Command.__init__( self )
		self.__Target = aTarget


	def Start( self ):
		"""
		"""
		Command.Start( self )

		self.Group.Regroup( self.__Target )
		
		return GROUP_UPDATE_COST_HIGH


	def Update( self ):
		"""
		"""
		Command.Update( self )

		if self.Group == None or self.Group.IsEmpty():
			self.Active = False
			self.Done = True
			return GROUP_UPDATE_COST_LOW

		if self.Group.IsAllAtTarget():
			self.Active = False
			self.Done = True
		
		return GROUP_UPDATE_COST_HIGH


class CMD_RegroupAt( Command ):


	def __init__( self, aPosition, aTarget = None ):
		"""
		"""

		Command.__init__( self )
		self.__Position = aPosition
		self.__Target = aTarget


	def Start( self ):
		"""
		"""
		Command.Start( self )

		self.Group.RegroupAt( self.__Position, self.__Target )
		
		return GROUP_UPDATE_COST_HIGH


	def Update( self ):
		"""
		"""
		Command.Update( self )

		if self.Group is None or self.Group.IsEmpty():
			self.Active = False
			self.Done = True
			return GROUP_UPDATE_COST_LOW

		if self.Group.IsAllAtTarget():
			self.Active = False
			self.Done = True
		
		return GROUP_UPDATE_COST_HIGH

## davidh 090113.
class CMD_RegroupAtOnNeed( Command ):


	def __init__( self, aPosition, aTarget, aLimit = CLOSE_TO_LIMIT ):
		"""
		"""

		Command.__init__( self )
		self.__Position = aPosition
		self.__Target = aTarget
		self.__Limit = aLimit


	def Start( self ):
		"""
		"""
		Command.Start( self )

		for aUnit in self.Group.myUnits:
			dist = wicmath.Distance( common.GetPosition( self.__Position ), aUnit.myPos )
			
			if dist > self.__Limit:
				self.Group.RegroupAt( self.__Position, self.__Target )   
				return GROUP_UPDATE_COST_HIGH 

		return GROUP_UPDATE_COST_HIGH


	def Update( self ):
		"""
		"""
		Command.Update( self )

		if self.Group is None or self.Group.IsEmpty():
			self.Active = False
			self.Done = True
			return GROUP_UPDATE_COST_LOW

		if self.Group.IsAllAtTarget():
			self.Active = False
			self.Done = True
		
		return GROUP_UPDATE_COST_HIGH



class CMD_LookAt( Command ):


	def __init__( self, aTarget ):
		"""
		"""

		Command.__init__( self )

		self.__Target = aTarget


	def Start( self ):
		"""
		"""
		Command.Start( self )

		self.Group.LookAt( self.__Target )

		self.Active = False
		self.Done = True
		
		return GROUP_UPDATE_COST_HIGH



class CMD_FaceDirection( Command ):


	def __init__( self, aDirection ):
		"""
		"""

		Command.__init__( self )

		self.__Direction = aDirection


	def Start( self ):
		"""
		"""
		Command.Start( self )

		self.Group.FaceDirection( self.__Direction )

		self.Active = False
		self.Done = True
		
		return GROUP_UPDATE_COST_HIGH


class CMD_SetSpeed( Command ):


	def __init__( self, aNewSpeed ):
		"""
		"""

		Command.__init__( self )

		self.__Speed = aNewSpeed


	def Start( self ):
		"""
		"""
		Command.Start( self )

		self.Active = False
		self.Done = True

		if self.Group is None:
			return

		self.Group.SetSpeed( self.__Speed )
		
		return GROUP_UPDATE_COST_LOW


class CMD_RestoreSpeed( Command ):


	def __init__( self ):
		"""
		"""

		Command.__init__( self )


	def Start( self ):
		"""
		"""
		Command.Start( self )

		self.Active = False
		self.Done = True

		if self.Group is None:
			return GROUP_UPDATE_COST_LOW

		self.Group.RestoreSpeed()
		
		return GROUP_UPDATE_COST_LOW


class CMD_SetUnifiedSpeed( Command ):


	def __init__( self, aFlag ):
		"""
		"""

		Command.__init__( self )

		self.__Flag = aFlag


	def Start( self ):
		"""
		"""
		Command.Start( self )

		self.Active = False
		self.Done = True

		if self.Group is None:
			return GROUP_UPDATE_COST_LOW

		self.Group.SetUnifiedSpeed( self.__Flag )
		
		return GROUP_UPDATE_COST_LOW


class CMD_SetFormation( Command ):


	def __init__( self, aFormation, aDistance = DEFAULT_FORMATION_DISTANCE ):
		"""
		"""

		Command.__init__( self )

		self.__Formation = aFormation
		self.__Distance = aDistance


	def Start( self ):
		"""
		"""
		Command.Start( self )

		self.Active = False
		self.Done = True

		if self.Group is None:
			return GROUP_UPDATE_COST_LOW

		self.Group.SetFormation( self.__Formation, self.__Distance )
		
		return GROUP_UPDATE_COST_LOW


class CMD_SetFormationEx( Command ):


	def __init__( self, aFormation, aDistance = DEFAULT_FORMATION_DISTANCE, anOffset = 3, anWidthOffset = 2 ):
		"""
		"""

		Command.__init__( self )

		self.__Formation = aFormation
		self.__Distance = aDistance
		self.__FormationOffset = anOffset
		self.__FormationWidthOffset = anWidthOffset


	def Start( self ):
		"""
		"""
		Command.Start( self )

		self.Active = False
		self.Done = True

		if self.Group is None:
			return GROUP_UPDATE_COST_LOW

		self.Group.SetFormationEx( self.__Formation, self.__Distance, self.__FormationOffset, self.__FormationWidthOffset )
		
		return GROUP_UPDATE_COST_LOW

class CMD_SetFormationOffset( Command ):

	def __init__( self, anOffset ):
		"""
		"""

		Command.__init__( self )

		self.__FormationOffset = anOffset


	def Start( self ):
		"""
		"""
		Command.Start( self )

		self.Active = False
		self.Done = True

		if self.Group is None:
			return GROUP_UPDATE_COST_LOW

		self.Group.SetFormationOffset( self.__FormationOffset )
		
		return GROUP_UPDATE_COST_LOW

class CMD_SetFormationWidthOffset( Command ):

	def __init__( self, anOffset ):
		"""
		"""

		Command.__init__( self )

		self.__FormationWidthOffset = anOffset


	def Start( self ):
		"""
		"""
		Command.Start( self )

		self.Active = False
		self.Done = True

		if self.Group is None:
			return GROUP_UPDATE_COST_LOW

		self.Group.SetFormationWidthOffset( self.__FormationWidthOffset )
		
		return GROUP_UPDATE_COST_LOW


class CMD_HoldFire( Command ):


	def __init__( self, aFlag ):
		"""
		"""

		Command.__init__( self )

		self.__Flag = aFlag


	def Start( self ):
		"""
		"""
		Command.Start( self )

		self.Active = False
		self.Done = True

		if self.Group is None:
			return GROUP_UPDATE_COST_LOW

		self.Group.HoldFire( self.__Flag )
		
		return GROUP_UPDATE_COST_LOW


class CMD_SetTransporterGroup( Command ):


	def __init__( self, aFlag ):
		"""
		"""

		Command.__init__( self )

		self.__Flag = aFlag


	def Start( self ):
		"""
		"""
		Command.Start( self )

		self.Active = False
		self.Done = True

		if self.Group is None:
			return GROUP_UPDATE_COST_LOW

		self.Group.SetTransporterGroup( self.__Flag )
		
		return GROUP_UPDATE_COST_LOW


class CMD_SetOwner( Command ):


	def __init__( self, aNewOwner ):
		"""
		"""

		Command.__init__( self )

		self.__NewOwner = aNewOwner


	def Start( self ):
		"""
		"""
		Command.Start( self )

		self.Active = False
		self.Done = True

		if self.Group is None or self.Group.IsEmpty():
			return GROUP_UPDATE_COST_LOW

		self.Group.SetOwner( self.__NewOwner )
		
		return GROUP_UPDATE_COST_MEDIUM


class CMD_SetGroupApOwner( Command ):


	def __init__( self, aNewApOwner ):
		"""
		"""

		Command.__init__( self )

		self.__NewApOwner = aNewApOwner


	def Start( self ):
		"""
		"""
		Command.Start( self )

		self.Active = False
		self.Done = True

		if self.Group is None or self.Group.IsEmpty():
			return GROUP_UPDATE_COST_LOW

		self.Group.SetGroupApOwner( self.__NewApOwner )
		
		return GROUP_UPDATE_COST_MEDIUM


class CMD_SetTeam( Command ):


	def __init__( self, aNewTeam ):

		Command.__init__(self)

		self.__NewTeam = aNewTeam


	def Start( self ):

		Command.Start( self )

		self.Active = False
		self.Done = True

		if self.Group is None or self.Group.IsEmpty():
			return GROUP_UPDATE_COST_LOW

		self.Group.SetTeam( self.__NewTeam )
		
		return GROUP_UPDATE_COST_MEDIUM


class CMD_SetHealth( Command ):


	def __init__( self, aNewHealth ):
		"""
		"""

		Command.__init__( self )

		self.__NewHealth = aNewHealth


	def Start( self ):
		"""
		"""
		Command.Start( self )

		self.Active = False
		self.Done = True

		if self.Group == None or self.Group.IsEmpty():
			return GROUP_UPDATE_COST_LOW

		self.Group.SetHealth( self.__NewHealth )
		
		return GROUP_UPDATE_COST_MEDIUM


class CMD_SetHealthByScale( Command ):


	def __init__( self, aHealthScale ):
		"""
		"""

		Command.__init__( self )

		self.__HealthScale = aHealthScale


	def Start( self):
		"""
		"""
		Command.Start( self )

		self.Active = False
		self.Done = True

		if self.Group == None or self.Group.IsEmpty():
			return GROUP_UPDATE_COST_LOW

		self.Group.SetHealthByScale( self.__HealthScale )
		
		return GROUP_UPDATE_COST_HIGH


class CMD_SetRandomHealth( Command ):


	def __init__( self, aMinHealth, aMaxHealth ):
		"""
		"""

		Command.__init__( self )

		self.__MinHealth = aMinHealth
		self.__MaxHealth = aMaxHealth


	def Start( self ):
		"""
		"""
		Command.Start( self )

		self.Active = False
		self.Done = True

		if self.Group is None or self.Group.IsEmpty():
			return GROUP_UPDATE_COST_LOW

		self.Group.SetRandomHealth( self.__MinHealth, self.__MaxHealth )
		
		return GROUP_UPDATE_COST_HIGH


class CMD_CreateGroup( Command ):


	def __init__( self, aUnits, aPos, aOwner, aTeam ):
		"""
		"""

		Command.__init__( self )

		self.__Units = aUnits
		self.__Pos = aPos
		self.__Owner = aOwner
		self.__Team = aTeam


	def Start( self ):
		"""
		"""
		Command.Start( self )

		self.Active = False
		self.Done = True

		if self.Group is None:
			return GROUP_UPDATE_COST_LOW

		self.Group.CreateGroup( self.__Units, self.__Pos, self.__Owner, self.__Team )
		
		return GROUP_UPDATE_COST_HIGH


class CMD_CreateUnits( Command ):


	def __init__( self, aUnits ):
		"""
		"""

		Command.__init__( self )

		self.__Units = aUnits


	def Start( self ):
		"""
		"""
		Command.Start( self )

		self.Active = False
		self.Done = True

		if self.Group is None:
			return GROUP_UPDATE_COST_LOW

		self.Group.CreateUnits( self.__Units )
		
		return GROUP_UPDATE_COST_HIGH


class CMD_CreateUnitsAtPosition( Command ):


	def __init__( self, aUnits, aTarget, aOwner, aTeam ):
		"""
		"""
		Command.__init__( self )

		self.__Units = aUnits
		self.__Target = aTarget
		self.__Owner = aOwner
		self.__Team = aTeam


	def Start( self ):
		"""
		"""
		Command.Start( self )

		self.Active = False
		self.Done = True

		if self.Group is None:
			return GROUP_UPDATE_COST_LOW

		self.Group.CreateUnitsAtPosition( self.__Units, self.__Target, self.__Owner, self.__Team )
		
		return GROUP_UPDATE_COST_HIGH


class CMD_AddUnits( Command ):


	def __init__( self, someUnits ):
		"""
		"""
		Command.__init__( self )

		self.__Units = someUnits


	def Start( self ):
		"""
		"""
		Command.Start( self )

		self.Active = False
		self.Done = True

		if self.Group is None:
			return GROUP_UPDATE_COST_LOW

		self.Group.AddUnits( self.__Units )
		
		return GROUP_UPDATE_COST_HIGH


class CMD_AddUnitsFromGroup( Command ):


	def __init__( self, aGroup ):
		"""
		"""
		Command.__init__( self )

		self.__Group = aGroup


	def Start( self ):
		"""
		"""
		Command.Start( self )

		self.Active = False
		self.Done = True

		if self.Group is None:
			return GROUP_UPDATE_COST_LOW

		self.Group.AddUnits( self.__Group.myUnits )
		
		return GROUP_UPDATE_COST_HIGH


class CMD_DestroyGroup( Command ):


	def __init__( self, aShouldExplode = 0 ):
		"""
		"""

		Command.__init__( self )

		self.__ShouldExplode = aShouldExplode


	def Start( self ):
		"""
		"""
		Command.Start( self )

		self.Active = False
		self.Done = True

		if self.Group == None or self.Group.IsEmpty():
			return GROUP_UPDATE_COST_LOW

		self.Group.DestroyGroup( self.__ShouldExplode )
		
		return GROUP_UPDATE_COST_HIGH


class CMD_DestroyUnits( Command ):


	def __init__( self, aStartIndex, aStopIndex, aShouldExplode = 0 ):
		"""
		"""

		Command.__init__( self )

		self.__ShouldExplode = aShouldExplode
		self.__StartIndex = aStartIndex
		self.__StopIndex = aStopIndex


	def Start( self ):
		"""
		"""
		Command.Start( self )

		self.Active = False
		self.Done = True

		if self.Group == None or self.Group.IsEmpty():
			return GROUP_UPDATE_COST_LOW

		self.Group.DestroyUnits( self.__StartIndex, self.__StopIndex, self.__ShouldExplode )
		
		return GROUP_UPDATE_COST_HIGH


class CMD_SetState( Command ):


	def __init__( self, aState ):
		"""
		"""

		Command.__init__( self )
		self.__State = aState


	def Start( self ):
		"""
		"""
		Command.Start( self )

		self.Active = False
		self.Done = True

		self.Group.SetState( self.__State )
		
		return GROUP_UPDATE_COST_LOW


class CMD_ActivateRefillMode( Command ):


	def __init__( self, aRefillLimit, aRefillAmount, aUnits, aSpawnTarget, aMoveRadius, aMoveTarget = None, aDelay = 0.0 ):
		"""
		"""

		Command.__init__( self )
		self.__RefillLimit = aRefillLimit
		self.__RefillAmount = aRefillAmount
		self.__RefillUnits = aUnits
		self.__RefillSpawnTarget = aSpawnTarget
		self.__RefillMoveRadius = aMoveRadius
		self.__MoveTarget = aMoveTarget
		self.__Delay = aDelay


	def Start( self ):
		"""
		"""
		Command.Start( self )

		self.Active = False
		self.Done = True

		self.Group.ActivateRefillMode( self.__RefillLimit, self.__RefillAmount, self.__RefillUnits, self.__RefillSpawnTarget, self.__RefillMoveRadius, self.__MoveTarget, self.__Delay )
		
		return GROUP_UPDATE_COST_MEDIUM


class CMD_UpdateRefillMode( Command ):


	def __init__( self, aRefillLimit, aRefillAmount, aUnits, aSpawnTarget, aMoveRadius, aMoveTarget = None, aDelay = 0.0, aRemovePendingRefill = False ):
		
		
		Command.__init__( self )
		self.__RefillLimit = aRefillLimit
		self.__RefillAmount = aRefillAmount
		self.__RefillUnits = aUnits
		self.__RefillSpawnTarget = aSpawnTarget
		self.__RefillMoveRadius = aMoveRadius
		self.__MoveTarget = aMoveTarget
		self.__Delay = aDelay
		self.__RemovePendingRefill = aRemovePendingRefill


	def Start( self ):
		"""
		"""
		Command.Start( self )

		self.Active = False
		self.Done = True

		self.Group.UpdateRefillMode( self.__RefillLimit, self.__RefillAmount, self.__RefillUnits, self.__RefillSpawnTarget, self.__RefillMoveRadius, self.__MoveTarget, self.__Delay, self.__RemovePendingRefill )
		
		return GROUP_UPDATE_COST_MEDIUM


class CMD_DeactivateRefillMode( Command ):


	def __init__( self, aRemovePendingRefill = False ):
		"""
		"""

		Command.__init__( self )
		self.__RemovePendingRefill = aRemovePendingRefill


	def Start( self ):
		"""
		"""
		Command.Start( self )

		self.Active = False
		self.Done = True

		self.Group.DeactivateRefillMode( self.__RemovePendingRefill )
		
		return GROUP_UPDATE_COST_MEDIUM


class CMD_Refill( Command ):


	def __init__( self ):

		Command.__init__( self )


	def Start( self ):

		Command.Start( self )

		self.Active = False
		self.Done = True

		self.Group.Refill()
		
		return GROUP_UPDATE_COST_HIGH


class CMD_Wait( Command ):


	def __init__( self, aDelay ):

		Command.__init__( self )

		self.__Delay = aDelay


	def __str__( self ):
		
		return 'CMD_Wait(%s, %d)' % ( self.Group, self.__Delay )
		

	def Start( self ):
		import serverimports
		
		Command.Start( self )

		serverimports.Delay( self.__Delay, serverimports.Action( self.Finish ) )
		
		return GROUP_UPDATE_COST_MEDIUM


	def Finish( self ):
		"""
		"""

		self.Done = True


class CMD_WaitUntil( Command ):


	def __init__( self, aFunction, *aArguments ):
		"""
		"""
		import reaction.action

		Command.__init__( self )
		self.__Action = reaction.action.Action( aFunction, *aArguments )


	def Update( self ):
		"""
		"""
		Command.Update( self )

		if self.__Action.Execute():
			self.Active = False
			self.Done = True
		
		return GROUP_UPDATE_COST_MEDIUM


class CMD_WaitUntilNextDrop( Command ):


	def __init__( self ):

		Command.__init__( self )


	def Start( self ):
		
		import serverimports as si		
		
		Command.Start( self )
		
		si.RE_OnGroupUnitsDropped( self.Group, si.Action( self.Finish ) )
		
		return GROUP_UPDATE_COST_LOW
	
	
	def Finish( self ):
		"""
		"""

		self.Active = False
		self.Done = True


class CMD_SetAttackBehavior( Command ):


	def __init__( self, aBehavior ):

		Command.__init__( self )
		self.__Behavior = aBehavior


	def Start( self ):

		Command.Start( self )

		self.Active = False
		self.Done = True

		if not self.Group:
			return

		self.Group.SetAttackBehavior( self.__Behavior )
		
		return GROUP_UPDATE_COST_MEDIUM



class CMD_SetBaseBehavior( Command ):


	def __init__( self, aBehavior ):
		"""
		"""

		Command.__init__( self )

		self.__Behavior = aBehavior


	def Start( self ):

		Command.Start( self )

		self.Active = False
		self.Done = True

		if not self.Group:
			return GROUP_UPDATE_COST_LOW

		self.Group.SetBaseBehavior( self.__Behavior )
		
		return GROUP_UPDATE_COST_MEDIUM


class CMD_AddCombatExceptionGroup( Command ):


	def __init__( self, someGroups ):

		Command.__init__( self )
		self.__Groups = someGroups


	def Start( self ):

		Command.Start( self )

		self.Active = False
		self.Done = True

		if not self.Group:
			return GROUP_UPDATE_COST_LOW

		self.Group.AddCombatExceptionGroup( self.__Groups )
		
		return GROUP_UPDATE_COST_MEDIUM


class CMD_RemoveCombatExceptionGroup( Command ):


	def __init__( self, someGroups ):
		"""
		"""

		Command.__init__( self )
		self.__Groups = someGroups


	def Start( self ):
		"""
		"""
		Command.Start( self )

		self.Active = False
		self.Done = True

		if not self.Group:
			return GROUP_UPDATE_COST_LOW

		self.Group.RemoveCombatExceptionGroup( self.__Groups )
		
		return GROUP_UPDATE_COST_MEDIUM


class CMD_CustomCommand( Command ):


	def __init__( self, aFunction, *aArguments ):
		
				
		import reaction.action

		Command.__init__( self )
		
		if isinstance( aFunction, list ):
			self.__Actions = aFunction
		elif isinstance( aFunction, reaction.action.Action ):
			self.__Actions = []
			self.__Actions.append( aFunction )
		else:
			self.__Actions = []
			self.__Actions.append( reaction.action.Action( aFunction, *aArguments ) )
	
	
	def Start( self ):
		
		Command.Start( self )

		self.Active = False
		self.Done = True
		
		for act in self.__Actions:
			act.Execute()
		
		return GROUP_UPDATE_COST_HIGH


