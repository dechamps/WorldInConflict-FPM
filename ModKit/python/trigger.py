"""World in Conflict trigger module. Contains basic triggertype classdefinitions as well as the TriggerContainer class.

Trigger objects are called through TriggerContainer.Update() each frame.
If Update() returns a value less than 0, an error is indicated.
If Update() return 0, it indicates that the Trigger have triggered and should be removed.
If Update() return a value more than 0, the trigger is still working on sometime and should be called again next frame.
"""


import base, wicg, game, debug


class Trigger( object ):
	""" Baseclass for all triggers."""

	def __init__( self, aCallFunction, someCallFunctionArguments = None ):
		""" Constructor
		"""
		self.myIsTriggered = False
		self.myCallFunction = aCallFunction
		self.myCallFunctionArguments = someCallFunctionArguments


	def __str__( self ):
		""" Gives a string when used as a string
		"""
		return "Trigger baseclass"

	
	def Update( self ):
		""" Empty baseclass function."""
		return 0


	def CatchEvent( self, anEvent ):
		""" Empty baseclass function."""
		return 0


	def Trigger( self ):
		""" Calls the triggerfunction
		"""
		base.DebugMessage( "Trigger calling %s" % self.myCallFunction.__name__ )
		if self.myCallFunctionArguments is None:
			self.myCallFunction()
		else:
			if isinstance( self.myCallFunctionArguments, dict ):
				self.myCallFunction( **self.myCallFunctionArguments )
			else:
				self.myCallFunction( self.myCallFunctionArguments )


	def IsTriggered( self ):
		""" Test weather the trigger is triggered."""
		try:
			return self.myIsTriggered
			
		except AttributeError:
			self.myIsTriggered = False
			return self.myIsTriggered


class TRG_CustomTrigger( Trigger ):
	""" A trigger that triggeres when a given testfunction returns true
	"""
	
	def __init__( self, aTestFunction, someTestFunctionArguments, aCallFunction, someCallFunctionArguments ):
		""" Constructor
		"""
		Trigger.__init__( self, aCallFunction, someCallFunctionArguments )
		self.__testFunction = aTestFunction
		self.__testFunctionArguments = someTestFunctionArguments
	
	
	def Update( self ):
		""" Check trigger condition
		"""
		if self.__testFunctionArguments:
			return self.__testFunction( self.__testFunctionArguments )
		else:
			return self.__testFunction()


class TRG_UnitInArea( Trigger ):
	""" Releases when one or more units reaches a certain area.
	"""

	def __init__( self, someUnits, aPosition, aRadius, aCallFunction, someCallFunctionArguments = None, aUnitContainer = None ):
		""" Constructor function.
		
		someUnits		- (list or int) One or more unitID in a list (if just one unit, no list is needed)
		aPosition		- (Position) A center position
		aRadius			- (float) a radius from center to check for unit.
		aCallFunction	- (func) a function to call when the Event happens.
		someCallFunctionArguments	- (list) list of arguments to aCallFunction
		"""
		Trigger.__init__( self, aCallFunction, someCallFunctionArguments ) #Run Trigger constructor
		
		self.myUnitIDs = []
		self.myPos = aPosition
		self.myRadius = aRadius
		
		try:
			self.myUnitIDs.extend( someUnits )
		except TypeError:
			self.myUnitIDs.append( someUnits )
		
##		base.DebugMessage( "New TRG_UnitInArea created: %s" % self )


	def GetInfoString( self ):
		""" Returns a short description of the trigger."""
		return self.__str__()


	def __str__( self ):
		""" Returns a short description of the trigger."""
		infoString = "\n<TRG_UnitInArea>"
		
		infoString = "%s\n\t<TrackedUnits count='%d'>" % ( infoString, len( self.myUnitIDs ) )
		
		for unitId in self.myUnitIDs:
			infoString = "%s\n\t\tUnit id: %d" % ( infoString, unitId )
		
		infoString = "%s\n\t</TrackedUnits>" % ( infoString )
		
		infoString = "%s\n\tCallFunctionName: %s" % ( infoString, self.myCallFunction.__name__ )
		
		infoString = "%s\n\t<CallFunctionArguments count='%d'>" % ( infoString, len( self.myCallFunctionArguments ) )
		
		for argument in self.myCallFunctionArguments:
			infoString = "%s\n\t\tType: %s Value: %s" % ( infoString, type( argument ), argument )
		
		infoString = "%s\n\t</CallFunctionArguments>" % ( infoString )
		
		infoString = "%s\n\tPosition: %s" % ( infoString, self.myPos )
		infoString = "%s\n\tRadius: %2.2f" % ( infoString, self.myRadius )
		infoString = "%s\n</TRG_UnitInArea>" % infoString
		
		return infoString


	def Update( self ):
		""" Checks if the units are within the area, if so calls myCallFunction.
		"""
		
		units = game.theGame.GetUnitsInAreaXZ( self.myPos, self.myRadius )
		
		if not len( units ):
			return 1
		
		for u in self.myUnitIDs:
			unit = game.theGame.GetUnit( u )
			if unit in units:
				base.DebugMessage( "TRG_UnitInArea calling %s" % self.myCallFunction.__name__ )
				self.Trigger()
				return 0
		
		return 1


class TRG_UnitsInAreaAllIn( Trigger ):
	""" Releases when one or more units reaches a certain area.
	"""

	def __init__( self, someUnits, aPosition, aRadius, aCallFunction, someCallFunctionArguments = None, aUnitContainer = None ):
		""" Constructor function.
		
		someUnits - (list) unitIDs in a list
		aPosition - (Position) A center position
		aRadius - (float) a radius from center to check for unit.
		aCallFunction - (func) a function to call when the Event happens.
		someCallFunctionArguments - (list) list of arguments to aCallFunction
		aUnitContainer - (None) legacy code kept for compability
		"""
		Trigger.__init__( self, aCallFunction, someCallFunctionArguments ) #Run Trigger constructor
		
		self.myUnitIDs = []
		self.myCallFunction = aCallFunction
		self.myCallFunctionArguments = someCallFunctionArguments
		self.myPos = aPosition
		self.myRadius = aRadius
		self.myHaveBeenInArea = 0
		
		try:
			self.myUnitIDs.extend(someUnits)
		except TypeError:
			self.myUnitIDs.append(someUnits)
		
##		base.DebugMessage( "New TRG_UnitsInAreaAllIn created: %s" % self )


	def __str__( self ):
		""" Returns a short description of the trigger."""
		infoString = "\n<TRG_UnitsInAreaAllIn>"
		
		infoString = "%s\n\t<trackedUnits count='%d'>" % ( infoString, len( self.myUnitIDs ) )
		for unitId in self.myUnitIDs:
			infoString = "%s\n\t\tUnit id: %d" % ( infoString, unitId )
		
		infoString = "%s\n\t</trackedUnits>" % ( infoString )
		infoString = "%s\n\tCallFunctionName: %s" % ( infoString, self.myCallFunction.__name__ )
		
		try:
			infoString = "%s\n\t<callFunctionArguments count='%d'>" % ( infoString, len( self.myCallFunctionArguments ) )
			for argument in self.myCallFunctionArguments:
				infoString = "%s\n\t\tType: %s Value: %s" % ( infoString, type( argument ), argument )
			
			infoString = "%s\n\t</callFunctionArguments>" % ( infoString )
		except Exception:
			infoString = "%s\n\tcallFunctionArgument: type=%s value=%s" % ( infoString, type( self.myCallFunctionArguments ), self.myCallFunctionArguments )
		
		infoString = "%s\n\tPosition: %s" % ( infoString, self.myPos )
		infoString = "%s\n\tRadius: %2.2f" % ( infoString, self.myRadius )
		
		infoString = "%s\n</TRG_UnitsInAreaAllIn>" % infoString
		
		return infoString


	def GetInfoString( self ):
		""" Returns a short description of the trigger."""
		return self.__str__()


	def Update( self ):
		""" Checks if the units are within the area, if so calls myCallFunction.
		"""
		
		if self.myCallFunction is None:
			return -1
		
		# new stuff
		for uID in self.myUnitIDs[:]:
			unit = game.theGame.GetUnit( uID )
			if unit is None:
				self.myUnitIDs.remove( uID )
		
		units = game.theGame.GetUnitsInAreaXZ( self.myPos, self.myRadius )
		
		for k in units:
			if k.myID in self.myUnitIDs[:]:
				self.myUnitIDs.remove(k.myID)
				self.myHaveBeenInArea = 1
		
		if  len(self.myUnitIDs) == 0 and self.myHaveBeenInArea == 1:
			base.DebugMessage( "TRG_UnitInAreaAllIn: Hit!" )
			self.Trigger()
			return 0
		
		if len(self.myUnitIDs) == 0:
			#remove trigger..
			return 0
		
		return 1


class TRG_UnitsInAreasAllIn( Trigger ):
	""" Releases when one or more units reaches a certain area.
	"""

	def __init__( self, someUnits, someAreas, aCallFunction, someCallFunctionArguments = None, aUnitContainer = None ):
		""" Constructor function.
		
		someUnits - (list) unitIDs in a list
		#aPosition - (Position) A center position
		#aRadius - (float) a radius from center to check for unit.
		someAreas - (list) areas in a list
		aCallFunction - (func) a function to call when the Event happens.
		someCallFunctionArguments - (list) list of arguments to aCallFunction
		aUnitContainer - (None) Legacy code kept for compability
		"""
		Trigger.__init__( self, aCallFunction, someCallFunctionArguments ) #Run Trigger constructor
		
		self.myUnitIDs = []
		self.myAreas = []
		self.myPos = None
		self.myRadius = 0.0
		self.myHaveBeenInArea = 0

		try:
			self.myUnitIDs.extend( someUnits )
		except TypeError:
			self.myUnitIDs.append( someUnits )

		try:
			self.myAreas.extend( someAreas )
		except TypeError:
			self.myAreas.append( someAreas )

##		base.DebugMessage( "New TRG_UnitsInAreasAllIn created: %s" % self )


	def __str__( self ):
		""" Returns a short description of the trigger."""
		infoString = "\n<TRG_UnitsInAreasAllIn>"

		infoString = "%s\n\t<trackedUnits count='%d'>" % ( infoString, len( self.myUnitIDs ) )
		for unitId in self.myUnitIDs:
			infoString = "%s\n\t\tUnit id: %d" % ( infoString, unitId )
		infoString = "%s\n\t</trackedUnits>" % ( infoString )

		infoString = "%s\n\tCallFunctionName: %s" % ( infoString, self.myCallFunction.__name__ )

		infoString = "%s\n\t<callFunctionArguments count='%d'>" % ( infoString, len( self.myCallFunctionArguments ) )
		for argument in self.myCallFunctionArguments:
			infoString = "%s\n\t\tType: %s Value: %s" % ( infoString, type( argument ), argument )
		infoString = "%s\n\t</callFunctionArguments>" % ( infoString )

		infoString = "%s\n\t<areas count='%d'>" % ( infoString, len( self.myAreas ) )
		for area in self.myAreas:
			infoString = "%s\n\t\tPosition: %s Radius: %2.2f" % ( infoString, area.myPos, area.myRadius )
		infoString = "%s\n\t</areas>" % ( infoString )

		infoString = "%s\n</TRG_UnitsInAreasAllIn>" % infoString

		return infoString

	
	def GetInfoString( self ):
		""" Returns a short description of the trigger."""
		return self.__str__()


	def Update( self ):
		""" Checks if the units are within the area, if so calls myCallFunction.
		"""

		if self.myCallFunction is None:
			return -1

		# new stuff
		for uID in self.myUnitIDs[:]:
			unit = game.theGame.GetUnit( uID )
			if unit is None:
				self.myUnitIDs.remove( uID )

		units = []
		for i in self.myAreas:
			units.extend(game.theGame.GetUnitsInAreaXZ( i.myPos, i.myRadius ))

		for k in units:
			if k.myID in self.myUnitIDs[:]:
				self.myUnitIDs.remove(k.myID)
				self.myHaveBeenInArea = 1

		if  len(self.myUnitIDs) == 0 and self.myHaveBeenInArea == 1:
			base.DebugMessage( "TRG_UnitInAreaAllIn: Hit!" )
			self.Trigger()
			return 0

		if len( self.myUnitIDs ) == 0:
			#remove trigger..
			return 0

		return 1



class TRG_UnitsKilled( Trigger ):
	""" Releases when all units is killed ( Warning this trigger is probably more expensive than using onUnitsDestroyed.. )
	"""

	def __init__( self, someUnitIDs, aCallFunction, someCallFunctionArguments = None, aUnitContainer = None ):
		""" Constructor function.

		someUnitsIDs - (list) unitIDs in a list
		aCallFunction - (func) a function to call when the Event happens.
		someCallFunctionArguments - (list) list of arguments to aCallFunction
		aUnitContainer - (None) Legacy code kept for compability
		"""
		Trigger.__init__( self, aCallFunction, someCallFunctionArguments )
		self.myUnitIDs = []

		try:
			self.myUnitIDs.extend( someUnitIDs )
		except TypeError:
			self.myUnitIDs.append( someUnitIDs )

##		base.DebugMessage( "New TRG_UnitsKilled: %s" % self )


	def __str__( self ):
		""" Returns a short description of the trigger."""
		infoString = "\n<TRG_UnitsKilled>"

		infoString = "%s\n\t<trackedUnits count='%d'>" % ( infoString, len( self.myUnitIDs ) )
		for unitId in self.myUnitIDs:
			infoString = "%s\n\t\tUnit id: %d" % ( infoString, unitId )
		infoString = "%s\n\t</trackedUnits>" % ( infoString )

		infoString = "%s\n\tCallFunctionName: %s" % ( infoString, self.myCallFunction.__name__ )

		try:
			infoString = "%s\n\t<callFunctionArguments count='%d'>" % ( infoString, len( self.myCallFunctionArguments ) )
		except:
			pass
		for argument in self.myCallFunctionArguments:
			infoString = "%s\n\t\tType: %s Value: %s" % ( infoString, type( argument ), argument )
		infoString = "%s\n\t</callFunctionArguments>" % ( infoString )

		infoString = "%s\n</TRG_UnitsKilled>" % infoString

		return infoString

	
	def GetInfoString( self ):
		""" Returns a short description of the trigger."""
		return self.__str__()


	def Update( self ):
		""" Checks if the units are within the area, if so calls myCallFunction.
		"""
		
		if self.myCallFunction is None:
			return -1
		
		for uID in self.myUnitIDs[:]:
			unit = game.theGame.GetUnit( uID )
			if unit is None:
				self.myUnitIDs.remove( uID )
		
		if  len( self.myUnitIDs ) == 0:
			base.DebugMessage( "TRG_UnitsKilled: Hit!" )
			self.Trigger()
			return 0
		
		return 1
	


class TRG_Timer(Trigger):
	""" Releases at a certain time.
	"""

	def __init__( self, aReleaseTime, aCallFunction, someCallFunctionArguments = None ):
		""" Constructor function.

		aReleaseTime  - (float) an absolute time when trigger should release (preferably more than base.GetCurrentTime())
		aCallFunction - (func) a function to call when the Event happens.
		someCallFunctionArguments - (list) list of arguments to aCallFunction
		"""
		Trigger.__init__( self, aCallFunction, someCallFunctionArguments )
		self.myReleaseTime = aReleaseTime


	def GetInfoString( self ):
		""" Returns a short description of the trigger."""
		return "TRG_Timer releasetime: %2.2f" % (self.myReleaseTime)


	def Update( self ):
		""" Checks if the timer have passed myReleaseTime, if so calls myCallFunction.
		"""

		if self.myCallFunction is None:
			return -1

		# Check if trigger is done.
		if base.GetCurrentTime() > self.myReleaseTime:
			self.Trigger()
			return 0
		return 1


class TRG_Event( Trigger ):
	"""	Triggers when a given event is recieved
	"""

	def __init__( self, anEvent, aCallFunction, someCallFunctionArguments = None ):
		""" Constructor function.

		anEvent		 	- (str) Event name
		aCallFunction   - (func) a function to call when the Event happens.
		someCallFunctionArguments   - (list) list of arguments to aCallFunction
		"""
		Trigger.__init__( self, aCallFunction, someCallFunctionArguments )
		self.myEvent = anEvent
		self.myHaveTriggered = False


	def GetInfoString( self ):
		""" Returns a short description of the trigger.
		"""
		return "TRG_Event - event: %s" % ( self.myEvent )


	def CatchEvent( self, anEvent ):
		""" Trigger catches events, if triggered it will call myCallFunction on next update.

		anEvent - (str) Event name.
		"""

		if self.myEvent == anEvent:
			self.myHaveTriggered = True
			return 1
		return 0


	def Update( self ):
		""" Checks if the event have occurred, if so calls myCallFunction.
		"""

		if self.myCallFunction is None:											# myCallFunction undefined ...
			return -1															# ... return ERROR!

		if self.myHaveTriggered == True:										# Check if trigger is done.
			self.Trigger()
			return 0
		return 1


class TRG_MessageBoxClosed( Trigger ):
	"""	Triggers when a given event is recieved
	"""

	def __init__( self, aMessageBoxID, aCallFunction, someCallFunctionArguments = None ):
		""" Constructor function.

		aMessageBoxID	- (int) ID of messagebox to handle
		aCallFunction   - (func) a function to call when the Event happens.
		someCallFunctionArguments   - (list) list of arguments to aCallFunction
		"""
		Trigger.__init__( self, aCallFunction, someCallFunctionArguments )
		self.myMessageBoxID = aMessageBoxID
		self.myHaveTriggered = False


	def __str__( self ):
		""" Returns a short description of the trigger.
		"""
		return "TRG_Event - message box: %s" % ( self.myMessageBoxID )


	def GetInfoString( self ):
		""" Returns a short description of the trigger.
		"""
		return "TRG_Event - message box: %s" % ( self.myMessageBoxID )


	def MessageBoxClosed( self, aMessageBoxID ):
		""" Trigger catches events, if triggered it will call myCallFunction on next update.
		
		anEvent - (str) Event name.
		"""
		
		if self.myMessageBoxID == aMessageBoxID:
			self.myHaveTriggered = True
			return 1
		
		return 0


	def Update( self ):
		""" Checks if the event have occurred, if so calls myCallFunction.
		"""
		if self.myHaveTriggered == True:
			self.Trigger()
			return 0
		
		return 1


class TRG_UnitUnderAttack( Trigger ):
	"""	This trigger will trigger when a given unit is attacked
	"""

	def __init__( self, aUnitID, aCallFunction, someCallFunctionArguments = None ):
		"""	Constructor
		
		aUnitID						- (int) Unit to track for attack
		aCallFunction				- (function) Function to call on trigger
		someCallFunctionArguments	- (list) List of arguments to pass to callfunction
		"""
		Trigger.__init__( self, aCallFunction, someCallFunctionArguments )
		self.myTrackedUnitID = aUnitID
		self.myHaveTriggered = False
		
		wicg.TrackUnit( self.myTrackedUnitID )


	def __str__( self ):
		""" Extensive description of the trigger
		"""
		infoString = "\n<TRG_UnitUnderAttack>"
		
		infoString += "\n\tTrackedUnit: %d" % self.myTrackedUnitID
		
		infoString = "%s\n\tCallFunctionName: %s" % ( infoString, self.myCallFunction.__name__ )
		
		try:
			infoString = "%s\n\t<CallFunctionArguments count='%d'>" % ( infoString, len( self.myCallFunctionArguments ) )
			
			for argument in self.myCallFunctionArguments:
				infoString = "%s\n\t\tType: %s Value: %s" % ( infoString, type( argument ), argument )
			
			infoString = "%s\n\t</CallFunctionArguments>" % ( infoString )
		except TypeError:
			infoString = "%s\n\tCallFunctionArgument: %s" % ( infoString, self.myCallFunctionArguments )
		
		
		infoString = "%s\n</TriggerCombination>" % infoString
		
		return infoString


	def UnitUnderAttack( self, aUnitID ):
		"""	Checks weather it's time to trigger
		
		aUnitID	- (int) the attacked unit
		"""
		if self.myTrackedUnitID == aUnitID:
			self.myHaveTriggered = True
			
			return 1
		
		return 0


	def Update( self ):
		if self.myCallFunction is None:
			return -1
		
		if self.myHaveTriggered:
			self.Trigger()
			return 0
		
		return 1


class TriggerCombination( Trigger ):
	""" TriggerCombination class. Baseclass for trigger combinations like AND/OR
	triggers.
	"""

	def __init__( self, aTriggerContainer, aCallFunction, someCallFunctionArguments = None ):
		""" Initiates a TRG_ANDList.
		
		aTriggerContainer	-   (TriggerContainer) an instance of a TriggerContainer class. Usually 'theTriggers'.
		aCallFunction		-   (func) a function to call when the trigger triggers.
		someCallFunctionArguments		-   (list) a list of arguments to pass to the function
		"""
		Trigger.__init__( self, aCallFunction, someCallFunctionArguments )
		self.myTriggers = []
		self.myParentTriggerContainer = aTriggerContainer
		base.DebugMessage( self.__str__() )


	def __str__( self ):
		""" Returns an extensive description of the trigger
		"""
		infoString = "\n<TriggerCombination>"
		
		infoString = "%s\n\t<SubTriggers count='%d'>" % ( infoString, len( self.myTriggers ) )
		
		for subTrigger in self.myTriggers:
			infoString = "%s\n\t\tTrigger type: %s" % ( infoString, type( subTrigger ) )
		
		infoString = "%s\n\tCallFunctionName: %s" % ( infoString, self.myCallFunction.__name__ )
		
		try:
			infoString = "%s\n\t<CallFunctionArguments count='%d'>" % ( infoString, len( self.myCallFunctionArguments ) )
			
			for argument in self.myCallFunctionArguments:
				infoString = "%s\n\t\tType: %s Value: %s" % ( infoString, type( argument ), argument )
			
			infoString = "%s\n\t</CallFunctionArguments>" % ( infoString )
		except TypeError:
			infoString = "%s\n\tCallFunctionArgument: %s" % ( infoString, self.myCallFunctionArguments )
		
		infoString = "%s\n</TriggerCombination>" % infoString
		
		return infoString


	def GetInfoString( self ):
		""" Returns a short description of the trigger.
		"""
		return "TriggerCombination baseclass"


	def Add( self, aTrigger ):
		""" Adds a trigger needed to trigger the TRG_ANDList
		"""
		self.myTriggers.append( aTrigger )
		base.DebugMessage( "Trigger added to TriggerCombination:\n%s" % aTrigger )


	def Remove( self, aTrigger ):
		""" Removes a trigger from the TRG_ANDList
		"""
		try:
			self.myTriggers.remove( aTrigger )
		except ValueError:
			pass


	def Update( self ):
		""" Dummy function
		"""
		return 0


class TRG_ANDList( TriggerCombination ):
	""" TRG_ANDList class. A trigger that activates when ALL triggers in a given
	set of other triggers have triggered. All triggers in the list have to
	be triggered or removed from the global triggerlist before the trigger
	triggers
	"""

	def GetInfoString( self ):
		""" Returns a short description of the trigger.
		"""
		return "TRG_ANDList - Number of childtriggers:" % ( len( self.myTriggers ) )


	def Update( self ):
		""" Checks if it's time to trigger
		"""
		for trigger in self.myTriggers:
			if not trigger in self.myParentTriggerContainer.myTriggers:
				try:
					self.myTriggers.remove( trigger )
				except ValueError:
					pass
		
		if not len( self.myTriggers ):
			self.Trigger()
			
			return 0
		
		return 1


class TRG_ORList( TriggerCombination ):
	""" TRG_ORList class. A trigger that activates when ANY trigger in a given
		set of other triggers have triggered. All triggers in the list have to
		be triggered or removed from the global triggerlist before the trigger
		triggers
	"""

	def GetInfoString( self ):
		""" Returns a short description of the trigger.
		"""
		return "TRG_ORList - Number of childtriggers:" % ( len( self.myTriggers ) )


	def Update( self ):
		""" Checks if it's time to trigger
		"""
		for trigger in self.myTriggers:
			if trigger not in self.myParentTriggerContainer.myTriggers:
				if trigger.IsTriggered():
					self.myIsTriggered = True
					self.Trigger()
				
				try:
					self.myTriggers.remove( trigger )
				except ValueError:
					pass
		
		if self.IsTriggered():
			for trigger in self.myTriggers:
				self.myTriggers.remove( trigger )
			
			return 0
		
		elif not len( self.myTriggers ):										# No point in updating an empty list
			try:
				self.myParentTriggerContainer.myTriggers.remove( self )
			except ValueError:
				pass
		
		return 1


class Triggers( object ):
	""" TriggerContaner class. Used as a containerclass (all triggers should be
	added here) and to update contained Triggers.
	"""

	def __init__( self, anIgnoredArgument = None ):
		""" Inits the triggercontainer.
		"""
		self.myStartTrigger	= 0
		self.myTriggers		= []
	
	
	def SyncTime( self, aDeltaTime ):
		"""
		"""
		for trigger in self.myTriggers:
			if type( trigger ) == TRG_Timer:
				trigger.myReleaseTime += aDeltaTime


	def Add( self, aTrigger ):
		""" Adds a trigger to the triggerlist to be evaluated later on.
		
		aTrigger	 - (Trigger) a trigger object
		"""
		self.myTriggers.append( aTrigger )
		debug.DebugMessage(
			"Trigger added to theTriggers:\n%s" % aTrigger,
			debug.EXCESSIVE )

	
	def Purge( self ):
		""" Clears all triggers
		"""
		self.myTriggers.clear()


	def Remove(  self, aTrigger ):
		""" Adds a trigger to the triggerlist to be evaluated later on.
		
		aTrigger	 - (Trigger) a trigger object
		"""
		try:
			self.myTriggers.remove( aTrigger )
		except ValueError:
			pass


	def ThrowEvent( self, anEvent ):
		""" Throws an event.
		
		If the event gets thrown in a server script, the event will be thrown to
		all players client side scripts as well. The event is sent to the clients
		before it's parsed in the server script.
		
		anEvent - (str) Event name
		"""
		
		wicg.ThrowEvent( anEvent );
		self.CatchEvent( anEvent );


	def ThrowEventToPlayer( self, aPlayer, anEvent ):
		""" Throws an event to a specific player (1-16). This event will ONLY be
		parsed in a client script.

		aPlayer - (int) recipient
		anEvent - (str) the event
		"""

		wicg.ThrowEventToPlayer( aPlayer, anEvent );


	def Count( self ):
		""" Returns the number of triggers in the container
		"""
		return len( self.myTriggers )


	def CatchEvent( self, anEvent ):
		""" CatchEvent(anEvent) is called on all triggers in the contaner.
		
		anEvent - (str) Event name
		"""
		
		num = 0
		
		for t in self.myTriggers:
			num += t.CatchEvent( anEvent )
		
		return num


	def MessageBoxClosed( self, aMessageBoxID ):
		"""	CloseMessageBox is called on all triggers in the container
		
		aMessageBoxID	- (int) ID of closed message box
		"""
		
		num = 0
		
		for trigger in self.myTriggers:
			try:
				num += trigger.MessageBoxClosed( aMessageBoxID )
			except AttributeError:
				pass
		
		return num


	def UnitUnderAttack( self, aUnitID ):
		"""	UnitUnderAttack is called on all triggers in the container
		
		aUnitID	- (int) ID of attacked unit
		"""
		
		num = 0
		
		for trigger in self.myTriggers:
			try:
				num += trigger.UnitUnderAttack( aUnitID )
			except AttributeError:
				pass
		
		if num:
			wicg.UnTrackUnit( aUnitID )
		
		return num


	def Update( self ):
		""" Calls Update() on all triggers in the container. If a trigger is
		'finished' (by returning something less than 1) it's removed from the
		trigger list.
		"""
		num = int( ( len( self.myTriggers ) * base.GetElapsedTime() ) + 0.5 )
		
		if num < 1:
			num = 1
		
		f = self.myTriggers[self.myStartTrigger:self.myStartTrigger+num]
		
		while len(f) > 0:
			t = f.pop()
			ret = t.Update()
			
			if ret < 0:
				debug.DebugMessage(
					"TriggerContainer::Update() - Error updating trigger (%s)." % ( t.GetInfoString() ),
					debug.BRIEF )
				
				try:
					self.myTriggers.remove(t)
					
				except ValueError:
					pass
				
			elif ret == 0:
				base.DebugMessage( "A %s-trigger triggered:\n%s" % ( type( t ), t ) )
				t.myIsTriggered = True
				
				try:
					self.myTriggers.remove(t)
					
				except ValueError:
					pass
		
		self.myStartTrigger += num
		
		if self.myStartTrigger >= len(self.myTriggers):
			self.myStartTrigger = 0
		
		return len(self.myTriggers)


TriggerContainer = Triggers
theTriggers = Triggers()
