import base
import debug

from test import *
from action import *
from globals import *


class ReactionException( Exception ): pass
class ReactionTypeException( ReactionException ): pass
class InvalidActionException( ReactionException ): pass


class CachedEvent( object ):
	
	
	def __init__(self, anEventString, someEventData):
				
		self.__EventString = anEventString
		self.__SomeEventData = someEventData
	
	
	def GetEventString(self):
		
		return self.__EventString
		
	
	def GetEventData(self):
		
		return self.__SomeEventData


class Reactions ( object ):
	
	__ReactionCounter = 0

	def __init__( self ):

		self.__ReactionHandlers = {}
		self.__EventData = []
		
		self.__Pause = False
		
		self.__IsActive = True
		self.__CachedEvents = []
		
		self.__LastActions = []
		self.__HasLastActions = False
		
		## special timer reactions used for performace
		self.__Timers = []

		## special index reactions used for performance
		self.__UnitDestroyed = {}
		self.__UnitInCombat = {}			
		self.__GroupSize = {}
		self.__GroupInCombat = {}
		
		self.__UpdateOneCounter = 0
		
		self.__EarlyOut = False
		
		self.__PostEventDepth = 0
		
	
	@classmethod
	def GetCounter( reactions ):
		
		reactions.__ReactionCounter += 1
		return reactions.__ReactionCounter


	@classmethod
	def PeekCounter( reactions ):
		
		return reactions.__ReactionCounter


	def __getEventData( self ):

		return self.__EventData[-1]


	myEventData = property( __getEventData )


	def __getReactionHandlers( self ):

		return self.__ReactionHandlers


	myReactionHandlers = property( __getReactionHandlers )


	def __getGroupInCombat( self ):

		return self.__GroupInCombat


	myGroupInCombat = property( __getGroupInCombat )


	def Pause( self, aPauseFlag = True ):
		
		self.__Pause = aPauseFlag


	def ResetEventDepth( self ):
		self.__PostEventDepth = 0


	## this is used by the EndGame and GameOver functions
	## to make sure that nothing is executed after those functions
	def DoEarlyOut( self ):
		
		self.__EarlyOut = True


	def Activate( self ):
		
		self.__IsActive = True
		
		for event in self.__CachedEvents:
			self.PostEvent( event.GetEventString(), *event.GetEventData() )
			
		self.__CachedEvents = []


	def Deactivate( self ):
		
		self.__IsActive = False


	def PostEvent( self, anEventString, *someEventData ):
		
		if self.__Pause:
			return
			
		if not self.__IsActive:
			self.PostCachedEvent( anEventString, *someEventData )
			return
	
		if __debug__ and anEventString not in debug.BannedEvents:
			
			eventDataStr = ''
			c = 0
			for d in someEventData:
				eventDataStr += ('%s' % d)
				if c < len( someEventData ) - 1:
					eventDataStr += ', '
				c += 1
			
			debug.DebugMessage( 'Reactions::PostEvent - %s(%s)' % (anEventString, eventDataStr) )
		
		
		## how many recursive post events has been called
		## we need this to execute the LastActions (executed at the end of a post event chain)
		self.__PostEventDepth += 1
		
		self.__EventData.append( someEventData )
		
		
		## Handle normal reactions
		if anEventString in self.__ReactionHandlers:
			if len(self.__ReactionHandlers[anEventString]):
				for currReaction in self.__ReactionHandlers[anEventString][:]:
					if currReaction in self.__ReactionHandlers[anEventString] and currReaction.Test( someEventData ):
						currReaction.Execute()
						
						if not currReaction.myRepeating:
							self.RemoveReaction( currReaction )
							
					if self.__EarlyOut:
						self.__PostEventDepth -= 1
						return
		
		## Handle all special update reactions
		if anEventString == 'Update':
			
			## handle timers (TimerReactions)
			if len( self.__Timers ):
				
				for timer in self.__Timers[:]:
					if timer.myTime <= someEventData[1]:
						timer.Execute()
						self.RemoveReaction( timer )
					
						if timer.myRepeating:
							timer.myTime += timer.myRepeatTime
							self.AddTimer( timer )
					else:
						break
					
					if self.__EarlyOut:
						self.__PostEventDepth -= 1
						return


			## handle low prio updates (UpdateOne reactions)
			if 'UpdateOne' in self.__ReactionHandlers and len( self.__ReactionHandlers['UpdateOne'] ):
				
				if self.__UpdateOneCounter >= len( self.__ReactionHandlers['UpdateOne'] ):
					self.__UpdateOneCounter = 0
					
				#for currReaction in self.__ReactionHandlers['UpdateOne'][:]:
				currReaction = self.__ReactionHandlers['UpdateOne'][self.__UpdateOneCounter]
				if currReaction.Test( someEventData ):
					currReaction.Execute()
						
					if not currReaction.myRepeating:
						self.RemoveReaction( currReaction )
										
				self.__UpdateOneCounter += 1

				if self.__EarlyOut:
					self.__PostEventDepth -= 1
					return

		
		## Handle UnitDestroyed reactions (UnitDestroyedReaction)
		elif anEventString == 'UnitDestroyed':
			if someEventData[0] in self.__UnitDestroyed:
				if len( self.__UnitDestroyed[someEventData[0]] ):
					for currReaction in self.__UnitDestroyed[someEventData[0]][:]:
						if currReaction in self.__UnitDestroyed[someEventData[0]] and currReaction.Test( someEventData ):
							currReaction.Execute()
							
							if not currReaction.myRepeating:
								self.RemoveReaction( currReaction )
						if self.__EarlyOut:
							self.__PostEventDepth -= 1
							return

		
		## Handle UnitInCombat reactions (UnitInCombatReaction)			
		elif anEventString == 'UnitInCombat':
			if someEventData[0] in self.__UnitInCombat:
				if len( self.__UnitInCombat[someEventData[0]] ):
					for currReaction in self.__UnitInCombat[someEventData[0]][:]:
						if currReaction in self.__UnitInCombat[someEventData[0]] and currReaction.Test( someEventData ):
							currReaction.Execute()
							
							if not currReaction.myRepeating:
								self.RemoveReaction( currReaction )
						if self.__EarlyOut:
							self.__PostEventDepth -= 1
							return

			elif someEventData[1] in self.__UnitInCombat:
				if len( self.__UnitInCombat[someEventData[1]] ):
					for currReaction in self.__UnitInCombat[someEventData[1]][:]:
						if currReaction in self.__UnitInCombat[someEventData[1]] and currReaction.Test( someEventData ):
							currReaction.Execute()
							
							if not currReaction.myRepeating:
								self.RemoveReaction( currReaction )
						if self.__EarlyOut:
							self.__PostEventDepth -= 1
							return

		## Handle GroupSize reactions (GroupSizeReaction)
		elif anEventString == 'GroupSize':
			if someEventData[0].myId in self.__GroupSize:
				if len( self.__GroupSize[someEventData[0].myId] ):
					for currReaction in self.__GroupSize[someEventData[0].myId][:]:
						if currReaction in self.__GroupSize[someEventData[0].myId] and currReaction.Test( someEventData ):
							currReaction.Execute()
						
							if not currReaction.myRepeating:
								self.RemoveReaction( currReaction )
						if self.__EarlyOut:
							self.__PostEventDepth -= 1
							return

		## Handle GroupInCombat reactions (GroupInCombatReaction)
		elif anEventString == 'GroupInCombat':
			if someEventData[0].myId in self.__GroupInCombat:
				if len( self.__GroupInCombat[someEventData[0].myId] ):
					for currReaction in self.__GroupInCombat[someEventData[0].myId][:]:
						if currReaction in self.__GroupInCombat[someEventData[0].myId] and currReaction.Test( someEventData ):
							currReaction.Execute()
						
							if not currReaction.myRepeating:
								self.RemoveReaction( currReaction )
						if self.__EarlyOut:
							self.__PostEventDepth -= 1
							return
		
		if len( self.__EventData ):
			self.__EventData.pop()
		
		## the Last Actions must be executed in the top most PostEvent
		if self.__HasLastActions and self.__PostEventDepth == 1:
			self.__HasLastActions = False
			for act in self.__LastActions[:]:
				act.Execute()
			self.__LastActions = []
		
		self.__PostEventDepth -= 1


	def PostCachedEvent( self, anEventString, *someEventData):
		
		self.__CachedEvents.append(CachedEvent(anEventString, someEventData))


	def AddLastAction( self, anAction ):
		
		self.__LastActions.append(anAction)
		self.__HasLastActions = True
	
	
	def AddTimer( self, aTimer ):
		
		counter = 0
		for timer in self.__Timers:
			if timer.myTime > aTimer.myTime:
				self.__Timers.insert( counter, aTimer )
				return
			counter += 1
			
		self.__Timers.append( aTimer )
		
	
	def AddTimeToTimers( self, aTime ):
		
		for timer in self.__Timers:
			timer.myTime += aTime
	
	
	def AddUnitDestroyedReaction( self, aReaction ):
		
		if not aReaction.myUnitId in self.__UnitDestroyed:
			self.__UnitDestroyed[aReaction.myUnitId] = []

		self.__UnitDestroyed[aReaction.myUnitId].append( aReaction )

		
	def AddUnitInCombatReaction( self, aReaction ):
		
		if not aReaction.myUnitId in self.__UnitInCombat:
			self.__UnitInCombat[aReaction.myUnitId] = []
			
		self.__UnitInCombat[aReaction.myUnitId].append( aReaction )


	def AddGroupSizeReaction( self, aReaction ):
		
		if not aReaction.myGroupId in self.__GroupSize:
			self.__GroupSize[aReaction.myGroupId] = []
		
		self.__GroupSize[ aReaction.myGroupId ].append( aReaction )


	def AddGroupInCombatReaction( self, aReaction ):
		
		if not aReaction.myGroupId in self.__GroupInCombat:
			self.__GroupInCombat[aReaction.myGroupId] = []
		
		self.__GroupInCombat[ aReaction.myGroupId ].append( aReaction )

	
	def RegisterReaction( self, aReaction, aFirstInList = False ):
			
		if isinstance( aReaction, TimerReaction ):
			aReaction.myTime += ( base.GetCurrentTime() - aReaction.myPauseTime )
			self.AddTimer( aReaction )
			return aReaction
		elif isinstance ( aReaction, UnitDestroyedReaction ):
			self.AddUnitDestroyedReaction( aReaction )
			return aReaction
		elif isinstance ( aReaction, UnitInCombatReaction ):
			self.AddUnitInCombatReaction( aReaction )
			return aReaction
		elif isinstance ( aReaction, GroupSizeReaction ):
			self.AddGroupSizeReaction( aReaction )
			return aReaction
		elif isinstance ( aReaction, GroupInCombatReaction ):
			self.AddGroupInCombatReaction( aReaction )
			return aReaction
	
		if not aReaction.myEventString in self.__ReactionHandlers:
			self.__ReactionHandlers[aReaction.myEventString] = []
		
		if aFirstInList:
			# insert this item first
			self.__ReactionHandlers[aReaction.myEventString].insert( 0, aReaction )
		else:
			self.__ReactionHandlers[aReaction.myEventString].append( aReaction )
		return aReaction


	def RemoveReaction( self, aReaction ):
		
		if __debug__:
			debug.DebugMessage( 'Reactions::RemoveReaction - %s' % aReaction )
		
		if aReaction is None:
			return

		if isinstance( aReaction, TimerReaction ):
			if aReaction in self.__Timers:
				self.__Timers.remove( aReaction )
				aReaction.myPauseTime = base.GetCurrentTime()
			return
		
		if isinstance( aReaction, UnitDestroyedReaction ):
			if aReaction.myUnitId in self.__UnitDestroyed:
				if aReaction in self.__UnitDestroyed[ aReaction.myUnitId ]:
					self.__UnitDestroyed[ aReaction.myUnitId ].remove( aReaction )
			return
			
		if isinstance( aReaction, UnitInCombatReaction ):
			if aReaction.myUnitId in self.__UnitInCombat:
				if aReaction in self.__UnitInCombat[ aReaction.myUnitId ]:
					self.__UnitInCombat[ aReaction.myUnitId ].remove( aReaction )
			return

		if isinstance( aReaction, GroupSizeReaction ):
			if aReaction.myGroupId in self.__GroupSize:
				if aReaction in self.__GroupSize[ aReaction.myGroupId ]:
					self.__GroupSize[ aReaction.myGroupId ].remove( aReaction )
			return

		if isinstance( aReaction, GroupInCombatReaction ):
			if aReaction.myGroupId in self.__GroupInCombat:
				if aReaction in self.__GroupInCombat[ aReaction.myGroupId ]:
					self.__GroupInCombat[ aReaction.myGroupId ].remove( aReaction )
			return

		if isinstance( aReaction, ComplexReaction ):
			aReaction.Shutdown()
			return
			
		if not isinstance( aReaction, Reaction ):
			raise ReactionTypeException( 'Reactions::RemoveReaction Trying to remove a none Reaction (%s)' % aReaction )
			
		if aReaction.myEventString in self.__ReactionHandlers:
			if aReaction in self.__ReactionHandlers[aReaction.myEventString]:
				self.__ReactionHandlers[aReaction.myEventString].remove( aReaction )
			else:
				return
		else:
			return
	
	
	def RemoveAllTimers( self ):
		
		self.__Timers = []
		

	def RemoveAllReactions( self ):
		
		debug.DebugMessage( 'Reactions::RemoveAllReaction Reactions Registered=%d' % self.GetCurrentNrOfReactions(), debug.VERBOSE )
		
		self.__ReactionHandlers = {}
		self.__UnitDestroyed = {}
		self.__UnitInCombat = {}
		self.__GroupSizeCombat = {}
		self.__GroupInCombatCombat = {}
		self.__Timers = []
		self.__EventData = []
		self.__LastActions = []
		self.__HasLastActions = False
				
	
	def GetCurrentNrOfReactions( self ):
		
		sum = 0
		
		for event in self.__ReactionHandlers:
			sum += len ( self.__ReactionHandlers[event] )
		
		sum += len( self.__Timers )
		
		for reactIndex in self.__UnitDestroyed:
			try:
				sum += len( self.__UnitDestroyed[reactIndex] )
			except TypeError:
				pass
		for reactIndex in self.__UnitInCombat:
			try:
				sum += len( self.__UnitInCombat[reactIndex] )
			except TypeError:
				pass
		for reactIndex in self.__GroupSize:
			try:
				sum += len( self.__GroupSize[reactIndex] )
			except TypeError:
				pass
		for reactIndex in self.__GroupInCombat:
			try:
				sum += len( self.__GroupInCombat[reactIndex] )
			except TypeError:
				pass
		return sum


	def GetNrOfReactionsByType( self, anEventString ):

		if anEventString in self.__ReactionHandlers:
			return len(self.__ReactionHandlers[anEventString])
		else:
			return 0
			

	def GetReactionsByType( self, anEventString, aMaxAmount = -1 ):
		
		if anEventString in self.__ReactionHandlers:
			if aMaxAmount == -1:
				return self.__ReactionHandlers[anEventString][:]
			else:
				if aMaxAmount > len(self.__ReactionHandlers[anEventString]):
					aMaxAmount = len(self.__ReactionHandlers[anEventString])
				
				return self.__ReactionHandlers[anEventString][0:aMaxAmount]
		
		return None


	def GetTimers( self ):
		
		return self.__Timers


	def GetNrOfTimers( self ):
		
		return len( self.__Timers )
		
	
	def GetNrOfBadTimers( self ):
		
		sum = 0
		for t in self.__Timers:
			if t.GetTimeLeft() < -BAD_TIMER_LIMIT:
				sum += 1
		return sum

	
	def GetNrOfUnitDestroyed( self ):
		
		sum = 0
		for reactIndex in self.__UnitDestroyed:
			try:
				sum += len( self.__UnitDestroyed[reactIndex] )
			except TypeError:
				pass
		return sum



	def GetNrOfUnitInCombat( self ):
		
		sum = 0
		for reactIndex in self.__UnitInCombat:
			try:
				sum += len( self.__UnitInCombat[reactIndex] )
			except TypeError:
				pass
		return sum



	def GetNrOfGroupInCombat( self ):
		
		sum = 0
		for reactIndex in self.__GroupInCombat:
			try:
				sum += len( self.__GroupInCombat[reactIndex] )
			except TypeError:
				pass
		return sum

	
	
	def GetNrOfGroupSize( self ):
		
		sum = 0
		for reactIndex in self.__GroupSize:
			try:
				sum += len( self.__GroupSize[reactIndex] )
			except TypeError:
				pass
		return sum


	
	def GetTotalNrOfReactions( self ):
				
		return Reactions.PeekCounter()


class Reaction( object ):

	def __init__( self, anEventString, someActions, someTestHandles = None ):
		
		self.__EventString = anEventString
		
		if isinstance( someActions, list ):
			for act in someActions:
				if not isinstance(act, Action):
					raise InvalidActionException( 'Reaction::__init__(): %s is not an valid Action' % someActions )
			
			self.__Actions = someActions
		else:
			if not isinstance(someActions, Action):
				raise InvalidActionException( 'Reaction::__init__(): %s is not an valid Action' % someActions )
		
			self.__Actions = [someActions]

		self.__TestHandles = someTestHandles
		self.__Repeating = False
		self.__NrOfExecutions = -1
		self.__EndActions = []
		self.__TestType = REACTION_TEST_AND
		self.__Name = '%s_%d' % (anEventString, Reactions.GetCounter())
	
		
	def __str__( self ):
		
		stringRep = '%s' % self.__Name
				
		for a in self.__Actions:
			stringRep += ' %s' % a
		
		return stringRep


	def __getName( self ):
		
		return self.__Name
		
	
	myName = property(__getName)


	def __getEventString( self ):
		
		return self.__EventString
		
	
	myEventString = property(__getEventString)

	
	def __getRepeating( self ):
		
		return self.__Repeating
	

	def __setRepeating( self, aRepeatingFlag ):
		
		self.__Repeating = aRepeatingFlag

	
	myRepeating = property( __getRepeating, __setRepeating )


	def __getNrOfExecutions( self ):
		
		return self.__NrOfExecutions
	

	def __setNrOfExecutions( self, aNrOfExecutions ):
		
		if aNrOfExecutions == 0:
			raise ReactionException( 'Reaction::__setNrOfExecutions - Cant set NrOfExecutions to 0!' )
		
		self.__NrOfExecutions = aNrOfExecutions
		
		if aNrOfExecutions > 0:
			self.__Repeating = True

	
	myNrOfExecutions = property( __getNrOfExecutions, __setNrOfExecutions )


	def __getTestType( self ):
		
		return self.__TestType


	def __setTestType( self, aTestType ):
		
		self.__TestType = aTestType

	
	myTestType = property( __getTestType, __setTestType )


	def GetTest( self, aIndex = 0 ):
		
		if isinstance( self.__TestHandles, list ):
			return self.__TestHandles[aIndex]
		else:
			return self.__TestHandles

	
	def AddAction( self, anAction ):
		
		self.__Actions.append( anAction )


	def AddActions( self, someActions ):
		
		self.__Actions.extend( someActions )

	
	def RemoveAction( self, anAction ):

		try:		
			self.__Actions.remove( anAction )
		except ValueError:
			pass

	
	def AddEndAction( self, anAction ):
		
		self.__EndActions.append( anAction )
	
	
	def AddTest( self, aTest ):
		
		self.__TestHandles.append( aTest )


	def RemoveAllTests( self ):
		
		self.__TestHandles = []

	
	def Test( self, someEventData ):
			
		if self.__TestHandles is None:
			return True
		
		if isinstance( self.__TestHandles, list ):
			if self.__TestType == REACTION_TEST_AND:
				for t in self.__TestHandles:
					if not t( someEventData ):
						return False
				return True
			elif self.__TestType == REACTION_TEST_OR:
				for t in self.__TestHandles:
					if t( someEventData ):
						return True
				return False
			elif self.__TestType == REACTION_TEST_XOR:
				counter = 0
				for t in self.__TestHandles:
					if t( someEventData ):
						counter += 1
				if counter == 1:
					return True
				else:
					return False
			elif self.__TestType == REACTION_TEST_NOT:
				for t in self.__TestHandlers:
					if t( someEventData ):
						return False
					return True
			return False
		else:
			testRes = self.__TestHandles(someEventData)
			
			if self.__TestType == REACTION_TEST_NOT:
				testRes = (not testRes)

			return testRes


	def Execute( self ):
		
		if self.__NrOfExecutions != -1:
			self.__NrOfExecutions -= 1
			
			if self.__NrOfExecutions == 0:
				self.__Repeating = False
		
		if self.__Actions is None:
			return
		
		for a in self.__Actions:
			a.Execute()
		
		## execute all end actions
		if len( self.__EndActions ) and not self.__Repeating:
			for a in self.__EndActions:
				a.Execute()


class TimerReaction( Reaction ):
	
	def __init__( self, someActions, aTime, aRepeatTime = 0.0 ):
		
		
		Reaction.__init__( self, 'TimerReaction', someActions )
		
		self.__Time = aTime
		self.__RepeatTime = aRepeatTime
		self.__PauseTime = base.GetCurrentTime()
		
		if self.__RepeatTime:
			self.myRepeating = True
		
	
	def __getTime( self ):
		
		return self.__Time

	def __setTime( self, aNewTime ):
		
		self.__Time = aNewTime
		
	myTime = property( __getTime, __setTime )

		
	def __getRepeatTime( self ):
		
		return self.__RepeatTime

	def __setRepeatTime( self, aNewRepeatTime ):
		
		self.__RepeatTime = aNewRepeatTime
		
	myRepeatTime = property( __getRepeatTime, __setRepeatTime )


	def __getPauseTime( self ):
		
		return self.__PauseTime

	def __setPauseTime( self, aNewPauseTime ):
		
		self.__PauseTime = aNewPauseTime
	
	myPauseTime = property( __getPauseTime, __setPauseTime )
	
	
	def GetTimeLeft( self ):
		
		return self.__Time - base.GetCurrentTime()
			
		
class UnitDestroyedReaction( Reaction ):
	
	def __init__( self, someActions, aUnitId ):
		
		
		Reaction.__init__( self, 'UnitDestroyedReaction', someActions )
		self.__UnitId = aUnitId


	def __getUnitId( self ):
		return self.__UnitId
		
	myUnitId = property( __getUnitId )
		
	
	def Test( self, someEventData ):
		
		if someEventData[0] == self.__UnitId:
			return True
		return False


class UnitInCombatReaction( Reaction ):
	
	def __init__( self, someActions, aUnitId ):
		
		
		Reaction.__init__( self, 'UnitInCombatReaction', someActions )
		self.__UnitId = aUnitId


	def __getUnitId( self ):
		return self.__UnitId
		
	myUnitId = property( __getUnitId )
		
	
	def Test( self, someEventData ):
		
		if someEventData[0] == self.__UnitId or someEventData[1] == self.__UnitId:
			return True
		return False


class GroupSizeReaction( Reaction ):
	
	def __init__( self, someActions, aGroup, aSize ):
		
		
		Reaction.__init__( self, 'GroupSizeReaction', someActions )
		self.__Group = aGroup
		self.__Size = aSize


	def __getGroupId( self ):
		return self.__Group.myId
		
	myGroupId = property( __getGroupId )
		
	
	def Test( self, someEventData ):
		
		
		if someEventData[0].myId == self.__Group.myId and someEventData[1] == self.__Size:
			return True
		if someEventData[0].myId == self.__Group.myId and self.__Size == -1:
			return True
		return False


class GroupInCombatReaction( Reaction ):
	
	def __init__( self, someActions, aGroup ):
		
		
		Reaction.__init__( self, 'GroupInCombatReaction', someActions, aGroup )
		self.__Group = aGroup


	def __getGroupId( self ):
		return self.__Group.myId
		
	myGroupId = property( __getGroupId )
		
	
	def Test( self, someEventData ):
		
		if someEventData[0].myId == self.__Group.myId:
			return True
		return False


class ComplexReaction( object ):

	def __init__(self, someActions ):
			
		if isinstance( someActions, list ):
			for act in someActions:
				if not isinstance(act, Action):
					raise InvalidActionException( 'Reaction::__init__(): %s is not an valid Action' % someActions )
			
			self.__Actions = someActions
		else:
			if not isinstance(someActions, Action):
				raise InvalidActionException( 'Reaction::__init__(): %s is not an valid Action' % someActions )
		
			self.__Actions = [someActions]
	

	def __str__( self ):
		
		return "%s" % (self.__class__.__name__)


	def AddAction( self, aAction ):
		
		self.__Actions.append( aAction )


	def RemoveAction( self, aAction ):

		try:		
			self.__Actions.remove( aAction )
		except ValueError:
			pass


	def Execute( self ):

		if self.__Actions is None:
			return
		
		for a in self.__Actions:
			a.Execute()
