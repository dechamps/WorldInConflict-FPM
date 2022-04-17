import wicg, base


class BuildingException( Exception ): pass
class UnknownBuildingException( BuildingException ): pass
class BuildingDestroyedException( BuildingException ): pass


class Building( object ):
	""" Building class wrapper

	Members:
	 health - (int) Current health of building
	 armor - (int) Armor of building
	 isVulnarable - (bool) True if the building takes damage
	 maxHealth - (int) Max health of undamaged building
	 numSlots - (int) Number of unit slots in building
	"""
	
	def Damage( self, aDamage ):
		"""
		"""
		return wicg.DamageBuilding( self.__name, aDamage )


	def __init__( self, aName ):
		""" Standard constructor
		
		Args:
		 aName - (String) Name of building
		"""
		self.__lastUpdate = -1
		self.__health= -1
		self.__armor = -1
		self.__isVulnerable = -1
		self.__maxHealth = -1
		self.__numSlots = -1
		self.__position = None
		self.__name = aName
		self.__update( True, True )


	def __str__( self ):
		""" Returns a string representation of the building
		
		Args:
		 none
		
		Returns:
		 String with relevant building data
		"""
		return "\n<Building>\n\tName:%s\n\tHealth:%d\n\tMaxHealth:%d\n\tVulnerable:%s\n\tArmor:%d\n\tNumSlots:%d\n</Building>" % ( self.__name, self.__health, self.__maxHealth, self.__isVulnerable, self.__armor, self.__numSlots )

	
	def __pos__( self ):
		
		return self.__position
	

	def __update( self, aForceFlag = False, aGetStaticDataFlag = False ):
		""" Updates the cached building data
		
		Args:
		 none
		
		Returns:
		 True on success and False on failure
		"""
		if self.__lastUpdate != base.GetCurrentTime() or aForceFlag:
			self.__lastUpdate = base.GetCurrentTime()
			wicg.GetBuildingData( self, aGetStaticDataFlag )
		
		return True


	def __getHealth( self ):
		""" Get accessor for Building.health
		
		Args:
		 none
		
		Returns:
		 The buildings health
		"""
		self.__update()
		return self.__health

	""" Current condition of the building """
	myHealth = property( __getHealth )


	def __getArmor( self ):
		""" Retrieves the buildings current armour
		
		Args:
		 none
		
		Returns:
		 The buildings armour
		"""
		self.__update()
		return self.__armor

	""" Armor of the building """
	myArmor = property( __getArmor )


	def __getVulnerability( self ):
		""" Retrieves the buildings vulnerability state
		
		Args:
		 none
		
		Returns:
		 The buildings vulnerability state
		"""
		self.__update()
		return self.__isVulnerable


	def __setVulnerability( self, aVulnerabilityFlag ):
		""" Sets the buildings vulnerability state
		
		Args:
		 aVulnerabilityFlag
		
		"""
		
		if wicg.SetBuildingData( self.__name, 'isVulnerable', aVulnerabilityFlag ):
			self.__isVulnerable = aVulnerabilityFlag


	myIsVulnerable = property( __getVulnerability, __setVulnerability )


	def __getMaxHealth( self ):
		""" Retrieves the maximum health of the building
		
		Args:
		 none
		
		Returns:
		 (int) Max health of the building
		"""
		return self.__maxHealth

	""" Max health of the building """
	myMaxHealth = property( __getMaxHealth )


	def __getNumSlots( self ):
		""" Retrieves the number of slots the building have
		
		Args:
		 none
		
		Returns:
		 (int) Number of slots the building have
		"""
		return self.__numSlots

	""" Number of units that can fit in the building """
	myNumSlots = property( __getNumSlots )


	def __getName( self ):
		""" Simple get accessor for Building.__name
		
		Args:
		 none
		
		Returns:
		 The name of the buildings
		"""
		return self.__name

	myName = property( __getName )


	def __getPosition( self ):
		""" Simple get accessor for Building.__position
		
		Args:
		 none
		
		Returns:
		 The position of the buildings
		"""
		return self.__position

	myPosition = property( __getPosition )


	def Destroy( self ):
		""" Instantly destroys the building. Just a shortcut for 'health = 0'
		
		Args:
		 none
		
		Returns:
		 nothing
		"""
		self.Damage( self.__getHealth() )


class Buildings( object ):
	""" Class working as an interface to 'all' buildings

	Use as a dictionary giving either the int name or the string name of the building as index
	"""
	__buildings = {}


	def __getitem__( self, aKey ):
		""" Fetches the given building
		
		Args:
		 aKey - (int/string) Name of building to fetch
		
		Returns:
		 The given building
		""" 
		if not aKey in self.__buildings:
			self.__buildings[aKey] = Building( aKey )
			base.DebugMessage( "Fetched new building %s:%s" % ( aKey, self.__buildings[aKey] ) )
		
		self.__buildings[aKey]._Building__update()
		
		return self.__buildings[aKey]


theBuildings = Buildings()