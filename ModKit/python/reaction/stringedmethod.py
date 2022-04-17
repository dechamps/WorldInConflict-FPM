import debug

class StringedMethod( object ):
	""" This class is made as a workaround for pickles inability to serialize
		instancemethod objects. It can take the string representation of a function
		and an object instance and from that be fully callable as it was the
		instancemethod itself.
	"""
	def __init__( self, anInstanceMethod, anInstance = None ):
		""" Constructor. If anInstanceMethod is unbound anInstance have to
			specify wich instance the method should be called from.
		"""
		if type( anInstanceMethod ) == type( self.__init__ ):
			if anInstanceMethod.im_self is None:
				self.__instance = anInstance
			else:
				self.__instance = anInstanceMethod.im_self
			
			self.__methodName = anInstanceMethod.__name__
			
		elif type( anInstanceMethod ) == type( [].pop ):
			self.__instance = anInstanceMethod.__self__
			
			self.__methodName = anInstanceMethod.__name__
			
		else:
			self.__methodName = anInstanceMethod
			self.__instance = anInstance
		
		
		self.__instance.__getattribute__( self.__methodName )
		self.__dict__['__name__'] = self.__methodName
	
	
	def __str__( self ):
		"""	Returns a string description of the StringedMethod instance.
		"""
		return self.__methodName
	
	
	def __call__( self, *someArgs ):
		"""	Makes it possible to call the StringedMethod as any normal function.
		"""
		return self.__instance.__getattribute__( self.__methodName )( *someArgs )
	
	
	def __getMethodName( self ):
		"""	Get accessor for __methodName
		"""
		return self.__methodName
	
	myMethodName = property( __getMethodName )
