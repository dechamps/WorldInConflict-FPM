import base
import wicg_common as common
import debug
import instance
import position
import wicg
import unit


class Area( object ):
	""" An area is basically a position and a radius. It has methods for
	checking for unit residence.
	"""
	def __init__( self, *someArgs ):
		""" Constructor
		"""
		global theAreas
		
		if isinstance( someArgs[0], str ):							## If a string is given we try to fetch the instance
			inst = instance.theInstances[someArgs[0]]
			self.__position = inst.myPos
			
			## check if a radius was given
			if len( someArgs ) == 2:
				self.__radius = someArgs[1]
			else:
				self.__radius = inst.myRadius
			
		elif isinstance( someArgs[0], instance.Instance ):						## If an instance object is given...
			self.__position = someArgs[0].myPos								## ...we copy it's position...
			
			## check if a radius was given
			if len( someArgs ) == 2:
				self.__radius = someArgs[1]
			else:
				self.__radius = someArgs[0].myRadius							## ...and it's radius
			
		else:
			self.__position = someArgs[0]									## It's also possible to give a position...
			self.__radius = someArgs[1]									## ...and a radius
			
			if not isinstance( self.__position, position.Position ):			## If the position is not a Position object...
				self.__position	= position.Position( *self.__position )			## ...we assume it's a tuple
		
		self.__lastUpdateTime	= -1
		self.__name				= Areas.GetUniqueName()
		self.__units			= None
		self.__updateDelay		= -1
		self.__updater			= None
		
		self.Update()
		
		theAreas.AddArea( self )


	def __pos__( self ):
		
		return self.__position


	def __radius__( self ):
		
		return self.__radius
		
	
	def __area__( self ):
		
		return self
	
	
	def __copy__( self ):
		
		return Area( self.__position, self.__radius )
		
	
	def HaveUnit( self, aUnit ):
		""" Returns a unit id or a list of unit id's if they are found in the
		area. Or None if no unit is found.
		"""
		self.Update()
		
		if isinstance( aUnit, list ):
			returnUnits = []
			
			for unit in aUnit:
				if unit in self.__units:
					returnUnits.append( unit )
			
			if len( returnUnits ):
				return returnUnits
			else:
				return None
			
		elif isinstance( aUnit, int ):
			if aUnit in self.__units:
				return aUnit
			else:
				return None
			
		else:
			if len( self.__units ):
				return self.__units
			else:
				return None
	
	
	def HaveUnits( self, someUnits ):
		""" Returns a unit id or a list of unit id's if they are found in the
		area. Or None if no unit is found.
		"""
		self.Update()
		
		if common.ListInList( someUnits, self.__units ):
			return True
		
		return False
	
	
	def Update( self ):
		""" Updates the areas unit list. If the area is auto updating it will
		post an event for every arrival and departure.
		"""
		if not self.__updater is None:
			oldUnits = self.__units
		
		## we updates everytime, watch out for performance problems
		#if self.__lastUpdateTime != base.GetCurrentTime():
		self.__units = wicg.GetUnitsInAreaXZ( self.__position, self.__radius )
		#self.__lastUpdateTime = base.GetCurrentTime()

	
	def __getName( self ):
		""" Get accessor for Area.__name
		"""
		return self.__name
	
	myName = property( __getName )
	
	
	def __getPosition( self ):
		""" Get accessor for Area.__position
		"""
		return self.__position
	
	def __setPosition( self, aPosition ):
		""" Set accessor for Area.__position
		"""
		self.__lastUpdateTime = -1
		if isinstance( aPosition, position.Position ):
			self.__position = aPosition
		else:
			self.__position = position.Position( *aPosition )
		
		return self.__position
	
	myPosition = property( __getPosition, __setPosition )
	
	myPos = property( __getPosition, __setPosition )


	def __getRadius( self ):
		""" Get accessor for Area.__radius
		"""
		return self.__radius
	
	def __setRadius( self, aRadius ):
		""" Set accessor for Area.__radius
		"""
		self.__lastUpdateTime = -1
		self.__radius = aRadius
	
	myRadius = property( __getRadius, __setRadius )
	
	
	def SetRadius( self, aRadius ):
		
		self.__lastUpdateTime = -1
		self.__radius = aRadius
		
	
	def __getUnits( self ):
		""" Get accessor for Area.__units
		"""
		self.Update()
		return self.__units
	
	myUnits = property( __getUnits )
	
	
	def HavePlayerUnit( self, aPlayer ):
		""" Returns True if a unit owned by aPlayer is in the area. Otherwise False
		"""
		self.Update()
		
		for unitId in self.__units:
			if unit.theUnits[unitId].myOwner == aPlayer and not common.IsRadarScan( unitId ):
				return True
			
		return False


	def HavePlayerUnitNotChopper( self, aPlayer ):
		""" Returns True if a unit owned by aPlayer is in the area. Otherwise False
		"""
		self.Update()
		
		for unitId in self.__units:
			if unit.theUnits[unitId].myOwner == aPlayer and not common.IsRadarScan( unitId ) and not common.IsAir( unitId ):
				return True
			
		return False


	def HaveRadarScanUnit( self, aPlayer ):

		self.Update()
		
		for unitId in self.__units:
			if unit.theUnits[unitId].myOwner == aPlayer and common.IsRadarScan( unitId ):
				return True
			
		return False

		
	def HaveTeamUnit( self, aTeam ):
		""" Returns True if a unit in team aTeam is in the area. Otherwise False
		"""
		self.Update()
		
		for unitId in self.__units:
			if unit.theUnits[unitId].myTeam == aTeam:
				return True
			
		return False
	
	
	def HaveGroup( self, aGroup ):
		""" Returns True if a all units in aGroup is in the area. Otherwise False
		"""
		
		self.Update()
		
		c = 0
		for unitId in self.__units:
			if aGroup.IsUnitInGroup( unitId ):
				c += 1
		
		if c < aGroup.Size():
			return False
		
		return True	
	
	
	def HaveGroupUnit( self, aGroup ):
		""" Returns True if a unit in Group aGroup is in the area. Otherwise False
		"""
		self.Update()
		
		for unitId in self.__units:
			if aGroup.IsUnitInGroup(unitId):
				return True
			
		return False


class Areas( object ):
	""" Container for all areas. So far it's not keepin references to the
	areas.
	"""
	__areaCounter = 0
	
	@classmethod
	def GetUniqueName( cls ):
		cls.__areaCounter += 1
		return "Area_%d" % cls.__areaCounter
	
	
	def __init__( self ):
		
		self.__areas = []
		
	
	def AddArea( self, anArea ):
		
		self.__areas.append( anArea )
		
	
	def RemoveArea( self, anArea ):
		
		if anArea in self.__areas:
			self.__areas.remove( anArea )
	
	
	def __getAreas( self ):
		
		return self.__areas
		
	myAreas = property( __getAreas )
	
	
theAreas = Areas()
