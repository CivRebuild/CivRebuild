#
#	FILE:	 Ice_Age.py
#	AUTHOR:  Bob Thomas (Sirian)
#	PURPOSE: Global map script - Simulates habitable region at the
#	         equator during severe glaciation of a random world.
#-----------------------------------------------------------------------------
#	Copyright (c) 2005 Firaxis Games, Inc. All rights reserved.
#-----------------------------------------------------------------------------
#

from CvPythonExtensions import *
import CvUtil
import CvMapGeneratorUtil
from CvMapGeneratorUtil import FractalWorld
from CvMapGeneratorUtil import TerrainGenerator
from CvMapGeneratorUtil import FeatureGenerator

import MapScriptTools as mst
balancer = mst.bonusBalancer

# The following global constants are not neccessary,
# but they are widely used and make reading the code easier.
# (Yes I know thet local variables are faster, but that's only appreciable
#  within deeply nested loops, and the script runs only once per game anyway.)
# ----------------------------------------------------------------------------
gc = CyGlobalContext()
map = CyMap()

'''
SIRIAN'S NOTES

Ice Age turned out to be a fun script. The extreme difference between the 
width and height pulls unusual results from the fractal generator: many 
wide, short landmasses that offer a unique map balance. Combined with the 
lower sea levels (lots of water from the oceans locked in the polar ice), 
this script offers a uniquely snaky and intertwining set of lands. The 
lands are also close to one another, allowing intense early naval activity.

This script can be particularly fun for team games!

- Bob Thomas  July 14, 2005
'''

def getVersion():
	return "1.20a"

def getDescription():
	return "TXT_KEY_MAP_SCRIPT_ICE_AGE_DESCR"

def getNumCustomMapOptions():
	return 1
	
def getCustomMapOptionName(argsList):
	translated_text = unicode(CyTranslator().getText("TXT_KEY_MAP_SCRIPT_LANDMASS_TYPE", ()))
	return translated_text
	
def getNumCustomMapOptionValues(argsList):
	# Four selections for Landmass Types option
	return 5
	
def getCustomMapOptionDescAt(argsList):
	iSelection = argsList[1]
	selection_names = ["TXT_KEY_MAP_SCRIPT_RANDOM",
	                   "TXT_KEY_MAP_SCRIPT_WIDE_CONTINENTS",
	                   "TXT_KEY_MAP_SCRIPT_NARROW_CONTINENTS",
	                   "TXT_KEY_MAP_SCRIPT_ISLANDS",
	                   "TXT_KEY_MAP_SCRIPT_SMALL_ISLANDS"]
	translated_text = unicode(CyTranslator().getText(selection_names[iSelection], ()))
	return translated_text
	
def getCustomMapOptionDefault(argsList):
	return 0

def isRandomCustomMapOption(argsList):
	# Disable default Random and implement custom "weighted" Random.
	return false

def isAdvancedMap():
	"This map should show up in simple mode"
	return 0

def isClimateMap():
	return 0

def beforeGeneration():
	print "-- beforeGeneration()"

	# Create mapInfo string - this should work for all maps
	mapInfo = ""
	for opt in range( getNumCustomMapOptions() ):
		nam = getCustomMapOptionName( [opt] )
		sel = map.getCustomMapOption( opt )
		txt = getCustomMapOptionDescAt( [opt,sel] )
		mapInfo += "%27s:   %s\n" % ( nam, txt )

	# Create function for mst.evalLatitude - here Ringworld3
	#if mapOptions.Polar == 0:
	#	compGetLat = "int(round([0.95,0.80,0.64,0.60,0.52,0.40,0.24,0.04,0.04,0.24,0.40,0.52,0.60,0.64,0.80,0.95][y]*80))"
	#elif mapOptions.Polar == 1:
	#	compGetLat = "int(round([0.98,0.86,0.75,0.65,0.56,0.48,0.41,0.34,0.27,0.21,0.16,0.12,0.09,0.06,0.03,0.00][y]*80))"
	#elif mapOptions.Polar == 2:
	#	compGetLat = "int(round([0.00,0.03,0.06,0.09,0.12,0.16,0.21,0.27,0.34,0.41,0.48,0.56,0.65,0.75,0.86,0.98][y]*80))"
	#elif mapOptions.Polar == 3:
	#	compGetLat = "int(round([0.70,0.57,0.47,0.37,0.28,0.20,0.13,0.08,0.03,0.00,0.03,0.08,0.13,0.20,0.28,0.37][y]*90))"

	# Initialize MapScriptTools
	mst.getModInfo( getVersion(), None, mapInfo, bNoSigns=False )

	# Initialize MapScriptTools.BonusBalancer
	# - balance boni, place missing boni, move minerals, longer balancing range
	balancer.initialize( True, True, True, True )

	# Initialize MapScriptTools.MapRegions, don't use landmarks for FFH or Planetfall
	#mst.mapRegions.initialize( noSigns = (mst.bFFH or bPfall) )

def getGridSize(argsList):
	# Override Grid Size function to make shorter than normal.
	# Map widths unchanged. Height reduced (lands lost to polar ice)
	grid_sizes = {
		WorldSizeTypes.WORLDSIZE_DUEL:		(10,4),
		WorldSizeTypes.WORLDSIZE_TINY:		(13,5),
		WorldSizeTypes.WORLDSIZE_SMALL:		(16,7),
		WorldSizeTypes.WORLDSIZE_STANDARD:	(22,10),
		WorldSizeTypes.WORLDSIZE_LARGE:		(28,12),
		WorldSizeTypes.WORLDSIZE_HUGE:		(36,14),
		WorldSizeTypes.WORLDSIZE_GIANT:		(42,18)
	}

	if (argsList[0] == -1): # (-1,) is passed to function on loads
		return []
	[eWorldSize] = argsList
	return grid_sizes[eWorldSize]

# Subclass FractalWorld to alter min/max Sea Level.
class IceAgeFractalWorld(CvMapGeneratorUtil.FractalWorld):
	def checkForOverrideDefaultUserInputVariances(self):
		self.seaLevelMax = 72
		self.seaLevelMin = 60
		return

def generatePlotTypes():
	NiTextOut("Setting Plot Types (Python Ice Age) ...")
	gc = CyGlobalContext()
	map = CyMap()
	dice = gc.getGame().getMapRand()
	fractal_world = IceAgeFractalWorld()
	water = 65

	# Get custom user input.
	userInputLandmass = map.getCustomMapOption(0)
	if userInputLandmass == 0: # Weighted Random
		random = True
		# Roll a D20 in case of random landmass size, to choose the option.
		# 0-1 = pangaea
		# 2-4 = large continents
		# 5-9 = mixed continents, widely varied in shape and size
		# 10-16 = small continents and islands
		# 17-19 = archipelago
		terrainRoll = dice.get(20, "PlotGen Chooser - Ice Age PYTHON")
		if terrainRoll < 2:
			land_type = 0
		elif terrainRoll < 5:
			land_type = 1
		elif terrainRoll < 10:
			land_type = 2
		elif terrainRoll < 17:
			land_type = 3
		else:
			land_type = 4

	else: # User's Choice
		if userInputLandmass > 1:
			land_type = userInputLandmass
		else:
			continentRoll = dice.get(5, "PlotGen Chooser - Ice Age PYTHON")
			if continentRoll > 1:
				land_type = 1
			else:
				land_type = 0

	# Now implement the landmass type.
	if land_type == 2: # Narrow Continents
		fractal_world.initFractal(continent_grain = 3, rift_grain = -1, has_center_rift = False, polar = True)
		return fractal_world.generatePlotTypes(water_percent = water, grain_amount = 4)
		
	elif land_type == 3: # Islands
		fractal_world.initFractal(continent_grain = 4, rift_grain = -1, has_center_rift = False, polar = True)
		return fractal_world.generatePlotTypes(water_percent = water, grain_amount = 4)
		
	elif land_type == 4: # Tiny Islands
		fractal_world.initFractal(continent_grain = 5, rift_grain = -1, has_center_rift = False, polar = True)
		return fractal_world.generatePlotTypes(water_percent = water, grain_amount = 4)
		
	elif land_type == 0: # Wide Continents, Huge
		fractal_world.initFractal(continent_grain = 1, rift_grain = 2, has_center_rift = False, polar = True)
		return fractal_world.generatePlotTypes(water_percent = water)
	
	else: # Wide Continents, Large
		fractal_world.initFractal(rift_grain = 3, has_center_rift = True, polar = True)
		return fractal_world.generatePlotTypes(water_percent = water)

# subclass TerrainGenerator to cool the climate compared to normal.
# Also, desert reduced, plains dramatically increased. Latitudes shifted colder.
class IceAgeTerrainGenerator(CvMapGeneratorUtil.TerrainGenerator):
	def __init__(self, iDesertPercent=20, iPlainsPercent=50, 
	             fSnowLatitude=0.4, fTundraLatitude=0.3,
	             fGrassLatitude=0.0, fDesertBottomLatitude=0.1, 
	             fDesertTopLatitude=0.2, fracXExp=-1, 
	             fracYExp=-1, grain_amount=4):
		
		self.gc = CyGlobalContext()
		self.map = CyMap()

		self.iWidth = self.map.getGridWidth()
		self.iHeight = self.map.getGridHeight()

		self.mapRand = self.gc.getGame().getMapRand()
		self.iFlags = self.map.getMapFractalFlags()

		self.grain_amount = grain_amount + self.gc.getWorldInfo(self.map.getWorldSize()).getTerrainGrainChange()

		self.deserts=CyFractal()
		self.plains=CyFractal()
		self.variation=CyFractal()

		self.iDesertTopPercent = 100
		self.iDesertBottomPercent = max(0,int(100-iDesertPercent))
		self.iPlainsTopPercent = 100
		self.iPlainsBottomPercent = max(0,int(100-iDesertPercent-iPlainsPercent))
		self.iMountainTopPercent = 75
		self.iMountainBottomPercent = 60

		self.fSnowLatitude = fSnowLatitude
		self.fTundraLatitude = fTundraLatitude
		self.fGrassLatitude = fGrassLatitude
		self.fDesertBottomLatitude = fDesertBottomLatitude
		self.fDesertTopLatitude = fDesertTopLatitude

		self.iDesertPercent = iDesertPercent
		self.iPlainsPercent = iPlainsPercent

		self.fracXExp = fracXExp
		self.fracYExp = fracYExp

		self.initFractals()

	def getLatitudeAtPlot(self, iX, iY):
		lat = abs((self.iHeight / 2) - iY)/float(self.iHeight/2) # 0.0 = equator, 1.0 = pole

		# Adjust latitude using self.variation fractal, to mix things up:
		lat += (128 - self.variation.getHeight(iX, iY))/(255.0 * 5.0)

		# Limit to the range [0, 1]:
		if lat < 0:
			lat = 0.0
		if lat > 1:
			lat = 1.0
		# Since the map is "shorter", adjust latitudes to match, at 0.6
		# In order to increase the coverage of tundra latitude, had to increase the "power" of each 0.1 of latitudal effect.
		# Making this change required changes to addIceAtPlot function.
		lat = lat * 0.6
                
		return lat

def generateTerrainTypes():
	NiTextOut("Generating Terrain (Python Ice Age) ...")
	terraingen = IceAgeTerrainGenerator()
	terrainTypes = terraingen.generateTerrain()
	return terrainTypes

# subclass FeatureGenerator to cool the climate compared to normal
# Jungles only appear on grass near equator. Percentage appearance reduced.
# Forest percentage reduced slightly.
class IceAgeFeatureGenerator(CvMapGeneratorUtil.FeatureGenerator):
	def __init__(self, iJunglePercent=30, iForestPercent=50, 
	             jungle_grain=7, forest_grain=6, 
	             fracXExp=-1, fracYExp=-1):
		self.gc = CyGlobalContext()
		self.map = CyMap()
		self.mapRand = self.gc.getGame().getMapRand()
		self.jungles = CyFractal()
		self.forests = CyFractal()
		self.iFlags = self.map.getMapFractalFlags()
		self.iGridW = self.map.getGridWidth()
		self.iGridH = self.map.getGridHeight()

		self.iJunglePercent = iJunglePercent
		self.iForestPercent = iForestPercent

		jungle_grain += self.gc.getWorldInfo(self.map.getWorldSize()).getFeatureGrainChange()
		forest_grain += self.gc.getWorldInfo(self.map.getWorldSize()).getFeatureGrainChange()

		self.jungle_grain = jungle_grain
		self.forest_grain = forest_grain

		self.fracXExp = fracXExp
		self.fracYExp = fracYExp

		self.__initFractals()
		self.__initFeatureTypes()
	
	def __initFractals(self):
		self.jungles.fracInit(self.iGridW, self.iGridH, self.jungle_grain, self.mapRand, self.iFlags, self.fracXExp, self.fracYExp)
		self.forests.fracInit(self.iGridW, self.iGridH, self.forest_grain, self.mapRand, self.iFlags, self.fracXExp, self.fracYExp)

		self.iJungleBottom = self.jungles.getHeightFromPercent((100 - self.iJunglePercent)/2)
		self.iJungleTop = self.jungles.getHeightFromPercent(100 - (self.iJunglePercent/2))
		self.iForestLevel = self.forests.getHeightFromPercent(self.iForestPercent)

	def __initFeatureTypes(self):
		self.featureIce = self.gc.getInfoTypeForString("FEATURE_ICE")
		self.featureJungle = self.gc.getInfoTypeForString("FEATURE_JUNGLE")
		self.featureForest = self.gc.getInfoTypeForString("FEATURE_FOREST")
		self.featureOasis = self.gc.getInfoTypeForString("FEATURE_OASIS")

	def getLatitudeAtPlot(self, iX, iY):
		"Ice Age specific function: returns a value in the range of 0.0 (temperate) to 0.6 (polar)"
		# 0.0 = equator, 0.3 = tundra, 0.6 = edge of impassable ice.
		return abs((self.iGridH/2) - iY)/float(self.iGridH/2) * 0.6
		
	def addIceAtPlot(self, pPlot, iX, iY, lat):
		if pPlot.canHaveFeature(self.featureIce):
			if iY == 0 or iY == self.iGridH - 1:
				pPlot.setFeatureType(self.featureIce, -1)
			elif lat > 0.47:
				rand = self.mapRand.get(100, "Add Ice PYTHON")/100.0
				if rand < 8*(lat-0.50):
					pPlot.setFeatureType(self.featureIce, -1)
				elif rand < 4*(lat-0.46):
					pPlot.setFeatureType(self.featureIce, -1)
			# Add encroaching icebergs reaching out beyond normal range - Sirian, June18-2005
			elif lat > 0.39:
				rand = self.mapRand.get(100, "Add Encroaching Ice - Sirian's Ice Age - PYTHON")/100.0
				if rand < 0.06:
					pPlot.setFeatureType(self.featureIce, -1)
			elif lat > 0.32:
				rand = self.mapRand.get(100, "Add Encroaching Ice - Sirian's Ice Age - PYTHON")/100.0
				if rand < 0.04:
					pPlot.setFeatureType(self.featureIce, -1)
			elif lat > 0.27:
				rand = self.mapRand.get(100, "Add Encroaching Ice - Sirian's Ice Age - PYTHON")/100.0
				if rand < 0.02:
					pPlot.setFeatureType(self.featureIce, -1)

def addFeatures():
	NiTextOut("Adding Features (Python Ice Age) ...")
	featuregen = IceAgeFeatureGenerator()
	featuregen.addFeatures()
	return 0


def addRivers():
	print "-- addRivers()"
	mst.mapPrint.buildTerrainMap( True, "addRivers()" )

	# Generate marsh terrain
	mst.marshMaker.convertTerrain()

	# Expand coastal waters - you may not want this
	mst.mapPrettifier.expandifyCoast()
	# Some scripts produce more chaotic terrain than others. You can create more connected
	# (bigger) deserts by converting surrounded plains and grass.
	# Prettify the map - create better connected deserts and plains
	mst.mapPrettifier.lumpifyTerrain( mst.etDesert, mst.etPlains, mst.etGrass )
	mst.mapPrettifier.lumpifyTerrain( mst.etPlains, mst.etDesert, mst.etGrass )

	# No standard rivers for 'SandsOfMars'
	CyPythonMgr().allowDefaultImpl()							# don't forget this

	# Put rivers on small islands
	mst.riverMaker.islandRivers()
	
def addLakes():
	print "-- addLakes()"
	mst.mapPrint.buildRiverMap( True, "addRivers()" )

	CyPythonMgr().allowDefaultImpl()
	
def addBonuses():
	print "-- addBonuses()"
	mst.mapPrint.buildFeatureMap( True, "addBonuses()" )

	# if the script handles boni itself, insert the function here
	CyPythonMgr().allowDefaultImpl()
	
def assignStartingPlots():
	print "-- assignStartingPlots()"
	mst.mapPrint.buildBonusMap( True, "assignStartingPlots()" )

	CyPythonMgr().allowDefaultImpl()
	
	
def normalizeStartingPlotLocations():
	print "-- normalizeStartingPlotLocations()"
	mst.mapPrint.buildRiverMap( True, "addRivers()" )		# river-map also shows starting-plots

	# shuffle starting-plots for teams
	#opt = map.getCustomMapOption(3)						# assuming the 4th map-option is for teams
	#if opt == 0:
	#	CyPythonMgr().allowDefaultImpl()					# by default civ places teams near to each other
	#	# mst.teamStart.placeTeamsTogether( True, True )	# use teamStart to place teams near to each other
	#elif opt == 1:
	#	mst.teamStart.placeTeamsTogether( False, True )		# shuffle starting-plots to separate team players
	#elif opt == 2:
	#	mst.teamStart.placeTeamsTogether( True, True )		# randomize starting-plots (may be near or not)
	#else:
	#	mst.teamStart.placeTeamsTogether( False, False )	# leave starting-plots alone

	# comment this out if team option exists
	CyPythonMgr().allowDefaultImpl()
	
def normalizeAddExtras():
	print "-- normalizeAddExtras()"

	# Balance boni, place missing boni and move minerals
	balancer.normalizeAddExtras()

	# Do the default housekeeping
	CyPythonMgr().allowDefaultImpl()

	# Print maps and stats
	mst.mapStats.statPlotCount( "" )
	# Print plotMap
	mst.mapPrint.buildPlotMap( True, "normalizeAddExtras()" )
	# Print areaMap
	mst.mapPrint.buildAreaMap( True, "normalizeAddExtras()" )
	# Print terrainMap
	mst.mapPrint.buildTerrainMap( True, "normalizeAddExtras()" )
	# Print featureMap
	mst.mapPrint.buildFeatureMap( True, "normalizeAddExtras()" )
	# Print bonusMap
	mst.mapPrint.buildBonusMap( True, "normalizeAddExtras()" )
	# Print riverMap
	mst.mapPrint.buildRiverMap( True, "normalizeAddExtras()" )
	# Print mod and map statistics
	mst.mapStats.mapStatistics()