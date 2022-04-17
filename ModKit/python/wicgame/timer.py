import serverimports


DEBUG_TIMER_POS_X = 0.046
DEBUG_TIMER_POS_Y = 0.048
DEBUG_TIMER_COLOR = 0x22ff22

FONT_NORMAL	= 0
FONT_BIG	= 1


class TimerException( Exception ): pass
class TimerNotStartedException( TimerException ): pass
class InvalidFontException( TimerException ): pass


class Timer( object ):


	def __init__( self, aTime, someActions, aTimerName = None, aAutoStart = True, aTimerIndex = 0 ):
		self.__Time = aTime
		self.__TimerName = aTimerName
		
		if isinstance( someActions, serverimports.Action ):
			self.__actAction = [someActions]
		elif someActions is None:
			self.__actAction = []
		elif isinstance( someActions, list ):
			self.__actAction = someActions
		else:
			raise TimerException( 'Bad actions. Must be None|Action|[action,action,...].' )
		
		self.__actAction.append( serverimports.Action( self.Remove ) )
		self.__reactTimer = None
		self.__reactPause = None
		self.__Paused = True
		self.__AutoStart = aAutoStart
		self.__TimerIndex = aTimerIndex
		self.__DelayList = []
		
		if self.__AutoStart:
			self.Start()


	def IsValid( self ):
		
		if self.__reactTimer:
			return True
		
		return False
	
	
	def IsActive( self ):
		
		return not self.__Paused
		

	def Start( self ):
		serverimports.RemoveReaction( self.__reactTimer )
		serverimports.RemoveReaction( self.__reactPause )
		self.__reactTimer = serverimports.Delay( self.__Time, self.__actAction )
		self.__Paused = False
		if self.__TimerName != None:
			serverimports.ShowTimer( 1, self.__TimerName, self.__Time, self.__TimerIndex )

		for aDelay in self.__DelayList:
			serverimports.RegisterReaction( aDelay )


	def Pause( self ):
		import math
		
		if self.__reactTimer is None:
			raise TimerNotStartedException( 'Timer(%s) must be started before calling Pause()' % self.__TimerName )
		
		serverimports.RemoveReaction( self.__reactTimer )
		serverimports.RemoveReaction( self.__reactPause )
		self.__Paused = True
		
		currentTime = math.floor( self.__reactTimer.GetTimeLeft() ) + 0.9
		
		if self.__TimerName != None:
			self.__reactPause = serverimports.RE_OnCustomEvent( 'Update', serverimports.Action( serverimports.ShowTimer, 1, self.__TimerName, currentTime, self.__TimerIndex ) )
			self.__reactPause.myRepeating = True

		for aDelay in self.__DelayList:
			serverimports.RemoveReaction( aDelay )
		
	def Resume( self ):
		import math
		
		if self.__reactTimer is None:
			raise TimerNotStartedException( 'Timer(%s) must be started before calling Resume()' % self.__TimerName )

		serverimports.RemoveReaction( self.__reactPause )
		serverimports.RemoveReaction( self.__reactTimer )
		serverimports.RegisterReaction( self.__reactTimer )
		self.__Paused = False
		if self.__TimerName != None:
			currentTime = math.floor( self.__reactTimer.GetTimeLeft() )
			serverimports.ShowTimer( 1, self.__TimerName, self.__reactTimer.GetTimeLeft(), self.__TimerIndex )

		for aDelay in self.__DelayList:
			serverimports.RegisterReaction( aDelay )


	def Remove( self ):
		serverimports.RemoveReaction( self.__reactTimer )
		self.__reactTimer = None
		serverimports.RemoveReaction( self.__reactPause )
		self.__Paused = True
		if self.__TimerName != None:
			serverimports.ShowTimer( 1, self.__TimerName, 0, self.__TimerIndex )

		for aDelay in self.__DelayList:
			serverimports.RemoveReaction( aDelay )
			
		self.__DelayList = []


	def AddTime( self, aTimeToAdd ):
		myCurrentTime = self.__reactTimer.GetTimeLeft()
		myCurrentTime += aTimeToAdd
		serverimports.RemoveReaction( self.__reactTimer )
		serverimports.RemoveReaction( self.__reactPause )
		self.__reactTimer = serverimports.Delay( myCurrentTime, self.__actAction )
		if self.__TimerName != None:
			serverimports.ShowTimer( 1, self.__TimerName, myCurrentTime, self.__TimerIndex )


	def RemoveTime( self, aTimeToRemove ):
		myCurrentTime = self.__reactTimer.GetTimeLeft()
		myCurrentTime -= aTimeToRemove
		
		if myCurrentTime < 0:
			myCurrentTime = 0
		
		serverimports.RemoveReaction( self.__reactTimer )
		serverimports.RemoveReaction( self.__reactPause )
		self.__reactTimer = serverimports.Delay( myCurrentTime, self.__actAction )
		if self.__TimerName != None:
			serverimports.ShowTimer( 1, self.__TimerName, myCurrentTime, self.__TimerIndex )


	def GetTimeLeft( self ):
		if self.__reactTimer:
			return self.__reactTimer.GetTimeLeft( )
		
		return 0


	def AddActionAfterStart( self, aTimeAfterStart, someActions ):
		if not self.IsActive():
			reactTemp = serverimports.Delay( aTimeAfterStart, someActions )
			self.__DelayList.append( reactTemp )
			serverimports.RemoveReaction( reactTemp )

	
	def AddActionBeforeEnd( self, aTimeBeforeEnd, someActions ):
		if not self.IsActive():
			aStartTime = self.__Time-aTimeBeforeEnd
			reactTemp = serverimports.Delay( aStartTime, someActions )
			self.__DelayList.append( reactTemp )
			serverimports.RemoveReaction( reactTemp )

		 



class DebugTimer( object ):

	def __init__( self, aTime, someActions = None, aAutoStart = True, aFontType = FONT_NORMAL, aPosX = DEBUG_TIMER_POS_X, aPosY = DEBUG_TIMER_POS_Y, aColor = DEBUG_TIMER_COLOR ):
		self.__Time = aTime
		self.__PosX = aPosX
		self.__PosY = aPosY
		self.__Color = aColor
		self.__FontType = aFontType
		
		if someActions is None:
			self.__actAction = []
		elif isinstance( someActions, serverimports.Action ):
			self.__actAction = [someActions]
		else:
			self.__actAction = someActions
		
		self.__reactTimer = None
		self.__reactUpdate = None
		self.__AutoStart = aAutoStart
		
		if self.__AutoStart:
			self.Start()


	def SetFont( self, aFontType ):
		
		self.__FontType = aFontType
		

	def Start( self ):
		serverimports.RemoveReaction( self.__reactTimer )
		serverimports.RemoveReaction( self.__reactUpdate )
		
		self.__actAction.append( serverimports.Action( self.Remove ) )
		
		self.__reactTimer = serverimports.Delay( self.__Time, self.__actAction )
		self.__reactUpdate = serverimports.RE_OnCustomEvent( 'Update', serverimports.Action( self.Update ) )
		self.__reactUpdate.myRepeating = True


	def Update( self ):
		
		timeGone = self.__Time - self.__reactTimer.GetTimeLeft()
		
		if self.__FontType == FONT_NORMAL:
			serverimports.ClientCommand( 'PrintText', '%.2f' % timeGone, self.__PosX, self.__PosY, self.__Color )
		elif self.__FontType == FONT_BIG:
			serverimports.ClientCommand( 'PrintTextBig', '%.2f' % timeGone, self.__PosX, self.__PosY, self.__Color )
		else:
			raise InvalidFontException( 'Trying to use invalid font! (%d) See timer.py for valid fonts.' % self.__FontType )

	
	def Pause( self ):
		import math
		
		serverimports.RemoveReaction( self.__reactTimer )
		
		
	def Resume( self ):
		import math
		
		serverimports.RemoveReaction( self.__reactTimer )
		serverimports.RegisterReaction( self.__reactTimer )

		
	def Remove( self ):
		serverimports.RemoveReaction( self.__reactTimer )
		serverimports.RemoveReaction( self.__reactUpdate )
