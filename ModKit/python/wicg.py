""" wicg module interface. These are the functions available to server-side
	scripts.
"""


def DebugMessage( aMessage ):
	""" Prints a debugmessage ingame. Type 'pythondebugtoggle' in the console to
	toggle the visibility of the debugmessages.
	
	aMessage (str) Debugmessage to show ingame.
	
	returns 1 on success, otherwise 0
	"""
	return 1


def GetGameData( aGameObject ):
	""" Fetches data about the game
	"""
	return 1


def CreateUnit( aType, aPosition, aHeading, anOwner, aTeam ):
	""" Creates a unit.

	This function should not be used directly. Use Game.CreateUnit() instead.

	Returns unitID of created unit (-1 if create failed).
	"""
	return None


def CreateUnitsWithSpawner():
	pass


def MoveUnit( aUnitID, aDestination, aHeading ):
	""" Gives a move order to a unit.

	This function should not be used directly. Use Unit.MoveUnit() instead.

	Returns 1 if move order succeeded, 0 otherwise
	"""
	return False


def MoveUnits( aUnitIDs, aDestination, aDirection, aWantBoxFormationFlag = False ):
	""" Gives a move order to a unit.

	This function should not be used directly. Use Unit.MoveUnit() instead.

	Returns 1 if move order succeeded, 0 otherwise
	"""
	return False


def ThrowEvent( anEvent ):
	""" Throws an event to all players client-side scripts.

	anEvent - (str) Event string.
	"""
	return 0


def SetWeather( aWeather ):
	""" Changes the current weather.

	aWeather - (str) New weather type (XEnvironment defined in <landscape>.juice)
	"""
	return 0


def GetPlayerTeam( aPlayer ):
	""" Gets the team aPlayer belongs to.

	aPlayer - (int) Player
	returns which team aPlayer belongs to.
	"""
	return 1


def RemoveUnit( aUnitID, aDestroyFlag ):
	""" Removes given unit from the game

	aUnitID			- (int) ID of unit to remove
	aDestroyFlag	- (int) Destroys unit if not 0
	"""
	return 0


def RemovePlayerUnit():
	pass


def GetUnitsInAreaXZ( aPosition, aRadius ):
	""" Returns a list of all units within the area

	aPosition   - (common.Position) Position of area center
	aRadius	 - (float) Radius of area

	returns a list of unitIDs (or empty list if no units).
	"""
	return []


def ThrowEventToPlayer( aPlayer, anEvent ):
	""" Throws an event to a specific player.

	anEvent - (str) Event string.
	"""
	return 0


def IsSinglePlayer():
	""" Returns if the game is single player or not.

	return 1 if game is singleplayer. 0 otherwise.
	"""
	return 0


def MissionCompleted( aTeam ):
	""" Sets aTeam as winner of the game.

	aTeam - (int) Team number of winning team (1 = US, 2 = Nato, 3 = USSR)
	"""
	return 0


def MissionFailed():
	""" Sets mission failed state in the game. Will cause all players to
	recieve the 'Failed' endscreen.
	"""
	return 0


def GetCommandPointOwner( aCommandPoint ):
	""" Returns the current owner of aCommandPoint

	aCommandPoint - (str) Instance name of the command point to look for

	returns which team currently controlling the command point (0 for neutral).
	"""
	return 0


def SetCommandPointOwner():
	pass


def CreateCommandPointEx( aName, aStartTeam, aRetakeFlag ):
	""" Creates a CommandPoint """

	return 0


def CreatePerimeterPointEx( aName, aCommandPoint ):
	""" Creates a perimeterpoint """

	return 0


def CreateFortificationPointEx( aName, aCommandPoint ):
	""" Creates a Defensive fortifiaction point """

	return 0


def GetVisibleEnemyUnits( aTeam ):
	""" Retrieves a list of all visible enemy units

	aTeam - (int) The team number looking for enemies (1 = US, 2 = Nato, 3 = USSR)

	returns a list of unitIDs (or empty list if no units).
	"""
	return []


def GetVisibleEnemyUnitsInArea( aTeam, aPosition, aRadius  ):
	""" Retrieves a list of visible enemy units in a given area

	aTeam		- (int) The team number looking for enemies (1 = US, 2 = Nato, 3 = USSR)
	aPosition	- (common.Position) Position of area center
	aRadius		- (float) Radius of area

	returns a list of unitIDs (or empty list if no units).
	"""
	return []


def DeploySupportWeapon( aWeaponType, aTargetPosition, aDirection, upgradeLevel, aTrackingName = "" ):
	""" Deploys a supportweapon as a given player

	aWeaponType		- (string) Weapon to deploy
	aTargetPosition		- (common.Position) Target position to deploy weapon at
	aDirection		- (common.Position) Direction to deploy weapon in
	upgradeLevel		- int
	aTrackingName		- (string) A name used to identify this TA, often used in the OnTASpawned event

	returns 1 on success
	"""
	return 0


def CancelSupportWeapon( aTrackingName ):
	""" Cancel/removes a support weapon
	
	aTrackingName	- (string) Tracked support weapon to abort
	"""
	pass


def TrackUnit( aUnitID ):
	""" Marks a given unit for tracking

	aUnitID	- (int) Id of unit to track

	returns 1 on success
	"""
	return 0


def UnTrackUnit( aUnitID ):
	""" Stops tracking a given unit

	aUnitID	- (int) Id of unit to stop tracking

	returns 1 on success
	"""
	return 0


def SetBuildingData( aBuildingID, aStatName, aNewValue ):
	""" Updates given building stat with new value
	
	Args:
	 aBuildingID - (int) Hashed name of building
	 aStatName - (string) Name of stat to be updated
	 aNewValue - (*) New value of the given stat
	
	Returns:
	 None
	"""
	pass


def SendChat():
	"""Sends a chat message
	"""
	pass
		

def SetSlowMo():
	"""Set time scale
	"""
	pass
	

def GetInstanceData():
	"""Fetches instance data
	"""
	pass
	

def GetInstances():
	"""Retrieves an ice handle to the instances data
	"""
	pass


def UnitEnterContainer():
	"""Gives a unit order to enter a another unit
	"""
	pass
	
	
def UnitUnloadContainer():
	"""Gives a container unit order to unload it's residents
	"""
	pass
	
	
def UnitEnterBuilding():
	"""Gives a unit order to enter a building
	"""
	pass
	
	
def UnitEnter():
	"""Gives a unit order to enter a container. Either a unit or a building
	"""
	pass
	
	
def Attack():
	"""Generic attackorder
	"""
	pass
	
	
def UnitAttackUnit():
	"""Gives a unit order to attack another unit
	"""
	pass
	
	
def UnitAttackPosition():
	"""Gives a unit order to attack a position
	"""
	pass
	
	
def UnitStop():
	"""Gives a unit order to stop whatever it's doing
	"""
	
	pass
	
	
def SetUnitPrisonerFlag():
	"""Sets unit prisoner flag
	"""
	pass
	
	
def GetUnitData():
	"""Refreshes the given unit's data
	"""
	pass
	
	
def GetUnitMember():
	"""Retrieves data from a unit
	"""
	pass
	
	
def SetUnitData():
	"""Updates given unit data
	"""
	pass
	
	
def ChangeUnitsOwner():
	"""Change the owner for units
	"""
	pass
	
	
def GetNextFreeSquadId():
	"""Retrieves the next free SquadI
	"""
	pass



def GetAndIncNextFreeSquadId():
	pass

	
def GetSquadSize():
	"""Retrieves the size of a given squa
	"""
	pass
	
	
def GetContainerId():
	"""Checks if unit is a passenger or no
	"""
	pass
	
	
def MoveUnitsCover():
	"""Moves a group of units (infantry) and uses the cover system
	"""
	pass
	
	
def DisableAllUnits():
	"""Disable/enable all units, effects, clouds etc (for ingame cinematics
	"""
	pass
	
	
def SetExperienceLevel():
	"""Sets experience level for a uni
	"""
	pass


def SetPlayerExperienceLevel():
	pass

	
def SetUnitCostForSPRole():
	"""Sets cost for single player role for specific unit type. Negative: make non-buyable, positive: make buyable (independently of blacklist
	"""
	pass
	
	
def SetUnitNumLimitedPurchasable():
	"""Sets number of limited purchasables for specific unit type (unit type's rebate should be set to REBATE_LIMITED for single player role
	"""
	pass


def AddUnitNumLimitedPurchasable():
	pass


def GetUnitNumLimitedPurchasable():
	"""Gets number of limited purchasables for specific unit type (unit type's rebate should be set to REBATE_LIMITED for single player role
	"""
	pass
	
	
def AddRectToPathMap( aCorner1, aCorner2, aCorner3, aCorner4 ):
	"""

	Args:
		aCorner1-4:	A 3d corner position of a rectangle, only the x and z values are used.

	Returns:
		TRUE if the rectangle was added to the vehicle and infantry path maps, FALSE if there were an error.

	"""
	pass


def RemoveRectToPathMap( aCorner1, aCorner2, aCorner3, aCorner4 ):
	"""

	Args:
		aCorner1-4:	A 3d corner position of a rectangle, only the x and z values are used.

	Returns:
		TRUE if the rectangle was removed from the vehicle and infantry path maps, FALSE if there were an error.

	"""
	pass


def IgnoreUnitsOwnedByPlayerId( aUnitId, aPlayerId ):
	"""

	Args:
		aUnitId:	A unit which should ignore the player's unit
		aPlayerId:	A player id which units to ignore, set to -1 to stop ignoring

	Returns:
		None

	"""
	pass


def ResupplyPlayerSquads():
	"""

	Args:
		None

	Retuns:
		None

	"""
	pass

def FreezeFortifications():
	"""Freeze or unfreeze the creation of new fortifications on a given perimeter point
	"""
	pass
	
	
def SetFortificationLevel():
	"""Creates defensive fortification points up to specified level
	"""
	pass
	
	
def RemoveFortification():
	"""Removes a defensive fortification point
	"""
	pass


def CheckFortificationLevel():
	pass



def SetCamera():
	"""Set camera for a player
	"""
	pass
	
	
def GetBuildingData():
	"""Fetches building data, static data can be exclude
	"""
	pass


def GetGameObjectData():
	"""Fetches prop data, static data can be excluded
	"""
	pass
	
	
def DamageBuilding():
	"""Damages given buildin
	"""
	pass
	

def DamageBuildingEx():
	pass

	
def DamageGameObject():
	"""Damages given pro
	"""
	pass


def MakeDestructibleObjectInvurnable():
	pass


def SetWidgetStatus():
	"""Sets the drawstate of a GUI widge
	"""
	pass
	
	
def FlashWidget():
	"""Flashes a GUI widge
	"""
	pass
	
	
def ClientPythonCommand():
	"""Runs a python command on the given clien
	"""
	pass
	
	
def ShowMessageBox2():
	"""Shows a message box of a given type to a specified playe
	"""
	pass
	
	
def PurgeMessageBoxQueue2():
	"""Shows a message box of a given type to a specified playe
	"""
	pass
	
	
def ShowMessageBox():
	"""Shows a message box of a given type to a specified playe
	"""
	pass
	
	
def PurgeMessageBoxQueue():
	"""Shows a message box of a given type to a specified playe
	"""
	pass

	
def GetPlayerData():
	"""Fetches player data, static data can be exclude
	"""
	pass
	
	
def SetPlayerData():
	"""Updates given players stat
	"""
	pass
	
	
def EndGame():
	"""Ends the gam
	"""
	pass
	
	
def SetObjective():
	"""Set objectiv
	"""
	pass
	
	
def UpdateObjective():
	"""Update objectiv
	"""
	pass
	
	
def AddSubObjectiveMarker():
	"""Adds a sub-objective to an existing objectiv
	"""
	pass
	
	
def RemoveSubObjectiveMarker():
	"""Removes a sub-objectiv from an existing objectiv
	"""
	pass
	
	
def CreateGenericModel():
	"""Creates a generic model
	"""
	pass


def DeleteGenericModel():
	pass

	
def CameraSplineFromFile():
	"""Move camera along a spline
	"""
	pass
	
	
def ShowTimer():
	"""Show timer for a player
	"""
	pass
	
	
def SetMRBState():
	"""Set State on MRB
	"""
	pass
	
	
def SetGameModePauseState():
	"""Set state on game mode. Disabling the game mode pauses the counter, disables the reinforcement and support menus, command points and domination bar. Can be used for entering scripted sessions on skirmish levels
	"""
	pass
	
	
def SetCoreSystemState():
	"""Set status on core system
	"""
	pass
	
	
def ShowMinimapIcon():
	"""Show icon on the minima
	"""
	pass
	
	
def FadeIn():
	"""Fade in when game starte
	"""
	pass
	
	
def EnableDropzone():
	"""Enable dropzone in singleplaye
	"""
	pass
	
	
def SetDropzone():
	"""Set dropzone in singleplaye
	"""
	pass
	
	
def GetDropzone():
	"""Get dropzone in singleplaye
	"""
	pass
	
	
def AddScriptEvent():
	"""Add new scripted event to a client's visible queu
	"""
	pass
	
	
def AddScriptEventAll():
	"""Add new scripted event to all clients' visible queue
	"""
	pass
	
	
def SetCommandPointActive():
	"""Activate or Deactivate Command Point by nam
	"""
	pass

	
def EnableAI():
	"""Enable or Disable an AI playe
	"""
	pass
	
	
def RemoveAIZone():
	"""Removes a zone from an AI playe
	"""
	pass
	
	
def HideAIZone():
	"""Hides a zone (Command Point) from an AI playe
	"""
	pass
	
	
def HoldAIZone():
	"""Give an AI a command to hold the specified are
	"""
	pass
	
	
def HoldAIZoneLine():
	"""Give an AI a command to hold the specified line
	"""
	pass
	
	
def HoldAICommandPointArea():
	"""Give an AI a command to hold the specified command poin
	"""
	pass
	
	
def EnableAIBuy():
	"""Toggle if the AI should buy units or no
	"""
	pass
	
	
def EnableAITAUse():
	"""Toggle if the AI should use TA or no
	"""
	pass


def DropTAUsingMeAsHost():
	pass
	

def EnableAISpecialAbilities():
	pass


def SetAISpecialAbilityOffensiveFactor():
	pass


def EnableAIInfantryEnterBuildings():
	pass


def SetAITAZones():
	pass


def ScriptDebugOutputAIEnable():
	pass
	
	
def ScriptDebugOutputAIDisable():
	pass


def IsScriptDebugOutputAIEnable():
	pass
	
	
def AddDeploymentZone():
	"""Add DeploymentZone image mask to list of available mask
	"""
	pass
	
	
def RemoveDeploymentZone():
	"""Remove DeploymentZone image mask from list of available mask
	"""
	pass
	
	
def AddDeploymentZoneToTeam():
	"""Give an existing DeploymentZone to a tea
	"""
	pass
	
	
def RemoveDeploymentZoneFromTeam():
	"""Give an existing DeploymentZone to a tea
	"""
	pass
	
	
def GetDeploymentZoneFileName():
	"""Get a filename for deployment zone
	"""
	pass
	
	
def CloneUnitType():
	"""Clone unit type
	"""
	pass
	
	
def OverrideHealthForUnitType():
	"""Override health on a cloned unit type
	"""
	pass
	
	
def GetMovieLength():
	"""Get the length of a cinematics movie
	"""
	pass
	
	
def GetNrOfScenesInMovie():
	"""Get the total number of scenes in a movie
	"""
	pass


def SetApRegrowthRate():
	pass


def SetStartingAP():
	pass


def SetMaxAP():
	pass


def SetUnitScoreToTAMultiplier():
	pass


def SetDomTotalDominationFactor():
	pass


def GetDifficultyLevel():
	pass


def IsLoadedGame():
	pass


def TeleportPlayerUnit():
	pass


def UnitRepair():
	pass


def SetPlayerUnitHealth():
	pass


def SetUnitApOwner():
	pass


def SetUnitCreditValue():
	pass


def GetCameraPosition():
	pass


def GetCameraRotation():
	pass


def GetCameraLookAt():
	pass


def GetCameraHeightToGround():
	pass


def CancelAllSpawners():
	pass


def AddLOSCircle():
	pass


def AddLOSRectangle():
	pass


def RemoveLOSArea():
	pass


def PlayerStopUnit():
	pass


def ShowAllDropships():
	pass


def AddSupportWeapon():
	pass


def RemoveSupportWeapon():
	pass


def ClearSupportWeapons():
	pass


def GetMapName():
	pass


def CompleteMedal():
	pass

def BindGenericModelSoundToBone(aPlayerId, aGenericModelId, aSoundName, aBoneName):
	""" Binds a sound to a specific bone in the generic model, so the sound can follow the bone in the animation """
	pass

def EnableDisbandUnit(anEnableFlag):
	""" Enables/disables disband unit functionality """
	pass
	
def EnableHoldFire(anEnableFlag):
	""" Enables/disables hold fire functionality """
	pass

def EnableSpecialAbilitiesForUnit(aUnitId, anEnableFlag):
	""" Enables/disables special abilities for a specific unit """
	pass

def SetSPEndBlackBackground(aFlag):
	pass

def IgnoreUnit(aUnitId, aUnitIdToIgnore, anIgnoreFlag):
	""" Enables/disables aUnitId's ignoring of another aUnitIdToIgnore """
	pass

def UseOffensiveSpecialAbilityOnUnit(aShootingUnitId, aTargetId, anOverrideCooldownFlag):
	"""
	This should be called from unit.py instead.
	
	aShootingUnitId (int) - The unit id of the shooting unit.
	aTargetUnitId (int) - The unit id of the target unit.
	anOverrideCooldownFlag (int) - If set to 1 this will shoot the special ability and reset the 
		cooldown no matter what, if set to 0 the action will fail as usual if it is on cooldown.
	"""
	pass

def UseDefensiveSpecialAbility(aUnitId, anOverrideCooldownFlag):
	"""
	This should be called from unit.py instead.
	
	aUnitId (int) - The id of the using unit.
	anOverrideCooldownFlag (int) - If set to 1 this will shoot the special ability and reset the 
		cooldown no matter what, if set to 0 the action will fail as usual if it is on cooldown.
	"""
	pass

def ForceSetStance(aUnitId, aStance):
	"""
	aUnitId (int) - The id of the using unit.
	aStance (string) - STAND, CROUCH or PRONE
	"""
	pass

def IsUnitInForest(aUnitId):
	"""
	This should be called from unit.py instead of from here.
	
	aUnitId - The id of the unit.
	"""
	pass
