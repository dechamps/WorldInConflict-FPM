from serverimports import *


class CinematicBadTypeException( Exception ): pass


class Scene( object ):
	
	def __init__( self, aStartTime, aFadeInTime, aFadeOutTime ):
		
		self.__StartTime = aStartTime
		self.__FadeInTime = aFadeInTime
		self.__FadeOutTime = aFadeOutTime
		
		self.__StartActions = []
		self.__StartClientFunction = None
		
		
	def __getStartTime( self ):
		
		return self.__StartTime
		
	myStartTime = property( __getStartTime )
	
	
	def __getFadeInTime( self ):
		
		return self.__FadeInTime
	
	myFadeInTime = property( __getFadeInTime )

		
	def __getFadeOutTime( self ):
		
		return self.__FadeOutTime
	
	myFadeOutTime = property( __getFadeOutTime )
	
	
	def AddFade( self, aFadeInTime = DEFAULT_SCENE_FADEIN_TIME, aFadeOutTime = DEFAULT_SCENE_FADEOUT_TIME ):
		
		self.__FadeInTime = aFadeInTime
		self.__FadeOutTime = aFadeOutTime
		

	def __getStartActions( self ):
		
		return self.__StartActions


	def AddStartAction( self, anAction ):
		
		self.__StartActions.append( anAction )
	

	myStartActions = property( __getStartActions )


	def __getStartClientFunction( self ):
		
		return self.__StartClientFunction


	def __setStartClientFunction( self, aStartClientFunction ):
		
		self.__StartClientFunction = aStartClientFunction


	def AddStartClientFunction( self, aStartClientFunction ):
		
		self.__StartClientFunction = aStartClientFunction


	myStartClientFunction = property( __getStartClientFunction, __setStartClientFunction )



class Cinematic( object ):


	def __init__( self, aName, aGrabCameraTime = DEFAULT_GRABCAMERA_TIME, aStartFadeInTime = DEFAULT_START_FADEIN_TIME, \
		 aStartFadeOutTime = DEFAULT_START_FADEOUT_TIME, anEndFadeInTime = DEFAULT_END_FADEIN_TIME, anEndFadeOutTime = DEFAULT_END_FADEOUT_TIME, aCinematicLength = -1, aIsSplineCinematic = False ):
		 
		import serverimports
		
		self.__Name = aName
		self.__GrabCameraTime = aGrabCameraTime
		self.__StartFadeInTime = aStartFadeInTime
		self.__StartFadeOutTime = aStartFadeOutTime
		self.__EndFadeInTime = anEndFadeInTime
		self.__EndFadeOutTime = anEndFadeOutTime
		self.__StartBlackTime = DEFAULT_START_BLACK_TIME

		# Set default values for Moviebox.
		if wicg.IsMoviebox():
			self.__GrabCameraTime = 0.0
			self.__StartFadeInTime = 0.0
			self.__StartBlackTime = 0.0


		self.__StartActions = []
		self.__StartClientFunction = None
		self.__EndActions = []
		self.__EndClientFunction = None
		
		self.__UseStartFadeOut = True
		
		self.__CreatedUnits = []
		
		self.__StartFadeDoneActions = []
		
		self.__Scenes = []
		
		self.__UnitsDisabled = GenericValue( False )
		
		self.__UseFadeOnEscape = False
		
		self.__ShowTimer = False
		
		self.__IsStartCinematic = False
		
		self.__UseReleaseCamera = True
		
		self.__ResetSoundVolumes = True
		
		## this is a spline cinematic where the camera is loaded from file
		if aIsSplineCinematic:
			self.__IsSplineCinematic = True
			self.__IsLuddeCinematic = False
			self.__Length = aCinematicLength
		
		## this is a ludde cinematic where the camera is scripted from python
		elif aCinematicLength != -1:
			self.__IsSplineCinematic = False
			self.__IsLuddeCinematic = True
			self.__Length = aCinematicLength
		
		## this is a normal cinematic where the camera and scene are loaded from file
		else:
			self.__IsSplineCinematic = False
			self.__IsLuddeCinematic = False
			self.__Length = serverimports.GetMovieLength( 'myCinematicsFile', self.__Name, -1 )

	
	def UseFadeOnEscape( self, aUseFade ):
		
		self.__UseFadeOnEscape = aUseFade
		

	def UseStartFadeOut( self, aUseFade ):
		
		self.__UseStartFadeOut = aUseFade
		
	
	def UseReleaseCamera( self, useRelease ):
		
		self.__UseReleaseCamera = useRelease

	
	def ResetSoundVolumesAtEnd( self, aFlag ):
		
		self.__ResetSoundVolumes = aFlag
		

	def ShowTimer( self, aShowTimer ):
		
		self.__ShowTimer = aShowTimer


	def SetStartCinematic( self, aStartCinematic ):
		
		self.__IsStartCinematic = aStartCinematic


	def SetStartFadeOutTime( self, aStartFadeOutTime ):
		
		self.__StartFadeOutTime = aStartFadeOutTime


	def SetStartFadeInTime( self, aStartFadeInTime ):
		
		self.__StartFadeInTime = aStartFadeInTime


	def SetEndFadeOutTime( self, aEndFadeOutTime ):
		
		self.__EndFadeOutTime = aEndFadeOutTime


	def SetEndFadeInTime( self, aEndFadeInTime ):
		
		self.__EndFadeInTime = aEndFadeInTime


	def AddStartAction( self, anAction ):
		
		self.__StartActions.append( anAction )


	def AddEndAction( self, anAction ):
		
		self.__EndActions.append( anAction )


	def AddStartFadeDoneAction( self, anAction ):
		
		self.__StartFadeDoneActions.append( anAction )


	def AddStartClientFunction( self, aStartClientFunction ):
		
		self.__StartClientFunction = aStartClientFunction


	def AddEndClientFunction( self, aEndClientFunction ):
		
		self.__EndClientFunction = aEndClientFunction
		
	
	def AddScene( self, aScene ):
		
		self.__Scenes.append( aScene )

	
	def AutoInitScenes( self ):
		import serverimports
		
		for i in range( serverimports.GetNrOfScenesInMovie( 'myCinematicsFile', self.__Name ) ):
			self.AddSceneFromJuice( i )


	def AddFadeToAllScenes( self ):
		
		for scene in self.__Scenes:
			scene.AddFade()


	def GetNumberOfScenes( self ):
		
		return len( self.__Scenes )

	
	def GetSceneByIndex( self, aIndex ):
		
		return self.__Scenes[aIndex]

	
	def AddSceneFromJuice( self, aSceneIndex, aFadeInTime = 0.0, aFadeOutTime = 0.0 ):
		import serverimports
		
		if self.__IsLuddeCinematic:
			raise CinematicBadTypeException( 'Cant add scene from juice to a LuddeCinematic!' )
		elif self.__IsSplineCinematic:
		 	raise CinematicBadTypeException( 'Cant add scene from juice to a SplineCinematic!' )
		
		sceneStartTime = 0.0
				
		## if it isnt the first scene we have to fetch the scene start time from the juice
		if aSceneIndex > 0:
			for i in range( aSceneIndex ):
				sceneStartTime += serverimports.GetMovieLength( 'myCinematicsFile', self.__Name, i )
		
		s = Scene( sceneStartTime, aFadeInTime, aFadeOutTime )
		self.__Scenes.append( s )
		return s


	def AddSceneFromTime( self, aSceneStartTime, aFadeInTime = 0.0, aFadeOutTime = 0.0 ):
		
		s = Scene( aSceneStartTime, aFadeInTime, aFadeOutTime )
		self.__Scenes.append( s )
		return s


	def SetupScene( self, aScene, aTimeToStart ):
		import serverimports
		
		shouldFade = (aScene.myFadeInTime > 0.0 or aScene.myFadeOutTime > 0.0)
		
		## add fades
		if shouldFade:
			actStartFadeIn = serverimports.Action( serverimports.ClientCommand, 'FadeIn', serverimports.BLACK, aScene.myFadeInTime, 1 )
			serverimports.Delay( aTimeToStart + aScene.myStartTime - aScene.myFadeInTime, actStartFadeIn )
		
			actStartFadeOut = serverimports.Action( serverimports.ClientCommand, 'FadeOut', aScene.myFadeOutTime, 1 )
			serverimports.Delay( aTimeToStart + aScene.myStartTime, actStartFadeOut )
		
		## add callbacks
		if len( aScene.myStartActions ):
			serverimports.Delay( aTimeToStart + aScene.myStartTime, aScene.myStartActions )
		
		## add client function
		if aScene.myStartClientFunction:
			actStart = serverimports.Action( serverimports.ClientCommand, aScene.myStartClientFunction )
			serverimports.Delay( aTimeToStart + aScene.myStartTime, actStart )

		
		return aScene.myStartTime

	
	def StartUnitListner( self ):
		import serverimports
		
		self.__CreatedUnits = []
		self.__CreateUnitReaction = serverimports.RE_OnCustomEvent( 'UnitCreated', serverimports.Action( self.AddUnitFromPostEvent ) )
			
	
	def AddUnitFromPostEvent( self ):
		import serverimports
		
		self.__CreatedUnits.append( serverimports.theReactions.myEventData[0] )
		
	
	def DestoyAllAliveUnits( self ):
		import serverimports
		
		serverimports.RemoveReaction( self.__CreateUnitReaction )
		self.__CreateUnitReaction = None
			
		for unitId in self.__CreatedUnits:
			
			try:
				serverimports.theUnits[unitId].myHealth
			except serverimports.UnknownUnitException:
				continue
			else:
				if serverimports.theUnits[unitId].myOwner != serverimports.PLAYER_SCRIPT:
					serverimports.RemovePlayerUnit( unitId, 0 )
				else:
					serverimports.RemoveUnit( unitId, 0 )
		
		self.__CreatedUnits = []
	
	
	def Play( self ):
		import serverimports
		
		## cancel all air drops
		serverimports.CancelAllActiveAirDrops()
		
		## this is a safety mutex so we dont enables units when they arent disabled
		#self.__UnitsDisabled.Set( False )
				
		## switch to the alternative system, all groups and reactions will be paused
		serverimports.UseAlternativeReactionSystem( )
		
		## disable all units as soon as the switch is done
		#actOnSwitched = 	[serverimports.Action( serverimports.DisableAllUnits, True ),\
		#			serverimports.Action( self.__UnitsDisabled.Set, True ),\
		#			serverimports.Action( self.Setup )]
		
		serverimports.RE_OnSystemSwitched( serverimports.Action( self.Setup ) )


	def Setup( self ):
		import serverimports as si
		
		self.__UnitsDisabled.Set( False )
		
		shouldDoStartFade = self.__StartFadeInTime > 0.0 or self.__StartFadeOutTime > 0.0
		
		timeToStart = self.__GrabCameraTime + self.__StartFadeInTime + self.__StartBlackTime
		
		si.RE_OnCustomEvent( 'SKIP_CUTSCENE', si.Action( self.Shutdown ) )
		si.Delay( timeToStart + self.__Length, si.Action( self.Shutdown ) )

		## if its a splinecinematic we call GrabCamera with the update flag set to False
		if self.__IsSplineCinematic:
			si.ClientCommand( 'GrabCamera', True, DEFAULT_ASPECT_RATIO, 0, 0, False )
		elif self.__IsLuddeCinematic:
			si.ClientCommand( 'GrabCamera', True, DEFAULT_ASPECT_RATIO )
		else:
			si.ClientCommand( 'GrabCamera', True, DEFAULT_ASPECT_RATIO )
			
			si.Delay( self.__GrabCameraTime, si.Action( si.ClientCommand, 'SetSoundVolumes', 0, -1, 0, 0, self.__StartFadeInTime ) )			
			si.Delay( self.__GrabCameraTime, si.Action( si.ClientCommand, 'PreStartMovieMusic', 'myCinematicsFile', self.__Name, self.__StartFadeInTime ) )
		
		if not self.__IsStartCinematic and shouldDoStartFade:
			si.Delay( self.__GrabCameraTime, si.Action( si.ClientCommand, 'FadeIn', si.BLACK, self.__StartFadeInTime, 1 ) )	
		
		## disable all units
		si.Delay( self.__GrabCameraTime + ( self.__StartFadeInTime * DEFAULT_HIDE_UNITS_TIME ), [si.Action( self.StartUnitListner ), si.Action( si.DisableAllUnits, True ), si.Action( self.__UnitsDisabled.Set, True )] )
		
		
		## if its a start cinematic use the special theGame.FadeIn
		if self.__IsStartCinematic:
			actStartFadeOut = si.Action( si.theGame.FadeIn, self.__StartFadeOutTime )
		else:
			#if self.__UseStartFadeOut:
			actStartFadeOut = si.Action( si.ClientCommand, 'FadeOut', self.__StartFadeOutTime, 1 )

		## setup the start actions
		actStart = []
		
		## start cinematic (1)
		actStartCinematic = si.Action( self.Start )
		actStart.append( actStartCinematic )
		
		## do the start fade out (this fades into the game) (2)
		if ( self.__IsStartCinematic or shouldDoStartFade ) and self.__UseStartFadeOut:
			actStart.append( actStartFadeOut )
			
			if not self.__IsSplineCinematic and not self.__IsLuddeCinematic:
				## theGame.FadeIn will reset the sound volumes, so we undo the reset with this action
				actStart.append( si.Action( si.ClientCommand, 'SetSoundVolumes', 0, -1, -1, 0 ) )
			
		si.Delay( timeToStart, actStart )
		
		if len( self.__StartFadeDoneActions ):
			si.Delay( timeToStart + self.__StartFadeOutTime, self.__StartFadeDoneActions )
		
		prevSceneTime = 0.0
		
		## loop through all scenes and initialize them
		for scene in self.__Scenes:
			self.SetupScene( scene, timeToStart )
			
			if USE_CINEMATIC_TIMER or self.__ShowTimer:
				si.Delay( timeToStart + prevSceneTime, si.Action( si.DebugTimer, scene.myStartTime - prevSceneTime, None, True, si.FONT_BIG, 0.046, 0.082, 0xff0000 ) )
				prevSceneTime = scene.myStartTime
		
		if (USE_CINEMATIC_TIMER or self.__ShowTimer) and len( self.__Scenes ):
			si.Delay( timeToStart + prevSceneTime, si.Action( si.DebugTimer, self.__Length - prevSceneTime, None, True, si.FONT_BIG, 0.046, 0.082, 0xff0000 ) )
			

	def Start( self ):
		import serverimports
		
		## if fadein or fadeout is greater than zero we should use an endfade
		shouldDoEndFade = self.__EndFadeInTime > 0.0 or self.__EndFadeOutTime > 0.0
		
		
		## if splinecinematic load camera from file
		if self.__IsSplineCinematic:
			serverimports.ClientCommand( 'LoadCinematicCamera', self.__Name )
			serverimports.ClientCommand( 'StartCinematicCamera' )
			
		## if luddecinematic dont do anything, camera is controlled from python
		elif self.__IsLuddeCinematic:
			pass
			
		## if normal cinematic load cinematic movie and setup correct soundvolumes
		else:
			serverimports.ClientCommand( 'SetSoundVolumes', 0, -1, 0, 0 )
			serverimports.ClientCommand( 'LoadMMovie', 'myCinematicsFile', self.__Name )
			serverimports.ClientCommand( 'ResetSoundVolumesIndividual', 0, 0, 1, 0, self.__StartFadeOutTime )
		
		## setup endfade
		if shouldDoEndFade:
			actEndFadeIn = serverimports.Action( serverimports.ClientCommand, 'FadeIn', serverimports.BLACK, self.__EndFadeInTime - DEFAULT_END_BLACK_TIME, 1 )
			serverimports.Delay( self.__Length - self.__EndFadeInTime, actEndFadeIn )
		
		## switch to alternative system on the client
		serverimports.ClientCommand( 'SwitchToAlternativeSystem' )
		
		## execute all start actions
		if len( self.__StartActions ):
			for act in self.__StartActions:
				act.Execute()
		
		## execute client startfunction
		if self.__StartClientFunction:
			serverimports.ClientCommand( self.__StartClientFunction )
		
		serverimports.PostEvent( '%sStart' % self.__Name )
		
		if USE_CINEMATIC_TIMER or self.__ShowTimer:
			serverimports.DebugTimer( self.__Length, None, True, serverimports.FONT_BIG )

	
	def Shutdown( self ):
		import serverimports
		
		## if fadein or fadeout is greater than zero we should use an endfade
		shouldDoEndFade = self.__EndFadeInTime > 0.0 or self.__EndFadeOutTime > 0.0
		
		## destroy all cinematic units/groups
		serverimports.DestroyAllGroups( )
		
		## if we have disabled all units we enable them
		if self.__UnitsDisabled.Get():
			## destroy all other units, so called BAD UNITS!
			self.DestoyAllAliveUnits()
			serverimports.DisableAllUnits( False )
			self.__UnitsDisabled.Set( False )
		
		serverimports.SetSlowMo( 1.0 )
		
		## if luddecinematic just reset the camera type
		if self.__IsLuddeCinematic:
			serverimports.ClientCommand( 'SetDefaultCameraType' )
			
		## if splinecinematic stop the camera
		elif self.__IsSplineCinematic:
			serverimports.ClientCommand( 'StopCinematicCamera' )
			
		## if normal cinematic unload the cinematic and reset the soundvolumes
		else:
			serverimports.ClientCommand( 'UnloadMMovie' )
			
			if self.__ResetSoundVolumes:
				serverimports.ClientCommand( 'ResetSoundVolumes', 4 )
			
			##serverimports.ClientCommand( 'SetSoundVolumes', -1, -1, -1, -1 )
			
		serverimports.ClientCommand( 'OverrideGlobalLodFudge', -1 )
		
		if wicg.IsMoviebox():
			serverimports.ClientCommand( 'ReleaseCamera', 0 )
			serverimports.ClientCommand( 'FadeOut', 0.0, 1 )
		else:
			if self.__UseFadeOnEscape and shouldDoEndFade:
				serverimports.ClientCommand( 'FadeIn', serverimports.BLACK, self.__EndFadeInTime, 1 )
			else:
				if self.__UseReleaseCamera:
					serverimports.ClientCommand( 'ReleaseCamera', 1 )
				if shouldDoEndFade:
					serverimports.ClientCommand( 'FadeOut', self.__EndFadeOutTime, 1 )
		
		serverimports.ClientCommand( 'SwitchToPrimarySystem' )

		serverimports.RE_OnSystemSwitched( serverimports.Action( self.End ) )
		serverimports.UsePrimaryReactionSystem( )


	def End( self ):
		import serverimports
		
		shouldDoEndFade = self.__EndFadeInTime > 0.0 or self.__EndFadeOutTime > 0.0		
		
		## for safety reasons
		if self.__IsStartCinematic:
			serverimports.theGame.FadeIn( 0.0 )
		
		if self.__UseFadeOnEscape and shouldDoEndFade:
			actEndFade = [serverimports.Action( serverimports.ClientCommand, 'ReleaseCamera', 1 ), serverimports.Action( serverimports.ClientCommand, 'FadeOut', self.__EndFadeOutTime, 1 )]
			serverimports.Delay( self.__EndFadeInTime + DEFAULT_END_BLACK_TIME, actEndFade )

		serverimports.PostEvent( '%sEnd' % self.__Name )

		if len( self.__EndActions ):
			for act in self.__EndActions:
				act.Execute()
		if self.__EndClientFunction:
			serverimports.ClientCommand( self.__EndClientFunction )
		


class LuddeCinematic( Cinematic ):


	def __init__( self, aName, aLength, aGrabCameraTime = DEFAULT_GRABCAMERA_TIME, aStartFadeInTime = DEFAULT_START_FADEIN_TIME, \
		 aStartFadeOutTime = DEFAULT_START_FADEOUT_TIME, anEndFadeInTime = DEFAULT_END_FADEIN_TIME, anEndFadeOutTime = DEFAULT_END_FADEOUT_TIME ):
		
		import serverimports
		
		Cinematic.__init__( self, aName, aGrabCameraTime, aStartFadeInTime, aStartFadeOutTime, anEndFadeInTime, anEndFadeOutTime, aLength )



class SplineCinematic( Cinematic ):


	def __init__( self, aName, aLength, aGrabCameraTime = DEFAULT_GRABCAMERA_TIME, aStartFadeInTime = DEFAULT_START_FADEIN_TIME, \
		 aStartFadeOutTime = DEFAULT_START_FADEOUT_TIME, anEndFadeInTime = DEFAULT_END_FADEIN_TIME, anEndFadeOutTime = DEFAULT_END_FADEOUT_TIME ):
		
		import serverimports
		
		Cinematic.__init__( self, aName, aGrabCameraTime, aStartFadeInTime, aStartFadeOutTime, anEndFadeInTime, anEndFadeOutTime, aLength, True )
