import debug, stringedmethod


class BadActionException( Exception ): pass										# Raised when an action is created that cannot execute properly


class Action ( object ):
	"""A combination of a function and some arguments. Used for callbacks, reactions, commands etc."""
	
	def __init__( self, aFunction, *someArgs ):
		"""	If the aFuntion is an unbound memberfunction, the first item in someArgs must be the
			instance to bind the function to.
		"""
		if not callable( aFunction ):
			raise BadActionException( 'First argument is not callable. %s' % aFunction )
		
		if type( aFunction ) == type( self.__init__ ):
			if aFunction.im_self is not None:
				self.__Function = stringedmethod.StringedMethod( aFunction )
			else:
				self.__Function = stringedmethod.StringedMethod( aFunction, someArgs[0] )
				someArgs = someArgs[1:]
			
		elif type( aFunction ) == type( [].pop ) and aFunction.__self__ is not None:
			self.__Function = stringedmethod.StringedMethod( aFunction )
			
		else:
			self.__Function = aFunction
		
		self.__Arguments = []
		unboundFunction = None
		
		for argument in someArgs:
			if unboundFunction:
				self.__Arguments.append( stringedmethod.StringedMethod( unboundFunction, argument ) )
				unboundFunction = None
				continue
			
			if type( argument ) == type( self.__init__ ):
				if argument.im_self is None:
					unboundFunction = argument
				else:
					self.__Arguments.append( stringedmethod.StringedMethod( argument ) )
				continue
			
			self.__Arguments.append( argument )
		
		if __debug__ and self.__str__() not in debug.BannedActions:
			debug.DebugMessage( "A new action created: %s" % self )
	
	
	def __str__( self ):
		"""	Returns a string description of the Action instance.
		"""
		if isinstance( self.__Function, stringedmethod.StringedMethod ):
			stringRep = "%s(" % self.__Function
		else:
			stringRep = "%s(" % self.__Function.__name__
		
		counter = 0
		for arg in self.__Arguments:
			if counter < (len(self.__Arguments) - 1):
				stringRep += "%s, " % str( arg )
			else:
				stringRep += "%s" % str( arg )
			
			counter += 1
		
		stringRep += ")"
		
		return stringRep
	
	
	def __call__( self ):
		"""	Makes it possible to call the Action as any normal function.
		"""
		return self.Execute()
	
	
	def __getArguments( self ):
		"""	Get accessor for __Arguments.
		"""
		return self.__Arguments
	
	myArguments = property( __getArguments )
	
	
	def Execute( self ):
		"""	Executes the Action's function with the stored arguments.
		"""
		if __debug__ and self.__str__() not in debug.BannedExecutions:
			debug.DebugMessage( 'Action::Execute - %s' % self )
		
		if len( self.__Arguments ) == 0:
			return self.__Function()
		else:
			return self.__Function( *self.__Arguments )
