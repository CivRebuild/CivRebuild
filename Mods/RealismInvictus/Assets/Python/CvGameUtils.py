# Sid Meier's Civilization 4
# Copyright Firaxis Games 2005
##
# Implementaion of miscellaneous game functions

import CvUtil

from CvPythonExtensions import *
from CvPythonEngine import *

import CvEventInterface
import Consts as con

## Revolutions ##
from Components import Revolutions
## Revolutions ##

# globals
gc = CyGlobalContext()


class CvGameUtils:
	"Miscellaneous game functions"

	def __init__(self):
		pass

	def isVictoryTest(self):
		if (gc.getGame().getElapsedGameTurns() > 10):
			return True
		else:
			return False

	def isVictory(self, argsList):
		eVictory = argsList[0]
		return True

	def isPlayerResearch(self, argsList):
		ePlayer = argsList[0]
		return True

	def getExtraCost(self, argsList):
		ePlayer = argsList[0]
		return 0

	def createBarbarianCities(self):
		return False

	def createBarbarianUnits(self):
		return False

	def skipResearchPopup(self, argsList):
		ePlayer = argsList[0]
		return False

	def showTechChooserButton(self, argsList):
		ePlayer = argsList[0]
		return True

	def getFirstRecommendedTech(self, argsList):
		ePlayer = argsList[0]
		return TechTypes.NO_TECH

	def getSecondRecommendedTech(self, argsList):
		ePlayer = argsList[0]
		eFirstTech = argsList[1]
		return TechTypes.NO_TECH

	def canRazeCity(self, argsList):
		iRazingPlayer, pCity = argsList
		return True

	def canDeclareWar(self, argsList):
		iAttackingTeam, iDefendingTeam = argsList
		return True

	def skipProductionPopup(self, argsList):
		pCity = argsList[0]
		return False

	def showExamineCityButton(self, argsList):
		pCity = argsList[0]
		return True

	def getRecommendedUnit(self, argsList):
		pCity = argsList[0]
		return UnitTypes.NO_UNIT

	def getRecommendedBuilding(self, argsList):
		pCity = argsList[0]
		return BuildingTypes.NO_BUILDING

	def updateColoredPlots(self):
		return False

	def isActionRecommended(self, argsList):
		pUnit = argsList[0]
		iAction = argsList[1]
		return False

	def unitCannotMoveInto(self, argsList):
		ePlayer = argsList[0]
		iUnitId = argsList[1]
		iPlotX = argsList[2]
		iPlotY = argsList[3]
		return False

	def cannotHandleAction(self, argsList):
		pPlot = argsList[0]
		iAction = argsList[1]
		bTestVisible = argsList[2]
		return False

	def canBuild(self, argsList):
		iX, iY, iBuild, iPlayer = argsList
		return -1  # Returning -1 means ignore; 0 means Build cannot be performed; 1 or greater means it can

	def cannotFoundCity(self, argsList):
		iPlayer, iPlotX, iPlotY = argsList
		return False

	def cannotSelectionListMove(self, argsList):
		pPlot = argsList[0]
		bAlt = argsList[1]
		bShift = argsList[2]
		bCtrl = argsList[3]
		return False

	def cannotSelectionListGameNetMessage(self, argsList):
		eMessage = argsList[0]
		iData2 = argsList[1]
		iData3 = argsList[2]
		iData4 = argsList[3]
		iFlags = argsList[4]
		bAlt = argsList[5]
		bShift = argsList[6]
		return False

	def cannotDoControl(self, argsList):
		eControl = argsList[0]
		return False

	def canResearch(self, argsList):
		ePlayer = argsList[0]
		eTech = argsList[1]
		bTrade = argsList[2]
		return False

	def cannotResearch(self, argsList):
		ePlayer = argsList[0]
		eTech = argsList[1]
		bTrade = argsList[2]
		return False

	def canDoCivic(self, argsList):
		ePlayer = argsList[0]
		eCivic = argsList[1]
		return False

	def cannotDoCivic(self, argsList):
		ePlayer = argsList[0]
		eCivic = argsList[1]
		return False

	def canTrain(self, argsList):
		pCity = argsList[0]
		eUnit = argsList[1]
		bContinue = argsList[2]
		bTestVisible = argsList[3]
		bIgnoreCost = argsList[4]
		bIgnoreUpgrades = argsList[5]
		return False

	def cannotTrain(self, argsList):
		pCity = argsList[0]
		eUnit = argsList[1]
		bContinue = argsList[2]
		bTestVisible = argsList[3]
		bIgnoreCost = argsList[4]
		bIgnoreUpgrades = argsList[5]
		return False

	def canConstruct(self, argsList):
		pCity = argsList[0]
		eBuilding = argsList[1]
		bContinue = argsList[2]
		bTestVisible = argsList[3]
		bIgnoreCost = argsList[4]
		return False

	def cannotConstruct(self, argsList):
		pCity = argsList[0]
		eBuilding = argsList[1]
		bContinue = argsList[2]
		bTestVisible = argsList[3]
		bIgnoreCost = argsList[4]
		return False

	def canCreate(self, argsList):
		pCity = argsList[0]
		eProject = argsList[1]
		bContinue = argsList[2]
		bTestVisible = argsList[3]
		return False

	def cannotCreate(self, argsList):
		pCity = argsList[0]
		eProject = argsList[1]
		bContinue = argsList[2]
		bTestVisible = argsList[3]
		return False

	def canMaintain(self, argsList):
		pCity = argsList[0]
		eProcess = argsList[1]
		bContinue = argsList[2]
		return False

	def cannotMaintain(self, argsList):
		pCity = argsList[0]
		eProcess = argsList[1]
		bContinue = argsList[2]
		return False

	def AI_chooseTech(self, argsList):
		ePlayer = argsList[0]
		bFree = argsList[1]
		return TechTypes.NO_TECH

	def AI_chooseProduction(self, argsList):
		pCity = argsList[0]
		return False

	def AI_unitUpdate(self, argsList):
		pUnit = argsList[0]
		return False

	def AI_doWar(self, argsList):
		eTeam = argsList[0]
		return False

	def AI_doDiplo(self, argsList):
		ePlayer = argsList[0]
		return False

	def calculateScore(self, argsList):
		ePlayer = argsList[0]
		bFinal = argsList[1]
		bVictory = argsList[2]

		iPopulationScore = CvUtil.getScoreComponent(
			gc.getPlayer(ePlayer).getPopScore(),
			gc.getGame().getInitPopulation(),
			gc.getGame().getMaxPopulation(),
			gc.getDefineINT("SCORE_POPULATION_FACTOR"),
			True,
			bFinal,
			bVictory
		)
		iLandScore = CvUtil.getScoreComponent(
			gc.getPlayer(ePlayer).getLandScore(),
			gc.getGame().getInitLand(),
			gc.getGame().getMaxLand(),
			gc.getDefineINT("SCORE_LAND_FACTOR"),
			True,
			bFinal,
			bVictory
		)
		iTechScore = CvUtil.getScoreComponent(
			gc.getPlayer(ePlayer).getTechScore(),
			gc.getGame().getInitTech(),
			gc.getGame().getMaxTech(),
			gc.getDefineINT("SCORE_TECH_FACTOR"),
			True,
			bFinal,
			bVictory
		)
		iWondersScore = CvUtil.getScoreComponent(
			gc.getPlayer(ePlayer).getWondersScore(),
			gc.getGame().getInitWonders(),
			gc.getGame().getMaxWonders(),
			gc.getDefineINT("SCORE_WONDER_FACTOR"),
			False,
			bFinal,
			bVictory
		)
		# MOD - START - Handicap Score Modifier
		# return int(iPopulationScore + iLandScore + iWondersScore + iTechScore)

		iModifier = gc.getPlayer(ePlayer).getHandicapScoreModifier()

		iTotalScore = int(iPopulationScore + iLandScore + iWondersScore + iTechScore)
		iTotalScore *= max(0, 100 + iModifier)
		iTotalScore /= 100

		return int(iTotalScore)
		# MOD - END - Handicap Score Modifier

	def doHolyCity(self):
		return False

	def doHolyCityTech(self, argsList):
		eTeam = argsList[0]
		ePlayer = argsList[1]
		eTech = argsList[2]
		bFirst = argsList[3]
		return False

	def doGold(self, argsList):
		ePlayer = argsList[0]
		return False

	def doResearch(self, argsList):
		ePlayer = argsList[0]
		return False

	def doGoody(self, argsList):
		ePlayer = argsList[0]
		pPlot = argsList[1]
		pUnit = argsList[2]
		return False

	def doGrowth(self, argsList):
		pCity = argsList[0]
		return False

	def doProduction(self, argsList):
		pCity = argsList[0]
		return False

	def doCulture(self, argsList):
		pCity = argsList[0]
		return False

	def doPlotCulture(self, argsList):
		pCity = argsList[0]
		bUpdate = argsList[1]
		ePlayer = argsList[2]
		iCultureRate = argsList[3]
		return False

	def doReligion(self, argsList):
		pCity = argsList[0]
		return False

	def cannotSpreadReligion(self, argsList):
		iOwner, iUnitID, iReligion, iX, iY = argsList[0]
		return False

	def doGreatPeople(self, argsList):
		pCity = argsList[0]
		return False

	def doMeltdown(self, argsList):
		pCity = argsList[0]
		return False

	def doReviveActivePlayer(self, argsList):
		"allows you to perform an action after an AIAutoPlay"
		iPlayer = argsList[0]
		return False

	def doPillageGold(self, argsList):
		"controls the gold result of pillaging"
		pPlot = argsList[0]
		pUnit = argsList[1]

		iPillageGold = 0
		iPillageGold = CyGame().getSorenRandNum(gc.getImprovementInfo(pPlot.getImprovementType()).getPillageGold(), "Pillage Gold 1")
		iPillageGold += CyGame().getSorenRandNum(gc.getImprovementInfo(pPlot.getImprovementType()).getPillageGold(), "Pillage Gold 2")

		iPillageGold += (pUnit.getPillageChange() * iPillageGold) / 100

		return iPillageGold

	def doCityCaptureGold(self, argsList):
		"controls the gold result of capturing a city"

		pOldCity = argsList[0]

		iCaptureGold = 0

		iCaptureGold += gc.getDefineINT("BASE_CAPTURE_GOLD")
		iCaptureGold += (pOldCity.getPopulation() * gc.getDefineINT("CAPTURE_GOLD_PER_POPULATION"))
		iCaptureGold += CyGame().getSorenRandNum(gc.getDefineINT("CAPTURE_GOLD_RAND1"), "Capture Gold 1")
		iCaptureGold += CyGame().getSorenRandNum(gc.getDefineINT("CAPTURE_GOLD_RAND2"), "Capture Gold 2")

		if (gc.getDefineINT("CAPTURE_GOLD_MAX_TURNS") > 0):
			iCaptureGold *= cyIntRange((CyGame().getGameTurn() - pOldCity.getGameTurnAcquired()), 0, gc.getDefineINT("CAPTURE_GOLD_MAX_TURNS"))
			iCaptureGold /= gc.getDefineINT("CAPTURE_GOLD_MAX_TURNS")

		return iCaptureGold

	def citiesDestroyFeatures(self, argsList):
		iX, iY = argsList
		return True

	def canFoundCitiesOnWater(self, argsList):
		iX, iY = argsList
		return False

	def doCombat(self, argsList):
		pSelectionGroup, pDestPlot = argsList
		return False

	def getConscriptUnitType(self, argsList):
		iPlayer = argsList[0]
		iConscriptUnitType = -1  # return this with the value of the UNIT TYPE you want to be conscripted, -1 uses default system

		return iConscriptUnitType

	def getCityFoundValue(self, argsList):
		iPlayer, iPlotX, iPlotY = argsList
		iFoundValue = -1  # Any value besides -1 will be used

		return iFoundValue

	def canPickPlot(self, argsList):
		pPlot = argsList[0]
		return true

	def getUnitCostMod(self, argsList):
		iPlayer, iUnit = argsList
		iCostMod = -1  # Any value > 0 will be used

		return iCostMod

	def getBuildingCostMod(self, argsList):
		iPlayer, iCityID, iBuilding = argsList
		pPlayer = gc.getPlayer(iPlayer)
		pCity = pPlayer.getCity(iCityID)

		iCostMod = -1  # Any value > 0 will be used

		# MOD - START - Wonder production cost modifier
		# possible place to set various building cost modifiers: this is a vanilla Firaxis python callback, only need to enable the USE_GET_BUILDING_COST_MOD_CALLBACK for it
		# maybe it's still better to do it directly through the .dll, with proper XML tags
		# if pPlayer.isCivic(con.iPastoralNomadism):
		#	BuildingInfo = gc.getBuildingInfo(iBuilding)
		#	if isWorldWonderClass(BuildingInfo.getBuildingClassType()) or isNationalWonderClass(BuildingInfo.getBuildingClassType()):
		#	#if isLimitedWonderClass(BuildingInfo.getBuildingClassType()):
		#		iCostMod = 150 # iCostMod is % of the original production cost
		# MOD - END - Wonder production cost modifier

		return iCostMod

	def canUpgradeAnywhere(self, argsList):
		pUnit = argsList

		bCanUpgradeAnywhere = 0

		return bCanUpgradeAnywhere

	def getWidgetHelp(self, argsList):
		eWidgetType, iData1, iData2, bOption = argsList
## Platy WorldBuilder ##
		if eWidgetType == WidgetTypes.WIDGET_PYTHON:
			if iData1 == 1027:
				return CyTranslator().getText("TXT_KEY_WB_PLOT_DATA", ())
			elif iData1 == 1028:
				return gc.getGameOptionInfo(iData2).getHelp()
			elif iData1 == 1029:
				if iData2 == 0:
					sText = CyTranslator().getText("TXT_KEY_WB_PYTHON", ())
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onFirstContact"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onChangeWar"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onVassalState"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onCityAcquired"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onCityBuilt"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onCultureExpansion"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onGoldenAge"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onEndGoldenAge"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onGreatPersonBorn"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onPlayerChangeStateReligion"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onReligionFounded"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onReligionSpread"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onReligionRemove"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onCorporationFounded"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onCorporationSpread"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onCorporationRemove"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onUnitCreated"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onUnitLost"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onUnitPromoted"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onBuildingBuilt"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onProjectBuilt"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onTechAcquired"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onImprovementBuilt"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onImprovementDestroyed"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onRouteBuilt"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onPlotRevealed"
					return sText
				elif iData2 == 1:
					return CyTranslator().getText("TXT_KEY_WB_PLAYER_DATA", ())
				elif iData2 == 2:
					return CyTranslator().getText("TXT_KEY_WB_TEAM_DATA", ())
				elif iData2 == 3:
					return CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_TECH", ())
				elif iData2 == 4:
					return CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_PROJECT", ())
				elif iData2 == 5:
					return CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_UNIT", ()) + " + " + CyTranslator().getText("TXT_KEY_CONCEPT_CITIES", ())
				elif iData2 == 6:
					return CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_PROMOTION", ())
				elif iData2 == 7:
					return CyTranslator().getText("TXT_KEY_WB_CITY_DATA2", ())
				elif iData2 == 8:
					return CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_BUILDING", ())
				elif iData2 == 9:
					return "Platy Builder\nVersion: 4.17b"
				elif iData2 == 10:
					return CyTranslator().getText("TXT_KEY_CONCEPT_EVENTS", ())
				elif iData2 == 11:
					return CyTranslator().getText("TXT_KEY_WB_RIVER_PLACEMENT", ())
				elif iData2 == 12:
					return CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_IMPROVEMENT", ())
				elif iData2 == 13:
					return CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_BONUS", ())
				elif iData2 == 14:
					return CyTranslator().getText("TXT_KEY_WB_PLOT_TYPE", ())
				elif iData2 == 15:
					return CyTranslator().getText("TXT_KEY_CONCEPT_TERRAIN", ())
				elif iData2 == 16:
					return CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_ROUTE", ())
				elif iData2 == 17:
					return CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_FEATURE", ())
				elif iData2 == 18:
					return CyTranslator().getText("TXT_KEY_MISSION_BUILD_CITY", ())
				elif iData2 == 19:
					return CyTranslator().getText("TXT_KEY_WB_ADD_BUILDINGS", ())
				elif iData2 == 20:
					return CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_RELIGION", ())
				elif iData2 == 21:
					return CyTranslator().getText("TXT_KEY_CONCEPT_CORPORATIONS", ())
				elif iData2 == 22:
					return CyTranslator().getText("TXT_KEY_ESPIONAGE_CULTURE", ())
				elif iData2 == 23:
					return CyTranslator().getText("TXT_KEY_PITBOSS_GAME_OPTIONS", ())
				elif iData2 == 24:
					return CyTranslator().getText("TXT_KEY_WB_SENSIBILITY", ())
				elif iData2 == 27:
					return CyTranslator().getText("TXT_KEY_WB_ADD_UNITS", ())
				elif iData2 == 28:
					return CyTranslator().getText("TXT_KEY_WB_TERRITORY", ())
				elif iData2 == 29:
					return CyTranslator().getText("TXT_KEY_WB_ERASE_ALL_PLOTS", ())
				elif iData2 == 30:
					return CyTranslator().getText("TXT_KEY_WB_REPEATABLE", ())
				elif iData2 == 31:
					return CyTranslator().getText("TXT_KEY_PEDIA_HIDE_INACTIVE", ())
				elif iData2 == 32:
					return CyTranslator().getText("TXT_KEY_WB_STARTING_PLOT", ())
				elif iData2 == 33:
					return CyTranslator().getText("TXT_KEY_INFO_SCREEN", ())
				elif iData2 == 34:
					return CyTranslator().getText("TXT_KEY_CONCEPT_TRADE", ())
			elif iData1 > 1029 and iData1 < 1040:
				if iData1 % 2:
					return "-"
				return "+"
			elif iData1 == 1041:
				return CyTranslator().getText("TXT_KEY_WB_KILL", ())
			elif iData1 == 1042:
				return CyTranslator().getText("TXT_KEY_MISSION_SKIP", ())
			elif iData1 == 1043:
				if iData2 == 0:
					return CyTranslator().getText("TXT_KEY_WB_DONE", ())
				elif iData2 == 1:
					return CyTranslator().getText("TXT_KEY_WB_FORTIFY", ())
				elif iData2 == 2:
					return CyTranslator().getText("TXT_KEY_WB_WAIT", ())
## Revolutions ##
			elif iData1 > 5999 and iData1 < 6100:
				iPlayer = iData1 - 6000
				pRevPlayer = gc.getPlayer(iPlayer)
				pCity = gc.getPlayer(iPlayer).getCity(iData2)
				if pCity.isNone():
					return ""
				iGlobalModifier = pRevPlayer.getRevModifier()
				sText = CyTranslator().getText("[ICON_UNHAPPY]", ()) + ": " + str(Revolutions.Revolutions().getRevHappy(pCity)) + "\n"
				sText += CyTranslator().getText("[ICON_UNHEALTHY]", ()) + ": " + str(Revolutions.Revolutions().getRevHealth(pCity)) + "\n"
				sText += CyTranslator().getText("[ICON_RELIGION]", ()) + ": " + str(Revolutions.Revolutions().getRevReligion(pCity, iPlayer)) + "\n"
				sText += CyTranslator().getText("[ICON_CULTURE]", ()) + ": " + str(int(Revolutions.Revolutions().getRevNationality(pCity, iPlayer))) + "\n"
				sText += CyTranslator().getText("[ICON_OCCUPATION]", ()) + ": " + str(Revolutions.Revolutions().getRevOccupation(pCity)) + "\n"
				sText += CyTranslator().getText("[ICON_DEFENSE]", ()) + ": " + str(Revolutions.Revolutions().getRevDefenders(pCity, iPlayer)) + "\n"
				sText += CyTranslator().getText("[ICON_ANGRYPOP]", ()) + ": " + str(Revolutions.Revolutions().getRevPopulation(pCity)) + "\n"
				sText += CyTranslator().getText("[ICON_ESPIONAGE]", ()) + ": " + str(Revolutions.Revolutions().getRevEspionage(pCity)) + "\n"
				sText += CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_CIVIC", ()) + ": " + str(Revolutions.Revolutions().getRevCivics(pCity, iPlayer)) + "\n"
				sText += CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_BUILDING", ()) + u" %c" % (CyGame().getSymbolID(FontSymbols.SEPARATISM_POS_CHAR)) + ": " + str(Revolutions.Revolutions().getRevBuildingsPositive(pCity)) + "\n"
				sText += CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_BUILDING", ()) + u" %c" % (CyGame().getSymbolID(FontSymbols.SEPARATISM_NEG_CHAR)) + ": " + str(Revolutions.Revolutions().getRevBuildingsNegative(pCity)) + "\n"
				sText += CyTranslator().getText("TXT_KEY_REVOLUTION_TOTAL", ()) + u" %c" % (CyGame().getSymbolID(FontSymbols.SEPARATISM_POS_CHAR)) + ": " + str(Revolutions.Revolutions().getRevPositives(pCity, iPlayer)) + "\n"
				sText += CyTranslator().getText("TXT_KEY_REVOLUTION_TOTAL", ()) + u" %c" % (CyGame().getSymbolID(FontSymbols.SEPARATISM_NEG_CHAR)) + ": " + str(Revolutions.Revolutions().getRevNegatives(pCity, iPlayer, iGlobalModifier)) + "\n"
				sText += CyTranslator().getText("Modifiers", ()) + ": " + str(iGlobalModifier) + str("%")
				return sText
			elif iData1 == 7474:
				return CyTranslator().getText("TXT_KEY_REVOLUTION_WATCH", ())
## Revolutions ##
			elif iData1 == 6785:
				return CyGameTextMgr().getProjectHelp(iData2, False, CyCity())
			elif iData1 == 6787:
				return gc.getProcessInfo(iData2).getDescription()
			elif iData1 == 6788:
				if iData2 == -1:
					return CyTranslator().getText("TXT_KEY_CULTURELEVEL_NONE", ())
				return gc.getRouteInfo(iData2).getDescription()
## Great People Bar ##
			elif iData1 > 7199 and iData1 < 7300:
				iPlayer = iData1 - 7200
				pPlayer = gc.getPlayer(iPlayer)
				pCity = pPlayer.getCity(iData2)
				if CyGame().GetWorldBuilderMode():
					return pCity.getName()
## Tech Widget Text##
			elif iData1 == 7871:
				return CyGameTextMgr().getTechHelp(iData2, False, False, False, False, -1)
## Civilization Widget Text##
			elif iData1 == 7872:
				iCiv = iData2 % 10000
				return CyGameTextMgr().parseCivInfos(iCiv, False)
## Promotion Widget Text##
			elif iData1 == 7873:
				return CyGameTextMgr().getPromotionHelp(iData2, False)
## Feature Widget Text##
			elif iData1 == 7874:
				if iData2 >= 0:
					iFeature = iData2 % 10000
				else:
					iFeature = -1
				return CyGameTextMgr().getFeatureHelp(iFeature, False)
## Terrain Widget Text##
			elif iData1 == 7875:
				return CyGameTextMgr().getTerrainHelp(iData2, False)
## Leader Widget Text##
			elif iData1 == 7876:
				iLeader = iData2 % 1000
				return CyGameTextMgr().parseLeaderTraits(iLeader, -1, False, False)
## Improvement Widget Text##
			elif iData1 == 7877:
				# MOD - START - Improved Civilopedia
				# return CyGameTextMgr().getImprovementHelp(iData2, False)
				return CyGameTextMgr().getImprovementHelp(iData2, False, False)
				# MOD - END - Improved Civilopedia
## Bonus Widget Text##
			elif iData1 == 7878:
				return CyGameTextMgr().getBonusHelp(iData2, False)
## Specialist Widget Text##
			elif iData1 == 7879:
				return CyGameTextMgr().getSpecialistHelp(iData2, False)
## Corporation Screen ##
			elif iData1 == 8201 or iData1 == 6782:
				return CyGameTextMgr().parseCorporationInfo(iData2, False)
## Military Screen ##
			elif iData1 == 8202:
				if iData2 == -1:
					return CyTranslator().getText("TXT_KEY_PEDIA_ALL_UNITS", ())
				return CyGameTextMgr().getUnitHelp(iData2, False, False, False, None)
			elif iData1 > 8299 and iData1 < 8400:
				iPlayer = iData1 - 8300
				pUnit = gc.getPlayer(iPlayer).getUnit(iData2)
				return CyGameTextMgr().getSpecificUnitHelp(pUnit, true, false)
## Civics Screen ##
			elif iData1 == 8205 or iData1 == 8206:
				sText = CyGameTextMgr().parseCivicInfo(iData2, False, True, False)
				if gc.getCivicInfo(iData2).getUpkeep() > -1:
					sText += "\n" + gc.getUpkeepInfo(gc.getCivicInfo(iData2).getUpkeep()).getDescription()
				else:
					sText += "\n" + CyTranslator().getText("TXT_KEY_CIVICS_SCREEN_NO_UPKEEP", ())
				return sText
## Platy WorldBuilder ##
		return u""

	def getUpgradePriceOverride(self, argsList):
		iPlayer, iUnitID, iUnitTypeUpgrade = argsList

		return -1  # Any value 0 or above will be used

	def getExperienceNeeded(self, argsList):
		# use this function to set how much experience a unit needs
		iLevel, iOwner = argsList

		iExperienceNeeded = 0

		# regular epic game experience
		iExperienceNeeded = iLevel * iLevel + 1

		iModifier = gc.getPlayer(iOwner).getLevelExperienceModifier()
		if (0 != iModifier):
			iExperienceNeeded += (iExperienceNeeded * iModifier + 99) / 100   # ROUND UP

		return iExperienceNeeded

