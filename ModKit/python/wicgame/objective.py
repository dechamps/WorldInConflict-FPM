import debug
import wicg_common as common

MARKER_HEIGHT_MODIFIER = 3.0

class Objective( object ):

	
	def __init__( self, aName, aTarget = -1, aType = 'primary', aCount = -1 ):
		
		self.__Name = aName
		self.__NewName = None
		
		self.__Type = aType
		self.__State = 'created'
		self.__CurrentCount = 0
		
		self.__PostCompleted = '%sCompleted' % aName
		self.__PostFailed = '%sFailed' % aName
		
		self.__SkipTotalCount = False
		
		self.__SubMarkers = {}
		self.__SubMarkerInfo = []
		
		if aCount == -1:
			self.__TotalCount = 0
			self.__HasCounter = False
		else:
			self.__TotalCount = aCount
			self.__HasCounter = True

		if isinstance( aTarget, int ):
			self.__Target = aTarget
		elif aTarget == None:
			self.__Target = common.Position( -1, -1, -1 )
		else:
			self.__Target = common.GetCopy( common.GetPosition( aTarget ) )
			
			# move the marker up 3 meters
			if self.__Target.myX != -1 and self.__Target.myY != -1 and self.__Target.myZ != -1:
				self.__Target.myY += MARKER_HEIGHT_MODIFIER


	def GetPostEvent( self ):
		return self.__PostCompleted


	def GetState( self ):
		return self.__State

	def GetName( self ):
		return self.__Name

	def GetCount( self ):
		return self.__CurrentCount


	def AddObjective( self ):
		import serverimports
		self.__State = 'active'
		serverimports.AddObjective( self.__Name, self.__Target, self.__Type, self.__TotalCount )
		for marker in self.__SubMarkerInfo:
			self.AddSubMarker( marker.SubName, marker.Target, marker.AutoCounter, marker.Unit, marker.PlayerId )
		
		self.__SubMarkerInfo = []		


	def RemoveObjective( self ):
		import serverimports
		self.__State = 'removed'
		serverimports.SetObjective( self.__Name, 'removed', self.__Type )

	
	def IsCompleted( self ):		
		return (self.__State == 'completed')


	def IsFailed( self ):
		return (self.__State == 'failed')


	def IsActive( self ):
		return (self.__State == 'active')

	
	def SkipTotalCount( self, aSkipFlag ):
		self.__SkipTotalCount = aSkipFlag


	def Completed( self ):
		import serverimports
		if self.__State == 'active':
			self.__State = 'completed'
			serverimports.SetObjective( self.__Name, 'completed', self.__Type )


	def Failed( self ):
		import serverimports
		if self.__State == 'active':
			self.__State = 'failed'
			serverimports.SetObjective( self.__Name, 'failed', self.__Type )


	def Cancel( self ):
		pass


	def Update( self, aNewObjective ):
		import serverimports
		if self.__State == 'active':
			self.__NewName = aNewObjective
			serverimports.UpdateObjective( self.__Name, self.__Target, self.__Type, self.__CurrentCount, self.__NewName )
			self.__Name = aNewObjective


	def AddToCounter( self, aNumber = 1 ):
		import serverimports
		
		if self.__State == 'active':
			self.__CurrentCount += aNumber
			if self.__CurrentCount >= 0:
				if self.__SkipTotalCount:
					serverimports.PostEvent( self.__Name+"_"+str( self.__CurrentCount ) )		
					serverimports.UpdateObjective( self.__Name, self.__Target, self.__Type, self.__CurrentCount )
				else:	
					if self.__CurrentCount != self.__TotalCount:
						serverimports.PostEvent( self.__Name+"_"+str( self.__CurrentCount ) )		
						serverimports.UpdateObjective( self.__Name, self.__Target, self.__Type, self.__CurrentCount )
					elif self.__CurrentCount == self.__TotalCount:
						serverimports.PostEvent( self.__PostCompleted )
			else:
				self.__CurrentCount = 0


	def AddSubMarker( self, aSubName, aTarget, aAutoCounter = False, aUnit = -1, aPlayerId = 1):
		import serverimports
		if self.__State == 'active':
			pos = common.GetPosition( aTarget )
			
			# move the marker up 3 meters			
			self.__SubMarkers[ aSubName ] = serverimports.AddSubObjectiveMarker( aPlayerId, self.__Name, aUnit, pos.myX, pos.myY + MARKER_HEIGHT_MODIFIER, pos.myZ )
			if self.__HasCounter and aAutoCounter:
				self.AddToCounter( -1 )
		else:
			self.__SubMarkerInfo.append( ObjSubMarkers( aSubName, aTarget, aAutoCounter, aUnit, aPlayerId ) )

		
	def RemoveSubMarker( self, aSubName, aAutoCounter = False, aPlayerId = 1, isUnitMarker = False ):
		import serverimports

		if self.__State == 'active':
			serverimports.RemoveSubObjectiveMarker( aPlayerId, self.__Name, self.__SubMarkers[ aSubName ], isUnitMarker )
			del self.__SubMarkers[ aSubName ]
			if self.__HasCounter and aAutoCounter:
				self.AddToCounter(  )

	def UpdateSubMarkerPos( self, aSubName, aTarget ):
		import serverimports
		if self.__State == 'active':
			self.RemoveSubMarker( aSubName )
			self.AddSubMarker( aSubName, aTarget )


	def GetSubMarkers( self ):
		import serverimports
		tempList = []
		if len( self.__SubMarkers ) > 0:
			for item in self.__SubMarkers:
				tempList.append( item )
			
			if len( tempList ) > 0:
				return tempList
		
		return None
	

class ObjSubMarkers( object ):

	def __init__( self, aSubName, aTarget, aAutoCounter = False, aUnit = -1, aPlayerId = 1 ):
		self.SubName = aSubName
		self.Target = aTarget
		self.AutoCounter = aAutoCounter
		self.Unit = aUnit
		self.PlayerId = aPlayerId
