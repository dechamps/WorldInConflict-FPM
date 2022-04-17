import base, wicg


class GameObjectException( Exception ): pass
class UnknownGameObjectException( GameObjectException ): pass


class GameObject( object ):
	""" wrapper for GameObjects
	"""
	
	def __init__( self, aName ):
		""" Constructor
		"""
		self.__name = aName
		self.__position = None
		self.__health = None
		self.__heading = None
		self.__armor = None
		self.__maxHealth = None
		
		self.__lastUpdateTime = None
		self.Update( True, True )
	
	
	def __pos__( self ):
		
		return self.__position
	
	
	def __getArmor( self ):
		""" Get accessor for GameObject.__armor
		"""
		return self.__armor
	
	myArmor = property( __getArmor )
	
	
	def __getHeading( self ):
		""" Get accessor for GameObject.__heading
		"""
		self.Update()
		return self.__heading
	
	myHeading = property( __getHeading )
	
	
	def __getHealth( self ):
		""" Get accessor for GameObject.__health
		"""
		self.Update()
		return self.__health
	
	myHealth = property( __getHealth )
	
	
	def __getMaxHealth( self ):
		""" Get accessor for GameObject.__maxHealth
		"""
		return self.__maxHealth
	
	myMaxHealth = property( __getMaxHealth )
	
	
	def __getName( self ):
		""" Get accessor for GameObject.__name
		"""
		return self.__name
	
	myName = property( __getName )
	
	
	def __getPosition( self ):
		""" Get accessor for GameObject.__position
		"""
		self.Update()
		return self.__position
	
	myPosition = property( __getPosition )
	
	
	def Update( self, aFetchStaticsFlag = False, aForceUpdateFlag = False ):
		""" Updates the GameObject from the game
		"""
		if self.__lastUpdateTime != base.GetCurrentTime() or aForceUpdateFlag:
			wicg.GetGameObjectData( self, aFetchStaticsFlag )
			self.__lastUpdateTime = base.GetCurrentTime()
	
	
	def Damage( self, anAmountOfDamage ):
		""" Inflict given damage on a GameObject
		"""
		wicg.DamageGameObject( self.__name, anAmountOfDamage )
	
	
	def Destroy( self ):
		""" Inflict damage on a GameObject
		"""
		self.Update()
		wicg.DamageGameObject( self.__name, self.__health + self.__armor )


class GameObjects( object ):
	""" Containerclass for caching GameObject instances
	"""
	
	def __init__( self ):
		""" Constructor
		"""
		self.__gameobjects = {}
	
	
	def __getitem__( self, aKey ):
		""" Enables dictionary like access to the GameObjects
		"""
		if not aKey in self.__gameobjects:
			self.__gameobjects[aKey] = GameObject( aKey )
		
		self.__gameobjects[aKey].Update()
		
		return self.__gameobjects[aKey]
	
	
	def __setitem__( self, aKey, aValue ):
		if not isinstance( aValue, GameObject ):
			raise ValueError( "theGameObjects only stores GameObject instances" )
		
		return self.__gameobjects.__setitem__( aKey, aValue )
	
	def __delitem__( self, aKey ):
		return self.__gameobjects.__delitem__( aKey )
	
	def __len__( self ):
		return self.__gameobjects.__len__()
	
	def __iter__( self ):
		return self.__gameobjects.__iter__()

