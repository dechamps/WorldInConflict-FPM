import wicg_common as common
import gameobject
import building
import wicmath.wicmath as wicmath
import random
import area


def TA_Position( aDelay, aPositionToBlow, aDirection = None, aSupportWeapon = 'SINGLEPLAYER_Artillery_USSR_SingleProjectile', aTrackingName = "" ):
	import serverimports as si
	
	targetPosition = common.GetPosition( aPositionToBlow )
	
	if aDirection is None:
		direction = targetPosition
	else:
		direction = wicmath.GetDirection( targetPosition, common.GetPosition( aDirection ) )
	
	actArty = si.Action( si.DeploySupportWeapon, aSupportWeapon, targetPosition, direction, 1, aTrackingName )

	if aDelay > 0.0:
		si.Delay( aDelay, actArty )
	else:
		actArty.Execute()


def TA_DestroyObject( aDelay, anObjectToBlow, aDirection = None, aSupportWeapon = 'SINGLEPLAYER_Artillery_USSR_SingleProjectile', aTrackingName = "" ):
	import serverimports as si

	targetPosition = common.GetPosition( anObjectToBlow )
	
	if aDirection is None:
		direction = targetPosition
	else:
		direction = wicmath.GetDirection( common.GetPosition( aDirection ), targetPosition )
		
	actDest = si.Action( gameobject.GameObject( anObjectToBlow ).Damage, gameobject.GameObject( anObjectToBlow ).myHealth * 0.99 )
	actArty = si.Action( si.DeploySupportWeapon, aSupportWeapon, targetPosition, direction, 1, aTrackingName )
	
	if aDelay > 0.0:
		si.Delay( aDelay, [ actDest, actArty ] )
	else:
		actDest.Execute()
		actArty.Execute()

	return anObjectToBlow


def TA_DestroyBuilding( aDelay, aBuildingToBlow, aDirection = None, aSupportWeapon = 'SINGLEPLAYER_Artillery_USSR_SingleProjectile', aTrackingName = "" ):
	import serverimports as si
	
	targetPosition = common.GetPosition( aBuildingToBlow )
	
	if aDirection is None:
		direction = targetPosition
	else:
		direction = wicmath.GetDirection( common.GetPosition( aDirection ), targetPosition )

	
	actDest = si.Action( building.Building( aBuildingToBlow ).Damage, building.Building( aBuildingToBlow ).myHealth * 0.99 )
	actArty = si.Action( si.DeploySupportWeapon, aSupportWeapon, targetPosition, direction, 1, aTrackingName )
	
	if aDelay > 0.0:
		si.Delay( aDelay, [ actDest, actArty ] )
	else:
		actDest.Execute()
		actArty.Execute()

	return aBuildingToBlow


class TA_Wrapper( object ):
	"""
	"""
	
	def __init__( self, aTA, aAreaList, aAmount, aDelay, aTimer, aAllowedIterations = -1, aDirection = None, aTrackingName = "" ):
		
		self.__TAname = aTA
		self.__AreaList = aAreaList
		self.__Amount = aAmount
		self.__Delay = aDelay
		self.__Timer = aTimer
		self.__AllowedIterations = aAllowedIterations
		self.__Shooting = False
		self.__reactShoots = []
		self.__reactNextShoot = None
		self.__ShootCounter = 0
		self.__Direction = aDirection
		self.__myTrackingName = aTrackingName
			
	
	def Shoot( self ):
		import serverimports
		
		if not self.__Shooting:
			return
		
		if self.__ShootCounter == self.__AllowedIterations:
			return
		
		if not self.__AllowedIterations == -1:
			self.__ShootCounter += 1
		
		n = 0
		self.__reactShoots = []
		self.__reactNextShoot = None
		
		while n < self.__Amount:
			n += 1
			somethingToTA = random.choice( self.__AreaList )
			
			if isinstance( somethingToTA, area.Area ):
				pos1 = wicmath.CalculateRandomPosition( somethingToTA.myPos, somethingToTA.myRadius )
			else:
				pos1 = wicmath.CalculateRandomPosition( common.GetPosition( somethingToTA ), serverimports.theGame.GetInstance( somethingToTA ).myRadius )
			
			if self.__Direction:
				pos2 = self.__Direction
			else:
				pos2 = common.GetPosition( somethingToTA )
			if random.randint( 0, 1 ):
				offsetTimer = random.random( )*1.5
			else:
				offsetTimer = - random.random( )*1.5
			
			if hasattr(self, "_TA_Wrapper__myTrackingName"):
				self.__reactShoots.append( serverimports.Delay( random.randint( 0, self.__Delay ) + offsetTimer, serverimports.Action( serverimports.DeploySupportWeapon, self.__TAname, pos1, pos2, 1, self.__myTrackingName ) ) )
			else:
				self.__reactShoots.append( serverimports.Delay( random.randint( 0, self.__Delay ) + offsetTimer, serverimports.Action( serverimports.DeploySupportWeapon, self.__TAname, pos1, pos2, 1, "" ) ) )

		else:
			self.__reactNextShoot = serverimports.Delay( self.__Timer, serverimports.Action( self.Shoot ) )
		

	def ChangeTA( self, aTA ):
		
		self.__TAname = aTA


	def ChangeAmount( self, aAmount ):
		
		self.__Amount = aAmount


	def ChangeDelay( self, aDelay ):
		
		self.__Delay = aDelay


	def ChangeTimer( self, aTimer ):
		
		self.__Timer = aTimer


	def ChangeTimerInstant( self, aTimer ):
		import serverimports
		
		serverimports.RemoveReaction( self.__reactNextShoot )
		self.__Timer = aTimer
		self.__reactNextShoot = serverimports.Delay( self.__Timer, serverimports.Action( self.Shoot ) )


	def AddArea( self, someAreas ):

		if isinstance( someAreas, list ):
			self.__AreaList.extend( someAreas )
		else:
			self.__AreaList.append( someAreas )

			
	def ChangeAreas( self, someAreas ):

		self.__AreaList = someAreas

	
	def RemoveArea( self, someAreas ):
		
		if isinstance( someAreas, list ):
			for area in someAreas:
				self.__AreaList.remove( someAreas )
		else:
			self.__AreaList.remove( someAreas )


	def HardStop( self ):
		import serverimports
		
		self.__Shooting = False
		
		serverimports.RemoveReaction( self.__reactNextShoot )
		for react in self.__reactShoots:
			serverimports.RemoveReaction( react )
		
			
	def Stop( self ):
		
		self.__Shooting = False

		
	def Start( self ):
		
		self.__Shooting = True
		
		self.Shoot()

		
	def IsStarted( self ):
		
		if self.__Shooting == True:
			return True
		else:
			return False

