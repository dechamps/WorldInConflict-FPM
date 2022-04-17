import wicp
import wicp_common as common
import position
import debug
import wicmath.wicmath as wicmath
import camera


DEFAULT_END_DELAY_TIME		= 3.0
DEFAULT_POINT_DELAY_TIME	= 2.0
DEFAULT_CLOSE_TO_LIMIT		= 10.0
DEFAULT_DISTANCE_TO_LOOKAT	= 1.0


class ObjectiveCameraType( camera.CameraType ):
	
	def __init__( self ):
		
		camera.CameraType.__init__( self )
		
		self.myMaxSpeed			= 120.0
		self.myMaxAcceleration		= 65.0
		self.myAngularElasticity	= 30.0
		self.myAngularDrag		= 10.0
		self.myPositionalElasticity	= 30.0
		self.myPositionalDrag		= 10.0
		self.myZoomElasticity		= 30.0
		self.myZoomDrag			= 10.0	
		self.myMaxRotationSpeed		= 1.0
		self.myMaxRotationAcceleration	= 0.7
		self.myBankScaleFactor		= 1.0



class ObjectiveBrowserType( camera.CameraType ):
	
	def __init__( self ):
		camera.CameraType.__init__( self )
		
		self.myMaxSpeed			= 120.0
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
		
		self.myMinTurbulenceTime	= [	0.0	, 2.0		, 0.0		, 0.0		, 0.0 ]
		self.myMaxTurbulenceTime	= [	0.4	, 5.0		, 0.0		, 0.0		, 0.0 ]
		self.myMinPosTurbulence		= [ position.Position()	, position.Position()	, position.Position()	, position.Position(), 	position.Position() ]
		self.myMaxPosTurbulence		= [ position.Position()	, position.Position()	, position.Position()	, position.Position(), 	position.Position() ]
		self.myMinRotTurbulence		= [ position.Position(0.30, 0.30, 0.0)	, position.Position(0.0, 0.0, 0.8)	, position.Position()	, position.Position(), 	position.Position() ]
		self.myMaxRotTurbulence		= [ position.Position(0.60, 0.60, 0.0)	, position.Position(0.0, 0.0, 1.0)	, position.Position()	, position.Position(), 	position.Position() ]


class ShakyCamSubtle( camera.CameraType ):
	
	def __init__( self ):
		camera.CameraType.__init__( self )
		
		self.myMaxSpeed			= 120.0
		self.myMaxAcceleration		= 100.0
		self.myAngularElasticity	= 60.0
		self.myAngularDrag		= 40.0
		self.myPositionalElasticity	= 30.0
		self.myPositionalDrag		= 10.0
		self.myZoomElasticity		= 30.0
		self.myZoomDrag			= 10.0
		self.myMaxRotationSpeed		= 1.0
		self.myMaxRotationAcceleration	= 0.7
		self.myBankScaleFactor		= 1.0
		
		self.myMinTurbulenceTime	= [	0.5	, 0.7		, 0.0		, 0.0		, 0.0 ]
		self.myMaxTurbulenceTime	= [	1.0	, 1.2		, 0.0		, 0.0		, 0.0 ]
		self.myMinPosTurbulence		= [ position.Position()	, position.Position()	, position.Position()	, position.Position(), 	position.Position() ]
		self.myMaxPosTurbulence		= [ position.Position()	, position.Position()	, position.Position()	, position.Position(), 	position.Position() ]
		self.myMinRotTurbulence		= [ position.Position(0.7, 0.7, 0.0)	, position.Position(0.7, 0.7, 0.0)	, position.Position()	, position.Position(), 	position.Position() ]
		self.myMaxRotTurbulence		= [ position.Position(1.2, 1.2, 0.0)	, position.Position(1.2, 1.2, 0.0)	, position.Position()	, position.Position(), 	position.Position() ]


class ShakyCamHarsh( camera.CameraType ):
	
	def __init__( self ):
		camera.CameraType.__init__( self )
		
		self.myMaxSpeed			= 220.0
		self.myMaxAcceleration		= 100.0
		self.myAngularElasticity	= 30.0
		self.myAngularDrag		= 40.0
		self.myPositionalElasticity	= 30.0
		self.myPositionalDrag		= 10.0
		self.myZoomElasticity		= 60.0
		self.myZoomDrag			= 10.0
		self.myCamOffset		= position.Position( 0.0, 0.0, 0.0 )
		self.myMaxRotationSpeed		= 1.0
		self.myMaxRotationAcceleration	= 0.7
		self.myBankScaleFactor		= 1.0
				
		self.myMinTurbulenceTime	= [	0.0	, 0.5		, 0.0		, 0.0		, 0.0 ]
		self.myMaxTurbulenceTime	= [	0.4	, 3.0		, 0.4		, 0.7		, 0.0 ]
		self.myMinPosTurbulence		= [ position.Position()	, position.Position()	, position.Position()	, position.Position(21.8, 21.8, 0.0), 	position.Position() ]
		self.myMaxPosTurbulence		= [ position.Position()	, position.Position()	, position.Position()	, position.Position(216.25, 216.25, 0.0), 	position.Position() ]
		self.myMinRotTurbulence		= [ position.Position(1.8, 1.8, 0.0)	, position.Position(0.0, 0.0, 6.0)	, position.Position(1.8, 1.8, 0.0)	, position.Position(), 	position.Position() ]
		self.myMaxRotTurbulence		= [ position.Position(2.25, 2.25, 0.0)	, position.Position(0.0, 0.0, 9.0)	, position.Position(2.25, 2.25, 0.0)	, position.Position(), 	position.Position() ]
		

class Helicopter( camera.CameraType ):
	
	def __init__( self ):
		camera.CameraType.__init__( self )
		
		self.myMaxSpeed			= 120.0
		self.myMaxAcceleration		= 100.0
		self.myAngularElasticity	= 60.0
		self.myAngularDrag		= 10.0
		self.myPositionalElasticity	= 30.0
		self.myPositionalDrag		= 10.0
		self.myZoomElasticity		= 50.0
		self.myZoomDrag			= 9.0
		self.myMaxRotationSpeed		= 1.0
		self.myMaxRotationAcceleration	= 0.7
		self.myBankScaleFactor		= 1.0
		
		self.myMinTurbulenceTime	= [	0.75	, 2.0		, 0.0		, 0.0		, 0.0 ]
		self.myMaxTurbulenceTime	= [	1.0	, 4.0		, 0.0		, 0.0		, 0.0 ]
		self.myMinPosTurbulence		= [ position.Position()	, position.Position()	, position.Position()	, position.Position(), 	position.Position() ]
		self.myMaxPosTurbulence		= [ position.Position()	, position.Position()	, position.Position()	, position.Position(), 	position.Position() ]
		self.myMinRotTurbulence		= [ position.Position(1.5, 0.5, 0.0)	, position.Position(0.0, 0.0, 3.0)	, position.Position()	, position.Position(), 	position.Position() ]
		self.myMaxRotTurbulence		= [ position.Position(1.5, 0.5, 0.0)	, position.Position(0.0, 0.0, 3.0)	, position.Position()	, position.Position(), 	position.Position() ]


cameraTypes = { 'ObjectiveBrowserType': ObjectiveBrowserType, 'DefaultCameraType' : ObjectiveCameraType, 'ShakyCamSubtle' : ShakyCamSubtle, 'ShakyCamHarsh' : ShakyCamHarsh, 'Helicopter' : Helicopter }


class Point( object ):
	
	
	def __init__( self, aMoveToTarget, aLookAtTarget, aDelayTime, aCloseToLimit, aDistanceToLookAt ):
		
		self.__MoveToTarget = aMoveToTarget
		self.__LookAtTarget = aLookAtTarget
		self.__DelayTime = aDelayTime
		self.__CloseToLimit = aCloseToLimit
		self.__DistanceToLookAt = aDistanceToLookAt
		
		self.__UseGoToNow = 0
		self.__UseLookAtNow = 0
		
	
	def CalculateLookAt( self ):
		
		if self.__LookAtTarget is None:
			return None
			
		if self.__DistanceToLookAt > 1.0:
		
			movePos = common.GetPosition( self.__MoveToTarget )
			lookAt = common.GetPosition( self.__LookAtTarget )
						
			lookDir = lookAt - movePos
			lookDir.Normalize()
			lookDir = lookDir * self.__DistanceToLookAt
			
			lookAtPos = movePos + lookDir
			
			return lookAtPos
		
		return common.GetPosition( self.__LookAtTarget )
		
	
	def __getMoveToTarget( self ):
		
		return self.__MoveToTarget


	def __setMoveToTarget( self, aMoveToTarget ):
		
		self.__MoveToTarget = aMoveToTarget
	
	
	myMoveToTarget = property( __getMoveToTarget, __setMoveToTarget )
		

	def __getLookAtTarget( self ):
		
		return self.CalculateLookAt()


	def __setLookAtTarget( self, aLookAtTarget ):
		
		self.__LookAtTarget = aLookAtTarget
	
	
	myLookAtTarget = property( __getLookAtTarget, __setLookAtTarget )


	def __getDelayTime( self ):
		
		return self.__DelayTime


	def __setDelayTime( self, aDelayTime ):
		
		self.__DelayTime = aDelayTime
	
	myDelayTime = property( __getDelayTime, __setDelayTime )
	
	
	def SetDelayTime( self, aDelayTime ):
		
		self.__DelayTime = aDelayTime


	def __getCloseToLimit( self ):
		
		return self.__CloseToLimit


	def __setCloseToLimit( self, aCloseToLimit ):
		
		self.__CloseToLimit = aCloseToLimit

		
	myCloseToLimit= property( __getCloseToLimit, __setCloseToLimit )
	
	
	def SetCloseToLimit( self, aCloseToLimit ):
		
		self.__CloseToLimit = aCloseToLimit


	def __getDistanceToLookAt( self ):
		
		return self.__DistanceToLookAt


	def __setDistanceToLookAt( self, aDistanceToLookAt ):
		
		self.__DistanceToLookAt = aDistanceToLookAt

		
	myDistanceToLookAt = property( __getDistanceToLookAt, __setDistanceToLookAt )
	
	
	def SetDistanceToLookAt( self, aDistanceToLookAt ):
		
		self.__DistanceToLookAt = aDistanceToLookAt
	
	
	def __getUseGoToNow( self ):
		
		return self.__UseGoToNow


	def __setUseGoToNow( self, aUseGoToNow ):
		
		self.__UseGoToNow = aUseGoToNow

		
	myUseGoToNow = property( __getUseGoToNow, __setUseGoToNow )
	
	
	def SetGoToNow( self, aGoToNowFlag ):
		
		self.__UseGoToNow = aGoToNowFlag


	def __getUseLookAtNow( self ):
		
		return self.__UseLookAtNow


	def __setUseLookAtNow( self, aUseLookAtNow ):
		
		self.__UseLookAtNow = aUseLookAtNow

	
	myUseLookAtNow = property( __getUseLookAtNow, __setUseLookAtNow )

	def SetLookAtNow( self, aLookAtNowFlag ):
		
		self.__UseLookAtNow = aLookAtNowFlag


class ObjectiveCameraEx( object ):
	
	
	def __init__( self, aName, aIsBrowserCamera = False ):
		
		self.__Name = aName
		self.__IsBrowserCamera = aIsBrowserCamera
		self.__Points = []
		self.__CommandPoints = []
		
		self.__CameraType = ObjectiveCameraType()
		
		self.__CurrentPoint = -1
		
		self.__CameraReaction = None
		self.__EscapeReaction = None
		
		self.__UseEndGrab = False
		self.__UseGrabOnEscape = True
				
		self.__EndDelayTime = DEFAULT_END_DELAY_TIME
		
		self.__Escapable = True
	
	
	def SetCameraType( self, aCameraType ):
		
		self.__CameraType = aCameraType
		
	
	def __getCameraType( self ):
		
		return self.__CameraType
		
	myCameraType = property( __getCameraType )
		
	
	def __getName( self ):
		
		return self.__Name
	
	myName = property( __getName )


	def __getPoints( self ):
		
		return self.__Points
	
	myPoints = property( __getPoints )

	def __getEndDelayTime( self ):
		
		return self.__EndDelayTime
	
	def __setEndDelayTime( self, aNewEndDelayTime ):
		
		self.__EndDelayTime = aNewEndDelayTime
	
	myEndDelayTime = property( __getEndDelayTime,__setEndDelayTime )
	
	
	def AddPoint( self, aMoveToTarget, aLookAtTarget, aDelayTime = DEFAULT_POINT_DELAY_TIME, aCloseToLimit = DEFAULT_CLOSE_TO_LIMIT, aDistanceToLookAt = DEFAULT_DISTANCE_TO_LOOKAT ):
		
		p = Point( aMoveToTarget, aLookAtTarget, aDelayTime, aCloseToLimit, aDistanceToLookAt )
		self.__Points.append( p )
		return p
		
	
	def RemovePoint( self, anIndex ):
		
		self.__Points.pop( anIndex )
	
	
	def MovePointUp( self, aPoint ):
		
		if not aPoint in self.__Points:
			return
		idx = self.__Points.index( aPoint )
		if idx == 0:
			return
		self.__Points.pop( idx )
		self.__Points.insert( idx - 1, aPoint )
				
		
	def MovePointDown( self, aPoint ):

		if not aPoint in self.__Points:
			return
		idx = self.__Points.index( aPoint )
		if idx == (len(self.__Points) - 1):
			return
		self.__Points.pop( idx )
		self.__Points.insert( idx + 1, aPoint )
		

	
	def AddCommandPoints( self, someCommandPoints ):
		
		if isinstance( someCommandPoints, list ):
			self.__CommandPoints.extend( someCommandPoints )
		else:
			self.__CommandPoints.append( someCommandPoints )

	
	def SetEndDelayTime( self, aNewEndDelay ):
		
		self.__EndDelayTime = aNewEndDelay
			
	
	def SetCameraMaxSpeed( self, aNewSpeed ):
		
		self.__CameraType.myMaxSpeed = aNewSpeed
	
	
	def __getCameraMaxSpeed( self ):
		
		return self.__CameraType.myMaxSpeed
	
	
	myCameraMaxSpeed = property( __getCameraMaxSpeed )
	


	def SetCameraMaxAcceleration( self, aNewAcceleration ):
		
		self.__CameraType.myMaxAcceleration = aNewAcceleration
	
	
	def __getCameraMaxAcceleration( self ):
		
		return self.__CameraType.myMaxAcceleration
	
	
	myCameraMaxAcceleration = property( __getCameraMaxAcceleration )
	
	
	def UseEndGrab( self, aFlag = True ):
		
		self.__UseEndGrab = aFlag


	def UseEndGrabOnEscape( self, aFlag = True ):
		
		self.__UseGrabOnEscape = aFlag

	
	def SetEscapable( self, aFlag ):
		
		self.__Escapable = aFlag
	
	
	def ToggleUseEndGrab( self ):
		
		if self.__UseEndGrab:
			self.__UseEndGrab = False
		else:
			self.__UseEndGrab = True

	
	def GetUseEndGrab( self ):
		
		return self.__UseEndGrab

	
	def Play( self, aIsBrowserCamera = None, aUseNewCallbacksFlag = True ):
		
		import clientimports
		if aIsBrowserCamera != None:
			self.__IsBrowserCamera = aIsBrowserCamera
		
		if not camera.IsActive():
			if self.__IsBrowserCamera:
				camera.GrabCamera( 0, 0.0, 0, 1 )
			else:
				camera.GrabCamera( 1 )
				camera.EnableFovOverride( 0 )
		
		if self.__IsBrowserCamera:
			camera.SetCameraType( ObjectiveCameraType() )
		else:
			camera.SetCameraType( self.__CameraType )
		
		for cp in self.__CommandPoints:
			wicp.SetCommandPointVisible( cp, True )
				
		self.__CurrentPoint = -1
		
		if self.__Escapable:
			
			self.__EscapeReaction = clientimports.RE_OnCustomEvent( 'SKIP_CUTSCENE', clientimports.Action( self.End, True ) )
		
		self.VisitNext(aUseNewCallbacksFlag)
				
	def End( self, aEscape = False ):
		import clientimports
		
		clientimports.RemoveReaction( self.__CameraReaction )
		clientimports.RemoveReaction( self.__EscapeReaction )
		
		## when objective browser is closed the camera is released
		if not self.__IsBrowserCamera:
		
			if self.__UseEndGrab and (not aEscape or self.__UseGrabOnEscape):
				camera.GrabCamera( 1 )
		
			camera.ReleaseCamera()
		
		wicp.SendPlayerAction( 'END_OF_CUTSCENE' )
		
	
	def VisitNext( self, aUseNewCallbacksFlag = True ):
		import clientimports as ci
		
		self.__CurrentPoint += 1
		
		if self.__CurrentPoint >= len( self.__Points ):
			
			## no support (or need) for end-delay in objectivebrowser
			if self.__IsBrowserCamera:
				self.End()
			else:
				ci.Delay( self.__EndDelayTime, ci.Action( self.End ) )
			return
		
		p = self.__Points[self.__CurrentPoint]
		
		if p.myMoveToTarget is None:
			movePos = None
		else:
			movePos = common.GetCopy( common.GetPosition( p.myMoveToTarget ) )
		
		if p.myLookAtTarget is None:
			lookAtPos = None
		else:
			lookAtPos = common.GetCopy( common.GetPosition( p.myLookAtTarget ) )
		
		## default fov for browser camera
		if self.__IsBrowserCamera:
			camera.ZoomTo( 40 )
		
		## no fov changes for ingame objective camera
		#else:
		#	camera.ZoomTo( 50 )
		
		## calculate delay time
		delayTime = 0.0
		if self.__CurrentPoint > 0 and self.__CurrentPoint < len( self.__Points ):
			delayTime = self.__Points[self.__CurrentPoint - 1].myDelayTime
		
		if not movePos is None:
			if p.myUseGoToNow:
				camera.GoToNow( movePos.myX, movePos.myY, movePos.myZ, delayTime )
			else:
				camera.GoTo( movePos.myX, movePos.myY, movePos.myZ, delayTime )
		
		if not lookAtPos is None:
			if p.myUseLookAtNow:
				camera.LookAtNow( lookAtPos.myX, lookAtPos.myY, lookAtPos.myZ, delayTime )
			else:
				camera.LookAt( lookAtPos.myX, lookAtPos.myY, lookAtPos.myZ, delayTime )
		

		if aUseNewCallbacksFlag == True:	
			if p.myCloseToLimit == 0:
				self.__CameraReaction = ci.RE_OnCustomEvent( 'ScriptCameraDone', ci.Action( self.VisitNext, aUseNewCallbacksFlag ))	
			else:
				self.__CameraReaction = ci.RE_OnCustomEvent( 'ScriptCameraAtPosition', ci.Action( self.VisitNext, aUseNewCallbacksFlag ),\
							 ci.PositionTest( movePos, p.myCloseToLimit ) )
		else:
			self.__CameraReaction = ci.RE_OnCustomEvent( 'CameraAtTarget', ci.Action( self.VisitNext, aUseNewCallbacksFlag ),\
						 ci.PositionTest( movePos, p.myCloseToLimit ) )
