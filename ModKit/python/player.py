import base, debug, wicg
import wic
import position


class PlayerException( Exception ): pass
class UnknownPlayerException( PlayerException ): pass
class IllegalPlayerException( PlayerException ): pass


class Player( object ):
	""" Abstraction of a player
	"""
	
	def __init__( self, anID ):
		"""
		"""
		self.__team				= -1
		self.__tacticalAid		= -1.0
		self.__maxTacticalAid	= -1.0
		self.__currentAP		= -1
		self.__maxAP			= -1
		self.__lastUpdateTime	= -1
		self.__id				= anID
		
		try:
			self.Update( True )
		except ( PlayerException, ValueError ), e:
			debug.DebugMessage( "\n%s<exception method='Player::__init__()'>\n%s\n</exception>" % (self, e ) )
			self.__id = -1
			raise e
	
	
	def __str__( self ):
		""" Returns a string description of the player
		"""
		return "\n<player>\n\tid: %s\n\tteam: %s\n\ttacticalAid: %s\n\tcurrentAP: %s\n\tmaxAP: %s\n<player>" % ( self.__id, self.__team, self.__tacticalAid, self.__currentAP, self.__maxAP )
	
	
	def Update( self, aForceUpdateFlag = False ):
		""" Refetches dynamic datat from the game
		"""
		if self.__lastUpdateTime == base.GetCurrentTime() and not aForceUpdateFlag:
			return
		
		wicg.GetPlayerData( self )
		self.__lastUpdateTime = base.GetCurrentTime()
	
	
	def __getCurrentAP( self ):
		""" Get accessor for Player.__currentAP
		"""
		self.Update()
		return self.__currentAP


	def __setCurrentAP( self, aCurrentAPValue ):
		""" Set accessor for Player.__currentAP
		"""
		try:
			wicg.SetPlayerData( self, "currentAP", int( aCurrentAPValue ) )
		except Exception, e:
			debug.DebugMessage( "\n%s<exception method='Player::__setCurrentAP()'>\n%s\n</exception>" % (self, e ) )
		else:
			self.__CurrentAP= int( aCurrentAPValue )

	
	myCurrentAP = property( __getCurrentAP, __setCurrentAP )
	
	
	def __getId( self ):
		""" Get accessor for Player.__id
		"""
		return self.__id
	
	myID = property( __getId )
	
	
	def __getMaxAP( self ):
		""" Get accessor for Player.__maxAP
		"""
		self.Update()
		return self.__maxAP


	def __setMaxAP( self, aMaxAPValue ):
		""" Set accessor for Player.__maxAP
		"""		
		try:
			wicg.SetPlayerData( self, "maxAP", int( aMaxAPValue ) )
		except Exception, e:
			debug.DebugMessage( "\n%s<exception method='Player::__setMaxAP()'>\n%s\n</exception>" % (self, e ) )
		else:
			self.__maxAP = int( aMaxAPValue )
	
	myMaxAP = property( __getMaxAP, __setMaxAP )
	

	def __getName( self ):
		return wic.game.Players[self.__id].Name


	def __setName( self, aName ):
		wic.game.Players[self.__id].Name = aName		

	
	myName = property( __getName, __setName )

	
	def __getTacticalAid( self ):
		""" Get accessor for Player.__tacticalAid
		"""
		self.Update()
		return self.__tacticalAid
	
	def __setTacticalAid( self, aTacticalAidValue ):
		""" Set accessor for Player.__tacticalAid
		"""
		debug.DebugMessage( "Changing tactical aid for player %s" % self.__id )
		
		try:
			wicg.SetPlayerData( self, "tacticalAid", float( aTacticalAidValue ) )
		except Exception, e:
			debug.DebugMessage( "\n%s<exception method='Player::__setTacticalAid()'>\n%s\n</exception>" % (self, e ) )
		else:
			self.__tacticalAid = float( aTacticalAidValue )
	
	myTacticalAid = property( __getTacticalAid, __setTacticalAid )
	
	
	def __getMaxTacticalAid( self ):
		""" Get accessor for Player.__tacticalAid
		"""
		self.Update()
		return self.__maxTacticalAid
	
	def __setMaxTacticalAid( self, aMaxTacticalAidValue ):
		""" Set accessor for Player.__maxTacticalAid
		"""
		debug.DebugMessage( "Changing max tactical aid for player %s" % self.__id )
		
		try:
			wicg.SetPlayerData( self, "maxTacticalAid", float( aMaxTacticalAidValue ) )
		except Exception, e:
			debug.DebugMessage( "\n%s<exception method='Player::__setMaxTacticalAid()'>\n%s\n</exception>" % (self, e ) )
		else:
			self.__maxTacticalAid = float( aMaxTacticalAidValue )
	
	myMaxTacticalAid = property( __getMaxTacticalAid, __setMaxTacticalAid )
	
	
	def __getTeam( self ):
		""" Get accessor for Player.__
		"""
		return self.__team
	
	myTeam = property( __getTeam )
	
	
	def CreateGenericModel( self, aModelFile, aPosition, aTimeToLive, aDirection = None, aSound = None, aSplineFile = None ):
		""" Creates a generic model and places it in the players world
		"""
		if aDirection:
			if aSound:
				if aSplineFile:
					return wicg.CreateGenericModel( self.__id, aModelFile, aPosition, float( aTimeToLive ), aDirection, aSound, aSplineFile )
				
				return wicg.CreateGenericModel( self.__id, aModelFile, aPosition, float( aTimeToLive ), aDirection, aSound )
			
			return wicg.CreateGenericModel( self.__id, aModelFile, aPosition, float( aTimeToLive ), aDirection )
		
		return wicg.CreateGenericModel( self.__id, aModelFile, aPosition, float( aTimeToLive ) )
	
	def BindGenericModelSoundToBone( self, aGenericModelId, aSoundName, aBoneName):
		return wicg.BindGenericModelSoundToBone(self.__id, aGenericModelId, aSoundName, aBoneName)
	
	def DeleteGenericModel( self, anId ):
		
		wicg.DeleteGenericModel( self.__id, anId )
	
	
	def HideWidget( self, aWidgetName ):
		""" Sets the given widgets status to hidden """
		import serverimports
		
		return serverimports.SetCoreSystemState( aWidgetName, 'hidden' )	
	
	
	def PurgeMessageBoxQueue( self ):
		""" Removes the current Message Box being showed, as well as clears all pending messageboxes so they will not be showed.
		"""
		try:
			ret = wicg.PurgeMessageBoxQueue( self.__id )
		except PlayerException, e:
			debug.DebugMessage( "\n<exception method='Player::PurgeMessageBoxQueue()'>\n%s\n</exception>" % e )
		
		return ret
	
	
	def PurgeMessageBoxQueue2( self ):
		""" Removes the current Message Box being showed, as well as clears all pending messageboxes so they will not be showed.
		"""
		try:
			ret = wicg.PurgeMessageBoxQueue2( self.__id )
		except PlayerException, e:
			debug.DebugMessage( "\n<exception method='Player::PurgeMessageBoxQueue()'>\n%s\n</exception>" % e )
		
		return ret
	
	
	def ClientPythonCommand( self, aCommandName, *someArguments ):
		wicg.ClientPythonCommand( self.__id, aCommandName, someArguments )
	
	
	def SetCameraPosition( self, aPosition, aDirection ):
		"""
		"""
		return wicg.SetCamera( self.__id, aPosition, aDirection )
	
	
	def AddObjective( self, aName, aTarget = -1, aType = 'primary', aTotalObjectiveCount = 0 ):
		haveTarget = 0
		
		if isinstance( aTarget, int ):
			if aTarget == -1:
				haveTarget = 1
			
			objectiveUnit		= aTarget
			objectivePosition	= position.Position( -1, -1, -1 )
		else:
			objectiveUnit		= -1
			objectivePosition	= aTarget
		
		wicg.SetObjective( self.__id, aName, aTotalObjectiveCount, haveTarget, objectiveUnit, objectivePosition, aType, 'new' )

	
	def SetObjective( self, aName, aState, aType = 'primary' ):
		wicg.SetObjective( self.__id, aName, 0, 0, -1, position.Position(), aType, aState )
	

	def UpdateObjective( self, aCurrentObjective, aTarget = -1, aType = 'primary', anObjectiveCounter = 0, aNewObjective = None ):
		haveTarget = 0
		
		if aNewObjective is None:
			aNewObjective = aCurrentObjective
		
		if isinstance( aTarget, int ):
			if aTarget == -1:
				haveTarget = 1
			
			objectiveUnit		= aTarget
			objectivePosition	= position.Position()
		else:
			objectiveUnit		= -1
			objectivePosition	= aTarget
		
		wicg.UpdateObjective( self.__id, aCurrentObjective, aNewObjective, anObjectiveCounter, haveTarget, objectiveUnit, objectivePosition, aType )


	def ShowMessageBox( self, aMessageboxName, aMessageBoxId, aUnitId = -1, aWorldPos = position.Position(), aBlinkFlag = 0 ):
		return wicg.ShowMessageBox( self.__id, aMessageboxName, aMessageBoxId, aUnitId, aWorldPos, aBlinkFlag )


	def HideMessageBox( self, aFadeTime = 0.0 ):
		return wicg.HideMessageBox( self.__id, aFadeTime )

	
	def ShowWidget( self, aWidgetName ):
		""" Reveals a hidden widget
		"""
		import serverimports
		
		return serverimports.SetCoreSystemState( aWidgetName, 'enabled' )	
		
	
	def AddSupportWeapon( self, aTAName ):
		from serverimports import AddSupportWeapon
		
		AddSupportWeapon( self.__id, aTAName )


	def RemoveSupportWeapon( self, aTAName ):
		from serverimports import RemoveSupportWeapon
		
		RemoveSupportWeapon( self.__id, aTAName )


	def ClearSupportWeapons( self ):
		from serverimports import ClearSupportWeapons
		
		ClearSupportWeapons( self.__id )


class Players( object ):
	""" Container class for player objects
	"""
	
	def __init__( self ):
		""" Constructor
		"""
		self.__players = {}
	
	
	def __getitem__( self, aKey ):
		""" Fetches the given player
		
		Args:
		 aKey - (int) Slot of player to select
		
		Returns:
		 The given player
		"""
		
		if not aKey in self.__players:
			debug.DebugMessage( "Fetching new player %d" % aKey )
			self.__players[aKey] = Player( aKey )
		
		self.__players[aKey].Update()
		
		return self.__players[aKey]


thePlayers = Players()