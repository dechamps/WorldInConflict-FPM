import serverimports as si


DEFAULT_MESSAGE_BOX_DELAY = 1.0
TYPE_NO_TYPE		= 0
TYPE_MESSAGEBOX 	= 1


class QueueItem( object ):
	
	def __init__( self, aType = TYPE_NO_TYPE ):
		
		self.__Action = None
		self.__EndReaction = None
		self.__Type = aType


	def __str__( self ):
				
		return 'Action:%s : EndReaction:%s' % ( self.__Action, self.__EndReaction )


	def SetAction( self, anAction ):
		
		self.__Action = anAction


	def SetEndReaction( self, anAction ):
		
		self.__EndReaction = anAction
		
	
	def GetType( self ):
		
		return self.__Type
	
	
	def IsMessageBox( self ):
		
		return ( TYPE_MESSAGEBOX == self.__Type )


	def Execute( self, anActionQueue ):
		
		if self.__Action:
			self.__Action.Execute()
		
		if self.__EndReaction is None:
			anActionQueue.Next()
		else:
			self.__EndReaction.Execute()


class ActionQueue( object ):
	
	
	def __init__( self, aTargetList, aName, aUseQueueSystem = True ):
		self.__QueueItems = []
		self.__CurrentItem = 0
		self.__UseQueueSystem = aUseQueueSystem
		self.__TargetList = aTargetList
		self.__Name = aName
	

	def RemoveAllItems( self ):
		
		self.__QueueItems = []
		

	def __getQueueItems( self ):
		
		return self.__QueueItems
		
	myQueueItems = property( __getQueueItems )

		
	def __getCurrentItem( self ):
		
		return self.__CurrentItem
		
	myCurrentItem = property( __getCurrentItem )


	def __getName( self ):
		
		return self.__Name
		
	myName = property( __getName )

	
	def AddMessageBox( self, aMessageBoxName, aMessageBoxId, aUnitId = -1, aWorldPos = si.Position(), aBlinkFlag = False ):
		
		newQueueItem = QueueItem( TYPE_MESSAGEBOX )
		newQueueItem.SetAction( si.Action( si.ShowMessageBox, aMessageBoxName, aMessageBoxId, aUnitId, aWorldPos, aBlinkFlag ) )
		newQueueItem.SetEndReaction( si.Action( si.RegisterReaction, si.Reaction( 'MessageBoxClosed', si.Action( self.Next ), si.SimpleTest( aMessageBoxId ) ) ) )
		self.__QueueItems.append( newQueueItem )

	
	def AddMessageBoxEx( self, aMessageBoxName, aMessageBoxId, aUnitId = -1, aWorldPos = si.Position(), aBlinkFlag = False ):
		
		self.AddAction( si.Action( si.PostEvent, 'MessageBoxOpened' ) )
		newQueueItem = QueueItem( TYPE_MESSAGEBOX )
		newQueueItem.SetAction( si.Action( si.ShowMessageBox, aMessageBoxName, aMessageBoxId, aUnitId, aWorldPos, aBlinkFlag ) )
		newQueueItem.SetEndReaction( si.Action( si.RegisterReaction, si.Reaction( 'MessageBoxClosed', si.Action( self.Next ), si.SimpleTest( aMessageBoxId ) ) ) )
		self.__QueueItems.append( newQueueItem )


	def AddEventString( self, aScriptEvent, aIsObjective = False ):

		newQueueItem = QueueItem()
		
		if not aIsObjective:
			newQueueItem.SetAction( si.Action( si.AddScriptEventAll, aScriptEvent ) )
		
		#newQueueItem.SetEndReaction( si.Action( si.RegisterReaction, si.Reaction( 'EventStringDone', si.Action( self.Next ), si.SimpleTest( si.StringToInt( aScriptEvent ) ) ) ) )
		newQueueItem.SetEndReaction( si.Action( si.RegisterReaction, si.Reaction( 'Update', si.Action( self.Next ), si.TimeTest( 2.5 ) ) ) )
		self.__QueueItems.append( newQueueItem )

		
	def AddDelay( self, aDelay ):

		newQueueItem = QueueItem()
		newQueueItem.SetEndReaction( si.Action( si.RegisterReaction, si.Reaction( 'Update', si.Action( self.Next ), si.TimeTest( aDelay ) ) ) )
		self.__QueueItems.append( newQueueItem )

		
	def AddAction( self, anAction ):

		newQueueItem = QueueItem()
		newQueueItem.SetAction( anAction )
		self.__QueueItems.append( newQueueItem )

	
	def AddFunction( self, aFunction, *someArgs ):

		self.AddAction( si.Action( aFunction, *someArgs ) )


	def AddObjective( self, aObjective ):
		self.AddFunction( aObjective.AddObjective )
		self.AddEventString( aObjective.GetName(), True )

	def AddObjectiveUpdate( self, aObjective, aNewObjective ):
		self.AddFunction( aObjective.Update, aNewObjective )
		self.AddEventString( aObjective.GetName(), True )

	def AddObjectiveMarker( self, aObjective, aSubName, aTarget, aAutoCounter = False, aUnit = -1, aPlayerId = 1 ):
		self.AddFunction( aObjective.AddSubMarker, aSubName, aTarget, aAutoCounter, aUnit, aPlayerId )
		if aAutoCounter:
			self.AddEventString( aObjective.GetName(), True )

	def AddObjectiveRemoveMarker( self, aObjective, aSubName, aAutoCounter = False, aPlayerId = 1 ):		
		self.AddFunction( aObjective.RemoveSubMarker, aSubName, aAutoCounter, aPlayerId )	
		if aAutoCounter:
			self.AddEventString( aObjective.GetName(), True )
					
	def AddObjectiveCompleted( self, aObjective ):
		self.AddFunction( aObjective.Completed )
		self.AddEventString( aObjective.GetName(), True )
		
	def AddObjectiveFailed( self, aObjective ):
		self.AddFunction( aObjective.Failed )
		self.AddEventString( aObjective.GetName(), True )

	def AddObjectiveMarkerUpdate( self, aObjective, aSubname, aTarget ):
		self.AddFunction( aObjective.UpdateSubMarkerPos, aSubname, aTarget )

	
	def __Start( self ):
		
		if len( self.__QueueItems ) == 0:
			self.Stop()
			return
		
		self.__CurrentItem = 0	
		self.__QueueItems[0].Execute( self )
		
	
	def Next( self ):
		
		## if we aren't the first queue item we save the type (this is used for message box delays)
		if self.__CurrentItem > -1 and self.__CurrentItem < len( self.__QueueItems ):
			lastType = self.__QueueItems[self.__CurrentItem].GetType()
		else:
			lastType = TYPE_NO_TYPE
		
		self.__CurrentItem += 1
		
		if len( self.__QueueItems ) <= self.__CurrentItem:
			self.Stop()
		else:
			if lastType == TYPE_MESSAGEBOX and self.__QueueItems[self.__CurrentItem].IsMessageBox():
				si.Delay( DEFAULT_MESSAGE_BOX_DELAY, si.Action( self.__QueueItems[self.__CurrentItem].Execute, self ) )
			else:
				self.__QueueItems[self.__CurrentItem].Execute( self )
		
	
	def Stop( self ):
		if not self.__UseQueueSystem:
			if self in self.__TargetList:
				self.__TargetList.remove( self )
			return
		
		if not self in self.__TargetList:
			return
		
		self.__TargetList.remove( self )
		
		if len( self.__TargetList ):
			self.__TargetList[0].__Start()
		
	
	def Execute( self ):
		if not self.__UseQueueSystem:
			self.__TargetList.append( self )
			self.__Start()
			return
		
		if self in self.__TargetList:
			return
		
		self.__TargetList.append( self )
		
		if len( self.__TargetList ) == 1:
			self.__Start()

			
def ShowMessageBoxQueue( aMessageBoxName, aMessageBoxId, aUnitId = -1, aWorldPos = si.Position(), aBlinkFlag = False ):
	
	aq = si.ActionQueue()
	aq.AddMessageBox( aMessageBoxName, aMessageBoxId, aUnitId, aWorldPos, aBlinkFlag )
	aq.Execute()


def PurgeActionQueues( anActionQueueList ):
	q_list = anActionQueueList[:]
	anActionQueueList = []
	
	for q in q_list:
		q.Stop( )
		q.RemoveAllItems()

