from serverimports import *
from wicgame.ai import * 
import mapvars

##---------------------------------------------------------------
#---------------------------  Player ----------------------------

def Player( ):
	DebugMessage( 'allunits.Player::' )
	
	# Create a group own by the player that has on heavy NATO tank. 
	mapvars.grpPlayer1 = CreateGroup( 'grpPlayer1', [ NATO_LEOPARD2 ], 'areaPlayerStartPos', PLAYER_HUMAN, TEAM_NATO )
	
	# set how many reinforcements point to get when the unit dies
	SetUnitCreditValue( mapvars.grpPlayer1.myUnits[ 0 ].myUnitId, GetUnitCost( 'NATO_Tank_Leopard2' ) )
	
	# set with player that will get the point
	mapvars.grpPlayer1.SetGroupApOwner( PLAYER_HUMAN )	
		
	# Create one more group, this one own by the script player so that we can do stuff with it before we give it to the player.
	mapvars.grpPlayer2 = CreateGroup( 'grpPlayer2', [ NATO_LEOPARD2 ], 'areaPlayerSpawnPos', PLAYER_SCRIPT, TEAM_NATO )
	SetUnitCreditValue( mapvars.grpPlayer2.myUnits[ 0 ].myUnitId, GetUnitCost( 'NATO_Tank_Leopard2' ) )
	mapvars.grpPlayer2.SetGroupApOwner( PLAYER_HUMAN )
	
	# Now lets post some command on the group, we want it to move to a position and make it look
	# at the CP before we gives it to the player.
	mapvars.grpPlayer2.PostCommand( CMD_RegroupAt( 'areaPlayerStartPos2', 'CP_Village' ) )
	mapvars.grpPlayer2.PostCommand( CMD_SetOwner( PLAYER_HUMAN ) )

	# Set the max and current reinforcement points that we want the player to have. Because we have
	# given the player some starting units we decrease there cost form the max value.
	thePlayers[ PLAYER_HUMAN ].myMaxAP = 6000
	thePlayers[ PLAYER_HUMAN ].myCurrentAP = ( thePlayers[ PLAYER_HUMAN ].myMaxAP - GetUnitCost( [ 'NATO_Tank_Leopard2', 'NATO_Tank_Leopard2' ] ) )
	
	# Set Tactical aid point cap.
	thePlayers[PLAYER_HUMAN].myMaxTacticalAid = 40
	
	# Add units to the reinforcements meny
	AddToSPReinforcement( 'NATO_LandRover' )
	AddToSPReinforcement( 'NATO_Warrior_APC' )
	AddToSPReinforcement( 'NATO_AMX30' )
	AddToSPReinforcement( 'NATO_Chieftain_MkV' )
	AddToSPReinforcement( 'NATO_Tank_Leopard2' )	
	
	# Create a platoon and add the player groups. We are using the platoon to check if all of the players unit has been killed.
	mapvars.pltPlayer = Platoon( [mapvars.grpPlayer1, mapvars.grpPlayer2] ) 

	
def PlayerAward( ):
	DebugMessage( 'allunits.PlayerAward::' )
	
	# add one helicopter with the cost of 0 to the reinforcements meny.
	AddToSPReinforcement( 'NATO_Mangusta', 1, 0 )
	
	

##---------------------------------------------------------------
#---------------------------  Village ---------------------------	
def Village( ):
	DebugMessage( 'allunits.Village::' )
	
	# Create a USSR group that are own by the script player and add an attack and base behaviour.
	mapvars.grpVillageRu1 = CreateGroup( 'grpVillageRu1', [ USSR_BMP_3 ], 'areaVillageSpawn1', PLAYER_SCRIPT, TEAM_USSR )
	mapvars.grpVillageRu1.SetBaseBehavior( BHB_IdleUnits( 'areaVillageRuMove1' ) )
	mapvars.grpVillageRu1.SetAttackBehavior( BHA_StandFast( ) )

	# Create a group that we sets to use cover formation on, that they will try to find position that are some what in cover.
	mapvars.grpVillageRu2 = CreateGroup( 'grpVillageRu2', [ USSR_MARINE, USSR_MARINE, USSR_AA_INFANTRY, USSR_MACHINE_GUNNER, USSR_ANTITANK ], 'areaVillageSpawn3', PLAYER_SCRIPT, TEAM_USSR  )
	mapvars.grpVillageRu2.SetAttackBehavior( BHA_Defensive(  ) )
	mapvars.grpVillageRu2.SetBaseBehavior( BHB_IdleInfantryCover( 'areaVillageRuMove1' ) )
	mapvars.grpVillageRu2.SetFormation( FORMATION_COVER )		
	
	# Creates a USSR group that has two transport units, trucks. Then create two infantry squads that we
	# enter in to the trucks. We make the group a transporters group; it makes that only vehicles in the
	# group will move other wise the infantry will exit the transport when the group gets a move order.
	mapvars.grpVillageRu3 = CreateGroup( 'grpVillageRu3', [ USSR_TRUCK, USSR_TRUCK ], 'areaVillageSpawn2', PLAYER_SCRIPT, TEAM_USSR  )	
	mapvars.grpVillageRu3.CreateSquad( [ USSR_MARINE, USSR_MARINE, USSR_MACHINE_GUNNER, USSR_ANTITANK ], 'areaVillageSpawn2' )
	mapvars.grpVillageRu3.CreateSquad( [ USSR_MARINE, USSR_MARINE, USSR_MACHINE_GUNNER, USSR_ANTITANK ], 'areaVillageSpawn2' )
	mapvars.grpVillageRu3.EnterGroup( None, True )
	mapvars.grpVillageRu3.SetTransporterGroup( True )

	# Move the group 50 units away from the Village CP then unload the infantry and set the attack and base behaviour.
	mapvars.grpVillageRu3.PostCommand( CMD_MoveGroup( 'CP_Village', 50 ) )
	mapvars.grpVillageRu3.PostCommand( CMD_UnloadAll( ) )
	mapvars.grpVillageRu3.PostCommand( CMD_SetTransporterGroup( False ) )
	mapvars.grpVillageRu3.PostCommand( CMD_SetAttackBehavior( BHA_Aggressive( ) ) )
	mapvars.grpVillageRu3.PostCommand( CMD_SetBaseBehavior( BHB_IdleUnits( 'CP_Village' ) ) )
	
	# Create a group that has three squads that we enter in to three buildings.
	mapvars.grpVillageBuilding = CreateGroup( 'grpVillageBuilding', [ ], None, PLAYER_SCRIPT, TEAM_USSR  )
	mapvars.grpVillageBuilding.CreateSquad( [ USSR_MARINE, USSR_ANTITANK ], 'areaVillageSpawn1' )
	mapvars.grpVillageBuilding.CreateSquad( [ USSR_MARINE, USSR_ANTITANK ], 'areaVillageSpawn1' )
	mapvars.grpVillageBuilding.CreateSquad( [ USSR_MARINE, USSR_ANTITANK ], 'areaVillageSpawn1' )
	mapvars.grpVillageBuilding.EnterBuilding( [ 'CountryHouse_03__3', 'CountryHouse_01__2', 'CountryHouse_03__2' ], True )
		
	# Add all the groups in to a non combat platoon, all groups attack behaviour won’t trigger if one of the groups gets in combat.
	mapvars.pltVillage = Platoon( [ mapvars.grpVillageRu1, mapvars.grpVillageRu2, mapvars.grpVillageRu3, mapvars.grpVillageBuilding ] )
	mapvars.pltVillage.SetCombatPlatoon( False )
	

##---------------------------------------------------------------
#---------------------------  Mansion ---------------------------	
def Mansion( ):
	DebugMessage( 'allunits.Mansion::' )
	
	mapvars.grpMansionRuDefenders1 = CreateGroup( 'grpMansionRuDefenders1', [ USSR_T62, USSR_T62 ], 'CP_Mansion', PLAYER_SCRIPT, TEAM_USSR )
	mapvars.grpMansionRuDefenders1.SetBaseBehavior( BHB_CaptureCommandPoint( [ 'PP_Mansion1', 'PP_Mansion2' ] ) )
	mapvars.grpMansionRuDefenders1.SetAttackBehavior( BHA_Aggressive(  ) )

	mapvars.grpMansionRuDefenders2 = CreateGroup( 'grpMansionRuDefenders2', [ USSR_T80U, USSR_T62 ], 'CP_Mansion', PLAYER_SCRIPT, TEAM_USSR )
	mapvars.grpMansionRuDefenders2.SetBaseBehavior( BHB_CaptureCommandPoint( [ 'PP_Mansion1', 'PP_Mansion2' ] ) )

	mapvars.grpMansionRuAttacker1 = CreateGroup( 'grpMansionRuAttacker1', [ ], None, PLAYER_SCRIPT, TEAM_USSR )
	mapvars.grpMansionRuAttacker2 = CreateGroup( 'grpMansionRuAttacker2', [  ], None, PLAYER_SCRIPT, TEAM_USSR )



def MansionAttack( ):
	DebugMessage( 'allunits.MansionAttack::' )
	
	# Ai that buy downs his own units
	mapvars.aiPlayer2Ru = AI( PLAYER2 )
	mapvars.aiPlayer2Ru.Enable( )
	mapvars.aiPlayer2Ru.HoldCommandPoint( 'CP_Mansion' )	

	mapvars.aiPlayer3Ru = AI( PLAYER3 )
	mapvars.aiPlayer3Ru.Enable( )
	mapvars.aiPlayer3Ru.DisableBuy( )
	mapvars.aiPlayer3Ru.DisableTA( )
	mapvars.aiPlayer3Ru.AddGroup( mapvars.grpMansionRuAttacker1 )
	mapvars.aiPlayer3Ru.HoldZone( 'CP_Mansion', 125, None )
	
	mapvars.grpMansionRuAttacker1.SetUseAirDrop( True )
	mapvars.grpMansionRuAttacker1.DropUnitsAtPosition( [ USSR_T80U, USSR_T62, USSR_T62 ], 'areaRuSpawn2' )
	mapvars.grpMansionRuAttacker1.ActivateRefillMode( 2, 3, [ USSR_T80U, USSR_T62, USSR_BMP_3 ], 'areaRuSpawn2', 5, None, 22 )

	mapvars.grpMansionRuAttacker2.DropUnitsAtPosition( [ USSR_PT_76, USSR_T62, USSR_BMP_3 ], 'areaRuSpawn1' )
	mapvars.grpMansionRuAttacker2.SetUseAirDrop( True )
	mapvars.grpMansionRuAttacker2.SetAttackBehavior( BHA_Defensive(  ) )
	mapvars.grpMansionRuAttacker2.SetBaseBehavior( BHB_IdleUnits( 'CP_Mansion', CLOSE_TO_LIMIT * 4, 8, 0.25, 35, 0.2, False, False ) )
	mapvars.grpMansionRuAttacker2.ActivateRefillMode( 1, 3, [ USSR_BMP_3, USSR_T62, USSR_BMP_3 ], 'areaRuSpawn1', 5, None, 20 )



def MansionEnd( ):	
	DebugMessage( 'allunits.MansionEnd::' )
	
	mapvars.aiPlayer2Ru.DisableBuy( )
	mapvars.grpMansionRuAttacker1.DeactivateRefillMode( )
	mapvars.grpMansionRuAttacker2.DeactivateRefillMode( )
	
	
##---------------------------------------------------------------
#--------------------------  LastStand --------------------------	

def LastStandUnitSetup( ):
	#Create empty groups to be able to add them to the platoon.
	mapvars.grpLastStandRu1 = CreateGroup( 'grpLastStandRu1', [], None, PLAYER_SCRIPT, TEAM_USSR )
	mapvars.grpLastStandRu2 = CreateGroup( 'grpLastStandRu2', [], None, PLAYER_SCRIPT, TEAM_USSR )
	mapvars.grpLastStandRu3 = CreateGroup( 'grpLastStandRu3', [], None, PLAYER_SCRIPT, TEAM_USSR )
		
	#Create a platoon of existing, different groups. 
	mapvars.pltLastStandRu = Platoon( [ mapvars.grpLastStandRu1, mapvars.grpLastStandRu2, mapvars.grpLastStandRu3, mapvars.grpMansionRuAttacker2 ] )
	mapvars.grpMansionRuAttacker1.MakeActive( ) 
	mapvars.pltLastStandRu.AddGroup( mapvars.grpMansionRuAttacker1 )

#--------
#The following code could be written in the same function, but I wanna be able to create the units at different time and 
def LastStand1( ):
	DebugMessage( 'allunits.LastStand1::' )
	mapvars.grpLastStandRu1.DropUnitsAtPosition( [ USSR_T62, USSR_T62, USSR_T80U, USSR_BMP_3 ], 'areaPlayerStartPos' )
	mapvars.grpLastStandRu1.SetBaseBehavior( BHB_IdleUnits( 'CP_Mansion' ) ) 

	mapvars.grpLastStandRu1.PostCommand( CMD_MoveGroup( 'areaVillageSpawn3' ) )
	mapvars.grpLastStandRu1.PostCommand( CMD_MoveGroup( 'CP_Mansion', 30 ) )
	mapvars.grpLastStandRu1.PostCommand( CMD_SetAttackBehavior( BHA_Aggressive( 60 ) ) )
	
	
	
def LastStand2( ):
	DebugMessage( 'allunits.LastStand2::' )
	mapvars.grpLastStandRu2.DropUnitsAtPosition( [ USSR_BMP_R, USSR_JEEP, USSR_T80U ], 'areaRuSpawn2' )
	#First Delay, how often they shall move. How far away from the target they can move (+/-). The target.
	mapvars.grpLastStandRu2.SetBaseBehavior( BHB_MoveRandomly( 2, 5, 'PotPlant__19' ) ) 
	mapvars.grpLastStandRu2.SetAttackBehavior( BHA_Defensive( ) ) 
		
def LastStand3( ):
	DebugMessage( 'allunits.LastStand3::' )
	mapvars.grpLastStandRu3.DropUnitsAtPosition( [ USSR_T62, USSR_T62, USSR_T80U], 'areaAASpawn2' )
	aPatrolList1 = [ 'areaPat1', 'areaPat2', 'areaRuSpawn2', 'areaPat2', 'areaPat1' ]
	mapvars.grpLastStandRu3.SetSpeed( 4 ) 
	mapvars.grpLastStandRu3.SetBaseBehavior( BHB_Patrol( aPatrolList1, BHB_PATROL_ALLPOINTS_DELAY, 15, BHB_PATROL_NORMAL, False, 36 ) )
	mapvars.grpLastStandRu3.SetAttackBehavior( BHA_Defensive( ) )
	
	

##---------------------------------------------------------------
#--------------------------  DestroyAA --------------------------	
def DestroyAA( ):
	DebugMessage( 'allunits.DestroyAA::' )
	
	mapvars.grpDestroyAA1 = CreateGroup( 'grpDestroyAA1', [ USSR_ZSU_SHILKA ], 'areaAASpawn1', PLAYER_SCRIPT, TEAM_USSR )	
	mapvars.grpDestroyAA2 = CreateGroup( 'grpDestroyAA2', [ USSR_ZSU_SHILKA ], 'areaAASpawn2', PLAYER_SCRIPT, TEAM_USSR )
	mapvars.grpDestroyAA3 = CreateGroup( 'grpDestroyAA3', [ USSR_ZSU_SHILKA ], 'areaAASpawn3', PLAYER_SCRIPT, TEAM_USSR )



##---------------------------------------------------------------
#-------------------------  RescueArty  -------------------------	

def RescueArty( ):
	DebugMessage( 'allunits.RescueArty::' )
	
	mapvars.grpRescueArty = CreateGroup( 'grpRescueArty', [ NATO_LARS_SF_2 ], 'areaArtySpawn', PLAYER_SCRIPT, TEAM_NATO )
	mapvars.grpRescueArty.SetInvulnerable( True )
	mapvars.grpRescueArty.RegroupAt( 'areaArtySpawn', 'areaAASpawn1' )
	mapvars.grpRescueArty.SetBaseBehavior( BHB_AreaArtillery( [ Area( 'areaKillArtyFire1', 40 ), Area( 'areaKillArtyFire2', 40 ), Area( 'areaKillArtyFire3', 40 ) ], 15  ) )
	
	mapvars.grpRescueArtyRu1 = CreateGroup( 'grpRescueArtyRu1', [  ], '', PLAYER_SCRIPT, TEAM_USSR )


def RescueArtyAttack( ):
	DebugMessage( 'allunits.RescueArtyAttack::' )
	mapvars.grpRescueArty.SetInvulnerable( False )	
	
	mapvars.grpRescueArtyRu1.CreateUnitsAtPosition( [ USSR_BMP_R, USSR_BMP_R ], 'areaKillArtyRuSpawn' )
	mapvars.grpRescueArtyRu1.SetSpeed( 7 )
	mapvars.grpRescueArtyRu1.SetAttackBehavior( BHA_Defensive( 40 ) )
	
	mapvars.grpRescueArtyRu1.PostCommand( CMD_RegroupAt( 'areaKillArtyRuMove1', 'areaArtySpawn' ) )
	mapvars.grpRescueArtyRu1.PostCommand( CMD_SetBaseBehavior( BHB_HoldPosition( 'areaKillArtyRuMove1' ) ) )


def RescueArtyGetUnit( ):
	DebugMessage( 'allunits.RescueArtyGetUnit::' )
	
	# Remove all behavior from the group
	mapvars.grpRescueArty.Purge( )
	
	# Give the unit to the player 
	mapvars.grpRescueArty.SetOwner( PLAYER_HUMAN )

	
	
##---------------------------------------------------------------
#-----------------------  DestroyHideouts  ----------------------

def DestroyHideouts( ):
	DebugMessage( 'allunits.DestroyHideouts::' )
	
	mapvars.grpDestroyHideouts = CreateGroup( '', [ ], None, PLAYER_SCRIPT, TEAM_USSR )
	
	if building.Building( 'Barn__3' ).myHealth >= 0:
		mapvars.grpDestroyHideouts.CreateSquad( [ USSR_ANTITANK, USSR_ANTITANK ], 'areaRuSpawn1' )
	
	if building.Building( 'CountryHouse_01__5' ).myHealth >= 0:
		mapvars.grpDestroyHideouts.CreateSquad( [ USSR_ANTITANK, USSR_ANTITANK ], 'areaRuSpawn1' )
	
	if building.Building( 'CountryHouse_02_V2__4' ).myHealth >= 0:		
		mapvars.grpDestroyHideouts.CreateSquad( [ USSR_ANTITANK, USSR_ANTITANK ], 'areaRuSpawn1' )
	
	mapvars.grpDestroyHideouts.EnterBuilding( [ 'Barn__3', 'CountryHouse_01__5', 'CountryHouse_02_V2__4' ], True )
	
	# Set the experience level for all units in the group 
	mapvars.grpDestroyHideouts.SetMaxExperienceLevel( )
	



##---------------------------------------------------------------
#----------------------  Ambiance Fighting  ---------------------

def AmbianceFighting( ):
		
	mapvars.grpAmbFightRu = CreateGroup( 'grpAmbFightRu', [ ], None, PLAYER_SCRIPT, TEAM_USSR )
	
	mapvars.aiPlayer5Ru = AI( PLAYER5 )
	mapvars.aiPlayer5Ru.Enable( )
	mapvars.aiPlayer5Ru.DisableBuy( )
	mapvars.aiPlayer5Ru.DisableTA( )
	mapvars.aiPlayer5Ru.AddGroup( mapvars.grpAmbFightRu )
	mapvars.aiPlayer5Ru.HoldZoneLine( [ GetPosition( 'areaAmbFightRuLine1' ), GetPosition( 'areaAmbFightRuLine2' ) ], 30,  [ GetPosition( 'areaAmbFightRu' ), 150 ], False, True )
	
	
	mapvars.grpAmbFightRu.SetUseAirDrop( True )
	mapvars.grpAmbFightRu.DropUnitsAtPosition( [ USSR_T80U, USSR_T80U, USSR_T62, USSR_T62, USSR_T62 ], 'areaRuSpawn2' )
	mapvars.grpAmbFightRu.ActivateRefillMode( 2, 3, [ USSR_T80U, USSR_T62, USSR_T62 ], 'areaRuSpawn2', 5, None, 10 )

	
	mapvars.grpAmbFightNato = CreateGroup( 'grpAmbFightNato', [ ], None, PLAYER_SCRIPT, TEAM_NATO )
	
	mapvars.aiPlayer4Nato = AI( PLAYER4 )
	mapvars.aiPlayer4Nato.Enable( )
	mapvars.aiPlayer4Nato.DisableBuy( )
	mapvars.aiPlayer4Nato.DisableTA( )
	mapvars.aiPlayer4Nato.AddGroup( mapvars.grpAmbFightNato )
	mapvars.aiPlayer4Nato.HoldZone( 'areaAmbFightNato', 70, None )
	
	mapvars.grpAmbFightNato.SetUseAirDrop( True )
	mapvars.grpAmbFightNato.DropUnitsAtPosition( [ NATO_LEOPARD2, NATO_CHIEFTAIN_MKV, NATO_CHIEFTAIN_MKV, NATO_CHIEFTAIN_MKV ], 'areaCamStartPos' )
	mapvars.grpAmbFightNato.ActivateRefillMode( 2, 2, [ NATO_LEOPARD2, NATO_CHIEFTAIN_MKV, NATO_CHIEFTAIN_MKV ], 'areaCamStartPos', 5, None, 10 )
	

	
def AmbianceFightingEnd( ):
	mapvars.grpAmbFightRu.DeactivateRefillMode( True )
	


