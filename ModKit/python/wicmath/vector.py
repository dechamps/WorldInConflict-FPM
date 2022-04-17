import math

from position import Position


class Vector( object ):
	""" Basic class to represent a 2D Vector.

	Members:
	 myX - X part of vector
	 myZ - Z part of vector
	"""

	
	def __init__( self, aX = 0.0, aZ = 0.0 ):
		""" Standard constructor

		Args:
		 aX - initial value of myX
		 aZ - initial value of myZ
		"""

		self.__x = 0.0
		self.__z = 0.0

		self.__x = float(aX)
		self.__z = float(aZ)
		
	
	def __copy__( self ):
		""" Makes a copy of this vector """
		return Vector( self.__x, self.__z )

	
	def __getX( self ):
		""" Simple get accessor for Vector::__x
		
		Args:
		 None
		
		Returns:
		 (float) The x value of the position
		"""
		
		return self.__x

	def __setX( self, aNewXValue ):
		""" Simple set function for Vector::__x
		
		Args:
		 aNewXValue - (float) New value of the X position
		
		Returns:
		 Nothing
		"""
		
		self.__x = float( aNewXValue )

	myX = property( __getX, __setX )


	def __getZ( self ):
		""" Simple get accessor for Vector::__z
		
		Args:
		 None
		
		Returns:
		 (float) The z value of the position
		"""
		
		return self.__z


	def __setZ( self, aNewZValue ):
		""" Simple set function for Vector::__z
		
		Args:
		 aNewZValue - (float) New value of the Z position
		
		Returns:
		 Nothing
		"""
		
		self.__z = float( aNewZValue )

	myZ = property( __getZ, __setZ )


	def __str__( self ):
		""" Returns string representation of vector

		Args:
		 None
		"""
		try:
			return "%2.2f,%2.2f" % ( self.__x, self.__z )
			
		except Exception, e:
			return "Failed to fetch Vector data: %s" % e


	def __add__( self, v ):
		""" Overloaded + operator.
		
		Args:
		 v - (Vector) The vector to add to this vector
		 
		Returns:
		 The new vector
		"""
		
		return Vector( self.__x + v.myX, self.__z + v.myZ )
		

	def __sub__( self, v ):
		""" Overloaded - operator.
		
		Args:
		 v - (Vector) The vector to subtract from this vector
		 
		Returns:
		 The new vector
		"""
		
		return Vector( self.__x - v.myX, self.__z - v.myZ )
	

	def __mul__( self, f ):
		""" Overloaded * operator.
		
		Args:
		 f - (float) The float to multiply this vector with
		 
		Returns:
		 The new vector
		"""
		
		return Vector( self.__x * f, self.__z * f )
	
	
	def Length( self ):
		""" Get the length of this vector.
		
		Args:
		 None
		 
		Returns:
		 The length of this vector
		"""
		
		return math.sqrt( self.__x * self.__x + self.__z * self.__z )
	
	def Normalize( self ):
		""" Normalizes the vector (length=1).
		
		Args:
		 None
		 
		Returns:
		 self
		"""
		
		l = self.Length()
		
		if l != 0:
			self.__x /= l
			self.__z /= l
		
		return self
			
		
