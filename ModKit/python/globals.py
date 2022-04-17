class GlobalsContainer( object ):
	"""	Container for data that should be persistent
	"""
	__globals = {}


	def __getattr__( self, aName ):
		"""
		"""
		if not aName in self.__globals:
			raise AttributeError( "There is no global '%s' defined!" % aName )
		else:
			return self.__globals[aName]
	
	
	def __setattr__( self, aName, aValue ):
		"""
		"""
		self.__globals[aName] = aValue
	
	
	def __getGlobals( self ):
		"""
		"""
		return __globals
	
	def __setGlobals( self, someGlobals ):
		"""
		"""
		self.__globals = someGlobals
	
	globals = property( __getGlobals, __setGlobals )


theGlobals = GlobalsContainer()
