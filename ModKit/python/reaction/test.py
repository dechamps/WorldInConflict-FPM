import debug
import action
import position

class BaseTest( object ):

	def __call__( self, someEventData ):
		
		return self.Test( someEventData )


	def __str__( self ):
		
		return self.__class__.__name__


	def Test( self, someEventData ):
		""" Overload this to create a new test.
		"""
		
		return True


class SimpleTest( BaseTest ):
	
	def __init__( self, aValue, anIndex = 0 ):
		
		self.__Value = aValue
		self.__Index = anIndex


	def Test( self, someEventData ):
		
		return ( someEventData[self.__Index] == self.__Value )


class ComplexTest( BaseTest ):
	
	def __init__( self, *someValues ):
		
		self.__Values = someValues


	def Test( self, someEventData ):
		
		counter = 0
		for value in self.__Values:
			if not value == someEventData[counter]:
				return False
			counter += 1
		
		return True


class CounterTest( BaseTest ):
	
	def __init__( self, aCounter ):
		
		self.__Counter = aCounter


	def Test( self, someEventData ):
		
		self.__Counter -= 1		
		return (self.__Counter < 1)


class TimeTest( BaseTest ):
	
	def __init__( self, aTime ):
		
		self.__Time = aTime
		self.__CurrentTime = aTime
		
	
	def __getCurrentTime( self ):
		
		return self.__CurrentTime
	
	
	myCurrentTime = property(__getCurrentTime)


	def Test( self, someEventData ):
		
		self.__CurrentTime -= someEventData[0]
		
		if ( 0 >= self.__CurrentTime ):
			self.__CurrentTime = self.__Time
			return True
		return False


class PositionTest( BaseTest ):
		
	def __init__( self, aPosition, aDistanceLimit = 1.0 ):
		
		self.__Position = aPosition
		self.__DistanceLimit = aDistanceLimit


	def Test( self, someEventData ):
		import wicmath.wicmath as wicmath
		if wicmath.Distance3D( self.__Position, position.Position( someEventData[0], someEventData[1], someEventData[2] ) ) <= self.__DistanceLimit:
			return True
		return False


class CustomTest( BaseTest ):
	
	def __init__( self, aFunction, *someArguments ):
		
		self.__Action = action.Action( aFunction, *someArguments )
		
	
	def Test( self, someEventData ):
		
		return self.__Action.Execute()
