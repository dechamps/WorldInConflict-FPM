import wicg, base, instance, debug, unit


class GameException( Exception ): pass
class UnknownSquadException( GameException ): pass


class Game( object ):
	""" Basic representation of the game itself.
	"""


	def CreateCommandPointEx( self, aName, aStartTeam = 0, aRetakeFlag = 1 ):
		""" Creates a zone.
		
		Call this to create the base zone. Call CreatePerimeterPoint() to
		create corresponding perimeter points.
		
		aPosition   - (float vector) Position of the command point flag.
		aStartTeam  - (int) Team that should own zone (0 is neutral)
		
		returns created CommandPointID
		
		Should not be called from a client script.
		"""
		wicg.CreateCommandPointEx( aName, aStartTeam, aRetakeFlag )
		
		return 0
	
	
	def CreateFortificationPointEx( self, aName, aCommandPoint ):
		""" Creates a fortification point
		
		aName			- (str) name of fortification Point
		aCommandPoint	- (str) name of command point parent
		
		Should not be called from a client script.
		"""
		wicg.CreateFortificationPointEx( aName, aCommandPoint )
		
		return 1


	def CreatePerimeterPointEx( self, aName, aCommandPoint ):
		""" Creates a perimeter point
		
		aName			- (str) name of Perimeter Point
		aCommandPoint	- (str) name of command point parent
		
		Should not be called from a client script.
		"""
		wicg.CreatePerimeterPointEx( aName, aCommandPoint )
		
		return 1


	def CreateUnit( self, aType, aUIName, aPosition, aHeading, anOwner, aTeam ):
		""" Creates a unit
		
		aType		- (int) the hashed value of a unittype (same as myType in Unit)
		aUIName		- (str) Unit UI name (not important, used to debug on error)
		aPosition	- (Position) position object of unit location
		aHeading	- (float) Heading of the unit
		anOwner		- (int) Owner of unit (1-16, 0 for units controlled by script)
		aTeam		- (int) Which team the unit should belong to (0 for neutral)
		
		Should not be called from a client script.
		
		returns the ID of the created unit. -1 if no unit was created.
		"""
		return wicg.CreateUnit( aType, aPosition, float( aHeading ), anOwner, aTeam )


	def CreateUnitFromInstance( self, anInstance, anOwner, aTeam ):
		""" Creates a unit
		
		anInstance	- (str) The instance that represents the unit to create
		anOwner		- (int) Owner of unit (1-16, 0 for units controlled by script)
		aTeam		- (int) Which team the unit should belong to (0 for neutral)
		
		Should not be called from a client script.
		
		returns the ID of the created unit. -1 if no unit was created.
		"""
		returnInstance = instance.theInstances[anInstance]
		
		return wicg.CreateUnit( base.StringToInt( returnInstance.myType ), returnInstance.myPos, returnInstance.myOri.x, anOwner, aTeam )


	def CreateSquadFromList( self, someUnitTypes, aPosition, aHeading, anOwner, aTeam ):
		""" Creates a unit
		
		someInstances - (list of instances) The instances to create units from
		aPosition - (Position) Squad spawn point
		aHeading - (float) Heading of the squad
		anOwner - (int) Owner of squad (1-16, 0 for units controlled by script)
		aTeam - (int) Which team the squad should belong to (0 for neutral)
		
		Should not be called from a client script.
		
		returns a list with the id's of the created units
		"""
		unitList = []
		
		if len( someUnitTypes ) > 6:
			raise ValueError( 'There is no support for squads with more than 6 members at the moment' )
		
		squadId = wicg.GetAndIncNextFreeSquadId()
		
		debug.DebugMessage( 'Next free squadId: %d ', squadId )
		
		for unitType in someUnitTypes:
			unitList.append( wicg.CreateUnit( unitType, aPosition, aHeading, anOwner, aTeam, squadId ) )
		
		return unitList
	
	
	def DeploySupportWeapon( self, aWeaponType, aTarget, aDirection, anUpgradeLevel ):
		"""
		"""
		return wicg.DeploySupportWeapon( aWeaponType, aTarget, aDirection, anUpgradeLevel )
	
	
	def HideGUIChunk( self, aGUIChunk ):
		"""
		"""
		from serverimports import SetCoreSystemState
		SetCoreSystemState( aGUIChunk, 'hidden' )
	
	
	def PauseGameMode( self ):
		"""
		"""
		wicg.SetGameModePauseState( 1 )
		
		## green smoke fix
		from serverimports import SetupShowPlayerDropZoneReaction
		SetupShowPlayerDropZoneReaction()

	def ShowGUIChunk( self, aGUIChunk ):
		"""
		"""
		from serverimports import SetCoreSystemState
		SetCoreSystemState( aGUIChunk, 'enabled' )


	def UnpauseGameMode( self ):
		"""
		"""
		wicg.SetGameModePauseState( 0 )


	def GetHeadingXZ( self, aFromPos, aToPos ):
		""" Returns the heading (in radians) from aFromPos to aToPos.
		
		aFromPos - (Position) From position
		aToPos   - (Position) To position
		
		returns the heading in radians
		"""
		return base.GetHeadingXZ( aFromPos, aToPos )


	def GetInstance( self, anInstanceName ):
		""" Retrieves instance information and returns an Instance object.
		
		An instance is a static object defined in Xed/WicEd. It can be a unit,
		prop or sphere/area definition (in case of a unit, it's where a unit is
		spawned, not the current position of the unit).
		
		anInstanceName - Name of instance to get
		"""
		return instance.theInstances[anInstanceName]


	def GetInstanceType(self, anInstanceName):
		""" Retrieves instance type information and returns s string.
		
		An instance is a static object defined in Xed/WicEd. It can be a
		unit, prop or sphere/area definition (in case of a unit, it's where
		a unit is spawned, not the current position of the unit).
		
		anInstanceName - Name of instance to get
		"""
		return instance.theInstances[anInstanceName].myType


	def GetUnit( self, aUnitId ):
		""" Returns a Unit object.
		
		aUnitID - (int) ID of unit to get.
		returns a Unit object of unit with aUnitID (if found, None otherwise)
		"""
		try:
			return unit.theUnits[aUnitId]
		except unit.UnknownUnitException:
			return None


	def GetUnitIDsInAreaXZ( self, aPosition, aRadius):
		""" Returns all units in area defined by aPosition and aRadius
		
		aPosition	- (Position) Position of area center
		aRadius		- (float) Radius of area
		
		returns a list of Unit objects (or empty list if no units).
		"""
		uids = wicg.GetUnitsInAreaXZ( aPosition, float( aRadius ) )
		
		return uids


	def GetUnitsInAreaXZ( self, aPosition, aRadius):
		""" Returns all units in area defined by aPosition and aRadius
		
		aPosition	- (Position) Position of area center
		aRadius		- (float) Radius of area
		
		returns a list of Unit objects (or empty list if no units).
		"""
		units	= []
		uids	= self.GetUnitIDsInAreaXZ( aPosition, aRadius )
		
		if uids is None:
			return []
		
		for id in uids:
			try:
				u = unit.theUnits[id]
			except unit.UnknownUnitException:
				continue
			
			units.append(u)
		
		return units
	
	
	def RemoveUnit( self, aUnitID, anExplodeFlag ):
		""" Removes a unit
		
		aUnitID			- (int) Unit ID of unit to remove
		anExplodeFlag	- (int) Set to 1 if the unit should explode upon removal.
		
		Should not be called from a client script.
		
		Returns 0 if something failed. 1 if the unit was found and removed.
		"""
		
		try:
			return wicg.RemoveUnit( aUnitID, anExplodeFlag )
		except unit.UnitException, e:
			debug.DebugMessage( 'Game::RemoveUnit()' % e )
			return 0


	def FadeIn( self, aFadeInTime = 2.0 ):
		"""
		"""
		wicg.FadeIn( float( aFadeInTime ) )
	
	
	def __init__( self, anIgnoredArgument = None, anOtherIgnoredArgument = None ):
		""" Constructor function.
		"""
		self.__isSinglePlayer = False
		
		wicg.GetGameData( self )
	
	
	def __getIsSinglePlayer( self ):
		""" Simple get accessor for Game::__isSinglePlayer
		"""
		return self.__isSinglePlayer
	
	myIsSinglePlayer = property( __getIsSinglePlayer )


theGame = Game()
