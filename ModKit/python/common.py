""" Common modules with definitions of standard object types.

	This module defines various classes to be used in WIC scripting.
"""
import building
import debug
import game
import instance
import player
import team
import unit
import gameobject
import unittypes
import base


from building import Building, theBuildings
from instance import Instance
from position import Position
from unit import Unit
from game import Game


# colors as ints
BLACK = 0x000000
WHITE = 0xffffff


OBJ_NEW = 'new'
OBJ_COMPLETED = 'completed'
OBJ_SECONDARY = 'secondary'
OBJ_FAILED = 'failed'


def ListInList( aSmallList, aBigList ):
	for item in aSmallList:
		if not item in aBigList:
			return False
	return True

def ListDiff( anAList, aBList, aSkipBCheckFlag = False ):
	"""
	"""
	missingFromA = []
	missingFromB = []

	for entry in anAList:
		if not entry in aBList:
			missingFromA.append( entry )

	if not aSkipBCheckFlag:
		for entry in aBList:
			if not entry in anAList:
				missingFromB.append( entry )

	return missingFromA, missingFromB


def GetPosition(aTarget):
	""" Converts aTarget to a Position.

	Args:
	 aTarget - (Position|Instance|String|Unit|Group)

	Returns:
	 A Position
	 
	"""
	if isinstance( aTarget, str ):
		aTarget = instance.theInstances[aTarget]

	return aTarget.__pos__()


def IsInfantryType(aUnitType):
	return (aUnitType in unittypes.infantryUS or aUnitType in unittypes.infantryNATO or aUnitType in unittypes.infantryUSSR)


def IsInfantry(aUnitId):
	""" Check if a unit is infantry.

	Args:
	 aUnitType - (int) The unittype to check.

	Returns:
	 Returns True if aUnitType is an infatery unit otherwise False.
	"""

	type = 	unit.theUnits[aUnitId].myType

	return (type in unittypes.infantryUS or type in unittypes.infantryNATO or type in unittypes.infantryUSSR)


def IsAir(aUnitId):
	""" Check if a unit is air.

	Args:
	 aUnitType - (int) The unittype to check.

	Returns:
	 Returns True if aUnitType is an air unit otherwise False.
	"""

	type = 	unit.theUnits[aUnitId].myType

	return (type in unittypes.airUS or type in unittypes.airNATO or type in unittypes.airUSSR)


def IsTank(aUnitId):
	""" Check if a unit is a tank.

	Args:
	 aUnitType - (int) The unittype to check.

	Returns:
	 Returns True if aUnitType is a tank unit otherwise False.
	"""

	type = 	unit.theUnits[aUnitId].myType

	return (type in unittypes.tanksUS or type in unittypes.tanksNATO or type in unittypes.tanksUSSR)


def IsArtillery(aUnitId):
	""" Check if a unit is an artillery unit.

	Args:
	 aUnitType - (int) The unittype to check.

	Returns:
	 Returns True if aUnitType is an artillery unit otherwise False.
	"""

	type = unit.theUnits[aUnitId].myType

	return (type in unittypes.artilleryUS or type in unittypes.artilleryNATO or type in unittypes.artilleryUSSR)


def IsContainer(aUnitId):
	"""
	"""

	type = unit.theUnits[aUnitId].myType

	return (type in unittypes.containerUS or type in unittypes.containerNATO or type in unittypes.containerUSSR)



def SetPrimaryObjective( aName, aState = OBJ_NEW ):
	"""
	"""

	player.thePlayers[1].SetObjective( aName, aState, 'primary' )
	#player.thePlayers[1].SetObjective( base.StringToInt( aName ), 'primary', aState )


def SetPrimarySubObjective( aName, aState = OBJ_NEW ):
	"""
	"""

	player.thePlayers[1].SetObjective( aName, aState, 'primarysub' )
	#player.thePlayers[1].SetObjective( base.StringToInt( aName ), 'primarysub', aState )


def SetSecondaryObjective( aName, aState = OBJ_NEW ):
	"""
	"""
	player.thePlayers[1].SetObjective( aName, aState, 'secondary' )
	#player.thePlayers[1].SetObjective( base.StringToInt( aName ), 'secondary', aState )
