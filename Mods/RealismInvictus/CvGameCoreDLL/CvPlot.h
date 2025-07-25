#pragma once

// CvPlot.h

#ifndef CIV4_PLOT_H
#define CIV4_PLOT_H

#include "CvStructs.h"
#include "LinkedList.h"
#include <bitset>

#if not defined(__GNUC__) //PORT NEW
#pragma warning( disable: 4251 )		// needs to have dll-interface to be used by clients of class
#endif

class CvArea;
class CvMap;
class CvPlotBuilder;
class CvRoute;
class CvRiver;
class CvCity;
class CvPlotGroup;
class CvFeature;
class CvUnit;
class CvSymbol;
class CvFlagEntity;

typedef bool (*ConstPlotUnitFunc)( const CvUnit* pUnit, int iData1, int iData2);
typedef bool (*PlotUnitFunc)(CvUnit* pUnit, int iData1, int iData2);

class CvPlot
{

public:
	CvPlot();
	virtual ~CvPlot();

	void init(int iX, int iY);
	void uninit();
	void reset(int iX = 0, int iY = 0, bool bConstructorCall=false);
	void setupGraphical();
	void updateGraphicEra();

	void erase();																																								// Exposed to Python
	// MOD - START - Graphical Paging (45deg)
	void destroyGraphics();
	// MOD - END - Graphical Paging (45deg)	
	DllExport float getPointX() const;														
	DllExport float getPointY() const;														
	DllExport NiPoint3 getPoint() const;																																	// Exposed to Python

	float getSymbolSize() const;
	DllExport float getSymbolOffsetX(int iID) const;
	DllExport float getSymbolOffsetY(int iID) const;

	TeamTypes getTeam() const;																																	// Exposed to Python

	void doTurn();

	void doImprovement();

	void updateCulture(bool bBumpUnits, bool bUpdatePlotGroups);

	void updateFog();
	void updateVisibility();

	void updateSymbolDisplay();
	void updateSymbolVisibility();
	void updateSymbols();

	void updateMinimapColor();

	void updateCenterUnit();

	void verifyUnitValidPlot();
	void forceBumpUnits(); // K-Mod

	//void nukeExplosion(int iRange, CvUnit* pNukeUnit = NULL);																							// Exposed to Python
	void nukeExplosion(int iRange, CvUnit* pNukeUnit = NULL, bool bBomb = true); //  K-Mod added bBomb, Exposed to Python

	bool isConnectedTo( const CvCity* pCity) const;																												// Exposed to Python
	bool isConnectedToCapital(PlayerTypes ePlayer = NO_PLAYER) const;																			// Exposed to Python
	int getPlotGroupConnectedBonus(PlayerTypes ePlayer, BonusTypes eBonus) const;													// Exposed to Python
	bool isPlotGroupConnectedBonus(PlayerTypes ePlayer, BonusTypes eBonus) const;								// Exposed to Python
	bool isAdjacentPlotGroupConnectedBonus(PlayerTypes ePlayer, BonusTypes eBonus) const;				// Exposed to Python
	void updatePlotGroupBonus(bool bAdd);

	// MOD - START - PlotGroup Bonus Efficiency
	void updateBonusCityTradeForTech(TeamTypes eTeam, TechTypes eTech, bool bHasTech);
	void updateForceRevealedBonus(TeamTypes eTeam, BonusTypes eBonus, bool bConnectionChange, bool bConnected);
	// MOD - END - PlotGroup Bonus Efficiency

	// MOD - START - PlotGroup Bonus Efficiency
	void changeNumPlotGroupBonuses(BonusTypes eIndex, int iChange);
	void changeNumPlotGroupBonuses(std::vector<CvBonusAmountChange>& aBonusChanges);
	// MOD - END - PlotGroup Bonus Efficiency

	// MOD - START - Bonus Converters
	void changeNumPlotGroupBonusConverterConsumedBonuses(BuildingTypes eBuilding, BonusTypes eBonus, int iChange);
	// MOD - END - Bonus Converters

	// MOD - START - Fort indexing
    //void CvPlot::updateFortIndex();
    void updateFortIndex();
    // MOD - END - Fort indexing

	bool isAdjacentToArea(int iAreaID) const;
	bool isAdjacentToArea(const CvArea* pArea) const;																						// Exposed to Python
	bool shareAdjacentArea( const CvPlot* pPlot) const;																					// Exposed to Python
	bool isAdjacentToLand() const;																															// Exposed to Python 
	bool isCoastalLand(int iMinWaterSize = -1) const;																																	// Exposed to Python

	bool isVisibleWorked() const;
	bool isWithinTeamCityRadius(TeamTypes eTeam, PlayerTypes eIgnorePlayer = NO_PLAYER) const;	// Exposed to Python

	DllExport bool isLake() const;																															// Exposed to Python
	bool isFreshWater() const;																												// Exposed to Python
	bool isPotentialIrrigation() const;																													// Exposed to Python
	bool canHavePotentialIrrigation() const;																										// Exposed to Python
	DllExport bool isIrrigationAvailable(bool bIgnoreSelf = false) const;												// Exposed to Python

	bool isRiverMask() const;
	DllExport bool isRiverCrossingFlowClockwise(DirectionTypes eDirection) const;
	bool isRiverSide() const;																																		// Exposed to Python
	bool isRiver() const;																																				// Exposed to Python
	bool isRiverConnection(DirectionTypes eDirection) const;																		// Exposed to Python

	CvPlot* getNearestLandPlotInternal(int iDistance) const;
	int getNearestLandArea() const;																															// Exposed to Python
	CvPlot* getNearestLandPlot() const;																													// Exposed to Python

	int seeFromLevel(TeamTypes eTeam) const;																										// Exposed to Python  
	int seeThroughLevel() const;																																// Exposed to Python
	void changeAdjacentSight(TeamTypes eTeam, int iRange, bool bIncrement, CvUnit* pUnit, bool bUpdatePlotGroups);
	bool canSeePlot(CvPlot *plot, TeamTypes eTeam, int iRange, DirectionTypes eFacingDirection) const;
	bool canSeeDisplacementPlot(TeamTypes eTeam, int dx, int dy, int originalDX, int originalDY, bool firstPlot, bool outerRing) const;
	bool shouldProcessDisplacementPlot(int dx, int dy, int range, DirectionTypes eFacingDirection) const;
	void updateSight(bool bIncrement, bool bUpdatePlotGroups);
	void updateSeeFromSight(bool bIncrement, bool bUpdatePlotGroups);

	bool canHaveBonus(BonusTypes eBonus, bool bIgnoreLatitude = false) const;																						// Exposed to Python
	bool canHaveImprovement(ImprovementTypes eImprovement, TeamTypes eTeam = NO_TEAM, bool bPotential = false) const;		// Exposed to Python

	bool canBuild(BuildTypes eBuild, PlayerTypes ePlayer = NO_PLAYER, bool bTestVisible = false) const;														// Exposed to Python
	int getBuildTime(BuildTypes eBuild) const;																																										// Exposed to Python
	int getBuildTurnsLeft(BuildTypes eBuild, int iNowExtra, int iThenExtra) const;																			// Exposed to Python
	int getFeatureProduction(BuildTypes eBuild, TeamTypes eTeam, CvCity** ppCity) const;																// Exposed to Python

	DllExport CvUnit* getBestDefender(PlayerTypes eOwner, PlayerTypes eAttackingPlayer = NO_PLAYER, const CvUnit* pAttacker = NULL, bool bTestAtWar = false, bool bTestPotentialEnemy = false, bool bTestCanMove = false) const; // Exposed to Python
	// MOD - START - Protect Valuable Units / Lead From Behind
	// MOD - START - Ranged Strike AI
	CvUnit* getBestDefender(PlayerTypes eOwner, PlayerTypes eAttackingPlayer, const CvUnit* pAttacker, bool bTestAtWar, bool bTestPotentialEnemy, bool bTestCanMove, bool bRanged) const;
	// MOD - END - Ranged Strike AI
	// MOD - END - Protect Valuable Units / Lead From Behind
	//int AI_sumStrength(PlayerTypes eOwner, PlayerTypes eAttackingPlayer = NO_PLAYER, DomainTypes eDomainType = NO_DOMAIN, bool bDefensiveBonuses = true, bool bTestAtWar = false, bool bTestPotentialEnemy = false) const; // disabled by K-Mod
	CvUnit* getSelectedUnit() const;																																// Exposed to Python
	int getUnitPower(PlayerTypes eOwner = NO_PLAYER) const;																					// Exposed to Python				

	int defenseModifier(TeamTypes eDefender, bool bIgnoreBuilding, bool bHelp = false) const;									// Exposed to Python				
	int movementCost(const CvUnit* pUnit, const CvPlot* pFromPlot) const;														// Exposed to Python				

	int getExtraMovePathCost() const;																																// Exposed to Python
	void changeExtraMovePathCost(int iChange);																																// Exposed to Python

	bool isAdjacentOwned() const;																																		// Exposed to Python
	bool isAdjacentPlayer(PlayerTypes ePlayer, bool bLandOnly = false) const;												// Exposed to Python
	bool isAdjacentTeam(TeamTypes eTeam, bool bLandOnly = false) const;															// Exposed to Python
	bool isWithinCultureRange(PlayerTypes ePlayer) const;																						// Exposed to Python
	int getNumCultureRangeCities(PlayerTypes ePlayer) const;																				// Exposed to Python
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      11/30/08                                jdog5000      */
/*                                                                                              */
/* General AI                                                                                   */
/************************************************************************************************/
	bool isHasPathToEnemyCity( TeamTypes eAttackerTeam, bool bIgnoreBarb = true );
	bool isHasPathToPlayerCity( TeamTypes eMoveTeam, PlayerTypes eOtherPlayer = NO_PLAYER );
	int calculatePathDistanceToPlot( TeamTypes eTeam, CvPlot* pTargetPlot );
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/

/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      08/21/09                                jdog5000      */
/*                                                                                              */
/* Efficiency                                                                                   */
/************************************************************************************************/
	// Plot danger cache (rewritten for K-Mod to fix bugs and improvement performance)
	inline int getActivePlayerSafeRangeCache() const { return m_iActivePlayerSafeRangeCache; }
	inline void setActivePlayerSafeRangeCache(int range) { m_iActivePlayerSafeRangeCache = range; }
	inline bool getBorderDangerCache(TeamTypes eTeam) const { return m_abBorderDangerCache[eTeam]; }
	inline void setBorderDangerCache(TeamTypes eTeam, bool bNewValue) { m_abBorderDangerCache[eTeam] = bNewValue; }
	void invalidateBorderDangerCache();
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/

	PlayerTypes calculateCulturalOwner() const;

	void plotAction(PlotUnitFunc func, int iData1 = -1, int iData2 = -1, PlayerTypes eOwner = NO_PLAYER, TeamTypes eTeam = NO_TEAM);
	int plotCount(ConstPlotUnitFunc funcA, int iData1A = -1, int iData2A = -1, PlayerTypes eOwner = NO_PLAYER, TeamTypes eTeam = NO_TEAM, ConstPlotUnitFunc funcB = NULL, int iData1B = -1, int iData2B = -1) const;
	CvUnit* plotCheck(ConstPlotUnitFunc funcA, int iData1A = -1, int iData2A = -1, PlayerTypes eOwner = NO_PLAYER, TeamTypes eTeam = NO_TEAM, ConstPlotUnitFunc funcB = NULL, int iData1B = -1, int iData2B = -1) const;

	bool isOwned() const;																																							// Exposed to Python
	bool isBarbarian() const;																																					// Exposed to Python
	bool isRevealedBarbarian() const;																																	// Exposed to Python

	bool isVisible(TeamTypes eTeam, bool bDebug) const;																			// Exposed to Python
	DllExport bool isActiveVisible(bool bDebug) const;																								// Exposed to Python
	bool isVisibleToCivTeam() const;																																	// Exposed to Python
	bool isVisibleToWatchingHuman() const;																														// Exposed to Python
	bool isAdjacentVisible(TeamTypes eTeam, bool bDebug) const;																				// Exposed to Python
	bool isAdjacentNonvisible(TeamTypes eTeam) const;																				// Exposed to Python

	DllExport bool isGoody(TeamTypes eTeam = NO_TEAM) const;																					// Exposed to Python
	bool isRevealedGoody(TeamTypes eTeam = NO_TEAM) const;																						// Exposed to Python
	void removeGoody();																																								// Exposed to Python

	DllExport bool isCity(bool bCheckImprovement = false, TeamTypes eForTeam = NO_TEAM) const;																																		// Exposed to Python
	bool isFriendlyCity(const CvUnit& kUnit, bool bCheckImprovement) const;																												// Exposed to Python
	bool isEnemyCity(const CvUnit& kUnit) const;																													// Exposed to Python

	bool isOccupation() const;																																				// Exposed to Python
	bool isBeingWorked() const;																															// Exposed to Python

	bool isUnit() const;																																							// Exposed to Python
	bool isInvestigate(TeamTypes eTeam) const;																												// Exposed to Python
	bool isVisibleEnemyDefender(const CvUnit* pUnit) const;																						// Exposed to Python
	CvUnit *getVisibleEnemyDefender(PlayerTypes ePlayer) const;
	int getNumDefenders(PlayerTypes ePlayer) const;																										// Exposed to Python
	int getNumVisibleEnemyDefenders(const CvUnit* pUnit) const;																				// Exposed to Python
	int getNumVisiblePotentialEnemyDefenders(const CvUnit* pUnit) const;															// Exposed to Python
	DllExport bool isVisibleEnemyUnit(PlayerTypes ePlayer) const;																			// Exposed to Python
	bool isVisiblePotentialEnemyUnit(PlayerTypes ePlayer) const; // K-Mod
	DllExport int getNumVisibleUnits(PlayerTypes ePlayer) const;
	bool isVisibleEnemyUnit(const CvUnit* pUnit) const;
	bool isVisibleOtherUnit(PlayerTypes ePlayer) const;																								// Exposed to Python
	DllExport bool isFighting() const;																																// Exposed to Python

	// MOD - START - Feature Latitude Restrictions
	//bool canHaveFeature(FeatureTypes eFeature) const;	// Exposed to Python
	bool canHaveFeature(FeatureTypes eFeature, bool bIgnoreLatitude = false) const;	// Exposed to Python
	// MOD - END - Feature Latitude Restrictions

	DllExport bool isRoute() const;																																		// Exposed to Python
	bool isValidRoute(const CvUnit* pUnit) const;																											// Exposed to Python
	bool isTradeNetworkImpassable(TeamTypes eTeam) const;																														// Exposed to Python
	bool isNetworkTerrain(TeamTypes eTeam) const;																											// Exposed to Python
	bool isBonusNetwork(TeamTypes eTeam) const;																												// Exposed to Python
	bool isTradeNetwork(TeamTypes eTeam) const;																												// Exposed to Python
	bool isTradeNetworkConnected(const CvPlot * pPlot, TeamTypes eTeam) const;												// Exposed to Python
	bool isRiverNetwork(TeamTypes eTeam) const;

	bool isValidDomainForLocation(const CvUnit& unit) const;																					// Exposed to Python
	bool isValidDomainForAction(const CvUnit& unit) const;																						// Exposed to Python
	bool isImpassable() const;																															// Exposed to Python

	DllExport int getX() const;																																				// Exposed to Python
#if (defined(__GNUC__) || defined(_USRDLL)) //PORT NEW
//#ifdef _USRDLL //PORT OLD
	inline int getX_INLINE() const
	{
		return m_iX;
	}
#endif
	DllExport int getY() const;																																				// Exposed to Python
#if (defined(__GNUC__) || defined(_USRDLL)) //PORT NEW
//#ifdef _USRDLL //PORT OLD
	inline int getY_INLINE() const
	{
		return m_iY;
	}
#endif
	bool at(int iX, int iY) const;																																		// Exposed to Python
	// MOD - START - Graphical Paging (45deg)
	static void EvictGraphicsIfNecessary();	
	void setShouldHaveFullGraphics(bool bShouldHaveFullGraphics);
	bool shouldHaveFullGraphics(void) const;	
	bool shouldHaveGraphics(void) const;
	// MOD - END - Graphical Paging (45deg)
	int getLatitude() const;																																					// Exposed to Python  
	int getFOWIndex() const;

	CvArea* area() const;																																							// Exposed to Python
/********************************************************************************/
/* 	BETTER_BTS_AI_MOD						01/02/09		jdog5000		*/
/* 																			*/
/* 	General AI																*/
/********************************************************************************/
/* original BTS code
	CvArea* waterArea() const;
*/
	CvArea* waterArea(bool bNoImpassable = false) const;
/********************************************************************************/
/* 	BETTER_BTS_AI_MOD						END								*/
/********************************************************************************/	

	// MOD - START - Multiple City Water Areas
	//CvArea* secondWaterArea(bool bNoImpassable = false) const;
	void waterAreas(CvArea* (&aWaterAreas)[MAX_CITY_WATER_AREAS], int &iNumWaterAreas, bool bNoImpassable = false, TeamTypes eRelevantTeam = NO_TEAM) const;
	// MOD - END - Multiple City Water Areas
	int getArea() const;																																		// Exposed to Python
	void setArea(int iNewValue);			

	DllExport int getFeatureVariety() const;																													// Exposed to Python

	int getOwnershipDuration() const;																																	// Exposed to Python
	bool isOwnershipScore() const;																																		// Exposed to Python
	void setOwnershipDuration(int iNewValue);																													// Exposed to Python
	void changeOwnershipDuration(int iChange);																												// Exposed to Python

	int getImprovementDuration() const;																																// Exposed to Python
	void setImprovementDuration(int iNewValue);																												// Exposed to Python
	void changeImprovementDuration(int iChange);																											// Exposed to Python

	int getUpgradeProgress() const;																													// Exposed to Python
	int getUpgradeTimeLeft(ImprovementTypes eImprovement, PlayerTypes ePlayer) const;				// Exposed to Python
	void setUpgradeProgress(int iNewValue);																														// Exposed to Python
	void changeUpgradeProgress(int iChange);																													// Exposed to Python

	int getForceUnownedTimer() const;																																	// Exposed to Python
	bool isForceUnowned() const;																																			// Exposed to Python
	void setForceUnownedTimer(int iNewValue);																													// Exposed to Python
	void changeForceUnownedTimer(int iChange);																												// Exposed to Python

	int getCityRadiusCount() const;																																		// Exposed to Python
	//int isCityRadius() const;																																					// Exposed to Python
	bool isCityRadius() const; // Exposed to Python (K-Mod changed to bool)
	void changeCityRadiusCount(int iChange);

	bool isStartingPlot() const;																																			// Exposed to Python
	void setStartingPlot(bool bNewValue);																															// Exposed to Python
	
	DllExport bool isNOfRiver() const;																																// Exposed to Python					
	void setNOfRiver(bool bNewValue, CardinalDirectionTypes eRiverDir);											// Exposed to Python					
																																																		
	DllExport bool isWOfRiver() const;																																// Exposed to Python					
	void setWOfRiver(bool bNewValue, CardinalDirectionTypes eRiverDir);											// Exposed to Python					
																																																		
	DllExport CardinalDirectionTypes getRiverNSDirection() const;																			// Exposed to Python					
	DllExport CardinalDirectionTypes getRiverWEDirection() const;																			// Exposed to Python					

	CvPlot* getInlandCorner() const;																																	// Exposed to Python
	bool hasCoastAtSECorner() const;

	bool isIrrigated() const;																																					// Exposed to Python
	void setIrrigated(bool bNewValue);
	void updateIrrigated();

	bool isPotentialCityWork() const;																																						// Exposed to Python
	bool isPotentialCityWorkForArea(CvArea* pArea) const;																												// Exposed to Python
	void updatePotentialCityWork();

	bool isShowCitySymbols() const;
	void updateShowCitySymbols();

	bool isFlagDirty() const;																																										// Exposed to Python
	void setFlagDirty(bool bNewValue);																																					// Exposed to Python

	DllExport PlayerTypes getOwner() const;																																			// Exposed to Python
#if (defined(__GNUC__) || defined(_USRDLL)) //PORT NEW
//#ifdef _USRDLL //PORT OLD
	inline PlayerTypes getOwnerINLINE() const
	{
		return (PlayerTypes)m_eOwner;
	}
#endif
	void setOwner(PlayerTypes eNewValue, bool bCheckUnits, bool bUpdatePlotGroup);

	PlotTypes getPlotType() const;																																			// Exposed to Python
	DllExport bool isWater() const;																																								// Exposed to Python
	bool isFlatlands() const;																																											// Exposed to Python
	DllExport bool isHills() const;																																								// Exposed to Python
	DllExport bool isPeak() const;																																								// Exposed to Python
	void setPlotType(PlotTypes eNewValue, bool bRecalculate = true, bool bRebuildGraphics = true);			// Exposed to Python

	DllExport TerrainTypes getTerrainType() const;																																	// Exposed to Python
	void setTerrainType(TerrainTypes eNewValue, bool bRecalculate = true, bool bRebuildGraphics = true);	// Exposed to Python

	DllExport FeatureTypes getFeatureType() const;																																	// Exposed to Python
	void setFeatureType(FeatureTypes eNewValue, int iVariety = -1);																				// Exposed to Python
	void setFeatureDummyVisibility(const char *dummyTag, bool show);																				// Exposed to Python
	void addFeatureDummyModel(const char *dummyTag, const char *modelTag);
	void setFeatureDummyTexture(const char *dummyTag, const char *textureTag);
	CvString pickFeatureDummyTag(int mouseX, int mouseY);
	void resetFeatureModel();

	DllExport BonusTypes getBonusType(TeamTypes eTeam = NO_TEAM) const;																							// Exposed to Python
	BonusTypes getNonObsoleteBonusType(TeamTypes eTeam = NO_TEAM, bool bCheckConnected = false) const;																	// Exposed to Python
	void setBonusType(BonusTypes eNewValue);																															// Exposed to Python

	DllExport ImprovementTypes getImprovementType() const;																													// Exposed to Python
	void setImprovementType(ImprovementTypes eNewValue);																									// Exposed to Python

	RouteTypes getRouteType() const;																																			// Exposed to Python
	void setRouteType(RouteTypes eNewValue, bool bUpdatePlotGroup);																															// Exposed to Python
	void updateCityRoute(bool bUpdatePlotGroup);

	DllExport CvCity* getPlotCity() const;																																					// Exposed to Python
	void setPlotCity(CvCity* pNewValue);

	CvCity* getWorkingCity() const;																																				// Exposed to Python
	void updateWorkingCity();

	CvCity* getWorkingCityOverride() const;																															// Exposed to Python
	void setWorkingCityOverride( const CvCity* pNewValue);

	int getRiverID() const;																																							// Exposed to Python
	void setRiverID(int iNewValue);																																			// Exposed to Python

	int getMinOriginalStartDist() const;																																// Exposed to Python
	void setMinOriginalStartDist(int iNewValue);

	int getReconCount() const;																																					// Exposed to Python
	void changeReconCount(int iChange);

	int getRiverCrossingCount() const;																																	// Exposed to Python
	void changeRiverCrossingCount(int iChange);

	// MOD - START - PlotGroup Bonus Efficiency
	bool isPlotGroupBonusDisabled() const;
	int getDisabledPlotGroupBonusCount() const;
	void changeDisabledPlotGroupBonusCount(int iChange);
	// MOD - END - PlotGroup Bonus Efficiency

	short* getYield();
	DllExport int getYield(YieldTypes eIndex) const;																										// Exposed to Python
	int calculateNatureYield(YieldTypes eIndex, TeamTypes eTeam, bool bIgnoreFeature = false) const;		// Exposed to Python
	int calculateBestNatureYield(YieldTypes eIndex, TeamTypes eTeam) const;															// Exposed to Python
	int calculateTotalBestNatureYield(TeamTypes eTeam) const;																						// Exposed to Python
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      10/06/09                                jdog5000      */
/*                                                                                              */
/* City AI                                                                                      */
/************************************************************************************************/
	// MOD - START - Advanced Yield and Commerce Effects
	//int calculateImprovementYieldChange(ImprovementTypes eImprovement, YieldTypes eYield, PlayerTypes ePlayer, bool bOptimal = false, bool bBestRoute = false) const;	// Exposed to Python
	int calculateImprovementYieldChange(ImprovementTypes eImprovement, YieldTypes eYield, PlayerTypes ePlayer, bool bOptimal = false, bool bBestRoute = false, const CvCity* pWorkingCity = NULL) const;	// Exposed to Python
	// MOD - START - Advanced Yield and Commerce Effects
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/
	int calculateYield(YieldTypes eIndex, bool bDisplay = false) const;												// Exposed to Python
	bool hasYield() const;																																		// Exposed to Python
	void updateYield();
	// int calculateMaxYield(YieldTypes eYield) const; // disabled by K-Mod
	int getYieldWithBuild(BuildTypes eBuild, YieldTypes eYield, bool bWithUpgrade) const;

	int getCulture(PlayerTypes eIndex) const;																									// Exposed to Python
	int countTotalCulture() const;																														// Exposed to Python
	int countFriendlyCulture(TeamTypes eTeam) const;
	TeamTypes findHighestCultureTeam() const;																														// Exposed to Python
	PlayerTypes findHighestCulturePlayer() const;
	int calculateCulturePercent(PlayerTypes eIndex) const;																		// Exposed to Python
	int calculateTeamCulturePercent(TeamTypes eIndex) const;																						// Exposed to Python
	void setCulture(PlayerTypes eIndex, int iNewValue, bool bUpdate, bool bUpdatePlotGroups);																		// Exposed to Python
	void changeCulture(PlayerTypes eIndex, int iChange, bool bUpdate);																	// Exposed to Python

	int countNumAirUnits(TeamTypes eTeam) const;																					// Exposed to Python
	int airUnitSpaceAvailable(TeamTypes eTeam) const;

	int getFoundValue(PlayerTypes eIndex);							// Exposed to Python
	bool isBestAdjacentFound(PlayerTypes eIndex);						// Exposed to Python
	void setFoundValue(PlayerTypes eIndex, short iNewValue);
	// K-Mod: I've changed iNewValue to be 'short' instead of 'int', so that it matches the cache.

	int getPlayerCityRadiusCount(PlayerTypes eIndex) const;																							// Exposed to Python
	bool isPlayerCityRadius(PlayerTypes eIndex) const;																									// Exposed to Python
	void changePlayerCityRadiusCount(PlayerTypes eIndex, int iChange);

	CvPlotGroup* getPlotGroup(PlayerTypes ePlayer) const;
	CvPlotGroup* getOwnerPlotGroup() const;
	void setPlotGroup(PlayerTypes ePlayer, CvPlotGroup* pNewValue);
	void updatePlotGroup();
	void updatePlotGroup(PlayerTypes ePlayer, bool bRecalculate = true);

	int getVisibilityCount(TeamTypes eTeam) const;																											// Exposed to Python
	void changeVisibilityCount(TeamTypes eTeam, int iChange, InvisibleTypes eSeeInvisible, bool bUpdatePlotGroups);							// Exposed to Python

	int getStolenVisibilityCount(TeamTypes eTeam) const;																								// Exposed to Python
	void changeStolenVisibilityCount(TeamTypes eTeam, int iChange);

	int getBlockadedCount(TeamTypes eTeam) const;																								// Exposed to Python
	void changeBlockadedCount(TeamTypes eTeam, int iChange);

	DllExport PlayerTypes getRevealedOwner(TeamTypes eTeam, bool bDebug) const;													// Exposed to Python
	TeamTypes getRevealedTeam(TeamTypes eTeam, bool bDebug) const;														// Exposed to Python
	void setRevealedOwner(TeamTypes eTeam, PlayerTypes eNewValue);
	void updateRevealedOwner(TeamTypes eTeam);

	DllExport bool isRiverCrossing(DirectionTypes eIndex) const;																				// Exposed to Python
	void updateRiverCrossing(DirectionTypes eIndex);
	void updateRiverCrossing();

	DllExport bool isRevealed(TeamTypes eTeam, bool bDebug) const;																								// Exposed to Python
	void setRevealed(TeamTypes eTeam, bool bNewValue, bool bTerrainOnly, TeamTypes eFromTeam, bool bUpdatePlotGroup);	// Exposed to Python
	bool isAdjacentRevealed(TeamTypes eTeam) const;																				// Exposed to Python
	bool isAdjacentNonrevealed(TeamTypes eTeam) const;																				// Exposed to Python

	ImprovementTypes getRevealedImprovementType(TeamTypes eTeam, bool bDebug) const;					// Exposed to Python
	void setRevealedImprovementType(TeamTypes eTeam, ImprovementTypes eNewValue);			

	RouteTypes getRevealedRouteType(TeamTypes eTeam, bool bDebug) const;											// Exposed to Python
	void setRevealedRouteType(TeamTypes eTeam, RouteTypes eNewValue);							

	int getBuildProgress(BuildTypes eBuild) const;																											// Exposed to Python  
	bool changeBuildProgress(BuildTypes eBuild, int iChange, TeamTypes eTeam = NO_TEAM);								// Exposed to Python 

	void updateFeatureSymbolVisibility(); 
	void updateFeatureSymbol(bool bForce = false);

	DllExport bool isLayoutDirty() const;							// The plot layout contains bonuses and improvements --- it is, like the city layout, passively computed by LSystems
	DllExport void setLayoutDirty(bool bDirty);
	DllExport bool isLayoutStateDifferent() const;
	DllExport void setLayoutStateToCurrent();
	bool updatePlotBuilder();

	DllExport void getVisibleImprovementState(ImprovementTypes& eType, bool& bWorked);				// determines how the improvement state is shown in the engine
	DllExport void getVisibleBonusState(BonusTypes& eType, bool& bImproved, bool& bWorked);		// determines how the bonus state is shown in the engine
	bool shouldUsePlotBuilder();
	CvPlotBuilder* getPlotBuilder() { return m_pPlotBuilder; }

	DllExport CvRoute* getRouteSymbol() const;
	void updateRouteSymbol(bool bForce = false, bool bAdjacent = false);

	DllExport CvRiver* getRiverSymbol() const;
	void updateRiverSymbol(bool bForce = false, bool bAdjacent = false);
	void updateRiverSymbolArt(bool bAdjacent = true);

	CvFeature* getFeatureSymbol() const;

	DllExport CvFlagEntity* getFlagSymbol() const;
	CvFlagEntity* getFlagSymbolOffset() const;
	DllExport void updateFlagSymbol();
	void clearFlagSymbol(); // advc.127c

	DllExport CvUnit* getCenterUnit() const;
	DllExport CvUnit* getDebugCenterUnit() const;
	void setCenterUnit(CvUnit* pNewValue);

	int getCultureRangeCities(PlayerTypes eOwnerIndex, int iRangeIndex) const;														// Exposed to Python
	bool isCultureRangeCity(PlayerTypes eOwnerIndex, int iRangeIndex) const;															// Exposed to Python
	void changeCultureRangeCities(PlayerTypes eOwnerIndex, int iRangeIndex, int iChange, bool bUpdatePlotGroups);

	int getInvisibleVisibilityCount(TeamTypes eTeam, InvisibleTypes eInvisible) const;										// Exposed to Python
	bool isInvisibleVisible(TeamTypes eTeam, InvisibleTypes eInvisible) const;														// Exposed to Python
	void changeInvisibleVisibilityCount(TeamTypes eTeam, InvisibleTypes eInvisible, int iChange);					// Exposed to Python

	int getNumUnits() const;																																		// Exposed to Python
	CvUnit* getUnitByIndex(int iIndex) const;																													// Exposed to Python
	void addUnit(CvUnit* pUnit, bool bUpdate = true);
	void removeUnit(CvUnit* pUnit, bool bUpdate = true);
	DllExport CLLNode<IDInfo>* nextUnitNode(CLLNode<IDInfo>* pNode) const;
	CLLNode<IDInfo>* prevUnitNode(CLLNode<IDInfo>* pNode) const;
	DllExport CLLNode<IDInfo>* headUnitNode() const;
	CLLNode<IDInfo>* tailUnitNode() const;

	int getNumSymbols() const;
	CvSymbol* getSymbol(int iID) const;
	CvSymbol* addSymbol();

	void deleteSymbol(int iID);
	void deleteAllSymbols();

	// MOD - START - Aid
	void changeAidSuppliedFromPlot(TeamTypes eTeam, AidTypes eAid, int iChange);

	void updateAidEffects(TeamTypes eTeam, AidTypes eAid);

	short getAidAmount(TeamTypes eTeam, AidTypes eAid) const;
	void changeAidAmount(TeamTypes eTeam, AidTypes eAid, int iChange);
	// MOD - END - Aid

	// MOD - START - Detriments
	void applyDetriments(TeamTypes eTeamA, TeamTypes eTeamB);
	void removeDetriments(TeamTypes eTeamA, TeamTypes eTeamB);
	void changeDetriments(TeamTypes eTeamA, TeamTypes eTeamB, bool bApply);

	void changeDetrimentSuppliedFromPlot(TeamTypes eAffectedTeam, DetrimentTypes eDetriment, int iChange);

	void updateDetrimentEffects(TeamTypes eAffectedTeam, DetrimentTypes eDetriment);

	short getDetrimentAmount(TeamTypes eAffectedTeam, DetrimentTypes eDetriment) const;
	void changeDetrimentAmount(TeamTypes eAffectedTeam, DetrimentTypes eDetriment, int iChange);
	// MOD - END - Detriments

	// MOD - START - Congestion
	void changeCongestionFromUnit(CvUnit* pUnit, int iChange);
	void changeCongestionFromCityStatus(int iChange);

	unsigned short getCombatUnitDomainCount(TeamTypes eTeam, DomainTypes eDomain) const; // Exposed to Python
	void setCombatUnitDomainCount(TeamTypes eTeam, DomainTypes eDomain, int iNewValue);
	// MOD - END - Congestion

	// MOD - START - Aid
	void applyAidSuppliedByImprovement(ImprovementTypes eImprovement);
	void removeAidSuppliedByImprovement(ImprovementTypes eImprovement);
	void changeAidSuppliedByImprovement(ImprovementTypes eImprovement, bool bApply);
	// MOD - END - Aid

	// Script data needs to be a narrow string for pickling in Python
	CvString getScriptData() const;																											// Exposed to Python
	void setScriptData(const char* szNewValue);																					// Exposed to Python

	bool canTrigger(EventTriggerTypes eTrigger, PlayerTypes ePlayer) const;
	bool canApplyEvent(EventTypes eEvent) const;
	void applyEvent(EventTypes eEvent);

	bool canTrain(UnitTypes eUnit, bool bContinue, bool bTestVisible) const;

	bool isEspionageCounterSpy(TeamTypes eTeam) const;

	DllExport int getAreaIdForGreatWall() const;
	DllExport int getSoundScriptId() const;
	DllExport int get3DAudioScriptFootstepIndex(int iFootstepTag) const;
	DllExport float getAqueductSourceWeight() const;  // used to place aqueducts on the map
	DllExport bool shouldDisplayBridge(CvPlot* pToPlot, PlayerTypes ePlayer) const;
	DllExport bool checkLateEra() const;

	void read(FDataStreamBase* pStream);
	void write(FDataStreamBase* pStream);
	// MOD - START - Advanced Automations
/************************************************************************************************/
/* Afforess	                  Start		 06/21/10                                               */
/*                                                                                              */
/*                                                                                              */
/************************************************************************************************/
	bool isBorder(bool bIgnoreWater = false) const;
		int getNumVisibleAdjacentEnemyDefenders(const CvUnit* pUnit) const;	
/************************************************************************************************/
/* Afforess	                     END                                                            */
/************************************************************************************************/
	// MOD - END - Advanced Automations

protected:

	short m_iX;
	short m_iY;
	int m_iArea;
	mutable CvArea *m_pPlotArea;
	short m_iFeatureVariety;
	short m_iOwnershipDuration;
	short m_iImprovementDuration;
	short m_iUpgradeProgress;
	short m_iForceUnownedTimer;
	short m_iCityRadiusCount;
	int m_iRiverID;
	short m_iMinOriginalStartDist;
	short m_iReconCount;
	short m_iRiverCrossingCount;

	// MOD - START - PlotGroup Bonus Efficiency
	short m_iDisabledPlotGroupBonusCount;
	// MOD - END - PlotGroup Bonus Efficiency

	bool m_bStartingPlot:1;
	bool m_bHills:1;
	bool m_bNOfRiver:1;
	bool m_bWOfRiver:1;
	bool m_bIrrigated:1;
	bool m_bPotentialCityWork:1;
	bool m_bShowCitySymbols:1;
	bool m_bFlagDirty:1;
	bool m_bPlotLayoutDirty:1;
	bool m_bLayoutStateWorked:1;

	char /*PlayerTypes*/ m_eOwner;
	short /*PlotTypes*/ m_ePlotType;
	short /*TerrainTypes*/ m_eTerrainType;
	short /*FeatureTypes*/ m_eFeatureType;
	short /*BonusTypes*/ m_eBonusType;
	short /*ImprovementTypes*/ m_eImprovementType;
	short /*RouteTypes*/ m_eRouteType;
	char /*CardinalDirectionTypes*/ m_eRiverNSDirection;
	char /*CardinalDirectionTypes*/ m_eRiverWEDirection;

	IDInfo m_plotCity;
	IDInfo m_workingCity;
	IDInfo m_workingCityOverride;

/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      08/21/09                                jdog5000      */
/*                                                                                              */
/* Efficiency                                                                                   */
/************************************************************************************************/
	// Plot danger cache
	//bool m_bActivePlayerNoDangerCache;
	int m_iActivePlayerSafeRangeCache; // K-Mod (the bbai implementation was flawed)
	bool* m_abBorderDangerCache;
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/

	short* m_aiYield;
	int* m_aiCulture;
	short* m_aiFoundValue;
	char* m_aiPlayerCityRadiusCount;
	int* m_aiPlotGroup;			// IDs - keep as int
	short* m_aiVisibilityCount;
	short* m_aiStolenVisibilityCount;
	short* m_aiBlockadedCount;
	char* m_aiRevealedOwner;

	bool* m_abRiverCrossing;	// bit vector
	bool* m_abRevealed;

	short* /*ImprovementTypes*/ m_aeRevealedImprovementType;
	short* /*RouteTypes*/ m_aeRevealedRouteType;

	char* m_szScriptData;

	short* m_paiBuildProgress;

	CvFeature* m_pFeatureSymbol;
	CvRoute* m_pRouteSymbol;
	CvRiver* m_pRiverSymbol;
	CvFlagEntity* m_pFlagSymbol;
	CvFlagEntity* m_pFlagSymbolOffset;
	CvUnit* m_pCenterUnit;

	CvPlotBuilder* m_pPlotBuilder;		// builds bonuses and improvements

	char** m_apaiCultureRangeCities;
	short** m_apaiInvisibleVisibilityCount;

	// MOD - START - Aid
	short** m_apaiTeamAidAmount;
	// MOD - END - Aid

	// MOD - START - Detriments
	short** m_apaiTeamDetrimentAmount;
	// MOD - END - Detriments

	// MOD - START - Congestion
	unsigned short** m_apaiTeamCombatUnitDomainCount;
	// MOD - END - Congestion

	CLinkList<IDInfo> m_units;

	std::vector<CvSymbol*> m_symbols;

	void doFeature();
	void doCulture();

	void processArea(CvArea* pArea, int iChange);
	void doImprovementUpgrade();

	ColorTypes plotMinimapColor();

	// added so under cheat mode we can access protected stuff
	friend class CvGameTextMgr;

/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      02/21/10                                jdog5000      */
/*                                                                                              */
/* Lead From Behind                                                                             */
/************************************************************************************************/
// From Lead From Behind by UncutDragon
public:
	bool hasDefender(bool bCheckCanAttack, PlayerTypes eOwner, PlayerTypes eAttackingPlayer = NO_PLAYER, const CvUnit* pAttacker = NULL, bool bTestAtWar = false, bool bTestPotentialEnemy = false, bool bTestCanMove = false) const;
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/
	// MOD - START - Graphical Paging (45deg)
	void pageGraphicsOut(void);
	static void notePageRenderStart(int iRenderArea);
	
protected:
	short m_iGraphicsPageIndex;
	// MOD - END - Graphical Paging (45deg)
};

#endif
