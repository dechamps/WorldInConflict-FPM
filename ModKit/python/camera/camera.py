import wicp
import ccamera
import base
from position import Position


undoSelection = True

def GrabCamera( aShowBordersFlag = 1, aAspectRatio = 0, aBorderPos = 0, aUseRealTimeFlag = 0, aUseUpdate = True ):
	global undoSelection
	
	# check if we have units selected
	#if not ccamera.IsActive():
	#	if wicp.GetSelectedUnit(0) == -1:
	#		undoSelection = False
	#	else:
	#		undoSelection = True
	
	return ccamera.GrabCamera( aShowBordersFlag, aAspectRatio, aBorderPos, aUseRealTimeFlag, aUseUpdate )

def ReleaseCamera( aBorderPos = 1 ):
	
	# reset the unit selections
	#if undoSelection:
	#	wicp.UndoSelection()
	
	return ccamera.ReleaseCamera( aBorderPos )

def EnableFovOverride( aUseOveride = 1 ):
	return ccamera.EnableFovOverride( aUseOveride )

def PurgeCamera():
	return ccamera.PurgeCamera()

def SetCameraType( aCameraType ):
	return ccamera.SetCameraType( aCameraType )

def GoTo( aX, aY, aZ, aDelay = 0.0 ):
	return ccamera.GoToPosition( Position( aX, aY, aZ ), aDelay )

def GoToNow( aX, aY, aZ, aDelay = 0.0 ):
	return ccamera.GoToPositionNow( Position( aX, aY, aZ ), aDelay )
	
def GoToAfterRelease( aX, aY, aZ, bX, bY, bZ ):
	return ccamera.GoToPositionAfterRelease(Position( aX, aY, aZ ), Position( bX, bY, bZ ))

def LookAtProjectileNow( aTaId, offset ):
	return ccamera.LookAtProjectileNow( aTaId, offset )

def LookAtNamedProjectileNow( aTrackingName, aTrackingId, offset ):
	return ccamera.LookAtNamedProjectileNow( aTrackingName, aTrackingId, offset )

def LookAtProjectile( aTaId, offset ):
	return ccamera.LookAtProjectile( aTaId, offset )

def LookAtNamedProjectile( aTrackingName, aTrackingId, offset ):
	return ccamera.LookAtNamedProjectile( aTrackingName, aTrackingId, offset )

def GoToProjectile( aTaId, offset ):
	return ccamera.GoToProjectile( aTaId, offset )

def GoToNamedProjectile( aTrackingName, aTrackingId, offset ):
	return ccamera.GoToNamedProjectile( aTrackingName, aTrackingId, offset )

def GoToProjectileNow( aTaId, offset ):
	return ccamera.GoToProjectileNow( aTaId, offset )

def GoToNamedProjectileNow( aTrackingName, aTrackingId, offset ):
	return ccamera.GoToNamedProjectileNow( aTrackingName, aTrackingId, offset )

def LookAtEffect( aTaId, offset ):
	return ccamera.LookAtEffect( aTaId, offset )

def LookAtNamedEffect( aTrackingName, offset ):
	return ccamera.LookAtNamedEffect( aTrackingName, offset )

def LookAtEffectNow( aTaId, offset ):
	return ccamera.LookAtEffectNow( aTaId, offset )

def LookAtNamedEffectNow( aTrackingName, offset ):
	return ccamera.LookAtNamedEffectNow( aTrackingName, offset )

def GoToEffect( aTaId, offset ):
	return ccamera.GoToEffect( aTaId, offset )

def GoToNamedEffect( aTrackingName, offset ):
	return ccamera.GoToNamedEffect( aTrackingName, offset )

def GoToEffectNow( aTaId, offset ):
	return ccamera.GoToEffectNow( aTaId, offset )

def GoToNamedEffectNow( aTrackingName, offset ):
	return ccamera.GoToNamedEffectNow( aTrackingName, offset )

def GetLatestEffectId( ):
	return ccamera.GetLatestEffectId( )

def GetLatestProjectileId( ):
	return ccamera.GetLatestProjectileId( )

def GoToUnit( anUnitId, anOffset ):
	return ccamera.GoToUnit( anUnitId, anOffset )

def GoToUnitNow( anUnitId, anOffset ):
	return ccamera.GoToUnitNow( anUnitId, anOffset )

def LookAt( aX, aY, aZ, aDelay = 0.0 ):
	return ccamera.LookAtPosition( Position( aX, aY, aZ ), aDelay )

def LookAtUnit( anUnitId, anOffset ):
	return ccamera.LookAtUnit( anUnitId, anOffset )

def LookAtNow( aX, aY, aZ, aDelay = 0.0 ):
	return ccamera.LookAtPositionNow( Position( aX, aY, aZ ), aDelay )


def LookAtUnitNow( anUnitId, anOffset ):
	return ccamera.LookAtUnitNow( anUnitId, anOffset )

def LookAngle( aX, aY, aZ, aDelay = 0.0 ):
	return ccamera.LookAngle( Position( aX, aY, aZ ), aDelay )

def LookAngleNow( aX, aY, aZ, aDelay = 0.0 ):
	return ccamera.LookAngleNow( Position( aX, aY, aZ ), aDelay )

def ZoomTo( aFOV, aDelay = 0.0 ):
	return ccamera.ZoomTo( float( aFOV ), aDelay )

def ZoomToNow( aFOV, aDelay = 0.0 ):
	return ccamera.ZoomToNow( float( aFOV ), aDelay )

def Bank( anAngle, aDelay = 0.0 ):
	return ccamera.Bank( float( anAngle ), aDelay )

def BankNow( anAngle, aDelay = 0.0 ):
	return ccamera.BankNow( float( anAngle ), aDelay )

def VelocityImpulse( aVector, aTime ):
	return ccamera.VelocityImpulse( aVector, float( aTime ) )

def ZoomImpulse( aFOV, aTime ):
	return ccamera.ZoomImpulse( float( aFOV ), float( aTime ) )

def RotationImpulse( aVector, aTime ):
	return ccamera.RotationImpulse( aVector, float( aTime ) )

def BankImpulse( anAngle, aTime ):
	return ccamera.BankImpulse( float( anAngle ), float( aTime ) )

def GetPosition():
	return ccamera.GetPosition()

def GetRotation():
	return ccamera.GetRotation()

def GetFov():
	return ccamera.GetFov()

def IsActive():
	return ccamera.IsActive()



class CameraType( object ):

	def __init__( self ):
		self.myMinPosTurbulence		= [ Position(), Position(), Position(), Position(), Position() ]
		self.myMaxPosTurbulence		= [ Position(), Position(), Position(), Position(), Position() ]
		self.myMinRotTurbulence		= [ Position(), Position(), Position(), Position(), Position() ]
		self.myMaxRotTurbulence		= [ Position(), Position(), Position(), Position(), Position() ]
		self.myMinTurbulenceTime	= [ 0.1, 0.1, 0.1, 0.1, 0.1 ]
		self.myMaxTurbulenceTime	= [ 0.1, 0.1, 0.1, 0.1, 0.1 ]
		
		self.myCamOffset			= Position( 0.0, 0.0, 0.0 )
		
		self.myMaxSpeed				= 0.0
		self.myMaxAcceleration			= 0.0
		self.myAngularElasticity		= 0.0
		self.myAngularDrag			= 0.0
		self.myPositionalElasticity		= 0.0
		self.myPositionalDrag			= 0.0
		self.myZoomElasticity			= 0.0
		self.myZoomDrag				= 0.0
		self.myMaxRotationSpeed			= 1.0
		self.myMaxRotationAcceleration		= 0.7
		self.myBankScaleFactor			= 1.0


	def AddPosTurbulence(self, aMinPosTurb, aMaxPosTurb):
		self.myMinPosTurbulence.append(aMinPosTurb)
		self.myMaxPosTurbulence.append(aMaxPosTurb)


	def AddRotTurbulence(self, aMinRotTurb, aMaxRotTurb):
		self.myMinRotTurbulence.append(aMinRotTurb)
		self.myMaxRotTurbulence.append(aMaxRotTurb)


	def AddTurbulenceTime(self, aMinTurbTime, aMaxTurbTime):
		
		self.myMinTurbulenceTime.append(aMinTurbTime)
		self.myMaxTurbulenceTime.append(aMaxTurbTime)
	
			
	def SetMaxSpeed( self, newMaxSpeed ):
		
		self.myMaxSpeed = newMaxSpeed

	def SetMaxAcceleration( self, newMaxAcceleration ):
		
		self.myMaxAcceleration = newMaxAcceleration

	def SetAngularElasticity( self, newAngularElasticity ):
		
		self.myAngularElasticity = newAngularElasticity

	def SetAngularDrag( self, newAngularDrag ):
		
		self.myAngularDrag = newAngularDrag

	def SetPositionalElasticity( self, newPositionalElasticity ):
		
		self.myPositionalElasticity = newPositionalElasticity

	def SetPositionalDrag( self, newPositionalDrag ):
		
		self.myPositionalDrag = newPositionalDrag

	def SetZoomElasticity( self, newZoomElasticity ):
		
		self.myZoomElasticity = newZoomElasticity

	def SetZoomDrag( self, newZoomDrag ):
		
		self.myZoomDrag = newZoomDrag

	

class DefaultCamera( CameraType ):
	
	def __init__( self ):
		CameraType.__init__( self )
		
		self.myMaxSpeed			= 100.0
		self.myMaxAcceleration		= 100.0
		self.myAngularElasticity	= 30.0
		self.myAngularDrag		= 10.0
		self.myPositionalElasticity	= 30.0
		self.myPositionalDrag		= 10.0
		self.myZoomElasticity		= 30.0
		self.myZoomDrag			= 10.0
		self.myMaxRotationSpeed		= 1.0
		self.myMaxRotationAcceleration	= 0.7
		self.myBankScaleFactor		= 1.0