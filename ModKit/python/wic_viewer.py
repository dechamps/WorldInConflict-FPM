""" This module if for debug purposes only. """

from serverimports import *


KEY_NONE 	= 0
KEY_UP		= 200
KEY_DOWN	= 208
KEY_LEFT	= 203
KEY_RIGHT	= 205
KEY_ENTER	= 28
KEY_PAGEUP	= 201
KEY_PAGEDOWN	= 209
KEY_HOME	= 199

MOUSE_LBUTTON = 0
MOUSE_RBUTTON = 1
MOUSE_MBUTTON = 2


READ_LINE_SIZE = 256

DEFAULT_COLOR		= 0xdddd00
MARKED_COLOR		= 0xff1111
SCREEN_MARKER_COLOR	= 0x11ee11
HEADLINE_COLOR		= 0x445544
TEXT_HEIGHT 	= 0.015
HEADLINE_HEIGHT = 0.02

DEFAULT_REMOVE_DELAY = 4.0

startPosition 		= Position( 0.02, 0.10, 0.0 )
currentPositionX 	= 0.0
currentPositionY 	= 0.0
headLinePositionX 	= 0.005
expansionWidth		= 0.015

isActive = False
theEntries = []
theExpanded = []
currentLevel = 0
currentEntry = 0
currentPrintOffset = 0

theCommands = []
theWatches = []
theStrings = []


doRender = True

theEditedAreas = []
theEditedCommandpoints = []

selectedArea = GenericValue( None )

mouseStartPosX = 0.021263
mouseStartPosY = (0.051154 * 2)
#0.153461
mouseTextWidth = 0.2
mouseTextHeight = 0.015

cursorPosLeft = None
cursorPosRight = None

leftMouseDown = False
rightMouseDown = False

nextStepDown = 0.0
nextStepUp = 0.0
firstStepDown = True
firstStepUp = True

lastMousePressedTime = 0.0
mouseSens = 0.08



class CiviliansEntry( object ):
	
	
	def __init__( self, aName = None ):
		global civDefaultRadius
		global civDefaultLifeTime
		global civDefaultNumberOfCivilians
		global civDefaultDelay
		global civDefaultY

		self.myName = aName
		self.myStartPosition = None
		self.myDirection = None
		self.myCivilians = []
		self.myRadius = civDefaultRadius
		self.myLifeTime = civDefaultLifeTime
		self.myNumberOfCivilians = civDefaultNumberOfCivilians
		self.myDelay = civDefaultDelay
		self.myY = civDefaultY
		
	
	
	def AddCivilian( self, aCivType ):
		
		if aCivType[1]:
			self.myCivilians.append( aCivType[0] )
		else:
			if aCivType[0] in self.myCivilians:
				self.myCivilians.remove( aCivType[0] )
	
	def SetLifeTime( self, aLifeTime ):
		
		self.myLifeTime = aLifeTime
		
	
	def SetRadius( self, aRadius ):
		
		self.myRadius = aRadius
		
	
	def SetNumberOfCivilians( self, aNrOfCivs ):
		
		self.myNumberOfCivilians = aNrOfCivs
		
	
	def SetDelay( self, aDelay ):
		
		self.myDelay = aDelay
	
	def SetY( self, aY ):
		
		self.myY = aY

	
	def SetEntryStart( self ):
	
		import wicp
	
		p = wicp.MouseToWorld()
		
		if p:
			self.myStartPosition = p
	
			
	def SetEntryDirection( self ):
	
		import wicp
	
		p = wicp.MouseToWorld()
		
		if p:
			self.myDirection = p


def VerifyCivBatch( batch ):
	global theCivilians
	
	if len( batch.myCivilians ) == 0:
		return 'No Civilians added'
	
	for c in batch.myCivilians:
		if c.myStartPosition == None:
			return 'No StartPosition in %s' % (c.myName)
		if c.myDirection == None:
			return 'No Direction in %s' % (c.myName)
		if len(c.myCivilians) == 0:
			return 'No Civilians added in %s' % (c.myName)
		if c.myNumberOfCivilians < 2:
			return 'NumberOfCivilians < 1'
	
	return 'All Ok'	


class CiviliansBatch( object ):
	
	def __init__( self, aName = None ):
		global civDefaultRadius
		global civDefaultLifeTime
		global civDefaultNumberOfCivilians
		global civDefaultDelay

		self.myName = aName
		self.myCivilians = []
		self.myGenericModelIds = []
		self.myDelayReactions = []
		
		##default stuff
		self.myDefaultRadius = civDefaultRadius
		self.myDefaultLifeTime = civDefaultLifeTime
		self.myDefaultNumberOfCivilians = civDefaultNumberOfCivilians
		self.myDefaultDelay = civDefaultDelay
		self.myDefaultY = civDefaultY

	
	def SetDefaultRadius( self, value ):
		self.myDefaultRadius = value

	def SetDefaultLifeTime( self, value ):
		self.myDefaultLifeTime = value

	def SetDefaultNumberOfCivilians( self, value ):
		self.myDefaultNumberOfCivilians = value

	def SetDefaultDelay( self, value ):
		self.myDefaultDelay = value

	def SetDefaultY( self, value ):
		self.myDefaultY = value
	
	
	def ApplyRadiusToAll( self, value ):
		for civ in self.myCivilians:
			civ.myRadius = value
			
	def ApplyLifeTimeToAll( self, value ):
		for civ in self.myCivilians:
			civ.myLifeTime = value
	
	def ApplyNumberOfCiviliansToAll( self, value ):
		for civ in self.myCivilians:
			civ.myNumberOfCivilians = value
	
	def ApplyDelayToAll( self, value ):
		for civ in self.myCivilians:
			civ.myDelay = value
	def ApplyYToAll( self, value ):
		for civ in self.myCivilians:
			civ.myY = value
	
	def Play( self ):
		
		from wicgame.civilians import SpawnCiviliansInClump
		
		if VerifyCivBatch( self ) != 'All Ok':
			return
		
		for civ in self.myCivilians:
			if civ.myDelay > 0:
				import serverimports as si
				self.myDelayReactions.append( si.Delay( civ.myDelay, si.Action( self.SpawnCivEntry, civ ) ) )
			else:
				self.SpawnCivEntry( civ )
	
	
	def SpawnCivEntry( self, aCivEntry ):
		from wicgame.civilians import SpawnCiviliansInClump
		
		startPos = GetCopy( aCivEntry.myStartPosition )
		direction = GetCopy( aCivEntry.myDirection )
		
		if aCivEntry.myY != 0.0:
			startPos.myY = aCivEntry.myY
			direction.myY = aCivEntry.myY
		
		self.myGenericModelIds.extend( SpawnCiviliansInClump( startPos, direction, aCivEntry.myNumberOfCivilians, aCivEntry.myLifeTime, aCivEntry.myCivilians, aCivEntry.myRadius ) )
		
			
	def Stop( self ):
		
		import serverimports as si
		
		for react in self.myDelayReactions:
			si.RemoveReaction( react )
			
		self.myDelayReactions = []
		
		for genmod_id in self.myGenericModelIds:
			si.thePlayers[ si.PLAYER_HUMAN ].DeleteGenericModel( genmod_id )
		
		self.myGenericModelIds = []
		


theCivilians = []
civDefaultRadius = 6
civDefaultLifeTime = 60
civDefaultNumberOfCivilians = 1
civDefaultDelay = 0
civDefaultY = 0.0

def SetDefaultRadius( value ):
	global civDefaultRadius
	civDefaultRadius = value

def SetDefaultLifeTime( value ):
	global civDefaultLifeTime
	civDefaultLifeTime = value

def SetDefaultNumberOfCivilians( value ):
	global civDefaultNumberOfCivilians
	civDefaultNumberOfCivilians = value

def SetDefaultDelay( value ):
	global civDefaultDelay
	civDefaultDelay = value

def SetDefaultY( value ):
	global civDefaultY
	civDefaultY = value


def PlayAllCivBatches():
	global theCivilians
	
	for civ in theCivilians:
		civ.Play()


def StopAllCivBatches():
	global theCivilians
	
	for i in range(60480):
		try:
			thePlayers[PLAYER_HUMAN].DeleteGenericModel(i)
		except Exception:
			continue
	
	#for civ in theCivilians:
	#	civ.Stop()


def RemoveCivBatch( batch ):
	global theCivilians
	
	if batch in theCivilians:
		theCivilians.remove( batch )
		

def RemoveCivEntry( batch, entry ):
	
	if entry in batch.myCivilians:
		batch.myCivilians.remove( entry )


def SaveCivilians():
	global theCivilians
	global civDefaultRadius
	global civDefaultLifeTime
	global civDefaultNumberOfCivilians
	global civDefaultDelay
	global civDefaultY
	import wicg

	try:
		f = file( 'maps\\%s_saved_civilians.foo' % wicg.GetMapName(), 'w')
	except IOError:
		return

	##default stuff
	f.write( '%f\n' % civDefaultRadius )
	f.write( '%f\n' % civDefaultLifeTime )
	f.write( '%d\n' % civDefaultNumberOfCivilians )
	f.write( '%f\n' % civDefaultDelay )
	f.write( '%f\n' % civDefaultY )


	f.write( '%d\n' % len(theCivilians) )

	for civ in theCivilians:
		f.write('<CIVILIANBATCH>\n')
		f.write('%s\n' % civ.myName)
		
		##defaults
		f.write('%f\n' % civ.myDefaultRadius)
		f.write('%f\n' % civ.myDefaultLifeTime)
		f.write('%d\n' % civ.myDefaultNumberOfCivilians)
		f.write('%f\n' % civ.myDefaultDelay)
		f.write('%f\n' % civ.myDefaultY)
		
		
		
		f.write( '%d\n' % len( civ.myCivilians ) )
		
		for civ_entry in civ.myCivilians:
			f.write('<CIVILIANENTRY>\n')
			
			f.write('%s\n' % civ_entry.myName)
			
			if civ_entry.myStartPosition is None:
				f.write('None\n')
			else:
				f.write('%f\n' % civ_entry.myStartPosition.myX)
				f.write('%f\n' % civ_entry.myStartPosition.myY)
				f.write('%f\n' % civ_entry.myStartPosition.myZ)
			
			if civ_entry.myDirection is None:
				f.write('None\n')
			else:			
				f.write('%f\n' % civ_entry.myDirection.myX)
				f.write('%f\n' % civ_entry.myDirection.myY)
				f.write('%f\n' % civ_entry.myDirection.myZ)
			
			f.write( '%d\n' % len( civ_entry.myCivilians ) )
			
			for c in civ_entry.myCivilians:
				f.write( '<CIVILIAN>\n' )
				f.write( '%s\n' % c )
				f.write( '</CIVILIAN>\n' )
			
			f.write( '%f\n' % civ_entry.myRadius )
			f.write( '%f\n' % civ_entry.myLifeTime )
			f.write( '%d\n' % civ_entry.myNumberOfCivilians )
			f.write( '%f\n' % civ_entry.myDelay )
			
			f.write('</CIVILIANENTRY>\n')
		
		f.write('</CIVILIANBATCH>\n')

	
	f.close()
	
	try:
		f = file( 'maps\\%s_saved_civilians.py' % wicg.GetMapName(), 'w')
	except IOError:
		return
	
	nr = 0
	for civ in theCivilians:
		f.write('def CivBatch%d():\n' % nr)
		
		auto_delay = 0.0
		for c in civ.myCivilians:
		
			if c.myStartPosition is None or c.myDirection is None:
				continue
			
			startPos = c.myStartPosition
			direction = c.myDirection
			
			if c.myY != 0.0:
				startPos.myY = c.myY
				direction.myY = c.myY

			if c.myDelay > 0.0:
				f.write( '\tDelay( %f, Action( SpawnCiviliansInClump, Position( %s ), Position( %s ), %d, %f, [' % ( c.myDelay, startPos, direction, c.myNumberOfCivilians, c.myLifeTime) )
			else:
				f.write( '\tSpawnCiviliansInClump( Position( %s), Position( %s ), %d, %f, [' % (startPos, direction, c.myNumberOfCivilians, c.myLifeTime) )
			
			c_nr = 0
			for civType in c.myCivilians:
				c_nr += 1
				if c_nr < len( c.myCivilians ):
					f.write( '\'%s\',' % civType )
				else:
					f.write( '\'%s\'' % civType )

			if c.myDelay > 0.0:
				f.write( '], %f ) )\n' % c.myRadius )
			else:
				f.write( '], %f )\n' % c.myRadius )
		
		f.write( '\n')
		
		nr += 1
	
	f.close()


def LoadCivilians():
	global theCivilians
	global civDefaultRadius
	global civDefaultLifeTime
	global civDefaultNumberOfCivilians
	global civDefaultDelay
	global civDefaultY

	import wicg

	try:
		f = file( 'maps\\%s_saved_civilians.foo' % wicg.GetMapName(), 'r')
	except IOError:
		return

	theCivilians = []

	line = f.readline(READ_LINE_SIZE)
	civDefaultRadius = float(line)
	line = f.readline(READ_LINE_SIZE)
	civDefaultLifeTime = float(line)
	line = f.readline(READ_LINE_SIZE)
	civDefaultNumberOfCivilians = int(line)
	line = f.readline(READ_LINE_SIZE)
	civDefaultDelay = float(line)
	line = f.readline(READ_LINE_SIZE)
	civDefaultY = float(line)


	line = f.readline(READ_LINE_SIZE)
	nrOfBatches = int(line)

	for i in range(nrOfBatches):
		
		##<CIVILIANBATCH>
		line = f.readline(READ_LINE_SIZE)
		
		## NAME
		line = f.readline(READ_LINE_SIZE)
		batchName = line.rstrip('\n')
		
		##default stuff
		line = f.readline(READ_LINE_SIZE)
		defaultRadius = float(line)
		line = f.readline(READ_LINE_SIZE)
		defaultLifeTime = float(line)
		line = f.readline(READ_LINE_SIZE)
		defaultNumberOfCivilians = float(line)
		line = f.readline(READ_LINE_SIZE)
		defaultDelay = float(line)
		line = f.readline(READ_LINE_SIZE)
		defaultY = float(line)


		## NR OF ENTRIES
		line = f.readline(READ_LINE_SIZE)
		nrOfEntries = int(line)
		
		newBatch = CiviliansBatch(batchName)
		newBatch.myDefaultRadius = defaultRadius
		newBatch.myDefaultLifeTime = defaultLifeTime
		newBatch.myDefaultNumberOfCivilians = defaultNumberOfCivilians
		newBatch.myDefaultDelay = defaultDelay
		
		for i in range( nrOfEntries ):
			##<CIVILIANENTRY>
			line = f.readline(READ_LINE_SIZE)
			
			line = f.readline(READ_LINE_SIZE)
			entryName = line.rstrip( '\n' )
			
			newEntry = CiviliansEntry( entryName )
						
			##start position			
			startPosition = Position()
			line = f.readline(READ_LINE_SIZE)
			
			if line.rfind('None') != -1:
				startPosition = None
			else:				
				startPosition.myX = float(line)
				line = f.readline(READ_LINE_SIZE)
				startPosition.myY = float(line)
				line = f.readline(READ_LINE_SIZE)
				startPosition.myZ = float(line)
			
			newEntry.myStartPosition = startPosition
			
			## direction	
			direction = Position()
			line = f.readline(READ_LINE_SIZE)
			
			if line.rfind('None') != -1:
				direction = None
			else:
				direction.myX = float(line)
				line = f.readline(READ_LINE_SIZE)
				direction.myY = float(line)
				line = f.readline(READ_LINE_SIZE)
				direction.myZ = float(line)
						
			newEntry.myDirection = direction
			
			##NR OF CIVILIANS
			line = f.readline(READ_LINE_SIZE)
			nrOfCivilians = int(line)
			
			for g in range( nrOfCivilians ):
				##<CIVILIAN>
				line = f.readline(READ_LINE_SIZE)
				
				##civilian
				line = f.readline(READ_LINE_SIZE)
				
				civilian = line.rstrip('\n')
				newEntry.myCivilians.append( civilian )

				##</CIVILIAN>
				line = f.readline(READ_LINE_SIZE)
				
			line = f.readline(READ_LINE_SIZE)
			newEntry.myRadius = float(line)
			line = f.readline(READ_LINE_SIZE)
			newEntry.myLifeTime = float(line)
			line = f.readline(READ_LINE_SIZE)
			newEntry.myNumberOfCivilians = int(line)
			line = f.readline(READ_LINE_SIZE)
			newEntry.myDelay = float(line)

			##</CIVILIANENTRY>
			line = f.readline(READ_LINE_SIZE)

			newBatch.myCivilians.append( newEntry )
					
		##</CIVILIANBATCH>
		line = f.readline(READ_LINE_SIZE)
		
		theCivilians.append( newBatch )

	f.close()

def CreateNewCivilianBatch( ):
	
	theCivilians.append( CiviliansBatch( 'CivBatch_%d' % len(theCivilians) ) )
	

def CreateNewCivEntry( civBatch ):
	
	newEntry = CiviliansEntry( 'Civ_%d' % len( civBatch.myCivilians ) )
	newEntry.myRadius = civBatch.myDefaultRadius
	newEntry.myLifeTime = civBatch.myDefaultLifeTime
	newEntry.myNumberOfCivilians = civBatch.myDefaultNumberOfCivilians
	newEntry.myDelay = civBatch.myDefaultDelay
	civBatch.myCivilians.append( newEntry )
	return newEntry


def CopyCivEntryToMouse( batch, civentry ):
	import wicp
	
	if civentry.myStartPosition is None or civentry.myDirection is None:
		return
	
	newEntry = CreateNewCivEntry( batch )

	p = wicp.MouseToWorld()
	if p:
		newEntry.myStartPosition = GetCopy(p)
		offset = civentry.myDirection - civentry.myStartPosition
		newEntry.myDirection = newEntry.myStartPosition + offset
		newEntry.myCivilians = []
		newEntry.myCivilians.extend( civentry.myCivilians )
		newEntry.myRadius = civentry.myRadius
		newEntry.myDelay = civentry.myDelay
		newEntry.myLifeTime = civentry.myLifeTime
		newEntry.myY = civentry.myY
		newEntry.myNumberOfCivilians = civentry.myNumberOfCivilians


def CopyCivBatchToMouse( batch ):
	import wicp
	
	pass
	

def SpawnPreviewCiv( aCiv ):
	import wicp
		
	p = wicp.MouseToWorld()
	if p:
		thePlayers[ PLAYER_HUMAN ].CreateGenericModel( aCiv, p, 6, p + Position( 1, 0, 0 ) )



useAutoGroupSelection = GenericValue( True )
lastAutoSelectedGroup = ''

useAutoGroupNameView = GenericValue( True )

showCommands = GenericValue( False )
showWatches = GenericValue( False )
showStrings = GenericValue( False )
showObjectiveCamera = GenericValue( True )
showSystemInfo = GenericValue( True )
showGroups = GenericValue( False )
showReactions = GenericValue( False )
showActionQueues = GenericValue( True )
showInstances = GenericValue( False )
showAreas = GenericValue( False )
showUnits = GenericValue( True )
showPlatoons = GenericValue( True )
showAI = GenericValue( False )
showServerplay = GenericValue( False )
showClient = GenericValue( False )
showServer = GenericValue( False )
showAreaEditor = GenericValue( True )
showCiviliansEditor = GenericValue( True )
showHighCivilians = GenericValue( False )
showRoofCivilians = GenericValue( False )
showGroundCivilians = GenericValue( True )

theSettings = { 'showCommands' : showCommands, 'showWatches' : showWatches, 'showStrings' : showStrings, 'showObjectiveCamera' : showObjectiveCamera,\
		 'showSystemInfo' : showSystemInfo, 'showGroups' : showGroups, 'showReactions' : showReactions, 'showActionQueues' : showActionQueues,\
		 'showInstances' : showInstances, 'showAreas' : showAreas, 'showUnits' : showUnits, 'showPlatoons' : showPlatoons, 'showAI' : showAI,\
		 'showServerplay' : showServerplay, 'showClient' : showClient, 'showServer' : showServer, 'showAreaEditor' : showAreaEditor,\
		 'useAutoGroupNameView': useAutoGroupNameView, 'useAutoGroupSelection' : useAutoGroupSelection, 'showCiviliansEditor' : showCiviliansEditor,\
		 'showHighCivilians' : showHighCivilians, 'showRoofCivilians' : showRoofCivilians, 'showGroundCivilians' : showGroundCivilians }


reactUpdate = None


def SaveSettings():
	global theSettings

	f = file( 'wic_viewer_settings.foo', 'w' )
	
	if not f:
		return
	
	f.write('%d\n' % len( theSettings ))
	
	for setting in theSettings:
		f.write('%s\n%d\n' % (setting, theSettings[setting].Get()))
	
	f.close()

def LoadSettings():
	global theSettings
	
	try:
		f = file( 'wic_viewer_settings.foo', 'r' )
	except IOError:
		return

	nrOfSettings = int(f.readline(READ_LINE_SIZE))
	
	for i in range( nrOfSettings ):
		setting = f.readline(READ_LINE_SIZE)
		setting = setting.rstrip('\n')
		flag = int(f.readline(READ_LINE_SIZE))
		theSettings[setting].Set(flag)
		
	f.close()


## edit areas stuff

class EditorArea( object ):
	
	def __init__( self, aName, aPosition, aRadius ):
		
		self.myName = aName
		self.myPos = aPosition
		self.myRadius = aRadius
	
	
	def SetRadius( self, aNewRadius ):
		
		self.myRadius = aNewRadius
	

def AddNewArea():
	global theEditedAreas
	import wicp
	
	p = wicp.MouseToWorld()
	
	if not p is None:
		theEditedAreas.append( EditorArea( 'Area__%d' % len( theEditedAreas ), p, 0.0 ) )


def UpdateArea( anArea ):
	import wicp
	
	p = wicp.MouseToWorld()
	anArea.myPos = p
	

def UpdateSelectedArea( ):
	global selectedArea
	global theEditedAreas
	
	if selectedArea.Get() != -1:
		UpdateArea( theEditedAreas[ selectedArea.Get() ] )

def SaveAreas():
	global theEditedAreas
	
	filePath = 'maps\\%s_saved_areas.foo' % wicg.GetMapName()
	
	try:
		f = file( filePath, 'w')
	except IOError:
		return
	
	f.write('%d\n' % len( theEditedAreas ) )
	
	for area in theEditedAreas:
		f.write('<AREA>\n')
		f.write('%s\n' % area.myName)
		f.write('%f\n' % area.myPos.myX)
		f.write('%f\n' % area.myPos.myY)
		f.write('%f\n' % area.myPos.myZ)
		f.write('%f\n' % area.myRadius)
		f.write('<\AREA>\n')
	
	f.close()
	
	filePath = 'maps\\%s_saved_areas.txt' % wicg.GetMapName()
	
	f = file( filePath, 'w')

	for area in theEditedAreas:
		f.write('Position( %.3f, %.3f, %.3f ) ## %s\n' % (area.myPos.myX, area.myPos.myY, area.myPos.myZ, area.myName) )

	for area in theEditedAreas:
		f.write('Area( Position( %.3f, %.3f, %.3f ), %.3f ) ## %s\n' % (area.myPos.myX, area.myPos.myY, area.myPos.myZ, area.myRadius, area.myName) )
		
	f.write('\n\n')
	
	for area in theEditedAreas:
		f.write('WicedAreaInstance %s\n' % area.myName)
		f.write('{\n')
		f.write('\tmyPosition\n')
		f.write('\t{\n')
		f.write('\t\tmyX %f\n' % area.myPos.myX)
		f.write('\t\tmyY %f\n' % area.myPos.myY)
		f.write('\t\tmyZ %f\n' % area.myPos.myZ)
		f.write('\t}\n')
		f.write('\n')
		f.write('\tmyRadius %f\n' % area.myRadius)
		f.write('\tmyLockedFlag 0\n')
		f.write('\tmyWarnedFlag 0\n')
		f.write('}\n')
		f.write('\n')

	f.close()
	

def LoadAreas():
	global theEditedAreas

	filePath = filePath = 'maps\\%s_saved_areas.foo' % wicg.GetMapName()
	
	try:
		f = file( filePath, 'r' )
	except IOError:
		return
	
	if not f:
		return
		
	theEditedAreas = []
	
	line = f.readline(READ_LINE_SIZE)
	DebugMessage( 'LoadAreas:: %s' %line )
	nrOfAreas = int(line)
	
	for i in range( nrOfAreas ):
		## <AREA>
		line = f.readline(READ_LINE_SIZE)
		
		
		## NAME
		line = f.readline(READ_LINE_SIZE)
		name = line.rstrip('\n')
		
		
		## X
		line = f.readline(READ_LINE_SIZE)
		x = float(line)
		
		
		## Y
		line = f.readline(READ_LINE_SIZE)
		y = float(line)
		
		
		## Z
		line = f.readline(READ_LINE_SIZE)
		z = float(line)
		
		
		## RADIUS
		line = f.readline(READ_LINE_SIZE)
		radius = float(line)
		
		
		## </AREA>
		line = f.readline(READ_LINE_SIZE)
		
		
		theEditedAreas.append( EditorArea( name, Position( x, y, z ), radius ) )
		
	f.close()


def AddNewCommandPoint():
	global theEditedCommandpoints
	import wicp
	pass


def SaveCommandPoints():
	global theEditedCommandpoints
	import wicp
	pass

## objective camera stuff
theObjectiveCameras = []


def AddObjectiveCamera():
	try:
		import camera.objectivecamera as oc
	except Exception:
		return
	global theObjectiveCameras
	theObjectiveCameras.append( oc.ObjectiveCameraEx( 'ObjCam%d' % len( theObjectiveCameras ) ) )



def SaveObjectiveCameras():
	global theObjectiveCameras
	
	filePath = 'maps\\%s_saved_objectivecameras.foo' % wicg.GetMapName()
	
	try:
		f = file( filePath, 'w' )
	except IOError:
		return
	
	f.write('%d\n' % len( theObjectiveCameras ) )
	for cam in theObjectiveCameras:
		f.write('<OBJ_CAM>\n')
		f.write('%s\n' % cam.myName)
		f.write('%f\n' % cam.myEndDelayTime)
		f.write('%f\n' % cam.myCameraMaxSpeed)
		f.write('%f\n' % cam.myCameraMaxAcceleration)
		f.write('%d\n' % cam.GetUseEndGrab())
		f.write('%d\n' % len(cam.myPoints))
		
		for p in cam.myPoints:
			f.write('<POINT>\n')
			f.write('%f\n' % p.myMoveToTarget.myX )
			f.write('%f\n' % p.myMoveToTarget.myY )
			f.write('%f\n' % p.myMoveToTarget.myZ )
			
			f.write('%f\n' % p.myLookAtTarget.myX )
			f.write('%f\n' % p.myLookAtTarget.myY )
			f.write('%f\n' % p.myLookAtTarget.myZ )

			f.write('%f\n' % p.myDelayTime )
			f.write('%f\n' % p.myCloseToLimit )
			
			f.write('%d\n' % p.myUseGoToNow )
			f.write('%d\n' % p.myUseLookAtNow )
			
			f.write( '<\POINT>\n' )
		
		f.write('</OBJ_CAM>\n')
	
	f.close()
	
	filePath = 'maps\\%s_saved_objectivecameras.py' % wicg.GetMapName()
	
	f = file( filePath, 'w' )
	
	
	for cam in theObjectiveCameras:
		f.write('def %sCamera( aIsBrowserCamera = True ):\n' % cam.myName)
		f.write('\t%s = ObjectiveCameraEx( \'%s\', aIsBrowserCamera )\n' % (cam.myName, cam.myName) )
		
		for p in cam.myPoints:
			f.write('\tp = %s.AddPoint( Position(%.3f, %.3f, %.3f), Position(%.3f, %.3f, %.3f), %.3f, %.3f )\n' % (cam.myName,\
			p.myMoveToTarget.myX, p.myMoveToTarget.myY, p.myMoveToTarget.myZ,\
			p.myLookAtTarget.myX, p.myLookAtTarget.myY, p.myLookAtTarget.myZ,\
			p.myDelayTime, p.myCloseToLimit))
			
			if p.myUseGoToNow:
				f.write('\tp.SetGoToNow( True )\n')
			if p.myUseLookAtNow:
				f.write('\tp.SetLookAtNow( True )\n')
				
		f.write('\t%s.SetEndDelayTime( %.3f )\n' % (cam.myName, cam.myEndDelayTime ))
		
		
		#f.write('\t%s.SetCameraType( %s )\n' % (cam.myCameraType.__class__.__name__() ))
		f.write('\t%s.SetCameraMaxSpeed( %.3f )\n' % (cam.myName, cam.myCameraMaxSpeed ))
		f.write('\t%s.SetCameraMaxAcceleration( %.3f )\n' % (cam.myName, cam.myCameraMaxAcceleration ))
		f.write('\t%s.UseEndGrab( %s )\n' % ( cam.myName, cam.GetUseEndGrab() ))
		
		f.write( '\t%s.Play()\n' % cam.myName)
		
		f.write( '\treturn %s\n' % cam.myName)
		
		f.write('\n\n')
			
	

def LoadObjectiveCameras():
	global theObjectiveCameras
	import camera.objectivecamera as oc
	
	filePath = 'maps\\%s_saved_objectivecameras.foo' % wicg.GetMapName()
	
	try:
		f = file( filePath, 'r' )
	except IOError:
		return
	
	if not f:
		return
		
	theObjectiveCameras = []
	
	line = f.readline(READ_LINE_SIZE)
	nrOfCams = int(line)
	
	for i in range( nrOfCams ):
		## <OBJ_CAM>
		line = f.readline(READ_LINE_SIZE)
		
		## NAME
		line = f.readline(READ_LINE_SIZE)
		name = line.rstrip('\n')
		
		## ENDDELAYTIME
		line = f.readline(READ_LINE_SIZE)
		endDelayTime = float(line)
		
		## CAMERAMAXSPEED
		line = f.readline(READ_LINE_SIZE)
		camMaxSpeed = float(line)
		
		## CAMERAMAXACCELERATION
		line = f.readline(READ_LINE_SIZE)
		camMaxAcceleration = float(line)

		## USE END GRAB
		line = f.readline(READ_LINE_SIZE)
		camUseEndGrab = int(line)
		
		newCam = oc.ObjectiveCameraEx( name )
		newCam.SetEndDelayTime( endDelayTime )
		newCam.UseEndGrab( camUseEndGrab )
		newCam.SetCameraMaxSpeed( camMaxSpeed )
		newCam.SetCameraMaxAcceleration( camMaxAcceleration )
		
		## NR OF POINT
		line = f.readline(READ_LINE_SIZE)
		nrOfPoints = int(line)
		
		for j in range( nrOfPoints ):
			## <POINT>
			line = f.readline(READ_LINE_SIZE)
			
			## move x
			line = f.readline(READ_LINE_SIZE)
			m_x = float(line)
			
			## move y
			line = f.readline(READ_LINE_SIZE)
			m_y = float(line)
			
			## move Z
			line = f.readline(READ_LINE_SIZE)
			m_z = float(line)

			## look x
			line = f.readline(READ_LINE_SIZE)
			l_x = float(line)
			
			## look y
			line = f.readline(READ_LINE_SIZE)
			l_y = float(line)
			
			## look Z
			line = f.readline(READ_LINE_SIZE)
			l_z = float(line)

			## delay time
			line = f.readline(READ_LINE_SIZE)
			delayTime = float(line)

			## close to limit
			line = f.readline(READ_LINE_SIZE)
			closeToLimit = float(line)
			
			## goto now
			line = f.readline(READ_LINE_SIZE)
			gotoNow = int(line)

			## lookat now
			line = f.readline(READ_LINE_SIZE)
			lookAtNow = int(line)
			
			p = newCam.AddPoint( Position( m_x, m_y, m_z ), Position( l_x, l_y, l_z ), delayTime, closeToLimit )
			p.SetGoToNow( gotoNow )
			p.SetLookAtNow( lookAtNow )
			
			## <\POINT>
			line = f.readline(READ_LINE_SIZE)
		
		theObjectiveCameras.append( newCam )
		
		## <\OBJ_CAM>
		line = f.readline(READ_LINE_SIZE)
			
	f.close()


mapFolders = ( 'seattle2', 'seattle3', 'ustown4', 'usfarmland3', 'ustown3', 'europe4', 'europe2', 'russia2', 'russia4', 'usfarmland2', 'ustown1', 'newyork1', 'seattle4', 'seattle1', 'usdesert2' )


def LoadObjectiveCamerasFromClient( mapFolderName ):
	global theObjectiveCameras
	import camera.objectivecamera as oc
	
	filePath = 'maps\\%s\\python\\client.py' % mapFolderName
	
	try:
		f = file( filePath, 'r' )
	except IOError:
		return
	
	if not f:
		return
	
	
	def ExtractPositions( l ):
		pass
		#idx = l.rfind( 'Position(' )
		#if idx != -1:
		#	sep = l[idx:-1].rfind( ',' )
		#	x = (float)l[idx+9:sep-1]
		
	
	debug.DebugMessage( 'SWANI LoadObjectiveCamerasFromClient(%s)' % mapFolderName )
	
	cameraName = ''
	inCameMode = False
	
	line = f.readline(READ_LINE_SIZE)
	while line:
		
		if inCameMode:
			
			debug.DebugMessage( 'In game mode (%s)' % line )
			
			##a point
			if line.rfind( '.AddPoint' ) != -1:
				pos = ExtractPositions( line )
				debug.DebugMessage( 'AddPoint (%s,%s)' % (pos[0], pos[1]) )
				
			##a point
			if line.rfind( '.SetEndDelayTime' ) != -1:
				pass
			##a point
			if line.rfind( '.AddPoint' ) != -1:
				pass
			##a point
			if line.rfind( '.AddPoint' ) != -1:
				pass
			##a point
			if line.rfind( '.AddPoint' ) != -1:
				pass
			
		
		
		## we found a camera!!!
		if line.rfind( 'def ObjCam' ) != -1:
			cameraName = line[line.rfind( 'ObjCam' ):line.rfind( '(' )]
			debug.DebugMessage( 'we found a camera(%s)' % cameraName )
			inCameMode = True
				
		line = f.readline(READ_LINE_SIZE)

	


def AddPoint( anOC ):
	
	try:
		import wicp
	except Exception:
		return
	
	try:
		import camera.objectivecamera as oc
	except Exception:
		return

	try:
		moveToPos = wicp.GetCameraPosition()
		lookAtPos = wicp.GetCameraLookAt()
		distance = wicp.GetDistanceToGround()
	except AttributeError:
		return
		
	anOC.AddPoint( moveToPos, lookAtPos, oc.DEFAULT_POINT_DELAY_TIME, oc.DEFAULT_CLOSE_TO_LIMIT, distance )

def GetLookAtPoint():
	try:
		import wicp
	except Exception:
		return
	
	try:
		moveToPos = wicp.GetCameraPosition()
		lookAtPos = wicp.GetCameraLookAt()
		distance = wicp.GetDistanceToGround()
	except AttributeError:
		return

	if lookAtPos is None or moveToPos is None:
		return None
	
	if distance == 1.0:
		distance = 10.0
	
	lookDir = lookAtPos - moveToPos
	lookDir.Normalize()
	lookDir = lookDir * distance
			
	lookAtPos = moveToPos + lookDir
			
	return lookAtPos

def UpdatePoint( anOC, aPointIndex ):

	try:
		import wicp
	except Exception:
		return
	
	try:
		moveToPos = wicp.GetCameraPosition()
		lookAtPos = wicp.GetCameraLookAt()
		distance = wicp.GetDistanceToGround()
	except AttributeError:
		return
	
	anOC.myPoints[aPointIndex].myMoveToTarget = moveToPos
	anOC.myPoints[aPointIndex].myLookAtTarget = lookAtPos
	anOC.myPoints[aPointIndex].myDistanceToLookAt = distance


def RemovePoint( anOC, aPointIndex ):
	
	anOC.RemovePoint( aPointIndex )


def TogglePyViewer():
	global isActive
	
	if isActive:
		Deactivate()
	else:
		Activate()


def ToggleGrabCamera():
	import camera.camera
	global doRender
	
	if camera.camera.IsActive():
		doRender = True
		camera.camera.ReleaseCamera()
	else:
		doRender = False
		camera.camera.GrabCamera(1)
	


def Activate():
	global isActive
	global reactUpdate
	global currentEntry
	global useAutoGroupNameView
	global theEditedAreas
	
	import serverimports as si
	
	isActive = True
	
	theExpanded = []
	si.RemoveReaction( reactUpdate )
	si.RemoveReactionFromPrimary( reactUpdate )
	
	currentEntry = 0

	reactUpdate = RE_OnCustomEvent( 'Update', Action( Update ) )
	reactUpdate.myRepeating = True
	
	RE_OnSystemSwitched( Action( Activate ) )
	
	## broken ??
	LoadSettings()
	LoadCivilians()
	LoadAreas()
	LoadObjectiveCameras()

	
def Deactivate():
	global isActive
	global theExpanded
	global currentEntry
	global reactUpdate
	
	isActive = False

	theExpanded = []
	RemoveReaction( reactUpdate )
	reactUpdate = None
	
	currentEntry = 0


class Entry( object ):
	
	myValue = ''
	myIsExpanded = False
	myLevel = 0
	myUniqueString = ''
	myInfo = -242
	myScreenPosition = None
	myScreenRadius = 0.0
	
	myScreenPositionList = []
	myScreenRadiusList = []
	myScreenNameList = []
	
	myOnClickActions = []
	myInfoGetFunction = None
	
	
	def __init__( self, aValue, aInfo = -242 ):
		global currentLevel
		
		self.myInfo = aInfo
		self.myValue = aValue
		self.myIsExpanded = False
		self.myLevel = currentLevel
		self.myUniqueString = ''
		self.myScreenPosition = None
		self.myScreenRadius = 0.0
		self.myOnClickActions = []
		self.myOnClickActionsEx = []
		self.myInfoGetFunction = None
		
		self.mySetFunction = None
		self.mySetIncrData = None
		self.mySetDecrData = None
		
		self.myOnSelectedActions = []
		self.myOnSelectionLostActions = []

		self.myScreenPositionList = []
		self.myScreenRadiusList = []
		self.myScreenNameList = []
		
		self.myMoveToExPosition = None
		self.myMoveToExLookAt = None



	def GetText( self ):
		
		if self.myInfo == -242:
			return self.myValue
		elif isinstance( self.myInfo, int ):
			return '%s(%d)' % ( self.myValue, self.myInfo )
		elif isinstance( self.myInfo, float ):
			return '%s(%.02f)' % ( self.myValue, self.myInfo )
		else:
			return '%s(%s)' % ( self.myValue, self.myInfo )


	def OnRightClick( self ):

		if len( self.myOnClickActionsEx ) > 0:
			try:
				self.myOnClickActionsEx[0](self.myOnClickActionsEx[1].Execute())
			except Exception:
				pass

		if len( self.myOnClickActions ) == 0:
			return
		
		for act in self.myOnClickActions:
			act.Execute()
	
	def OnKeyRight( self ):
		if self.mySetFunction:
			self.mySetFunction( self.mySetIncrData )
				
	def OnKeyLeft( self ):
		if self.mySetFunction:
			self.mySetFunction( self.mySetDecrData )		
	
	def OnSelected( self ):
		for act in self.myOnSelectedActions:
			act.Execute()
	
	def OnSelectionLost( self ):
		
		for act in self.myOnSelectionLostActions:
			act.Execute()
	
	def AddMoveToAction( self ):
		
		movePos = GetCopy( self.myScreenPosition )
		
		## height
		movePos.myY += 64
		
		## offset
		movePos.myX += 64
		movePos.myZ += 64
		
		lookAtPos = GetCopy( self.myScreenPosition )
		self.myOnClickActions.append( Action( thePlayers[1].SetCameraPosition, movePos, lookAtPos ) )


	def AddMoveToActionEx( self ):
		
		if not self.myMoveToExPosition or not self.myMoveToExLookAt:
			return
		
		movePos = self.myMoveToExPosition
		lookAtPos = self.myMoveToExLookAt	
		self.myOnClickActions.append( Action( thePlayers[1].SetCameraPosition, movePos, lookAtPos ) )




class Expanded( object ):
	
	myValue = ''
	myIsExpanded = False	
	
	
	def __init__( self, aValue, aIsExpanded = True ):
		global currentLevel
				
		self.myValue = aValue
		self.myIsExpanded = aIsExpanded
	
	
	def __cmp__( self, other ):
		
		if self.myValue == other:
			return 0
		else:
			return 1


def IsExpanded( aEntry ):
	
	if (aEntry + 1) >= len( theEntries ):
		return False
	
	if theEntries[aEntry].myLevel >= theEntries[aEntry + 1].myLevel:
		return False
	
	return theEntries[aEntry].myIsExpanded


def AddCommand( aString, someActions ):
	global theCommands
	
	if not isinstance( someActions, list ):
		someActions = [someActions]
	
	e = Entry( aString )
	e.myOnClickActions = someActions
	theCommands.append( e )


def AddWatch( aString, aGetFunction ):
	global theWatches
	
	e = Entry( aString, aGetFunction() )
	e.myInfoGetFunction = aGetFunction
	theWatches.append( e )
	

def AddString( aString, aAutoRemove = False, aRemoveDelay = DEFAULT_REMOVE_DELAY ):
	global theStrings
	
	e = Entry( aString )
	theStrings.append( e )
	
	if aAutoRemove:
		Delay( aRemoveDelay, Action( theStrings.remove, e ) )


def SanityUnitCheck():
	global theGroups
	
	try:
		import wicp
	except Exception:
		return

	badUnits = 'Bad units = '

	allOk = True
	
	import serverimports as si
	
	for grp_str in si.theGroups.myGroups:
		grp = si.theGroups[ grp_str ]
		if grp:
			for grpUnit in grp.myUnits:
				try:
					unit.theUnits[ grpUnit.myUnitId ]
				except unit.UnknownUnitException:
					badUnits += '(%d in %s)' % ( grpUnit.myUnitId, grp )
					allOk = False
	if allOk:
		return 'All units OK!'
	else:
		return badUnits


def UpdateEntries():
	import serverimports as si
	
	global theEntries
	global theExpanded
	global currentLevel
	global currentEntry
	global useAutoGroupSelection
	global theStrings
	global theEditedCommandpoints
	global theEditedAreas

	if currentEntry < len( theEntries ):
		currentEntryStr = CalculateUniqueString( currentEntry )	
	else:
		currentEntryStr = ''
	
	theEntries = []
	currentLevel = 0

	## SETTINGS
	
	theEntries.append( Entry( 'SETTINGS' ) )
	
	currentLevel += 1
	
	
	e = Entry('GroupAutoSelection', useAutoGroupSelection )
	e.myOnClickActions.append( Action( useAutoGroupSelection.Toggle ) )
	e.myOnClickActions.append( Action( SaveSettings ) )
	theEntries.append( e )

	e = Entry('GroupNameAutoView', useAutoGroupNameView)
	e.myOnClickActions.append( Action( useAutoGroupNameView.Toggle ) )
	e.myOnClickActions.append( Action( SaveSettings ) )
	theEntries.append( e )

	e = Entry('ShowCommands', showCommands )
	e.myOnClickActions.append( Action( showCommands.Toggle ) )
	e.myOnClickActions.append( Action( SaveSettings ) )
	theEntries.append( e )

	e = Entry('ShowWatches', showWatches )
	e.myOnClickActions.append( Action( showWatches.Toggle ) )
	e.myOnClickActions.append( Action( SaveSettings ) )
	theEntries.append( e )

	e = Entry('ShowStrings', showStrings )
	e.myOnClickActions.append( Action( showStrings.Toggle ) )
	e.myOnClickActions.append( Action( SaveSettings ) )
	theEntries.append( e )

	e = Entry('ShowSystemInfo', showSystemInfo )
	e.myOnClickActions.append( Action( showSystemInfo.Toggle ) )
	e.myOnClickActions.append( Action( SaveSettings ) )
	theEntries.append( e )

	e = Entry('ShowObjectiveCamera', showObjectiveCamera )
	e.myOnClickActions.append( Action( showObjectiveCamera.Toggle ) )
	e.myOnClickActions.append( Action( SaveSettings ) )
	theEntries.append( e )

	e = Entry('ShowGroups', showGroups )
	e.myOnClickActions.append( Action( showGroups.Toggle ) )
	e.myOnClickActions.append( Action( SaveSettings ) )
	theEntries.append( e )

	e = Entry('ShowReactions', showReactions )
	e.myOnClickActions.append( Action( showReactions.Toggle ) )
	e.myOnClickActions.append( Action( SaveSettings ) )
	theEntries.append( e )

	e = Entry('ShowActionQueues', showActionQueues )
	e.myOnClickActions.append( Action( showActionQueues.Toggle ) )
	e.myOnClickActions.append( Action( SaveSettings ) )
	theEntries.append( e )

	e = Entry('ShowInstances', showInstances )
	e.myOnClickActions.append( Action( showInstances.Toggle ) )
	e.myOnClickActions.append( Action( SaveSettings ) )
	theEntries.append( e )

	e = Entry('ShowAreas', showAreas )
	e.myOnClickActions.append( Action( showAreas.Toggle ) )
	e.myOnClickActions.append( Action( SaveSettings ) )
	theEntries.append( e )

	e = Entry('ShowUnits', showUnits )
	e.myOnClickActions.append( Action( showUnits.Toggle ) )
	e.myOnClickActions.append( Action( SaveSettings ) )
	theEntries.append( e )

	e = Entry('ShowPlatoons', showPlatoons )
	e.myOnClickActions.append( Action( showPlatoons.Toggle ) )
	e.myOnClickActions.append( Action( SaveSettings ) )
	theEntries.append( e )

	e = Entry('ShowAI', showAI )
	e.myOnClickActions.append( Action( showAI.Toggle ) )
	e.myOnClickActions.append( Action( SaveSettings ) )
	theEntries.append( e )

	e = Entry('ShowServerplay', showServerplay )
	e.myOnClickActions.append( Action( showServerplay.Toggle ) )
	e.myOnClickActions.append( Action( SaveSettings ) )
	theEntries.append( e )

	e = Entry('ShowClient', showClient )
	e.myOnClickActions.append( Action( showClient.Toggle ) )
	e.myOnClickActions.append( Action( SaveSettings ) )
	theEntries.append( e )

	e = Entry('ShowServer', showServer )
	e.myOnClickActions.append( Action( showServer.Toggle ) )
	e.myOnClickActions.append( Action( SaveSettings ) )
	theEntries.append( e )
	
	e = Entry('ShowAreaEditor', showAreaEditor )
	e.myOnClickActions.append( Action( showAreaEditor.Toggle ) )
	e.myOnClickActions.append( Action( SaveSettings ) )
	theEntries.append( e )

	e = Entry('ShowCiviliansEditor', showCiviliansEditor )
	e.myOnClickActions.append( Action( showCiviliansEditor.Toggle ) )
	e.myOnClickActions.append( Action( SaveSettings ) )
	theEntries.append( e )

	e = Entry('ShowHighCivilians', showHighCivilians )
	e.myOnClickActions.append( Action( showHighCivilians.Toggle ) )
	e.myOnClickActions.append( Action( SaveSettings ) )
	theEntries.append( e )

	e = Entry('ShowRoofCivilians', showRoofCivilians )
	e.myOnClickActions.append( Action( showRoofCivilians.Toggle ) )
	e.myOnClickActions.append( Action( SaveSettings ) )
	theEntries.append( e )

	e = Entry('ShowGroundCivilians', showGroundCivilians )
	e.myOnClickActions.append( Action( showGroundCivilians.Toggle ) )
	e.myOnClickActions.append( Action( SaveSettings ) )
	theEntries.append( e )


	currentLevel -= 1


	## COMMANDS
	
	if showCommands.Get():
		theEntries.append( Entry( 'COMMANDS' ) )
		
		currentLevel += 1
		
		for cmd_entry in theCommands:
			
			cmd_entry.myLevel = currentLevel
			theEntries.append( cmd_entry )
		
		currentLevel -= 1
	
	
	## WATCHES
	
	if showWatches.Get():
		theEntries.append( Entry( 'WATCHES' ) )
		
		currentLevel += 1
		
		for watch in theWatches:
			watch.myLevel = currentLevel
			if watch.myInfoGetFunction:
				watch.myInfo = watch.myInfoGetFunction()
			theEntries.append( watch )
		
		currentLevel -= 1

	
	## STRINGS
	
	if showStrings.Get():
		theEntries.append( Entry( 'STRINGS' ) )
		
		currentLevel += 1
		
		for s in theStrings:
			s.myLevel = currentLevel
			theEntries.append( s )
		
		currentLevel -= 1
	
	
	## files
	
	if showServerplay.Get():
		allOk = True
		try:
			import serverplay
		except Exception:
			theEntries.append( Entry( 'Could not import serverplay' ) )
			allOk = False
		
		if allOk:
			theEntries.append( Entry( 'SERVERPLAY' ) )
			
			currentLevel += 1
			
			for n in serverplay.__dict__:
				if n.find( 'Cine' ) != -1 and n.find( 'Start' ) != -1:
					e = Entry( '%s()' % n )
					e.myOnClickActions.append( Action( eval, '%s()' % n, serverplay.__dict__ ) )
					theEntries.append( e )
			
			currentLevel -= 1
	
	
	## client
	
	if showClient.Get():
		allOk = True
		try:
			import client
		except Exception:
			theEntries.append( Entry( 'Could not import client' ) )
			allOk = False
		
		if allOk:
			theEntries.append( Entry( 'CLIENT' ) )
			
			currentLevel += 1
			
			for n in client.__dict__:
				
				try:
					client.__dict__[n].__module__
				except AttributeError:
					continue
								
				if client.__dict__[n].__module__ == 'client':
					try:
						if client.__dict__[n].func_defaults and client.__dict__[n].func_defaults[0] == True:
								if len(client.__dict__[n].func_code.co_names) > 1 and ( client.__dict__[n].func_code.co_names[1] == 'aIsBrowserCamera' or client.__dict__[n].func_code.co_names[1] == 'aIsBrowser' ):
									e = Entry( '%s()' % n )
									e.myOnClickActions.append( Action( eval, '%s(False)' % n, client.__dict__ ) )
									theEntries.append( e )
									
									currentLevel += 1
									global theObjectiveCameras
									e = Entry( 'CopyToMyCameras' )
									e.myOnClickActionsEx.append( theObjectiveCameras.append )
									e.myOnClickActionsEx.append( Action( eval, '%s(False)' % n, client.__dict__ ) )
									theEntries.append( e )
									
									
									currentLevel -= 1
					except AttributeError:
						continue
				
						
			currentLevel -= 1
	
	
	if showServer.Get():
		allOk = True
		try:
			import server
		except Exception:
			theEntries.append( Entry( 'Could not import server' ) )
			allOk = False
		
		if allOk:
			theEntries.append( Entry( 'SERVER' ) )
			
			currentLevel += 1
			
			for n in server.__dict__:
				if n.find( 'Setup' ) != -1:
					e = Entry( '%s( True )' % n )
					e.myOnClickActions.append( Action( eval, '%s( True )' % n, server.__dict__ ) )
					theEntries.append( e )
			
			currentLevel -= 1
	
	
	## OBJECTIVE CAMERA
	
	##qwert
	
	if showObjectiveCamera.Get():
		e = Entry( 'OBJECTIVE CAMERAS' )
		theEntries.append( e )
		
		currentLevel += 1
		
		e = Entry( 'Save Cameras to file' )
		e.myOnClickActions.append( Action( SaveObjectiveCameras ) )
		theEntries.append( e )
	
		e = Entry( 'Create new Camera' )
		e.myOnClickActions.append( Action( AddObjectiveCamera ) )
		e.myOnClickActions.append( Action( SaveObjectiveCameras ) )
		theEntries.append( e )		
	
		try:
			import wicp
			
			e = Entry( 'CurrentPosition', wicp.GetCameraPosition() )
			e.myScreenPosition = wicp.GetCameraPosition()
			theEntries.append( e )
	
			e = Entry( 'CurrentLookAt', wicp.GetCameraLookAt() )
			dist = wicp.GetDistanceToGround()
			
			if dist == 1.0:
				dist = 10.0
			e.myScreenPosition = wicp.GetCameraPosition() + ((wicp.GetCameraLookAt() - wicp.GetCameraPosition()).Normalize()) * dist
			
			theEntries.append( e )
	
		except Exception:
			pass
			
		global theObjectiveCameras
		
		for oc in theObjectiveCameras:
			e = Entry(oc.myName)
			theEntries.append( e )
			
			currentLevel += 1
	
			e = Entry( 'Play' )
			e.myOnClickActions.append( Action( oc.Play ) )
			theEntries.append( e )
	

			e = Entry( 'Remove Cam' )
			e.myOnClickActions.append( Action( theObjectiveCameras.remove, oc ) )
			theEntries.append( e )

	
			e = Entry( 'Add new Keyframe' )
			lp = GetLookAtPoint()
			if lp != None:
				e.myScreenPosition = lp
			e.myOnClickActions.append( Action( AddPoint, oc ) )
			e.myOnClickActions.append( Action( SaveObjectiveCameras ) )
			theEntries.append( e )
	
			theEntries.append(Entry('Cam Settings'))
	
			currentLevel += 1

			e = Entry( 'CameraType' )
			theEntries.append( e )
			
			currentLevel += 1
			
			import camera.objectivecamera as oc_module
			for ct in oc_module.cameraTypes:
				e = Entry( ct )
				e.myOnClickActions.append( Action( oc.SetCameraType, oc_module.cameraTypes[ct]() ) )
				theEntries.append( e )
			
			currentLevel -= 1


			e = Entry( 'Use Grab on Release(%d)' % oc.GetUseEndGrab() )
			e.myOnClickActions.append( Action( oc.ToggleUseEndGrab ) )
			theEntries.append( e )

	
			e = Entry( 'EndDelayTime', oc.myEndDelayTime )
			e.mySetFunction = oc.SetEndDelayTime
			e.mySetIncrData = oc.myEndDelayTime + 0.2
			e.mySetDecrData = oc.myEndDelayTime - 0.2
			theEntries.append( e )
	
	
			e = Entry( 'MaxSpeed', oc.myCameraMaxSpeed )
			e.mySetFunction = oc.SetCameraMaxSpeed
			e.mySetIncrData = oc.myCameraMaxSpeed + 5.0
			e.mySetDecrData = oc.myCameraMaxSpeed - 5.0
			theEntries.append( e )
	
	
			e = Entry( 'MaxAcceleration', oc.myCameraMaxAcceleration )
			e.mySetFunction = oc.SetCameraMaxAcceleration
			e.mySetIncrData = oc.myCameraMaxAcceleration + 2.0
			e.mySetDecrData = oc.myCameraMaxAcceleration - 2.0
			theEntries.append( e )

			#cameraType = oc.myCameraType

			#e = Entry( 'AngularElasticity', cameraType.myAngularElasticity )
			#e.mySetFunction = cameraType.SetAngularElasticity
			#e.mySetIncrData = cameraType.myAngularElasticity + 1.0
			#e.mySetDecrData = cameraType.myAngularElasticity - 1.0
			#theEntries.append( e )
			
			#e = Entry( 'AngularDrag', cameraType.myAngularDrag )
			#e.mySetFunction = cameraType.SetAngularDrag
			#e.mySetIncrData = cameraType.myAngularDrag + 1.0
			#e.mySetDecrData = cameraType.myAngularDrag - 1.0
			#theEntries.append( e )

			#e = Entry( 'PositionalElasticity', cameraType.myPositionalElasticity )
			#e.mySetFunction = cameraType.SetPositionalElasticity
			#e.mySetIncrData = cameraType.myPositionalElasticity + 1.0
			#e.mySetDecrData = cameraType.myPositionalElasticity - 1.0
			#theEntries.append( e )

			#e = Entry( 'PositionalDrag', cameraType.myPositionalDrag )
			#e.mySetFunction = cameraType.SetPositionalDrag
			#e.mySetIncrData = cameraType.myPositionalDrag + 1.0
			#e.mySetDecrData = cameraType.myPositionalDrag - 1.0
			#theEntries.append( e )

			#e = Entry( 'ZoomElasticity', cameraType.myZoomElasticity )
			#e.mySetFunction = cameraType.SetZoomElasticity
			#e.mySetIncrData = cameraType.myZoomElasticity + 1.0
			#e.mySetDecrData = cameraType.myZoomElasticity - 1.0
			#theEntries.append( e )
			
			#e = Entry( 'ZoomDrag', cameraType.myZoomDrag )
			#e.mySetFunction = cameraType.SetZoomDrag
			#e.mySetIncrData = cameraType.myZoomDrag + 1.0
			#e.mySetDecrData = cameraType.myZoomDrag - 1.0
			#theEntries.append( e )
			
			
			currentLevel -= 1
	
			
			c = 0
			for p in oc.myPoints:
				e = Entry('Keyframe%d' % c)
				e.myScreenPosition = p.myMoveToTarget
				e.myMoveToExPosition = p.myMoveToTarget
				e.myMoveToExLookAt = p.myLookAtTarget
				e.AddMoveToActionEx()
				theEntries.append( e )
				
				currentLevel += 1
	
				e = Entry( 'Remove Keyframe' )
				e.myOnClickActions.append( Action( RemovePoint, oc, c ) )
				theEntries.append( e )
	
				e = Entry( 'Update Keyframe' )
				lp = GetLookAtPoint()
				if lp != None:
					e.myScreenPosition = lp
				e.myOnClickActions.append( Action( UpdatePoint, oc, c ) )
				theEntries.append( e )

				e = Entry( 'Move Keyframe Up' )
				e.myOnClickActions.append( Action( oc.MovePointUp, p ) )
				theEntries.append( e )

				e = Entry( 'Move Keyframe Down' )
				e.myOnClickActions.append( Action( oc.MovePointDown, p ) )
				theEntries.append( e )
	
				#e = Entry( 'MoveTo', p.myMoveToTarget )
				#e.myScreenPosition = p.myMoveToTarget
				#e.AddMoveToAction()
				#theEntries.append( e )
				
				#e = Entry( 'LookAt', p.myLookAtTarget )
				#e.myScreenPosition = p.myLookAtTarget
				#e.AddMoveToAction()
				#theEntries.append( e )
				
				theEntries.append( Entry( 'Keyframe Settings' ) )
				
				currentLevel += 1
				
				e = Entry( 'DelayTime', p.myDelayTime )
				e.mySetFunction = p.SetDelayTime
				e.mySetIncrData = p.myDelayTime + 0.5
				e.mySetDecrData = p.myDelayTime - 0.5
				theEntries.append( e )
	
				e = Entry( 'CloseToLimit', p.myCloseToLimit )
				e.mySetFunction = p.SetCloseToLimit
				
				if p.myCloseToLimit < 128.0:
					e.mySetIncrData = p.myCloseToLimit + 2.0
				else:
					p.SetCloseToLimit( 128.0 )
					e.mySetIncrData = 128.0
				e.mySetDecrData = p.myCloseToLimit - 2.0
				
				theEntries.append( e )
	
				e = Entry( 'DistanceToLookAt', p.myDistanceToLookAt )
				e.mySetFunction = p.SetDistanceToLookAt
				e.mySetIncrData = p.myDistanceToLookAt + 5.0
				e.mySetDecrData = p.myDistanceToLookAt - 5.0
				theEntries.append( e )

				e = Entry( 'UseGotoNow', p.myUseGoToNow )
				b = 1
				if p.myUseGoToNow:
					b = 0 
				e.myOnClickActions.append( Action( p.SetGoToNow, b ) )
				theEntries.append( e )

				e = Entry( 'UseLookAtNow', p.myUseLookAtNow )
				b = 1
				if p.myUseLookAtNow:
					b = 0 
				e.myOnClickActions.append( Action( p.SetLookAtNow, b ) )
				theEntries.append( e )
				
				currentLevel -= 1
				
				currentLevel -= 1
				
				c += 1
			
			
			currentLevel -= 1
		
		currentLevel -=1
	
	
	## SYSTEM INFO
	
	if showSystemInfo.Get():
		theEntries.append( Entry( 'SYSTEM INFO' ) )
		
		currentLevel += 1
		
		theEntries.append( Entry( 'CurrentNrOfReactions', si.theReactions.GetCurrentNrOfReactions() ) )
		theEntries.append( Entry( 'CurrentNrOfGroups', si.theGroups.GetCurrentNumberOfGroups() ) )
		theEntries.append( Entry( 'CurrentNrOfRefillerGroups', si.theGroups.GetCurrentNumberOfRefillerGroups() ) )
		theEntries.append( Entry( 'CurrentNrOfUnits', si.theGroups.GetCurrentNumberOfUnits() ) )
		theEntries.append( Entry( 'AverageGroupUpdateDelay', si.theGroups.GetAverageUpdateDelay( 1.0 ) ) )
		theEntries.append( Entry( 'LastGroupUpdateDelay', si.theGroups.GetLastUpdateAverage() ) )
		theEntries.append( Entry( 'AlternativeMode(%s)' % si.serverimports.isInAlternativeMode ) )
		theEntries.append( Entry( 'NrOfBadTimers', si.theReactions.GetNrOfBadTimers() ) )
		theEntries.append( Entry( 'UnitSanityCheck', SanityUnitCheck() ) )
		
		e = Entry( 'SwitchSystem', si.serverimports.isInAlternativeMode )
		if si.serverimports.isInAlternativeMode:
			e.myOnClickActions.append( Action( si.UsePrimaryReactionSystem ) )
		else:
			e.myOnClickActions.append( Action( si.UseAlternativeReactionSystem ) )
		theEntries.append( e )
		
		
		currentLevel -= 1
	
	
	## GROUPS
	
	if showGroups.Get():
	
		theEntries.append( Entry( 'GROUPS' ) )
		
		currentLevel += 1
		
		for grp in si.theGroups.myGroups.values():
			
			e = Entry( '%s' % grp.myName, grp.Size( ) )
			if grp.Size():
				e.myScreenPosition = grp.GetPosition()
				e.AddMoveToAction()
				
			theEntries.append( e )
			
			currentLevel += 1
			
			theEntries.append( Entry( 'RealSize', grp.Size( True ) ) )
			theEntries.append( Entry( 'myUnits', grp.Size() ) )
			
			if showUnits.Get():
				currentLevel += 1
				for unit in grp.myUnits:
					e = Entry( 'Id=%d SquadId=%d Owner=%d Team=%d Type=%s(%d)' % (unit.myUnitId, unit.myUnit.mySquadId, unit.myUnit.myOwner, unit.myUnit.myTeam, unit.myUnit.myUIName, unit.myUnit.myType ) )
					e.myScreenPosition = unit.myPos
					e.AddMoveToAction()
					theEntries.append( e )
					
				currentLevel -= 1
			
			
			theEntries.append( Entry( 'myOwner', grp.myOwner ) )
			theEntries.append( Entry( 'myTeam', grp.myTeam ) )
			
			refillGroups = grp.myRefillGroups
			
			if len( refillGroups ):
				theEntries.append( Entry( 'myRefillGroups' ) )
				
				currentLevel += 1
				
				for g in refillGroups:
					e = Entry( '%s' % g )
					if g.Size():
						e.myScreenPosition = g.GetPosition()
						e.AddMoveToAction()
					theEntries.append( e )

				
				currentLevel -= 1
				
				
			else:
				theEntries.append( Entry( 'myRefillGroups=None' ) )
			
			e = Entry( 'myParentGroup', grp.myParentGroup )
			
			if grp.myParentGroup and grp.myParentGroup.Size():
				e.myScreenPosition = grp.myParentGroup.GetPosition()
				e.AddMoveToAction()
				
			theEntries.append( e )
			theEntries.append( Entry( 'myState', grp.GetState() ) )
			theEntries.append( Entry( 'BHB=%s' % grp.myBehaviorManager.myBaseBehavior ) )
			theEntries.append( Entry( 'BHA=%s' % grp.myBehaviorManager.myAttackBehavior ) )
			
			theEntries.append( Entry( 'Refill=%s' % grp.myRefillMode ) )
			
			
			theEntries.append( Entry( 'Passive=%s' % grp.IsPassive() ) )
			
			
			## PLATOON	
			if showPlatoons.Get():
			
				theEntries.append( Entry( 'Platoons', len(grp.myPlatoons) ) )
				
				currentLevel += 1
				
				for plt in grp.myPlatoons:
					theEntries.append( Entry( '%s' % plt, len( plt.myGroups ) ) )
					
					currentLevel += 1
					
					for g in plt.myGroups:
						e = Entry( '%s' % g )
						if g.Size():
							e.myScreenPosition = g.GetPosition()
							e.AddMoveToAction()
						theEntries.append( e )
					
					currentLevel -= 1
				
				currentLevel -= 1
					
			
			## AI
			
			ai = grp.GetAI()
			
			theEntries.append( Entry( 'AI=%s' % ai ) )
			
			if not ai is None:
				currentLevel += 1
				theEntries.append( Entry( 'Id', ai.myId ) )
				theEntries.append( Entry( 'IsEnabled', ai.myIsEnabled ) )
				theEntries.append( Entry( 'CurrentCommand', ai.myCurrentCommand ) )
				theEntries.append( Entry( 'Groups' ) )
				
				currentLevel += 1
				
				for g in ai.myGroups:
					e = Entry( '(AI)%s' % g )
					
					if g.Size():
						e.myScreenPosition = g.GetPosition()
						e.AddMoveToAction()
						
					theEntries.append( e )
				
				currentLevel -= 1
				
				e = Entry( 'ToggleDebugOutput', ai.IsDebugOutputEnabled() )
				e.myOnClickActions.append( Action( ai.ToggleDebugOutput ) )
				theEntries.append( e )
				
				currentLevel -= 1
			
			
			## FORMATION
			form = grp.GetFormation()
			formString = ''	
			if form == FORMATION_BOX:
				formString = 'BOX'
			elif form == FORMATION_LINE:
				formString = 'LINE'
			elif form == FORMATION_COVER:
				formString = 'COVER'
			else:
				formString = 'UNDEFINED'
				
			theEntries.append( Entry( 'Formation=%s' % formString, grp.GetFormationDistance() ) )
			
			
			## PRIMARY COMMANDS
			p_cmd = grp.GetCommands( CMD_PRIMARY )
			theEntries.append( Entry( 'PrimaryCommands', len( p_cmd ) ) )
			currentLevel += 1
			
			for c in p_cmd:
				theEntries.append( Entry( '%s' % c ) )
			
			currentLevel -= 1		
			
			## ATTACK COMMANDS
			a_cmd = grp.GetCommands( CMD_ATTACK )
			theEntries.append( Entry( 'AttackCommands', len( a_cmd ) ) )
			currentLevel += 1
			
			for c in a_cmd:
				theEntries.append( Entry( '%s' % c ) )
			
			currentLevel -= 1		
			
			## BASE COMMANDS
			b_cmd = grp.GetCommands( CMD_BASE )
			theEntries.append( Entry( 'BaseCommands', len( b_cmd ) ) )
			currentLevel += 1
			
			for c in b_cmd:
				theEntries.append( Entry( '%s' % c ) )
			
			currentLevel -= 1		
	
			## REFILL COMMANDS
			r_cmd = grp.GetRefillCommands( )
			theEntries.append( Entry( 'RefillCommands', len( r_cmd ) ) )
			currentLevel += 1
			
			for r in r_cmd:
				theEntries.append( Entry( '%s' % r ) )
			
			currentLevel -= 1		
	
			currentLevel -= 1
		
		currentLevel -= 1


	## REACTIONS
	if showReactions.Get():

		theEntries.append( Entry( 'REACTIONS' ) )
		
		
		currentLevel += 1
		
		
		timers = si.theReactions.GetTimers()
		
		theEntries.append( Entry( 'Timers', si.theReactions.GetNrOfTimers() ) )
		
		currentLevel += 1
		
		for t in timers:
			theEntries.append( Entry( '%s : ' % t, t.GetTimeLeft() ) )
		
		currentLevel -= 1
		
		theEntries.append( Entry( 'UnitDestroyed_I', si.theReactions.GetNrOfUnitDestroyed() ) )
		theEntries.append( Entry( 'UnitInCombat_I', si.theReactions.GetNrOfUnitInCombat() ) )
		theEntries.append( Entry( 'GroupInCombat_I', si.theReactions.GetNrOfGroupInCombat() ) )
		theEntries.append( Entry( 'GroupSize_I', si.theReactions.GetNrOfGroupSize() ) )
		
		for event in si.theReactions.myReactionHandlers:
			theEntries.append( Entry( '%s' % event, si.theReactions.GetNrOfReactionsByType( event ) ) )
			
			currentLevel += 1
			
			reactions = si.theReactions.GetReactionsByType( event )
			
			if not reactions is None:
				for r in reactions:
					theEntries.append( Entry( '%s' % r ) )
				
			currentLevel -= 1
			
		
		currentLevel -= 1


	## ACTIONQUEUES
	
	if showActionQueues.Get():
		import wicgame.actionqueue
		
		theEntries.append( Entry( 'ACTIONQUEUES' ) )
		
		currentLevel += 1
		
		theEntries.append( Entry( 'NormalQueues' ) )
		
		currentLevel += 1
		
		import serverimports as si
		queues = si.theExecutionQueue
		
		c = 0
		for q in queues:			
			theEntries.append( Entry( q.myName ) )
			
			currentLevel += 1
			
			d = 0
			for item in q.myQueueItems:
				if d == q.myCurrentItem:
					theEntries.append( Entry( '>%s' % item ) )
				else:
					theEntries.append( Entry( '%s' % item ) )
				d += 1
			
			currentLevel -= 1
			
			c += 1
		
		theEntries.append( Entry( 'End' ) )
		
		currentLevel -= 1
		
		theEntries.append( Entry( 'RougeQueues' ) )
		
		currentLevel += 1
		
		queues = si.theExpressList
		
		c = 0
		for q in queues:			
			theEntries.append( Entry( q.myName ) )
			
			currentLevel += 1
			
			d = 0
			for item in q.myQueueItems:
				if d == q.myCurrentItem:
					theEntries.append( Entry( '>%s' % item ) )
				else:
					theEntries.append( Entry( '%s' % item ) )
				d += 1
			
			currentLevel -= 1
			
			c += 1
		
		theEntries.append( Entry( 'End' ) )
		
		currentLevel -= 1
		
		currentLevel -= 1
	
	
	## INSTANCES
	if showInstances.Get():
		
		theEntries.append( Entry( 'INSTANCES' ) )
		
		currentLevel += 1
		
		import instance
		
		for inst_name in instance.theInstances:
			
			inst = instance.theInstances[inst_name]
			
			e = Entry( '%s' % inst.myName )
			e.myScreenPosition = GetCopy( inst.myPos )
			e.myScreenRadius = inst.myRadius
			e.AddMoveToAction()
			theEntries.append( e )
			
			currentLevel += 1
			
			e = Entry( 'Position', inst.myPos )
			e.myScreenPosition = GetCopy( inst.myPos )
			e.myScreenRadius = inst.myRadius
			e.AddMoveToAction()
			theEntries.append( e )
			
			e = Entry( 'Radius', inst.myRadius )
			e.myScreenPosition = GetCopy( inst.myPos )
			e.myScreenRadius = inst.myRadius
			e.AddMoveToAction()
			
			e.mySetFunction = inst.SetRadius
			e.mySetIncrData = inst.myRadius + 5
			e.mySetDecrData = inst.myRadius - 5

			theEntries.append( e )
			
			e = Entry( 'Type', inst.myType )
			e.myScreenPosition = GetCopy( inst.myPos )
			e.myScreenRadius = inst.myRadius
			e.AddMoveToAction()
			theEntries.append( e )
			
			currentLevel -= 1
		
		currentLevel -= 1
	
	
	
	## AREAEDITOR
	
	if showAreaEditor.Get():
		theEntries.append( Entry( 'AREAEDITOR' ) )
		
		currentLevel += 1
		
		theEntries.append( Entry( 'Areas' ) )
		
		currentLevel += 1
		
		e = Entry( 'CreateNewArea' )
		e.myOnClickActions.append( si.Action( AddNewArea ) )
		
		for a in theEditedAreas:
			e.myScreenPositionList.append( a.myPos )
			e.myScreenRadiusList.append( a.myRadius )
			e.myScreenNameList.append( a.myName )
			
		
		theEntries.append( e )

		e = Entry( 'SaveAreas' )
		e.myOnClickActions.append( si.Action( SaveAreas ) )
		theEntries.append( e )


		e = Entry( 'UpdateAreas' )
		e.myOnClickActions.append( si.Action( UpdateAreas ) )
		theEntries.append( e )
		
		c = 0
		for a in theEditedAreas:
			e = Entry( '%s' % a.myName )
			e.myScreenPosition = a.myPos
			e.myScreenRadius = a.myRadius	
			e.AddMoveToAction()
			
			global selectedArea
			e.myOnSelectedActions.append( si.Action( selectedArea.Set, c ) )
			e.myOnSelectionLostActions.append( si.Action( selectedArea.Set, -1 ) )
			
			theEntries.append( e )
			
			currentLevel += 1

			e = Entry( 'Remove' )
			e.myOnClickActions.append( si.Action( theEditedAreas.remove, a ) )
			theEntries.append( e )

			e = Entry( 'Update' )
			e.myOnClickActions.append( si.Action( UpdateArea, a ) )
			theEntries.append( e )

			
			e = Entry( 'Pos', a.myPos )
			e.myScreenPosition = a.myPos
			e.myScreenRadius = a.myRadius
			e.AddMoveToAction()
			theEntries.append( e )

			e = Entry( 'Radius', a.myRadius )
			e.myScreenPosition = a.myPos
			e.myScreenRadius = a.myRadius
			e.mySetFunction = a.SetRadius
			e.mySetIncrData = a.myRadius + 2
			e.mySetDecrData = a.myRadius - 2
			e.AddMoveToAction()
			theEntries.append( e )
			
			currentLevel -= 1
			c += 1


		currentLevel -= 1
		
		theEntries.append( Entry( 'CommandPoints' ) )		
		currentLevel += 1
		
		e = Entry( 'CreateNewCP' )
		e.myOnClickActions.append( si.Action( AddNewCommandPoint ) )
		
		for a in theEditedCommandpoints:
			e.myScreenPositionList.append( a.myPos )
			e.myScreenRadiusList.append( 0 )
			e.myScreenNameList.append( a.myName )
					
		theEntries.append( e )

		e = Entry( 'SaveCP' )
		e.myOnClickActions.append( si.Action( SaveCommandPoints ) )
		theEntries.append( e )		
		
		
		c = 0
		for a in theEditedCommandpoints:
			e = Entry( '%s' % a.myName )
			e.myScreenPosition = a.myPos
			e.myScreenRadius = a.myRadius	
			e.AddMoveToAction()
			
			global selectedCommandPoint
			e.myOnSelectedActions.append( si.Action( selectedCommandPoint.Set, c ) )
			e.myOnSelectionLostActions.append( si.Action( selectedCommandPoint.Set, -1 ) )
			
			theEntries.append( e )
			
			currentLevel += 1

			e = Entry( 'Remove' )
			e.myOnClickActions.append( si.Action( theEditedCommandpoints.remove, a ) )
			theEntries.append( e )

			e = Entry( 'Update' )
			e.myOnClickActions.append( si.Action( UpdateCommandPoint, a ) )
			theEntries.append( e )
			
			e = Entry( 'Pos', a.myPos )
			e.myScreenPosition = a.myPos
			e.myScreenRadius = a.myRadius
			e.AddMoveToAction()
			theEntries.append( e )

			e = Entry( 'AddPP' )
			e.myOnClickActions.append( si.Action( AddNewPerimeterPoint, a ) )
			theEntries.append( e )

			c2 = 0
			for pp in a.myPP:
				
				e = Entry( '%s' % pp.myName )
				e.myScreenPosition = pp.myPos
				e.myScreenRadius = pp.myRadius	
				e.AddMoveToAction()				

				global selectedPerimeterPoint
				e.myOnSelectedActions.append( si.Action( selectedPerimeterPoint.Set, c ) )
				e.myOnSelectionLostActions.append( si.Action( selectedPerimeterPoint.Set, -1 ) )

				
				theEntries.append( e )
				currentLevel += 1
				
				e = Entry( 'Remove' )
				e.myOnClickActions.append( si.Action( a.myPP.remove, pp ) )
				theEntries.append( e )

				e = Entry( 'Update' )
				e.myOnClickActions.append( si.Action( UpdatePerimeterPoint, pp ) )
				theEntries.append( e )
				# OnRightClick
				
				e = Entry( 'Pos', pp.myPos )
				e.myScreenPosition = pp.myPos
				e.myScreenRadius = pp.myRadius
				e.AddMoveToAction()
				theEntries.append( e )
								
				currentLevel -= 1
				c2 += 1
				
			currentLevel -= 1
			c += 1				
		
		
		currentLevel -= 1
	
		currentLevel -= 1
	
	
	## CIVILIANS
	
	
	if showCiviliansEditor.Get():
		
		global theCivilians
		global civDefaultRadius
		global civDefaultLifeTime
		global civDefaultNumberOfCivilians
		global civDefaultDelay

		
		theEntries.append( Entry( 'CIVILIANS' ) )
				
		currentLevel += 1
		
		#ASDFG
		
		e = Entry( 'CreateNewBatch' )
		e.myOnClickActions.append( si.Action( CreateNewCivilianBatch ) )
		e.myOnClickActions.append( si.Action( SaveCivilians ) )
		theEntries.append( e )

		e = Entry( 'Save Civilians' )
		e.myOnClickActions.append( si.Action( SaveCivilians ) )
		theEntries.append( e )
		
		
		e = Entry( 'Play All' )
		e.myOnClickActions.append( si.Action( PlayAllCivBatches ) )
		e.myOnClickActions.append( si.Action( SaveCivilians ) )
		theEntries.append( e )

		e = Entry( 'Stop All' )
		e.myOnClickActions.append( si.Action( StopAllCivBatches ) )
		theEntries.append( e )


		e = Entry( 'Settings' )
		theEntries.append( e )
				
		currentLevel += 1
		
		e = Entry( 'Default Radius(%f)' % civDefaultRadius )
		e.mySetFunction = SetDefaultRadius
		e.mySetIncrData = civDefaultRadius + 0.5
		e.mySetDecrData = civDefaultRadius - 0.5
		theEntries.append( e )
		
		e = Entry( 'Default LifeTime(%f)' % civDefaultLifeTime )
		e.mySetFunction = SetDefaultLifeTime
		e.mySetIncrData = civDefaultLifeTime + 1.0
		e.mySetDecrData = civDefaultLifeTime - 1.0
		theEntries.append( e )

		e = Entry( 'Default NumberOfCivilians(%d)' % (civDefaultNumberOfCivilians - 1) )
		e.mySetFunction = SetDefaultNumberOfCivilians
		e.mySetIncrData = civDefaultNumberOfCivilians + 1
		e.mySetDecrData = civDefaultNumberOfCivilians - 1
		theEntries.append( e )

		e = Entry( 'Default Delay(%f)' % civDefaultDelay )
		e.mySetFunction = SetDefaultDelay
		e.mySetIncrData = civDefaultDelay + 0.2
		e.mySetDecrData = civDefaultDelay - 0.2
		theEntries.append( e )

		e = Entry( 'Default Y Offset(%f)' % civDefaultY )
		e.mySetFunction = SetDefaultY
		e.mySetIncrData = civDefaultY + 0.01
		e.mySetDecrData = civDefaultY - 0.01
		theEntries.append( e )

		e = Entry( 'Default Y Offset(%f) - 1m' % civDefaultY )
		e.mySetFunction = SetDefaultY
		e.mySetIncrData = civDefaultY + 1.0
		e.mySetDecrData = civDefaultY - 1.0
		theEntries.append( e )

		
		currentLevel -= 1
		
		
		for c in theCivilians:
			e = Entry( c.myName )
			theEntries.append( e )

			currentLevel += 1
						
			e = Entry( 'Settings' )
			for c_e in c.myCivilians:
				e.myScreenPositionList.append( c_e.myStartPosition )
				e.myScreenRadiusList.append( c_e.myRadius )
				e.myScreenNameList.append( 'Start(%s)' % c_e.myName )

				e.myScreenPositionList.append( c_e.myDirection )
				e.myScreenRadiusList.append( 0 )
				e.myScreenNameList.append( 'Dest(%s)' % c_e.myName )
			theEntries.append( e )
			
			
			currentLevel += 1
			
			e = Entry( 'Default Radius(%f)' % c.myDefaultRadius )
			e.myOnClickActions.append( si.Action( c.ApplyRadiusToAll, c.myDefaultRadius ) )
			e.mySetFunction = c.SetDefaultRadius
			e.mySetIncrData = c.myDefaultRadius + 0.5
			e.mySetDecrData = c.myDefaultRadius - 0.5
			theEntries.append( e )
			
			e = Entry( 'Default LifeTime(%f)' % c.myDefaultLifeTime )
			e.myOnClickActions.append( si.Action( c.ApplyLifeTimeToAll, c.myDefaultLifeTime ) )
			e.mySetFunction = c.SetDefaultLifeTime
			e.mySetIncrData = c.myDefaultLifeTime + 1.0
			e.mySetDecrData = c.myDefaultLifeTime - 1.0
			theEntries.append( e )
	
			e = Entry( 'Default NumberOfCivilians(%d)' % (c.myDefaultNumberOfCivilians - 1) )
			e.myOnClickActions.append( si.Action( c.ApplyNumberOfCiviliansToAll, c.myDefaultNumberOfCivilians ) )
			e.mySetFunction = c.SetDefaultNumberOfCivilians
			e.mySetIncrData = c.myDefaultNumberOfCivilians + 1
			e.mySetDecrData = c.myDefaultNumberOfCivilians - 1
			theEntries.append( e )
	
			e = Entry( 'Default Delay(%f)' % c.myDefaultDelay )
			e.myOnClickActions.append( si.Action( c.ApplyDelayToAll, c.myDefaultDelay ) )
			e.mySetFunction = c.SetDefaultDelay
			e.mySetIncrData = c.myDefaultDelay + 0.2
			e.mySetDecrData = c.myDefaultDelay - 0.2
			theEntries.append( e )

			e = Entry( 'Default Y Offset(%f)' % c.myDefaultY )
			e.myOnClickActions.append( si.Action( c.ApplyYToAll, c.myDefaultY ) )
			e.mySetFunction = c.SetDefaultY
			e.mySetIncrData = c.myDefaultY + 0.01
			e.mySetDecrData = c.myDefaultY - 0.01
			theEntries.append( e )

			e = Entry( 'Default Y Offset(%f) - 1m' % c.myDefaultY )
			e.myOnClickActions.append( si.Action( c.ApplyYToAll, c.myDefaultY ) )
			e.mySetFunction = c.SetDefaultY
			e.mySetIncrData = c.myDefaultY + 1.0
			e.mySetDecrData = c.myDefaultY - 1.0
			theEntries.append( e )

			
			currentLevel -= 1
						
			e = Entry( 'Play(%s)' % VerifyCivBatch( c ) )
			e.myOnClickActions.append( si.Action( c.Play ) )
			e.myOnClickActions.append( si.Action( SaveCivilians ) )
			theEntries.append( e )


			e = Entry( 'Stop' )
			e.myOnClickActions.append( si.Action( c.Stop ) )
			theEntries.append( e )


			e = Entry( 'Remove Batch' )
			e.myOnClickActions.append( si.Action( RemoveCivBatch, c ) )
			theEntries.append( e )

			
			#currentLevel += 1

			
			e = Entry( 'CreateNewCivilian' )
			e.myOnClickActions.append( si.Action( CreateNewCivEntry, c ) )
			e.myOnClickActions.append( si.Action( SaveCivilians ) )
			theEntries.append( e )
			
			for civ_entry in c.myCivilians:
				e = Entry( civ_entry.myName )
				e.myScreenPosition = civ_entry.myStartPosition
				e.myScreenRadius = civ_entry.myRadius
				theEntries.append( e )

				currentLevel += 1

				e = Entry( 'Remove Civilian' )
				e.myOnClickActions.append( si.Action( RemoveCivEntry, c, civ_entry ) )
				theEntries.append( e )

				e = Entry( 'Copy Civilian to MousePos' )
				e.myOnClickActions.append( si.Action( CopyCivEntryToMouse, c, civ_entry ) )
				theEntries.append( e )

				e = Entry( 'Civilians' )
				theEntries.append( e )
				
				currentLevel += 1
				

				if showGroundCivilians.Get():
				
					from wicgame.civilians import ALL_ON_GROUND
					e = Entry( 'All On Ground' )
					theEntries.append( e )
	
					currentLevel += 1
					
					for cc in ALL_ON_GROUND:
						
						nr = civ_entry.myCivilians.count ( cc )
						
						e = Entry( '%s(%d)' % (cc, nr) )
						e.myOnClickActions.append( si.Action( SpawnPreviewCiv, cc ) )
						e.mySetFunction = civ_entry.AddCivilian
						e.mySetIncrData = [cc, True]
						e.mySetDecrData = [cc, False]
						theEntries.append( e )
	
					
					currentLevel -= 1

				
				if showHighCivilians.Get():
				
					from wicgame.civilians import ALL_HIGH
					e = Entry( 'All High' )
					theEntries.append( e )
	
					currentLevel += 1
	
					for cc in ALL_HIGH:
						
						nr = civ_entry.myCivilians.count ( cc )
						
						e = Entry( '%s(%d)' % (cc, nr) )
						e.myOnClickActions.append( si.Action( SpawnPreviewCiv, cc ) )
						e.mySetFunction = civ_entry.AddCivilian
						e.mySetIncrData = [cc, True]
						e.mySetDecrData = [cc, False]
						theEntries.append( e )
	
					
					currentLevel -= 1
				
				if showRoofCivilians.Get():
				
					from wicgame.civilians import HIGH_ON_ROOF
					e = Entry( 'All On Roof' )
					theEntries.append( e )
	
					currentLevel += 1
	
					for cc in HIGH_ON_ROOF:
						
						nr = civ_entry.myCivilians.count ( cc )
						
						e = Entry( '%s(%d)' % (cc, nr) )
						e.myOnClickActions.append( si.Action( SpawnPreviewCiv, cc ) )
						e.mySetFunction = civ_entry.AddCivilian
						e.mySetIncrData = [cc, True]
						e.mySetDecrData = [cc, False]
						theEntries.append( e )
	
					
					currentLevel -= 1
				
				
				currentLevel -= 1

				e = Entry( 'NrOfCivilians(%d)' % (civ_entry.myNumberOfCivilians - 1) )
				e.mySetFunction = civ_entry.SetNumberOfCivilians
				e.mySetIncrData = civ_entry.myNumberOfCivilians + 1.0
				e.mySetDecrData = civ_entry.myNumberOfCivilians - 1.0
				theEntries.append( e )

				
				e = Entry( 'Set Start(%s)' % civ_entry.myStartPosition )
				e.myScreenPosition = civ_entry.myStartPosition
				e.myScreenRadius = civ_entry.myRadius
				e.myOnClickActions.append( si.Action( civ_entry.SetEntryStart ) )
				theEntries.append( e )
				
				e = Entry( 'Set Direction(%s)' % civ_entry.myDirection )
				e.myScreenPosition = civ_entry.myDirection
				e.myOnClickActions.append( si.Action( civ_entry.SetEntryDirection ) )
				theEntries.append( e )

				e = Entry( 'LifeTime(%f)' % civ_entry.myLifeTime )
				e.mySetFunction = civ_entry.SetLifeTime
				e.mySetIncrData = civ_entry.myLifeTime + 1.0
				e.mySetDecrData = civ_entry.myLifeTime - 1.0
				theEntries.append( e )

				e = Entry( 'Radius(%f)' % civ_entry.myRadius )
				e.myScreenPosition = civ_entry.myStartPosition
				e.myScreenRadius = civ_entry.myRadius
				e.mySetFunction = civ_entry.SetRadius
				e.mySetIncrData = civ_entry.myRadius + 0.2
				e.mySetDecrData = civ_entry.myRadius - 0.2
				theEntries.append( e )

				e = Entry( 'Delay(%f)' % civ_entry.myDelay )
				e.mySetFunction = civ_entry.SetDelay
				e.mySetIncrData = civ_entry.myDelay + 0.5
				e.mySetDecrData = civ_entry.myDelay - 0.5
				theEntries.append( e )

				e = Entry( 'Y Offset(%f)' % civ_entry.myY )
				e.mySetFunction = civ_entry.SetY
				e.mySetIncrData = civ_entry.myY + 0.01
				e.mySetDecrData = civ_entry.myY - 0.01
				theEntries.append( e )

				e = Entry( 'Y Offset(%f) - 1m' % civ_entry.myY )
				e.mySetFunction = civ_entry.SetY
				e.mySetIncrData = civ_entry.myY + 1.0
				e.mySetDecrData = civ_entry.myY - 1.0
				theEntries.append( e )

				
				currentLevel -= 1
			
			
			currentLevel -= 1

	## AREAS
	
	if showAreas.Get():
	
		theEntries.append( Entry( 'AREAS' ) )
		
		currentLevel += 1
		
		import area
		
		for a in area.theAreas.myAreas:
			
			e = Entry( '%s' % a.myName )
			e.myScreenPosition = GetCopy( a.myPos )
			e.myScreenRadius = a.myRadius
			e.AddMoveToAction()
			theEntries.append( e )
			
			currentLevel += 1
			
			## POSITION
			e = Entry( 'Position', a.myPos )
			e.myScreenPosition = GetCopy( a.myPos )
			e.myScreenRadius = a.myRadius
			e.AddMoveToAction()
			theEntries.append( e )
			
			## RADIUS			
			e = Entry( 'Radius', a.myRadius )
			e.myScreenPosition = GetCopy( a.myPos )
			e.myScreenRadius = a.myRadius
			e.AddMoveToAction()

			e.mySetFunction = a.SetRadius
			e.mySetIncrData = a.myRadius + 5
			e.mySetDecrData = a.myRadius - 5

			theEntries.append( e )
			
			currentLevel -= 1
		
		currentLevel -= 1
	
	
	## AI
	
	if showAI.Get():
		import wicg
		
		theEntries.append( Entry( 'AI' ) )
		
		currentLevel += 1
		
		isDebugEnabled = False
		for i in range( 0, 16 ):
			
			try:
				isDebugEnabled = wicg.IsScriptDebugOutputAIEnable( i )
			except Exception, e:
				continue
			
			e = Entry( 'AI_%d' % i )
			theEntries.append( e )
			
			if not isDebugEnabled:
				e.myOnSelectedActions.append( Action( wicg.ScriptDebugOutputAIEnable, i ) )

			if isDebugEnabled:
				e.myOnSelectionLostActions.append( Action( wicg.ScriptDebugOutputAIDisable, i ) )
			
			currentLevel += 1
						
			e = Entry( 'EnableDebugOutput', isDebugEnabled )
			
			if isDebugEnabled:
				e.myOnClickActions.append( Action( wicg.ScriptDebugOutputAIDisable, i ) )
			else:
				e.myOnClickActions.append( Action( wicg.ScriptDebugOutputAIEnable, i ) )
			
			theEntries.append( e )
			
			currentLevel -= 1

		currentLevel -= 1
	
	
	
	CalculateAllUniqueStrings()


	## UPDATE SELECTION AND EXPANSION
	if currentEntry >= len( theEntries ):
		currentEntry = len( theEntries ) - 1
	
	counter = 0
	for entry in theEntries:
		if entry.myUniqueString == currentEntryStr:
			currentEntry = counter
		if entry.myUniqueString in theExpanded:
			entry.myIsExpanded = True
		counter += 1
			

def PrintEntries():
	global theEntries
	
	allowedLevel = 0
	prevLevel = 0
	visibleEntryCounter = 0
	for idx in range( len( theEntries ) ):
	
		entry = theEntries[idx]

		if entry.myIsExpanded and entry.myLevel <= allowedLevel:
			allowedLevel += 1
		if entry.myLevel < prevLevel:
			allowedLevel -= (prevLevel  - entry.myLevel)
	
		if entry.myLevel <= allowedLevel:
				
			if  visibleEntryCounter >= currentPrintOffset:
				expanded = 0
				
				if (idx + 1) < len( theEntries ):
					if entry.myLevel >= theEntries[ idx + 1 ].myLevel:
						expanded = 0
					elif entry.myIsExpanded:
						expanded = 2
					else:
						expanded = 1
			
				if idx == currentEntry:
					Print( entry, True, expanded )
				else:
					Print( entry, False, expanded )
						
			visibleEntryCounter += 1
			prevLevel = entry.myLevel


def Print( aEntry, aMarked, aExpandedMode = False ):
	global currentPositionX
	global currentPositionY
	
	try:
		import wicp
	except Exception:
		return
	
	if not doRender:
		return
	
	color = DEFAULT_COLOR
	
	text = aEntry.GetText()
	
	if aMarked:
		color = MARKED_COLOR
		
	if aExpandedMode == 1:
		text = '+%s' % text
	elif aExpandedMode == 2:
		text = '-%s' % text
	
	ClientCommand( 'PrintText', text, currentPositionX + (expansionWidth * aEntry.myLevel), currentPositionY, color )
	
	c = 0
	for a in aEntry.myScreenPositionList:
		
		if a == None:
			continue
		
		screenPos = wicp.World2Screen( a )
		
		if not screenPos is None:
			text = '<%s' % aEntry.myScreenNameList[c]
			ClientCommand( 'PrintText', text, screenPos[0], screenPos[1], SCREEN_MARKER_COLOR )
			
		if aEntry.myScreenRadiusList[c] > 0.0:
			
			import math
			
			nrOfMarkers = math.ceil( math.sqrt( aEntry.myScreenRadiusList[c] ) )
			nrOfMarkers += 1
			nrOfMarkers *= 2
			
			piSlice = 1.0 / nrOfMarkers
			pi2 = math.pi * 2
			for i in range( 1, nrOfMarkers + 1 ):
				
				worldPos = Position()				
				sliceSize = pi2 * (i * piSlice)
				
				worldPos.myX = a.myX + aEntry.myScreenRadiusList[c] * math.cos( sliceSize )
				worldPos.myY = a.myY
				worldPos.myZ = a.myZ + aEntry.myScreenRadiusList[c] * math.sin( sliceSize )
				
				screenPos = wicp.World2Screen( worldPos )
				
				if not screenPos is None:
					ClientCommand( 'PrintText', '*', screenPos[0], screenPos[1], SCREEN_MARKER_COLOR )
		
		c += 1
	
	
	if aMarked and aEntry.myScreenPosition:
		screenPos = wicp.World2Screen( aEntry.myScreenPosition )
		
		if not screenPos is None:
			text = '<%s' % aEntry.myValue
			ClientCommand( 'PrintText', text, screenPos[0], screenPos[1], SCREEN_MARKER_COLOR )
			
		if aEntry.myScreenRadius > 0.0:
			
			import math
			
			nrOfMarkers = math.ceil( math.sqrt( aEntry.myScreenRadius ) )
			nrOfMarkers += 1
			nrOfMarkers *= 2
			
			piSlice = 1.0 / nrOfMarkers
			pi2 = math.pi * 2
			for i in range( 1, nrOfMarkers + 1 ):
				
				worldPos = Position()				
				sliceSize = pi2 * (i * piSlice)
				
				worldPos.myX = aEntry.myScreenPosition.myX + aEntry.myScreenRadius * math.cos( sliceSize )
				worldPos.myY = aEntry.myScreenPosition.myY
				worldPos.myZ = aEntry.myScreenPosition.myZ + aEntry.myScreenRadius * math.sin( sliceSize )
				
				screenPos = wicp.World2Screen( worldPos )
				
				if not screenPos is None:
					ClientCommand( 'PrintText', '*', screenPos[0], screenPos[1], SCREEN_MARKER_COLOR )

	
	currentPositionY += TEXT_HEIGHT


def Update( ):
	global isActive
	global currentPositionX
	global currentPositionY
	global startPosition
	global theEntries
	global currentEntry
	global lastMousePressedTime
	global cursorPosLeft
	global cursorPosRight
	global leftMouseDown
	global rightMouseDown
	global currentPrintOffset
	global nextStepDown
	global nextStepUp
	global firstStepDown
	global firstStepUp

	
	try:
		import wicp
	except Exception:
		return
	
	if useAutoGroupNameView.Get():
		AutoViewGroupName()
	
	if not isActive:
		return
	
	if IsSinglePlayer():
				
		currentPositionX = startPosition.myX
		currentPositionY = startPosition.myY

		UpdateEntries()
		
		oldSelectedEntry = currentEntry
		
		cursorPosLeft = wicp.CheckMousePressed( MOUSE_LBUTTON )
		cursorPosRight = wicp.CheckMousePressed( MOUSE_RBUTTON )
		
		if cursorPosLeft and not leftMouseDown:
			HandleMousePressed( cursorPosLeft[0], cursorPosLeft[1], False )
			leftMouseDown = True
		
		if cursorPosLeft is None:
			leftMouseDown = False
			
		if cursorPosRight and not rightMouseDown:
			HandleMousePressed( cursorPosRight[0], cursorPosRight[1], True )
			rightMouseDown = True
		
		if cursorPosRight is None:
			rightMouseDown = False

		## UP and DOWN browsing explorer style
		if wicp.CheckKeyDown(KEY_UP):
			if nextStepUp < GetCurrentTime():
				PrevEntry()
				if firstStepUp:
					nextStepUp = GetCurrentTime() + 0.4
					firstStepUp = False
				else:
					nextStepUp = GetCurrentTime() + 0.03
		else:
			nextStepUp = GetCurrentTime()
			firstStepUp = True

		
		if wicp.CheckKeyDown(KEY_DOWN):
			if nextStepDown < GetCurrentTime():
				NextEntry()
				if firstStepDown:
					nextStepDown = GetCurrentTime() + 0.4
					firstStepDown = False
				else:
					nextStepDown = GetCurrentTime() + 0.03
		else:
			nextStepDown = GetCurrentTime()
			firstStepDown = True
			
			
		if wicp.CheckKeyPressed(KEY_RIGHT):
			theEntries[currentEntry].OnKeyRight()
			Expand()
			
		if wicp.CheckKeyPressed(KEY_LEFT):
			theEntries[currentEntry].OnKeyLeft()
			Collapse()

		if wicp.CheckKeyPressed(KEY_ENTER):
			theEntries[currentEntry].OnRightClick()
		
		if wicp.CheckKeyPressed(KEY_PAGEUP):
			currentPrintOffset -= 4
			if currentPrintOffset < 0:
				currentPrintOffset = 0
			
		if wicp.CheckKeyPressed(KEY_PAGEDOWN):
			currentPrintOffset += 4
			
		if wicp.CheckKeyPressed(KEY_HOME):
			currentPrintOffset = 0
			
		if useAutoGroupSelection.Get():
			AutoSelect()
				
		PrintEntries()
		
		if theEntries[oldSelectedEntry].myUniqueString != theEntries[currentEntry].myUniqueString:
			theEntries[oldSelectedEntry].OnSelectionLost()
			theEntries[currentEntry].OnSelected()


def NextEntry():
	global theEntries
	global currentEntry
	
	entryCounter = currentEntry
	
	if (currentEntry + 1) >= len( theEntries ) or len( theEntries ) < 2:
		return
	
	if IsExpanded( currentEntry ):
		currentEntry += 1
	else:
		entryCounter += 1		
				
		while theEntries[currentEntry].myLevel < theEntries[entryCounter].myLevel:
			entryCounter += 1
			
			if entryCounter >= len( theEntries ):
				return
		
		currentEntry = entryCounter
		
	
def PrevEntry():
	global theEntries
	global currentEntry
		
	allowedLevel = 0
	prevLevel = 0
	lastEntryPrinted = 0
	
	for idx in range( len( theEntries ) ):
		entry = theEntries[idx]
		if entry.myIsExpanded and entry.myLevel <= allowedLevel:
			allowedLevel += 1
		if entry.myLevel < prevLevel:
			allowedLevel -= (prevLevel  - entry.myLevel)
			
		## print entry
		if entry.myLevel <= allowedLevel:
		
			if idx == currentEntry:
				currentEntry = lastEntryPrinted
				return
			
			lastEntryPrinted = idx
			prevLevel = entry.myLevel


def Expand():
	global theEntries
	global theExpanded
	
	if (currentEntry + 1) >= len( theEntries ):
		return
	
	if theEntries[currentEntry + 1].myLevel > theEntries[currentEntry].myLevel:
		theEntries[currentEntry].myIsExpanded = True
		
		expStr = CalculateUniqueString( currentEntry )
		
		if not expStr in theExpanded:
			theExpanded.append( Expanded( expStr ) )


def Collapse():
	global theEntries
	global theExpanded
	
	theEntries[currentEntry].myIsExpanded = False

	expStr = CalculateUniqueString( currentEntry )

	if expStr in theExpanded:
		theExpanded.remove( expStr )



def CalculateAllUniqueStrings():
	global theEntries
	
	parentStrings = []
	
	nextIndex = 0
	for entry in theEntries:		
		entry.myUniqueString = entry.myValue
		
		for i in range( len( parentStrings ) - 1, -1, -1 ):
			entry.myUniqueString += parentStrings[i]
		
		nextIndex += 1
		
		if nextIndex < len( theEntries ):
			
			levelDiff = theEntries[nextIndex].myLevel - entry.myLevel
			
			if levelDiff > 0:
				parentStrings.append( entry.myValue )
			elif levelDiff < 0:
				for i in range( levelDiff, 0 ):
					if len( parentStrings ):
						parentStrings.pop()



def CalculateUniqueString( aEntryIndex ):
	global theEntries
	
	expStr = '%s' % theEntries[aEntryIndex].myValue
	
	currentEntry = aEntryIndex
	for c in range( aEntryIndex, 0, -1 ):
		if theEntries[c].myLevel < theEntries[currentEntry].myLevel:
			expStr += '%s' % theEntries[c].myValue
			currentEntry = c
	
	return expStr


def HandleMousePressed( x, y, rightClick = False ):
	global currentEntry
	
	allowedLevel = 0
	prevLevel = 0
	
	if x < mouseStartPosX or x > mouseStartPosX + mouseTextWidth or y < mouseStartPosY:
		return
		
	indx = (int)((y - mouseStartPosY) / mouseTextHeight)
	#indx += currentPrintOffset
	
	stepCounter = 0
	visibleEntryCounter = 0
	for idx in range( len( theEntries ) ):
		entry = theEntries[idx]
	
		if entry.myIsExpanded and entry.myLevel <= allowedLevel:
			allowedLevel += 1
		if entry.myLevel < prevLevel:
			allowedLevel -= (prevLevel  - entry.myLevel)
	
		if entry.myLevel <= allowedLevel:
			
			if  visibleEntryCounter >= currentPrintOffset:
		
				if indx == stepCounter:
					currentEntry = idx
					
					if rightClick:
						theEntries[currentEntry].OnRightClick()
					else:
						if theEntries[currentEntry].myIsExpanded:
							Collapse()
						else:
							Expand()				
					return
					
				stepCounter += 1
			
			visibleEntryCounter += 1
			prevLevel = entry.myLevel


def AutoSelect():
	global theGroups
	global theEntries
	global currentEntry
	global theExpanded
	global lastAutoSelectedGroup
	
	try:
		import wicp
	except Exception:
		return
	
	
	unitId = wicp.GetSelectedUnit()
	
	if unitId == -1:
		return
	
	
	grpName = theGroups.GetNameByUnit( unitId )
	
	if grpName == None or grpName == lastAutoSelectedGroup:
		return
		
	
	counter = 0
	newEntry = currentEntry
	for entry in theEntries:
		
		entryValue = ''
		c = 0
		while c < len(entry.myValue) and entry.myValue[c] != '(':
			entryValue += entry.myValue[c]
			c += 1
			
		if grpName == entryValue:
			newEntry = counter
			break
			
		counter += 1
	
	if newEntry != currentEntry:
		currentEntry = newEntry
		lastAutoSelectedGroup = grpName
		
		##expand upwards
		c = currentEntry
		level = theEntries[currentEntry].myLevel
		while c > 0:
			
			if theEntries[c].myLevel < level:
				s = CalculateUniqueString( c )
				
				if not s in theExpanded:
					theExpanded.append( s )
					theEntries[c].myIsExpanded = True
				level = theEntries[c].myLevel
			
			c -= 1


def AutoViewGroupName():
	global theGroups
	
	try:
		import wicp
	except Exception:
		return
		
	import unit
	
	
	unitId = wicp.GetSelectedUnit()
	
	if unitId == -1:
		return
	
	grp = theGroups.GetGroupByUnit( unitId )
	
	if grp == None:
		return
	
	pos = unit.theUnits[unitId].myPos
	screenPos = wicp.World2Screen( pos )
	
	if not screenPos is None:
		ClientCommand( 'PrintTextBig', '<%s(%d/%d)' % (grp.myName, grp.Size(), grp.Size( True )), screenPos[0], screenPos[1], SCREEN_MARKER_COLOR )



########################################################################

def UpdateAreas( ):
	global theEditedAreas

	allLines = [ ]
	count = 0
		
	filePath = 'maps\\%s\\python\\' % wicg.GetMapName()
	
	try:
		f = file( filePath + 'saved_areas.txt', 'r' )
	except IOError:
		return
	
	if not f:
		return
		
	theEditedAreas = []
	 	
	allLines = f.readlines()
	f.close()
	 
	for line in allLines:
		if line.startswith( 'WicedAreaInstance' ):
			aName = line[18:]
			aName = aName.rstrip( )
			myX = allLines[ count+4 ].lstrip( )
			myX = myX.lstrip( 'myX ' )
			myY = allLines[ count+5 ].lstrip( )
			myY = myY.lstrip( 'myY ' )
			myZ = allLines[ count+6 ].lstrip( )
			myZ = myZ.lstrip( 'myZ ' )
			aPosition = Position( myX, myY, myZ )
			aRadius = allLines[ count+9 ].lstrip( )
			aRadius = aRadius.lstrip( 'myRadius ' )
			
			theEditedAreas.append( EditorArea( aName, aPosition, float( aRadius ) ) )
			
		count += 1		
	
	SaveAreas( )
	LoadAreas( )
	
	del allLines
	del count


