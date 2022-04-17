"""
		mapvars.disBannon = Disobey( )
		mapvars.disBannon.AddSomeAreas( Area( 'CP_TrainStation', 200 ) )
		mapvars.disBannon.AddSomeGroups( [ mapvars.grpPlayer9RuAI1, mapvars.grpPlayer10RuAI1 ] )
		mapvars.disBannon.AddFirstMess(  [ 'r2_60', 160, 'r2_59', 159 ] )
		mapvars.disBannon.AddSecondMess( [ 'r2_61', 161 ] )
		mapvars.disBannon.AddThirdMess(  [ 'DestroyAA03', 162 ] )		
		
		mapvars.disBannon = Disobey( [ mapvars.grpPlayer9RuAI1, mapvars.grpPlayer10RuAI1 ], Area( 'CP_TrainStation', 200 ), [ 'r2_60', 160, 'r2_59', 159, 'r2_61', 161, 'DestroyAA03', 162 ] )
		mapvars.disBannon.Activate( True )	
		
		mapvars.disBannon = Disobey( [ mapvars.grpPlayer9RuAI1, mapvars.grpPlayer10RuAI1 ], Area( 'CP_TrainStation', 200 ) )
		RE_OnCustomEvent( 'DisobeyWarning_1', Action( ShowMessageBoxQueue, dsafsda, 111 ) )
		RE_OnCustomEvent( 'DisobeyWarning_3', Action( GameOver, mapvars.objTest ) )

		mapvars.disBannon = Disobey( )
		mapvars.disBannon.AddSomeAreas( Area( 'gauntlet1_CP', 200 ) )
		mapvars.disBannon.AddSomeGroups( [ mapvars.grpGauntlet ] )
		mapvars.disBannon.Activate( True )	
		
		RE_OnCustomEvent( 'DisobeyWarning_1', Action( SetCommandPointActive, 'gauntlet2_CP', False ) )
		RE_OnCustomEvent( 'DisobeyWarning_3', Action( GameOver, False ) )
	
"""

class Disobey( object ):
	
	def __init__( self, someGroups = None, someAreas = None, someMessageBoxs = None ):
		import serverimports
		
		self.__Groups = [] 
		self.__Areas = []
		self.__MessageBoxs = []
		self.__ReactivateTime = 30		
		self.__FirstDisMessAi = None
		self.__FirstDisMessAiId = None
		self.__FirstDisMessCommander = None
		self.__FirstDisMessCommanderId = None
		self.__SecondDisMessAi = None
		self.__SecondDisMessAiId = None
		self.__ThirdDisMessAi = None
		self.__ThirdDisMessAiId = None
		self.__Activated = False
		self.__gvDisobeyCounter = serverimports.GenericValue( 0 )
		self.__reactDisobey = None
		self.__Name = None
		
		if someGroups != None:
			self.AddSomeGroups( someGroups )

		if someAreas != None:
			self.AddSomeAreas( someAreas )

		if someMessageBoxs != None:
			self.AddSomeMessageBoxs( someMessageBoxs )

	
	def AddSomeGroups( self, someGroups ):	
		if not isinstance( someGroups, list ):
			self.__Groups = [ someGroups ]
		else:
			self.__Groups = someGroups
		
		self.Update( )

	def AddNewGroups( self, someGroups ):
		if not isinstance( someGroups, list ):
			self.__Groups.append( someGroups )
		else:
			self.__Groups.extend( someGroups )
			
		self.Update( )
			
	def RemoveGroups( self, someGroups ):
		if not isinstance( someGroups, list ):
			self.__Groups.remove( someGroups )
		else:
			for grp in someGroups:
				self.__Groups.remove( grp )
				
		self.Update( )

	def AddSomeAreas( self, someAreas ):
		if not isinstance( someAreas, list ):
			someAreas = [ someAreas ]
		
		for area in someAreas:
			self.__Areas.append( self.MakeArea( area ) )
		
		self.Update( )
	
	def AddNewAreas( self, someAreas ):
		if not isinstance( someAreas, list ):
			someAreas = [ someAreas ]

		for area in someAreas:
			self.__Areas.append( Self.MakeArea( area ) )
				
		self.Update( )	
			
	def RemoveAreas( self, someAreas ):
		if not isinstance( someAreas, list ):
			self.__Areas.remove( someAreas )
		else:
			for area in someAreas:
				self.__Areas.remove( area )	
		
		self.Update( )

	def MakeArea( self, aArea ):
		import serverimports
		if isinstance( aArea, serverimports.Area ):
			return aArea
		else:
			return serverimports.Area( aArea )

	def SetName( self, aName ):
		self.__Name = aName
		
	
	def Update( self ):
		import serverimports
		
		if self.__reactDisobey == None:
			return			
		
		serverimports.RemoveReaction( self.__reactDisobey )
		self.__reactDisobey = serverimports.RE_OnPlayerInAreasKillsUnitsInGroups( serverimports.PLAYER_HUMAN, self.__Areas, self.__Groups, serverimports.Action( self.Execute ) )
		
		if not self.__Activated:
			serverimports.RemoveReaction( self.__reactDisobey )
		
	
	def AddSomeMessageBoxs( self, someMessageBoxs ):
		
		if len( someMessageBoxs ) >= 4:		
			self.AddFirstMess( someMessageBoxs[:4] )
		if len( someMessageBoxs ) >= 6:		
			self.AddSecondMess( someMessageBoxs[4:6] )
		if len( someMessageBoxs ) >= 8:		
			self.AddThirdMess( someMessageBoxs[6:] )


	def AddFirstMess( self, someMessageBoxs ):
		
		self.__FirstDisMessAi = someMessageBoxs[ 0 ]
		self.__FirstDisMessAiId = someMessageBoxs[ 1 ]
		self.__FirstDisMessCommander = someMessageBoxs[ 2 ]
		self.__FirstDisMessCommanderId = someMessageBoxs[ 3 ]


	def AddSecondMess( self, someMessageBoxs ):
		
		self.__SecondDisMessAi = someMessageBoxs[ 0 ]
		self.__SecondDisMessAiId = someMessageBoxs[ 1 ]


	def AddThirdMess( self, someMessageBoxs ):
		
		self.__ThirdDisMessAi = someMessageBoxs[ 0 ]
		self.__ThirdDisMessAiId = someMessageBoxs[ 1 ]
		
	
	def ResetCounter( self ):
		self.__gvDisobeyCounter.Set( 0 )
	
	
	def Activate( self, aFlag ):
		import serverimports
		serverimports.DebugMessage( 'Disobey:Activate::' )		
		self.__Activated = aFlag
			
		if self.__Activated:
			if self.__reactDisobey == None:
				self.__reactDisobey = serverimports.RE_OnPlayerInAreasKillsUnitsInGroups( serverimports.PLAYER_HUMAN, self.__Areas, self.__Groups, serverimports.Action( self.Execute ) )
			else:
				serverimports.RegisterReaction( self.__reactDisobey )
		else:
			serverimports.RemoveReaction( self.__reactDisobey )
	
	
	def Execute( self ):
		import serverimports
		
		serverimports.DebugMessage( 'Disobey:Execute::' )
		
		if not self.__Activated:
			return
			
		queDisobey = serverimports.ActionQueue( 'queDisobey', False )
		
		if self.__gvDisobeyCounter.Test( 0 ):
			self.__gvDisobeyCounter.Add( 1 )
			
			if self.__Name == None:
				queDisobey.AddFunction( serverimports.PostEvent, 'DisobeyWarning_1' )
			else:
				postString = 'DisobeyWarning'+ self.__Name +'_1'
				queDisobey.AddFunction( serverimports.PostEvent, postString )
			
			if self.__FirstDisMessAi != None:
				queDisobey.AddMessageBox( self.__FirstDisMessAi, self.__FirstDisMessAiId )
				queDisobey.AddMessageBox( self.__FirstDisMessCommander, self.__FirstDisMessCommanderId )
			queDisobey.AddFunction( self.DelayReActivate )			

		elif self.__gvDisobeyCounter.Test( 1 ):
			self.__gvDisobeyCounter.Add( 1 )

			if self.__Name == None:
				queDisobey.AddFunction( serverimports.PostEvent, 'DisobeyWarning_2' )
			else:
				postString = 'DisobeyWarning'+ self.__Name +'_2'
				queDisobey.AddFunction( serverimports.PostEvent, postString )

			if self.__SecondDisMessAi != None:
				queDisobey.AddMessageBox( self.__SecondDisMessAi, self.__SecondDisMessAiId )
			queDisobey.AddFunction( self.DelayReActivate )			

		elif self.__gvDisobeyCounter.Test( 2 ):

			if self.__Name == None:
				queDisobey.AddFunction( serverimports.PostEvent, 'DisobeyWarning_3' )
			else:
				postString = 'DisobeyWarning'+ self.__Name +'_3'
				queDisobey.AddFunction( serverimports.PostEvent, postString )

			if self.__ThirdDisMessAi != None:
				queDisobey.AddMessageBox( self.__ThirdDisMessAi, self.__ThirdDisMessAiId )
				queDisobey.AddFunction( serverimports.GameOver, False )
		
		queDisobey.Execute( )

		
	def DelayReActivate( self ):
		import serverimports
		serverimports.Delay( self.__ReactivateTime, serverimports.Action( self.ReActivate ) )

	
	def ReActivate( self ):
		import serverimports
		serverimports.RegisterReaction( self.__reactDisobey )
		
