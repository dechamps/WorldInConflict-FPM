import debug

class Position( object ):
	""" Basic class to represent a Position.

	Members:
	 myX - X part of position
	 myY - Y part of position
	 myZ - Z part of position
	"""

	def __init__( self, anX = 0.0, anY = 0.0, aZ = 0.0 ):
		""" Standard constructor

		Args:
		 anX - initial value of myX
		 anY - initial value of myY
		 aZ - initial value of myZ
		"""
		self.__x = float( anX )
		self.__y = float( anY )
		self.__z = float( aZ )
	
	
	def __pos__( self ):
		return self
		
	
	def __copy__( self ):
		return Position( self.__x, self.__y, self.__z )
	
	
	def __getX( self ):
		""" Simple get accessor for Position::__x
		
		Args:
		 None
		
		Returns:
		 (float) The x value of the position
		"""
		return self.__x

	def __setX( self, aNewXValue ):
		""" Simple set accessor for Position::__x
		
		Args:
		 aNewXValue - (float) New value of the X position
		
		Returns:
		 Nothing
		"""
		self.__x = float( aNewXValue )

	x = property( __getX, __setX )
	myX = property( __getX, __setX )


	def __getY( self ):
		""" Simple get accessor for Position::__y
		
		Args:
		 None
		
		Returns:
		 (float) The y value of the position
		"""
		return self.__y

	def __setY( self, aNewYValue ):
		""" Simple set accessor for Position::__y
		
		Args:
		 aNewYValue - (float) New value of the Y position
		
		Returns:
		 Nothing
		"""
		self.__y = float( aNewYValue )

	y = property( __getY, __setY )
	myY = property( __getY, __setY )


	def __getZ( self ):
		""" Simple get accessor for Position::__z
		
		Args:
		 None
		
		Returns:
		 (float) The z value of the position
		"""
		return self.__z


	def __setZ( self, aNewZValue ):
		""" Simple set accessor for Position::__z
		
		Args:
		 aNewZValue - (float) New value of the Z position
		
		Returns:
		 Nothing
		"""
		self.__z = float( aNewZValue )

	z = property( __getZ, __setZ )
	myZ = property( __getZ, __setZ )


	def __str__( self ):
		""" Returns string representation of position

		Args:
		 none
		"""
		try:
			return "%2.2f,%2.2f,%2.2f" % ( self.__x, self.__y, self.__z )
			
		except Exception, e:
			return "Failed to fetch Position data: %s" % e


	def __add__( self, p ):
		""" Overloaded + operator.
		
		Args:
		 p - (Position) The Position to add to this Position
		 
		Returns:
		 The new Position
		"""
		
		return Position( self.__x + p.myX, self.__y + p.myY, self.__z + p.myZ )
		

	def __sub__( self, p ):
		""" Overloaded - operator.
		
		Args:
		 p - (Position) The position to subtract from this Position
		 
		Returns:
		 The new Position
		"""
		
		return Position( self.__x - p.myX, self.__y - p.myY, self.__z - p.myZ )
	

	def __mul__( self, f ):
		""" Overloaded * operator.
		
		Args:
		 f - (float) The float to multiply this Position with
		 
		Returns:
		 The new Position
		"""
		
		return Position( self.__x * f, self.__y * f, self.__z * f )
	

	def Set( self, anX, anY, aZ ):
		""" Set object members

		Args:
		 anX - new value for myX
		 anY - new value for myY
		 aZ - new value for myZ
		"""
		self.__x = float( anX )
		self.__y = float( anY )
		self.__z = float( aZ )


	def Length( self ):
		""" Get the length of this position.
		
		Args:
		 None
		 
		Returns:
		 The length of this position
		"""
		
		import math
		
		return math.sqrt( self.__x * self.__x + self.__y * self.__y + self.__z * self.__z )


	def Normalize( self ):
		""" Normalizes the position (length=1).
		
		Args:
		 None
		 
		Returns:
		 self
		"""
		
		l = self.Length()
		
		if l != 0:
			self.__x /= l
			self.__y /= l
			self.__z /= l
		
		return self

	
	def AlmostEqual( self, aPos ):
		
		THRESHOLD = 0.01
		return abs(self.__x - aPos.myX) < THRESHOLD and abs(self.__y - aPos.myY) < THRESHOLD and abs(self.__z - aPos.myZ) < THRESHOLD
		
	
	@staticmethod
	def Create( anX = 0.0, anY = 0.0, aZ = 0.0 ):
		""" Static method for creating a new Position instance
		
		Args:
		 anX - (float) X component of Position
		 anY - (float) Y component of Position
		 aZ - (float) Z component of Position
		
		Returns:
		 a new Position instance with the optional given values
		"""
		return Position( anX, anY, aZ )
