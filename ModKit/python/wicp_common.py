import wicp

from position import Position
from wico_common import *


def GetPosition( aTarget ):
	""" Converts aTarget to a Position.

	Args:
	 aTarget - (Position|String)

	Returns:
	 A Position
	 
	"""
	
	if isinstance( aTarget, str ):
		return wicp.GetInstancePosition( aTarget )
	elif isinstance( aTarget, Position ):
		return aTarget
	
	return aTarget.__pos__()


def GetRadius( aTarget ):
	""" Fetches the radius from aTarget.

	Args:
	 aTarget - (float|int|String)

	Returns:
	 A float
	 
	"""
	
	if isinstance( aTarget, float ):
		return aTarget
	elif isinstance( aTarget, int ):
		return float(aTarget)
	elif isinstance( aTarget, str ):
		return wicp.GetInstanceRadius( aTarget )
	
	return aTarget.__radius__()

