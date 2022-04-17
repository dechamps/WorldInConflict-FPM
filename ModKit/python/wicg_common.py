import game
import instance
import player
import unit
import unittypes

from instance import Instance
from position import Position
from unit import Unit
from game import Game

from wico_common import *


def GetPosition( aTarget ):
	""" Converts aTarget to a Position.

	Args:
	 aTarget - (Position|Instance|String|Unit|Group)

	Returns:
	 A Position
	 
	"""
	if isinstance( aTarget, str ):
		aTarget = instance.theInstances[aTarget]

	return aTarget.__pos__()


def GetRadius( aTarget ):
	""" Fetches the radius from aTarget.

	Args:
	 aTarget - (float|int|Instance|String|Area)

	Returns:
	 A float
	 
	"""
	
	if isinstance( aTarget, float ):
		return aTarget
	elif isinstance( aTarget, int ):
		return float(aTarget)
	elif isinstance( aTarget, str ):
		aTarget = instance.theInstances[aTarget]

	return aTarget.__radius__()

	
def GetArea( aTarget ):
	""" Converts aTarget to an Area.

	Args:
	 aTarget - (Instance|String|Area)

	Returns:
	 an Area
	 
	"""
	
	if isinstance( aTarget, str ):
		aTarget = instance.theInstances[aTarget]

	return aTarget.__area__()

	

def IsInfantryType( aUnitType ):
	return ( aUnitType in unittypes.infantryUS or aUnitType in unittypes.infantryNATO or aUnitType in unittypes.infantryUSSR )


def IsInfantry( aUnitId ):
	""" Check if a unit is infantry.

	Args:
	 aUnitType - (int) The unittype to check.

	Returns:
	 Returns True if aUnitType is an infatery unit otherwise False.
	"""

	unitType = unit.theUnits[aUnitId].myType

	return ( unitType in unittypes.infantryUS or unitType in unittypes.infantryNATO or unitType in unittypes.infantryUSSR )



def IsSquadUnitType( aUnitType ):
	""" Check if a unit is a squad spawner unit.
	"""

	return ( aUnitType in unittypes.squadUS or aUnitType in unittypes.squadNATO or aUnitType in unittypes.squadUSSR )
	

def IsTank( aUnitId ):
	""" Check if a unit is a tank.

	Args:
	 aUnitType - (int) The unittype to check.

	Returns:
	 Returns True if aUnitType is a tank unit otherwise False.
	"""

	unitType = unit.theUnits[aUnitId].myType

	return ( unitType in unittypes.tanksUS or unitType in unittypes.tanksNATO or unitType in unittypes.tanksUSSR )


def IsArtillery( aUnitId ):
	""" Check if a unit is an artillery unit.

	Args:
	 aUnitType - (int) The unittype to check.

	Returns:
	 Returns True if aUnitType is an artillery unit otherwise False.
	"""

	unitType = unit.theUnits[aUnitId].myType

	return ( unitType in unittypes.artilleryUS or unitType in unittypes.artilleryNATO or unitType in unittypes.artilleryUSSR )


def IsRepairUnit( aUnitId ):
	"""
	"""

	type = unit.theUnits[aUnitId].myType

	return ( type in unittypes.repairUS or type in unittypes.repairNATO or type in unittypes.repairUSSR )



def IsContainer( aUnitId ):

	unitType = unit.theUnits[aUnitId].myType

	return ( unitType in unittypes.containerUS or unitType in unittypes.containerNATO or unitType in unittypes.containerUSSR )


def IsAir( aUnitId ):

	unitType = unit.theUnits[aUnitId].myType

	return ( unitType in unittypes.airUS or unitType in unittypes.airNATO or unitType in unittypes.airUSSR )


def IsRadarScan( aUnitId ):
	
	## we are not using radar scan units anymore
	#unitType = unit.theUnits[aUnitId].myType
	#return ( unitType == unittypes.RADAR_SCAN_LEVEL_1 or unitType == unittypes.RADAR_SCAN_LEVEL_2 or unitType == unittypes.RADAR_SCAN_LEVEL_3 )	
	return False
