import wicg, base


class UnitException( Exception ): pass
class UnknownUnitException( UnitException ): pass
class UnknownUnitTypeException( UnitException ): pass
class IllegalUnitException( UnitException ): pass
class UnitDestroyedException( UnitException ): pass
class IllegalUnitDestinationException( UnitException ): pass


FREE_FIRE	= 0
RETURN_FIRE	= 1
HOLD_FIRE	= 2


class Unit( object ):
	""" Unit class with relevant data. A unit will auto update if needed when it's members are read from.
	"""
	
	def __init__( self, anId ):
		""" Constructor function
		"""
		
		import position
		
		self.__heading = 0.0
		self.__health = -1
		self.__maxHealth = -1
		self.__lastUpdateTime = 0.0
		self.__maxSpeed = 0.0
		self.__owner = -1
		self.__position = position.Position()
		self.__squadId = -1
		self.__team = -1
		self.__type = 0
		self.__uiName = ""
		self.__id = anId
		self.__isContainer = False
		self.__isHoldingFire = False
		self.__invulnerable = False
		
		self.__minrange = 0.0
		self.__maxrange = 0.0
		
		self.Update( True, True )
		self.__speed = self.__maxSpeed


	def __str__( self ):
		""" Returns basic unit info in the form of a string.
		"""
		infoString = "\n<unit id='%d'>\n" % self.__id
		try:
			self.Update()
		except UnknownUnitException:
			infoString = "\t!!!THE UNIT IS DESTROYED!!!\n"
		
		infoString = "%s\n\theading: %2.2f" % ( infoString, self.__heading )
		infoString = "%s\n\thealth: %d" % ( infoString, self.__health )
		infoString = "%s\n\tid: %d" % ( infoString, self.__id )
		infoString = "%s\n\tmaxSpeed: %2.2f" % ( infoString, self.__maxSpeed )
		infoString = "%s\n\towner: %d" % ( infoString, self.__owner )
		infoString = "%s\n\tposition: %s" % ( infoString, self.__position )
		infoString = "%s\n\tsquadId: %d" % ( infoString, self.__squadId )
		infoString = "%s\n\tspeed: %2.2f" % ( infoString, self.__speed )
		infoString = "%s\n\tteam: %d" % ( infoString, self.__team )
		infoString = "%s\n\ttype: %d" % ( infoString, self.__type )
		infoString = "%s\n\tUIName: %s" % ( infoString, self.__uiName )
		infoString = "%s\n</unit>" % infoString
		
		return infoString
	
	
	def __pos__( self ):
		return self.__position
	
	
	def __getIsHoldingFire( self ):
		""" Get accessor for Unit.__isHoldingFire
		"""
		
		self.__isHoldingFire = wicg.GetUnitMember( self.__id, 'isholdingfire' )
		return self.__isHoldingFire
	
	
	def __setIsHoldingFire( self, aHoldFireFlag ):
		""" Set accessor for Unit.__isHoldingFire
		"""
		if not isinstance( aHoldFireFlag, bool ):
			raise ValueError
		
		wicg.SetUnitData( self.__id, "isHoldingFire", aHoldFireFlag )
		self.__isHoldingFire = aHoldFireFlag
	
	myIsHoldingFire = property( __getIsHoldingFire, __setIsHoldingFire )
	
	
	def __getHeading( self ):
		""" Simple get accessor for Unit::__heading
		
		Args:
		 None
		
		Returns:
		 (float) Unit::__heading
		"""
		self.__heading = wicg.GetUnitMember( self.__id, 'heading' )
		return self.__heading
	
	def __setHeading( self, aHeading ):
		""" Simple set accessor for Unit::__heading
		
		Args:
		 aHeading - (float) the new heading of the unit in radians
		
		Returns:
		 Nothing
		"""
		try:
			wicg.SetUnitData( self.__id, "heading", aHeading )
		except Exception, e:
			base.DebugMessage( 'Unit::__setHeading' % e )

	myHeading = property( __getHeading, __setHeading )
	
	
	def __getHealth( self ):
		""" Simple get accessor for Unit::__health
		
		Args:
		 None
		
		Returns:
		 (int) Unit::__health
		"""
		
		self.__health = wicg.GetUnitMember( self.__id, 'health' )
		return self.__health
	
	def __setHealth( self, aHealthValue ):
		""" Simple set accessor for Unit::__health
		
		Will automaticly cap the health to the unit types max health
		
		Args:
		 aNewHealthValue - (int) New health of the unit
		
		Returns:
		 Nothing
		"""
		
		## is this a player unit
		if self.__getOwner() == 1: ## Use __getOwner so we really get the current owner of the unit. davidh 080722.
			
			wicg.SetPlayerUnitHealth( self.__id, aHealthValue )			
		else:
			try:
				wicg.SetUnitData( self.__id, "health", aHealthValue )
			except Exception, e:
				base.DebugMessage( 'Unit::__setHealth - %s' % e )

	myHealth = property( __getHealth, __setHealth )
	
	
	def __getInvulnerable( self ):
		self.__invulnerable = wicg.GetUnitMember( self.__id, 'invunerable')
		return self.__invulnerable
	
	def __setInvulnerable( self, anInvulnerableFlag ):

		## if unit isn't a script owned unit (0)
		if self.__getOwner() != 0:
			wicg.SetPlayerUnitInvulnerable( self.__id, anInvulnerableFlag )
		else:
			wicg.SetUnitData( self.__id, 'invulnerable', anInvulnerableFlag )
		self.__invulnerable = anInvulnerableFlag

			
	myInvulnerable = property( __getInvulnerable, __setInvulnerable )
	

	def IsInvulnerable( self ):
		
		self.__invulnerable = wicg.GetUnitMember( self.__id, 'invunerable')
		return self.__invulnerable

	
	def __getMaxHealth( self ):
		""" Simple get accessor for Unit::__maxHealth
		
		Args:
		 None
		
		Returns:
		 (int) Unit::__maxHealth
		"""
		
		self.__maxHealth = wicg.GetUnitMember( self.__id, 'maxhealth')
		return self.__maxHealth
		
	myMaxHealth = property(__getMaxHealth)


	def __getId( self ):
		""" Simple get accessor for Unit::__id
		
		Args:
		 None
		
		Returns:
		 (int) User::__id
		"""
		return self.__id

	myID = property( __getId )
	
	
	def __getIsCointainer( self ):
		""" Get accessor for Unit.__isContainer
		"""
		self.__isContainer = wicg.GetUnitMember( self.__id, 'iscontainer' )
		return self.__isContainer

	myIsContainer = property( __getIsCointainer )


	def __getLastUpdateTime( self ):
		return self.__lastUpdateTime
	
	def __setLastUpdateTime( self, anUpdateTime ):
		self.__lastUpdateTime = anUpdateTime
		
	myLastUpdateTime = property( __getLastUpdateTime, __setLastUpdateTime )


	def __getMaxSpeed( self ):
		"""
		"""
		self.__maxSpeed = wicg.GetUnitMember( self.__id, 'maxspeed' )
		return self.__maxSpeed
	
	myMaxSpeed = property( __getMaxSpeed )


	def __getOwner( self ):
		""" Simple get accessor for Unit::__owner
		
		Args:
		 None
		
		Returns:
		 (int) Unit::__owner
		"""
		
		self.__owner = wicg.GetUnitMember( self.__id, 'owner' )
		return self.__owner
	
	def __setOwner( self, anOwner ):
		""" Simple set accessor for Unit::__owner
		
		Args:
		 anOwner - (int) New owner of unit
		
		Returns:
		 None
		"""
		try:
			wicg.SetUnitData( self.__id, "owner", anOwner )
		except Exception, e:
			base.DebugMessage( 'Unit::__setOwner' % e )

	myOwner = property( __getOwner, __setOwner )


	def __getPosition( self ):
		""" Simple get accessor for Unit::__position
		
		Args:
		 None
		
		Returns:
		 (Position) Unit::__position
		"""
		
		self.__position = wicg.GetUnitMember( self.__id, 'position' )
		return self.__position
	
	
	def __setPosition( self, aPosition ):
		""" Simple set accessor for Unit::__position
		
		Args:
		 aPosition - (Position) New position of unit
		
		Returns:
		 Nothing
		"""
		try:
			wicg.SetUnitData( self.__id, 'position', aPosition )

		except Exception, e:
			base.DebugMessage( 'Unit::__setHeading - %s' % e )

	myPos = property( __getPosition, __setPosition )

	
	def __getSpeed( self ):
		"""
		"""
				
		return self.__speed
	
	def __setSpeed( self, aNewSpeed ):
		"""
		"""
		self.__speed = max( 0.0, min( self.__maxSpeed, aNewSpeed ) )

	mySpeed = property( __getSpeed, __setSpeed )
	
	
	def __getSquadId( self ):
		"""
		"""
		self.__squadId = wicg.GetUnitMember( self.__id, 'squadid' )
		return self.__squadId
	
	mySquadId = property( __getSquadId )
	

	def __getTeam( self ):
		""" Simple get accessor for Unit::__team
		
		Args:
		 None
		
		Returns:
		 (int) Unit::__team
		"""
		
		self.__team = wicg.GetUnitMember( self.__id, 'team' )
		return self.__team
	
	def __setTeam( self, aTeam ):
		""" Simple set accessor for Unit::__team
		
		Args:
		 aTeam - (int) New team of unit
		
		Returns:
		 Nothing
		"""
		try:
			wicg.SetUnitData( self.__id, 'team', aTeam )
		except Exception, e:
			base.DebugMessage( 'Unit::__setTeam - %s' % e )


	myTeam = property( __getTeam, __setTeam )
	

	def __getType( self ):
		""" Simple get accessor for Unit::__type
		
		Args:
		 None
		
		Returns:
		 (int) Unit::__type
		"""
		self.__type = wicg.GetUnitMember( self.__id, 'type' )
		return self.__type
	
	myType = property( __getType )
	
	
	def __getUIName( self ):
		""" Simple get accessor for Unit::__uiName
		
		Args:
		 None
		
		Returns:
		 (string) Unit::__uiName
		"""
		self.__uiName = wicg.GetUnitMember( self.__id, 'uiname' )
		return self.__uiName
	
	myUIName = property( __getUIName )


	def __getMinRange( self ):
		"""
		"""
		self.__minrange = wicg.GetUnitMember( self.__id, 'minrange' )
		return self.__minrange
	
	myMinRange = property( __getMinRange )


	def __getMaxRange( self ):
		"""
		"""
		self.__maxrange = wicg.GetUnitMember( self.__id, 'maxrange' )
		return self.__maxrange
	
	myMaxRange = property( __getMaxRange )


	def Attack( self, aTarget ):
		"""
		"""
		return wicg.Attack( self, aTarget )


	def AttackPosition( self, aPosition ):
		""" Tells the Unit to attack a Position. Only units owned by
		script-player can be issued an attack order.

		aPosition - (Position) position to attack

		Should not be called from a client script.

		returns -1 on error. 1 otherwise.
		"""
		wicg.UnitAttackPosition( self.__id, aPosition )

		return 1


	def AttackUnit( self, aUnitToAttack ):
		""" Tells the Unit to attack an Enemy unit with a certain ID. Only
		units owned by script-player can be issued an attack order.

		aUnitToAttackID - (int) Unit to attack

		Should not be called from a client script.

		returns -1 on error. 1 otherwise.
		"""
		wicg.UnitAttackUnit( self.__id, aUnitToAttack )

		return 1


	def ChangeHealth( self, aChangeDelta ):
		""" Call this function to change the health of a specific unit.

		aChangeDelta - (int) a change in health (positive for increased health, negative for decreased)

		Should not be called from a client script.
		"""
		
		self.__setHealth( self.__health + aChangeDelta )

		return 0


	def SetHealth( self, aNewHealth ):
		""" Call this function to set the health of a specific unit.

		aNewHealth - (int) a new health

		Should not be called from a client script.
		"""
		
		self.__setHealth( aNewHealth )

		return 0


	def ChangeOwner( self, aNewOwner ):
		""" Call this function to change the owner of a unit. Only works on
		units owned by Script Player.

		aNewOwner - (int) the new owner (Can only change owner on units belonging to Script Player (0)

		Should not be called from a client script.
		"""
		try:
			self.__setOwner( aNewOwner )
		except Exception, e:
			base.DebugMessage( 'Unit::ChangeOwner() - %s' % e )

		return 0


	def EnterBuilding( self, aBuilding, aInstantEnter = False ):
		""" Tells the Unit to enter a building identified by aBuildingString.
		Only units owned by script-player can be issued an attack order.

		aBuildingString - (str) building to enter

		Should not be called from a client script.

		returns -1 on error. 1 otherwise.
		"""
		wicg.UnitEnterBuilding( self.__id, aBuilding, aInstantEnter )

		return 1


	def EnterContainer( self, aContainerUnit, anInstantEnterFlag = False ):
		""" Tells the Unit to enter another unit with ID aContainerUnit. Only units owned by script-player can be issued orders.

		aContainerUnit  - (int) A container unit to enter

		Should not be called from a client script.

		returns True on success and False on failure
		"""
		return wicg.UnitEnterContainer( self.__id, aContainerUnit, anInstantEnterFlag )


	def GetInfoString( self ):
		"""
		"""
		return self.__str__()
	

	def LookAt( self, aTarget ):
		""" Call this function to give the Unit an order to turn towards a
		position. Only works on units owned by Script Player.

		aPosition   - (Position) aPosition to look at

		Should not be called from a client script.
		"""
		self.MoveTo( self.__position, base.GetHeadingXZ( self.__position, aTarget ) );

		return 0


	def MoveTo( self, aDestination, aHeading = None, aSpeed = None, aBackwards = False ):
		""" Call this function to give a move-order to the Unit. Only works on
		units owned by Script Player.

		aDestination	- (Position) a end-position
		aHeading		- (float) a heading in radians

		Should not be called from a client script.
		"""
		if aSpeed is None:
			aSpeed = self.__speed
		
		if aHeading is None:
			aHeading = 100.0

		try:
			return wicg.MoveUnit( self.__id, aDestination, float( aHeading ), aSpeed, aBackwards )
		
		except Exception, e:
			if __debug__:
				base.DebugMessage( 'Unit(%d)::MoveTo - pos(%s), %s' % ( self.__id, aDestination, e ) )
			return False


	def Stop( self ):
		""" Tells the Unit to stop moving (if it is indeed moving). Only units
		owned by script-player can be orders.
		
		returns -1 on error. 1 otherwise.
		
		Should not be called from a client script.
		"""
		wicg.UnitStop( self.__id )
		
		return 1


	def UnloadAll( self ):
		""" Tells the Unit unload all contained units.
		
		returns -1 on error. 1 otherwise.
		"""
		
		wicg.UnitUnloadContainer( self.__id )
		
		return 1


	def Update( self, aForceUpdateFlag = False, anUpdateStaticsFlag = False ):
		""" Updates the object woth data from the game.
		
		Args:
		 aForceUpdateFlag - (bool) Set to force an update of the unit data
		 anUpdateAllFlag - (bool) Set to update the units unchanging data
		"""
		if self.__lastUpdateTime == base.GetCurrentTime() and not aForceUpdateFlag:
			return True
		
		wicg.GetUnitData( self, anUpdateStaticsFlag )
		
		self.__lastUpdateTime = base.GetCurrentTime()
		
		return True
		
	def UseOffensiveSpecialAbilityOnUnit(self, aTargetId, anOverrideCooldownFlag = 0):
		"""
		aTargetUnitId (int) - The unit id of the target unit.
		anOverrideCooldownFlag (int) - If set to 1 this will shoot the special ability and reset the 
			cooldown no matter what, if set to 0 the action will fail as usual if it is on cooldown.
		"""
		return wicg.UseOffensiveSpecialAbilityOnUnit(self.__id, aTargetId, anOverrideCooldownFlag)

	def UseDefensiveSpecialAbility(self, anOverrideCooldownFlag = 0):
		"""
		anOverrideCooldownFlag (int) - If set to 1 this will shoot the special ability and reset the 
			cooldown no matter what, if set to 0 the action will fail as usual if it is on cooldown.
		"""
		return wicg.UseDefensiveSpecialAbility(self.__id, anOverrideCooldownFlag)
		
	def IsUnitInForest(self):
		return wicg.IsUnitInForest(self.__id)

class Units( object ):
	""" Container class for units. Caches units fetched from C++.
	"""

	def __init__( self ):
		""" Constructor
		"""
		self.__units = {}
	
	
	def __getitem__( self, aKey ):
		""" Fetches the given unit
		
		Args:
		 aKey - (int) Slot ID of unit to fetch
		
		Returns:
		 The requested unit
		"""
		if type( aKey ) != int:
			raise TypeError( "Units.__units can only be accessed with an int key, was given a %s" % type( aKey ) )
		
		if not aKey in self.__units:
			self.__units[aKey] = Unit( aKey )
		
		return self.__units[aKey]


theUnits = Units()
