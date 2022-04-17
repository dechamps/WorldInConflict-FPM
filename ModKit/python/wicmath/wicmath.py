import math
import random
import debug

from vector import Vector
from position import Position


def Vector2Position(aVec):
    
	""" Converts a Vector to a Position.
	
	Args:
	aVec - (Vector) The vector to convert
	
	Returns:
	The Position corresponding to the given vector
	"""
	
	return Position(aVec.myX, 0.0, aVec.myZ)


def Position2Vector(aPos):
	""" Converts a Position to a Vector.
	
	Args:
			aPos - (Position) The position to convert
	
	Returns:
			The Vector corresponding to the given position
	"""
	
	return Vector(aPos.myX, aPos.myZ)
	
	
def Distance(aPosA, aPosB):
	""" Calculates the distance between two Positions
	
	Args:
			aPosA - (Position) First position
			aPosB - (Position) Second position
	
	Returns:
			The distance between first and second position
	"""
	
	X = aPosA.myX - aPosB.myX
	Z = aPosA.myZ - aPosB.myZ
	
	return math.sqrt(X * X + Z * Z)

		
def Distance3D(aPosA, aPosB):
	""" Calculates the distance between two Positions
	
	Args:
			aPosA - (Position) First position
			aPosB - (Position) Second position
	
	Returns:
			The distance between first and second position
	"""
	
	X = aPosA.myX - aPosB.myX
	Y = aPosA.myY - aPosB.myY
	Z = aPosA.myZ - aPosB.myZ
	
	return math.sqrt(X * X + Y * Y + Z * Z)

		
def GetVector(aPosA, aPosB):
	""" Get the normalized vector from aPosA to aPosB.
	
	Args:
			aPosA - (Position) Start position
			aPosB - (Position) End position
	
	Returns:
			The vector from aPosA to aPosB
	"""
	
	return (GetLine(aPosA, aPosB).Normalize())


def GetDirection(aPosA, aPosB):
	""" Get the normalized vector as a Position from aPosA to aPosB.
	
	Args:
			aPosA - (Position) Start position
			aPosB - (Position) End position
	
	Returns:
			The Position from aPosA to aPosB
	"""
	
	return Vector2Position( (GetLine(aPosA, aPosB).Normalize()) )


def GetRandomDirection():
		
	x = random.uniform( -8.0, 12.0 )
	y = random.uniform( -12.0, 8.0 )
	
	if random.random() < 0.5:
		v = Vector( x, y )
	else:
		v = Vector( y, x )
	
	v.Normalize()
	return Vector2Position( v )
		

def GetLine(aPosA, aPosB):
	""" Get the line from aPosA to aPosB as a vector.
	
	Args:
			aPosA - (Position) Start of line
			aPosB - (Position) End of line
	
	Returns:
			The vector from aPosA to aPosB
	"""
	
	return Vector(aPosB.myX - aPosA.myX, aPosB.myZ - aPosA.myZ)


def Dot(aVecA, aVecB):
	""" The dot product.
	
	Args:
			aVecA - (Vector)
			aVecB - (Vector)
	
	Returns:
			The dot product of aVecA and aVecB
	"""
	
	return (aVecA.myX * aVecB.myX + aVecA.myZ * aVecB.myZ)


def PosDot(aPosA, aPosB):
	""" The dot product.
	
	Args:
			aPosA - (Position)
			aPosB - (Position)
	
	Returns:
			The dot product of aPosA and aPosB
	"""
	
	return (aPosA.myX * aPosB.myX + aPosA.myY * aPosB.myY + aPosA.myZ * aPosB.myZ)


def Heading2Vector(aHeading):
	""" Get the vector describing a certain heading.
	
	Args:
			aHeading - (float) A heading in radians.
	
	Returns:
			The resulting Vector
	"""
	
	vect = Vector()
	
	vect.myX = math.sin(aHeading)
	vect.myZ = math.cos(aHeading)
	
	return vect


def Vector2Heading(aVector):
	""" Get the angle describing a certain vectors direction.
	
	Args:
			aVector - (Vector) A Vector.
	
	Returns:
			The resulting Heading
	"""
	
	return math.atan2(aVector.myX, aVector.myZ)


def GetHeading(aFrom, aTo):
	""" Get the angle describing a certain direction.
	
	Args:
			aFrom - (Vector) A Vector.
			aTo - (Vector) A Vector.
	
	Returns:
			The resulting Heading
	"""
	
	vec = aTo - aFrom
	vec.Normalize()
	return Vector2Heading(vec)


def RotateVector(aVector, aAng):
	""" Rotates a vector counter clockwise.
	
	Args:
			aVector - (Vector) The vector to rotate.
			aAng - (float) The angle to rotate the vector.
	
	Returns:
			The rotated vector.
	"""
	
	vect = Vector()
	
	vect.myX = aVector.myX * math.cos(aAng) + aVector.myZ * math.sin(aAng)
	vect.myZ = aVector.myZ * math.cos(aAng) - aVector.myX * math.sin(aAng)
	
	return vect


def RotatePosition(aPosition, aAng):
	""" Rotates a position counter clockwise.
	
	Args:
			aPosition - (Position) The vector to rotate.
			aAng - (float) The angle to rotate the position.
	
	Returns:
			The rotated position.
	"""
	
	pos = Position()
	
	pos.myX = aPosition.myX * math.cos(aAng) + aPosition.myZ * math.sin(aAng)
	pos.myY = aPosition.myY
	pos.myZ = aPosition.myZ * math.cos(aAng) - aPosition.myX * math.sin(aAng)
	
	return pos
		

def Angles2Direction( someAngles ):

	pos = Position()
	
	someAngles.myX = -someAngles.myX
	someAngles.myY = -someAngles.myY
	
	pos.myX = (-math.cos( someAngles.myX )) * math.sin( someAngles.myY )
	pos.myY = math.sin( someAngles.myX )
	pos.myZ = math.cos( someAngles.myX ) * math.cos( someAngles.myY )
	
	return pos
		
		
def CalculateFlankPosition(aOurPosition, aTargetPosition, aAngularLimit, aRadius, aRightFlank = False):
	"""
	"""
	
	target_dir = GetVector(aOurPosition, aTargetPosition)
	target_vec = Position2Vector(aTargetPosition)
	
	if target_dir is None:
		return None
	
	flank_angle = random.uniform(aAngularLimit, math.pi - aAngularLimit)
	
	if aRightFlank:
		flank_angle = -flank_angle
	
	flank_dir = RotateVector(target_dir, flank_angle)
	flank_pos = Vector2Position(target_vec + (flank_dir * aRadius))
	
	return flank_pos


def CalculateBehindPosition(aOurPosition, aTargetPosition, aDistance):
	"""
	"""
	
	target_dir = GetVector(aOurPosition, aTargetPosition)
	target_vec = Position2Vector(aTargetPosition)
	
	if target_dir is None:
		return None
	
	behind_pos = Vector2Position(target_vec + (target_dir * aDistance))    
	
	return behind_pos


def CalculateRandomPosition(aCenter, aRadius):
	"""
	"""
	
	rand_pos = Position(aCenter.myX, aCenter.myY, aCenter.myZ)
	rand_pos.myX += random.randint(-int(aRadius), int(aRadius))
	rand_pos.myZ += random.randint(-int(aRadius), int(aRadius))
	
	return rand_pos

		
def CalculateRandomBoxPosition(aCenter, aSize):
	"""
	"""
	
	rand_pos = Position(aCenter.myX - aSize, aCenter.myY, aCenter.myZ - aSize)
	rand_pos.myX += random.randint(0, int(aSize * 2))
	rand_pos.myZ += random.randint(0, int(aSize * 2))
	
	return rand_pos


def CalculateRandomPositionInStrip( SpawnPositionA, SpawnPositionB, StripWidth ):
	"""
	Two positions to define the ends of the strips.  The positions bisect the ends.
	StripWidths is the distance from a bisecting position to the edge of the strip.
	*  a position
	|  is a StripWidth
	
	|-------------------------|
	|                         |
	*                         *
	|                         |
	|-------------------------|
	"""
	SpawnPositionA.myY = SpawnPositionB.myY
	FromAtoB = GetDirection( SpawnPositionA, SpawnPositionB )
	dist = Distance( SpawnPositionA, SpawnPositionB )
	aRandomPosition = SpawnPositionA + ( FromAtoB * dist * random.random() )
	aRandomPosition = aRandomPosition + ( RotatePosition( FromAtoB, 1.560795 ) * StripWidth * random.uniform(-1.0, 1.0) )
	return aRandomPosition  

		
def BetweenPosition(aFrom, aTo, aScale = 0.5):
	"""
	"""
	
	dir_vec = GetVector(aFrom, aTo)
	distance = Distance(aFrom, aTo)
	from_vec = Position2Vector(aFrom)
	
	return Vector2Position(from_vec + (dir_vec * (distance * aScale)))


def NearPosition(aFrom, aTo, aDistance):
	"""
	"""
	
	dir_vec = GetVector(aFrom, aTo)
	to_vec = Position2Vector(aTo)
	
	return Vector2Position(to_vec - (dir_vec * aDistance))


def Deg2Rad( aDeg ):
	"""
	"""
	
	return aDeg * (math.pi / 180.0)
