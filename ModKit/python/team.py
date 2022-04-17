import wicg
from player import PlayerException


class Team( object ):
	""" Abstraction of a game team. Team ID is be either:
	- 1 for USA
	- 2 for NATO or
	- 3 for Soviet
	- 0 is used for neutral units.	
	"""
	__teamID = -1
	__teamName = None
	
	
	def __init__( self, aTeamID ):
		"""
		"""
		self.__teamID = aTeamID
		if self.__teamID == 1:
			self.__teamName = "usa"
		elif self.__teamID == 2:
			self.__teamName = "nato"
		elif self.__teamID == 3:
			self.__teamName = "soviet"


	def ShowTimedMessageBox( self, aTextIndex, aCharacterIndex, aSoundfileIndex, aTimeToShow, aMessageBoxID ):
		""" Shows a messagebox ingame. The aTextIndex referes to the member in myLocStrings list in in <mapname>.juice
			with the instance-name aTextIndex. Same goes for aSoundfileIndex (in myLocFiles).
	
		aTextIndex	  - (string) instance name of localized string in myLocStrings
		aSoundfileIndex - (string) instance name of in myLocFiles pointing to the soundfile to play
		aCharacterIndex - (string) name of the character to play (defined in characters.juice)
		aTimeToShow	 - (float) Time to show the message box
		aMessageBoxID   - (int) identifier of a message box (so you can get a callback when the player have closed it)
		"""
		ret = 0
		try:
			ret += wicg.ShowMessageBox( self.__teamName, "timed", aTextIndex, aCharacterIndex, aSoundfileIndex, aMessageBoxID, aTimeToShow )
		except PlayerException, e:
			DebugMessage( "\n<exception method='Team::ShowTimedMessageBox()' player='%d'>\n%s\n</exception>" % ( player.myID, e ) )

		return ret


	def ShowButtonMessageBox( self, aTextIndex, aCharacterIndex, aSoundfileIndex, aMessageBoxID ):
		""" Shows a messagebox ingame. The aTextIndex referes to the member in myLocStrings list in in <mapname>.juice
			with the instance-name aTextIndex. Same goes for aSoundfileIndex (in myLocFiles).
	
		aTextIndex	  - (string) instance name of localized string in myLocStrings
		aSoundfileIndex - (string) instance name of in myLocFiles pointing to the soundfile to play
		aCharacterIndex - (string) name of the character to play (defined in characters.juice)
		aMessageBoxID   - (int) identifier of a message box (so you can get a callback when the player have closed it)
		"""
		try:
			ret = wicg.ShowMessageBox( self.__teamName, "button", aTextIndex, aCharacterIndex, aSoundfileIndex, aMessageBoxID )
		except PlayerException, e:
			DebugMessage( "\n<exception method='Team::ShowButtonMessageBox()'>\n%s\n</exception>" % e )

		return ret


	def ShowAutomaticMessageBox( self, aTextIndex, aCharacterIndex, aSoundfileIndex, aMessageBoxID ):
		""" Shows a messagebox ingame. The aTextIndex referes to the member in myLocStrings list in in <mapname>.juice
			with the instance-name aTextIndex. Same goes for aSoundfileIndex (in myLocFiles).
	
		aTextIndex	  - (string) instance name of localized string in myLocStrings
		aSoundfileIndex - (string) instance name of in myLocFiles pointing to the soundfile to play
		aCharacterIndex - (string) name of the character to play (defined in characters.juice)
		aMessageBoxID   - (int) identifier of a message box (so you can get a callback when the player have closed it)
		"""
		try:
			ret = wicg.ShowMessageBox( self.__teamName, "automatic", aTextIndex, aCharacterIndex, aSoundfileIndex, aMessageBoxID )
		except PlayerException, e:
			DebugMessage( "\n<exception method='Team::ShowAutomaticMessageBox()'>\n%s\n</exception>" % e )

		return ret

	
	def PurgeMessageBoxQueue( self ):
		""" Removes the current Message Box being showed, as well as clears all pending messageboxes so they will not be showed.
		"""
		try:
			ret = wicg.PurgeMessageBoxQueue( self.__teamName )
		except PlayerException, e:
			DebugMessage( "\n<exception method='Team::PurgeMessageBoxQueue()'>\n%s\n</exception>" % e )

		return ret


teamAll = Team( 0 )
teamUSA = Team( 1 )
teamNato = Team( 2 )
teamSoviet = Team( 3 )
