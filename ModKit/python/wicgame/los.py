import serverimports as si
import wicg
import wicg_common as common
import wicmath.wicmath as wicmath


class LOS( object ):
	
	def __init__( self ):
		
		self.Id = -1
	
	
	def Remove( self ):
		
		wicg.RemoveLOSArea( self.Id )


class LOSCircle( LOS ):
	
	def __init__( self, aTarget, aRadius = -1 ):
		
		LOS.__init__( self )
		
		self.__Center = common.GetPosition( aTarget )
		
		if aRadius != -1:
			self.__Radius = aRadius
		else:
			self.__Radius = common.GetRadius( aTarget )
		
		self.Id = wicg.AddLOSCircle( self.__Center, self.__Radius )
			
	
	def Add( self ):
		
		self.Id = wicg.AddLOSCircle( self.__Center, self.__Radius )
		
	
	def Update( self, aTarget, aRadius = -1 ):
		
		self.__Center = common.GetPosition( aTarget )
		
		if aRadius != -1:
			self.__Radius = aRadius
		else:
			self.__Radius = common.GetRadius( aTarget )
		
		self.Remove()
		self.Id = wicg.AddLOSCircle( self.__Center, self.__Radius )
	
	
	def UpdateCenter( self, aTarget ):
		
		self.__Center = common.GetPosition( aTarget )		
		self.Remove()
		self.Id = wicg.AddLOSCircle( self.__Center, self.__Radius )
		
		
	def UpdateRadius( self, aRadius ):
		
		self.__Radius = common.GetRadius( aRadius )		
		self.Remove()
		self.Id = wicg.AddLOSCircle( self.__Center, self.__Radius )




class LOSRectangle( LOS ):
	
	
	def __init__( self, aTarget, aSize, anOrientation = 0.0 ):
		
		LOS.__init__( self )
		
		self.__Position = common.GetPosition( aTarget )
		self.__Size = aSize
		self.__Orientation = anOrientation
		self.Id = wicg.AddLOSRectangle( self.__Position, self.__Size, self.__Orientation )
		
	
	def Add( self ):
		
		self.Id = wicg.AddLOSRectangle( self.__Position, self.__Size, self.__Orientation )
	
		
	def Update( self, aTarget, aSize, anOrientation = 0.0 ):
		
		self.__Position = common.GetPosition( aTarget )
		self.__Size = aSize
		self.__Orientation = anOrientation
		self.Remove()
		self.Id = wicg.AddLOSRectangle( self.__Position, self.__Size, self.__Orientation )
		
	
	def Rotate( self, anAngle ):
		
		dirVec = wicmath.Heading2Vector( self.__Orientation )
		dirVec = wicmath.RotateVector( dirVec, anAngle )
		self.__Orientation = wicmath.Vector2Heading( dirVec )
		self.Remove()
		self.Id = wicg.AddLOSRectangle( self.__Position, self.__Size, self.__Orientation )

