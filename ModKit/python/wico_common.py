import debug
import base
import sys


# colors as ints
BLACK = 0x000000
WHITE = 0xffffff


def GetCopy( aObject ):
	
	return aObject.__copy__()


class GenericValue( object ):
	
	
	def __init__( self, aValue = False ):
		
		self.__Value = aValue
		
	
	def __str__( self ):
		
		return '%s' % self.__Value
		
	
	def Set( self, aNewValue ):
		
		self.__Value = aNewValue

	
	def SetByAction( self, anAction ):
		
		self.__Value = anAction.Execute()
		
	
	def Get( self ):
		
		return self.__Value
	
		
	def Toggle( self ):
		
		if self.__Value:
			self.__Value = False
		else:
			self.__Value = True


	def Add( self, aValue ):
		
		self.__Value += aValue
	

	def Subtract( self, aValue ):
		
		self.__Value -= aValue


	def Test( self, aValue ):
		
		return self.__Value == aValue



def StackTrace( aMaxDepth = 32 ):
	
	debug.DebugMessage( 'TraceBack - Start' )
	
	try:
		for i in range(1, aMaxDepth):
			debug.DebugMessage( '\t%s (%d): %s' % (sys._getframe(i).f_code.co_filename, sys._getframe(i).f_lineno, sys._getframe(i).f_code.co_name) )
	except ValueError:
		pass
	
	debug.DebugMessage( 'TraceBack - End' )


def ListInList( aSmallList, aBigList ):

	for item in aSmallList:
		if not item in aBigList:
			return False
	return True


def ListDiff( anAList, aBList, aSkipBCheckFlag = False ):

	missingFromA = []
	missingFromB = []

	for entry in anAList:
		if not entry in aBList:
			missingFromA.append( entry )

	if not aSkipBCheckFlag:
		for entry in aBList:
			if not entry in anAList:
				missingFromB.append( entry )

	return missingFromA, missingFromB
