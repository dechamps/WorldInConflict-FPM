import serverimports
from globals import *


class Platoon( object ):
	
	def __init__( self, someGroups = [] ):
		
		self.__Groups = []
		
		self.__CombatPlatoon = True
		
		for grp in someGroups:
			self.AddGroup( grp )

		self.__UpdateTime = PLATOON_DEFAULT_UPDATE_TIME
		self.__LastUpdateTime = 0.0


	def __pos__( self ):
		
		for grp in self.__Groups:
			try:
				grp.GetPosition()
			except serverimports.EmptyGroupException:
				continue
			else:
				## we found a non empty group
				return grp.GetPosition()
		
		## all groups are empty, raise an exception	
		raise serverimports.EmptyGroupException( 'Empty platoon has no position' )
	

	def __getUpdateTime( self ):
		return self.__UpdateTime
	
	def __setUpdateTime( self, aUpdateTime ):
		self.__UpdateTime = aUpdateTime
	
	myUpdateTime = property( __getUpdateTime, __setUpdateTime )


	def __getGroups( self ):
		return self.__Groups
	
	myGroups = property( __getGroups )


	def __getCombatPlatoon( self ):
		return self.__CombatPlatoon

	def __setCombatPlatoon( self, aCombatPlatoon ):
		self.__CombatPlatoon = aCombatPlatoon

	myCombatPlatoon = property( __getCombatPlatoon, __setCombatPlatoon )


	def SetCombatPlatoon( self, aCombatFlag ):
		self.__CombatPlatoon = aCombatFlag


	def AddGroup( self, aGroup ):

		# Add aGroup to platoon
		self.__Groups.append( aGroup )
		aGroup.AddPlatoon( self )


	def RemoveGroup( self, aGroup ):

		self.__Groups.remove( aGroup )
		aGroup.RemovePlatoon( self )
		

	def Size( self, aCountRefillUnits = False ):
		size = 0
		for grp in self.__Groups:
			size += grp.Size( aCountRefillUnits )
		return size
	
	
	def GetPlatoonHealth( self ):
		'''Returns the total health of all unit in the platoon'''
		
		PlatoonTotalHealth = 0
		
		for g in self.myGroups:
			PlatoonTotalHealth += g.GetGroupHealth()
		
		return PlatoonTotalHealth

	
	def OnInCombat( self, aGroup, anUnitId, anAttackerId ):
		
		currTime = serverimports.GetCurrentTime()
		
		if currTime - self.__UpdateTime > self.__LastUpdateTime:
			
			self.__LastUpdateTime = currTime
			
			if self.__CombatPlatoon:
				for grp in self.__Groups:
					if not grp is aGroup:
						grp.myBehaviorManager.UpdateAttackBehavior( anUnitId, anAttackerId )
					
			serverimports.PostEvent( 'PlatoonInCombat', self )
				
		
	def OnSize( self ):
		
		size = self.Size()
		serverimports.PostEvent( 'PlatoonSize', self, size )
		