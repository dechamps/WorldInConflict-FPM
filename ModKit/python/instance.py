import wicg, debug

from position import Position

class InstanceException( Exception ): pass
class UnknownInstanceException( InstanceException ): pass


class Instance( object ):
	""" Instance class.

	A instance object represents position and orientation or radius of data in
	the <map>instances file (sphere instances have radius but no orientation,
	all others have orientation but no radius).

	"""
	def __init__( self, aName ):
		""" Standard constructor.
		
		aName - (string) Name of the instance to be loaded
		"""
		self.__name			= aName
		self.__position		= Position()
		self.__orientation	= 0.0
		self.__radius		= 0.0
		self.__type			= 'not an agent'

		if wicg.GetInstanceData( self ) is None:
			raise UnknownInstanceException( 'wicg.GetInstanceData returned None. Check your juice for %s.' % aName )

		debug.DebugMessage( 'A new instance created: %s' % self )
		return
	
	
	def __pos__( self ):
		return self.__position
		
	
	def __radius__( self ):
		return self.__radius
		
	def __area__( self ):
		import area
		return area.Area( self.__position, self.__radius )
	
	
	def __getName( self ):
		""" Get accessor fot Instance::__name
		
		Returns the name of instance
		"""
		return self.__name

	myName = property( __getName )


	def __getPosition( self ):
		"""
		"""
		return self.__position
	
	myPos = property( __getPosition )


	def __getOrientation( self ):
		"""
		"""
		return self.__orientation
	
	myOri = property( __getOrientation )
	
	
	def __getRadius( self ):
		"""
		"""
		return self.__radius

	myRadius = property( __getRadius )
	
	
	def SetRadius( self, aRadius ):
		
		self.__radius = aRadius
	

	def __getType( self ):
		"""
		"""
		return self.__type

	myType = property( __getType )


	def __str__( self ):
		"""
		"""
		theName = self.__name
		thePosition = "%s" % self.__position
		theOrientation = "%s - %s" % ( self.__orientation, type( self.__orientation ) )
		theRadius = "%s - %s" % ( self.__radius, type( self.__radius ) )
		theType = self.__type
		
		return """
<instance>
	name:			%s
	position:		%s
	orientation:	%s
	radius:			%s
	type:			%s
</instance>
""" % ( theName, thePosition, theOrientation, theRadius, theType )


class Instances( object ):
	"""
	"""
	def __init__( self ):
		"""
		"""
		self.__instances = {}
	
	
	def __getitem__( self, aKey ):
		""" Magic method to treat an Instances instance as a dictionary
		"""
		if not isinstance( aKey, str ):
			raise ValueError( 'Instances can only be accessed by their string name' )
		
		if not aKey in self.__instances:
			self.__instances[aKey] = Instance( aKey )
		
		return self.__instances[aKey]
	
	
	def __setitem__( self, aKey, aValue ):
		raise Exception( 'Cannot change values here' )
	
	
	def __delitem__( self, aKey ):
		raise Exception( 'Cannot delete values here' )
	
	
	def __len__( self ):
		return self.__instances.__len__()
	
	
	def __iter__( self ):
		return self.__instances.__iter__()

theInstances = Instances()