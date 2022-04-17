import wicg_common as common
import random

import serverimports as si


class CommandPointFeedbackRuFortif( object ):

	def __init__( self, aCommandPoint, aRougeMessage = False, anActiveChecker = True, aUseBannon = True, aUseWebb = True, aUseSawyer = True, anOwnMessageList = False ):
		
		
		self.__myCommandPoint = aCommandPoint
		self.__myRougeMessageChecker = aRougeMessage
		self.__myUseBannon = aUseBannon
		self.__myUseWebb = aUseWebb
		self.__myUseSawyer = aUseSawyer
		self.__myOwnMessageList = anOwnMessageList
		
		self.__Active = anActiveChecker
		self.__myMessagesToChoseFrom = []
		self.__reactCommandPointTaken = None
		
		if self.__Active:
			self.MessageSetup()

	def MessageSetup( self ):
		
		if not self.__Active:
			return

		if len( self.__myMessagesToChoseFrom ) == 0:

			if self.__myOwnMessageList:
				self.__myMessagesToChoseFrom.extend( self.__myOwnMessageList )

			if self.__myUseBannon:
				self.__myMessagesToChoseFrom.extend( [ 'cp_ru_fortif_bannon_1', 'cp_ru_fortif_bannon_2', 'cp_ru_fortif_bannon_3' ] )
			if self.__myUseWebb:
				self.__myMessagesToChoseFrom.extend( [ 'cp_ru_fortif_webb_1', 'cp_ru_fortif_webb_2', 'cp_ru_fortif_webb_3' ] )
			if self.__myUseSawyer:
				self.__myMessagesToChoseFrom.extend( [ 'cp_ru_fortif_sawyer_1', 'cp_ru_fortif_sawyer_2', 'cp_ru_fortif_sawyer_3' ] )
				
		message = random.choice( self.__myMessagesToChoseFrom )	
		self.__myMessagesToChoseFrom.remove( message )
		
		aqRuTakesCP = si.ActionQueue( 'Queue', self.__myRougeMessageChecker )
		aqRuTakesCP.AddDelay( 2 )
		aqRuTakesCP.AddMessageBox( message, si.lastShownFeedBackMessageBoxId )
		aqRuTakesCP.AddAction( si.Action( self.MessageSetup ) )

		self.__reactCommandPointTaken = si.RE_OnCommandPointTaken( self.__myCommandPoint, si.TEAM_RUSSIA, si.Action( aqRuTakesCP.Execute ) )
	
		si.lastShownFeedBackMessageBoxId += 1
		
	def Start( self ):
		
		self.__Active = True
		self.MessageSetup()
		
	def Stop( self ):

		si.RemoveReaction( self.__reactCommandPointTaken )
		self.__Active = False
		
	def ChangeCommandPoint( self, aCommandPoint ):
		
		si.RemoveReaction( self.__reactCommandPointTaken )
		self.__myCommandPoint = aCommandPoint
		self.MessageSetup( )
		
###################### 

class CommandPointFeedbackCPLost( object ):

	def __init__( self, aCommandPoint, aRougeMessage = False, anActiveChecker = True, aUseBannon = True, aUseWebb = True, aUseSawyer = True, anOwnMessageList = False ):
		
		self.__myCommandPoint = aCommandPoint
		self.__myRougeMessageChecker = aRougeMessage
		self.__myUseBannon = aUseBannon
		self.__myUseWebb = aUseWebb
		self.__myUseSawyer = aUseSawyer
		self.__myOwnMessageList = anOwnMessageList
		
		self.__Active = anActiveChecker
		self.__myMessagesToChoseFrom = []
		self.__reactCommandPointTaken = None
		self.__reactCommandPointLost = None
		
		if self.__Active:
			self.ReactionSetup()
			
	def ReactionSetup( self ):
		
		if not self.__Active:
			return
		
		self.__reactCommandPointTaken = si.RE_OnCommandPointTaken( self.__myCommandPoint, si.TEAM_USA, si.Action( self.MessageSetup ) )
		
	def MessageSetup( self ):

		if len( self.__myMessagesToChoseFrom ) == 0:

			if self.__myOwnMessageList:
				self.__myMessagesToChoseFrom.extend( self.__myOwnMessageList )

			if self.__myUseBannon:
				self.__myMessagesToChoseFrom.extend( [ 'cp_lost_bannon_1', 'cp_lost_bannon_2', 'cp_lost_bannon_3' ] )
			if self.__myUseWebb:
				self.__myMessagesToChoseFrom.extend( [ 'cp_lost_webb_1', 'cp_lost_webb_2', 'cp_lost_webb_3' ] )
			if self.__myUseSawyer:
				self.__myMessagesToChoseFrom.extend( [ 'cp_lost_sawyer_1', 'cp_lost_sawyer_2', 'cp_lost_sawyer_3' ] )
	
		message = random.choice( self.__myMessagesToChoseFrom )	
		self.__myMessagesToChoseFrom.remove( message )

		aqPlayerLoseCP = si.ActionQueue( 'Queue', self.__myRougeMessageChecker )
		aqPlayerLoseCP.AddDelay( 2 )
		aqPlayerLoseCP.AddMessageBox( message, si.lastShownFeedBackMessageBoxId )
		aqPlayerLoseCP.AddAction( si.Action( self.ReactionSetup ) )

		self.__reactCommandPointLost = si.RE_OnCommandPointTaken( self.__myCommandPoint, si.TEAM_NEUTRAL, si.Action( aqPlayerLoseCP.Execute ) )

		si.lastShownFeedBackMessageBoxId += 1

	def Start( self ):

		self.__Active = True

		self.ReactionSetup()

	def Stop( self ):

		si.RemoveReaction( self.__reactCommandPointTaken )
		si.RemoveReaction( self.__reactCommandPointTaken )

		self.__Active = False

	def ChangeCommandPoint( self, aCommandPoint ):

		si.RemoveReaction( self.__reactCommandPointTaken )
		si.RemoveReaction( self.__reactCommandPointTaken )

		self.__myCommandPoint = aCommandPoint
		self.MessageSetup( )

