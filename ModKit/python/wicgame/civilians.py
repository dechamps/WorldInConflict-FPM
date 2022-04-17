from serverimports import *

ALL_WALKING = ( 'F_Walk1', 'F_Walk2', 'F_Walk3', 'F_Walk4', 'F_Walk5', 'F_Walk6', \
				'Fam1', 'Fam2', 'Fam3', 'Fam4', 'Fam5', 'Fam6', 'Fam7', \
				'M_Walk1', 'M_Walk2', 'M_Walk3', 'M_Walk4', 'M_Walk5', 'M_Walk6', 'M_Walk7', 'M_Walk8', 'M_Walk9', 'M_Walk10', \
				'M_Wounded1', 'M_Wounded2', 'M_Wounded3', 'M_Wounded4', \
				'Par1', 'Par2', 'Par3', 'Par4', 'Par5', 'Par6' )
ALL_RUNNING = ( 'B_Run', \
				'F_Jog1', 'F_Jog2', 'F_Jog3', \
				'F_Runcrouched1', 'F_Runcrouched2', 'F_Runcrouched3', 'F_Runcrouched4', \
				'G_Run1', 'G_Run2', \
				'M_Jog1', 'M_Jog2', 'M_Jog3', \
				'M_Run1', 'M_Run2', \
				'M_Runcrouched1', 'M_Runcrouched2', 'M_Runcrouched3', 'M_Runcrouched4', 'M_Runcrouched5', 'M_Runcrouched6' )
ALL_MOTORIZED = ( 'Sedan', 'StationWagon', 'Pickup', 'Citybus', 'Van', 'Bike' )


HIGH_ALL_WALKING = ( 'HIGH_F_Walk1', 'HIGH_F_Walk2', 'HIGH_F_Walk3', 'HIGH_F_Walk4', 'HIGH_F_Walk5', 'HIGH_F_Walk6', \
				'HIGH_Fam1', 'HIGH_Fam2', 'HIGH_Fam3', 'HIGH_Fam4', 'HIGH_Fam5', 'HIGH_Fam6', 'HIGH_Fam7', \
				'HIGH_M_Walk1', 'HIGH_M_Walk2', 'HIGH_M_Walk3', 'HIGH_M_Walk4', 'HIGH_M_Walk5', 'HIGH_M_Walk6', 'HIGH_M_Walk7', 'HIGH_M_Walk8', 'HIGH_M_Walk9', 'HIGH_M_Walk10', \
				'HIGH_M_Wounded1', 'HIGH_M_Wounded2', 'HIGH_M_Wounded3', 'HIGH_M_Wounded4', \
				'HIGH_Par1', 'HIGH_Par2', 'HIGH_Par3', 'HIGH_Par4', 'HIGH_Par5', 'HIGH_Par6' )
HIGH_ALL_RUNNING = ( 'HIGH_B_Run', \
				'HIGH_F_Jog1', 'HIGH_F_Jog2', 'HIGH_F_Jog3', \
				'HIGH_F_Runcrouched1', 'HIGH_F_Runcrouched2', 'HIGH_F_Runcrouched3', 'HIGH_F_Runcrouched4', \
				'HIGH_G_Run1', 'HIGH_G_Run2', \
				'HIGH_M_Jog1', 'HIGH_M_Jog2', 'HIGH_M_Jog3', \
				'HIGH_M_Run1', 'HIGH_M_Run2', \
				'HIGH_M_Runcrouched1', 'HIGH_M_Runcrouched2', 'HIGH_M_Runcrouched3', 'HIGH_M_Runcrouched4', 'HIGH_M_Runcrouched5', 'HIGH_M_Runcrouched6' )
HIGH_ALL_MOTORIZED = ( 'HIGH_Sedan', 'HIGH_StationWagon', 'HIGH_Pickup', 'HIGH_Citybus', 'HIGH_Van', 'HIGH_Bike' )


HIGH_ON_ROOF = ( 'Roof_Female_01', 'Roof_Female_02', 'Roof_Male_01', 'Roof_Male_02', 'Roof_Male_03' )


ALL_HIGH = HIGH_ALL_WALKING + HIGH_ALL_RUNNING + HIGH_ALL_MOTORIZED

ALL_NONMOTORIZED = ALL_WALKING + ALL_RUNNING
ALL_ON_GROUND = ALL_WALKING + ALL_RUNNING + ALL_MOTORIZED
ALL_CIVS = ALL_WALKING + ALL_RUNNING + ALL_MOTORIZED + ALL_HIGH
TotalCivCount = len( ALL_CIVS )


CIV_SOUNDS = {\
	'F_Walk1' : 'civ_walk_01', 'F_Walk2' : 'civ_walk_02', 'F_Walk3' : 'civ_walk_03', 'F_Walk4' : 'civ_walk_04', 'F_Walk5' : 'civ_walk_05', 'F_Walk6' : 'civ_walk_01', \
	'Fam1' : 'civ_walk_02', 'Fam2' : 'civ_walk_03', 'Fam3' : 'civ_walk_04', 'Fam4' : 'civ_walk_05', 'Fam5' : 'civ_walk_01', 'Fam6' : 'civ_walk_02', 'Fam7' : 'civ_walk_03', \
	'M_Walk1' : 'civ_walk_04', 'M_Walk2' : 'civ_walk_05', 'M_Walk3' : 'civ_walk_01', 'M_Walk4' : 'civ_walk_02', 'M_Walk5' : 'civ_walk_03', 'M_Walk6' : 'civ_walk_04', 'M_Walk7' : 'civ_walk_05', 'M_Walk8' : 'civ_walk_01', 'M_Walk9' : 'civ_walk_02', 'M_Walk10' : 'civ_walk_03', \
	'M_Wounded1' : 'civ_walk_04', 'M_Wounded2' : 'civ_walk_05', 'M_Wounded3' : 'civ_walk_01', 'M_Wounded4' : 'civ_walk_02', \
	'Par1' : 'civ_walk_03', 'Par2' : 'civ_walk_04', 'Par3' : 'civ_walk_05', 'Par4' : 'civ_walk_01', 'Par5' : 'civ_walk_02', 'Par6' : 'civ_walk_03', \
	\
	'B_Run' : 'civ_run_01', \
	'F_Jog1' : 'civ_run_02', 'F_Jog2' : 'civ_run_01', 'F_Jog3' : 'civ_run_02', \
	'F_Runcrouched1' : 'civ_run_01', 'F_Runcrouched2' : 'civ_run_02', 'F_Runcrouched3' : 'civ_run_01', 'F_Runcrouched4' : 'civ_run_02', \
	'G_Run1' : 'civ_run_01', 'G_Run2' : 'civ_run_02', \
	'M_Jog1' : 'civ_run_01', 'M_Jog2' : 'civ_run_02', 'M_Jog3' : 'civ_run_01', \
	'M_Run1' : 'civ_run_02', 'M_Run2' : 'civ_run_01', \
	'M_Runcrouched1' : 'civ_run_02', 'M_Runcrouched2' : 'civ_run_01', 'M_Runcrouched3' : 'civ_run_02', 'M_Runcrouched4' : 'civ_run_01', 'M_Runcrouched5' : 'civ_run_02', 'M_Runcrouched6' : 'civ_run_01', \
	\
	'Sedan' : 'civ_veh_01', 'StationWagon' : 'civ_veh_02', 'Pickup' : 'civ_veh_03', 'Citybus' : 'civ_veh_01', 'Van' : 'civ_veh_02', 'Bike' : 'civ_veh_03', \
	\
	'Roof_Female_01' : 'civ_walk_01', 'Roof_Female_02' : 'civ_walk_02', 'Roof_Male_01' : 'civ_walk_03', 'Roof_Male_02' : 'civ_walk_04', 'Roof_Male_03' : 'civ_walk_05' }



def SpawnCiviliansInClump( SpawnPosition, Destination, NumberOfCivilians = TotalCivCount, LifeTime = 180, CiviliansToSpawn = None, Deviation = 15, Style = 'All' ):
	"""
	<====================================================================>
	
	SpawnPosition
	=-> General location where the civilians are spawned
	
	Destination
	=-> A location where the civilians will walk to
	
	NumberOfCivilians 
	-- Defaults to 37 civilians
	=-> How many civilians do you want to spawn
	
	LifeTime 
	-- Defauts to 180
	=-> The time in seconds that the civilians will exist
	
	CiviliansToSpawn 
	-- Defaults to the ALL_CIVS Tuple
	=-> Specify a Tuple to Spawn from that ordered sequence
	
	Deviation 
	-- Defaults to 20
	=-> Radius within civilians spawn
	
	Style
	-- Defaults to 'All'
	=-> Specify the type of civs to spawn 'All', 'Walking', 'Running', 'NonMotorized', or 'Motorized'
	"""

	if SpawnPosition is None or Destination is None:
		return []

	if CiviliansToSpawn == None:
		if Style == 'All':
			ListOfCivsToSpawn = list( ALL_CIVS )
			random.shuffle( ListOfCivsToSpawn )
		elif Style == 'Walking':
			ListOfCivsToSpawn = list( ALL_WALKING )
			random.shuffle( ListOfCivsToSpawn )
		elif Style == 'Running':
			ListOfCivsToSpawn = list( ALL_RUNNING )
			random.shuffle( ListOfCivsToSpawn )
		elif Style == 'NonMotorized':
			ListOfCivsToSpawn = list( ALL_NONMOTORIZED )
			random.shuffle( ListOfCivsToSpawn )
		elif Style == 'Motorized':
			ListOfCivsToSpawn = list( ALL_MOTORIZED )
			random.shuffle( ListOfCivsToSpawn )
		else:
			raise ValueError, 'Style must be All, Walking, Running, Motorized'
	else:
		ListOfCivsToSpawn = CiviliansToSpawn
		
	count = 1
	lenOfCivList = len( ListOfCivsToSpawn )
	
	if lenOfCivList == 0:
		return []
	
	ids = []
	
	import serverimports as si
	
	delay = 0.0
	isFirstCivilian = True
	while count < NumberOfCivilians :
		civType = ListOfCivsToSpawn[ ( count % lenOfCivList) ]
		
		## only use sound on the first civilian
		#if isFirstCivilian:
		#	if civType.rfind( 'HIGH_' ) != -1:
		#		civNameForSound = civType[5:]
		#	else:
		#		civNameForSound = civType
		#	
		#	SOUND = CIV_SOUNDS[civNameForSound]
		#else:
		#	SOUND = None
		
		##use delay to prevent stalls when spawning lots of civilians
		si.Delay( delay, si.Action( thePlayers[ PLAYER_HUMAN ].CreateGenericModel, civType, wicmath.CalculateRandomBoxPosition( SpawnPosition, Deviation ), LifeTime, wicmath.GetDirection( SpawnPosition, Destination ) ) )

		count += 1
		delay += 0.1
		isFirstCivilian = False
	
	return ids

		
def SpawnCiviliansAlongStrip( SpawnPositionA, SpawnPositionB, StripWidth, Destination, NumberOfCivilians = TotalCivCount, LifeTimeA = 150, LifeTimeB = 180, CiviliansToSpawn = None, Style = 'All' ):
	"""
	<====================================================================>
	
	SpawnPosition
	=-> General location where the civilians are spawned
	
	Destination
	=-> A location where the civilians will walk to
	
	NumberOfCivilians 
	-- Defaults to 37 civilians
	=-> How many civilians do you want to spawn
	
	LifeTime 
	-- Defauts to 180
	=-> The time in seconds that the civilians will exist
	
	CiviliansToSpawn 
	-- Defaults to the ALL_CIVS Tuple
	=-> Specify a Tuple to Spawn from that ordered sequence
	
	Deviation 
	-- Defaults to 20
	=-> Radius within civilians spawn
	
	Style
	-- Defaults to 'All'
	=-> Specify the type of civs to spawn 'All', 'Walking', 'Running', 'NonMotorized', or 'Motorized'
	"""

	if CiviliansToSpawn == None :
		if Style == 'All':
			ListOfCivsToSpawn = list( ALL_CIVS )	
			random.shuffle( ListOfCivsToSpawn )
		elif Style == 'Walking':
			ListOfCivsToSpawn = list( ALL_WALKING )
			random.shuffle( ListOfCivsToSpawn )
		elif Style == 'Running':
			ListOfCivsToSpawn = list( ALL_RUNNING )
			random.shuffle( ListOfCivsToSpawn )
		elif Style == 'NonMotorized':
			ListOfCivsToSpawn = list( ALL_NONMOTORIZED )
			random.shuffle( ListOfCivsToSpawn )			
		elif Style == 'Motorized':
			ListOfCivsToSpawn = list( ALL_MOTORIZED )
			random.shuffle( ListOfCivsToSpawn )
		else:
			raise ValueError, 'Style must be All, Walking, Running, Motorized'
	else:
		ListOfCivsToSpawn = CiviliansToSpawn
		
	count = 1
	lenOfCivList = len( ListOfCivsToSpawn )
		
	while count < NumberOfCivilians :
		civType = ListOfCivsToSpawn[ ( count % lenOfCivList) ]			
		thePlayers[ PLAYER_HUMAN ].CreateGenericModel( civType, wicmath.CalculateRandomPositionInStrip( SpawnPositionA, SpawnPositionB, StripWidth ), random.randint( LifeTimeA, LifeTimeB ), wicmath.GetDirection( SpawnPositionA, Destination ) )
		count += 1


		
class CivilianGenerator:
	"""
	<====================================================================>
	Slowly spawns civilians over a period of time
	
	Required Arguments:
	------------------
	
	SpawnPosition
	=-> General location where the civilians are spawned
	
	Destination
	=-> A location where the civilians will walk to
	
	Defaults to one Civilian at a time per 5 seconds
	
	TotalSpawnTime
	=-> The time span to spawn during
	
	TimeBetweenSpawns = 5
	=-> The time between each spawn
	
	CivsPerSpawn = 1
	=-> The number of civilians to spawn at a time
	
	"""


	def __init__( self, SpawnPosition, Destination, TotalSpawnTime, TimeBetweenSpawns = 5, CivsPerSpawn = 1 ):
		self.__SpawnPosition = SpawnPosition
		self.__Destination = Destination
		self.__TotalSpawnTime = TotalSpawnTime
		self.__TimeBetweenSpawns = TimeBetweenSpawns
		self.__CivsPerSpawn = CivsPerSpawn
		self.__LifeTime = 180
		self.__CiviliansTuple = None
		self.__SpawnDeviation = 0
		
		
	def ChangeSpawnPosition( self, newPosition ):
		self.__SpawnPosition = newPosition

		
	def ChangeDestination( self, newDestination ):
		self.__Destination = newDestination
		
		
	def SetLifeTime( self, newTime ):
		self.__LifeTime = newTime

		
	def SetCiviliansToSpawn( self, newCivilianTuple ):
		self.__CiviliansTuple = newCivilianTuple

		
	def SetSpawnRadius( self, newDeviation ):
		self.__newDeviation = newDeviation

		
	def Start( self ):
		if self.__TotalSpawnTime < self.__TimeBetweenSpawns :
			raise ValueError, 'TotalSpawnTime must be >= self.TimeBetweenSpawns'
		civRepeater = Repeat( self.__TimeBetweenSpawns, Action( SpawnCivilians, self.__SpawnPosition, self.__Destination, self.__CivsPerSpawn, self.__LifeTime, self.__CiviliansTuple, self.__SpawnDeviation ) )
		civRepeater.myRepeating = True
		civRepeater.myNrOfExecutions = int( self.__TotalSpawnTime ) / int( self.__TimeBetweenSpawns )
		civRepeater.Execute( )


		