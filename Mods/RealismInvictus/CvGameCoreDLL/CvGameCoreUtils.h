#pragma once

// utils.h

#ifndef CIV4_GAMECORE_UTILS_H
#define CIV4_GAMECORE_UTILS_H

//#include "CvGameCoreDLL.h"
#include "CvStructs.h"
#include "CvGlobals.h"
#include "CvSelectionGroup.h"
#include "CvMap.h"
#include "FAssert.h"

#if not defined(__GNUC__) //PORT NEW
#ifndef _USRDLL
// use non inline functions when not in the dll
#define getMapINLINE	getMap
#define getGridHeightINLINE	getGridHeight
#define getGridWidthINLINE	getGridWidth
#define isWrapYINLINE	isWrapY
#define isWrapXINLINE	isWrapX
#define plotINLINE	plot
#define getX_INLINE	getX
#define getY_INLINE	getY

#endif
#endif

class CvPlot;
class CvCity;
class CvUnit;
class CvString;
class CvRandom;
class FAStarNode;
class FAStar;
class CvInfoBase;


#ifndef SQR
#define SQR(x) ( (x)*(x))
#endif

#undef max
#undef min

//sign function taken from FirePlace - JW
template<class T> __forceinline T getSign( T x ) { return (( x < 0 ) ? T(-1) : x > 0 ? T(1) : T(0)); };

inline int range(int iNum, int iLow, int iHigh)
{
	FAssertMsg(iHigh >= iLow, "High should be higher than low");

	if (iNum < iLow)
	{
		return iLow;
	}
	else if (iNum > iHigh)
	{
		return iHigh;
	}
	else
	{
		return iNum;
	}
}

inline float range(float fNum, float fLow, float fHigh)
{
	FAssertMsg(fHigh >= fLow, "High should be higher than low");

	if (fNum < fLow)
	{
		return fLow;
	}
	else if (fNum > fHigh)
	{
		return fHigh;
	}
	else
	{
		return fNum;
	}
}

inline int coordDistance(int iFrom, int iTo, int iRange, bool bWrap)
{
	if (bWrap && (abs(iFrom - iTo) > (iRange / 2)))
	{
		return (iRange - abs(iFrom - iTo));
	}

	return abs(iFrom - iTo);
}

inline int wrapCoordDifference(int iDiff, int iRange, bool bWrap)
{
	if (bWrap)
	{
		if (iDiff > (iRange / 2))
		{
			return (iDiff - iRange);
		}
		else if (iDiff < -(iRange / 2))
		{
			return (iDiff + iRange);
		}
	}

	return iDiff;
}

inline int xDistance(int iFromX, int iToX)
{
	return coordDistance(iFromX, iToX, GC.getMapINLINE().getGridWidthINLINE(), GC.getMapINLINE().isWrapXINLINE());
}

inline int yDistance(int iFromY, int iToY)
{
	return coordDistance(iFromY, iToY, GC.getMapINLINE().getGridHeightINLINE(), GC.getMapINLINE().isWrapYINLINE());
}

inline int dxWrap(int iDX)																													// Exposed to Python
{
	return wrapCoordDifference(iDX, GC.getMapINLINE().getGridWidthINLINE(), GC.getMapINLINE().isWrapXINLINE());
}

inline int dyWrap(int iDY)																													// Exposed to Python
{
	return wrapCoordDifference(iDY, GC.getMapINLINE().getGridHeightINLINE(), GC.getMapINLINE().isWrapYINLINE());
}

// 4 | 4 | 3 | 3 | 3 | 4 | 4
// -------------------------
// 4 | 3 | 2 | 2 | 2 | 3 | 4
// -------------------------
// 3 | 2 | 1 | 1 | 1 | 2 | 3
// -------------------------
// 3 | 2 | 1 | 0 | 1 | 2 | 3
// -------------------------
// 3 | 2 | 1 | 1 | 1 | 2 | 3
// -------------------------
// 4 | 3 | 2 | 2 | 2 | 3 | 4
// -------------------------
// 4 | 4 | 3 | 3 | 3 | 4 | 4
//
// Returns the distance between plots according to the pattern above...
inline int plotDistance(int iX1, int iY1, int iX2, int iY2)													// Exposed to Python
{
	int iDX;
	int iDY;

	iDX = xDistance(iX1, iX2);
	iDY = yDistance(iY1, iY2);

	return (std::max(iDX, iDY) + (std::min(iDX, iDY) / 2));
}

// K-Mod, plot-to-plot alias for convenience:
inline int plotDistance(const CvPlot* plot1, const CvPlot* plot2)
{
	return plotDistance(plot1->getX_INLINE(), plot1->getY_INLINE(), plot2->getX_INLINE(), plot2->getY_INLINE());
}
// K-Mod end

// 3 | 3 | 3 | 3 | 3 | 3 | 3
// -------------------------
// 3 | 2 | 2 | 2 | 2 | 2 | 3
// -------------------------
// 3 | 2 | 1 | 1 | 1 | 2 | 3
// -------------------------
// 3 | 2 | 1 | 0 | 1 | 2 | 3
// -------------------------
// 3 | 2 | 1 | 1 | 1 | 2 | 3
// -------------------------
// 3 | 2 | 2 | 2 | 2 | 2 | 3
// -------------------------
// 3 | 3 | 3 | 3 | 3 | 3 | 3
//
// Returns the distance between plots according to the pattern above...
inline int stepDistance(int iX1, int iY1, int iX2, int iY2)													// Exposed to Python
{
	return std::max(xDistance(iX1, iX2), yDistance(iY1, iY2));
}

// K-Mod, plot-to-plot alias for convenience:
inline int stepDistance(const CvPlot* plot1, const CvPlot* plot2)
{
	return stepDistance(plot1->getX_INLINE(), plot1->getY_INLINE(), plot2->getX_INLINE(), plot2->getY_INLINE());
}
// K-Mod end

inline CvPlot* plotDirection(int iX, int iY, DirectionTypes eDirection)							// Exposed to Python
{
	if(eDirection == NO_DIRECTION)
	{
		return GC.getMapINLINE().plotINLINE(iX, iY);
	}
	else
	{
		return GC.getMapINLINE().plotINLINE((iX + GC.getPlotDirectionX()[eDirection]), (iY + GC.getPlotDirectionY()[eDirection]));
	}
}

inline CvPlot* plotCardinalDirection(int iX, int iY, CardinalDirectionTypes eCardinalDirection)	// Exposed to Python
{
	return GC.getMapINLINE().plotINLINE((iX + GC.getPlotCardinalDirectionX()[eCardinalDirection]), (iY + GC.getPlotCardinalDirectionY()[eCardinalDirection]));
}

inline CvPlot* plotXY(int iX, int iY, int iDX, int iDY)																// Exposed to Python
{
	return GC.getMapINLINE().plotINLINE((iX + iDX), (iY + iDY));
}

inline CvPlot* plotXY(const CvPlot* pPlot, int iDX, int iDY) { return plotXY(pPlot->getX_INLINE(), pPlot->getY_INLINE(), iDX, iDY); } // K-Mod

inline DirectionTypes directionXY(int iDX, int iDY)																		// Exposed to Python
{
	if ((abs(iDX) > DIRECTION_RADIUS) || (abs(iDY) > DIRECTION_RADIUS))
	{
		return NO_DIRECTION;
	}
	else
	{
		return GC.getXYDirection((iDX + DIRECTION_RADIUS), (iDY + DIRECTION_RADIUS));
	}
}

inline DirectionTypes directionXY(const CvPlot* pFromPlot, const CvPlot* pToPlot)			// Exposed to Python
{
	return directionXY(dxWrap(pToPlot->getX_INLINE() - pFromPlot->getX_INLINE()), dyWrap(pToPlot->getY_INLINE() - pFromPlot->getY_INLINE()));
}

CvPlot* plotCity(int iX, int iY, int iIndex);																			// Exposed to Python
int plotCityXY(int iDX, int iDY);																									// Exposed to Python
int plotCityXY(const CvCity* pCity, const CvPlot* pPlot);													// Exposed to Python

CardinalDirectionTypes getOppositeCardinalDirection(CardinalDirectionTypes eDir);	// Exposed to Python 
DirectionTypes cardinalDirectionToDirection(CardinalDirectionTypes eCard);				// Exposed to Python
DllExport bool isCardinalDirection(DirectionTypes eDirection);															// Exposed to Python
DirectionTypes estimateDirection(int iDX, int iDY);																// Exposed to Python
DllExport DirectionTypes estimateDirection(const CvPlot* pFromPlot, const CvPlot* pToPlot);
DllExport float directionAngle(DirectionTypes eDirection);

bool atWar(TeamTypes eTeamA, TeamTypes eTeamB);												// Exposed to Python
bool isPotentialEnemy(TeamTypes eOurTeam, TeamTypes eTheirTeam);			// Exposed to Python

DllExport CvCity* getCity(IDInfo city);	// Exposed to Python
DllExport CvUnit* getUnit(IDInfo unit);	// Exposed to Python

inline bool isCycleGroup(const CvSelectionGroup* pGroup) { return pGroup->getNumUnits() > 0 && !pGroup->isWaiting() && !pGroup->isAutomated(); } // K-Mod
bool isBeforeUnitCycle(const CvUnit* pFirstUnit, const CvUnit* pSecondUnit);
bool isBeforeGroupOnPlot(const CvSelectionGroup* pFirstGroup, const CvSelectionGroup* pSecondGroup); // K-Mod
int groupCycleDistance(const CvSelectionGroup* pFirstGroup, const CvSelectionGroup* pSecondGroup); // K-Mod
bool isPromotionValid(PromotionTypes ePromotion, UnitTypes eUnit, bool bLeader);	// Exposed to Python

int getPopulationAsset(int iPopulation);								// Exposed to Python
int getLandPlotsAsset(int iLandPlots);									// Exposed to Python
int getPopulationPower(int iPopulation);								// Exposed to Python
int getPopulationScore(int iPopulation);								// Exposed to Python
int getLandPlotsScore(int iLandPlots);									// Exposed to Python
int getTechScore(TechTypes eTech);											// Exposed to Python
int getWonderScore(BuildingClassTypes eWonderClass);		// Exposed to Python

//ImprovementTypes finalImprovementUpgrade(ImprovementTypes eImprovement, int iCount = 0);		// Exposed to Python
ImprovementTypes finalImprovementUpgrade(ImprovementTypes eImprovement); // Exposed to Python, K-Mod. (I've removed iCount here, and in the python defs. It's a meaningless parameter.)

int getWorldSizeMaxConscript(CivicTypes eCivic);								// Exposed to Python

bool isReligionTech(TechTypes eTech);														// Exposed to Python

bool isTechRequiredForUnit(TechTypes eTech, UnitTypes eUnit);							// Exposed to Python
bool isTechRequiredForBuilding(TechTypes eTech, BuildingTypes eBuilding);	// Exposed to Python
bool isTechRequiredForProject(TechTypes eTech, ProjectTypes eProject);		// Exposed to Python

// MOD - START - Advanced Building Prerequisites (Civic)
bool isCivicRequiredForBuilding(CivicTypes eCivic, BuildingTypes eBuilding);	// Exposed to Python
// MOD - END - Advanced Building Prerequisites (Civic)

// MOD - START - Relation Caching
bool isTraitRelatedToImprovement(TraitTypes eTrait, ImprovementTypes eImprovement);
bool isTraitRelatedToSpecialist(TraitTypes eTrait, SpecialistTypes eSpecialist);

bool isTechRelatedToBonus(TechTypes eTech, BonusTypes eBonus);
bool isTechRelatedToBuild(TechTypes eTech, BuildTypes eBuild);
bool isTechRelatedToImprovement(TechTypes eTech, ImprovementTypes eImprovement);
bool isTechRelatedToUnit(TechTypes eTech, UnitTypes eUnit);
bool isTechRelatedToBuilding(TechTypes eTech, BuildingTypes eBuilding);

bool isReligionRelatedToUnit(ReligionTypes eReligion, UnitTypes eUnit);
bool isReligionRelatedToBuilding(ReligionTypes eReligion, BuildingTypes eBuilding);

bool isCivicRelatedToFeature(CivicTypes eCivic, FeatureTypes eFeature);
bool isCivicRelatedToImprovement(CivicTypes eCivic, ImprovementTypes eImprovement);
bool isCivicRelatedToSpecialist(CivicTypes eCivic, SpecialistTypes eSpecialist);
bool isCivicRelatedToUnit(CivicTypes eCivic, UnitTypes eUnit);
bool isCivicRelatedToBuilding(CivicTypes eCivic, BuildingTypes eBuilding);

bool isBonusRelatedToBuild(BonusTypes eBonus, BuildTypes eBuild);
bool isBonusRelatedToUnit(BonusTypes eBonus, UnitTypes eUnit);
bool isBonusRelatedToBuilding(BonusTypes eBonus, BuildingTypes eBuilding);

bool isImprovementRelatedToBuilding(ImprovementTypes eImprovement, BuildingTypes eBuilding);

bool isSpecialistRelatedToBuilding(SpecialistTypes eSpecialist, BuildingTypes eBuilding);

bool isBuildingRelatedToUnitCombat(BuildingTypes eBuilding, UnitCombatTypes eUnitCombat);
bool isBuildingRelatedToUnit(BuildingTypes eBuilding, UnitTypes eUnit);
bool isBuildingRelatedToBuilding(BuildingTypes eBuildingA, BuildingTypes eBuildingB);

bool isUnitRelatedToDomain(UnitTypes eUnit, DomainTypes eDomain);
bool isUnitRelatedToTerrain(UnitTypes eUnit, TerrainTypes eTerrain);
bool isUnitRelatedToFeature(UnitTypes eUnit, FeatureTypes eFeature);
bool isUnitRelatedToBuild(UnitTypes eUnit, BuildTypes eBuild);
bool isUnitRelatedToUnitCombat(UnitTypes eUnit, UnitCombatTypes eUnitCombat);
bool isUnitRelatedToUnit(UnitTypes eUnitA, UnitTypes eUnitB);
bool isUnitRelatedToPromotion(UnitTypes eUnit, PromotionTypes ePromotion);

bool isPromotionRelatedToDomain(PromotionTypes ePromotionA, DomainTypes eDomain);
bool isPromotionRelatedToTerrain(PromotionTypes ePromotion, TerrainTypes eTerrain);
bool isPromotionRelatedToFeature(PromotionTypes ePromotion, FeatureTypes eFeature);
bool isPromotionRelatedToUnitCombat(PromotionTypes ePromotion, UnitCombatTypes eUnitCombat);
bool isPromotionRelatedToPromotion(PromotionTypes ePromotionA, PromotionTypes ePromotionB);

bool isEventRelatedToEvent(EventTypes eEventA, EventTypes eEventB);
bool isEventRelatedToUnitCombat(EventTypes eEvent, UnitCombatTypes eUnitCombat);
bool isEventRelatedToUnit(EventTypes eEvent, UnitTypes eUnit);
bool isEventRelatedToBuilding(EventTypes eEvent, BuildingTypes eBuilding);
// MOD - END - Relation Caching

bool isWorldUnitClass(UnitClassTypes eUnitClass);											// Exposed to Python
bool isTeamUnitClass(UnitClassTypes eUnitClass);											// Exposed to Python
bool isNationalUnitClass(UnitClassTypes eUnitClass);									// Exposed to Python
bool isLimitedUnitClass(UnitClassTypes eUnitClass);										// Exposed to Python

bool isWorldWonderClass(BuildingClassTypes eBuildingClass);						// Exposed to Python
bool isTeamWonderClass(BuildingClassTypes eBuildingClass);						// Exposed to Python
bool isNationalWonderClass(BuildingClassTypes eBuildingClass);				// Exposed to Python
bool isLimitedWonderClass(BuildingClassTypes eBuildingClass);					// Exposed to Python
int limitedWonderClassLimit(BuildingClassTypes eBuildingClass);

bool isWorldProject(ProjectTypes eProject);														// Exposed to Python
bool isTeamProject(ProjectTypes eProject);														// Exposed to Python
bool isLimitedProject(ProjectTypes eProject);													// Exposed to Python

__int64 getBinomialCoefficient(int iN, int iK);
int getCombatOdds(const CvUnit* pAttacker, const CvUnit* pDefender); // Exposed to Python
int estimateCollateralWeight(const CvPlot* pPlot, TeamTypes eAttackTeam, TeamTypes eDefenceTeam = NO_TEAM); // K-Mod

int getEspionageModifier(TeamTypes eOurTeam, TeamTypes eTargetTeam);							// Exposed to Python

DllExport void setTradeItem(TradeData* pItem, TradeableItems eItemType = TRADE_ITEM_NONE, int iData = 0);

bool isPlotEventTrigger(EventTriggerTypes eTrigger);

TechTypes getDiscoveryTech(UnitTypes eUnit, PlayerTypes ePlayer);

void setListHelp(wchar* szBuffer, const wchar* szStart, const wchar* szItem, const wchar* szSeparator, bool bFirst);
void setListHelp(CvWString& szBuffer, const wchar* szStart, const wchar* szItem, const wchar* szSeparator, bool bFirst);
void setListHelp(CvWStringBuffer& szBuffer, const wchar* szStart, const wchar* szItem, const wchar* szSeparator, bool bFirst);

// PlotUnitFunc's...
bool PUF_isGroupHead( const CvUnit* pUnit, int iData1 = -1, int iData2 = -1);
bool PUF_isPlayer( const CvUnit* pUnit, int iData1, int iData2 = -1);
bool PUF_isTeam( const CvUnit* pUnit, int iData1, int iData2 = -1);
bool PUF_isCombatTeam(const CvUnit* pUnit, int iData1, int iData2);
bool PUF_isOtherPlayer( const CvUnit* pUnit, int iData1, int iData2 = -1);
bool PUF_isOtherTeam( const CvUnit* pUnit, int iData1, int iData2 = -1);
bool PUF_isEnemy( const CvUnit* pUnit, int iData1, int iData2 = -1);
bool PUF_isVisible( const CvUnit* pUnit, int iData1, int iData2 = -1);
bool PUF_isVisibleDebug( const CvUnit* pUnit, int iData1, int iData2 = -1);
bool PUF_canSiege( const CvUnit* pUnit, int iData1, int iData2 = -1);
bool PUF_isPotentialEnemy( const CvUnit* pUnit, int iData1, int iData2 = -1);
bool PUF_canDeclareWar( const CvUnit* pUnit, int iData1 = -1, int iData2 = -1);
bool PUF_canDefend( const CvUnit* pUnit, int iData1 = -1, int iData2 = -1);
bool PUF_cannotDefend( const CvUnit* pUnit, int iData1 = -1, int iData2 = -1);
bool PUF_canDefendGroupHead( const CvUnit* pUnit, int iData1 = -1, int iData2 = -1);
bool PUF_canDefendEnemy( const CvUnit* pUnit, int iData1, int iData2 = -1);
bool PUF_canDefendPotentialEnemy( const CvUnit* pUnit, int iData1, int iData2 = -1);
bool PUF_canAirAttack( const CvUnit* pUnit, int iData1 = -1, int iData2 = -1);
bool PUF_canAirDefend( const CvUnit* pUnit, int iData1 = -1, int iData2 = -1);
bool PUF_isFighting( const CvUnit* pUnit, int iData1, int iData2 = -1);
bool PUF_isAnimal( const CvUnit* pUnit, int iData1 = -1, int iData2 = -1);
bool PUF_isMilitaryHappiness( const CvUnit* pUnit, int iData1 = -1, int iData2 = -1);
bool PUF_isInvestigate( const CvUnit* pUnit, int iData1 = -1, int iData2 = -1);
bool PUF_isCounterSpy( const CvUnit* pUnit, int iData1 = -1, int iData2 = -1);
bool PUF_isSpy( const CvUnit* pUnit, int iData1 = -1, int iData2 = -1);
bool PUF_isUnitType( const CvUnit* pUnit, int iData1, int iData2 = -1);
bool PUF_isDomainType( const CvUnit* pUnit, int iData1, int iData2 = -1);
bool PUF_isUnitAIType( const CvUnit* pUnit, int iData1, int iData2 = -1);
bool PUF_isCityAIType( const CvUnit* pUnit, int iData1, int iData2 = -1);
bool PUF_isNotCityAIType( const CvUnit* pUnit, int iData1, int iData2 = -1);
bool PUF_isSelected( const CvUnit* pUnit, int iData1 = -1, int iData2 = -1);
bool PUF_makeInfoBarDirty(CvUnit* pUnit, int iData1 = -1, int iData2 = -1);
bool PUF_isNoMission(const CvUnit* pUnit, int iData1 = -1, int iData2 = -1);
bool PUF_isFiniteRange(const CvUnit* pUnit, int iData1 = -1, int iData2 = -1);
// bbai
bool PUF_isAvailableUnitAITypeGroupie(const CvUnit* pUnit, int iData1, int iData2);
bool PUF_isUnitAITypeGroupie(const CvUnit* pUnit, int iData1, int iData2);
bool PUF_isFiniteRangeAndNotJustProduced(const CvUnit* pUnit, int iData1, int iData2);
// bbai end
bool PUF_isMissionAIType(const CvUnit* pUnit, int iData1, int iData2); // K-Mod
bool PUF_isAirIntercept(const CvUnit* pUnit, int iData1, int iData2); // K-Mod

// FAStarFunc...
int potentialIrrigation(FAStarNode* parent, FAStarNode* node, int data, const void* pointer, FAStar* finder);
int checkFreshWater(FAStarNode* parent, FAStarNode* node, int data, const void* pointer, FAStar* finder);
int changeIrrigated(FAStarNode* parent, FAStarNode* node, int data, const void* pointer, FAStar* finder);
int pathDestValid(int iToX, int iToY, const void* pointer, FAStar* finder);
int pathHeuristic(int iFromX, int iFromY, int iToX, int iToY);
int pathCost(FAStarNode* parent, FAStarNode* node, int data, const void* pointer, FAStar* finder);
int pathValid_join(FAStarNode* parent, FAStarNode* node, CvSelectionGroup* pSelectionGroup, int iFlags); // K-Mod
int pathValid_source(FAStarNode* parent, CvSelectionGroup* pSelectionGroup, int iFlags); // K-Mod
int pathValid(FAStarNode* parent, FAStarNode* node, int data, const void* pointer, FAStar* finder);
int pathAdd(FAStarNode* parent, FAStarNode* node, int data, const void* pointer, FAStar* finder);
int stepDestValid(int iToX, int iToY, const void* pointer, FAStar* finder);
int stepHeuristic(int iFromX, int iFromY, int iToX, int iToY);
int stepValid(FAStarNode* parent, FAStarNode* node, int data, const void* pointer, FAStar* finder);
int stepCost(FAStarNode* parent, FAStarNode* node, int data, const void* pointer, FAStar* finder);
int stepAdd(FAStarNode* parent, FAStarNode* node, int data, const void* pointer, FAStar* finder);

/********************************************************************************/
/* 	BETTER_BTS_AI_MOD					11/30/08				jdog5000	*/
/* 																			*/
/* 																			*/
/********************************************************************************/
int teamStepValid(FAStarNode* parent, FAStarNode* node, int data, const void* pointer, FAStar* finder);
/********************************************************************************/
/* 	BETTER_BTS_AI_MOD						END								*/
/********************************************************************************/
int routeValid(FAStarNode* parent, FAStarNode* node, int data, const void* pointer, FAStar* finder);
int borderValid(FAStarNode* parent, FAStarNode* node, int data, const void* pointer, FAStar* finder);
int areaValid(FAStarNode* parent, FAStarNode* node, int data, const void* pointer, FAStar* finder);
int joinArea(FAStarNode* parent, FAStarNode* node, int data, const void* pointer, FAStar* finder);
int plotGroupValid(FAStarNode* parent, FAStarNode* node, int data, const void* pointer, FAStar* finder);
int countPlotGroup(FAStarNode* parent, FAStarNode* node, int data, const void* pointer, FAStar* finder);

int baseYieldToSymbol(int iNumYieldTypes, int iYieldStack);

bool isPickableName(const TCHAR* szName);

DllExport int* shuffle(int iNum, CvRandom& rand);
void shuffleArray(int* piShuffle, int iNum, CvRandom& rand);

int getTurnMonthForGame(int iGameTurn, int iStartYear, CalendarTypes eCalendar, GameSpeedTypes eSpeed);
int getTurnYearForGame(int iGameTurn, int iStartYear, CalendarTypes eCalendar, GameSpeedTypes eSpeed);

void getDirectionTypeString(CvWString& szString, DirectionTypes eDirectionType);
void getCardinalDirectionTypeString(CvWString& szString, CardinalDirectionTypes eDirectionType);
void getActivityTypeString(CvWString& szString, ActivityTypes eActivityType);
void getMissionTypeString(CvWString& szString, MissionTypes eMissionType);
void getMissionAIString(CvWString& szString, MissionAITypes eMissionAI);
void getUnitAIString(CvWString& szString, UnitAITypes eUnitAI);

// Lead From Behind by UncutDragon
int LFBgetCombatOdds(int iAttackerLowFS, int iAttackerHighFS, int iDefenderLowFS, int iDefenderHighFS, int iNeededRoundsAttacker, int iNeededRoundsDefender, int iAttackerOdds);

// MOD - START - Advanced Automations
/************************************************************************************************/
/* Afforess	                  Start		 06/21/10                                               */
/*                                                                                              */
/*                                                                                              */
/************************************************************************************************/
DirectionTypes getOppositeDirection(DirectionTypes eDirection);
bool isAdjacentDirection(DirectionTypes eFacingDirection, DirectionTypes eOtherDirection);
/************************************************************************************************/
/* Afforess	                         END                                                        */
/************************************************************************************************/
// MOD - END - Advanced Automations

// MOD - START - Widget Data Packing
inline int packByteID(int iData1)
{
	FASSERT_BOUNDS(-1, MAX_UNSIGNED_CHAR, iData1, "packByteID");
	return ~(((iData1 >= 0 ? iData1 + 1 : 0) & MAX_UNSIGNED_CHAR));
}

inline int packByteID(int iData1, int iData2)
{
	FASSERT_BOUNDS(-1, MAX_UNSIGNED_CHAR, iData1, "packByteID");
	FASSERT_BOUNDS(-1, MAX_UNSIGNED_CHAR, iData2, "packByteID");
	return ~(((iData1 >= 0 ? iData1 + 1 : 0) & MAX_UNSIGNED_CHAR) | (((iData2 >= 0 ? iData2 + 1 : 0) & MAX_UNSIGNED_CHAR) << 8));
}

inline int packByteID(int iData1, int iData2, int iData3)
{
	FASSERT_BOUNDS(-1, MAX_UNSIGNED_CHAR, iData1, "packByteID");
	FASSERT_BOUNDS(-1, MAX_UNSIGNED_CHAR, iData2, "packByteID");
	FASSERT_BOUNDS(-1, MAX_UNSIGNED_CHAR, iData3, "packByteID");
	return ~(((iData1 >= 0 ? iData1 + 1 : 0) & MAX_UNSIGNED_CHAR) | (((iData2 >= 0 ? iData2 + 1 : 0) & MAX_UNSIGNED_CHAR) << 8) | (((iData3 >= 0 ? iData3 + 1 : 0) & MAX_UNSIGNED_CHAR) << 16));
}

inline int packByteID(int iData1, int iData2, int iData3, int iData4)
{
	FASSERT_BOUNDS(-1, MAX_UNSIGNED_CHAR, iData1, "packByteID");
	FASSERT_BOUNDS(-1, MAX_UNSIGNED_CHAR, iData2, "packByteID");
	FASSERT_BOUNDS(-1, MAX_UNSIGNED_CHAR, iData3, "packByteID");
	FASSERT_BOUNDS(-1, MAX_UNSIGNED_CHAR, iData4, "packByteID");
	return ~(((iData1 >= 0 ? iData1 + 1 : 0) & MAX_UNSIGNED_CHAR) | (((iData2 >= 0 ? iData2 + 1 : 0) & MAX_UNSIGNED_CHAR) << 8) | (((iData3 >= 0 ? iData3 + 1 : 0) & MAX_UNSIGNED_CHAR) << 16) | (((iData4 >= 0 ? iData4 + 1 : 0) & MAX_UNSIGNED_CHAR) << 24));
}

inline int packWordID(int iData1)
{
	FASSERT_BOUNDS(-1, MAX_UNSIGNED_SHORT, iData1, "packWordID");
	return ~(((iData1 >= 0 ? iData1 + 1 : 0) & MAX_UNSIGNED_SHORT));
}

inline int packWordID(int iData1, int iData2)
{
	FASSERT_BOUNDS(-1, MAX_UNSIGNED_SHORT, iData1, "packWordID");
	FASSERT_BOUNDS(-1, MAX_UNSIGNED_SHORT, iData2, "packWordID");
	return ~(((iData1 >= 0 ? iData1 + 1 : 0) & MAX_UNSIGNED_SHORT) | (((iData2 >= 0 ? iData2 + 1 : 0) & MAX_UNSIGNED_SHORT) << 16));
}

inline int getPackedByteID1(int iPackedData)
{
	return ((~iPackedData) & MAX_UNSIGNED_CHAR) - 1;
}

inline int getPackedByteID2(int iPackedData)
{
	return (((~iPackedData) >> 8) & MAX_UNSIGNED_CHAR) - 1;
}

inline int getPackedByteID3(int iPackedData)
{
	return (((~iPackedData) >> 16) & MAX_UNSIGNED_CHAR) - 1;
}

inline int getPackedByteID4(int iPackedData)
{
	return (((~iPackedData) >> 24) & MAX_UNSIGNED_CHAR) - 1;
}

inline int getPackedWordID1(int iPackedData)
{
	return ((~iPackedData) & MAX_UNSIGNED_SHORT) - 1;
}

inline int getPackedWordID2(int iPackedData)
{
	return (((~iPackedData) >> 16) & MAX_UNSIGNED_SHORT) - 1;
}
// MOD - END - Widget Data Packing

// MOD - START - Improved Civilopedia
void doPediaLink(std::wstring szLink); // Exposed to Python
void doPediaAction(CivilopediaSectionTypes eSection);
void doPediaAction(CivilopediaViewTypes eView, int iViewData1 = -1, int iViewData2 = -1);
void doPediaAction(CivilopediaPageTypes ePage, int iPageData1 = -1, int iPageData2 = -1);
// MOD - END - Improved Civilopedia

// MOD - START - Congestion
void getRelevantCongestionTypes(std::vector<CongestionTypes>& aRelevantCongestionTypes, DomainTypes eDomain, bool bInsideCity);
CongestionTypes getCongestionRelativeToCurrent(const CvPlot* pPlot, TeamTypes eTeam, DomainTypes eDomain, int iOffset);
// MOD - END - Congestion

#endif
