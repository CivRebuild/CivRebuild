#!/usr/bin/env python2
##############################################################################
## File: TotestraRG32.py version 2019-07-28 (July 28, 2019)

## 2019-07-19 Update: The map generator now places huts on the map;
## each non-desert land non-ice square has a 2.5% chance of having a hut; 
## each desert square has a 3.7% chance of having a hut.  A hut must be at 
## least three squares away from other huts.  This way, huts
## do not vary every time we generate a map with a given seed, and it's
## now possible for the user to adjust how many huts a map has.
## One can change the number of huts by setting desertHutChance and
## normalHutChance.

## 2019-07-06 Update: New preset seed; it's now possible to run this
## generator stand alone.  Make sure to have Python2 installed (yes, I know,
## but this generator is from the mid-first-2000s-decade), then type in
## something like: python TotestraRG32.py 5
## This will generate the "T5" random map, which is the same map as the
## "T5" pull-down seed option.  Note that, when run standalone, the map
## generator will generate a plot map then exit.  The map is all of the
## default options, which can not be changed (in particular, in the stand
## alone mode, we only generate 144x96 huge medium patience world maps)
## This allows us to make random worlds without needing Civilization IV
## installed.  This has two benefits:
## 1) People without Civilization IV can enjoy this map generator
## 2) We can now automate the generation of maps to better find really
##	good random worlds

## 2018-07-14 Update: Update preset seeds to make good 3:2 maps
## 2018-07-04 Update: Make sure RG32 maps use different service tags
## than MT19937 maps, so there is no confusion.  Increase number of possible
## maps from 9007199254740992 to 95428956661682176; the preset seed
## maps use different seeds and will never show up if random seed chosen
## The service tag now has the literal base-26 string used as the map seed
## (more RNGs should have support for string seeds)
## Note: We use RagioGatun[32] instead of MT19937 for RNG
## Note: This is a finished product.  
## Original file: PerfectWorld.py version 2.06
## Author: Rich Marinaccio
## Modified by Sam Trenholme; I am assigning all copyright to Rich
## Copyright 2007 Rich Marinaccio
##
## This map script for Civ4 generates a random, earth-like map, usually with a
## 'New World' with no starting locations that can only be reached with
## ocean going technology. Though great pains are taken to accurately simulate
## landforms and climate, the goal must be to make unpredictible, beautiful
## looking maps that are fun to play on.
## 
## -- Summary of creation process: --
## First, a random heightfield is created using midpoint displacement. The
## resulting altitudes are then modified by a plate tectonics scheme that
## grows random plates and raises the altitudes near the plate borders to
## create mountain ranges and island chains.
##
## In generating the plot types from a heightmap, I had found that using
## peaks for high altitude and land for less altitude created large clusters
## of peaks, surrounded by a donut of hills, surrounded again by a donut of
## land. This looked absolutely terrible for Civ, so I made it such that
## peaks and hills are determined by altitude *differences* rather than by
## absolute altitude. This approach looks much better and more natural.
##
## The terrain generator gives the other needed visual cues to communicate
## altitude. Since air temperature gets colder with altitude, the peaks will
## be plots of ice and tundra, even near the equator, if the altitude
## is high enough. Prevailing winds, temperature and rainfall are all simulated
## in the terrain generator. You will notice that the deserts and rainforests
## are where they should be, as well as rain shadows behind mountain ranges.
##
## Rivers and lakes are also generated from the heightmap and follow accurate
## drainage paths, although with such a small heightmap some randomness needs
## to be thrown in to prevent rivers from being merely straight lines.
##
## Map bonuses are placed following the XML Rules but slightly differently than
## the default implimentation to better accomodate this map script.
##
## I've always felt that the most satisfying civ games are the ones that
## provide a use for those explorers and caravels. Though the map generator
## does not explicitly create a 'New World', it will take advantage of any
## continents that can serve that purpose. No starting locations will be placed
## on these continents. Therefore, the likelyhood of a significant new world
## is very high, but not guaranteed. It might also come in the form of multiple
## smaller 'New Worlds' rather than a large continent.
##
##############################################################################
## Version History
## Totestra - Sam Trenholme's update of PerfectWorld2.py
##
## 2017-03-30:
## 1) Converted line feeds in to DOS format so the script can be edited
##	in Notepad on Windows.  No other changes done.
##
## 2017-03-29:
## 1) Update tropical climate done by q3max, see http://bit.ly/2oAKQSx
##	for original patch
##
## 20120615:
## 1) One-line bugfix for multi-player maps
##
## 20120612:
## 1) Bugfix with rocky maps
##
## 20120603:
## 1) The chance of a large continent splitting at the edge of the map
##	has been greatly reduced
## 2) There is now an option to remove coastal mountains and reduce inland
##	mountains
## 3) New map wrap option: PerfectWorld-compatible toric wrap
## 4) All bits in the service tag are now used up.  I'm declaring Totestra
##	finished.
##
## 20120530:
## 1) Added 2-bit "parity" to service tag
##
## 20120527:
## 1) Adding test case for bug reported by En Dotter
##
## 20120526:
## 1) En Dotter feature request: It's now possible to change how the map
##	distributes resources
##
## 20120524:
## 1) New civ placement option: Have all civs placed on the same continent
##
## 20120523:
## 1) New option: Handicap level.  This can give the human player extra
##	starting resources.
## 2) Options to split continents and to have players on the "new world"
##	verified to work.
##
## 20120522:
## 1) "Service tag" added as a sign in maps, so people who forgot to log
##	Python debug information can still get full support.
##
## 20120521:
## 1) Overhaul of selection code; symbolic names are now used instead of
##	numbers
## 2) Map ratios now can be selected (within reason)
##
## 20120519:
## 1) Extra-slow maps disabled; they just put PerfectWorld in to an 
##	infinite loop
## 2) "Fast and cheap" maps tested; they work with all three preset 
##	seeds so I'm declaring these maps stable.
## 3) Iceberg code overhaul: Polar icebergs are now more common in cold 
##	and/or large maps, and less common in smaller and/or warmer maps.
##
## 20120512:
## 1) Faster lower-quality maps now tweaked and fixed.  "fast and dirty" caps
##	the size: if you ask for huge you will get a medium sized map.
## 2) Climate can now be selected and it affects the map
## 3) Begin work on making the map ratio user-configurable
##
## 20120505: 
## 1) Water level can now be adjusted in Civ4's GUI
## 2) It is now possible to use a fixed or a random map seed
## 3) There is an untested ability to more quickly make lower-quality maps,
##	or, likewise, more slowly make better maps.
##
## Perfect World 2, Cephalo's original map generator changelog history:
##
## 2.06 - Fixed a few bugs from my minimum hill/maximum bad feature function.
##
## 2.05 - Made maps of standard size and below a bit smaller. Changed the way I
## remove jungle to prevent excessive health problems. Tiles in FC on different
## continents have zero value. Tiles on different continents will not be boosted
## with resources or hills. Water tiles have zero value for non-coastal cities.
## Water tiles will not be boosted with resources for non-coastal cities, land
## tiles will be boosted instead. (lookout Sid's Sushi!)
##
## 2.04 - Changed many percent values to be a percent of land tiles rather than
## total map tiles for easier, more predictable adjustment. Ensured a minimum
## number of hills in a starting fat cross. Disabled the normalizeRemovePeaks
## function a replaced it with a maximum peaks in FC function. Added bonus
## resources to FC depending on player handicap. Added a value bonus for cities
## placed on river sides.
##
## 2.03 - Fixed an initialization problem related to Blue Marble. Added some
## enhanced error handling to help me track down some of the intermittant bugs
## that still remain.
##
## 2.02 - Fixed some problems with monsoons that were creating strange artifacts
## near the tropics. Added an exponential curve to heat loss due to altitude, so
## that jungles can appear more readily without crawling to inappropriate
## latitudes.
##
## 2.01 - Changed the way I handled a vanilla version difference. Added toroidal
## and flat map options. Made tree amount more easily adjustable. Added a variable to
## tune the level of resource bonuses. Changed the rules for fixing tundra/ice next
## to desert. Added altitude noise to the plate map to improve island chains. Added
## a variable to control heat loss due to high altitude. Implimented a new interleaved
## bonus placement scheme so that bonuses are placed individually in random order,
## rather than all of each bonus type at once. Brought back the meteor code from
## PerfectWorld 1 and eliminated the east/west continent divide.
##
## 2.0 - Rebuilt the landmass and climate model using the FaireWeather.py for
## Colonization map script engine. Improved the river system. Fixed some
## old bugs.
##
## 1.13 - Fixed a bug where starting on a goody hut would crash the game.
## Prevented start plots from being on mountain peaks. Changed an internal
## distance calculation from a straight line to a path distance, improving
## start locations somewhat. Created a new tuning variable called
## DesertLowTemp. Since deserts in civ are intended to be hot deserts, this
## variable will prevent deserts from appearing near the poles where the
## desert texture clashes horribly with the tundra texture.
##
## 1.12 - Found a small bug in the bonus placer that gave bonuses a minimum
## of zero, this is why duel size maps were having so much trouble.
##
## 1.11 - limited the features mixing with bonuses to forests only. This
## eliminates certain undesireable effects like floodplains being erased by
## or coinciding with oil or incense, or corn appearing in jungle.
##
## 1.10 - Wrapped all map constants into a class to avoid all those
## variables being loaded up when PW is not used. Also this makes it a
## little easier to change them programatically. Added two in-game options,
## New World Rules and Pangaea Rules. Added a tuning variable that allows
## bonuses with a tech requirement to co-exist with features, so that the
## absence of those features does not give away their location.
##
## 1.09 - Fixed a starting placement bug introduced in 1.07. Added a tuning
## variable to turn off 'New world' placement.
##
## 1.08 - Removed the hemispheres logic and replaced it with a simulated meteor
## shower to break up pangeas. Added a tuning variable to allow pangeas.
##
## 1.07 - Placing lakes and harbors after river placement was not updating river
## crossings. Resetting rivers after lake placement should solve this. Fixed a
## small discrepancy between Python randint and mapRand to make them behave the
## same way. Bonuses of the same bonus class, when forced to appear on the
## same continent, were sometimes crowding each other off the map. This was
## especially problematic on the smaller maps. I added some additional, less
## restrictive, passes to ensure that every resource has at least one placement
## unless the random factors decide that none should be placed. Starting plot
## normalization now will place food if a different bonus can not be used due
## to lack of food. Changed heightmap generation to more likely create a
## new world.
##
## 1.06 - Overhauled starting positions and resource placement to better
## suit the peculiarities of PerfectWorld
##
## 1.05 - Fixed the Mac bug and the multi-player bug.
##
## 1.04a - I had unfairly slandered getMapRand in my comments. I had stated
## that the period was shortened unnecessarily, which is not the case.
##
## 1.04 - Added and option to use the superior Python random number generator
## or the getMapRand that civ uses. Made the number of rivers generated tunable.
## Fixed a bug that prevented floodplains on river corners. Made floodplains
## in desert tunable.
##
## 1.03a - very minor change in hope of finding the source of a multi-player
## glitch.
##
## 1.03 - Improved lake generation. Added tuning variables to control some
## new features. Fixed some minor bugs involving the Areamap filler
## and fixed the issue with oasis appearing on lakes. Maps will now report
## the random seed value that was used to create them, so they can be easily
## re-created for debugging purposes.
##
## 1.02 - Fixed a bug that miscalculated the random placing of deserts. This
## also necessitated a readjustment of the default settings.
##
## 1.01 - Added global tuning variables for easier customization. Fixed a few
## bugs that caused deserts to get out of control.
##

IsStandAlone = False
if __name__ != "__main__":
	from CvPythonExtensions import *
	import CvUtil
	import CvMapGeneratorUtil 

from array import array
from random import random,randint,seed
import math
import sys
import time
import os

import MapScriptTools as mst
balancer = mst.bonusBalancer

map = CyMap()

# Options
OPTION_MapSeed = 10
OPTION_NewWorld = 0
OPTION_Pangaea = 1
OPTION_Wrap = 2
OPTION_IslandFactor = 3
OPTION_Patience = 4
OPTION_MapRatio = 5
OPTION_MapResources = 6
OPTION_Handicap = 7
OPTION_NoRotate = 8
OPTION_SmoothPeaks = 9
OPTION_MAX = OPTION_MapSeed + 1 # Add 1 because it's 1-indexed

# Setting this to 1 will allow the buggy 1:2 ratio and the huge 6:4 ratio
# these ratios have problems because of limitations in Civ 4's engine.  
# You have been warned.
ALLOW_EXTREME_RATIOS = 0

# Setting this to 0 will make it so the map does not have a "Service Tag"
# sign placed on it.  If the sign (which should be placed in an unusable
# ice square, usually at the top of the map) annoys you, disabled this, but
# heed this warning first:
# I CAN NOT PROVIDE TECHNICAL ASSISTANCE WITHOUT A SERVICE TAG FOR YOUR
# MAP.  DO NOT FILE A BUG REPORT OR ASK FOR TECHNICAL ASSISTANCE UNLESS YOU
# HAVE A SERVICE TAG.
ADD_SERVICE_TAG = 0

# Quick and dirty 2-bit "party" of hex number
def a91a15d7(x):
		# a and b are 2-bit inputs for the s-box
		# s is a 32-bit representation of this s-box
	def sbox(a,b,s):
		a &= 3
		b &= 3
		index = (a | (b << 2))
		out = s
		out >>= (index * 2)
		out &= 3
		return out

	if x < 0:
		return -1 # ERROR
	out = 0
	index = 0
	while(x > 0):
		q = (x & 3)
		s = sbox(q,index,0xa91a15d7) # From RadioGatun[32] of "parity"
		out += s
		out ^= q
		out &= 3
		index += 1
		index &= 3
		x >>= 2
	return out & 3

class MapConstants :
	def __init__(self):
		self.totestra = 0 
		self.hmWidth  = 0
		self.hmHeight = 0
		self.noRotate = 0
		self.smoothPeaks = 1
		self.serviceFlags = 0 # Used for concise description of flags
		self.xtraFlags = 0 # We're running out of bits :(
		self.AllowPangeas = False
		self.serviceString = "MP No Tag" # No cheating in multiplayer!
		return
		
	def initialize(self):
		print "Initializing map constants"
##############################################################################
## GLOBAL TUNING VARIABLES: Change these to customize the map results
		
		#---The following variables are not based on percentages. Because temperature
		#---is so strongly tied to latitude, using percentages for things like ice and
		#---tundra leads to very strange results if most of the worlds land lies near
		#---the equator


		#Sets the threshold for jungle rainfall by modifying the plains threshold by this factor.
		self.TreeFactor = 1.4

		#This is the maximum chance for a tree to be placed when rainfall is above jungle level.
		#use a value between 0.0 and 1.0
		self.MaxTreeChance = 0.8

		#Percentages of hot flat Grassland, cool flat Grassland, and Tundra squares wet enough to be Marsh.
		#The first category replaces Jungle tiles, and the last category represents summer melting.
		self.HotMarshPercent  = 0.04
		self.MidMarshPercent  = self.HotMarshPercent * 2.0
		self.ColdMarshPercent = self.MidMarshPercent * 0

		#Chance Mushrooms will appear. A tile must be either Grassland, or Tundra with Grassland rainfall,
		#and not already have been given a Marsh.
		self.MushroomChance = 0.03
		self.Soil1Chance = 0.02
		self.Soil2Chance = 0.02

		#Chance an Oasis will appear. A tile must be Desert, not be near another Oasis, and not be next to any
		#non-Desert tiles. (Desert Lakes and Desert Peaks are allowed.)
		self.OasisPercent   = 0.3
		self.OasisMinChance = 0.1
		self.OasisMaxChance = 1.0

		#Chance Scrub will appear. A tile must be Desert, and not be directly next to any water tiles.
		self.ScrubPercent   = 0.10
		self.ScrubMinChance = 0.10
		self.ScrubMaxChance = 0.80

		#The percent chance that Coral will appear in a Coast tile in the tropical latitudes, and twice
		#the percent chance it will appear in an Ocean tile in the temperate and subpolar latitudes. Real reef chance is self.ReefChance-self.IslandChance!
		self.ReefChance = 0.09
		self.IslandChance = 0.03

		#How many squares are added to a lake for each unit of drainage flowing
		#into it.
		self.LakeSizePerDrainage = 14.0

		#This value modifies LakeSizePerRiverLength when a lake begins in desert
		self.DesertLakeModifier = .60

		#This value controls the amount of siltification in lakes
		self.maxSiltPanSize = 200

		#This value controls the number of mid-altitude lake depressions per
		#map square. It will become a lake if enough water flows into the
		#depression.
		self.numberOfLakesPerPlot = 0.003

		#This value sets the minimum altitude of lake depressions. They
		#generally look better higher up.
		self.minLakeAltitude = 0.45
				
		#This value is used to decide if enough water has accumulated to form a river.
		#A lower value creates more rivers over the entire map.
		self.RiverThreshold = 4
		
		#The percent chance that an oasis may appear in desert. A tile must be desert and
		#surrounded on all sides by desert.
		self.OasisChance = .25

		# The chance out of 1000 that we have a goody hut on a desert 
		# (either flat or hill) square
		self.desertHutChance = 37 # 3.7 percent
		
		# The chance out of 1000 we will have a goody hut on a non-desert
		# non-ice land (flat/hill) square
		self.normalHutChance = 25 # 2.5 percent

		#This sets the amount of heat lost at the highest altitude. 1.0 loses all heat
		#0.0 loses no heat.
		self.heatLostAtOne = 1.0
		
		#This value is an exponent that controls the curve associated with
		#temperature loss. Higher values create a steeper curve.
		self.temperatureLossCurve = 1.3
		
		#Degrees latitude for the top and bottom of the map. This allows
		#for more specific climate zones
		self.topLatitude = 90
		self.bottomLatitude = -90

		#Horse latitudes and polar fronts plus and minus in case you
		#want some zones to be compressed or emphasized.
		self.horseLatitude = 30
		self.polarFrontLatitude = 60

		#Tropics of Cancer and Capricorn plus and minus respectively
		#self.tropicsLatitude = 23

		#Oceans are slow to gain and lose heat, so the max and min temps
		#are reduced and raised by this much.
		self.oceanTempClamp = .10

		#Minimum amount of rain dropped by default before other factors
		#add to the amount of rain dropped
		self.minimumRainCost = 0.01

		#Strength of geostrophic rainfall versus monsoon rainfall
		self.geostrophicFactor = 6.0

		#Monsoon uplift factor. This value is an ajustment so that monsoon uplift
		#matches geostrophic uplift.
		self.monsoonUplift = 500.0
		
		#Option to divide map into two continents as far as the midpoint
		#displacement is concerned. For guaranteed continent separation, further
		#steps will be needed but this option will cause more ocean in the
		#middle of the map. The possible choices are 0 = NO_SEPARATION,
		#1 = NORTH_SOUTH_SEPARATION and 2 = EAST_WEST_SEPARATION.
		self.hmSeparation = 0

		#Creates a water margin around the map edges. 
		self.northMargin = False
		self.southMargin = False
		self.eastMargin = False
		self.westMargin = False

		#If you sink the margins all the way to 0.0, they become too obvious.
		#This variable sets the maximum amount of sinking
		self.hmMarginDepth = 0.60

		#Margin of ocean around map edge when not wrapping and also through
		#middle when using separation.
		self.hmGrainMargin = 2

		#These are not mountain peaks, but points on the height map initialized
		#to 1.0 before the midpoint displacement process begins. This sets the
		#percentage of 'peaks' for points that are not on the grain margin.
		self.hmInitialPeakPercent = 0.30
		
		#Scales the heuristic for random midpoint displacement. A higher number
		#will create more noise(bumpy), a smaller number will make less
		#noise(smooth).
		self.hmNoiseLevel = 2.0

		#Influence of the plate map, or how much of it is added to the height map.
		self.plateMapScale = 1.1

		#Minimun distance from one plate seed to another
		self.minSeedRange = 15

		#Minimum distance from a plate seed to edge of map
		self.minEdgeRange = 5

		#Chance for plates to grow. Higher chance tends to make more regular
		#shapes. Lower chance makes more irregular shapes and takes longer.
		self.plateGrowthChanceX = 0.3
		self.plateGrowthChanceY = 0.3

		#This sets the amount that tectonic plates differ in altitude.
		self.plateStagger = 0.1

		#This sets the max amount a plate can be staggered up to on the heightmap
		self.plateStaggerRange = 1.0

		#This is the chance for a plate to sink into the water when it is on map edge
		self.chanceForWaterEdgePlate = 0.45
		
		#This is the frequency of the cosine ripple near plate boundaries.
		self.rippleFrequency = 0.5

		#This is the amplitude of the ripples near plate boundaries.
		self.rippleAmplitude = 0.75

		#This is the amount of noise added to the plate map.
		self.plateNoiseFactor = 1.2

		#Filter size for temperature smoothing. Must be odd number
		self.filterSize = 15

		#Filter size for altitude smoothing and distance finding. Must be
		#odd number
		self.distanceFilterSize = 5

		#It is necessary to eliminate small inland lakes during the initial
		#heightmap generation. Keep in mind this number is in relation to
		#the initial large heightmap (mc.hmWidth, mc.hmHeight) before the
		#shrinking process
		self.minInlandSeaSize = 100

		#Too many meteors will simply destroy the Earth, and just
		#in case the meteor shower can't break the pangaea, this will also
		#prevent and endless loop.
		self.maximumMeteorCount = 15
		
		#Minimum size for a meteor strike that attemps to break pangaeas.
		#Don't bother to change this it will be overwritten depending on
		#map size.
		self.minimumMeteorSize = 6	  
		
		#---These values are for evaluating starting locations
		
		#Minimum number of hills in fat cross
		self.MinHillsInFC = 1

		#Max number of peaks in fat cross
		self.MaxPeaksInFC = 2

		#Max number of bad features(jungle) in fat cross
		self.MaxBadFeaturesInFC = 3

		#The following values are used for assigning starting locations. For now,
		#they have the same ratio that is found in CvPlot::getFoundValue
		self.CommerceValue = 20
		self.ProductionValue = 20
		self.FoodValue = 30

		#Coastal cities are important, how important is determined by this
		#value.
		self.CoastalCityValueBonus = 1.1

		#River side cities are also important, how important is determined by this
		#value.
		self.RiverCityValueBonus = 1.2
		
		#Hill cities are important, how important is determined by this value.
		self.HillCityValueBonus = 1.1
		
		#Decides whether to use the Python random generator or the one that is
		#intended for use with civ maps. The Python random has much higher precision
		#than the civ one. 53 bits for Python result versus 16 for getMapRand. The
		#rand they use is actually 32 bits, but they shorten the result to 16 bits.
		#However, the problem with using the Python random is that it may create
		#syncing issues for multi-player now or in the future, therefore it must
		#be optional.
		self.UsePythonRandom = True		
		
		##############################################################################
		## Fuyu Settings
		##############################################################################

		#This variable adjusts the maximun number of identical bonuses to be placed in a
		#single group. People tend not to like all instances of a bonus type to be found within
		#a single 3x3 area. When set to -1 (default), the maximum group size is between 3 and 6,
		#based on WorldSize. When set to 0, the maximum group size is a random number between
		# zero and (number of players). When set to 1, this will disable all bonus grouping.
		self.BonusMaxGroupSize = -1

		#Randomly allows strategic bonuses to be used to sweeten starting positions.
		#(Chance per starting position to allow 1 Classical Era or earlier strategic resource)
		self.allowWonderBonusChance = 0.0

		#Randomly allows bonuses with continent limiter to be used to sweeting starting positions.
		#(Chance per attempt to place an area-restricted resource in the wrong area)
		self.ignoreAreaRestrictionChance = 0.0
		
		#Below here are static defines. If you change these, the map won't work.
		#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		self.L = 0
		self.N = 1
		self.S = 2
		self.E = 3
		self.W = 4
		self.NE = 5
		self.NW = 6
		self.SE = 7
		self.SW = 8

		self.NO_SEPARATION = 0
		self.NORTH_SOUTH_SEPARATION = 1
		self.EAST_WEST_SEPARATION = 2

		# THESE DO NOT CHANGE ANYTHING.  They are overwritten by
		# mmap.getGridWidth() and mmap.getGridHeight()
		self.width = 104
		self.height = 64

		# These should probably not be changed...
		self.OCEAN = 0
		self.LAND = 1
		self.HILLS = 2
		self.PEAK = 3

		self.OCEAN = 0
		self.COAST = 1
		self.MARSH = 2
		self.GRASS = 3
		self.PLAINS = 4
		self.DESERT = 5
		self.TUNDRA = 6
		self.SNOW = 7

		self.minimumLandInChoke = 0.5

		return
	
	def initInGameOptions(self):
		gc = CyGlobalContext()
		mmap = gc.getMap()

		# Sea level comes from preferences
		try:
			seaLevel = int(mmap.getSeaLevel())
		except:
			seaLevel = 1
		self.landPercent = 0.29
		if seaLevel == 0:
			self.landPercent = 0.43
		elif seaLevel == 2:
			self.landPercent = 0.19

		self.serviceFlags = 0 # Used for concise description of flags
		if(seaLevel != 0):
			self.serviceFlags |= (seaLevel & 3) # 2 bits; total 2
		else:
			self.serviceFlags |= 3 # Make sure Service Tag is always 21 digits
		  
		# Have climate affect the maps 
		# This is increased for a "tropical" climate
		self.tropicsLatitude = 23
 
		# These are increased for "rocky" climates
		#How many land squares will be above peak threshold and thus 'peaks'.
		self.PeakPercent = 0.12

		#How many land squares will be above hill threshold and thus 'hills' 
		#unless hey are also above peak threshold in which case they will 
		#be 'peaks'.
		self.HillPercent = 0.35
		
		#In addition to the relative peak and hill generation, there is also a
		#process that changes flats to hills or peaks based on altitude. This tends
		#to randomize the high altitude areas somewhat and improve their appearance.
		#These variables control the frequency of hills and peaks at the highest altitude.
		self.HillChanceAtOne = .50
		self.PeakChanceAtOne = .27

		#How many land squares will be below desert rainfall threshold. In this case,
		#rain levels close to zero are very likely to be desert, while rain levels close
		#to the desert threshold will more likely be plains.
		self.DesertPercent = 0.15

		#How many land squares will be below plains rainfall threshold. Rain levels close
		#to the desert threshold are likely to be plains, while those close to the plains
		#threshold are likely to be grassland. 
		self.PlainsPercent = 0.42
		
		#What temperature will be considered cold enough to be ice. Temperatures range
		#from coldest 0.0 to hottest 1.0.
		self.SnowTemp = .25

		#What temperature will be considered cold enough to be tundra. Temperatures range
		#from coldest 0.0 to hottest 1.0.
		self.TundraTemp = .35

		#Hotter than this temperature will be considered deciduous forest, colder will
		#be evergreen forest.Temperatures range from coldest 0.0 to hottest 1.0.
		self.ForestTemp = .45

		#What temperature will be considered hot enough to be jungle. Temperatures range
		#from coldest 0.0 to hottest 1.0.
		self.JungleTemp = .60

		# Temperate: 0 Tropical: 1 Arid: 2 Rocky: 3 Cold: 4
		self.iceChance = 1.0 # Chance of having iceberg at top/bottom of map
		self.iceRange = 4 # Number of squares we add icebergs to
		self.iceSlope = 0.66 # How quickly we reduce icebergs
		clim = mmap.getClimate() 
		if clim == 1: # Tropical
			self.tropicsLatitude = 46
			# q3max changes
			self.DesertPercent = .10 # added
			self.PlainsPercent = .30 # added
			self.SnowTemp = .20 # added
			self.TundraTemp = .30 # added
			self.ForestTemp = .35 # added
			self.JungleTemp = .50 # added
			# End q3max changes
			self.iceSlope = 0.33 # Less ice
		elif clim == 2: # Arid
			self.DesertPercent = 0.40
			self.PlainsPercent = 0.82
			self.iceSlope = 0.33 # Less ice
		elif clim == 3: # Rocky
			self.PeakPercent = 0.24
			self.HillPercent = 0.70
			self.HillChanceAtOne = 0.70
			self.PeakChanceAtOne = 0.43
			self.iceSlope = 0.75 # Some more ice
			self.iceRange = 6
		elif clim == 4: # Cold
			self.tropicsLatitude = 0
			self.SnowTemp = .50
			self.TundraTemp = .75
			self.ForestTemp = .85
			self.JungleTemp = .99
			self.iceRange = 12
			self.iceChance = 1.2
			self.iceSlope = 0.87 # Lots of ice
		
		self.serviceFlags <<= 3
		self.serviceFlags |= (clim & 7) # 3 bits; total 5
	  
		#New World Rules
		selectionID = mmap.getCustomMapOption(OPTION_NewWorld)
		self.AllowNewWorld = True
		self.ShareContinent = False
		if selectionID == 1:
			self.AllowNewWorld = False
		elif selectionID == 2:
			self.ShareContinent = True

		self.xtraFlags = 0
		self.xtraFlags |= ((self.ShareContinent & 1) << 4)

		self.serviceFlags <<= 1
		self.serviceFlags |= (self.AllowNewWorld & 1) # 1 bit; total 6

		#Pangaea Rules
		selectionID = mmap.getCustomMapOption(OPTION_Pangaea)
		self.AllowPangeas = False
		if selectionID == 1:
			self.AllowPangeas = True

		self.serviceFlags <<= 1
		self.serviceFlags |= (self.AllowPangeas & 1) # 1 bit; total 7

		# How long are they willing to wait for the map to be made
		patience = mmap.getCustomMapOption(OPTION_Patience)
		patience += 1 # Patience at 0 is broken

		# This allows me to have one final usable bit in the service tag
		self.serviceFlags <<= 3
		self.serviceFlags |= (patience & 3) # 2 bits; total 10

		# The preset worlds have hard-coded values
		selectionID = mmap.getCustomMapOption(OPTION_MapSeed)

		# Disabled: we will only alter seed (it's now for debugging)
		#if selectionID != 0:
			#patience = 2
			#if selectionID != 3:
			#	self.landPercent = 0.29 # We will force this here too

		self.patience = patience
		#Size of largest map increment to begin midpoint displacement. Must
		#be a power of 2.
		self.hmMaxGrain = 2 ** (2 + patience)

		#Height and Width of main climate and height maps. This does not
		#reflect the resulting map size. Both dimensions( + 1 if wrapping in
		#that dimension = False) must be evenly divisble by self.hmMaxGrain
		# SAM:
		# Make it easy to change the size while keeping the aspect ratio
		# The bigger the size factor, the smaller the continents and the
		# slower the map generation process

		# X and Y values for the map's aspect ratio
		ratioValue = mmap.getCustomMapOption(OPTION_MapRatio)
		if 1 == 2: # Dummy, does nothing, so we don't get elif problems
			self.ratioX = 3
			self.ratioY = 2
		elif ratioValue == 0: # 2:3
			self.ratioX = 2
			self.ratioY = 3
		elif ratioValue == 1: # 1:1
			self.ratioX = 2
			self.ratioY = 2
		elif ratioValue == 2: # 3:2
			self.ratioX = 3
			self.ratioY = 2
		elif ratioValue == 3: # 2:1
			self.ratioX = 4
			self.ratioY = 2
		elif ratioValue == 4: # 7:1, Ringworld 
			self.ratioX = 7
			self.ratioY = 1
		elif ratioValue == 5: # 3:3, Big square (untested)
			self.ratioX = 3
			self.ratioY = 3
		elif ratioValue == 6: # 3:2 but twice the size
			self.ratioX = 6
			self.ratioY = 4
		elif ratioValue == 7: # 1:2; down here because it's buggy
			self.ratioX = 2
			self.ratioY = 4

		if patience < 2:
			self.ratioX = 3 # One less thing to SQA
			self.ratioY = 2

		self.serviceFlags <<= 3
		self.serviceFlags |= (ratioValue & 7) # 3 bits; total 13

		selectionID = mmap.getCustomMapOption(OPTION_IslandFactor)

		self.serviceFlags <<= 2
		self.serviceFlags |= (selectionID & 3) # Island factor

		# If they want a fast map, don't allow them to select more islands
		if (patience < 2):
			selectionID = 0

		heightmap_size_factor = 3 + selectionID
		self.hmWidth  = (self.hmMaxGrain * self.ratioX * 
						 heightmap_size_factor)
		self.hmHeight = (self.hmMaxGrain * self.ratioY * 
						 heightmap_size_factor) + 1

		# These are expressed in 4x4 "Grid" units
		self.maxMapWidth = int(self.hmWidth / 4)
		self.maxMapHeight = int(self.hmHeight / 4)
			 
		#Wrap options
		selectionID = mmap.getCustomMapOption(OPTION_Wrap)
		wrapString = "Cylindrical"
		self.WrapX = True
		self.WrapY = False

		self.serviceFlags <<= 2 
		self.serviceFlags |= (selectionID & 3) # Map wrap; 2 bits total 15
		self.serviceFlags <<= 6 # 6 bits so we know the map size total 21

		# handicap of 0 means player is equal to AI and may get a 
		# starting position that can not be won at higher difficulty
		# settings.  Values of 1, 2, or 3 make it easier for the player
		handicap = mmap.getCustomMapOption(OPTION_Handicap)
		self.xtraFlags |= ((handicap & 3) << 5)
		
		#Bonus resources to add depending on difficulty settings
		self.SettlerBonus = handicap
		self.ChieftainBonus = handicap 
		self.WarlordBonus = handicap 
		self.NobleBonus = handicap 
		self.PrinceBonus = handicap 
		self.MonarchBonus = handicap 
		self.EmperorBonus = handicap 
		self.ImmortalBonus = handicap 
		self.DeityBonus = handicap 
		   
		# Now that we have calculated the player's bonus resources, how many
		# resources should the map as a whole have? 

		#This variable adjusts the amount of bonuses on the map. Values above 1.0 will add bonus
		#bonuses. People often want lots of bonuses, and for those people, this variable is definately
		#a bonus.
		self.BonusBonus = 1.0
		self.spreadResources = False 
		bonus_add = mmap.getCustomMapOption(OPTION_MapResources)
		if bonus_add == 1: # More evenly spread out
			self.BonusBonus = 0.7 # Compensate for spread's increase
			self.spreadResources = True # Increases resources
		if bonus_add == 2: # Full of resources
			self.BonusBonus = 1.5 # Increases resources
			self.spreadResources = True # Increases resources more
		self.xtraFlags |= ((bonus_add & 3) << 2)
		   
		self.noRotate = mmap.getCustomMapOption(OPTION_NoRotate)
		self.smoothPeaks = mmap.getCustomMapOption(OPTION_SmoothPeaks)
	 
		#After generating the heightmap, bands of ocean can be added to the map
		#to allow a more consistent climate generation. These bands are useful
		#if you are generating part of a world where the weather might be coming
		#in from off the map. These bands can be kept if needed or cropped off
		#later in the process.
		self.northWaterBand = 10
		self.southWaterBand = 10
		self.eastWaterBand = 0
		self.westWaterBand = 0
		#These variables are intended for use with the above water band variables
		#but you can crop the map edge after climate generation for any reason.
		self.northCrop = 10
		self.southCrop = 10
		self.eastCrop = 0
		self.westCrop = 0

		if selectionID == 1 or selectionID == 3: #Toroidal
			self.hmHeight -= 1
			self.WrapY = True
			if selectionID == 1:
				self.iceChance *= 0.1
			self.northWaterBand = 0
			self.northCrop = 0
			self.southWaterBand = 0
			self.southCrop = 0
			wrapString = "Toroidal"
		elif selectionID == 2: #Flat
			self.hmWidth += 1
			self.WrapX = False
			wrapString = "Flat"
	   
		# Random seed options (fixed or random)
		selectionID = mmap.getCustomMapOption(OPTION_MapSeed)
		mapRString = "Random"
		self.totestra = 0 
		if selectionID == 1: 
			self.totestra = 8 
		elif selectionID == 2: 
			self.totestra = 5  
		elif selectionID == 3: 
			self.totestra = 10 
		elif selectionID == 4: 
			self.totestra = 285 # Could use more rivers
		elif selectionID == 5:
			self.totestra = 324 # Could use more rivers
		elif selectionID == 6:
			self.totestra = 2997 # Really nice
		elif selectionID == 7:
			self.totestra = 4677 # Could use more rivers
		elif selectionID == 8:
			self.totestra = 7187 # Small but fun
		elif selectionID == 9:
			self.totestra = 8207 # It's a Chili pepper!
		elif selectionID == 10:
			self.totestra = 12244 # Very small and fun
		elif selectionID == 11:
			self.totestra = 14194
		# Force all fixed-seed maps to be 3:2, because the seeds are
		# calibrated to make reasonably good maps at that ratio
		if selectionID != 0: 
			self.ratioX = 3
			self.ratioY = 2
			self.hmWidth  = (self.hmMaxGrain * self.ratioX * heightmap_size_factor)
			self.hmHeight = (self.hmMaxGrain * self.ratioY * heightmap_size_factor) + 1
			self.maxMapWidth = int(self.hmWidth / 4)
			self.maxMapHeight = int(self.hmHeight / 4)
			self.WrapX = True
			self.WrapY = False

		#Number of tectonic plates
		self.hmNumberOfPlates = int(float(self.hmWidth * self.hmHeight) * 0.0016)
		if patience == 0:
			self.hmNumberOfPlates = int(float(self.hmWidth * self.hmHeight) * 0.0032)
		elif patience == 1:
			self.hmNumberOfPlates = int(float(self.hmWidth * self.hmHeight) * 0.0024)
		elif patience == 3:
			self.hmNumberOfPlates = int(float(self.hmWidth * self.hmHeight) * 0.0008)
		elif patience == 4:
			self.hmNumberOfPlates = int(float(self.hmWidth * self.hmHeight) * 0.0004)
		elif patience >= 5:
			self.hmNumberOfPlates = int(float(self.hmWidth * self.hmHeight) * 0.0002)

		self.optionsString = "Map Options: \n"
		if self.AllowNewWorld:
			self.optionsString += "AllowNewWorld = true\n"
		else:
			self.optionsString += "AllowNewWorld = false\n"
		if self.AllowPangeas:
			self.optionsString += "AllowPangeas = true\n"
		else:
			self.optionsString += "AllowPangeas = false\n"
		self.optionsString += "Wrap Option = " + wrapString + "\n"
		self.optionsString += "Map world = " + mapRString + "\n" 
		self.optionsString += "Land percent = " + str(self.landPercent) + "\n"
		self.optionsString += "RatioX = " + str(self.ratioX) + "\n"
		self.optionsString += "RatioY = " + str(self.ratioY) + "\n"
		self.optionsString += "Climate = " + str(clim) + "\n"
		self.optionsString += "Patience = " + str(patience) + "\n"
		self.optionsString += "Island factor = " + str(heightmap_size_factor) +"\n" 

		print str(self.optionsString) + "\n" 
		return
	

# Class RadioGatun32 is under different copyright:
# Copyright (c) 2012-2017 Sam Trenholme
# 
# TERMS
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#	notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#	notice, this list of conditions and the following disclaimer in the
#	documentation and/or other materials provided with the distribution.
#
# This software is provided 'as is' with no guarantees of correctness or
# fitness for purpose.

# This is a Python implementation of RadioGatun32.  It takes about 10
# seconds to set up the RNG, then it can output approximately
# 30,000 16-bit random numbers per second on a Core i5-2430M

# There is another open-source Python RadioGatun implementation here:
# https://github.com/doegox/python-cryptoplus

# I would like to thank Lorenzo for his suggestion to use xrange to speed up
# the program

class RadioGatun32:
	def __init__(self, m):
		self.wordsize = 32
		self.millsize = 19
		self.beltrows = 3
		self.beltcol = 13
		self.beltfeed = 12
		self.mask = 0xffffffff # 32-bit
		self.index = 0
		(self.a, self.b) = self.seed(str(m))
	def mill(self,a):
		aa = []
		for g in xrange(self.millsize):
			aa.append(0)
		x = 0
		i = 0
		y = 0
		r = 0
		z = 0
		for i in xrange(self.millsize):
			y = (i * 7) % self.millsize
			r = ((i * (i + 1)) / 2) % self.wordsize
			x = a[y] ^ (a[ ((y + 1) % self.millsize) ] |
				(a[ ((y + 2) % self.millsize) ] ^ self.mask))
			aa[i] = ((x >> r) | (x << (self.wordsize - r))
					& self.mask)
		for i in xrange(self.millsize):
			y = i
			r = (i + 1) % self.millsize
			z = (i + 4) % self.millsize
			a[i] = aa[y] ^ aa[r] ^ aa[z]
		a[0] ^= 1
		return a
	def belt(self,a,b):
		q = []
		for g in xrange(self.beltrows):
			q.append(0)
		s = 0	
		i = 0
		v = 0
		for s in xrange(self.beltrows):
			q[s] = b[((s * self.beltcol) + self.beltcol - 1)]
		i = self.beltcol - 1
		while i > 0:
			for s in xrange(self.beltrows):
				v = i - 1
				if v < 0:
					v = self.beltcol - 1
				b[((s * self.beltcol) + i)] = (
					b[((s * self.beltcol) + v)])
			i -= 1
		for s in xrange(self.beltrows):
			b[(s * self.beltcol)] = q[s]
		for i in xrange(self.beltfeed):
			s = (i + 1) + ((i % self.beltrows) * self.beltcol)
			b[s] ^= a[(i + 1)]
		a = self.mill(a)
		for i in xrange(self.beltrows):
			a[(i + self.beltcol)] ^= q[i]
		return (a, b)
	def seed(self,m):
		p = []
		for g in xrange(3):
			p.append(0)
		q = 0
		c = 0
		r = 0
		done = 0
		index = 0
		counter = 0
		a = []
		b = []
		for g in xrange(self.millsize):
			a.append(0)
		for g in xrange(self.beltrows * self.beltcol):
			b.append(0)
		for counter in xrange(16777218): # Infinite loop protection
			p[0] = p[1] = p[2] = 0
			for r in xrange(3):
				q = 0
				while q < self.wordsize:
					x = 0
					try:
						x = ord(m[index])
					except:
						x = 1
					index += 1
					if(index > len(m)):
						done = 1
						x = 1
					p[r] |= x << q
					if done == 1:
						for c in xrange(3):
							b[c * 13] ^= p[c]
							a[16 + c] ^= p[c]
						(a,b) = self.belt(a,b)
						for c in xrange(16):	
							(a,b) = self.belt(a,b)
						return (a,b)
					q += 8
			for c in xrange(3):
				b[c * 13] ^= p[c]
				a[16 + c] ^= p[c]
			(a,b) = self.belt(a,b)
		return (a,b) # We should never get here
	# Return 16-bit random integer (between 0 and 65535)
	def rng16(self):
		if (self.index % 4) == 0:
			(self.a, self.b) = self.belt(self.a, self.b)
			self.index += 1
			return (((self.a[1] & 0xff) << 8) | 
				 ((self.a[1] & 0xff00) >> 8))
		self.index += 1
		if (self.index % 4) == 2:
			return(((self.a[1] & 0xff0000) >> 8) |
				((self.a[1] & 0xff000000) >> 24))
		elif (self.index % 4) == 3:
			return(((self.a[2] & 0xff) << 8) |
				((self.a[2] & 0xff00) >> 8))
		elif (self.index % 4) == 0:
			return(((self.a[2] & 0xff0000) >> 8) |
				((self.a[2] & 0xff000000) >> 24))
		else: # Should never get here
			return -1
	# Return 32-bit random integer
	def rng32(self):
		if(self.index & 1):
			self.index += 1
		self.index &= 2
		if(self.index):
			self.index = 0
			return (((self.a[2] & 0xff) << 24) |
				((self.a[2] & 0xff000000) >> 24) |
				((self.a[2] & 0xff00) << 8) |
				((self.a[2] & 0xff0000) >> 8))
		(self.a, self.b) = self.belt(self.a, self.b)
		self.index = 2
		return (((self.a[1] & 0xff) << 24) |
			((self.a[1] & 0xff000000) >> 24) |
			((self.a[1] & 0xff00) << 8) |
			((self.a[1] & 0xff0000) >> 8))
	# Return 64-bit random integer
	def rng64(self):
		left = self.rng32()
		right = self.rng32()
		return ((left << 32) | right)
	# Return number between 0 (can be 0) and 1 (can be slightly smaller
	# than 1 but never 1)
	def random(self):
		return float(self.rng64()) / 18446744073709551616
	# Return a number between a and b
	def randint(self, low, high):
		if(low == high):
			return low
		if(high < low):
			swap = low
			low = high
			high = swap
		range = 1 + high - low	
		# For low ranges, we can use 16-bit ints to get number
		if(range <= 10000):
			max = 65536 - (65536 % range)
			number = max
			while number >= max:
				number = self.rng16()
			return low + (number % range)
		# int() returns the floor, e.g. int(1.99999) returns 1
		return int(low + (self.random() * range))

def do_rg32_test(testInput):
	# 16 16-bit numbers
	rg32test = RadioGatun32(testInput)
	line = "16-bit:	"
	for a in range(16):
		line += ("%04x" % (rg32test.rng16()))
	print(line)
	# 8 32-bit numbers
	rg32test = RadioGatun32(testInput)
	line = "32-bit:	"
	for a in range(8):
		line += ("%08x" % (rg32test.rng32()))
	print(line)
	# 4 64-bit numbers
	rg32test = RadioGatun32(testInput)
	line = "64-bit:	"
	for a in range(4):
		line += ("%016x" % (rg32test.rng64()))
	print(line)
	# 16-bit then 32-bit
	rg32test = RadioGatun32(testInput)
	line = "16/32 bit: "
	for a in range(4):
		line += ("%04x" % (rg32test.rng16()))
		line += "----"
		line += ("%08x" % (rg32test.rng32()))
	print(line)
	# 32-bit then 16-bit
	rg32test = RadioGatun32(testInput)
	line = "32/16 bit: "
	for a in range(4):
		line += ("%08x" % (rg32test.rng32()))
		line += ("%04x" % (rg32test.rng16()))
		line += "----"
	print(line)
	# Mix it up (16,16,32,64,64,32,16,16)
	rg32test = RadioGatun32(testInput)
	line = "Mix it up: "
	line += ("%04x" % (rg32test.rng16()))
	line += ("%04x" % (rg32test.rng16()))
	line += ("%08x" % (rg32test.rng32()))
	line += ("%016x" % (rg32test.rng64()))
	line += ("%016x" % (rg32test.rng64()))
	line += ("%08x" % (rg32test.rng32()))
	line += ("%04x" % (rg32test.rng16()))
	line += ("%04x" % (rg32test.rng16()))
	print(line)

##### END BSD LICENSED CODE ##############################################

mc = MapConstants()


def beforeGeneration():
	print "-- beforeGeneration()"

	# Create mapInfo string - this should work for all maps
	mapInfo = ""
	for opt in range( getNumCustomMapOptions() ):
		nam = getCustomMapOptionName( [opt] )
		sel = map.getCustomMapOption( opt )
		txt = getCustomMapOptionDescAt( [opt,sel] )
		mapInfo += "%27s:   %s\n" % ( nam, txt )

	# Initialize MapScriptTools
	mst.getModInfo( getVersion(), None, mapInfo, bNoSigns=False )

	# Initialize MapScriptTools.BonusBalancer
	# - balance boni, place missing boni, move minerals, longer balancing range
	balancer.initialize( True, True, True, True )

class PythonRandom :
	def __init__(self):
		self.rg32 = RadioGatun32('12345678')
		return
	def seed(self):
		#Python randoms are not usable in network games.
		if mc.UsePythonRandom:
			self.usePR = True
		else:
			self.usePR = False
		if not IsStandAlone and self.usePR and CyGame().isNetworkMultiPlayer():
			print "Detecting network game. Setting UsePythonRandom to False."
			self.usePR = False
		if self.usePR:
			seed() #Start with system time
			if (mc.totestra == 0):
				seedValue = "R"
				seedletter="abcdefghijkl7nopqrstuv8xyz" # No wide letters
				for seedMake in range(12):
					seedMe = randint(0,25)
					seedValue += seedletter[seedMe:seedMe+1]
				self.seedString = "Random seed (Using Python rands) for this map is " + seedValue
			else:
				seedValue = "RT" + str(mc.totestra)
				self.seedString = "Fixed seed (Using Python rands) for this map is " + seedValue
			mc.serviceTag = 0
			mc.serviceTag |= (mc.serviceFlags << 60)
			mc.serviceTag |= (mc.xtraFlags << 53)
			if(mc.noRotate == 0):
				mc.serviceTag |= (1 << 83)
			if(mc.smoothPeaks == 1):
				mc.serviceTag |= (1 << 75)
			mc.serviceTag |= (a91a15d7(mc.serviceTag) << 53)
			mc.serviceTag >>= 52
			mc.serviceString = ("%x" % mc.serviceTag)
			mc.serviceString += seedValue
			print "SERVICE TAG: " + mc.serviceString 
			self.rg32 = RadioGatun32(seedValue)
			
		else:
			gc = CyGlobalContext()
			self.mapRand = gc.getGame().getMapRand()
			
			seedValue = self.mapRand.get(65535,"Seeding mapRand - FairWeather.py")
			self.mapRand.init(seedValue)
			self.seedString = "Random seed (Using getMapRand) for this map is %(s)20d" % {"s":seedValue}			
			
##			seedValue = 56870
##			self.mapRand.init(seedValue)
##			self.seedString = "Pre-set seed (Using getMapRand) for this map is %(s)20d" % {"s":seedValue}
			
		print str(self.seedString)
		return
	def random(self):
		if self.usePR:
			return self.rg32.random()
		else:
			#This formula is identical to the getFloat function in CvRandom. It
			#is not exposed to Python so I have to recreate it.
			fResult = float(self.mapRand.get(65535,"Getting float -FairWeather.py"))/float(65535)
#			print fResult
			return fResult
	def randint(self,rMin,rMax):
		#if rMin and rMax are the same, then return the only option
		if rMin == rMax:
			return rMin
		#returns a number between rMin and rMax inclusive
		if self.usePR:
			return self.rg32.randint(rMin,rMax)
		else:
			#mapRand.get() is not inclusive, so we must make it so
			return rMin + self.mapRand.get(rMax + 1 - rMin,"Getting a randint - FairWeather.py")
#Set up random number system for global access
PRand = PythonRandom()

################################################################################
## Global functions
################################################################################

def errorPopUp(message):
	gc = CyGlobalContext()
	iPlayerNum = 0
	for iPlayer in range(gc.getMAX_PLAYERS()):
		player = gc.getPlayer(iPlayer)
		if player.isAlive():
			iPlayerNum = iPlayerNum + 1
			if player.isHuman():
				text = message + "\n\n" + mc.optionsString + "\n" + PRand.seedString
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
				popupInfo.setText(text)
				popupInfo.setOnClickedPythonCallback("")
				popupInfo.addPythonButton("Ok","")
				popupInfo.addPopup(iPlayer)
				
#This function converts x and y to a one-dimensional index.
def GetIndex(x,y):
	#Check X for wrap
	if mc.WrapX == True:
		xx = x % mc.width
	elif x < 0 or x >= mc.width:
		return -1
	else:
		xx = x
	#Check y for wrap
	if mc.WrapY == True:
		yy = y % mc.height
	elif y < 0 or y >= mc.height:
		return -1
	else:
		yy = y

	i = yy * mc.width + xx
	return i

# This does the same thing for the height map (as opposed to the plot map)
def GetHmIndex(x,y):
	#Check X for wrap
	if mc.WrapX == True:
		xx = x % mc.hmWidth
	elif x < 0 or x >= mc.hmWidth:
		return -1
	else:
		xx = x
	#Check y for wrap
	if mc.WrapY == True:
		yy = y % mc.hmHeight
	elif y < 0 or y >= mc.hmHeight:
		return -1
	else:
		yy = y

	i = yy * mc.hmWidth + xx
	return i

#Handles arbitrary size
def GetIndexGeneral(x,y,width,height):
	#Check X for wrap
	if mc.WrapX == True:
		xx = x % width
	elif x < 0 or x >= width:
		return -1
	else:
		xx = x
	#Check y for wrap
	if mc.WrapY == True:
		yy = y % height
	elif y < 0 or y >= height:
		return -1
	else:
		yy = y

	i = yy * width + xx
	return i

#This function scales a float map so that all values are between
#0.0 and 1.0.
def NormalizeMap(fMap,width,height):
	#find highest and lowest points
	maxAlt = 0.0
	minAlt = 0.0
	for y in range(height):
		for x in range(width):
			plot = fMap[GetIndexGeneral(x,y,width,height)]
			if plot > maxAlt:
				maxAlt = plot
			if plot < minAlt:
				minAlt = plot
	#normalize map so that all altitudes are between 1 and 0
	#first add minAlt to all values if necessary
	if minAlt < 0.0:
		for y in range(height):
			for x in range(width):
				fMap[GetIndexGeneral(x,y,width,height)] -= minAlt
	#add minAlt to maxAlt also before scaling entire map
	maxAlt -= minAlt
	scaler = 1.0/maxAlt
	for y in range(height):
		for x in range(width):
			fMap[GetIndexGeneral(x,y,width,height)] = fMap[GetIndexGeneral(x,y,width,height)] * scaler			  
	return

# This takes a large map and scales it to make it smaller
def ShrinkMap(largeMap,lWidth,lHeight,sWidth,sHeight):

	smallMap = array('d')
	for y in range(sHeight):
		for x in range(sWidth):
			smallMap.append(0)

	# If the "small" map is, in fact, bigger, repeat the "large" map
	# This looks **REALLY BAD** and should not be done
	if(sWidth > lWidth and sHeight > lHeight):
		for x in range(sWidth):
			for y in range(sHeight):
				smallMap[GetIndexGeneral(x,y,sWidth,sHeight)] = (largeMap[GetIndexGeneral(x % lWidth,y % lHeight, lWidth, lHeight)])
		return smallMap

	#Scale down a large map down to a small map
	yScale = float(lHeight)/float(sHeight)
	xScale = float(lWidth)/float(sWidth)
	for y in range(sHeight):
		for x in range(sWidth):
##			print "x = %d, y = %d" % (x,y)
			weights = 0.0
			contributors = 0.0
			yyStart = int(y * yScale)
			yyStop = int((y + 1) * yScale)
			if yyStop < ((y + 1) * yScale):
				yyStop += 1
			for yy in range(yyStart,yyStop):
				xxStart = int(x * xScale)
				xxStop = int((x + 1) * xScale)
				if xxStop < ((x + 1) * xScale):
					xxStop += 1
				for xx in range(xxStart,xxStop):
##					print "  xx = %d, yy = %d" % (xx,yy)
					weight = GetWeight(x,y,xx,yy,xScale,yScale)
##					print "  weight = %f" % weight
					i = yy * lWidth + xx
##					print "  i = %d" % i
					contributor = largeMap[i]
##					print "  contributer = %f" % contributor
					weights += weight
					contributors += weight * contributor
##			print " final height = %f" % (contributors/weights)		
			#smallMap.append(contributors/weights)
			smallMap[GetIndexGeneral(x,y,sWidth,sHeight)] = (contributors/weights)
			#smallMap.append(contributors/weights)
					
	return smallMap

def GetWeight(x,y,xx,yy,xScale,yScale):
	xWeight = 1.0
##	print "   xScale = %f" % xScale
##	print "   x * xScale = %f, xx = %f" % ((x * xScale),xx)
	if float(xx) < x * xScale:
##		print "   first"
		xWeight = 1.0 - ((x * xScale) - float(xx))
	elif float(xx + 1) > (x + 1) * xScale:
##		print "   second"
		xWeight = ((x + 1) * xScale) - float(xx)
##	print "   xWeight = %f" % xWeight
		
	yWeight = 1.0
##	print "   yScale = %f" % yScale
##	print "   y * yScale = %f, yy = %f" % ((y * yScale),yy)
	if float(yy) < y * yScale:
##		print "   first"
		yWeight = 1.0 - ((y * yScale) - float(yy))
	elif float(yy + 1) > (y + 1) * yScale:
##		print "   second"
		yWeight = ((y + 1) * yScale) - float(yy)
##	print "   yWeight = %f" % yWeight
		
	return xWeight * yWeight

def CropMap(theMap):
	newMap = array('d')
	for y in range(mc.hmHeight):
		if y < mc.southCrop or y >= mc.hmHeight - mc.northCrop:
			continue
		for x in range(mc.hmWidth):
			if x < mc.westCrop or x >= mc.hmWidth - mc.eastCrop:
				continue
			i = GetHmIndex(x,y)
			newMap.append(theMap[i])
	return newMap

def AngleDifference(a1,a2):
	diff = a1 - a2
	while(diff < -180.0):
		diff += 360.0
	while(diff > 180.0):
		diff -= 360.0
	return diff
def AppendUnique(theList,newItem):
	if IsInList(theList,newItem) == False:
		theList.append(newItem)
	return

def IsInList(theList,newItem):
	itemFound = False
	for item in theList:
		if item == newItem:
			itemFound = True
			break
	return itemFound

def DeleteFromList(theList,oldItem):
	for n in range(len(theList)):
		if theList[n] == oldItem:
			del theList[n]
			break
	return  
	
def ShuffleList(theList):
		preshuffle = list()
		shuffled = list()
		numElements = len(theList)
		for i in range(numElements):
			preshuffle.append(theList[i])
		for i in range(numElements):
				n = PRand.randint(0,len(preshuffle)-1)
				shuffled.append(preshuffle[n])
				del preshuffle[n]
		return shuffled
	
def GetInfoType(string):
	cgc = CyGlobalContext()
	return cgc.getInfoTypeForString(string)
	
def GetDistance(x,y,dx,dy):
	distance = math.sqrt(abs((float(x - dx) * float(x - dx)) + (float(y - dy) * float(y - dy))))
	return distance

def GetOppositeDirection(direction):
	opposite = mc.L
	if direction == mc.N:
		opposite = mc.S
	elif direction == mc.S:
		opposite = mc.N
	elif direction == mc.E:
		opposite = mc.W
	elif direction == mc.W:
		opposite = mc.E
	elif direction == mc.NW:
		opposite = mc.SE
	elif direction == mc.SE:
		opposite = mc.NW
	elif direction == mc.SW:
		opposite = mc.NE
	elif direction == mc.NE:
		opposite = mc.SW
	return opposite

def GetXYFromDirection(x,y,direction):
	xx = x
	yy = y
	if direction == mc.N:
		yy += 1
	elif direction == mc.S:
		yy -= 1
	elif direction == mc.E:
		xx += 1
	elif direction == mc.W:
		xx -= 1
	elif direction == mc.NW:
		yy += 1
		xx -= 1
	elif direction == mc.NE:
		yy += 1
		xx += 1
	elif direction == mc.SW:
		yy -= 1
		xx -= 1
	elif direction == mc.SE:
		yy -= 1
		xx += 1
	return xx,yy	

##This function is a general purpose value tuner. It finds a value that will be greater
##than or less than the desired percent of a whole map within a given tolerance. Map values
##should be between 0 and 1. To exclude parts of the map, set them to value 0.0
def FindValueFromPercent(mmap,width,height,percent,tolerance,greaterThan):
	inTolerance = False
	#to speed things up a little, lets take some time to find the middle value
	#in the dataset and use that to begin our search
	minV = 100.0
	maxV = 0.0
	totalCount = 0
	for i in range(height*width):
		if mmap[i] != 0.0:
			totalCount += 1
			if minV > mmap[i]:
				minV = mmap[i]
			if maxV < mmap[i]:
				maxV = mmap[i]
	mid = (maxV - minV)/2.0 + minV
	overMinCount = 0
	equalMinCount = 0
	for i in range(height*width):
		if mmap[i] > minV:
			overMinCount += 1
		elif mmap[i] == minV:
			equalMinCount += 1
##	print "--------------------------------------------------------------"
##	print "totalCount = %d" % totalCount
##	print "overMinCount = %d" % overMinCount
##	print "equalMinCount = %d" % equalMinCount
##	print "starting threshold = %f" % mid
##	print "desired percent = %f" % percent
##	print "minV = %f, maxV = %f" % (minV,maxV)
	
	threshold = mid
	thresholdChange = mid
	iterations = 0
	lastAdded = False
	while not inTolerance:
		iterations += 1
		if(iterations > 500):
			print "can't find value within tolerance, end value = "
			print "threshold = %f, thresholdChange = %f" % (threshold, thresholdChange)
			break #close enough
		matchCount = 0
		for i in range(height*width):
			if mmap[i] != 0.0:
				if greaterThan == True:
					if(mmap[i] > threshold):
						matchCount += 1
				else:
					if(mmap[i] < threshold):  
						matchCount += 1
##		print "current threshold = %f" % threshold
##		print "current thresholdChange = %f" % thresholdChange
##		print "matchCount = %d" % matchCount
		currentPercent = float(matchCount)/float(totalCount)
##		print "currentPercent = %f" % currentPercent
		if currentPercent < percent + tolerance and \
		   currentPercent > percent - tolerance:
			inTolerance = True
		elif greaterThan == True:
			if currentPercent < percent:
##				print "threshold subtract"
				threshold -= thresholdChange
				if lastAdded:
					#only cut thresholdChange when direction is changed
					thresholdChange = thresholdChange/2.0
				lastAdded = False
			else:
##				print "threshold add"
				threshold += thresholdChange
				if not lastAdded:
					thresholdChange = thresholdChange/2.0
				lastAdded = True
		else:
			if currentPercent > percent:
##				print "threshold subtract"
				threshold -= thresholdChange
				if lastAdded:
					#only cut thresholdChange when direction is changed
					thresholdChange = thresholdChange/2.0
				lastAdded = False
			else:
##				print "threshold add"
				threshold += thresholdChange
				if not lastAdded:
					thresholdChange = thresholdChange/2.0
				lastAdded = True
##		print "--------------"

		#at this point value should be in tolerance or close to it
##	print "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
	return threshold
	
##This function is a general purpose value tuner. It finds a value that will be greater
##than or less than the desired percent of a whole map within a given tolerance. Map values
##should be between 0 and 1. To exclude parts of the map, set them to value 0.0
def FindValueFromPercentLen(map, length, percent, greaterThan):
	if length == 0:
		if greaterThan:
			return 1.0
		else:
			return 0.0
	tolerance = percent / 50.0
	inTolerance = False
	#to speed things up a little, lets take some time to find the middle value
	#in the dataset and use that to begin our search
	minV = 100.0
	maxV = 0.0
	totalCount = 0
	for i in range(length):
		if map[i] != 0.0:
			totalCount += 1
			if minV > map[i]:
				minV = map[i]
			if maxV < map[i]:
				maxV = map[i]
	mid = (maxV - minV) / 2.0 + minV
	overMinCount  = 0
	equalMinCount = 0
	for i in range(length):
		if map[i] > minV:
			overMinCount += 1
		elif map[i] == minV:
			equalMinCount += 1
	threshold       = mid
	thresholdChange = mid
	iterations = 0
	lastAdded = False
	while not inTolerance:
		iterations += 1
		if(iterations > 500):
			print "can't find value within tolerance, end value = "
			print "threshold = %f, thresholdChange = %f" % (threshold, thresholdChange)
			break #close enough
		matchCount = 0
		for i in range(length):
			if map[i] != 0.0:
				if greaterThan:
					if map[i] > threshold:
						matchCount += 1
				else:
					if map[i] < threshold:
						matchCount += 1
		currentPercent = float(matchCount) / float(totalCount)
		if currentPercent < percent + tolerance and currentPercent > percent - tolerance:
			inTolerance = True
		elif greaterThan:
			if currentPercent < percent:
				threshold -= thresholdChange
				if lastAdded:
					#only cut thresholdChange when direction is changed
					thresholdChange = thresholdChange / 2.0
				lastAdded = False
			else:
				threshold += thresholdChange
				if not lastAdded:
					thresholdChange = thresholdChange / 2.0
				lastAdded = True
		else:
			if currentPercent > percent:
				threshold -= thresholdChange
				if lastAdded:
					#only cut thresholdChange when direction is changed
					thresholdChange = thresholdChange / 2.0
				lastAdded = False
			else:
				threshold += thresholdChange
				if not lastAdded:
					thresholdChange = thresholdChange / 2.0
				lastAdded = True
	#at this point value should be in tolerance or close to it
	return threshold

def GetNeighbor(x, y, direction):
	if direction == mc.L:
		return x, y
	elif direction == mc.N:
		return x, y + 1
	elif direction == mc.S:
		return x, y - 1
	elif direction == mc.E:
		return x + 1, y
	elif direction == mc.W:
		return x - 1, y
	elif direction == mc.NE:
		return x + 1, y + 1
	elif direction == mc.NW:
		return x - 1, y + 1
	elif direction == mc.SE:
		return x + 1, y - 1
	elif direction == mc.SW:
		return x - 1, y - 1
	return -1, -1	
	
def isWaterMatch(x,y):
	result = hm.isBelowSeaLevel(x,y)
##	print "match function results - x = %d,y = %d,result = %d" % (x,y,result)
	return result
	
def isDeepWaterMatch(x, y):
	if not hm.isBelowSeaLevel(x, y):
		return False
	plot = CyMap().plot(x, y)
	if plot.isImpassable():
		return True
	for direction in range(1, 9):
		xx, yy = GetNeighbor(x, y, direction)
		ii = GetIndex(xx, yy)
		if ii >= 0 and not hm.isBelowSeaLevel(x, y):
			return False
	return True

def isPeakWaterMatch(x, y):
	return hm.isBelowSeaLevel(x, y) or (sm.plotMap[GetIndex(x, y)] == mc.PEAK)

class HeightMap :
	def __init__(self):
		return
	
	def generateHeightMap(self):
		self.heightMap = array('d')
		for i in range(mc.hmWidth * mc.hmHeight):
			self.heightMap.append(0.0)

		self.generateMidpointDisplacement()
		return
	
	def checkMaxGrain(self):
		#hm map dimensions(minus 1 if no wrapping) must be evenly divisible
		#by max grain
		ok = True
		width = mc.hmWidth
		height = mc.hmHeight
		if mc.WrapX == False:
			width -= 1
		if mc.WrapY == False:
			height -= 1
			
		if 0 != width % mc.hmMaxGrain:
			ok = False
		if 0 != height % mc.hmMaxGrain:
			ok = False

		if ok == False:
			raise ValueError, ("height map dimesions not divisible by mc.hmMaxGrain. also check wrapping options Width %d Height %d w %d h %d %s %s" % (mc.hmWidth , mc.hmHeight, width, height, str(mc.WrapX), str(mc.WrapY)))
			
		return

	def isPlotOnMargin(self,x,y):
		#first check top and bottom
		if mc.southMargin == True:
			if y < (mc.hmMaxGrain * mc.hmGrainMargin):
				return True
		if mc.northMargin == True:
			if y > (mc.hmHeight - (mc.hmMaxGrain * mc.hmGrainMargin)):
				return True
		#check right and left
		if mc.westMargin == True:
			if x < (mc.hmMaxGrain * mc.hmGrainMargin):
				return True
		if mc.eastMargin == True:
			if x > (mc.hmWidth - (mc.hmMaxGrain * mc.hmGrainMargin)):
				return True

		#now check middle
		if mc.hmSeparation != mc.NO_SEPARATION:
			if mc.hmSeparation == mc.NORTH_SOUTH_SEPARATION:
				dimension = y
				middle = mc.hmHeight/2
			elif mc.hmSeparation == mc.EAST_WEST_SEPARATION:
				dimension = x
				middle = mc.hmWidth/2
			else:
				raise ValueError, "bad hmSeparation type"

			if dimension > middle - (mc.hmMaxGrain * mc.hmGrainMargin) \
			and dimension < middle + (mc.hmMaxGrain * mc.hmGrainMargin):
				return True

		return False
	
	def generateMidpointDisplacement(self):
		self.checkMaxGrain()
		
		#make list of map plots that aren't on margin for each
		#map quadrant. We want to place the initial peaks randomly, but we
		#also want to ensure fairly even distribution so that
		#not all the peaks are on one side of the map. For this purpose
		#we will treat each map quadrant separately.

		peaksNWList = list()
		peaksNEList = list()
		peaksSWList = list()
		peaksSEList = list()
		middleX = mc.hmWidth/2
		middleY = mc.hmHeight/2
		for y in range(0,mc.hmHeight,mc.hmMaxGrain):
			for x in range(0,mc.hmWidth,mc.hmMaxGrain):
				if not self.isPlotOnMargin(x,y):
					if x < middleX and y < middleY:
						peaksSWList.append((x,y))
					elif x >= middleX and y < middleY:
						peaksSEList.append((x,y))
					elif x < middleX and y >= middleY:
						peaksNWList.append((x,y))
					elif x >= middleX and y >= middleY:
						peaksNEList.append((x,y))
		#shuffle the lists
		peaksNWList = ShuffleList(peaksNWList)
		peaksNEList = ShuffleList(peaksNEList)
		peaksSWList = ShuffleList(peaksSWList)
		peaksSEList = ShuffleList(peaksSEList)

		#place desired number of peaks in each quadrant
		totalNonMargin = len(peaksNWList)
		totalNonMargin += len(peaksNEList)
		totalNonMargin += len(peaksSWList)
		totalNonMargin += len(peaksSEList)
		
		count = max(1,int(float(totalNonMargin) * mc.hmInitialPeakPercent * 0.25))
		print "peak count = %d" % (count)
		for n in range(count):
			x,y = peaksNWList[n]
			i = GetHmIndex(x,y)
			self.heightMap[i] = 1.0
			print "%d,%d = 1.0" % (x,y)
			
			x,y = peaksNEList[n]
			i = GetHmIndex(x,y)
			self.heightMap[i] = 1.0
			
			x,y = peaksSWList[n]
			i = GetHmIndex(x,y)
			self.heightMap[i] = 1.0
			
			x,y = peaksSEList[n]
			i = GetHmIndex(x,y)
			self.heightMap[i] = 1.0
			
		self.printInitialPeaks()

		#Now use a diamond-square algorithm(sort of) to generate the rest
		currentGrain = float(mc.hmMaxGrain)
		while currentGrain > 1.0:
			#h is scalar for random displacement
			h = (currentGrain/float(mc.hmMaxGrain)) * float(mc.hmNoiseLevel)
			#First do the 'square' pass
			for y in range(0,mc.hmHeight,int(currentGrain)):
				for x in range(0,mc.hmWidth,int(currentGrain)):
					#on the square pass, GetHmIndex should handle all wrapping needs
					topLeft = GetHmIndex(x,y)
					topRight = GetHmIndex(x + int(currentGrain),y)
					if topRight == -1:
						continue #this means no wrap in x direction
					bottomLeft = GetHmIndex(x,y + int(currentGrain))
					if bottomLeft == -1:
						continue #this means no wrap in y direction
					bottomRight = GetHmIndex(x + int(currentGrain),y + int(currentGrain))
					middle = GetHmIndex(x + int(currentGrain/2.0),y + int(currentGrain/2.0))
					average = (self.heightMap[topLeft] + self.heightMap[topRight] \
					+ self.heightMap[bottomLeft] + self.heightMap[bottomRight])/4.0
					displacement = h * PRand.random() - h/2.0
					self.heightMap[middle] = average + displacement
					#now add that heuristic to the four points to diminish
					#artifacts. We don't need this on the diamond pass I don't think
					displacement = h * PRand.random() - h/2.0
					self.heightMap[topLeft] += displacement
					displacement = h * PRand.random() - h/2.0
					self.heightMap[topRight] += displacement
					displacement = h * PRand.random() - h/2.0
					self.heightMap[bottomLeft] += displacement
					displacement = h * PRand.random() - h/2.0
					self.heightMap[bottomRight] += displacement
			#Now do the 'diamond' pass, there are two diamonds for each x.
			#Possible wrapping is a big complication on this pass. Sorry!
			for y in range(0,mc.hmHeight,int(currentGrain)):
				for x in range(0,mc.hmWidth,int(currentGrain)):
					#first do the right facing diamond
					left = GetHmIndex(x,y)
					right = GetHmIndex(x + int(currentGrain),y)
					if right != -1: #if we're off map at this point go to next diamond
						average = self.heightMap[left] + self.heightMap[right]
						contributers = 2 #each diamond may have two or three contributers, 2 so far
						top = GetHmIndex(x + int(currentGrain/2.0),y - int(currentGrain/2.0))
						if top != -1:
							contributers += 1
							average += self.heightMap[top]
						bottom = GetHmIndex(x + int(currentGrain/2.0),y + int(currentGrain/2.0))
						if bottom != -1:
							contributers += 1
							average += self.heightMap[bottom]
						average = average/float(contributers)
						middle = GetHmIndex(x + int(currentGrain/2.0),y)
						displacement = h * PRand.random() - h/2.0
						self.heightMap[middle] = average + displacement
					#now do the down facing diamond
					top = GetHmIndex(x,y)
					bottom = GetHmIndex(x,y + int(currentGrain))
					if bottom != -1:
						average = self.heightMap[top] + self.heightMap[bottom]
						contributers = 2
						right = GetHmIndex(x + int(currentGrain/2.0),y + int(currentGrain/2.0))
						if right != -1:
							contributers += 1
							average += self.heightMap[right]
						left = GetHmIndex(x - int(currentGrain/2.0),y + int(currentGrain/2.0))
						if left != -1:
							contributers += 1
							average += self.heightMap[left]
						average = average/float(contributers)
						middle = GetHmIndex(x,y + int(currentGrain/2.0))
						displacement = h * PRand.random() - h/2.0
						self.heightMap[middle] = average + displacement
						
			currentGrain = currentGrain/2.0

		NormalizeMap(self.heightMap,mc.hmWidth,mc.hmHeight)
		
		return
	
	def performTectonics(self):
		self.plateMap = list()
		borderMap = array('i')#this will help in later distance calculations
		self.plateHeightMap = array('d')
		preSmoothMap = array('d')
		growthPlotList = list()
		plateList = list()
		maxDistance = math.sqrt(pow(float(mc.distanceFilterSize/2),2) + pow(float(mc.distanceFilterSize/2),2))
		#initialize maps
		for y in range(mc.hmHeight):
			for x in range(mc.hmWidth):
				i = GetHmIndex(x,y)
				self.plateMap.append(PlatePlot(0,maxDistance))
				borderMap.append(False)
				self.plateHeightMap.append(0.0)
				preSmoothMap.append(0.0)

		plateList.append(Plate(0,-1,-1))#zero placeholder (very silly I know)
		#seed plates
		for i in range(1,mc.hmNumberOfPlates + 1):
			#first find a random seed point that is not blocked by
			#previous points
			iterations = 0
			while(True):
				iterations += 1
				if iterations > 10000:
					raise ValueError, "endless loop in region seed placement"
				seedX = PRand.randint(0,mc.hmWidth + 1)
				seedY = PRand.randint(0,mc.hmHeight + 1)
				n = GetHmIndex(seedX,seedY)
				if self.isSeedBlocked(plateList,seedX,seedY) == False:
					self.plateMap[n].plateID = i
					plate = Plate(i,seedX,seedY)
					plateList.append(plate)
					#Now fill a 3x3 area to insure a minimum region size
					for direction in range(1,9,1):
						xx,yy = GetXYFromDirection(seedX,seedY,direction)
						nn = GetHmIndex(xx,yy)
						if nn != -1:
							self.plateMap[nn].plateID = i
							plot = (xx,yy,i)
							growthPlotList.append(plot)

					break
				
##		self.printPlateMap(self.plateMap)
		
		#Now cause the seeds to grow into plates
		iterations = 0
		while(len(growthPlotList) > 0):
			iterations += 1
			if iterations > 200000:
				self.printPlateMap(self.plateMap)
				print "length of growthPlotList = %d" % (len(growthPlotList))
				raise ValueError, "endless loop in plate growth"
			plot = growthPlotList[0]
			roomLeft = False
			for direction in range(1,5,1):
				x,y,plateID = plot
				i = GetHmIndex(x,y)
				xx,yy = GetXYFromDirection(x,y,direction)
				ii = GetHmIndex(xx,yy)
				if ii == -1:
					plateList[plateID].isOnMapEdge = True
					continue
				if self.plateMap[ii].plateID != plateID and self.plateMap[ii].plateID != 0:
					borderMap[i] = True
					borderMap[ii] = True				   
				elif self.plateMap[ii].plateID == 0:
					roomLeft = True
					if direction == mc.N or direction == mc.S:
						growthChance = mc.plateGrowthChanceY
					else:
						growthChance = mc.plateGrowthChanceX
					if PRand.random() < growthChance:
						self.plateMap[ii].plateID = plateID
						newPlot = (xx,yy,plateID)
						growthPlotList.append(newPlot)
				
					
			#move plot to the end of the list if room left, otherwise
			#delete it if no room left
			if roomLeft:
				growthPlotList.append(plot)
			del growthPlotList[0]
							
##		self.printPlateMap(self.plateMap)

		#to balance the map we want at least one plate stagger upward
		#in each quadrant
		NWfound = False
		NEfound = False
		SEfound = False
		SWfound = False
		for plate in plateList:
			if plate.GetQuadrant() == plate.NW and NWfound == False:
				plate.raiseOnly = True
				NWfound = True
			if plate.GetQuadrant() == plate.NE and NEfound == False:
				plate.raiseOnly = True
				NEfound = True
			if plate.GetQuadrant() == plate.SE and SEfound == False:
				plate.raiseOnly = True
				SEfound = True
			if plate.GetQuadrant() == plate.SW and SWfound == False:
				plate.raiseOnly = True
				SWfound = True
		
		#Stagger the plates somewhat to add interest
		steps = int(mc.plateStaggerRange/mc.plateStagger)
		for i in range(0,mc.hmHeight*mc.hmWidth):
			if plateList[self.plateMap[i].plateID].isOnMapEdge and PRand.random() < mc.chanceForWaterEdgePlate:
				preSmoothMap[i] = 0.0
			elif plateList[self.plateMap[i].plateID].raiseOnly:
				preSmoothMap[i] = (float(self.plateMap[i].plateID % steps) * mc.plateStagger)/2.0 + 0.5			   
			else:
				preSmoothMap[i] = float(self.plateMap[i].plateID % steps) * mc.plateStagger

##		self.printPreSmoothMap(preSmoothMap)

		#Now smooth the plate height map and create the distance map at the same time
		#Since the algorithm is the same
		for y in range(0,mc.hmHeight):
			for x in range(0,mc.hmWidth):
				contributers = 0
				avg = 0
				i = GetHmIndex(x,y)
				isBorder = False
				if borderMap[i] == True:
					isBorder = True
				plateID = self.plateMap[i].plateID
				for yy in range(y - mc.distanceFilterSize/2,y + mc.distanceFilterSize/2 + 1,1):
					for xx in range(x - mc.distanceFilterSize/2,x + mc.distanceFilterSize/2 + 1,1):
						ii = GetHmIndex(xx,yy)
						if ii == -1:
							continue
						contributers += 1
						avg += preSmoothMap[ii]
						if isBorder and plateID != self.plateMap[ii].plateID:
							distance = math.sqrt(pow(float(y - yy),2) + pow(float(x - xx),2))
							if distance < self.plateMap[ii].distanceList[plateID]:
								self.plateMap[ii].distanceList[plateID] = distance
				avg = avg/float(contributers)
				self.plateHeightMap[i] = avg
				
##		self.printPlateHeightMap()
#		self.printDistanceMap(distanceMap,maxDistance)

		#Now add ripple formula to plateHeightMap
		for i in range(mc.hmWidth*mc.hmHeight):
			avgRippleTop = 0.0
			avgRippleBottom = 0.0
			for plateID in range(1,mc.hmNumberOfPlates + 1):
				distanceWeight = maxDistance - self.plateMap[i].distanceList[plateID]
#				print "a1 = %f, a2 = %f" % (plateList[self.plateMap[i].plateID].angle,plateList[plateID].angle)
				if plateList[plateID].seedX < plateList[self.plateMap[i].plateID].seedX:
					angleDifference = AngleDifference(plateList[self.plateMap[i].plateID].angle,plateList[plateID].angle)
				else:
					angleDifference = AngleDifference(plateList[plateID].angle,plateList[self.plateMap[i].plateID].angle)
#				print angleDifference
				ripple = (pow(math.cos(mc.rippleFrequency * self.plateMap[i].distanceList[plateID]) * \
				(-self.plateMap[i].distanceList[plateID]/maxDistance + 1),2) + (-self.plateMap[i].distanceList[plateID]/maxDistance + 1)) \
				* mc.rippleAmplitude * math.sin(math.radians(angleDifference))
				avgRippleTop += (ripple * distanceWeight)
				avgRippleBottom += distanceWeight
			if avgRippleBottom == 0.0:
				avgRipple = 0.0
			else:
				avgRipple = avgRippleTop/avgRippleBottom
			self.plateHeightMap[i] += avgRipple - (avgRipple * PRand.random() * mc.plateNoiseFactor)
			
		NormalizeMap(self.plateHeightMap,mc.hmWidth,mc.hmHeight)
##		self.printPlateHeightMap()


	def combineMaps(self):					
		#Now add plateHeightMap to HeightMap
		for i in range(mc.hmWidth * mc.hmHeight):
			self.heightMap[i] += self.plateHeightMap[i] * mc.plateMapScale

		#depress margins, this time with brute force
		marginSize = mc.hmMaxGrain * mc.hmGrainMargin
		for y in range(mc.hmHeight):
			for x in range(mc.hmWidth):
				i = GetHmIndex(x,y)
				if mc.westMargin == True:
					if x < marginSize:
						self.heightMap[i] *= (float(x)/float(marginSize)) * (1.0 - mc.hmMarginDepth) + mc.hmMarginDepth
				if mc.eastMargin == True:
					if mc.hmWidth - x < marginSize:
						self.heightMap[i] *= (float(mc.hmWidth - x)/float(marginSize)) * (1.0 - mc.hmMarginDepth) + mc.hmMarginDepth
				if mc.southMargin == True:
					if y < marginSize:
						self.heightMap[i] *= (float(y)/float(marginSize)) * (1.0 - mc.hmMarginDepth) + mc.hmMarginDepth
				if mc.northMargin == True:
					if mc.hmHeight - y < marginSize:
						self.heightMap[i] *= (float(mc.hmHeight - y)/float(marginSize)) * (1.0 - mc.hmMarginDepth) + mc.hmMarginDepth

				if mc.hmSeparation == mc.NORTH_SOUTH_SEPARATION:
					difference = abs((mc.hmHeight/2) - y)
					if difference < marginSize:
						self.heightMap[i] *= (float(difference)/float(marginSize)) * (1.0 - mc.hmMarginDepth) + mc.hmMarginDepth

				elif mc.hmSeparation == mc.EAST_WEST_SEPARATION:
					difference = abs((mc.hmWidth/2) - x)
					if difference < marginSize:
						self.heightMap[i] *= (float(difference)/float(marginSize)) * (1.0 - mc.hmMarginDepth) + mc.hmMarginDepth
						
##		#Now lets square the heightmap to simulate erosion
##		for i in range(mc.hmWidth * mc.hmHeight):
##			self.heightMap[i] = self.heightMap[i] * self.heightMap[i]

		NormalizeMap(self.heightMap,mc.hmWidth,mc.hmHeight)

	def rotateMap(self):

		if mc.noRotate != 0:
			return

			# This rotates a map east or west so that the map wraps around where
			# the lowest vertical band is on the map
		low = 0
		min = 10000.0

	# Find the place on the map with the most water (lowest heightfield)
		for x in range(mc.hmWidth):
			sum = 0.0
			for y in range(mc.hmHeight):
				sum += self.heightMap[GetHmIndex(x,y)]
		#print "for x %d sum is %f min %f" % (x,sum,min)
		if(sum < min):
			low = x
			min = sum
	#print "low x is %d" % (low) #DEBUG
	
	# Rotate the height map so we wrap where there is more water
		for y in range(mc.hmHeight):
			tempStripe = []
			for x in range(mc.hmWidth):
				tempStripe.append(self.heightMap[GetHmIndex(x,y)])
			for x in range(mc.hmWidth):
				self.heightMap[GetHmIndex(x,y)] = tempStripe[((x + low) % mc.hmWidth)]

	# Done
		return


	def addWaterBands(self):
		#validate water bands. Maps that wrap cannot have one in that direction
		if mc.WrapX and (mc.eastWaterBand != 0 or mc.westWaterBand != 0):
			raise ValueError,"east/west water bands cannot be used when wrapping in X direction."
		if mc.WrapY and (mc.northWaterBand != 0 or mc.southWaterBand != 0):
			raise ValueError,"north/south water bands cannot be used when wrapping in Y direction."
		
		newWidth = mc.hmWidth + mc.eastWaterBand + mc.westWaterBand
		newHeight = mc.hmHeight + mc.northWaterBand + mc.southWaterBand
		newHeightMap = array('d')
		for y in range(newHeight):
			for x in range(newWidth):
				oldX = x - mc.westWaterBand
				oldY = y - mc.southWaterBand
#				i = GetIndexGeneral(x,y,newWidth,newHeight)
				ii = GetHmIndex(oldX,oldY)
				if ii == -1:
					newHeightMap.append(0.0)
				else:
					newHeightMap.append(self.heightMap[ii])

		mc.hmWidth = newWidth
		mc.hmHeight = newHeight
		self.heightMap = newHeightMap
		
	def calculateSeaLevel(self):
		if mc.patience == 0:
			mc.landPercent *= 2
			if mc.landPercent > 1:
				mc.landPercent = 1
		if mc.patience == 1:
			mc.landPercent *= 1.5
			if mc.landPercent > 1:
				mc.landPercent = 1
		self.seaLevel = FindValueFromPercent(self.heightMap,mc.hmWidth,mc.hmHeight,mc.landPercent,0.02,True)
		return
	
	def isBelowSeaLevel(self,x,y):
		i = GetHmIndex(x,y)
##		print "heightMap = %f at %d,%d" % (self.heightMap[i],x,y)
##		print "seaLevel = %f" % self.seaLevel
		if self.heightMap[i] < self.seaLevel:
##			print "True"
			return True
##		print "False"
		return False
	
	## This function returns altitude in relation to sea level with
	## 0.0 being seaLevel and 1.0 being highest altitude
	def getAltitudeAboveSeaLevel(self,x,y):
		i = GetHmIndex(x,y)
		if i == -1:
			return 0.0
		altitude = self.heightMap[i]
		if altitude < self.seaLevel:
			return 0.0
		altitude = 1.0/(1.0 - self.seaLevel) * (altitude - self.seaLevel)
		return altitude

	def setAltitudeAboveSeaLevel(self,x,y,altitude):
		i = GetHmIndex(x,y)
		if i == -1:
			return
		self.heightMap[i] = ((1.0 - self.seaLevel) * altitude) + self.seaLevel
		
##	def Erode(self):
##		for y in range(mc.hmHeight):
##			for x in range(mc.hmWidth):
##				alt = self.getAltitudeAboveSeaLevel(x,y)
##				if alt > 0:
##					eroded = pow(alt,mc.erosionPower)
##					self.setAltitudeAboveSeaLevel(x,y,eroded)
				
	def isSeedBlocked(self,plateList,seedX,seedY):
		for plate in plateList:
			if seedX > plate.seedX - mc.minSeedRange and seedX < plate.seedX + mc.minSeedRange:
				if seedY > plate.seedY - mc.minSeedRange and seedY < plate.seedY + mc.minSeedRange:
					return True
		#Check for edge
		if seedX < mc.minEdgeRange or seedX >= (mc.hmWidth + 1) - mc.minEdgeRange:
			return True
		if seedY < mc.minEdgeRange or seedY >= (mc.hmHeight + 1) - mc.minEdgeRange:
			return True
		return False
	def GetInfluFromDistance(self,sinkValue,peakValue,searchRadius,distance):
		influence = peakValue
		maxDistance = math.sqrt(pow(float(searchRadius),2) + pow(float(searchRadius),2))
		#minDistance = 1.0
		influence -= ((peakValue - sinkValue)* (distance - 1.0))/(maxDistance - 1.0)
		return influence
	def FindDistanceToPlateBoundary(self,x,y,searchRadius):
		minDistance = 10.0
		i = self.GetIndex(x,y)
		for yy in range(y - searchRadius,y + searchRadius):
			for xx in range(x - searchRadius,x + searchRadius):
				ii = self.GetIndex(xx,yy)
				if self.plateMap[i] != self.plateMap[ii]:
					distance = math.sqrt(pow(float(xx-x),2) + pow(float(yy-y),2))
					if distance < minDistance:
						minDistance = distance
						   
		if minDistance == 10.0:
			return 0.0
		
		return minDistance
	
	def fillInLakes(self):
		#smaller lakes need to be filled in for now. The river system will
		#most likely recreate them later due to drainage calculation
		#according to certain rules. This makes the lakes look much better
		#and more sensible.
		am = Areamap(mc.hmWidth,mc.hmHeight,True,True)
		am.defineAreas(isWaterMatch)
##		am.PrintAreaMap()
		oceanID = am.getOceanID()
		for y in range(mc.hmHeight):
			for x in range(mc.hmWidth):
				i = GetHmIndex(x,y)
				if self.isBelowSeaLevel(x,y) and am.areaMap[i] != oceanID:
					#check the size of this body of water, if too small,
					#change to land
					for a in am.areaList:
						if a.ID == am.areaMap[i] and a.size < mc.minInlandSeaSize:
							self.heightMap[i] = self.seaLevel
		
		return
	
	def printInitialPeaks(self):
		lineString = "midpoint displacement peaks and margins"
		print lineString
		if not mc.WrapY:
			adjustedHeight = mc.hmHeight - 1
		else:
			adjustedHeight = mc.hmHeight - mc.hmMaxGrain
		for y in range(adjustedHeight,-1,-mc.hmMaxGrain):
			lineString = ""
			for x in range(0,mc.hmWidth,mc.hmMaxGrain):
				i = GetHmIndex(x,y)
				if self.isPlotOnMargin(x,y):
					lineString += "*"
				elif self.heightMap[i] == 1.0:
					lineString += "1"
				elif self.heightMap[i] == 0.0:
					lineString += "0"
			print lineString
		lineString = " "
		print lineString
		
	def printHeightMap(self):
		print self.heightMap[:]
		lineString = "Height Map"
		print lineString
		for y in range(mc.hmHeight - 1,-1,-1):
			lineString = ""
			for x in range(0,mc.hmWidth,1):
				i = GetHmIndex(x,y)
				mapLoc = int((self.heightMap[i] - self.seaLevel)/(1.0 - self.seaLevel) * 10)
				#mapLoc = int(self.heightMap[i] * 10)
				if self.heightMap[i] < self.seaLevel:
					lineString += '.'
				else:
					lineString += chr(mapLoc + 48)
			print lineString
		lineString = " "
		print lineString
		
	def printPlateMap(self,plateMap):
		lineString = "Plate Map"
		print lineString
		for y in range(mc.hmHeight - 1,-1,-1):
			lineString = ""
			for x in range(0,mc.hmWidth,1):
				i = GetHmIndex(x,y)
				mapLoc = plateMap[i].plateID
				if mapLoc > 40:
					mapLoc = 41
				lineString += chr(mapLoc + 48)
			print lineString
		lineString = " "
		print lineString
		
	def printPreSmoothMap(self,preSmoothMap):
		lineString = "Pre-Smooth Map"
		print lineString
		for y in range(mc.hmHeight - 1,-1,-1):
			lineString = ""
			for x in range(0,mc.hmWidth,1):
				i = GetHmIndex(x,y)
				mapLoc = int(preSmoothMap[i] * 40)
				lineString += chr(mapLoc + 48)
			print lineString
		lineString = " "
		print lineString
		
	def printPlateHeightMap(self):
		lineString = "Plate Height Map"
		print lineString
		for y in range(mc.hmHeight - 1,-1,-1):
			lineString = ""
			for x in range(0,mc.hmWidth,1):
				i = GetHmIndex(x,y)
				mapLoc = int(self.plateHeightMap[i] * 40)
				lineString += chr(mapLoc + 48)
			print lineString
		lineString = " "
		print lineString
		
	def printDistanceMap(self,distanceMap,maxDistance):
		lineString = "Plate Height Map"
		print lineString
		for y in range(mc.hmHeight - 1,-1,-1):
			lineString = ""
			for x in range(0,mc.hmWidth,1):
				i = GetHmIndex(x,y)
				mapLoc = int((distanceMap[i]/maxDistance) * 40)
				lineString += chr(mapLoc + 48)
			print lineString
		lineString = " "
		print lineString
		
class Plate :
	def __init__(self,ID,seedX,seedY):
		self.ID = ID
		self.seedX = seedX
		self.seedY = seedY
		self.isOnMapEdge = False
		self.angle = (PRand.random() * 360) - 180
		self.raiseOnly = False
		self.NW = 0
		self.NE = 1
		self.SE = 2
		self.SW = 3
	def GetQuadrant(self):
		if self.seedY < mc.hmHeight/2:
			if self.seedX < mc.hmWidth/2:
				return self.SW
			else:
				return self.SE
		else:
			if self.seedX < mc.hmWidth/2:
				return self.NW
			else:
				return self.NE
				
class PlatePlot :
	def __init__(self,plateID,maxDistance):
		self.plateID = plateID
		self.distanceList = list()
		for i in range(mc.hmNumberOfPlates + 1):
			self.distanceList.append(maxDistance)
			
class ClimateMap :
	def __init__(self):
		return
	def createClimateMaps(self):
		summerSunMap = array('d')
		winterSunMap = array('d')
		self.summerTempsMap = array('d')
		self.winterTempsMap = array('d')
		self.averageTempMap = array('d')
		self.moistureMap = array('d')
		self.rainFallMap = array('d')

		self.initializeTempMap(summerSunMap,mc.tropicsLatitude)
		self.initializeTempMap(winterSunMap,-mc.tropicsLatitude)

		#smooth both sun maps into the temp maps
		for y in range(0,mc.hmHeight):
			for x in range(0,mc.hmWidth):
				contributers = 0
				summerAvg = 0
				winterAvg = 0
				i = GetHmIndex(x,y)
				for yy in range(y - mc.filterSize/2,y + mc.filterSize/2 + 1,1):
					for xx in range(x - mc.filterSize/2,x + mc.filterSize/2 + 1,1):
						ii = GetHmIndex(xx,yy)
						if ii == -1:
							continue
						contributers += 1
						summerAvg += summerSunMap[ii]
						winterAvg += winterSunMap[ii]
				summerAvg = summerAvg/float(contributers)
				winterAvg = winterAvg/float(contributers)
				self.summerTempsMap.append(summerAvg)
				self.winterTempsMap.append(winterAvg)
				
		#create average temp map
		for y in range(mc.hmHeight):
			for x in range(mc.hmWidth):
				i = GetHmIndex(x,y)
				#average summer and winter
				avgTemp = (self.summerTempsMap[i] + self.winterTempsMap[i])/2.0
				#cool map for altitude
				self.averageTempMap.append(avgTemp * (1.0 - pow(hm.getAltitudeAboveSeaLevel(x,y),mc.temperatureLossCurve) * mc.heatLostAtOne))
		
		#init moisture and rain maps
		for i in range(mc.hmHeight*mc.hmWidth):
			self.moistureMap.append(0.0)
			self.rainFallMap.append(0.0)
			
		#create sortable plot list for summer monsoon rains
		temperatureList = list()
		for y in range(mc.hmHeight):
			for x in range(mc.hmWidth):
				i = GetHmIndex(x,y)
				rainPlot = RainPlot(x,y,self.summerTempsMap[i],0)
				temperatureList.append(rainPlot)
		#sort by temperature, coldest first
		temperatureList.sort(lambda x,y:cmp(x.order,y.order))
		  
		#Drop summer monsoon rains
		self.dropRain(temperatureList,self.summerTempsMap,False,None)

		#clear moisture map
		for i in range(mc.hmHeight*mc.hmWidth):
			self.moistureMap[i] = 0.0
			
		#create sortable plot list for winter monsoon rains
		temperatureList = list()
		for y in range(mc.hmHeight):
			for x in range(mc.hmWidth):
				i = GetHmIndex(x,y)
				rainPlot = RainPlot(x,y,self.winterTempsMap[i],0)
				temperatureList.append(rainPlot)
		#sort by temperature, coldest first
		temperatureList.sort(lambda x,y:cmp(x.order,y.order))
		  
		#Drop winter monsoon rains
		self.dropRain(temperatureList,self.winterTempsMap,False,None)

		#clear moisture map
		for i in range(mc.hmHeight*mc.hmWidth):
			self.moistureMap[i] = 0.0
			
		#set up WindZones class
		wz = WindZones(mc.hmHeight,mc.topLatitude,mc.bottomLatitude)

		#create ordered list for geostrophic rain
		orderList = list()
		for zone in range(6):
			topY = wz.GetYFromZone(zone,True)
			bottomY = wz.GetYFromZone(zone,False)
			if topY == -1 and bottomY == -1:
				continue #This wind zone is not represented on this map at all so skip it
			if topY == -1: #top off map edge
				topY = mc.hmHeight - 1
			if bottomY == -1:
				bottomY = 0

			dx,dy = wz.GetWindDirectionsInZone(zone)
			if dy < 0:
				yStart = topY
				yStop = bottomY - 1
			else:
				yStart = bottomY
				yStop = topY + 1
			if dx < 0:
				xStart = mc.hmWidth - 1
				xStop = -1
			else:
				xStart = 0
				xStop = mc.hmWidth
			order = 0.0
			for y in range(yStart,yStop,dy):
				for x in range(xStart,xStop,dx):
					rainPlot = RainPlot(x,y,order,abs(yStop - y))
					orderList.append(rainPlot)
					order += 1.0

		#Sort order list
		orderList.sort(lambda x,y:cmp(x.order,y.order))

		#drop geostrophic rain			
		self.dropRain(orderList,self.averageTempMap,True,wz)
		

		NormalizeMap(self.rainFallMap,mc.hmWidth,mc.hmHeight)

##		self.printRainFallMap(True)
##		self.printRainFallMap(False)
		
				
	def dropRain(self,plotList, tempMap, bGeostrophic, windZones):
		countRemaining = len(plotList)
		bDebug = False
		for plot in plotList:
			i = GetHmIndex(plot.x,plot.y)
			if bDebug:
				print "rainplot at %d,%d" % (plot.x,plot.y)
				print "order = %f" % (plot.order)
				print "initial moisture = %f" % (self.moistureMap[i])
			#First collect moisture from sea
			if hm.isBelowSeaLevel(plot.x,plot.y):
				self.moistureMap[i] += tempMap[i]
				if bDebug:
					print "collecting %f moisture from sea" % (tempMap[i])
					
			nList = list()
			if bGeostrophic:
				#make list of neighbors in geostrophic zone, even if off map
				zone = windZones.GetZone(plot.y)
				dx,dy = windZones.GetWindDirectionsInZone(zone)
				if bDebug:
					if dy < 0:
						yString = "v"
					else:
						yString = "^"
					if dx < 0:
						xString = "<"
					else:
						xString = ">"
					print "Wind direction ------------------------------- %s%s - %s" % (xString,yString,windZones.GetZoneName(zone))
				nList.append((plot.x,plot.y + dy))
				nList.append((plot.x + dx,plot.y))
				nList.append((plot.x + dx,plot.y + dy))
				
			else:
				#make list of neighbors with higher temp
				for direction in range(1,9,1):
					xx,yy = GetXYFromDirection(plot.x,plot.y,direction)
					ii = GetHmIndex(xx,yy)
					if ii != -1 and tempMap[i] <= tempMap[ii]:
						nList.append((xx,yy))
				#divide moisture by number of neighbors for distribution
				if len(nList) == 0:
					continue #dead end, dump appropriate rain
			moisturePerNeighbor = self.moistureMap[i]/float(len(nList))
			if bDebug:
				print "moisturePerNeighbor = %f for %d neighbors" % (moisturePerNeighbor,len(nList))

			geostrophicFactor = 1.0
			if bGeostrophic:
				geostrophicFactor = mc.geostrophicFactor
			for xx,yy in nList:
				ii = GetHmIndex(xx,yy)
				if bDebug:
					print "  neighbor %d,%d" % (xx,yy)
					print "  countRemaining = %d" % countRemaining
				#Get the rain cost to enter this plot. Cost is
				#percentage of present moisture available for this
				#neighbor
				if bGeostrophic:
					cost = self.getRainCost(plot.x,plot.y,xx,yy,plot.uplift)
				else:
					cost = self.getRainCost(plot.x,plot.y,xx,yy,countRemaining/mc.monsoonUplift)
					
				if bDebug:
					print "  rain cost = %f" % cost

				#Convert moisture into rain
				#self.moistureMap[i] -= cost * moisturePerNeighbor (this line is unecessary actually, we are finished with moisture map for this plot) 
				self.rainFallMap[i] += cost * moisturePerNeighbor * geostrophicFactor #geostrophicFactor is not involved with moisture, only to weigh against monsoons
				if bDebug:
					print "  dropping %f rain here" % (cost * moisturePerNeighbor)

				#send remaining moisture to neighbor
				if ii != -1:
					self.moistureMap[ii] += moisturePerNeighbor - (cost * moisturePerNeighbor)
					if bDebug:
						print "  remaining moisture to neighbor = %f" % (moisturePerNeighbor - (cost * moisturePerNeighbor))

			if bDebug:
				print "total rainfall = %f" % self.rainFallMap[i]
			countRemaining -= 1
			
	def getRainCost(self,x1,y1,x2,y2,distanceToUplift):
		cost = mc.minimumRainCost
		cRange = 1.0 - mc.minimumRainCost/1.0#We don't want to go over 1.0 so the range is reduced
		upliftCost = (1.0/(float(distanceToUplift) + 1.0)) * cRange
		i = GetHmIndex(x1,y1)
		ii = GetHmIndex(x2,y2)
		cost += max((self.averageTempMap[ii] - self.averageTempMap[i]) * 2.0 * cRange,upliftCost)
		return cost
			
	def initializeTempMap(self,tempMap,tropic):
		for y in range(mc.hmHeight):
			for x in range(mc.hmWidth):
				tempMap.append(self.getInitialTemp(x,y,tropic))
		return

	def getInitialTemp(self,x,y,tropic):
		i = GetHmIndex(x,y)
		lat = self.getLatitude(y)
		latRange = float(90 + abs(tropic))
		latDifference = abs(float(lat - tropic))
		aboveSeaLevel = hm.heightMap[i] > hm.seaLevel
		if aboveSeaLevel:
			tempPerLatChange = 1.0/latRange
			temp = 1.0 - (tempPerLatChange * latDifference)
		else:
			tempPerLatChange = (1.0 - (2.0*mc.oceanTempClamp))/latRange
			temp = 1.0 - mc.oceanTempClamp - (tempPerLatChange * latDifference)

		return temp

	def getLatitude(self,y):
		latitudeRange = mc.topLatitude - mc.bottomLatitude
		degreesPerDY = float(latitudeRange)/float(mc.hmHeight - mc.northCrop - mc.southCrop)
		if y > mc.hmHeight - mc.northCrop:
			return mc.topLatitude
		if y < mc.southCrop:
			return mc.bottomLatitude
		latitude = (mc.bottomLatitude + (int(round(float(y - mc.southCrop)* degreesPerDY))))
		return latitude
	
	def printRainFallMap(self,bOcean):
		lineString = "Rainfall Map"
		print lineString
		wz = WindZones(mc.hmHeight,mc.topLatitude,mc.bottomLatitude)
		for y in range(mc.hmHeight - 1,-1,-1):
			lineString = ""
			for x in range(0,mc.hmWidth,1):
				i = GetHmIndex(x,y)
				if bOcean:
					if self.rainFallMap[i] < 0.1:
						mapLoc = int(self.rainFallMap[i] * 100)
						lineString += chr(mapLoc + 48)
					else:	
						mapLoc = int(self.rainFallMap[i] * 10)
						lineString += chr(mapLoc + 65)
				else:
					if hm.isBelowSeaLevel(x,y):
						lineString += '.'
					elif self.rainFallMap[i] < 0.00001:
						lineString += 'X'
					else:
						if self.rainFallMap[i] < 0.1:
							mapLoc = int(self.rainFallMap[i] * 100)
							lineString += chr(mapLoc + 48)
						else:	
							mapLoc = int(self.rainFallMap[i] * 10)
							lineString += chr(mapLoc + 65)
			z = wz.GetZone(y)
			dx,dy = wz.GetWindDirectionsInZone(z)
			lineString += ' - '
			if dx < 0:
				lineString += '<'
			else:
				lineString += '>'
			if dy < 0:
				lineString += 'v'
			else:
				lineString += '^'
			lineString += ' ' + wz.GetZoneName(z)
			print lineString
		lineString = " "
		print lineString
	def printTempMap(self,tempMap):
		lineString = "Temp Map"
		print lineString
		wz = WindZones(mc.hmHeight,mc.topLatitude,mc.bottomLatitude)
		for y in range(mc.hmHeight - 1,-1,-1):
			lineString = ""
			for x in range(0,mc.hmWidth,1):
				i = GetHmIndex(x,y)
				mapLoc = int(tempMap[i] * 10)
				lineString += chr(mapLoc + 48)
			z = wz.GetZone(y)
			dx,dy = wz.GetWindDirectionsInZone(z)
			lineString += ' - '
			if dx < 0:
				lineString += '<'
			else:
				lineString += '>'
			if dy < 0:
				lineString += 'v'
			else:
				lineString += '^'
			lineString += ' ' + wz.GetZoneName(z)
			print lineString
		lineString = " "
		print lineString
		
class RainPlot :
	def __init__(self,x,y,order,uplift):
		self.x = x
		self.y = y
		self.order = order
		self.uplift = uplift
		
class WindZones :
	def __init__(self,mapHeight,topLat,botLat):
		self.NPOLAR = 0
		self.NTEMPERATE = 1
		self.NEQUATOR = 2
		self.SEQUATOR = 3
		self.STEMPERATE = 4
		self.SPOLAR = 5
		self.NOZONE = 99
		self.mapHeight = mapHeight
		self.topLat = topLat
		self.botLat = botLat
	def GetZone(self,y):
		if y < 0 or y >= self.mapHeight:
			return self.NOZONE
		lat = cm.getLatitude(y)
		if lat > mc.polarFrontLatitude:
			return self.NPOLAR
		elif lat > mc.horseLatitude:
			return self.NTEMPERATE
		elif lat > 0:
			return self.NEQUATOR
		elif lat > -mc.horseLatitude:
			return self.SEQUATOR
		elif lat > -mc.polarFrontLatitude:
			return self.STEMPERATE
		else:
			return self.SPOLAR
		return
	def GetZoneName(self,zone):
		if zone == self.NPOLAR:
			return "NPOLAR"
		elif zone == self.NTEMPERATE:
			return "NTEMPERATE"
		elif zone == self.NEQUATOR:
			return "NEQUATOR"
		elif zone == self.SEQUATOR:
			return "SEQUATOR"
		elif zone == self.STEMPERATE:
			return "STEMPERATE"
		else:
			return "SPOLAR"
		return
	def GetYFromZone(self,zone,bTop):
		if bTop:
			for y in range(self.mapHeight - 1,-1,-1):
				if zone == self.GetZone(y):
					return y
		else:
			for y in range(self.mapHeight):
				if zone == self.GetZone(y):
					return y
		return -1
	def GetZoneSize(self):
		latitudeRange = self.topLat - self.botLat
		degreesPerDY = float(latitudeRange)/float(self.mapHeight)
		size = 30.0/degreesPerDY
		return size
	def GetWindDirections(self,y):
		z = self.GetZone(y)
		#get x,y directions
		return self.GetWindDirectionsInZone(z)
	def GetWindDirectionsInZone(self,z):
		#get x,y directions
		if z == self.NPOLAR:
			return (-1,-1)
		elif z == self.NTEMPERATE:
			return (1,1)
		elif z == self.NEQUATOR:
			return (-1,-1)
		elif z == self.SEQUATOR:
			return (-1,1)
		elif z == self.STEMPERATE:
			return (1,-1)
		elif z == self.SPOLAR:
			return (-1,1)
		return (0,0)

def isSmallWaterMatch(x,y):
	return sm.isBelowSeaLevel(x,y)

class SmallMaps :
	def __init__(self):
		return
	def initialize(self):
		self.cropMaps()
		newHeightMap = ShrinkMap(hm.heightMap,mc.hmWidth ,mc.hmHeight,mc.width,mc.height)
		newRainFallMap = ShrinkMap(cm.rainFallMap,mc.hmWidth,mc.hmHeight,mc.width,mc.height)
		newAverageTempMap = ShrinkMap(cm.averageTempMap,mc.hmWidth,mc.hmHeight,mc.width,mc.height)

		self.heightMap = array('d')
		self.rainFallMap = array('d')
		self.averageTempMap = array('d')

		for y in range(mc.height):
			for x in range(mc.width):
				oldX = x
				i = GetIndexGeneral(oldX,y,mc.width,mc.height)
				if i != -1:
					self.heightMap.append(newHeightMap[i])
					self.rainFallMap.append(newRainFallMap[i])
					self.averageTempMap.append(newAverageTempMap[i])
				else:
					self.heightMap.append(hm.seaLevel - 0.000001)
					self.rainFallMap.append(0.0)
					self.averageTempMap.append(0.0)

		#Smooth coasts so there are fewer hills on coast
	# (This might make deep ocean difficult to implement)
		for y in range(mc.height):
			for x in range(mc.width):
				if self.isBelowSeaLevel(x,y):
					i = GetIndex(x,y)
					self.heightMap[i] = hm.seaLevel - 0.000001
					
		self.fillInLakes()

		self.createPlotMap()
		self.printPlotMap()
		self.createTerrainMap()
		continentMap.generateContinentMap()

	def fillInLakes(self):
		#smaller lakes need to be filled in again because the map
		#shrinker sometimes creates lakes.
		am = Areamap(mc.width,mc.height,True,True)
		am.defineAreas(isSmallWaterMatch)
		am.PrintAreaMap()
		oceanID = am.getOceanID()
		for y in range(mc.height):
			for x in range(mc.width):
				i = GetIndex(x,y)
				if self.isBelowSeaLevel(x,y) and am.areaMap[i] != oceanID:
					#check the size of this body of water, if too small,
					#change to land
					for a in am.areaList:
						if a.ID == am.areaMap[i] and a.size < mc.minInlandSeaSize:
							self.heightMap[i] = hm.seaLevel
		
		return
		
	def isBelowSeaLevel(self,x,y):
		i = GetIndex(x,y)
		if self.heightMap[i] < hm.seaLevel:
			return True
		return False
	
	## This function returns altitude in relation to sea level with
	## 0.0 being seaLevel and 1.0 being highest altitude
	def getAltitudeAboveSeaLevel(self,x,y):
		i = GetIndex(x,y)
		if i == -1:
			return 0.0
		altitude = self.heightMap[i]
		if altitude < hm.seaLevel:
			return 0.0
		altitude = 1.0/(1.0 - hm.seaLevel) * (altitude - hm.seaLevel)
		return altitude
	

	def createPlotMap(self):
		print "creating plot map"
		self.plotMap = array('i')
		#create height difference map to allow for tuning
		self.diffMap = array('d')
		for i in range(0,mc.height*mc.width):
			self.diffMap.append(0.0)
		#I tried using a deviation from surrounding average altitude
		#to determine hills and peaks but I didn't like the
		#results. Therefore I an using lowest neighbor
		for y in range(mc.height):
			for x in range(mc.width):
				i = GetIndex(x,y)
				myAlt = self.heightMap[i]
				minAlt = 1.0
				for direction in range(1,9,1):
					xx,yy = GetXYFromDirection(x,y,direction)
					ii = GetIndex(xx,yy)
					if ii == -1:
						continue
					if self.heightMap[ii] < minAlt:
						minAlt = self.heightMap[ii]
				print (i, "x:", x, "y:", y, "Alt:", myAlt, "minAlt:", minAlt, "TrueAlt:", self.heightMap[i])
				self.diffMap[i] = myAlt - minAlt

		NormalizeMap(self.diffMap,mc.width,mc.height)

		#zero out water tiles so percent is percent of land
		for y in range(mc.height):
			for x in range(mc.width):
				i = GetIndex(x,y)
				if self.isBelowSeaLevel(x,y):
					self.diffMap[i] = 0.0
					
		peakHeight = FindValueFromPercent(self.diffMap,mc.width,mc.height,mc.PeakPercent,0.01,True)
		hillHeight = FindValueFromPercent(self.diffMap,mc.width,mc.height,mc.HillPercent,0.01,True)

		self.plotMap = array('i')
		#initialize map with 0CEAN
		for i in range(0,mc.height*mc.width):
			self.plotMap.append(mc.OCEAN)

		for y in range(mc.height):
			for x in range(mc.width):
				i = GetIndex(x,y)
				altDiff = self.diffMap[i]
				if (self.heightMap[i] < hm.seaLevel):
					self.plotMap[i] = mc.OCEAN
				elif altDiff < hillHeight:
					self.plotMap[i] = mc.LAND
				elif altDiff < peakHeight:
					self.plotMap[i] = mc.HILLS
				else:
					self.plotMap[i] = mc.PEAK
		print "debug plot map"
		self.printPlotMap()
		
		#Randomize high altitude areas
		for y in range(mc.height):
			for x in range(mc.width):
				i = GetIndex(x,y)
				if self.plotMap[i] == mc.LAND:
					randomNum = PRand.random()
					if randomNum < mc.PeakChanceAtOne * self.getAltitudeAboveSeaLevel(x,y):
						self.plotMap[i] = mc.PEAK
					elif randomNum < mc.HillChanceAtOne * self.getAltitudeAboveSeaLevel(x,y):
						self.plotMap[i] = mc.HILLS

		#break up large clusters of hills and peaks
		for y in range(mc.height):
			for x in range(mc.width):
				i = GetIndex(x,y)
				if self.plotMap[i] == mc.HILLS and mc.smoothPeaks == 1:
					allHills = True
					for direction in range(1,9,1):
						xx,yy = GetXYFromDirection(x,y,direction)
						ii = GetIndex(xx,yy)
						if self.plotMap[ii] != mc.HILLS:
							allHills = False
					if allHills == True:
						self.plotMap[i] = mc.LAND
				if self.plotMap[i] == mc.PEAK and mc.smoothPeaks == 1:
					allPeaks = True
					peakCount = 0
					nextToOcean = False
					#print "peak at %d %d" % (x,y) #DEBUG
					# While we're here, let's eliminate seaside peaks
					for direction in range(1,9,1):
						xx,yy = GetXYFromDirection(x,y,direction)
						ii = GetIndex(xx,yy)
						if self.plotMap[ii] != mc.PEAK:
							allPeaks = False
						else:
							peakCount += 1
						if self.plotMap[ii] == mc.OCEAN:
						#print "nextToOcean %d %d" % (x,y) #DEBUG
							nextToOcean = True
					if allPeaks == True or peakCount > 3:
						self.plotMap[i] = mc.HILLS
					if nextToOcean == True:
						self.plotMap[i] = mc.HILLS
		
		return
	def createTerrainMap(self):
		print "creating terrain map"
		self.terrainMap = array('i')
		#initialize terrainMap with OCEAN
		for i in range(0,mc.height*mc.width):
			self.terrainMap.append(mc.OCEAN)

		#Find minimum rainfall on land
		minRain = 10.0
		for i in range(mc.width*mc.height):
			if self.plotMap[i] != mc.OCEAN:
				if self.rainFallMap[i] < minRain:
					minRain = self.rainFallMap[i]

		#zero water tiles to obtain percent of land			
		for y in range(mc.height):
			for x in range(mc.width):
				i = GetIndex(x,y)
				if self.isBelowSeaLevel(x,y):
					self.rainFallMap[i] = 0.0
					
		self.desertThreshold = FindValueFromPercent(self.rainFallMap,mc.width,mc.height,mc.DesertPercent,.001,False)
		self.plainsThreshold = FindValueFromPercent(self.rainFallMap,mc.width,mc.height,mc.PlainsPercent,.001,False)
		for y in range(mc.height):
			for x in range(mc.width):
				i = GetIndex(x,y)
				if self.plotMap[i] == mc.OCEAN:
					for direction in range (1,9,1):
						xx,yy = GetXYFromDirection(x,y,direction)
						ii = GetIndex(xx,yy)
						if ii == -1:
							continue
						if self.plotMap[ii] != mc.OCEAN:
							self.terrainMap[i] = mc.COAST

				#instead of harsh thresholds, allow a random deviation chance
				#based on how close to the threshold the rainfall is
				elif self.rainFallMap[i] < self.desertThreshold:
					if self.averageTempMap[i] < mc.SnowTemp:
						self.terrainMap[i] = mc.SNOW
					elif self.averageTempMap[i] < mc.TundraTemp:
						self.terrainMap[i] = mc.TUNDRA
					else:
						if self.rainFallMap[i] < (PRand.random() * (self.desertThreshold - minRain) + self.desertThreshold - minRain)/2.0 + minRain:
							self.terrainMap[i] = mc.DESERT
						else:
							self.terrainMap[i] = mc.PLAINS
				elif self.rainFallMap[i] < self.plainsThreshold:
					if self.averageTempMap[i] < mc.SnowTemp:
						self.terrainMap[i] = mc.SNOW
					elif self.averageTempMap[i] < mc.TundraTemp:
						self.terrainMap[i] = mc.TUNDRA
					else:
						if self.rainFallMap[i] < ((PRand.random() * (self.plainsThreshold - self.desertThreshold) + self.plainsThreshold - self.desertThreshold))/2.0 + self.desertThreshold: 
							self.terrainMap[i] = mc.PLAINS
						else:
							self.terrainMap[i] = mc.GRASS
				else:
					if self.averageTempMap[i] < mc.SnowTemp:
						self.terrainMap[i] = mc.SNOW
					elif self.averageTempMap[i] < mc.TundraTemp:
						self.terrainMap[i] = mc.TUNDRA
					else:
						self.terrainMap[i] = mc.GRASS

		#Make sure ice is always higher than tundra, and tundra is always higher than
		#everything else. Also, desert does not blend well with these so change it.
		for y in range(mc.height):
			for x in range(mc.width):
				i = GetIndex(x,y)
				if self.terrainMap[i] == mc.OCEAN or self.terrainMap[i] == mc.COAST:
					continue
				if self.terrainMap[i] == mc.SNOW:
					lowerFound = False
					for direction in range(1,9,1):
						xx,yy = GetXYFromDirection(x,y,direction)
						ii = GetIndex(xx,yy)
						if ii == -1:
							continue
						if self.terrainMap[ii] != mc.OCEAN and self.terrainMap[ii] != mc.COAST \
						and self.terrainMap[ii] != mc.SNOW:
							lowerFound = True
						if self.terrainMap[ii] != mc.TUNDRA and self.terrainMap[ii] != mc.SNOW and\
						self.terrainMap[ii] != mc.OCEAN and self.terrainMap[ii] != mc.COAST:
							self.terrainMap[i] = mc.TUNDRA
						if self.terrainMap[ii] == mc.DESERT:
							self.terrainMap[i] = mc.PLAINS
					if lowerFound and self.plotMap[i] == mc.LAND:
						self.plotMap[i] = mc.HILLS
				elif self.terrainMap[i] == mc.TUNDRA:
					lowerFound = False
					for direction in range(1,9,1):
						xx,yy = GetXYFromDirection(x,y,direction)
						ii = GetIndex(xx,yy)
						if ii == -1:
							continue
						if self.terrainMap[ii] != mc.OCEAN and self.terrainMap[ii] != mc.COAST \
						and self.terrainMap[ii] != mc.SNOW and self.terrainMap[ii] != mc.TUNDRA:
							lowerFound = True
						if self.terrainMap[ii] == mc.DESERT:
							self.terrainMap[i] = mc.PLAINS
					if lowerFound and self.plotMap[i] == mc.LAND:
						if PRand.random() < 0.5:
							self.plotMap[i] = mc.HILLS
						else:
							self.plotMap[i] = mc.PEAK
				else:
					higherFound = False
					for direction in range(1,9,1):
						xx,yy = GetXYFromDirection(x,y,direction)
						ii = GetIndex(xx,yy)
						if self.terrainMap[ii] == mc.SNOW or self.terrainMap[ii] == mc.TUNDRA:
							higherFound = True
					if higherFound and self.plotMap[i] != mc.LAND:
						self.plotMap[i] = mc.LAND
		return
	def cropMaps(self):
		hm.heightMap = CropMap(hm.heightMap)
		cm.averageTempMap = CropMap(cm.averageTempMap)
		cm.rainFallMap = CropMap(cm.rainFallMap)
		mc.hmWidth = mc.hmWidth - mc.westCrop - mc.eastCrop
		mc.hmHeight = mc.hmHeight - mc.northCrop - mc.southCrop

	def printHeightMap(self):
		print self.heightMap[:]
		lineString = "Height Map"
		print lineString
		for y in range(mc.height - 1,-1,-1):
			lineString = ""
			for x in range(0,mc.width,1):
				i = GetIndexGeneral(x,y,mc.width,mc.height)
				mapLoc = int((self.heightMap[i] - hm.seaLevel)/(1.0 - hm.seaLevel) * 10)
				#mapLoc = int(self.heightMap[i] * 10)
				if self.heightMap[i] < hm.seaLevel:
					lineString += '.'
				else:
					lineString += chr(mapLoc + 48)
			print lineString
		lineString = " "
		print lineString
		
	def printPlotMap(self):
		print "Plot Map"
		for y in range(mc.height - 1,-1,-1):
			lineString = ""
			for x in range(mc.width):
				mapLoc = self.plotMap[GetIndex(x,y)]
				if mapLoc == mc.PEAK:
					lineString += 'A'
				elif mapLoc == mc.HILLS:
					lineString += 'n'
				elif mapLoc == mc.LAND:
					lineString += '+'
				else:
					lineString += '.'
			print lineString
		lineString = " "
		print lineString
	def printTerrainMap(self):
		print "Terrain Map"
		wz = WindZones(mc.height,80,-80)
		for y in range(mc.height - 1,-1,-1):
			lineString = ""
			for x in range(mc.width):
				mapLoc = self.terrainMap[GetIndex(x,y)]
				if mapLoc == mc.OCEAN:
					lineString += ','
				elif mapLoc == mc.COAST:
					lineString += '.'
				elif mapLoc == mc.DESERT:
					lineString += 'D'
				elif mapLoc == mc.GRASS:
					lineString += '+'
				elif mapLoc == mc.MARSH:
					lineString += 'M'
				elif mapLoc == mc.PLAINS:
					lineString += 'P'
				elif mapLoc == mc.TUNDRA:
					lineString += 'T'
				elif mapLoc == mc.SNOW:
					lineString += 'I'
			lineString += "-" + wz.GetZoneName(wz.GetZone(y))
			print lineString
		lineString = " "
		print lineString

def isHmWaterMatch(x,y):
	i = GetHmIndex(x,y)
	if pb.distanceMap[i] > mc.minimumMeteorSize/3:
		return True
	return False

class PangaeaBreaker :
	def __init__(self):
		return
	def breakPangaeas(self):
		self.areaMap = Areamap(mc.hmWidth,mc.hmHeight,True,True)
		meteorThrown = False
		pangeaDetected = False
##		anotherPangaea = True
#		self.cm.PrintAreaMap()
##		while anotherPangaea:
##			NormalizeMap(hm.heightMap,mc.hmWidth,mc.hmHeight)
##			hm.calculateSeaLevel()
		self.createDistanceMap()
##		self.printDistanceMap()
		self.areaMap.defineAreas(isHmWaterMatch)
##		self.areaMap.PrintAreaMap()
		meteorCount = 0
		while not mc.AllowPangeas and self.isPangea() and meteorCount < mc.maximumMeteorCount:
			pangeaDetected = True
			x,y = self.getMeteorStrike()
			print "A meteor has struck the Earth at %(x)d, %(y)d!!" % {"x":x,"y":y}
			self.castMeteorUponTheEarth(x,y)
			meteorThrown = True
			meteorCount += 1
##			hm.printHeightMap()
			self.createDistanceMap()
##			self.printDistanceMap()
			self.areaMap.defineAreas(isHmWaterMatch)
##			self.areaMap.PrintAreaMap()
##			anotherPangaea = False
			
		if meteorThrown:
			print "The age of dinosours has come to a cataclysmic end."
		if meteorCount == 15:
			print "Maximum meteor count of %d has been reached. Pangaea may still exist." % meteorCount
		if mc.AllowPangeas:
			print "Pangeas are allowed on this map and will not be suppressed."
		elif pangeaDetected == False:
			print "No pangea detected on this map."
##		self.areaMap.PrintAreaMap()
	def isPangea(self):
##		starttime = time.clock()
		continentList = list()
		for a in self.areaMap.areaList:
			if a.water == False:
				continentList.append(a)

		totalLand = 0			 
		for c in continentList:
			totalLand += c.size
			
		#sort all the continents by size, largest first
		continentList.sort(lambda x,y:cmp(x.size,y.size))
		continentList.reverse()
		biggestSize = continentList[0].size
		if 0.70 < float(biggestSize)/float(totalLand):
##			endtime = time.clock()
##			elapsed = endtime - starttime
##			print "isPangea time = %(t)s" % {"t":str(elapsed)}
			return True
##		endtime = time.clock()
##		elapsed = endtime - starttime
##		print "isPangea time = "
##		print elapsed
##		print
		return False
	def getMeteorStrike(self):
##		starttime = time.clock()
		continentList = list()
		for a in self.areaMap.areaList:
			if a.water == False:
				continentList.append(a)
			
		#sort all the continents by size, largest first
		continentList.sort(lambda x,y:cmp(x.size,y.size))
		continentList.reverse()
		biggestContinentID = continentList[0].ID

		x,y = self.getHighestCentrality(biggestContinentID)

		return x,y
		
##		chokeList = list()
##		for y in range(mc.hmHeight):
##			for x in range(mc.hmWidth):
##				i = GetHmIndex(x,y)
##				if i == -1:
##					continue
##				if self.areaMap.areaMap[i] == biggestContinentID and\
##				not hm.isBelowSeaLevel(x,y): #this helps narrow the search
##					if self.isChokePoint(x,y,biggestContinentID):
####						print "chokepoint area at %d,%d = %d" % (x,y,biggestContinentID)
##						ap = AreaPlot(x,y)
##						chokeList.append(ap)
##		#calculate distances to center
##		center = self.getContinentCenter(biggestContinentID)
##		xCenter,yCenter = center
##
##		for n in range(len(chokeList)):
##			distance = self.getDistance(chokeList[n].x,chokeList[n].y,xCenter,yCenter)
##			chokeList[n].avgDistance = distance
##			
##		#sort plotList for most avg distance and chokeList for least
##		#average distance
##		chokeList.sort(lambda x,y:cmp(x.avgDistance,y.avgDistance))
##
##		if len(chokeList) == 0:#return bad value if no chokepoints
####			endtime = time.clock()
####			elapsed = endtime - starttime
####			print "getMeteorStrike time = "
####			print elapsed
####			print
##			return -1,-1
##
####		endtime = time.clock()
####		elapsed = endtime - starttime
####		print "getMeteorStrike time = "
####		print elapsed
####		print
##		
##		return chokeList[0].x,chokeList[0].y
				
	def isChokePoint(self,x,y,biggestContinentID):
		circlePoints = self.getCirclePoints(x,y,mc.minimumMeteorSize)
		waterOpposite = False
		landOpposite = False
		for cp in circlePoints:
			if isHmWaterMatch(cp.x,cp.y):
				#Find opposite
				ox = x + (x - cp.x)
				oy = y + (y - cp.y)
				if isHmWaterMatch(ox,oy):
					waterOpposite = True
			else:
				#Find opposite
				ox = x + (x - cp.x)
				oy = y + (y - cp.y)
				if not isHmWaterMatch(ox,oy):
					landOpposite = True
		if landOpposite and waterOpposite:
			percent = self.getLandPercentInCircle(circlePoints,biggestContinentID)
			if percent >= mc.minimumLandInChoke:
				return True
		return False
	def getLandPercentInCircle(self,circlePoints,biggestContinentID):
		land = 0
		water = 0
		circlePoints.sort(lambda n,m:cmp(n.y,m.y))
		for n in range(0,len(circlePoints),2):
			cy = circlePoints[n].y
			if circlePoints[n].x < circlePoints[n + 1].x:
				x1 = circlePoints[n].x
				x2 = circlePoints[n + 1].x
			else:
				x2 = circlePoints[n].x
				x1 = circlePoints[n + 1].x
			landLine,waterLine = self.countCraterLine(x1,x2,cy,biggestContinentID)
			land += landLine
			water += waterLine
		percent = float(land)/float(land + water)
		return percent
			
	def countCraterLine(self,x1,x2,y,biggestContinentID):
		land = 0
		water = 0
		for x in range(x1,x2 + 1):
			i = GetHmIndex(x,y)
			if self.areaMap.areaMap[i] == biggestContinentID:
				land += 1
			else:
				water += 1
		return land,water
		
	def getContinentCenter(self,ID):
		IDCount = 0
		xTotal = 0
		yTotal = 0
		for y in range(mc.hmHeight):
			for x in range(mc.hmWidth):
				i = GetHmIndex(x,y)
				if self.areaMap.areaMap[i] == ID:
					IDCount += 1
					xTotal += x
					yTotal += y
		xCenter = round(float(xTotal)/float(IDCount))
		yCenter = round(float(yTotal)/float(IDCount))
##		#first find center in x direction
##		changes = list()
##		yMin = mc.height
##		yMax = -1
##		meridianOverlap = False
##		onContinent = False
##		for x in range(mc.hmWidth):
##			continentFoundThisPass = False
##			for y in range(mc.hmHeight):
##				i = GetHmIndex(x,y)
##				if self.areaMap.areaMap[i] == ID:
##					continentFoundThisPass = True
##					if y < yMin:
##						yMin = y
##					elif y > yMax:
##						yMax = y
##			if x == 0 and continentFoundThisPass:
##				meridianOverlap = True
##				onContinent = True
##			if onContinent and not continentFoundThisPass:
##				changes.append(x)
##				onContinent = False
##			elif not onContinent and continentFoundThisPass:
##				changes.append(x)
##				onContinent = True
##		changes.sort()
##		xCenter = -1
##		if len(changes) == 0: #continent is continuous
##			xCenter = -1
##		elif len(changes) == 1:#continent extends to map edge
##			if meridianOverlap:
##				xCenter = changes[0]/2
##			else:
##				xCenter = (mc.width - changes[0])/2 + changes[0]
##		else:
##			if meridianOverlap:
##				xCenter = ((changes[1] - changes[0])/2 + changes[0] + (mc.hmWidth/2)) % mc.hmWidth
##			else:
##				xCenter = (changes[1] - changes[0])/2 + changes[0]
##		yCenter = (yMax - yMin)/2 + yMin
		center = xCenter,yCenter
		return center
	
	def getDistance(self,x,y,dx,dy):
		xx = x - dx
		if abs(xx) > mc.hmWidth/2:
			xx = mc.hmWidth - abs(xx)
			
		distance = max(abs(xx),abs(y - dy))
		return distance
	def castMeteorUponTheEarth(self,x,y):
##		starttime = time.clock()
		radius = PRand.randint(mc.minimumMeteorSize,max(mc.minimumMeteorSize + 1,mc.hmWidth/16))
		circlePointList = self.getCirclePoints(x,y,radius)
##		print "circlePointList"
##		print circlePointList
		circlePointList.sort(lambda n,m:cmp(n.y,m.y))
		for n in range(0,len(circlePointList),2):
			cy = circlePointList[n].y
			if circlePointList[n].x < circlePointList[n + 1].x:
				x1 = circlePointList[n].x
				x2 = circlePointList[n + 1].x
			else:
				x2 = circlePointList[n].x
				x1 = circlePointList[n + 1].x
			self.drawCraterLine(x1,x2,cy)
			
##		for n in range(0,len(circlePointList),2): not needed since this is happening on heightmap only
##			cy = circlePointList[n].y
##			if circlePointList[n].x < circlePointList[n + 1].x:
##				x1 = circlePointList[n].x
##				x2 = circlePointList[n + 1].x
##			else:
##				x2 = circlePointList[n].x
##				x1 = circlePointList[n + 1].x
##			self.drawCraterCoastLine(x1,x2,cy)
		return
	
##	def drawCraterCoastLine(self,x1,x2,y): not needed since this is happening on heightmap only
##		if y < 0 or y >= mc.hmHeight:
##			return
##		for x in range(x1,x2 + 1):
##			if self.hasLandNeighbor(x,y):
##				i = GetHmIndex(x,y)
##				sm.terrainMap[i] = mc.COAST				   
##		return
	def drawCraterLine(self,x1,x2,y):
		if y < 0 or y >= mc.hmHeight:
			return
		for x in range(x1,x2 + 1):
			i = GetHmIndex(x,y)
##			sm.terrainMap[i] = mc.OCEAN
			hm.heightMap[i] = 0.0
##			sm.plotMap[i] = mc.OCEAN
		return
##	def hasLandNeighbor(self,x,y): not needed since this is happening on heightmap only
##		#y cannot be outside of map so I'm not testing for it
##		for yy in range(y - 1,y + 2):
##			for xx in range(x - 1,x + 2):
##				if yy == y and xx == x:
##					continue
##				ii = GetHmIndex(xx,yy)
##				if sm.terrainMap[ii] != mc.COAST and sm.terrainMap[ii] != mc.OCEAN:
##					return True
##		return False
	def getCirclePoints(self,xCenter,yCenter,radius):
		circlePointList = list()
		x = 0
		y = radius
		p = 1 - radius

		self.addCirclePoints(xCenter,yCenter,x,y,circlePointList)

		while (x < y):
			x += 1
			if p < 0:
				p += 2*x + 1
			else:
				y -= 1
				p += 2*(x - y) + 1
			self.addCirclePoints(xCenter,yCenter,x,y,circlePointList)
			
		return circlePointList
	
	def addCirclePoints(self,xCenter,yCenter,x,y,circlePointList):
		circlePointList.append(CirclePoint(xCenter + x,yCenter + y))
		circlePointList.append(CirclePoint(xCenter - x,yCenter + y))
		circlePointList.append(CirclePoint(xCenter + x,yCenter - y))
		circlePointList.append(CirclePoint(xCenter - x,yCenter - y))
		circlePointList.append(CirclePoint(xCenter + y,yCenter + x))
		circlePointList.append(CirclePoint(xCenter - y,yCenter + x))
		circlePointList.append(CirclePoint(xCenter + y,yCenter - x))
		circlePointList.append(CirclePoint(xCenter - y,yCenter - x))
		return
	
	def createDistanceMap(self):
		self.distanceMap = array('i')
		processQueue = []
		for y in range(mc.hmHeight):
			for x in range(mc.hmWidth):
				if hm.isBelowSeaLevel(x,y):
					self.distanceMap.append(1000)
				else:
					self.distanceMap.append(0)
					processQueue.append((x,y))
					
		while len(processQueue) > 0:
			x,y = processQueue[0]
			i = GetHmIndex(x,y)
			del processQueue[0]
			distanceToLand = self.distanceMap[i]
			for direction in range(1,9,1):
				xx,yy = GetXYFromDirection(x,y,direction)
				ii = GetHmIndex(xx,yy)
				neighborDistanceToLand = self.distanceMap[ii]
				if neighborDistanceToLand > distanceToLand + 1:
					self.distanceMap[ii] = distanceToLand + 1
					processQueue.append((xx,yy))
			
	def printDistanceMap(self):
		lineString = "Pangaea Breaker distance map"
		print lineString
		for y in range(mc.hmHeight - 1,-1,-1):
			lineString = ""
			for x in range(0,mc.hmWidth,1):
				i = GetHmIndex(x,y)
				mapLoc = int(self.distanceMap[i])
				#mapLoc = int(self.heightMap[i] * 10)
				if mapLoc > 9:
					lineString += '.'
				else:
					lineString += chr(mapLoc + 48)
			print lineString
		lineString = " "
		print lineString
		
	def getHighestCentrality(self,ID):
		C = self.createCentralityList(ID)
		C.sort(lambda x,y:cmp(x.centrality,y.centrality))
		C.reverse()
		return C[0].x,C[0].y
	def createContinentList(self,ID):
		C = []
		indexMap = []
		gap = 5
		n = 0
		for y in range(0,mc.hmHeight):
			for x in range(0,mc.hmWidth):
				i = GetHmIndex(x,y)
##				print "h %% gap = %d, w %% gap = %d" % (y % gap,y % gap)
				if y % gap == 0 and x % gap == 0 and \
				self.areaMap.areaMap[i] == ID:
					C.append(CentralityScore(x,y))
					indexMap.append(n)
					n += 1
				else:
					indexMap.append(-1)

		n = 0
		for s in C:
##			print "s at %d,%d index %d is neighbors with" % (s.x,s.y,n)
			#Check 4 nieghbors
			xx = s.x - gap
			if xx < 0:
				xx = mc.hmWidth/gap * gap
			i = GetHmIndex(xx,s.y)
			if i != -1 and self.areaMap.areaMap[i] == ID:
				s.neighborList.append(indexMap[i])
##				print "%d,%d index %d" % (xx,s.y,indexMap[i])
			xx = s.x + gap
			if xx >= mc.hmWidth:
				xx = 0
			i = GetHmIndex(xx,s.y)
			if i != -1 and self.areaMap.areaMap[i] == ID:
				s.neighborList.append(indexMap[i])
##				print "%d,%d index %d" % (xx,s.y,indexMap[i])
			yy = s.y - gap
			if yy < 0:
				yy = mc.hmHeight/gap * gap
			i = GetHmIndex(s.x,yy)
			if i != -1 and self.areaMap.areaMap[i] == ID:
				s.neighborList.append(indexMap[i])
##				print "%d,%d index %d" % (s.x,yy,indexMap[i])
			yy = s.y + gap
			if yy > mc.hmHeight:
				yy = 0
			i = GetHmIndex(s.x,yy)
			if i != -1 and self.areaMap.areaMap[i] == ID:
				s.neighborList.append(indexMap[i])
##				print "%d,%d index %d" % (s.x,yy,indexMap[i])

			n += 1

##		self.areaMap.PrintAreaMap()
##		self.printContinentList(ID,gap)

		return C
			
	def printContinentList(self,ID,gap):
		lineString = "Continent neighbor map"
		print lineString
		for y in range(mc.hmHeight - 1,-1,-1):
			lineString = ""
			for x in range(0,mc.hmWidth,1):
				i = GetHmIndex(x,y)
				if y % gap == 0 and x % gap == 0 and \
				self.areaMap.areaMap[i] == ID:
					lineString += '@'
				elif self.areaMap.areaMap[i] == ID:
					lineString += '*'
				else:
					lineString += '.'
			print lineString
		lineString = " "
		print lineString
		
	
	def createCentralityList(self,ID):
		C = self.createContinentList(ID)
		
		for s in range(len(C)):
			S = []
			P = []
			sigma = []
			d = []
			delta = []
			for t in range(len(C)):
				sigma.append(0)
				d.append(-1)
				P.append([])
				delta.append(0)
			sigma[s] = 1
			d[s] = 0
			Q = []
			Q.append(s)
			while len(Q) > 0:
				v = Q.pop(0)
##				print len(Q)
				S.append(v)
				for w in C[v].neighborList:
					if d[w] < 0:
						Q.append(w)
#							print len(Q)
						d[w] = d[v] + 1
					if d[w] == d[v] + 1:
						sigma[w] = sigma[w] + sigma[v]
						P[w].append(v)
			while len(S) > 0:
				w = S.pop()
				for v in P[w]:
					delta[v] = delta[v] + (sigma[v]/sigma[w]) * (1 + delta[w])
					if w != s:
						C[w].centrality = C[w].centrality + delta[w]
##			print s
		
		return C
	
	def isNeighbor(self,x,y,xx,yy):
			#Check X for wrap
		if mc.WrapX == True:
			mx = xx % mc.hmWidth
		elif x < 0 or x >= mc.hmWidth:
			return False
		else:
			mx = xx
		#Check y for wrap
		if mc.WrapY == True:
			my = yy % mc.hmHeight
		elif y < 0 or y >= mc.hmHeight:
			return False
		else:
			my = yy

		if abs(x - mx) <= 1 and abs(y - my) <= 1:
			if x == mx and y == my:
				return False
			else:
				return True
		return False
			
				
					
pb = PangaeaBreaker()

class CirclePoint :
	def __init__(self,x,y):
		self.x = x
		self.y = y
class CentralityScore :
	def __init__(self,x,y):
		self.x = x
		self.y = y
		self.centrality = 0
		self.neighborList = []
		
def isNonCoastWaterMatch(x,y):
	i = GetIndex(x,y)
	if sm.terrainMap[i] == mc.OCEAN:
		return True
	return False
		
class ContinentMap :
	def __init__(self):
		return
	def generateContinentMap(self):
		self.areaMap = Areamap(mc.width,mc.height,True,True)
		self.areaMap.defineAreas(isNonCoastWaterMatch)
##		self.areaMap.PrintAreaMap()
		self.newWorldID = self.getNewWorldID()
#		self.cm.PrintAreaMap()
		return
		
	def getNewWorldID(self):
		nID = 0
		continentList = list()
		for a in self.areaMap.areaList:
			if a.water == False:
				continentList.append(a)

		totalLand = 0			 
		for c in continentList:
			totalLand += c.size
			
##		print totalLand

		#sort all the continents by size, largest first
#		continentList.sort(key=operator.attrgetter('size'),reverse=True)
		continentList.sort(lambda x,y:cmp(x.size,y.size))
		continentList.reverse()
		
		print ''
		print "All continents"
		print self.areaMap.PrintList(continentList)

		#now remove a percentage of the landmass to be considered 'Old World'
		oldWorldSize = 0
		#biggest continent is automatically 'Old World'
		oldWorldSize += continentList[0].size
		del continentList[0]

		#If this was the only continent than we have a pangaea. Oh well.
		if len(continentList) == 0:
			return -1
		
		#get the next largest continent and temporarily remove from list
		#add it back later and is automatically 'New World'
		biggestNewWorld = continentList[0]
		del continentList[0]
		
		#sort list by ID rather than size to make things
		#interesting and possibly bigger new worlds
#		continentList.sort(key=operator.attrgetter('ID'),reverse=True)
		continentList.sort(lambda x,y:cmp(x.ID,y.ID))
		continentList.reverse()
		
		for n in range(len(continentList)):
			oldWorldSize += continentList[0].size
		# Don't delete "new worlds" from the list if we're going to
			# put everyone on the "old world" continent
			if mc.ShareContinent == False:
				del continentList[0]
			if float(oldWorldSize)/float(totalLand) > 0.60:
				break

		#add back the biggestNewWorld continent
		continentList.append(biggestNewWorld)
		
		#what remains in the list will be considered 'New World'
		print ''
		print "New World Continents"
		print self.areaMap.PrintList(continentList)

		#get ID for the next continent, we will use this ID for 'New World'
		#designation
		nID = continentList[0].ID
		del continentList[0] #delete to avoid unnecessary overwrite

		#now change all the remaining continents to also have nID as their ID
		for i in range(mc.height*mc.width):
			for c in continentList:
				if c.ID == self.areaMap.areaMap[i]:
					self.areaMap.areaMap[i] = nID
 
		return nID
continentMap = ContinentMap()

class Areamap :
	def __init__(self,width,height,b8connected,bSwitch4Or8OnFalseMatch):
		self.mapWidth = width
		self.mapHeight = height
		self.areaMap = array('i')
		self.b8connected = b8connected
		self.bSwitch4Or8OnFalseMatch = bSwitch4Or8OnFalseMatch
		#initialize map with zeros
		for i in range(0,self.mapHeight*self.mapWidth):
			self.areaMap.append(0)
		return
	def defineAreas(self,matchFunction):
#		self.areaSizes = array('i')
##		starttime = time.clock()
		self.areaList = list()
		areaID = 0
		#make sure map is erased in case it is used multiple times
		for i in range(0,self.mapHeight*self.mapWidth):
			self.areaMap[i] = 0
#		for i in range(0,1):
		for i in range(0,self.mapHeight*self.mapWidth):
			if self.areaMap[i] == 0: #not assigned to an area yet
				areaID += 1
				areaSize,match = self.fillArea(i,areaID,matchFunction)
				area = Area(areaID,areaSize,match)
				self.areaList.append(area)

##		endtime = time.clock()
##		elapsed = endtime - starttime
##		print "defineAreas time ="
##		print elapsed
##		print

		return

##	def isWater(self,x,y,coastIsLand):
##		#coastIsLand = True means that we are trying to find continents that
##		#are not connected by coasts to the main landmasses, allowing us to
##		#find continents suitable as a 'New World'. Otherwise, we
##		#are just looking to fill in lakes and coast needs to be considered
##		#water in that case
##		ii = self.getIndex(x,y)
##		if ii == -1:
##			return False
##		if coastIsLand:
##			if hm.plotMap[ii] == hm.OCEAN and terr.terrainMap[ii] != terr.COAST:
##				return True
##			else:
##				return False
##		else:
##			if hm.isBelowSeaLevel(x,y):
##				return True
##			else:
##				return False
##			
##		return False
	def getAreaByID(self,areaID):
		for i in range(len(self.areaList)):
			if self.areaList[i].ID == areaID:
				return self.areaList[i]
		return None
	def getOceanID(self):
#		self.areaList.sort(key=operator.attrgetter('size'),reverse=True)
		self.areaList.sort(lambda x,y:cmp(x.size,y.size))
		self.areaList.reverse()
		for a in self.areaList:
			if a.water == True:
				return a.ID
						
	def getIndex(self,x,y):
		#Check X for wrap
		if mc.WrapX == True:
			xx = x % self.mapWidth
		elif x < 0 or x >= self.mapWidth:
			return -1
		else:
			xx = x
		#Check y for wrap
		if mc.WrapY == True:
			yy = y % self.mapHeight
		elif y < 0 or y >= self.mapHeight:
			return -1
		else:
			yy = y

		i = yy * self.mapWidth + xx
		return i
	
	def fillArea(self,index,areaID,matchFunction):
		#first divide index into x and y
		y = index/self.mapWidth
		x = index%self.mapWidth
		#We check 8 neigbors for land,but 4 for water. This is because
		#the game connects land squares diagonally across water, but
		#water squares are not passable diagonally across land
		self.segStack = list()
		self.size = 0
		matchValue = matchFunction(x,y)
		#place seed on stack for both directions
		seg = LineSegment(y,x,x,1)
		self.segStack.append(seg) 
		seg = LineSegment(y+1,x,x,-1)
		self.segStack.append(seg) 
		while(len(self.segStack) > 0):
			seg = self.segStack.pop()
			self.scanAndFillLine(seg,areaID,matchValue,matchFunction)
##			if (seg.y < 8 and seg.y > 4) or (seg.y < 70 and seg.y > 64):
##			if (areaID == 4
##				PrintPlotMap(hm)
##				self.PrintAreaMap()
		
		return self.size,matchFunction(x,y)
	def scanAndFillLine(self,seg,areaID,matchValue,matchFunction):
		#check for y + dy being off map
		i = self.getIndex(seg.xLeft,seg.y + seg.dy)
		if i < 0:
##			print "scanLine off map ignoring",str(seg)
			return
		debugReport = False
##		if (seg.y < 8 and seg.y > 4) or (seg.y < 70 and seg.y > 64):
##		if (areaID == 4):
##			debugReport = True
		#for land tiles we must look one past the x extents to include
		#8-connected neighbors
		if self.b8connected:
			if self.bSwitch4Or8OnFalseMatch and matchValue:
				landOffset = 0
			else:
				landOffset = 1
		else:
			if self.bSwitch4Or8OnFalseMatch and matchValue:
				landOffset = 1
			else:
				landOffset = 0
		
		lineFound = False
		#first scan and fill any left overhang
		if debugReport:
			print ""
			print "areaID = %(a)4d" % {"a":areaID}
			print "matchValue = %(w)2d, landOffset = %(l)2d" % {"w":matchValue,"l":landOffset} 
			print str(seg)
			print "Going left"
		if mc.WrapX == True:
			xStop = 0 - (self.mapWidth*20)
		else:
			xStop = -1
		for xLeftExtreme in range(seg.xLeft - landOffset,xStop,-1):
			i = self.getIndex(xLeftExtreme,seg.y + seg.dy)
			if debugReport:
				print "xLeftExtreme = %(xl)4d" % {'xl':xLeftExtreme}
			if debugReport:
				print "i = %d, seg.y + seg.dy = %d" % (i,seg.y + seg.dy)
				print "areaMap[i] = %d, matchValue match = %d" % (self.areaMap[i],matchValue == matchFunction(xLeftExtreme,seg.y + seg.dy))
			if self.areaMap[i] == 0 and matchValue == matchFunction(xLeftExtreme,seg.y + seg.dy):
				self.areaMap[i] = areaID
				self.size += 1
				lineFound = True
			else:
				#if no line was found, then xLeftExtreme is fine, but if
				#a line was found going left, then we need to increment
				#xLeftExtreme to represent the inclusive end of the line
				if lineFound:
					xLeftExtreme += 1
				break
		if debugReport:
			print "xLeftExtreme finally = %(xl)4d" % {'xl':xLeftExtreme}
			print "Going Right"
		#now scan right to find extreme right, place each found segment on stack
#		xRightExtreme = seg.xLeft - landOffset #needed sometimes? one time it was not initialized before use.
		xRightExtreme = seg.xLeft #needed sometimes? one time it was not initialized before use.
		if mc.WrapX == True:
			xStop = self.mapWidth*20
		else:
			xStop = self.mapWidth
		for xRightExtreme in range(seg.xLeft + lineFound - landOffset,xStop,1):
			if debugReport:			
				print "xRightExtreme = %(xr)4d" % {'xr':xRightExtreme}
			i = self.getIndex(xRightExtreme,seg.y + seg.dy)
			if debugReport:
				print "i = %d, seg.y + seg.dy = %d" % (i,seg.y + seg.dy)
				print "areaMap[i] = %d, matchValue match = %d" % (self.areaMap[i],matchValue == matchFunction(xRightExtreme,seg.y + seg.dy))
			if self.areaMap[i] == 0 and matchValue == matchFunction(xRightExtreme,seg.y + seg.dy):
				self.areaMap[i] = areaID
				self.size += 1
				if lineFound == False:
					lineFound = True
					xLeftExtreme = xRightExtreme #starting new line
					if debugReport:
						print "starting new line at xLeftExtreme= %(xl)4d" % {'xl':xLeftExtreme}
			elif lineFound == True: #found the right end of a line segment!				
				lineFound = False
				#put same direction on stack
				newSeg = LineSegment(seg.y + seg.dy,xLeftExtreme,xRightExtreme - 1,seg.dy)
				self.segStack.append(newSeg)
				if debugReport:
					print "same direction to stack",str(newSeg)
				#determine if we must put reverse direction on stack
				if xLeftExtreme < seg.xLeft or xRightExtreme >= seg.xRight:
					#out of shadow so put reverse direction on stack also
					newSeg = LineSegment(seg.y + seg.dy,xLeftExtreme,xRightExtreme - 1,-seg.dy)
					self.segStack.append(newSeg)
					if debugReport:
						print "opposite direction to stack",str(newSeg)
				if xRightExtreme >= seg.xRight + landOffset:
					if debugReport:
						print "finished with line"
					break; #past the end of the parent line and this line ends
			elif lineFound == False and xRightExtreme >= seg.xRight + landOffset:
				if debugReport:
					print "no additional lines found"
				break; #past the end of the parent line and no line found
			else:
				continue #keep looking for more line segments
		if lineFound == True: #still a line needing to be put on stack
			if debugReport:
				print "still needing to stack some segs"
			lineFound = False
			#put same direction on stack
			newSeg = LineSegment(seg.y + seg.dy,xLeftExtreme,xRightExtreme - 1,seg.dy)
			self.segStack.append(newSeg)
			if debugReport:
				print str(newSeg)
			#determine if we must put reverse direction on stack
			if xLeftExtreme < seg.xLeft or xRightExtreme - 1 > seg.xRight:
				#out of shadow so put reverse direction on stack also
				newSeg = LineSegment(seg.y + seg.dy,xLeftExtreme,xRightExtreme - 1,-seg.dy)
				self.segStack.append(newSeg)
				if debugReport:
					print str(newSeg)
		
		return
	#for debugging
	def PrintAreaMap(self):
		
		print "Area Map"
		for y in range(self.mapHeight - 1,-1,-1):
			lineString = ""
			for x in range(self.mapWidth):
				mapLoc = self.areaMap[self.getIndex(x,y)]
				if mapLoc + 34 > 127:
					mapLoc = 127 - 34
				lineString += chr(mapLoc + 34)
			lineString += "-" + str(y)
			print lineString
		oid = self.getOceanID()
		if oid == None or oid + 34 > 255:
			print "Ocean ID is unknown"
		else:
			print "Ocean ID is %(oid)4d or %(c)s" % {'oid':oid,'c':chr(oid + 34)}
		lineString = " "
		print lineString

		return
	def PrintList(self,s):
		for a in s:
			char = chr(a.ID + 34)
			lineString = str(a) + ' ' + char
			print lineString
			
class LineSegment :
	def __init__(self,y,xLeft,xRight,dy):
		self.y = y
		self.xLeft = xLeft
		self.xRight = xRight
		self.dy = dy
	def __str__ (self):
		string = "y = %(y)3d, xLeft = %(xl)3d, xRight = %(xr)3d, dy = %(dy)2d" % \
		{'y':self.y,'xl':self.xLeft,'xr':self.xRight,'dy':self.dy}
		return string
					   
class Area :
	def __init__(self,iD,size,water):
		self.ID = iD
		self.size = size
		self.water = water

	def __str__(self):
		string = "{ID = %(i)4d, size = %(s)4d, water = %(w)1d}" % \
		{'i':self.ID,'s':self.size,'w':self.water}
		return string
class AreaPlot :
	def __init__(self,x,y):
		self.x = x
		self.y = y
		self.avgDistance = -1
		
#OK! now that directions N,S,E,W are important, we have to keep in mind that
#the map plots are ordered from 0,0 in the SOUTH west corner! NOT the northwest
#corner! That means that Y increases as you go north.
class RiverMap :
	def __init__(self):
		#To provide global access without allocating alot of resources for
		#nothing, object initializer must be empty
		return
	def generateRiverMap(self):
		self.L = 0 #also denotes a 'pit' or 'flat'
		self.N = 1
		self.S = 2
		self.E = 3
		self.W = 4
		self.NE = 5
		self.NW = 6
		self.SE = 7
		self.SW = 8
		self.O = 5 #used for ocean or land without a river

		#averageHeightMap, flowMap, averageRainfallMap and drainageMap are offset from the other maps such that
		#each element coincides with a four tile intersection on the game map
		self.averageHeightMap = array('d')
		self.flowMap = array('i')
		self.averageRainfallMap = array('d')		
		self.drainageMap = array('d')
		self.riverMap = array('i')
		#initialize maps with zeros
		for i in range(0,mc.height*mc.width):
			self.averageHeightMap.append(0.0)
			self.flowMap.append(0)
			self.averageRainfallMap.append(0.0)
			self.drainageMap.append(0.0)
			self.riverMap.append(self.O)
		#Get highest intersection neighbor
		for y in range(mc.height):
			for x in range(mc.width):
				i = GetIndex(x,y)
				maxHeight = 0.0;
				for yy in range(y,y-2,-1):
					for xx in range(x,x+2):
						ii = GetIndex(xx,yy)
						#use an average hight of <0 to denote an ocean border
						#this will save processing time later
						if(sm.plotMap[ii] == mc.OCEAN):
							maxHeight = -100.0
						elif maxHeight < sm.heightMap[ii] and maxHeight >= 0:
							maxHeight = sm.heightMap[ii]
				self.averageHeightMap[i] = maxHeight
		#Now try to silt in any lakes
		self.siltifyLakes()
		self.createLakeDepressions()
		#create flowMap by checking for the lowest of each 4 connected
		#neighbor plus self	   
		for y in range(mc.height):
			for x in range(mc.width):
				i = GetIndex(x,y)
				lowestAlt = self.averageHeightMap[i]
				if(lowestAlt < 0.0):
					#if height is <0 then that means this intersection is
					#adjacent to an ocean and has no flow
					self.flowMap[i] = self.O
				else:
					#First assume this place is lowest, like a 'pit'. Then
					#for each place that is lower, add it to a list to be
					#randomly chosen as the drainage path
					drainList = list()
					nonDrainList = list()
					self.flowMap[i] = self.L 
					ii = GetIndex(x,y+1)
					#in the y direction, avoid wrapping
					if(y > 0 and self.averageHeightMap[ii] < lowestAlt):
						drainList.append(self.N)
					else:
						nonDrainList.append(self.N)
					ii = GetIndex(x,y-1)
					if(y < mc.height - 1 and self.averageHeightMap[ii] < lowestAlt):
						drainList.append(self.S)
					else:
						nonDrainList.append(self.S)
					ii = GetIndex(x-1,y)
					if(self.averageHeightMap[ii] < lowestAlt):
						drainList.append(self.W)
					else:
						nonDrainList.append(self.W)
					ii = GetIndex(x+1,y)
					if(self.averageHeightMap[ii] < lowestAlt):
						drainList.append(self.E)
					else:
						nonDrainList.append(self.E)
						
					#never go straight when you have other choices
					count = len(drainList)
					if count == 3:
						oppDir = GetOppositeDirection(nonDrainList[0])
						for n in range(count):
							if drainList[n] == oppDir:
								del drainList[n]
								break
						count = len(drainList)
							
					if count > 0:
						choice = int(PRand.random()*count)
#						print count,choice
						self.flowMap[i] = drainList[choice]
				  
		#Create average rainfall map so that each intersection is an average
		#of the rainfall from rm.rainMap
		for y in range(mc.height):
			for x in range(mc.width):
				i = GetIndex(x,y)
				avg = 0.0;
				for yy in range(y,y-2,-1):
					for xx in range(x,x+2):
						ii = GetIndex(xx,yy)
						avg += sm.rainFallMap[ii]
				avg = avg/4.0
				self.averageRainfallMap[i] = avg
			   
		#Now use the flowMap as a guide to distribute average rainfall.
		#Wherever the most rainfall ends up is where the rivers will be.
		print "Distributing rainfall"
		for y in range(mc.height):
			for x in range(mc.width):
				i = GetIndex(x,y)
				flow = self.flowMap[i]
				rainFall = self.averageRainfallMap[i]
				xx = x
				yy = y
				loop = 1
				hereSeen = {}
				while(flow != self.L and flow != self.O):
					loop += 1
					if(loop > 512):
						raise ValueError, "Rainfall infinite loop"

					if(flow == self.N):
						yy += 1
					elif(flow == self.S):
						yy -= 1
					elif(flow == self.W):
						xx -= 1
					elif(flow == self.E):
						xx += 1
					#wrap
					if(xx < 0):
						xx = mc.width - 1
					elif(xx >= mc.width):
						xx = 0
					if(yy < 0):
						yy = mc.height - 1
					elif(yy >= mc.height):
						yy = 0
					#dump rainfall here
					ii = GetIndex(xx,yy)
					self.drainageMap[ii] += rainFall
					#reset flow
					flow = self.flowMap[ii]
					if ii in hereSeen:
						flow = self.O # Break loop
					hereSeen[ii] = True
					
		
		riverThreshold = sm.plainsThreshold * mc.RiverThreshold
		for i in range(mc.height*mc.width):
			if(self.drainageMap[i] > riverThreshold):
##					riverCount += 1
				self.riverMap[i] = self.flowMap[i]
			else:
				self.riverMap[i] = self.O

		#at this point river should be in tolerance or close to it
		#riverMap is ready for use

	def rxFromPlot(self,x,y,direction):
		if direction == self.NE:
			return x,y + 1
		if direction == self.SW:
			return x - 1,y 
		if direction == self.SE:
			return x,y 
		raise ValueError,"rxFromPlot using bad direction input"
	
	def siltifyLakes(self):
		lakeList = []
		onQueueMap = array('i')
		for y in range(mc.height):
			for x in range(mc.width):
				onQueueMap.append(0)
				i = GetIndex(x,y)
				if self.isLake(x,y):
					lakeList.append((x,y,1))
					onQueueMap[i] = 1
##		print "initial lakes = %d" % (len(lakeList))
		largestLength = len(lakeList)
		while len(lakeList) > 0:
##			print "len = %d" % (len(lakeList))
			if len(lakeList) > largestLength:
				largestLength = len(lakeList)
			x,y,lakeSize = lakeList[0]
			del lakeList[0]
			i = GetIndex(x,y)
			onQueueMap[i] = 0

			if lakeSize > mc.maxSiltPanSize:
				continue
			lakeSize += 1
##			print x,y
			lowestNeighborAlt = self.getLowestNeighborAltitude(x,y)
			self.averageHeightMap[i] = lowestNeighborAlt + 0.005
			for direction in range(1,5,1):
				xx,yy = GetXYFromDirection(x,y,direction)
				ii = GetIndex(xx,yy)
				if ii == -1:
					continue
				if self.isLake(xx,yy) and onQueueMap[ii] == 0:
##					print "appending lake at %d,%d" % (xx,yy)
					lakeList.append((xx,yy,lakeSize))
					onQueueMap[ii] = 1
##		print "returning from siltify"
##		print "largest length of lakeList = %d" % largestLength
		return
	def isLake(self,x,y):
		i = GetIndex(x,y)
		alt = self.averageHeightMap[i]
		if alt < 0.0:
			return False
		for direction in range(1,5,1):
			xx,yy = GetXYFromDirection(x,y,direction)
			ii = GetIndex(xx,yy)
			if ii == -1:
				continue
			if self.averageHeightMap[ii] < alt:
				return False
		return True
	def getLowestNeighborAltitude(self,x,y):
		lowest = 1.0
		for direction in range(1,5,1):
			xx,yy = GetXYFromDirection(x,y,direction)
			ii = GetIndex(xx,yy)
			if ii == -1:
				continue
			if self.averageHeightMap[ii] < lowest:
				lowest = self.averageHeightMap[ii]
		return lowest
	def createLakeDepressions(self):
		lakeList = []
		for y in range(mc.height):
			for x in range(mc.width):
				i = GetIndex(x,y)
				if self.averageHeightMap[i] > mc.minLakeAltitude:
					lakeList.append((x,y))
		lakeList = ShuffleList(lakeList)
		numLakes = int(mc.height * mc.width * mc.numberOfLakesPerPlot)
#		for n in range(numLakes):
#			x,y = lakeList[n]
#			i = GetIndex(x,y)
#			lowestAlt = self.getLowestNeighborAltitude(x,y)
#			if lowestAlt < 0.0:
#				continue
#			self.averageHeightMap[i] = lowestAlt - 0.001
		
	
	def printRiverMap(self):
		print "River Map"
		wz = WindZones(mc.height,80,-80)
		for y in range(mc.height - 1,-1,-1):
			lineString = ""
			for x in range(mc.width):
				mapLoc = self.riverMap[GetIndex(x,y)]
				if mapLoc == self.O:
					lineString += '.'
				elif mapLoc == self.L:
					lineString += 'L'
				elif mapLoc == self.N:
					lineString += 'N'
				elif mapLoc == self.S:
					lineString += 'S'
				elif mapLoc == self.E:
					lineString += 'E'
				elif mapLoc == self.W:
					lineString += 'W'
			lineString += "-" + wz.GetZoneName(wz.GetZone(y))
			print lineString
		lineString = " "
		print lineString
			
	def printFlowMap(self):
		print "Flow Map"
		wz = WindZones(mc.height,80,-80)
		for y in range(mc.height - 1,-1,-1):
			lineString = ""
			for x in range(mc.width):
				mapLoc = self.flowMap[GetIndex(x,y)]
				if mapLoc == self.O:
					lineString += '.'
				elif mapLoc == self.L:
					lineString += 'L'
				elif mapLoc == self.N:
					lineString += 'N'
				elif mapLoc == self.S:
					lineString += 'S'
				elif mapLoc == self.E:
					lineString += 'E'
				elif mapLoc == self.W:
					lineString += 'W'
			lineString += "-" + wz.GetZoneName(wz.GetZone(y))
			print lineString
		lineString = " "
		print lineString
	def printRiverAndTerrainAlign(self):
		print "River Alignment Check"
		for y in range(mc.height - 1,-1,-1):
			lineString1 = ""
			lineString2 = ""
			for x in range(mc.width):
				mapLoc = sm.terrainMap[GetIndex(x,y)]
				if mapLoc == mc.OCEAN:
					lineString1 += ',.'
				elif mapLoc == mc.COAST:
					lineString1 += ',.'
				elif mapLoc == mc.DESERT:
					lineString1 += 'D.'
				elif mapLoc == mc.GRASS:
					lineString1 += 'R.'
				elif mapLoc == mc.PLAINS:
					lineString1 += 'P.'
				elif mapLoc == mc.TUNDRA:
					lineString1 += 'T.'
				elif mapLoc == mc.MARSH:
					lineString1 += 'M.'
				elif mapLoc == mc.SNOW:
					lineString1 += 'I.'
				mapLoc = rm.riverMap[GetIndex(x,y)]
				if mapLoc == rm.O:
					lineString2 += '..'
				elif mapLoc == rm.L:
					lineString2 += '.L'
				elif mapLoc == rm.N:
					lineString2 += '.^'
				elif mapLoc == rm.S:
					lineString2 += '.v'
				elif mapLoc == rm.E:
					lineString2 += '.>'
				elif mapLoc == rm.W:
					lineString2 += '.<'
##			lineString1 += "-" + wz.GetZoneName(wz.GetZone(y))
##			lineString2 += "-" + wz.GetZoneName(wz.GetZone(y))
			print lineString1
			print lineString2
		lineString1 = " "
		print lineString1
class EuropeMap :
	def __init__(self):
		return
	def initialize(self):
		self.europeMap = array('i')
		for i in range(mc.width*mc.height):
			self.europeMap.append(0)
			
class BonusPlacer :
	def __init__(self):
		return
	def AddBonuses(self):
		gc = CyGlobalContext()
		CyMap().recalculateAreas()
		self.AssignBonusAreas()
		numBonuses = gc.getNumBonusInfos()
		#Create a list of map indices and shuffle them
		plotIndexList = []
		for i in range(mc.height*mc.width):
			plotIndexList.append(i)
		plotIndexList = ShuffleList(plotIndexList)

		#AIAndy - Check which placement orders are used, discard -1
		orderSet = {}
		for i in range(numBonuses):
			bonusInfo = gc.getBonusInfo(self.bonusList[i].eBonus)
			porder = bonusInfo.getPlacementOrder()
			if porder >= 0:
				orderSet[porder] = 1
		porderList = sorted(orderSet.keys())
		startAtIndex = 0
		for order in porderList:
			placementList = []
			for i in range(numBonuses):
				bonusInfo = gc.getBonusInfo(self.bonusList[i].eBonus)
				if bonusInfo.getPlacementOrder() == order:
					for n in range(self.bonusList[i].desiredBonusCount):
						placementList.append(self.bonusList[i].eBonus)
			if len(placementList) > 0:
				placementList = ShuffleList(placementList)
				for eBonus in placementList:
					startAtIndex = self.AddBonusType(eBonus, plotIndexList, startAtIndex)
		#now check to see that all resources have been placed at least once, this
		#pass ignoring area rules
		for i in range(numBonuses):
			bonus = self.bonusList[i]
			if bonus.currentBonusCount == 0 and bonus.desiredBonusCount > 0:
				startAtIndex = self.AddEmergencyBonus(bonus, False, plotIndexList, startAtIndex)
		#now check again to see that all resources have been placed at least once,
		#this time ignoring area rules and also class spacing
		for i in range(numBonuses):
			bonus = self.bonusList[i]
			if bonus.currentBonusCount == 0 and bonus.desiredBonusCount > 0:
				startAtIndex = self.AddEmergencyBonus(bonus, True, plotIndexList, startAtIndex)
		#now report resources that simply could not be placed
		for i in range(numBonuses):
			bonus = self.bonusList[i]
			bonusInfo = gc.getBonusInfo(bonus.eBonus)
			if bonus.currentBonusCount == 0 and bonus.desiredBonusCount > 0:
				print "No room at all found for %(bt)s!!!" % {"bt":bonusInfo.getType()}
			print "Placed %(cb)d, desired %(db)d for %(bt)s" % {"cb":bonus.currentBonusCount, "db":bonus.desiredBonusCount, "bt":bonusInfo.getType()}
		return
	def AddEmergencyBonus(self, bonus, ignoreClass, plotIndexList, startAtIndex):
		gc = CyGlobalContext()
		bonusInfo = gc.getBonusInfo(bonus.eBonus)
		plotListLength = len(plotIndexList)
		lastI = 0
		fFloodPlains = gc.getInfoTypeForString("FEATURE_FLOOD_PLAINS")
		fOasis       = gc.getInfoTypeForString("FEATURE_OASIS")
		fCoral       = gc.getInfoTypeForString("FEATURE_REEF")
		fReef        = gc.getInfoTypeForString("FEATURE_REEF")
		fIsland      = gc.getInfoTypeForString("FEATURE_ISLAND")
		fIslandNorth = gc.getInfoTypeForString("FEATURE_ISLAND_NORTH")
		fKelp         = gc.getInfoTypeForString("FEATURE_REEF")
		fShallowCoral = gc.getInfoTypeForString("FEATURE_REEF")
		fDeepCoral    = gc.getInfoTypeForString("FEATURE_REEF")
		for i in range(startAtIndex, startAtIndex + plotListLength):
			index = 0
			lastI = i
			if i >= plotListLength:
				index = plotIndexList[i - plotListLength]
			else:
				index = plotIndexList[i]
			plot = CyMap().plotByIndex(index)
			x = plot.getX()
			y = plot.getY()
			featureEnum = plot.getFeatureType()
			requiredFeature = (featureEnum == fFloodPlains or featureEnum == fOasis or featureEnum == fCoral or featureEnum == fReef or featureEnum == fIsland or featureEnum == fIslandNorth)
			if ((ignoreClass and self.PlotCanHaveBonus(plot, bonus.eBonus, False, True)) or self.CanPlaceBonusAt(plot, bonus.eBonus, False, True)) and not requiredFeature:
				#temporarily remove any feature
				if featureEnum != FeatureTypes.NO_FEATURE:
					featureVariety = plot.getFeatureVariety()
					plot.setFeatureType(FeatureTypes.NO_FEATURE, -1)
				#place bonus
				plot.setBonusType(bonus.eBonus)
				bonus.currentBonusCount += 1
				#restore the feature if possible
				if featureEnum != FeatureTypes.NO_FEATURE:
					if bonusInfo == None or bonusInfo.isFeature(featureEnum):
						plot.setFeatureType(featureEnum, featureVariety)
				print "Emergency placement of 1 %(bt)s" % {"bt":bonusInfo.getType()}
				break
		lastI = (lastI + 1) % plotListLength
		return lastI
	def AddBonusType(self, eBonus, plotIndexList, startAtIndex):
		#first get bonus/area link
		bonus = self.bonusList[self.bonusDict[eBonus]]
		if bonus.currentBonusCount >= bonus.desiredBonusCount:
			return False
		gc = CyGlobalContext()
		bonusInfo = gc.getBonusInfo(eBonus)
		bonusPlaced = False
		plotListLength = len(plotIndexList)
		lastI = 0
		#now add bonuses
		for i in range(startAtIndex, startAtIndex + plotListLength):
			index = 0
			lastI = i
			if i >= plotListLength:
				index = plotIndexList[i - plotListLength]
			else:
				index = plotIndexList[i]
			plot = CyMap().plotByIndex(index)
			x = plot.getX()
			y = plot.getY()
			if self.CanPlaceBonusAt(plot, eBonus, False, False):
				#place bonus
				plot.setBonusType(eBonus)
				bonusPlaced = True
				bonus.currentBonusCount += 1
				groupRange = bonusInfo.getGroupRange()
				#NEW CODE - Fuyu/LM
				#added/maxAdd: avoid grouping ALL the resources of a type together.
				#it's annoying to find 6 wines together and nowhere else on the map.
				added = 0
				if (mc.BonusMaxGroupSize == -1):
					maxAdd = (gc.getMap().getWorldSize() / 2) + 3
				elif (mc.BonusMaxGroupSize == 0):
					maxAdd = PRand.randint(1, gc.getGame().countCivPlayersEverAlive())
				else:
					maxAdd = PRand.randint(1, mc.BonusMaxGroupSize)
				for dx in range(-groupRange, groupRange + 1):
					for dy in range(-groupRange, groupRange + 1):
						#NEW CODE - Fuyu
						if(added >= maxAdd):
							break
						if bonus.currentBonusCount < bonus.desiredBonusCount:
							loopPlot = self.plotXY(x, y, dx, dy)
							if loopPlot != None:
								if loopPlot.getX() == -1:
									raise ValueError, "plotXY returns invalid plots plot= %(x)d, %(y)d" % {"x":x, "y":y}
								if self.CanPlaceBonusAt(loopPlot,eBonus,False,False):
									if PRand.randint(0, 99) < bonusInfo.getGroupRand():
										#place bonus
										loopPlot.setBonusType(eBonus)
										bonus.currentBonusCount += 1
										#NEW CODE - Fuyu
										added += 1
			if bonusPlaced:
				break
		lastI = (lastI + 1) % plotListLength
		return lastI
	
	def plotXY(self,x,y,dx,dy):
		gameMap = CyMap()
		#The one that civ uses will return junk so I have to make one
		#that will not
		x = (x + dx) % mc.width
		y = y + dy
		if y < 0 or y > mc.height - 1:
			return None
		return gameMap.plot(x,y)
		
	def AssignBonusAreas(self):
		gc = CyGlobalContext()
		self.areas = CvMapGeneratorUtil.getAreas()
		self.bonusList = list()
		#Create and shuffle the bonus list and keep tally on one-area
		#bonuses and find the smallest min area requirement among those
		numUniqueBonuses = 0
		minLandAreaSize = -1
		numBonuses = gc.getNumBonusInfos()
		for i in range(numBonuses):
			bonus = BonusArea()
			bonus.eBonus = i
			self.bonusList.append(bonus)
			bonusInfo = gc.getBonusInfo(i)
			if bonusInfo.isOneArea():
				numUniqueBonuses += 1
				minAreaSize = bonusInfo.getMinAreaSize()
				if (minLandAreaSize == -1 or minLandAreaSize > minAreaSize) and minAreaSize > 0:
					minLandAreaSize = minAreaSize
		self.bonusList = ShuffleList(self.bonusList)
		self.bonusDict = [0] * numBonuses
		for i in range(numBonuses):
			eBonus = self.bonusList[i].eBonus
			self.bonusDict[eBonus] = i
			self.bonusList[i].desiredBonusCount = self.CalculateNumBonusesToAdd(eBonus)
			bonusInfo = gc.getBonusInfo(eBonus)
			if not bonusInfo.isOneArea():
				continue #Only assign areas to area bonuses
			areaSuitabilityList = list()
			for area in self.areas:
				if area.getNumTiles() >= minLandAreaSize:
					aS = AreaSuitability(area.getID())
					aS.suitability,aS.numPossible = self.CalculateAreaSuitability(area, eBonus)
					areaSuitabilityList.append(aS)
			#Calculate how many areas to assign (numUniqueBonuses will be > 0 if we get here)
			areasPerBonus = 1
			#Sort areaSuitabilityList best first
			areaSuitabilityList.sort(lambda x, y:cmp(x.numPossible, y.numPossible))
			areaSuitabilityList.reverse()
			#assign the best areas to this bonus
			for n in range(areasPerBonus):
				self.bonusList[i].areaList.append(areaSuitabilityList[n].areaID)
			#assign areas that have a high suitability also
			for n in range(areasPerBonus,len(areaSuitabilityList)):
				if areaSuitabilityList[n].suitability > 0.3:
					self.bonusList[i].areaList.append(areaSuitabilityList[n].areaID)


	def CanPlaceBonusAt(self, plot, eBonus, bIgnoreLatitude, bIgnoreArea):
		gc = CyGlobalContext()
		x = plot.getX()
		y = plot.getY()
		areaID = plot.getArea()
		if not self.PlotCanHaveBonus(plot, eBonus, bIgnoreLatitude, bIgnoreArea):
			return False
		for i in range(DirectionTypes.NUM_DIRECTION_TYPES):
			loopPlot = plotDirection(x, y, DirectionTypes(i))
			if loopPlot.getBonusType(TeamTypes.NO_TEAM) != BonusTypes.NO_BONUS and loopPlot.getBonusType(TeamTypes.NO_TEAM) != eBonus:
			   return False
		bonusInfo = gc.getBonusInfo(eBonus)
		classInfo = gc.getBonusClassInfo(bonusInfo.getBonusClassType())
		if plot.isWater():
			if (CyMap().getNumBonusesOnLand(eBonus) * 100) / (CyMap().getNumBonuses(eBonus) + 1) < bonusInfo.getMinLandPercent():
				return False
		#Make sure there are no bonuses of the same class (but a different type) nearby:
		if classInfo != None:
			try:
				iRange = classInfo.getUniqueRange()
			except:
				iRange = classInfo.getUniqueRange #<--attribute for vanilla
			iRange = max(0, int(iRange - (round(mc.BonusBonus) - 1)))
			for dx in range(-iRange, iRange + 1):
				for dy in range(-iRange, iRange + 1):
					loopPlot = self.plotXY(x, y, dx, dy)
					if loopPlot != None:
						if areaID == loopPlot.getArea():
							if plotDistance(x, y, loopPlot.getX(), loopPlot.getY()) <= iRange:
								eOtherBonus = loopPlot.getBonusType(TeamTypes.NO_TEAM)
								if eOtherBonus != BonusTypes.NO_BONUS:
									if gc.getBonusInfo(eOtherBonus).getBonusClassType() == bonusInfo.getBonusClassType():
										return False
		#Make sure there are no bonuses of the same type nearby:
		iRange = bonusInfo.getUniqueRange()
		iRange = max(0, int(iRange - (round(mc.BonusBonus) - 1)))
		for dx in range(-iRange, iRange + 1):
			for dy in range(-iRange, iRange + 1):
				loopPlot = self.plotXY(x, y, dx, dy)
				if loopPlot != None:
					if areaID == loopPlot.getArea():
						if plotDistance(x, y, loopPlot.getX(), loopPlot.getY()) <= iRange:
							eOtherBonus = loopPlot.getBonusType(TeamTypes.NO_TEAM)
							if eOtherBonus != BonusTypes.NO_BONUS:
								if eOtherBonus == eBonus:
									return False
		return True


	def PlotCanHaveBonus(self, plot, eBonus, bIgnoreLatitude, bIgnoreArea):
		#This function is like CvPlot::canHaveBonus but will ignore blocking features and checks for a valid area.
		if eBonus == BonusTypes.NO_BONUS:
			return True
		if plot.getBonusType(TeamTypes.NO_TEAM) != BonusTypes.NO_BONUS:
			return False

		#################################################
		## MongooseMod 3.5 BEGIN
		#################################################

		gc = CyGlobalContext()
		bonusInfo = gc.getBonusInfo(eBonus)
		if plot.getFeatureType() != FeatureTypes.NO_FEATURE:
			if not bonusInfo.isFeature(plot.getFeatureType()) or  not bonusInfo.isFeatureTerrain(plot.getTerrainType()):
				return False
		elif plot.isPeak():
			if not bonusInfo.isTerrain(plot.getTerrainType()) and not bonusInfo.isFeatureTerrain(plot.getTerrainType()):
				return False
		else:
			if not bonusInfo.isTerrain(plot.getTerrainType()):
				return False
		if plot.isFlatlands():
			if not bonusInfo.isFlatlands():
				return False
		elif plot.isHills():
			if not bonusInfo.isHills():
				return False
		elif plot.isPeak():
			return False

		#################################################
		## MongooseMod 3.5 END
		#################################################

		if bonusInfo.isNoRiverSide():
			if plot.isRiverSide():
				return False
		if bonusInfo.getMinAreaSize() != -1:
			if plot.area().getNumTiles() < bonusInfo.getMinAreaSize():
				return False
		if not bIgnoreLatitude:
			if plot.getLatitude() > bonusInfo.getMaxLatitude():
				return False
			if plot.getLatitude() < bonusInfo.getMinLatitude():
				return False
		if not plot.isPotentialCityWork():
			return False
		if bonusInfo.isOneArea() and not bIgnoreArea:
			areaID = plot.getArea()
			areaFound = False
			i = self.bonusDict[eBonus]
			areaList = self.bonusList[i].areaList
			for n in range(len(areaList)):
				if areaList[n] == areaID:
					areaFound = True
					break
			if not areaFound:
				return False
		return True


	def CalculateNumBonusesToAdd(self, eBonus):
		#This is like the function in CvMapGenerator except it uses
		#self.PlotCanHaveBonus instead of CvPlot::canHaveBonus
		gc = CyGlobalContext()
		bonusInfo = gc.getBonusInfo(eBonus)
		if bonusInfo.getPlacementOrder() < 0:
			return 0
		rand1 = PRand.randint(0, bonusInfo.getRandAppearance1())
		rand2 = PRand.randint(0, bonusInfo.getRandAppearance2())
		rand3 = PRand.randint(0, bonusInfo.getRandAppearance3())
		rand4 = PRand.randint(0, bonusInfo.getRandAppearance4())
		baseCount = bonusInfo.getConstAppearance() + rand1 + rand2 + rand3 + rand4
		bIgnoreLatitude = False
		bIgnoreArea     = True
		landTiles   = 0
		numPossible = 0
		if bonusInfo.getTilesPer() > 0:
			for i in range(mc.height*mc.width):
				plot = CyMap().plotByIndex(i)
				if self.PlotCanHaveBonus(plot, eBonus, bIgnoreLatitude, bIgnoreArea):
					numPossible += 1
			landTiles += numPossible / bonusInfo.getTilesPer()
		players = CyGame().countCivPlayersAlive() * bonusInfo.getPercentPerPlayer() / 100
		bonusCount = baseCount * (landTiles + players) / 100
		bonusCount = max(1, int(bonusCount * mc.BonusBonus))
		return bonusCount


	def GetUniqueBonusTypeCountInArea(self, area):
		gc = CyGlobalContext()
		areaID = area.getID()
		uniqueBonusCount = 0
		for i in range(len(self.bonusList)):
			areaList = self.bonusList[i].areaList
			bonusInfo = gc.getBonusInfo(self.bonusList[i].eBonus)
			if not bonusInfo.isOneArea():
				continue
			for n in range(len(areaList)):
				if areaList[n] == areaID:
					uniqueBonusCount += 1
					break
		return uniqueBonusCount


	def GetSameClassTypeCountInArea(self, area, eBonus):
		gc = CyGlobalContext()
		areaID = area.getID()
		uniqueBonusCount = 0
		bonusInfo = gc.getBonusInfo(eBonus)
		eClass = bonusInfo.getBonusClassType()
		if eClass == BonusClassTypes.NO_BONUSCLASS:
			return 0
		classInfo = gc.getBonusClassInfo(eClass)
		if classInfo == None:
			return 0
		try:
			uRange = classInfo.getUniqueRange()
		except:
			uRange = classInfo.getUniqueRange #<--vanilla Civ4
		uRange = max(0, int(uRange - (round(mc.BonusBonus) - 1)))
		for i in range(len(self.bonusList)):
			areaList = self.bonusList[i].areaList
			bonusInfo = gc.getBonusInfo(self.bonusList[i].eBonus)
			if not bonusInfo.isOneArea():
				continue
			if bonusInfo.getBonusClassType() != eClass:
				continue
			for n in range(len(areaList)):
				if areaList[n] == areaID:
					uniqueBonusCount += 1
					break
		#Same class types tend to really crowd out any bonus types that are placed later. A single cow can block
		#5 * 5 squares of pig territory for example. Probably shouldn't place them on the same area at all, but
		#sometimes it might be necessary.
		return uniqueBonusCount * uRange * uRange


	def CalculateAreaSuitability(self, area, eBonus):
		gc = CyGlobalContext()
		areaID = area.getID()
		uniqueTypesInArea    = self.GetUniqueBonusTypeCountInArea(area)
		sameClassTypesInArea = self.GetSameClassTypeCountInArea(area, eBonus)
		#Get the raw number of suitable tiles
		numPossible = 0
		for i in range(mc.height*mc.width):
			plot = CyMap().plotByIndex(i)
			if plot.getArea() == areaID:
				if self.PlotCanHaveBonus(plot, eBonus, False, True):
					numPossible += 1
		numPossible = numPossible / (uniqueTypesInArea + sameClassTypesInArea + 1)
		suitability = float(numPossible) / float(area.getNumTiles())
		return suitability, numPossible
#Global Access
bp = BonusPlacer()

class BonusArea :
	def __init__(self):
		self.eBonus = -1
		self.desiredBonusCount = -1
		self.currentBonusCount = 0
		self.areaList = list()
			
class AreaSuitability :
	def __init__(self,areaID):
		self.areaID = areaID
		self.suitability = 0
		self.numPossible = 0
		
class StartingPlotFinder :
	def __init__(self):
		return
		
	def CachePlotValue(self):
		self.inlandValueList  = []
		self.inlandFoodList   = []
		self.coastalValueList = []
		self.coastalFoodList  = []
		for y in range(mc.height):
			for x in range(mc.width):
				food, value = self.getPlotPotentialValueUncached(x, y, False)
				self.inlandValueList.append(value)
				self.inlandFoodList.append(food)
				food, value = self.getPlotPotentialValueUncached(x, y, True)
				self.coastalValueList.append(value)
				self.coastalFoodList.append(food)	
		
	def SetStartingPlots(self):
		gc = CyGlobalContext()
		iPlayers = gc.getGame().countCivPlayersEverAlive()
		self.CachePlotValue()
		#Shuffle players so the same player doesn't always get the first pick.
		#lifted from Highlands.py that ships with Civ.
		player_list = []
		for plrCheckLoop in range(gc.getMAX_CIV_PLAYERS()):
			if CyGlobalContext().getPlayer(plrCheckLoop).isEverAlive():
				player_list.append(plrCheckLoop)
		shuffledPlayers = []
		for playerLoop in range(iPlayers):
			iChoosePlayer = PRand.randint(0, len(player_list) - 1)
			shuffledPlayers.append(player_list[iChoosePlayer])
			del player_list[iChoosePlayer]

		CyMap().recalculateAreas()
		areas = CvMapGeneratorUtil.getAreas()
		#get old/new world status
		areaOldWorld = self.setupOldWorldAreaList()
		print "len(areaOldWorld) = %d" % len(areaOldWorld)
		#LM - Set up a map that merges Coast-linked landmasses so we can allow island starts while still ensuring adequate expansion room.
		regionMap = Areamap(mc.width, mc.height, True, True)
		regionMap.defineAreas(isDeepWaterMatch)
		#LM - Set up a map that divides areas by Peaks so we can prevent starting locations from being walled-off in small pockets.
		if gc.getGame().getStartEra() < 3:
			self.peakMap = Areamap(mc.width, mc.height, True, True)
			self.peakMap.defineAreas(isPeakWaterMatch)

		self.startingAreaList = list()
		if gc.getMap().getSeaLevel() == 0:
			if mc.AllowNewWorld:
				iWorldSizeFactor = 3
			else:
				iWorldSizeFactor = 5
		elif gc.getMap().getSeaLevel() == 1:
			if mc.AllowNewWorld:
				iWorldSizeFactor = 3.5
			else:
				iWorldSizeFactor = 6
		elif gc.getMap().getSeaLevel() == 2:
			if mc.AllowNewWorld:
				iWorldSizeFactor = 2.5
			else:
				iWorldSizeFactor = 4
		elif gc.getMap().getSeaLevel() == 3:
			if mc.AllowNewWorld:
				iWorldSizeFactor = 4
			else:
				iWorldSizeFactor = 7
		else:
			if mc.AllowNewWorld:
				iWorldSizeFactor = 2
			else:
				iWorldSizeFactor = 3
		self.iMinIslandSize = 5 + int(round(gc.getMap().getWorldSize() * iWorldSizeFactor))
		iMinRegionSize = self.iMinIslandSize * 4
		for i in range(len(areas)):
			if areaOldWorld[i] and areas[i].getNumTiles() >= self.iMinIslandSize:
				iRegionSize = 0
				for pI in range(mc.width * mc.height):
					plot = CyMap().plotByIndex(pI)
					if plot.getArea() == areas[i].getID():
						iRegionSize = regionMap.getAreaByID(regionMap.areaMap[pI]).size
						break
				if iRegionSize >= iMinRegionSize:
					startArea = StartingArea(areas[i].getID())
					self.startingAreaList.append(startArea)

		#Get the value of the whole old world
		oldWorldValue = 0
		for i in range(len(self.startingAreaList)):
			oldWorldValue += self.startingAreaList[i].rawValue
		#calulate value per player of old world
		oldWorldValuePerPlayer = oldWorldValue / len(shuffledPlayers)
		#Sort startingAreaList by rawValue
		self.startingAreaList.sort(lambda x, y: cmp(x.rawValue, y.rawValue))
		#Get rid of areas that have less value than oldWorldValuePerPlayer
		#as they are too small to put a player on, however leave at least
		#half as many continents as there are players, just in case the
		#continents are *all* quite small.
		#LM - max(1) is not necessary! Use max(0) in case it's already at or below the minimum number of areas allowed.
		numAreas = max(0, len(self.startingAreaList) - len(shuffledPlayers) / 2)
		for i in range(numAreas):
			if self.startingAreaList[0].rawValue < oldWorldValuePerPlayer:
				del self.startingAreaList[0]
			else:
				break #All remaining should be big enough
		#Recalculate the value of the whole old world
		oldWorldValue = 0
		for i in range(len(self.startingAreaList)):
			oldWorldValue += self.startingAreaList[i].rawValue
		#Recalulate value per player of old world so we are starting more accurately
		oldWorldValuePerPlayer = oldWorldValue / len(shuffledPlayers)
		#Record the ideal number of players for each continent
		for startingArea in self.startingAreaList:
			#LM - Store fractional values for accurate scaling below.
			startingArea.idealNumberOfPlayers = float(startingArea.rawValue) / float(oldWorldValuePerPlayer)
		#Now we want best first
		self.startingAreaList.reverse()
		print "number of starting areas is %(s)3d" % {"s":len(self.startingAreaList)}
		#LM - This iteration-based while loop is a complete mess. Not only is it slow and inefficient, but it
		#ONLY MODIFIES THE BEST/LARGEST LANDMASS'S PLAYER COUNT, no matter HOW far off it is in either direction!
		#You can EASILY end up with a super-crowded main landmass, or a nearly-deserted one, this way.
		#Player count assignments SHOULD SCALE PROPORTIONATELY!!!
		floatTotal = 0.0
		for startingArea in self.startingAreaList:
			floatTotal += startingArea.idealNumberOfPlayers
		fRatio = float(len(shuffledPlayers)) / floatTotal
		for startingArea in self.startingAreaList:
			startingArea.idealNumberOfPlayers *= fRatio
		#LM - Reallocate players as needed to fix any overloaded landmasses.
		iterations = len(self.startingAreaList)
		bSpaceAvailable = True
		while iterations > 0 and bSpaceAvailable:
			for startingArea in self.startingAreaList:
				difference = startingArea.idealNumberOfPlayers - float(len(startingArea.plotList))
				if difference > 0.0:
					searchTotal = 0.0
					for searchArea in self.startingAreaList:
						if searchArea.idealNumberOfPlayers < float(len(searchArea.plotList)):
							searchTotal += searchArea.idealNumberOfPlayers
					if searchTotal > 0.0:
						startingArea.idealNumberOfPlayers = float(len(startingArea.plotList))
						fRatio = (searchTotal + difference) / searchTotal
						for searchArea in self.startingAreaList:
							if searchArea.idealNumberOfPlayers < float(len(searchArea.plotList)):
								searchArea.idealNumberOfPlayers *= fRatio
					else:
						raise ValueError, "Not enough room on the map to place all players!"
						bSpaceAvailable = False
						break
			iterations -= 1
		#LM - Done with fractional values, finally.
		for startingArea in self.startingAreaList:
			startingArea.idealNumberOfPlayers = int(round(startingArea.idealNumberOfPlayers))
		#LM - Total player allocation should be pretty close to the correct number here. Smooth out any difference that's left.
		idealTotal = 0
		for startingArea in self.startingAreaList:
			idealTotal += startingArea.idealNumberOfPlayers
		if idealTotal < len(shuffledPlayers):
			iNum = len(shuffledPlayers) - idealTotal
			while iNum > 0:
				iEntry = iNum
				for startingArea in self.startingAreaList:
					if startingArea.idealNumberOfPlayers < len(startingArea.plotList):
						startingArea.idealNumberOfPlayers += 1
						iNum -= 1
						if iNum == 0:
							break
				if iNum == iEntry:
					raise ValueError, "Not enough room on the map to place all players!"
					break
		elif idealTotal > len(shuffledPlayers):
			iNum = idealTotal - len(shuffledPlayers)
			while iNum > 0:
				iEntry = iNum
				for startingArea in self.startingAreaList:
					if startingArea.idealNumberOfPlayers > 0:
						startingArea.idealNumberOfPlayers -= 1
						iNum -= 1
						if iNum == 0:
							break
				if iNum == iEntry:
					raise ValueError, "Not enough room on the map to place all players!"
					break
		#Assign players.
		for startingArea in self.startingAreaList:
			for i in range(startingArea.idealNumberOfPlayers):
				startingArea.playerList.append(shuffledPlayers[0])
				del shuffledPlayers[0]
			startingArea.FindStartingPlots()
		if len(shuffledPlayers) > 0:
			raise ValueError, "Some players not placed in starting plot finder!"
		#Now set up for normalization
		self.plotList = list()
		for startingArea in self.startingAreaList:
			for i in range(len(startingArea.plotList)):
				self.plotList.append(startingArea.plotList[i])
		#Remove bad features. (Jungle in the case of standard game)
		#also ensure minimum hills
		for i in range(len(self.plotList)):
			if not self.plotList[i].vacant:
				self.ensureMinimumHills(self.plotList[i].x, self.plotList[i].y)
		#find the best totalValue
		self.plotList.sort(lambda x, y:cmp(x.totalValue, y.totalValue))
		self.plotList.reverse()
		bestTotalValue = self.plotList[0].totalValue
		for i in range(len(self.plotList)):
			if not self.plotList[i].vacant:
				currentTotalValue = self.plotList[i].totalValue
				percentLacking = 1.0 - (float(currentTotalValue) / float(bestTotalValue))
				if percentLacking > 0:
					bonuses = min(5, int(percentLacking / 0.2))
					self.boostCityPlotValue(self.plotList[i].x, self.plotList[i].y, bonuses, self.plotList[i].isCoast())
		#add bonuses due to player difficulty settings
		self.addHandicapBonus()
	
	def setupOldWorldAreaList(self):
		gc = CyGlobalContext()
		gameMap = CyMap()
		#get official areas and make corresponding lists that determines old
		#world vs. new and also the pre-settled value.
		areas = CvMapGeneratorUtil.getAreas()
		areaOldWorld = list()
		for i in range(len(areas)):
			for pI in range(mc.height*mc.width):
				plot = gameMap.plotByIndex(pI)
				if plot.getArea() == areas[i].getID():
					if mc.AllowNewWorld and continentMap.areaMap.areaMap[pI] == continentMap.newWorldID:
						areaOldWorld.append(False)#new world true = old world false
					else:
						areaOldWorld.append(True)
					break

			
		return areaOldWorld
		
	def getCityPotentialValue(self, x, y):
		gc = CyGlobalContext()
		numCityPlots = gc.getNUM_CITY_PLOTS()
		totalValue = 0
		totalFood  = 0
		start = CyMap().plot(x, y)
		if start.isWater():
			return -1, -1
		if start.isImpassable():
			return -1, -1

		#################################################
		## MongooseMod 3.5 BEGIN
		#################################################

		if start.isPeak():
			return -1, -1

		#################################################
		## MongooseMod 3.5 END
		#################################################

		#LM - Block invalid locations!
		terrainInfo = gc.getTerrainInfo(start.getTerrainType())
		if not terrainInfo.isFound() and (not terrainInfo.isFoundCoast() or not start.isCoastalLand()) and (not terrainInfo.isFoundFreshWater() or not start.isFreshWater()):
			return -1, -1
		featureEnum = start.getFeatureType()
		if featureEnum != FeatureTypes.NO_FEATURE:
			featureInfo = gc.getFeatureInfo(featureEnum)
			if featureInfo.isNoCity():
				return -1, -1
		#LM - Also block sucky locations unless there's a good feature present!
		base = terrainInfo.getYield(YieldTypes.YIELD_FOOD) + terrainInfo.getYield(YieldTypes.YIELD_PRODUCTION) + terrainInfo.getYield(YieldTypes.YIELD_COMMERCE)
		if featureEnum != FeatureTypes.NO_FEATURE:
			extra = featureInfo.getYieldChange(YieldTypes.YIELD_FOOD)
		else:
			extra = 0
		if base <= 0 and extra <= 0:
			return -1, -1

		cityPlotList = list()
		#The StartPlot class has a nifty function to determine salt water vs. fresh
		sPlot = StartPlot(x, y, 0)
		#noFoodPlots  = 0
		#lowFoodPlots = 0
		for i in range(numCityPlots):
			plot = plotCity(x, y, i)
			if not plot.isWater() and plot.getArea() != start.getArea():
				food, value = 0, 0
			elif plot.getX() == start.getX() and plot.getY() == start.getY():
				food, value = self.getCityPlotPotentialValueUncached(plot.getX(), plot.getY(), sPlot.isCoast())
			else:
				food, value = self.getPlotPotentialValue(plot.getX(), plot.getY(), sPlot.isCoast())
			totalFood += food
			#if food == 0:
			#	noFoodPlots  += 1
			#elif food == 1:
			#	lowFoodPlots += 1
			cPlot = CityPlot(food, value)
			cityPlotList.append(cPlot)
		#if noFoodPlots > 6 or lowFoodPlots + noFoodPlots > 12:
		#	return totalFood, 0
		usablePlots = totalFood / gc.getFOOD_CONSUMPTION_PER_POPULATION()
		cityPlotList.sort(lambda x, y:cmp(x.value, y.value))
		cityPlotList.reverse()
		#value is obviously limited to available food
		if usablePlots > numCityPlots:
			usablePlots = numCityPlots
		for i in range(usablePlots):
			cPlot = cityPlotList[i]
			totalValue += cPlot.value
		#LM - Removed redundant assignment.
		if sPlot.isCoast():
			totalValue = int(float(totalValue) * mc.CoastalCityValueBonus)
		#LM - Use isRiver, not isRiverSide!
		if start.isRiver():
			totalValue = int(float(totalValue) * mc.RiverCityValueBonus)
		#LM - Add small bonus for hill defense.
		if start.isHills():
			totalValue = int(float(totalValue) * mc.HillCityValueBonus)
		#LM - Add small bonus for starting on bonus.
		bonusEnum = start.getBonusType(TeamTypes.NO_TEAM)
		if bonusEnum != BonusTypes.NO_BONUS:
			bonusInfo = gc.getBonusInfo(bonusEnum)
			if bonusInfo.getBonusClassType() == gc.getInfoTypeForString("BONUSCLASS_WONDER") or bonusInfo.getBonusClassType() == gc.getInfoTypeForString("BONUSCLASS_RUSH") or bonusInfo.getBonusClassType() == gc.getInfoTypeForString("BONUSCLASS_MODERN"):
				totalValue = int(float(totalValue) * mc.StrategicBonusCityValueBonus)
			else:
				totalValue = int(float(totalValue) * mc.OtherBonusCityValueBonus)
		return totalFood, totalValue
		
	def getPlotPotentialValue(self, x, y, coastalCity):
		i = GetIndex(x, y)
		#LM - This included an extension of the "ignore lakes" TRAIN WRECK below.
		#CODE ERASED.
		if coastalCity:
			value = self.coastalValueList[i]
			food  = self.coastalFoodList[i]
		else:
			value = self.inlandValueList[i]
			food  = self.inlandFoodList[i]
		return food, value


	def getPlotPotentialValueUncached(self, x, y, coastalCity):
		plot = CyMap().plot(x, y)
		sPlot = StartPlot(x, y, 0)
		gc = CyGlobalContext()
		fPlains      = gc.getInfoTypeForString("TERRAIN_PLAINS")
		fFloodPlains = gc.getInfoTypeForString("FEATURE_FLOOD_PLAINS")
		#LM - Store highest era allowed for any of these things.
		if gc.getGame().getStartEra() < 5:
			eraLimit = 6
		else:
			eraLimit = 7
		#LM - Store most advanced route type that can be built within the allowed Era range.
		maxRoute = -1
		for n in range(gc.getNumRouteInfos()):
			for i in range(gc.getNumBuildInfos()):
				buildInfo = gc.getBuildInfo(i)
				if buildInfo.getRoute() == n:
					if buildInfo.getTechPrereq() == TechTypes.NO_TECH or gc.getTechInfo(buildInfo.getTechPrereq()).getEra() <= eraLimit:
						maxRoute = n
					break

		terrainEnum = plot.getTerrainType()
		terrainInfo = gc.getTerrainInfo(terrainEnum)
		featureEnum = plot.getFeatureType()
		featureInfo = gc.getFeatureInfo(featureEnum)

		#Get best bonus improvement score. Test tachnology era of bonus first, then test each improvement
		food       = plot.calculateBestNatureYield(YieldTypes.YIELD_FOOD,       TeamTypes.NO_TEAM)
		production = plot.calculateBestNatureYield(YieldTypes.YIELD_PRODUCTION, TeamTypes.NO_TEAM)
		commerce   = plot.calculateBestNatureYield(YieldTypes.YIELD_COMMERCE,   TeamTypes.NO_TEAM)
		#LM - Handle Plains-Floodplains (since it's a special case).
		if featureEnum == fFloodPlains and terrainEnum == fPlains:
			food -= 2
		#LM - Assume Lighthouse (since it's always one of the very first things a coastal city builds), and add in the VITAL extra food point from it.
		#But remember it doesn't apply on Sea Ice!
		if plot.isWater() and coastalCity and not plot.isImpassable():
			food += 1

		bonusEnum = plot.getBonusType(TeamTypes.NO_TEAM)
		bonusFood       = 0
		bonusProduction = 0
		bonusCommerce   = 0
		if bonusEnum != BonusTypes.NO_BONUS:
			bonusInfo = gc.getBonusInfo(bonusEnum)
			if bonusInfo.getTechReveal() == TechTypes.NO_TECH or gc.getTechInfo(bonusInfo.getTechReveal()).getEra() <= gc.getGame().getStartEra() + 1:
				food       += bonusInfo.getYieldChange(YieldTypes.YIELD_FOOD)
				production += bonusInfo.getYieldChange(YieldTypes.YIELD_PRODUCTION)
				commerce   += bonusInfo.getYieldChange(YieldTypes.YIELD_COMMERCE)
			elif gc.getTechInfo(bonusInfo.getTechReveal()).getEra() <= eraLimit:
				bonusFood       += bonusInfo.getYieldChange(YieldTypes.YIELD_FOOD)
				bonusProduction += bonusInfo.getYieldChange(YieldTypes.YIELD_PRODUCTION)
				bonusCommerce   += bonusInfo.getYieldChange(YieldTypes.YIELD_COMMERCE)
			else:
				bonusEnum = BonusTypes.NO_BONUS

		improvementList = list()
		for n in range(gc.getNumBuildInfos()):
			#Test for improvement validity
			buildInfo = gc.getBuildInfo(n)
			impEnum = buildInfo.getImprovement()
			if impEnum == ImprovementTypes.NO_IMPROVEMENT:
				continue
			impInfo = gc.getImprovementInfo(impEnum)
			#LM - Add support for Towns and Mountain Villages, NOT JUST COTTAGES!!!
			while impInfo.getImprovementUpgrade() != ImprovementTypes.NO_IMPROVEMENT:
				impEnum = impInfo.getImprovementUpgrade()
				impInfo = gc.getImprovementInfo(impEnum)

			#some mods use improvements for other things, so if there's no tech requirement we still don't want it factored in.
			#LM - Yeah, umm... WRONG! This is a disaster. It completely blocks feature removal builds (which the below code TRIES to use!)
			#due to their empty main tech prereqs, as well as the Igloo and Snowman improvements.
			#CODE ERASED.
			#LM - Okay, I was wrong again. Blocking feature removal builds is FINE b/c they SUCK, and the below code was mainly trying to support
			#the standard feature removal REQUIRED by most builds. Plus I block Igloo and Snowman further down anyway, so why not save some time.
			#So yeah, umm... Oops. :)
			#CODE RESTORED.
			if buildInfo.getTechPrereq() == TechTypes.NO_TECH or gc.getTechInfo(buildInfo.getTechPrereq()).getEra() > eraLimit:
				continue
			#LM - I'm not even going to block water tile improvements for non-coastal cities, b/c even if a player both DOESN'T have, and will NEVER have,
			#Workboat access to a non-coastal city's water tiles (VERY unlikely - start a war to get there if necessary!), we don't block land tiles that
			#are across a channel and might ultimately end up under enemy control... Plus an ally may come along and place Fishing Nets for him anyway.
			if plot.canHaveImprovement(impEnum, TeamTypes.NO_TEAM, True):
				impFood       = plot.calculateImprovementYieldChange(impEnum, YieldTypes.YIELD_FOOD,       PlayerTypes.NO_PLAYER, False)
				impProduction = plot.calculateImprovementYieldChange(impEnum, YieldTypes.YIELD_PRODUCTION, PlayerTypes.NO_PLAYER, False)
				impCommerce   = plot.calculateImprovementYieldChange(impEnum, YieldTypes.YIELD_COMMERCE,   PlayerTypes.NO_PLAYER, False)
				#That function will not find bonus yield changes for NO_PLAYER, much to my annoyance
				if bonusEnum != BonusTypes.NO_BONUS:
					impFood       += impInfo.getImprovementBonusYield(bonusEnum, YieldTypes.YIELD_FOOD)
					impProduction += impInfo.getImprovementBonusYield(bonusEnum, YieldTypes.YIELD_PRODUCTION)
					impCommerce   += impInfo.getImprovementBonusYield(bonusEnum, YieldTypes.YIELD_COMMERCE)
				#LM - Assume irrigation (since it's very easy to get everywhere once you have Civil Service), and add in any extra yields from it.
				#(bOptimal is false, so calculateImprovementYieldChange() didn't add anything.)
				impFood       += impInfo.getIrrigatedYieldChange(YieldTypes.YIELD_FOOD)
				impProduction += impInfo.getIrrigatedYieldChange(YieldTypes.YIELD_PRODUCTION)
				impCommerce   += impInfo.getIrrigatedYieldChange(YieldTypes.YIELD_COMMERCE)
				#LM - Add in extra yields from the most advanced route type that is unlocked up through the Era limit.
				#(bOptimal is false and these plots don't have any routes already on them, so calculateImprovementYieldChange() didn't add anything.)
				if maxRoute >= 0:
					impFood       += impInfo.getRouteYieldChanges(maxRoute, YieldTypes.YIELD_FOOD)
					impProduction += impInfo.getRouteYieldChanges(maxRoute, YieldTypes.YIELD_PRODUCTION)
					impCommerce   += impInfo.getRouteYieldChanges(maxRoute, YieldTypes.YIELD_COMMERCE)
				#LM - Undo later tech modifiers, and ALL civic modifiers, to the improvement, since calculateImprovementYieldChange()
				#adds them in when called with NO_PLAYER, regardless of the bOptimal parameter.
				for i in range(gc.getNumTechInfos()):
					if gc.getTechInfo(i).getEra() > eraLimit:
						impFood       -= impInfo.getTechYieldChanges(i, YieldTypes.YIELD_FOOD)
						impProduction -= impInfo.getTechYieldChanges(i, YieldTypes.YIELD_PRODUCTION)
						impCommerce   -= impInfo.getTechYieldChanges(i, YieldTypes.YIELD_COMMERCE)
				for i in range(gc.getNumCivicInfos()):
					civicInfo = gc.getCivicInfo(i)
					impFood       -= civicInfo.getImprovementYieldChanges(impEnum, YieldTypes.YIELD_FOOD)
					impProduction -= civicInfo.getImprovementYieldChanges(impEnum, YieldTypes.YIELD_PRODUCTION)
					impCommerce   -= civicInfo.getImprovementYieldChanges(impEnum, YieldTypes.YIELD_COMMERCE)
				#See if feature is removed, if so we must subtract the added yield from that feature
				bProceed = True
				if featureEnum != FeatureTypes.NO_FEATURE and buildInfo.isFeatureRemove(featureEnum):
					if buildInfo.getFeatureTech(featureEnum) == TechTypes.NO_TECH or gc.getTechInfo(buildInfo.getFeatureTech(featureEnum)).getEra() <= gc.getGame().getStartEra() + 2:
						#LM - Ceph's code was subtracting out the feature's extra river and hill yields EVEN IF THERE WAS NO RIVER OR HILL ON THE PLOT!!!
						#It was ALSO not restoring the TERRAIN'S extra river and hill yields afterward, which are used when no feature is present.
						#Wow, so many major bugs in this function...
						impFood       -= featureInfo.getYieldChange(YieldTypes.YIELD_FOOD)
						impProduction -= featureInfo.getYieldChange(YieldTypes.YIELD_PRODUCTION)
						impCommerce   -= featureInfo.getYieldChange(YieldTypes.YIELD_COMMERCE)
						if plot.isRiver():
							impFood       -= featureInfo.getRiverYieldChange(YieldTypes.YIELD_FOOD)
							impProduction -= featureInfo.getRiverYieldChange(YieldTypes.YIELD_PRODUCTION)
							impCommerce   -= featureInfo.getRiverYieldChange(YieldTypes.YIELD_COMMERCE)
							impFood       += terrainInfo.getRiverYieldChange(YieldTypes.YIELD_FOOD)
							impProduction += terrainInfo.getRiverYieldChange(YieldTypes.YIELD_PRODUCTION)
							impCommerce   += terrainInfo.getRiverYieldChange(YieldTypes.YIELD_COMMERCE)
						if plot.isHills():
							impFood       -= featureInfo.getHillsYieldChange(YieldTypes.YIELD_FOOD)
							impProduction -= featureInfo.getHillsYieldChange(YieldTypes.YIELD_PRODUCTION)
							impCommerce   -= featureInfo.getHillsYieldChange(YieldTypes.YIELD_COMMERCE)
							impFood       += terrainInfo.getHillsYieldChange(YieldTypes.YIELD_FOOD)
							impProduction += terrainInfo.getHillsYieldChange(YieldTypes.YIELD_PRODUCTION)
							impCommerce   += terrainInfo.getHillsYieldChange(YieldTypes.YIELD_COMMERCE)
					else:
						bProceed = False
				if bProceed:
					imp = Improvement(impEnum, impFood, impProduction, impCommerce, 0)
					improvementList.append(imp)
		for i in range(len(improvementList)):
			impFood       = improvementList[i].food       + food       + bonusFood
			impProduction = improvementList[i].production + production + bonusProduction
			impCommerce   = improvementList[i].commerce   + commerce   + bonusCommerce
			impValue = (impFood * mc.FoodValue) + (impProduction * mc.ProductionValue) + (impCommerce * mc.CommerceValue)
			#LM - Encourage Lush, Mushrooms, Floodplains, Oases, Sea Grass, Kelp, and early food resources here to differentiate them from tile improvements that add food!
			if food >= 3:
				impValue *= 2
			#LM - Encourage Forest/Savanna-Plains-Hills and early production resources here to differentiate them from tile improvements that add production!
			if production >= 3:
				impValue *= 2
			#LM - Encourage Oases, Coral, and early commerce resources here to differentiate them from tile improvements that add commerce!
			if commerce >= 3:
				impValue *= 2
			#LM - Discourage coastal water when dealing with a non-coastal city, BUT LEAVE LAKES ALONE!!!
			if not coastalCity and sPlot.isCoast():
				impValue /= 2
			#LM - Add small value for improvements with coughup chances.
			impInfo = gc.getImprovementInfo(improvementList[i].e)
			for n in range(gc.getNumBonusInfos()):
				if impInfo.getImprovementBonusDiscoverRand(n) > 0:
					impValue += (mc.ProductionValue / 2) + (mc.CommerceValue / 2)
					break
			#Food surplus makes the square much more valuable than if there is no food here.
			#LM - Another CRITICAL BUGFIX!!! This code was using "food", which is the base yield of the tile, rather than "impFood", which is the final value that actually MATTERS.
			#Since "food" is a constant from outside this loop, the result was value multiplication being always applied or never applied, regardless of the improvement under consideration.
			if impFood > gc.getFOOD_CONSUMPTION_PER_POPULATION():
				impValue *= 3
			elif impFood == gc.getFOOD_CONSUMPTION_PER_POPULATION():
				impValue *= 2
			#LM - "Commerce / 2" is my standard rule for yield balance, and it allows the code to rule out Igloo and Snowman while allowing everything else.
			elif impFood + impProduction + (impCommerce / 2) < 3:
				impValue = 0
			improvementList[i].value = impValue
		if len(improvementList) > 0:
			#sort all allowed improvement values to find the best
			improvementList.sort(lambda x, y:cmp(x.value, y.value))
			improvementList.reverse()
			bestImp = improvementList[0]
			#LM - And yet ANOTHER huge bug... I've lost count, lol. This code was ADDING bestImp's yields to the base yields, but bestImp already INCLUDED the base yields!!!
			#The result was a VERY messed up final value calculation below. None of this is necessary at all though; since the calculation is the same, just use bestImp's values directly.
			return bestImp.food, bestImp.value

		#Try to avoid included water food resources for non-coastal starts. It confuses the AI.
		#LM - Yeah, umm, WRONG! This is a TRAIN WRECK!!! It completely blocks lakes which have HUGE base values, and even then, coastal tiles can
		#be useful to non-coastal cities even WITHOUT any tile improvements or coastal buildings, especially with features or resources present.
		#CODE ERASED.

		#LM - Now we have to support the case where no valid improvements were found (even though it'll probably never happen, sigh).
		value = ((food + bonusFood) * mc.FoodValue) + ((production + bonusProduction) * mc.ProductionValue) + ((commerce + bonusCommerce) * mc.CommerceValue)
		if food >= 3:
			value *= 2
		if production >= 3:
			value *= 2
		if commerce >= 3:
			value *= 2
		if not coastalCity and sPlot.isCoast():
			value /= 2
		food += bonusFood
		if food > gc.getFOOD_CONSUMPTION_PER_POPULATION():
			value *= 3
		elif food == gc.getFOOD_CONSUMPTION_PER_POPULATION():
			value *= 2
		elif food + (production + bonusProduction) + ((commerce + bonusCommerce) / 2) < 3:
			value = 0
		return food, value


	#LM - We need a whole new version of the function specifically for city plots, because they have different rules for calculating yields (and no tile improvements either).
	def getCityPlotPotentialValueUncached(self, x, y, coastalCity):
		plot = CyMap().plot(x, y)
		gc = CyGlobalContext()
		fFloodPlains = gc.getInfoTypeForString("FEATURE_FLOOD_PLAINS")
		if gc.getGame().getStartEra() < 5:
			eraLimit = 6
		else:
			eraLimit = 7

		terrainEnum = plot.getTerrainType()
		terrainInfo = gc.getTerrainInfo(terrainEnum)
		featureEnum = plot.getFeatureType()
		featureInfo = gc.getFeatureInfo(featureEnum)
		bonusEnum   = plot.getBonusType(TeamTypes.NO_TEAM)
		bonusInfo   = gc.getBonusInfo(bonusEnum)

		#LM - Get base value, then subtract out ALL feature and resource effects.
		food       = plot.calculateBestNatureYield(YieldTypes.YIELD_FOOD,       TeamTypes.NO_TEAM)
		production = plot.calculateBestNatureYield(YieldTypes.YIELD_PRODUCTION, TeamTypes.NO_TEAM)
		commerce   = plot.calculateBestNatureYield(YieldTypes.YIELD_COMMERCE,   TeamTypes.NO_TEAM)
		bonusFood       = 0
		bonusProduction = 0
		bonusCommerce   = 0
		if featureEnum != FeatureTypes.NO_FEATURE:
			food       -= featureInfo.getYieldChange(YieldTypes.YIELD_FOOD)
			production -= featureInfo.getYieldChange(YieldTypes.YIELD_PRODUCTION)
			commerce   -= featureInfo.getYieldChange(YieldTypes.YIELD_COMMERCE)
			if plot.isRiver():
				food       -= featureInfo.getRiverYieldChange(YieldTypes.YIELD_FOOD)
				production -= featureInfo.getRiverYieldChange(YieldTypes.YIELD_PRODUCTION)
				commerce   -= featureInfo.getRiverYieldChange(YieldTypes.YIELD_COMMERCE)
				food       += terrainInfo.getRiverYieldChange(YieldTypes.YIELD_FOOD)
				production += terrainInfo.getRiverYieldChange(YieldTypes.YIELD_PRODUCTION)
				commerce   += terrainInfo.getRiverYieldChange(YieldTypes.YIELD_COMMERCE)
			if plot.isHills():
				food       -= featureInfo.getHillsYieldChange(YieldTypes.YIELD_FOOD)
				production -= featureInfo.getHillsYieldChange(YieldTypes.YIELD_PRODUCTION)
				commerce   -= featureInfo.getHillsYieldChange(YieldTypes.YIELD_COMMERCE)
				food       += terrainInfo.getHillsYieldChange(YieldTypes.YIELD_FOOD)
				production += terrainInfo.getHillsYieldChange(YieldTypes.YIELD_PRODUCTION)
				commerce   += terrainInfo.getHillsYieldChange(YieldTypes.YIELD_COMMERCE)
		if bonusEnum != BonusTypes.NO_BONUS:
			food       -= bonusInfo.getYieldChange(YieldTypes.YIELD_FOOD)
			production -= bonusInfo.getYieldChange(YieldTypes.YIELD_PRODUCTION)
			commerce   -= bonusInfo.getYieldChange(YieldTypes.YIELD_COMMERCE)

		#LM - Apply city minimum effects, then add permanent features and visible resources back in on top.
		food       = max(food,       gc.getYieldInfo(YieldTypes.YIELD_FOOD).getMinCity())
		production = max(production, gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getMinCity())
		commerce   += gc.getYieldInfo(YieldTypes.YIELD_COMMERCE).getMinCity()
		if featureEnum == fFloodPlains:
			food += 1
		if bonusEnum != BonusTypes.NO_BONUS:
			if bonusInfo.getTechReveal() == TechTypes.NO_TECH or gc.getTechInfo(bonusInfo.getTechReveal()).getEra() <= gc.getGame().getStartEra() + 1:
				food       += bonusInfo.getYieldChange(YieldTypes.YIELD_FOOD)
				production += bonusInfo.getYieldChange(YieldTypes.YIELD_PRODUCTION)
				commerce   += bonusInfo.getYieldChange(YieldTypes.YIELD_COMMERCE)
			elif gc.getTechInfo(bonusInfo.getTechReveal()).getEra() <= eraLimit:
				bonusFood       += bonusInfo.getYieldChange(YieldTypes.YIELD_FOOD)
				bonusProduction += bonusInfo.getYieldChange(YieldTypes.YIELD_PRODUCTION)
				bonusCommerce   += bonusInfo.getYieldChange(YieldTypes.YIELD_COMMERCE)

		#LM - Now calculate tile value the same way as in getPlotPotentialValueUncached().
		value = ((food + bonusFood) * mc.FoodValue) + ((production + bonusProduction) * mc.ProductionValue) + ((commerce + bonusCommerce) * mc.CommerceValue)
		if food >= 3:
			value *= 2
		if production >= 3:
			value *= 2
		if commerce >= 3:
			value *= 2
		food += bonusFood
		if food > gc.getFOOD_CONSUMPTION_PER_POPULATION():
			value *= 3
		elif food == gc.getFOOD_CONSUMPTION_PER_POPULATION():
			value *= 2
		elif food + (production + bonusProduction) + ((commerce + bonusCommerce) / 2) < 3:
			value = 0
		return food, value


	def boostCityPlotValue(self, x, y, bonuses, isCoastalCity):
		mapGen = CyMapGenerator()
		food, value = self.getCityPotentialValue(x, y)
		gc = CyGlobalContext()
		numCityPlots = gc.getNUM_CITY_PLOTS()
		#Shuffle the bonus order so that different cities have different preferences for bonuses
		bonusList = list()
		numBonuses = gc.getNumBonusInfos()
		for i in range(numBonuses):
			bonusList.append(i)
		shuffledBonuses = list()
		for i in range(numBonuses):
			n = PRand.randint(0, len(bonusList) - 1)
			shuffledBonuses.append(bonusList[n])
			del bonusList[n]
		if len(shuffledBonuses) != numBonuses:
			raise ValueError, "Bad bonus shuffle. Learn 2 shuffle."
		bonusCount = 0
		#Do this process in 3 passes for each yield type
		yields = []
		yields.append(YieldTypes.YIELD_PRODUCTION)
		yields.append(YieldTypes.YIELD_COMMERCE)
		yields.append(YieldTypes.YIELD_FOOD)
		#NEW CODE - Fuyu
		allowBonusWonderClass = (PRand.random() < mc.allowWonderBonusChance)
		plotList = []
		for i in range(numCityPlots):
			plotList.append(plotCity(x, y, i))
		plotList = ShuffleList(plotList)
		for n in range(len(yields) * bonuses + 1):
			for plot in plotList:
				#NEW CODE - LM
				if bonusCount >= bonuses:
					return
				if plot.getX() == x and plot.getY() == y:
					continue
				if plot.isWater() and not isCoastalCity:
					continue
				if not plot.isWater() and CyMap().plot(x, y).getArea() != plot.getArea():
					continue
				if plot.getBonusType(TeamTypes.NO_TEAM) != BonusTypes.NO_BONUS:
					continue
				food, value = self.getCityPotentialValue(x, y)
				#NEW CODE - Fuyu
				currentYield = yields[(n + bonusCount) % (len(yields))]
				#switch to food if food is needed
				usablePlots = food / gc.getFOOD_CONSUMPTION_PER_POPULATION()
				if usablePlots <= numCityPlots / 2:
					currentYield = YieldTypes.YIELD_FOOD
				#temporarily remove any feature
				featureEnum = plot.getFeatureType()
				if featureEnum != FeatureTypes.NO_FEATURE:
					featureVariety = plot.getFeatureVariety()
					plot.setFeatureType(FeatureTypes.NO_FEATURE, -1)
				for b in range(numBonuses):
					bonusEnum = shuffledBonuses[b]
					if (bonusEnum == 23) or (bonusEnum == 27):
						continue
					bonusInfo = gc.getBonusInfo(bonusEnum)
					if not bonusInfo.isNormalize():
						continue
					if bonusInfo.getYieldChange(currentYield) < 1:
						continue
					#NEW CODE - Fuyu/LM
					if bonusInfo.getTechReveal() != TechTypes.NO_TECH and gc.getTechInfo(bonusInfo.getTechReveal()).getEra() > gc.getGame().getStartEra() + 1:
						continue
					if not bp.PlotCanHaveBonus(plot, bonusEnum, False, False):
						if not PRand.random() < mc.ignoreAreaRestrictionChance:
							continue
						if not bp.PlotCanHaveBonus(plot, bonusEnum, False, True):
							continue
					if bonusInfo.getBonusClassType() == gc.getInfoTypeForString("BONUSCLASS_WONDER") or bonusInfo.getBonusClassType() == gc.getInfoTypeForString("BONUSCLASS_RUSH") or bonusInfo.getBonusClassType() == gc.getInfoTypeForString("BONUSCLASS_MODERN"):
						if not allowBonusWonderClass:
							continue
						else:
							allowBonusWonderClass = False
					plot.setBonusType(bonusEnum)
					bonusCount += 1
					break
				#restore the feature if possible
				if featureEnum != FeatureTypes.NO_FEATURE:
					bonusInfo = gc.getBonusInfo(plot.getBonusType(TeamTypes.NO_TEAM))
					if bonusInfo == None or bonusInfo.isFeature(featureEnum):
						plot.setFeatureType(featureEnum, featureVariety)


	def ensureMinimumHills(self, x, y):
		gc = CyGlobalContext()
		hillsFound = 0
		peaksFound = 0
		badFeaturesFound = 0
		plotList = []
		for i in range(gc.getNUM_CITY_PLOTS()):
			plot = plotCity(x, y, i)
			featureInfo = gc.getFeatureInfo(plot.getFeatureType())
			if plot.getX() == x and plot.getY() == y:
				#remove bad feature on start but don't count it.
				if featureInfo != None:
					totalYield = 0
					for yi in range(YieldTypes.NUM_YIELD_TYPES):
						totalYield += featureInfo.getYieldChange(YieldTypes(yi))
					if totalYield <= 0:#bad feature
						plot.setFeatureType(FeatureTypes.NO_FEATURE, -1)
				continue
			if plot.getPlotType() == PlotTypes.PLOT_HILLS and CyMap().plot(x, y).getArea() == plot.getArea():
				hillsFound += 1
			if plot.getPlotType() == PlotTypes.PLOT_PEAK:
				peaksFound += 1
			if featureInfo != None:
				#now count the bad features
				totalYield = 0
				for yi in range(YieldTypes.NUM_YIELD_TYPES):
					totalYield += featureInfo.getYieldChange(YieldTypes(yi))
				if totalYield <= 0:#bad feature
					badFeaturesFound += 1
			if plot.isWater():
				continue
			if plot.getBonusType(TeamTypes.NO_TEAM) != BonusTypes.NO_BONUS:
				continue
			plotList.append(plot)
		plotList = ShuffleList(plotList)
		#ensure maximum number of peaks
		if peaksFound > mc.MaxPeaksInFC:
			for plot in plotList:
				if peaksFound == mc.MaxPeaksInFC:
					break
				if plot.getPlotType() == PlotTypes.PLOT_PEAK:
					plot.setPlotType(PlotTypes.PLOT_HILLS, True, True)
					if plot.getArea() == CyMap().plot(x, y).getArea():
						hillsFound += 1
					peaksFound -= 1
		#Ensure minimum number of hills
		hillsNeeded = mc.MinHillsInFC - hillsFound
		if hillsNeeded > 0:
			for plot in plotList:
				if hillsNeeded <= 0:
					break
				featureInfo = gc.getFeatureInfo(plot.getFeatureType())
				requiresFlatlands = (featureInfo != None and featureInfo.isRequiresFlatlands())
				bonusInfo = gc.getBonusInfo(plot.getBonusType(TeamTypes.NO_TEAM))
				if plot.getPlotType() != PlotTypes.PLOT_HILLS and plot.getArea() == CyMap().plot(x, y).getArea() and bonusInfo == None and not requiresFlatlands:
					plot.setPlotType(PlotTypes.PLOT_HILLS, True, True)
					hillsNeeded -= 1
			if hillsNeeded > 0:
				for plot in plotList:
					if plot.getPlotType() != PlotTypes.PLOT_HILLS and plot.getArea() == CyMap().plot(x, y).getArea() and (bonusInfo == None or not bonusInfo.isRequiresFlatlands()):
						plot.setPlotType(PlotTypes.PLOT_HILLS, True, True)
						hillsNeeded -= 1
						if requiresFlatlands:
							plot.setFeatureType(FeatureTypes.NO_FEATURE, -1)
		#ensure maximum number of bad features
		badFeaturesToRemove = badFeaturesFound - mc.MaxBadFeaturesInFC
		if badFeaturesToRemove > 0:
			#remove half from flatlands, the rest from hills
			badFeaturesToRemoveFromFlatlands = badFeaturesToRemove / 2 + badFeaturesToRemove % 2
			badFeaturesToRemove -= badFeaturesToRemoveFromFlatlands
			for plot in plotList:
				if badFeaturesToRemoveFromFlatlands <= 0 and badFeaturesToRemove <= 0:
					break
				featureEnum = plot.getFeatureType()
				featureInfo = gc.getFeatureInfo(featureEnum)
				bonusEnum = plot.getBonusType(TeamTypes.NO_TEAM)
				if featureInfo != None:
					totalYield = 0
					for yi in range(YieldTypes.NUM_YIELD_TYPES):
						totalYield += featureInfo.getYieldChange(YieldTypes(yi))
					if totalYield <= 0:#bad feature
						if plot.getPlotType() == PlotTypes.PLOT_LAND and badFeaturesToRemoveFromFlatlands > 0:
							badFeaturesToRemoveFromFlatlands -= 1
						if plot.getPlotType() == PlotTypes.PLOT_HILLS and badFeaturesToRemove > 0:
							badFeaturesToRemove -= 1
						plot.setFeatureType(FeatureTypes.NO_FEATURE, -1)
						if (bonusEnum != BonusTypes.NO_BONUS and not bp.PlotCanHaveBonus(plot, bonusEnum, True, True)):
							badFeaturesToRemove += 1
							plot.setFeatureType(featureEnum, -1)
			#if there are not enough hills or flatlands, there will be leftovers
			badFeaturesToRemove += badFeaturesToRemoveFromFlatlands
			for plot in plotList:
				if badFeaturesToRemove <= 0:
					break
				featureInfo = gc.getFeatureInfo(plot.getFeatureType())
				if featureInfo != None:
					totalYield = 0
					for yi in range(YieldTypes.NUM_YIELD_TYPES):
						totalYield += featureInfo.getYieldChange(YieldTypes(yi))
					if totalYield <= 0:#bad feature
						badFeaturesToRemove -= 1
						plot.setFeatureType(FeatureTypes.NO_FEATURE, -1)


	def addHandicapBonus(self):
		gc = CyGlobalContext()
		for ePlayer in range(gc.getMAX_CIV_PLAYERS()):
			player = gc.getPlayer(ePlayer)
			if player.isEverAlive() and player.isHuman():
				eHandicap = player.getHandicapType()
				startPlot = player.getStartingPlot()
				sPlot = StartPlot(startPlot.getX(),startPlot.getY(), 0)
				if eHandicap == gc.getInfoTypeForString("HANDICAP_SETTLER"):
					if mc.SettlerBonus > 0:
						print "Human player at Settler difficulty, adding %d resources" % mc.SettlerBonus
						self.boostCityPlotValue(startPlot.getX(), startPlot.getY(), mc.SettlerBonus, sPlot.isCoast())
				elif eHandicap == gc.getInfoTypeForString("HANDICAP_WARLORD"):
					if mc.WarlordBonus > 0:
						print "Human player at Warlord difficulty, adding %d resources" % mc.WarlordBonus
						self.boostCityPlotValue(startPlot.getX(), startPlot.getY(), mc.WarlordBonus, sPlot.isCoast())
				elif eHandicap == gc.getInfoTypeForString("HANDICAP_NOBLE"):
					if mc.NobleBonus > 0:
						print "Human player at Noble difficulty, adding %d resources" % mc.NobleBonus
						self.boostCityPlotValue(startPlot.getX(), startPlot.getY(), mc.NobleBonus, sPlot.isCoast())
				elif eHandicap == gc.getInfoTypeForString("HANDICAP_PRINCE"):
					if mc.PrinceBonus > 0:
						print "Human player at Prince difficulty, adding %d resources" % mc.PrinceBonus
						self.boostCityPlotValue(startPlot.getX(), startPlot.getY(), mc.PrinceBonus, sPlot.isCoast())
				elif eHandicap == gc.getInfoTypeForString("HANDICAP_MONARCH"):
					if mc.MonarchBonus > 0:
						print "Human player at Monarch difficulty, adding %d resources" % mc.MonarchBonus
						self.boostCityPlotValue(startPlot.getX(), startPlot.getY(), mc.MonarchBonus, sPlot.isCoast())
				elif eHandicap == gc.getInfoTypeForString("HANDICAP_EMPEROR"):
					if mc.EmperorBonus > 0:
						print "Human player at Emperor difficulty, adding %d resources" % mc.EmperorBonus
						self.boostCityPlotValue(startPlot.getX(), startPlot.getY(), mc.EmperorBonus, sPlot.isCoast())
				elif eHandicap == gc.getInfoTypeForString("HANDICAP_IMMORTAL"):
					if mc.ImmortalBonus > 0:
						print "Human player at Immortal difficulty, adding %d resources" % mc.ImmortalBonus
						self.boostCityPlotValue(startPlot.getX(), startPlot.getY(), mc.ImmortalBonus, sPlot.isCoast())
				elif eHandicap == gc.getInfoTypeForString("HANDICAP_TITAN"):
					if mc.TitanBonus > 0:
						print "Human player at Titan difficulty, adding %d resources" % mc.TitanBonus
						self.boostCityPlotValue(startPlot.getX(), startPlot.getY(), mc.TitanBonus, sPlot.isCoast())
				elif eHandicap == gc.getInfoTypeForString("HANDICAP_DEITY"):
					if mc.DeityBonus > 0:
						print "Human player at Deity Difficulty, adding %d resources" % mc.DeityBonus
						self.boostCityPlotValue(startPlot.getX(), startPlot.getY(), mc.DeityBonus, sPlot.isCoast())
 
#Global access
spf = StartingPlotFinder()

class CityPlot :
	def __init__(self,food,value):
		self.food = food
		self.value = value
class Improvement :
	def __init__(self,e,food,production,commerce,value):
		self.e = e
		self.food = food
		self.production = production
		self.commerce = commerce
		self.value = value

class StartingArea :
	def __init__(self,areaID):
		self.areaID = areaID
		self.playerList = list()
		self.plotList = list()
		self.distanceTable = array('i')
		self.rawValue = 0
		self.CalculatePlotList()
		self.idealNumberOfPlayers = 0
		return
	def CalculatePlotList(self):
		gc = CyGlobalContext()
		gameMap = CyMap()
		
		for y in range(mc.height):
			for x in range(mc.width):
				plot = gameMap.plot(x,y)
				if plot.getArea() == self.areaID:
					#don't place a city on top of a bonus
					if plot.getBonusType(TeamTypes.NO_TEAM) != BonusTypes.NO_BONUS:
						continue
					food,value = spf.getCityPotentialValue(x,y)
					if value > 0:
						startPlot = StartPlot(x,y,value)
						if plot.isWater() == True:
							raise ValueError, "potential start plot is water!"
						self.plotList.append(startPlot)
		#Sort plots by local value
		self.plotList.sort(lambda x, y: cmp(x.localValue, y.localValue))
		
		#To save time and space let's get rid of some of the lesser plots
		cull = (len(self.plotList) * 2) / 3
		for i in range(cull):
			del self.plotList[0]
			
		#You now should be able to eliminate more plots by sorting high to low
		#and having the best plot eat plots within 3 squares, then same for next,
		#etc.
		self.plotList.reverse()
##		print "number of initial plots in areaID = %(a)3d is %(p)5d" % {"a":self.areaID,"p":len(self.plotList)}
		numPlots = len(self.plotList)
		for n in range(numPlots):
			#At some point the length of plot list will be much shorter than at
			#the beginning of the loop, so it can never end normally
			if n >= len(self.plotList) - 1:
				break
			y = self.plotList[n].y
			x = self.plotList[n].x
			for yy in range(y - 3,y + 4):
				for xx in range(x - 3,x + 4):
					if yy < 0 or yy >= mc.height:
						continue
					xx = xx % mc.width#wrap xx
					if xx < 0:
						raise ValueError, "xx value not wrapping properly in StartingArea.CalculatePlotList"
					for m in range(n,len(self.plotList)):
						#At some point the length of plot list will be much shorter than at
						#the beginning of the loop, so it can never end normally
						if m >= len(self.plotList) - 1:
							break
##						print "m = %(m)3d, n = %(n)3d" % {"m":m,"n":n}
						if self.plotList[m] != self.plotList[n]:
							if self.plotList[m].x == xx and self.plotList[m].y == yy:
##								print "deleting m = %(m)3d" % {"m":m}
								del self.plotList[m]
##								print "length of plotList now %(len)4d" % {"len":len(self.plotList)}
								 
##		print "number of final plots in areaID = %(a)3d is %(p)5d" % {"a":self.areaID,"p":len(self.plotList)}
								
		#At this point we should have a list of the very best places
		#to build cities on this continent. Now we need a table with
		#the distance from each city to every other city

		#Create distance table
		for i in range(len(self.plotList)*len(self.plotList)):
			self.distanceTable.append(-11)
		#Fill distance table
		for n in range(len(self.plotList)):
			#While were already looping lets calculate the raw value
			self.rawValue += self.plotList[n].localValue
			avgDistance = 0
			for m in range(n,len(self.plotList)):
				nPlot = gameMap.plot(self.plotList[n].x,self.plotList[n].y)
				mPlot = gameMap.plot(self.plotList[m].x,self.plotList[m].y)
				gameMap.resetPathDistance()
				distance = gameMap.calculatePathDistance(nPlot,mPlot)
#			   distance = self.getDistance(nPlot.getX(),nPlot.getY(),mPlot.getX(),mPlot.getY())
				#If path fails try reversing it
##				gameMap.resetPathDistance()
##				newDistance = gameMap.calculatePathDistance(mPlot,nPlot)
##				if distance != newDistance:
##					print "distance between n=%(n)d nx=%(nx)d,ny=%(ny)d and m=%(m)d mx=%(mx)d,my=%(my)d is %(d)d or %(nd)d" % \
##					{"n":n,"nx":nPlot.getX(),"ny":nPlot.getY(),"m":m,"mx":mPlot.getX(),"my":mPlot.getY(),"d":distance,"nd":newDistance}
				self.distanceTable[n*len(self.plotList) + m] = distance
				self.distanceTable[m*len(self.plotList) + n] = distance
				avgDistance += distance
			self.plotList[n].avgDistance = avgDistance
 
		return
	def FindStartingPlots(self):
		gc = CyGlobalContext()
		gameMap = CyMap()
		numPlayers = len(self.playerList)
		if numPlayers <= 0:
			return

		avgDistanceList = list()
		for i in range(len(self.plotList)):
			avgDistanceList.append(self.plotList[i])
			
		#Make sure first guy starts on the end and not in the middle,
		#otherwise if there are two players one will start on the middle
		#and the other on the end
		avgDistanceList.sort(lambda x,y:cmp(x.avgDistance,y.avgDistance))
		avgDistanceList.reverse()
		#First place players as far as possible away from each other
		#Place the first player
		avgDistanceList[0].vacant = False
		for i in range(1,numPlayers):
			distanceList = list()
			for n in range(len(self.plotList)):
				if self.plotList[n].vacant == True:
					minDistance = -1
					for m in range(len(self.plotList)):
						if self.plotList[m].vacant == False:
							ii = n * len(self.plotList) + m
							distance = self.distanceTable[ii]
							if minDistance == -1 or minDistance > distance:
								minDistance = distance
					self.plotList[n].nearestStart = minDistance
					distanceList.append(self.plotList[n])
			#Find biggest nearestStart and place a start there
			distanceList.sort(lambda x,y:cmp(x.nearestStart,y.nearestStart))
			distanceList.reverse()
			distanceList[0].vacant = False
##			print "Placing start at x=%(x)d, y=%(y)d nearestDistance to city is %(n)d" % \
##			{"x":distanceList[0].x,"y":distanceList[0].y,"n":distanceList[0].nearestStart}
				
		self.CalculateStartingPlotValues()
				
##		self.PrintPlotMap()
##		self.PrintPlotList()
##		self.PrintDistanceTable()
	  
		#Now place all starting positions
		n = 0
		for m in range(len(self.plotList)):
			if self.plotList[m].vacant == False:
				sPlot = gameMap.plot(self.plotList[m].x,self.plotList[m].y)
				if sPlot.isWater() == True:
					raise ValueError, "Start plot is water!"
				sPlot.setImprovementType(gc.getInfoTypeForString("NO_IMPROVEMENT"))
				playerID = self.playerList[n]
				player = gc.getPlayer(playerID)
				sPlot.setStartingPlot(True)
				player.setStartingPlot(sPlot,True)
				n += 1

			
		return
	def CalculateStartingPlotValues(self):
		gameMap = CyMap()
		numPlots = len(self.plotList)
		
		for n in range(numPlots):
			self.plotList[n].owner = -1
			self.plotList[n].totalValue = 0
			
		for n in range(numPlots):
			if self.plotList[n].vacant == True:
				continue
			self.plotList[n].totalValue = 0
			self.plotList[n].numberOfOwnedCities = 0
			for m in range(numPlots):
				i = n * numPlots + m
				nDistance = self.distanceTable[i]
				if nDistance == -1:
					leastDistance = False
				else:
					leastDistance = True #Being optimistic, prove me wrong
				for p in range(numPlots):
					if p == n or self.plotList[p].vacant == True:
						continue
					ii = p * numPlots + m
					pDistance = self.distanceTable[ii]
##					print "n= %(n)3d, m = %(m)3d, p = %(p)3d, nDistance = %(nd)3d, pDistance = %(pd)3d" %\
##					{"n":n,"m":m,"p":p,"nd":nDistance,"pd":pDistance}
					if pDistance > -1 and pDistance <= nDistance:
						leastDistance = False #Proven wrong
						break
					
				if leastDistance == True:
					self.plotList[n].totalValue += self.plotList[m].localValue
#					print "m = %(m)3d owner change from %(mo)3d to %(n)3d" % {"m":m,"mo":self.plotList[m].owner,"n":n}
					self.plotList[m].owner = self.plotList[n]
					self.plotList[m].distanceToOwner = nDistance
					self.plotList[n].numberOfOwnedCities += 1
					
		return
	def getDistance(self,x,y,dx,dy):
		xx = x - dx
		if abs(xx) > mc.width/2:
			xx = mc.width - abs(xx)
			
		distance = max(abs(xx),abs(y - dy))
		return distance
	def PrintPlotMap(self):
		gameMap = CyMap()
		print "Starting Plot Map"
		for y in range(hm.mapHeight - 1,-1,-1):
			lineString = ""
			for x in range(hm.mapWidth):
				inList = False
				for n in range(len(self.plotList)):
					if self.plotList[n].x == x and self.plotList[n].y == y:
						if self.plotList[n].plot().isWater() == True:
							if self.plotList[n].vacant == True:
								lineString += 'VV'
							else:
								lineString += 'OO'
						else:
							if self.plotList[n].vacant == True:
								lineString += 'vv'
							else:
								lineString += 'oo'
						inList = True
						break
				if inList == False:
					plot = gameMap.plot(x,y)
					if plot.isWater() == True:
						lineString += '.;'
					else:
						lineString += '[]'

			lineString += "-" + str(y)
			print lineString
			
		lineString = " "
		print lineString

		return
	def PrintPlotList(self):
		for n in range(len(self.plotList)):
			print str(n) + ' ' + str(self.plotList[n])
		return
	
	def PrintDistanceTable(self):
		print "Distance Table"
		lineString = "%(n)05d" % {"n":0} + ' '
		for n in range(len(self.plotList)):
			lineString += "%(n)05d" % {"n":n} + ' '
		print lineString
		lineString = ""
		for n in range(len(self.plotList)):
			lineString = "%(n)05d" % {"n":n} + ' '
			for m in range(len(self.plotList)):
				i = n * len(self.plotList) + m
				lineString += "%(d)05d" % {"d":self.distanceTable[i]} + ' '
			print lineString	
		return

class StartPlot :
	def __init__(self,x,y,localValue):
		self.x = x
		self.y = y
		self.localValue = localValue
		self.totalValue = 0
		self.numberOfOwnedCities = 0
		self.distanceToOwner = -1
		self.nearestStart = -1
		self.vacant = True
		self.owner = None
		self.avgDistance = 0
		return
	def isCoast(self):
		gameMap = CyMap()
		plot = gameMap.plot(self.x,self.y)
		waterArea = plot.waterArea()
		if waterArea.isNone() == True or waterArea.isLake() == True: 
			return False
		return True
	
	def isRiverSide(self):
		gameMap = CyMap()
		plot = gameMap.plot(self.x,self.y)
		return plot.isRiverSide()		

	def plot(self):
		gameMap = CyMap()
		return gameMap.plot(self.x,self.y)
	def copy(self):
		cp = StartPlot(self.x,self.y,self.localValue)
		cp.totalValue = self.totalValue
		cp.numberOfOwnedCities = self.numberOfOwnedCities
		cp.distanceToOwner = self.distanceToOwner
		cp.nearestStart = self.nearestStart
		cp.vacant = self.vacant
		cp.owner = self.owner
		cp.avgDistance = self.avgDistance
		return cp
	def __str__(self):
		linestring = "x=%(x)3d,y=%(y)3d,localValue=%(lv)6d,totalValue =%(tv)6d, nearestStart=%(ad)6d, coastalCity=%(cc)d" % \
		{"x":self.x,"y":self.y,"lv":self.localValue,"tv":self.totalValue,"ad":self.nearestStart,"cc":self.isCoast()}
		return linestring
		
hm = HeightMap()
cm = ClimateMap()
sm = SmallMaps()
rm = RiverMap()
em = EuropeMap()
###############################################################################	 
#functions that civ is looking for
###############################################################################
def getVersion():
	return "1.20a"
	
def getDescription():
	"""
	A map's Description is displayed in the main menu when players go to begin a game.
	For no description return an empty string.
	"""
	return "Random map that simulates earth-like plate tectonics, " +\
		"geostrophic and monsoon winds and rainfall."
def getWrapX():
	return mc.WrapX
	
def getWrapY():
	print "mc.WrapY == %d at getWrapY" % mc.WrapY
	return mc.WrapY
	
def getNumCustomMapOptions():
	"""
	Number of different user-defined options for this map
	Return an integer
	"""
	mc.initialize()
	return OPTION_MAX
	
def getCustomMapOptionName(argsList):
	"""
	Returns name of specified option
	argsList[0] is Option ID (int)
	Return a Unicode string
	"""
	optionID = argsList[0]
	if optionID == OPTION_NewWorld:
		return "Civ placement"
	elif optionID == OPTION_Pangaea:
		return "Pangaea Rule"
	elif optionID == OPTION_Wrap:
		return "Wrap Option"
	elif optionID == OPTION_MapSeed:
		return "Map seed"
	elif optionID == OPTION_IslandFactor:
		return "Continent amount"
	elif optionID == OPTION_Patience:
		return "Patience amount"
	elif optionID == OPTION_MapRatio:
		return "Map ratio"
	elif optionID == OPTION_Handicap:
		return "Player bonus resources"
	elif optionID == OPTION_MapResources:
		return "Map resources"
	elif optionID == OPTION_NoRotate:
		return "Wrap land"
	elif optionID == OPTION_SmoothPeaks:
		return "Reduce Mountains"

	return u""
	
def getNumCustomMapOptionValues(argsList):
		"""
		Number of different choices for a particular setting
		argsList[0] is Option ID (int)
		Return an integer
		"""
		optionID = argsList[0]
		if optionID == OPTION_NewWorld:
			return 3
		elif optionID == OPTION_Pangaea:
			return 2
		elif optionID == OPTION_Wrap:
			return 4
		elif optionID == OPTION_MapSeed: # Map world
			return 12 # Number of possible map seed to choose
		elif optionID == OPTION_IslandFactor: # Number continents
			return 4
		elif optionID == OPTION_Patience: # Speed/quality tradeoff
		# Slow but good disabled: Causes infinite loops
			return 2
		elif optionID == OPTION_MapRatio: # Map ratio
			if ALLOW_EXTREME_RATIOS == 1:
				return 8 
			else:
				return 7
		elif optionID == OPTION_Handicap:
			return 4
		elif optionID == OPTION_MapResources:
			return 3
		elif optionID == OPTION_NoRotate:
			return 2
		elif optionID == OPTION_SmoothPeaks:
			return 2
		return 0
	
def getCustomMapOptionDescAt(argsList):
	"""
	Returns name of value of option at specified row
	argsList[0] is Option ID (int)
	argsList[1] is Selection Value ID (int)
	Return a Unicode string
	"""
	optionID = argsList[0]
	selectionID = argsList[1]
	if optionID == OPTION_NewWorld:
		if selectionID == 0:
			return "Keep New World empty"
		elif selectionID == 1:
			return "Start anywhere reasonable"
		elif selectionID == 2:
			return "Everyone on same landmass"
	elif optionID == OPTION_Pangaea:
		if selectionID == 0:
			return "Break Pangaeas"
		elif selectionID == 1:
			return "Allow Pangaeas"
	elif optionID == OPTION_Wrap:
		if selectionID == 0:
			return "Cylindrical"
		elif selectionID == 1:
			return "Toroidal"
		elif selectionID == 2:
			return "Flat"
		elif selectionID == 3:
			return "Toric w/ ice band"
	elif optionID == OPTION_MapSeed:
		if selectionID == 0:
			return "Random"
		elif selectionID == 1:
			return "T8"
		elif selectionID == 2:
			return "T5"
		elif selectionID == 3:
			return "T10"
		elif selectionID == 4:
			return "T285 (Big)"
		elif selectionID == 5:
			return "T324"
		elif selectionID == 6:
			return "T2997 (Nice)"
		elif selectionID == 7:
			return "T4677"
		elif selectionID == 8:
			return "T7187 (Small)"
		elif selectionID == 9:
			return "T8207 (Chili)"
		elif selectionID == 10:
			return "T12244 (Tiny)"
		elif selectionID == 11:
			return "T14194"
	elif optionID == OPTION_IslandFactor:
		if selectionID == 0:
			return "Few (faster)"
		elif selectionID == 1:
			return "Some"
		elif selectionID == 2:
			return "Many"
		elif selectionID == 3:
			return "Lots (slow)"
	elif optionID == OPTION_Patience:
		if selectionID == -1:
			return "Not very (Faster mapgen)"
		elif selectionID == 0:
			return "A little (faster mapgen)"
		elif selectionID == 1:
			return "Somewhat"
		elif selectionID == 2:
			return "Extremely (nicer map)"
	elif optionID == OPTION_MapRatio: # Map ratio
		if selectionID == 0: 
			return "2:3 (Tall map)" 
		elif selectionID == 1: 
			return "1:1 (Square map)"
		elif selectionID == 2:
			return "3:2 (Earth-like)"
		elif selectionID == 3:
			return "2:1 (Wide map)"
		elif selectionID == 4:
			return "7:1 (Ringworld)"
		elif selectionID == 5:
			return "3:3 (Big square)"
		elif selectionID == 6:
			return "6:4 (Huge earth-like; can be buggy)"
		elif selectionID == 7: 
			return "1:2 (BUGGY)" 
	elif optionID == OPTION_Handicap:
		if selectionID == 0:
			return "None (Player equal to AI)"
		elif selectionID == 1:
			return "A little"
		elif selectionID == 2:
			return "Some"
		elif selectionID == 3:
			return "Lots (Easier for player)"
	elif optionID == OPTION_MapResources:
		if selectionID == 0:
			return "Like Perfect World"
		elif selectionID == 1:
			return "Resources evenly spread"
		elif selectionID == 2:
			return "Full of resources"
	elif optionID == OPTION_NoRotate:
		if selectionID == 0:
			return "Fix continent split"
		else:
			return "PerfectWorld style"
	elif optionID == OPTION_SmoothPeaks:
		if selectionID == 0:
			return "No"
		else:
			return "Yes"
	return u""
	
def getCustomMapOptionDefault(argsList):
	"""
	Returns default value of specified option
	argsList[0] is Option ID (int)
	Return an integer
	"""
	#Always zero in this case
	#print argsList[0]
	if argsList[0] == OPTION_Patience:
		return 1 # Slow speed/good quality (Mark's default)
	elif argsList[0] == OPTION_MapRatio:
		return 2 # 3:2 Earthlike map
	elif argsList[0] == OPTION_SmoothPeaks:
		return 1 # By default, smooth coastal and other peaks
	else: # Everything else defaults to first choice
		return 0
	
def isRandomCustomMapOption(argsList):
	"""
	Returns a flag indicating whether a random option should be provided
	argsList[0] is Option ID (int)
	Return a bool
	"""
	return False
	
#This doesn't work with my river system so it is disabled. Some civs
#might start without a river. Boo hoo.
def normalizeAddRiver():
	return
def normalizeAddLakes():
	return
def normalizeAddGoodTerrain():
	return
def normalizeRemoveBadTerrain():
	return
def normalizeRemoveBadFeatures():
	return
def normalizeAddFoodBonuses():
	return
def normalizeAddExtras():
	print "-- normalizeAddExtras()"

	# Balance boni, place missing boni and move minerals
	balancer.normalizeAddExtras()

	# Do the default housekeeping
	CyPythonMgr().allowDefaultImpl()

	# Make sure marshes are on flatlands
	mst.marshMaker.normalizeMarshes()

	# Give extras to special regions
	mst.mapRegions.addRegionExtras()

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
	# Print manaMap if FFH
	if mst.bFFH: mst.mapPrint.buildBonusMap( True, "normalizeAddExtras():Mana", None, mst.mapPrint.manaDict )
	# Print riverMap
	mst.mapPrint.buildRiverMap( True, "normalizeAddExtras()" )
	# Print mod and map statistics
	mst.mapStats.mapStatistics()
	return
def normalizeRemovePeaks():
	return
GlobalThisIsAdvanced = 0
def isAdvancedMap():
	return 0
	
def isClimateMap():
	return 1
	
def isSeaLevelMap():
	return 1
	
def getTopLatitude():
	"Default is 90. 75 is past the Arctic Circle"
	return 90

def getBottomLatitude():
	"Default is -90. -75 is past the Antartic Circle"
	return -90
	
def getGridSize(argsList):
	grid_sizes = {
		WorldSizeTypes.WORLDSIZE_DUEL:		(11,7),
		WorldSizeTypes.WORLDSIZE_TINY:		(15,10),
		WorldSizeTypes.WORLDSIZE_SMALL:		(20,13),
		WorldSizeTypes.WORLDSIZE_STANDARD:	(24,16),
		WorldSizeTypes.WORLDSIZE_LARGE:		(30,20),
		WorldSizeTypes.WORLDSIZE_HUGE:		(36,24),
		WorldSizeTypes.WORLDSIZE_GIANT:		(42,28)
	}
	if (argsList[0] == -1): # (-1,) is passed to function on loads
			return []
	[eWorldSize] = argsList

	(sizex, sizey) = grid_sizes[eWorldSize]
	# The above values are for a 3:2 ratio.  We also support other ratios
	base_size = float(sizey) / 2 # base sizes: 3.5, 5, 6.5, 8, 10, 12
	sizex = int((base_size * mc.ratioX) + 0.5)
	sizey = int((base_size * mc.ratioY) + 0.5)
	
	# Let's reduce ice on smaller maps
	if(sizey < 20):
		mc.iceSlope *= 0.85
	if(sizey < 11):
		mc.iceSlope *= 0.85

	# The map generator goes in to an infinite loop if the output map is
	# bigger than (hmWidth, hmHeight)
	if(sizex > mc.maxMapWidth):
		sizex = mc.maxMapWidth
	if(sizey > mc.maxMapHeight):
		sizey = mc.maxMapHeight

	mc.serviceFlags |= sizey # 21 bits, we have 3 more for other flags
	return (sizex, sizey)

def generatePlotTypes():
	# Core height map generator
	gc = CyGlobalContext()
	mmap = gc.getMap()
	mc.width = mmap.getGridWidth()
	mc.height = mmap.getGridHeight()
	mc.minimumMeteorSize = (1 + int(round(float(mc.hmWidth)/float(mc.width)))) * 3
	PRand.seed()
	hm.performTectonics()
	hm.generateHeightMap()
	hm.combineMaps()
	hm.calculateSeaLevel()
	hm.fillInLakes()
	pb.breakPangaeas()
##	hm.Erode()
	hm.printHeightMap()
	hm.rotateMap()
	hm.addWaterBands()
##	hm.printHeightMap()
	cm.createClimateMaps()
	sm.initialize()
	rm.generateRiverMap()
	plotTypes = [PlotTypes.PLOT_OCEAN] * (mc.width*mc.height)

	for i in range(mc.width*mc.height):
		mapLoc = sm.plotMap[i]
		if mapLoc == mc.PEAK:
			plotTypes[i] = PlotTypes.PLOT_PEAK
		elif mapLoc == mc.HILLS:
			plotTypes[i] = PlotTypes.PLOT_HILLS
		elif mapLoc == mc.LAND:
			plotTypes[i] = PlotTypes.PLOT_LAND
		else:
			plotTypes[i] = PlotTypes.PLOT_OCEAN
	print "Finished generating plot types."		 
	return plotTypes

def generateTerrainTypes():
	NiTextOut("Generating Terrain  ...")
	print "Adding Terrain"
	gc = CyGlobalContext()
	terrainDesert = gc.getInfoTypeForString("TERRAIN_DESERT")
	terrainPlains = gc.getInfoTypeForString("TERRAIN_PLAINS")
	terrainIce = gc.getInfoTypeForString("TERRAIN_SNOW")
	terrainTundra = gc.getInfoTypeForString("TERRAIN_TUNDRA")
	terrainGrass = gc.getInfoTypeForString("TERRAIN_GRASS")
	terrainHill = gc.getInfoTypeForString("TERRAIN_HILL")
	terrainCoast = gc.getInfoTypeForString("TERRAIN_COAST")
	terrainOcean = gc.getInfoTypeForString("TERRAIN_OCEAN")
	terrainPeak = gc.getInfoTypeForString("TERRAIN_PEAK")
	
	terrainTypes = [0]*(mc.width*mc.height)
	for i in range(mc.width*mc.height):
		if sm.terrainMap[i] == mc.OCEAN:
			terrainTypes[i] = terrainOcean
		elif sm.terrainMap[i] == mc.COAST:
			terrainTypes[i] = terrainCoast
		elif sm.terrainMap[i] == mc.DESERT:
			terrainTypes[i] = terrainDesert
		elif sm.terrainMap[i] == mc.PLAINS:
			terrainTypes[i] = terrainPlains
		elif sm.terrainMap[i] == mc.GRASS:
			terrainTypes[i] = terrainGrass
		elif sm.terrainMap[i] == mc.TUNDRA:
			terrainTypes[i] = terrainTundra
		elif sm.terrainMap[i] == mc.SNOW:
			terrainTypes[i] = terrainIce
	print "Finished generating terrain types."
	return terrainTypes

def addRivers():
	NiTextOut("Adding Rivers....")
	print "Adding Rivers"
	gc = CyGlobalContext()
	pmap = gc.getMap()
	for y in range(mc.height):
		for x in range(mc.width):
			placeRiversInPlot(x,y)

##	rm.printRiverAndTerrainAlign()
			
	#peaks and rivers don't always mix well graphically, so lets eliminate
	#these potential glitches. Basically if there are adjacent peaks on both
	#sides of a river, either in a cardinal direction or diagonally, they
	#will look bad.
	for y in range(mc.height):
		for x in range(mc.width):
			plot = pmap.plot(x,y)
			if plot.isPeak() == True:
				if plot.isNOfRiver() == True:
					for xx in range(x - 1,x + 2,1):
						yy = y - 1
						if yy < 0:
							break
						#wrap in x direction
						if xx == -1:
							xx = mc.width - 1
						elif xx == mc.width:
							xx = 0
						newPlot = pmap.plot(xx,yy)
						ii = GetIndex(xx,yy)
						if newPlot.isPeak():
							plot.setPlotType(PlotTypes.PLOT_HILLS,True,True)
							sm.plotMap[ii] = mc.HILLS
							break
			#possibly changed so checked again
			if plot.isPeak() == True:
				if plot.isWOfRiver() == True:
					for yy in range(y - 1,y + 2,1):
						xx = x + 1
						if xx == mc.width:
							xx = 0
						#do not wrap in y direction
						if yy == -1:
							continue
						elif yy == mc.height:
							continue
						newPlot = pmap.plot(xx,yy)
						ii = GetIndex(xx,yy)
						if newPlot.isPeak():
							plot.setPlotType(PlotTypes.PLOT_HILLS,True,True)
							sm.plotMap[ii] = mc.HILLS
							break
	
def placeRiversInPlot(x,y):
	gc = CyGlobalContext()
	pmap = gc.getMap()
	plot = pmap.plot(x,y)
	#NE
	xx,yy = rm.rxFromPlot(x,y,rm.NE)
	ii = GetIndex(xx,yy)
	if ii != -1:
		if rm.riverMap[ii] == rm.S:
			plot.setWOfRiver(True,CardinalDirectionTypes.CARDINALDIRECTION_SOUTH)
	#SW
	xx,yy = rm.rxFromPlot(x,y,rm.SW)
	ii = GetIndex(xx,yy)
	if ii != -1:
		if rm.riverMap[ii] == rm.E:
			plot.setNOfRiver(True,CardinalDirectionTypes.CARDINALDIRECTION_EAST)
	#SE
	xx,yy = rm.rxFromPlot(x,y,rm.SE)
	ii = GetIndex(xx,yy)
	if ii != -1:
		if rm.riverMap[ii] == rm.N:
			plot.setWOfRiver(True,CardinalDirectionTypes.CARDINALDIRECTION_NORTH)
		elif rm.riverMap[ii] == rm.W:
			plot.setNOfRiver(True,CardinalDirectionTypes.CARDINALDIRECTION_WEST)

'''
This function examines a lake area and removes ugly surrounding rivers. Any
river that is flowing away from the lake, or alongside the lake will be
removed. This function also returns a list of riverID's that flow into the
lake.
'''
def cleanUpLake(x,y):
	gc = CyGlobalContext()
	mmap = gc.getMap()
	riversIntoLake = list()
	plot = mmap.plot(x,y+1)#North
	if plot != 0 and plot.isNOfRiver() == True:
		plot.setNOfRiver(False,CardinalDirectionTypes.NO_CARDINALDIRECTION)
	if plot != 0 and plot.isWOfRiver() == True:
		if plot.getRiverNSDirection() == CardinalDirectionTypes.CARDINALDIRECTION_SOUTH:
			riversIntoLake.append(plot.getRiverID())
		else:
			plot.setWOfRiver(False,CardinalDirectionTypes.NO_CARDINALDIRECTION)
	plot = mmap.plot(x - 1,y)#West
	if plot != 0 and plot.isWOfRiver() == True:
		plot.setWOfRiver(False,CardinalDirectionTypes.NO_CARDINALDIRECTION)
	if plot != 0 and plot.isNOfRiver() == True:
		if plot.getRiverWEDirection() == CardinalDirectionTypes.CARDINALDIRECTION_EAST:
			riversIntoLake.append(plot.getRiverID())
		else:
			plot.setNOfRiver(False,CardinalDirectionTypes.NO_CARDINALDIRECTION)
	plot = mmap.plot(x + 1,y)#East
	if plot != 0 and plot.isNOfRiver() == True:
		if plot.getRiverWEDirection() == CardinalDirectionTypes.CARDINALDIRECTION_WEST:
			riversIntoLake.append(plot.getRiverID())
		else:
			plot.setNOfRiver(False,CardinalDirectionTypes.NO_CARDINALDIRECTION)
	plot = mmap.plot(x,y-1)#South
	if plot != 0 and plot.isWOfRiver() == True:
		if plot.getRiverNSDirection() == CardinalDirectionTypes.CARDINALDIRECTION_NORTH:
			riversIntoLake.append(plot.getRiverID())
		else:
			plot.setWOfRiver(False,CardinalDirectionTypes.NO_CARDINALDIRECTION)
	plot = mmap.plot(x-1,y+1)#Northwest
	if plot != 0 and plot.isWOfRiver() == True:
		if plot.getRiverNSDirection() == CardinalDirectionTypes.CARDINALDIRECTION_SOUTH:
			riversIntoLake.append(plot.getRiverID())
		else:
			plot.setWOfRiver(False,CardinalDirectionTypes.NO_CARDINALDIRECTION)
	if plot != 0 and plot.isNOfRiver() == True:
		if plot.getRiverWEDirection() == CardinalDirectionTypes.CARDINALDIRECTION_EAST:
			riversIntoLake.append(plot.getRiverID())
		else:
			plot.setNOfRiver(False,CardinalDirectionTypes.NO_CARDINALDIRECTION)
	plot = mmap.plot(x+1,y+1)#Northeast
	if plot != 0 and plot.isNOfRiver() == True:
		if plot.getRiverWEDirection() == CardinalDirectionTypes.CARDINALDIRECTION_WEST:
			riversIntoLake.append(plot.getRiverID())
		else:
			plot.setNOfRiver(False,CardinalDirectionTypes.NO_CARDINALDIRECTION)
	plot = mmap.plot(x-1,y-1)#Southhwest
	if plot != 0 and plot.isWOfRiver() == True:
		if plot.getRiverNSDirection() == CardinalDirectionTypes.CARDINALDIRECTION_NORTH:
			riversIntoLake.append(plot.getRiverID())
		else:
			plot.setWOfRiver(False,CardinalDirectionTypes.NO_CARDINALDIRECTION)
	#Southeast plot is not relevant 
			
	return riversIntoLake

'''
This function replaces rivers to update the river crossings after a lake or
channel is placed at X,Y. There had been a long standing problem where water tiles
added after a river were causing graphical glitches and incorrect river rules
due to not updating the river crossings.
'''
def replaceRivers(x,y):
	gc = CyGlobalContext()
	mmap = gc.getMap()
	plot = mmap.plot(x,y+1)#North
	if plot != 0 and plot.isWOfRiver() == True:
		if plot.getRiverNSDirection() == CardinalDirectionTypes.CARDINALDIRECTION_SOUTH:
			#setting the river to what it already is will be ignored by the dll,
			#so it must be unset and then set again.
			plot.setWOfRiver(False,CardinalDirectionTypes.NO_CARDINALDIRECTION)
			plot.setWOfRiver(True,CardinalDirectionTypes.CARDINALDIRECTION_SOUTH)
	plot = mmap.plot(x - 1,y)#West
	if plot != 0 and plot.isNOfRiver() == True:
		if plot.getRiverWEDirection() == CardinalDirectionTypes.CARDINALDIRECTION_EAST:
			plot.setNOfRiver(False,CardinalDirectionTypes.NO_CARDINALDIRECTION)
			plot.setNOfRiver(True,CardinalDirectionTypes.CARDINALDIRECTION_EAST)
	plot = mmap.plot(x + 1,y)#East
	if plot != 0 and plot.isNOfRiver() == True:
		if plot.getRiverWEDirection() == CardinalDirectionTypes.CARDINALDIRECTION_WEST:
			plot.setNOfRiver(False,CardinalDirectionTypes.NO_CARDINALDIRECTION)
			plot.setNOfRiver(True,CardinalDirectionTypes.CARDINALDIRECTION_WEST)
	plot = mmap.plot(x,y-1)#South
	if plot != 0 and plot.isWOfRiver() == True:
		if plot.getRiverNSDirection() == CardinalDirectionTypes.CARDINALDIRECTION_NORTH:
			plot.setWOfRiver(False,CardinalDirectionTypes.NO_CARDINALDIRECTION)
			plot.setWOfRiver(True,CardinalDirectionTypes.CARDINALDIRECTION_NORTH)
	plot = mmap.plot(x-1,y+1)#Northwest
	if plot != 0 and plot.isWOfRiver() == True:
		if plot.getRiverNSDirection() == CardinalDirectionTypes.CARDINALDIRECTION_SOUTH:
			plot.setWOfRiver(False,CardinalDirectionTypes.NO_CARDINALDIRECTION)
			plot.setWOfRiver(True,CardinalDirectionTypes.CARDINALDIRECTION_SOUTH)
	if plot != 0 and plot.isNOfRiver() == True:
		if plot.getRiverWEDirection() == CardinalDirectionTypes.CARDINALDIRECTION_EAST:
			plot.setNOfRiver(False,CardinalDirectionTypes.NO_CARDINALDIRECTION)
			plot.setNOfRiver(True,CardinalDirectionTypes.CARDINALDIRECTION_EAST)
	plot = mmap.plot(x+1,y+1)#Northeast
	if plot != 0 and plot.isNOfRiver() == True:
		if plot.getRiverWEDirection() == CardinalDirectionTypes.CARDINALDIRECTION_WEST:
			plot.setNOfRiver(False,CardinalDirectionTypes.NO_CARDINALDIRECTION)
			plot.setNOfRiver(True,CardinalDirectionTypes.CARDINALDIRECTION_WEST)
	plot = mmap.plot(x-1,y-1)#Southhwest
	if plot != 0 and plot.isWOfRiver() == True:
		if plot.getRiverNSDirection() == CardinalDirectionTypes.CARDINALDIRECTION_NORTH:
			plot.setWOfRiver(False,CardinalDirectionTypes.NO_CARDINALDIRECTION)
			plot.setWOfRiver(True,CardinalDirectionTypes.CARDINALDIRECTION_NORTH)
	#Southeast plot is not relevant 
			
	return

'''
It looks bad to have a lake, fed by a river, sitting right next to the coast.
This function tries to minimize that occurance by replacing it with a
natural harbor, which looks much better.
'''
def makeHarbor(x,y,oceanMap):
	oceanID = oceanMap.getOceanID()
	i = oceanMap.getIndex(x,y)
	if oceanMap.areaMap[i] != oceanID:
		return
	#N
	xx = x
	yy = y + 2
	ii = oceanMap.getIndex(xx,yy)
	if ii > -1 and \
	oceanMap.getAreaByID(oceanMap.areaMap[ii]).water == True and \
	oceanMap.areaMap[ii] != oceanID:
		makeChannel(x,y + 1)
		oceanMap.defineAreas(isSmallWaterMatch)
		oceanID = oceanMap.getOceanID()
	#S
	xx = x
	yy = y - 2
	ii = oceanMap.getIndex(xx,yy)
	if ii > -1 and \
	oceanMap.getAreaByID(oceanMap.areaMap[ii]).water == True and \
	oceanMap.areaMap[ii] != oceanID:
		makeChannel(x,y - 1)
		oceanMap.defineAreas(isSmallWaterMatch)
		oceanID = oceanMap.getOceanID()
	#E
	xx = x + 2
	yy = y 
	ii = oceanMap.getIndex(xx,yy)
	if ii > -1 and \
	oceanMap.getAreaByID(oceanMap.areaMap[ii]).water == True and \
	oceanMap.areaMap[ii] != oceanID:
		makeChannel(x + 1,y)
		oceanMap.defineAreas(isSmallWaterMatch)
		oceanID = oceanMap.getOceanID()
	#W
	xx = x - 2
	yy = y 
	ii = oceanMap.getIndex(xx,yy)
	if ii > -1 and \
	oceanMap.getAreaByID(oceanMap.areaMap[ii]).water == True and \
	oceanMap.areaMap[ii] != oceanID:
		makeChannel(x - 1,y)
		oceanMap.defineAreas(isSmallWaterMatch)
		oceanID = oceanMap.getOceanID()
	#NW
	xx = x - 1
	yy = y + 1
	ii = oceanMap.getIndex(xx,yy)
	if ii > -1 and \
	oceanMap.getAreaByID(oceanMap.areaMap[ii]).water == True and \
	oceanMap.areaMap[ii] != oceanID:
		makeChannel(x - 1,y)
		oceanMap.defineAreas(isSmallWaterMatch)
		oceanID = oceanMap.getOceanID()
	#NE
	xx = x + 1
	yy = y + 1
	ii = oceanMap.getIndex(xx,yy)
	if ii > -1 and \
	oceanMap.getAreaByID(oceanMap.areaMap[ii]).water == True and \
	oceanMap.areaMap[ii] != oceanID:
		makeChannel(x + 1,y)
		oceanMap.defineAreas(isSmallWaterMatch)
		oceanID = oceanMap.getOceanID()
	#SW
	xx = x - 1
	yy = y - 1
	ii = oceanMap.getIndex(xx,yy)
	if ii > -1 and \
	oceanMap.getAreaByID(oceanMap.areaMap[ii]).water == True and \
	oceanMap.areaMap[ii] != oceanID:
		makeChannel(x ,y - 1)
		oceanMap.defineAreas(isSmallWaterMatch)
		oceanID = oceanMap.getOceanID()
	#NW
	xx = x - 1
	yy = y + 1
	ii = oceanMap.getIndex(xx,yy)
	if ii > -1 and \
	oceanMap.getAreaByID(oceanMap.areaMap[ii]).water == True and \
	oceanMap.areaMap[ii] != oceanID:
		makeChannel(x,y + 1)
		oceanMap.defineAreas(isSmallWaterMatch)
		oceanID = oceanMap.getOceanID()
	return
def makeChannel(x,y):
	gc = CyGlobalContext()
	mmap = gc.getMap()
	terrainCoast = gc.getInfoTypeForString("TERRAIN_COAST")
	plot = mmap.plot(x,y)
	cleanUpLake(x,y)
	plot.setTerrainType(terrainCoast,True,True)
	plot.setRiverID(-1)
	plot.setNOfRiver(False,CardinalDirectionTypes.NO_CARDINALDIRECTION)
	plot.setWOfRiver(False,CardinalDirectionTypes.NO_CARDINALDIRECTION)
	replaceRivers(x,y)
	i = GetIndex(x,y)
	sm.plotMap[i] = mc.OCEAN
	return
def expandLake(x,y,riversIntoLake,oceanMap):
	class LakePlot :
		def __init__(self,x,y,altitude):
			self.x = x
			self.y = y
			self.altitude = altitude
	gc = CyGlobalContext()
	mmap = gc.getMap()
	terrainCoast = gc.getInfoTypeForString("TERRAIN_COAST")
	lakePlots = list()
	lakeNeighbors = list()
	i = oceanMap.getIndex(x,y)
	desertModifier = 1.0
	if sm.terrainMap[i] == mc.DESERT:
		desertModifier = mc.DesertLakeModifier
	drainage = rm.drainageMap[i]
	lakeSize = max(3,int(drainage * mc.LakeSizePerDrainage * desertModifier ))
	start = LakePlot(x,y,sm.heightMap[i])
	lakeNeighbors.append(start)
#	print "lakeSize",lakeSize
	while lakeSize > 0 and len(lakeNeighbors) > 0:
#		lakeNeighbors.sort(key=operator.attrgetter('altitude'),reverse=False)
		lakeNeighbors.sort(lambda x,y:cmp(x.altitude,y.altitude))
		currentLakePlot = lakeNeighbors[0]
		del lakeNeighbors[0]
		lakePlots.append(currentLakePlot)
		plot = mmap.plot(currentLakePlot.x,currentLakePlot.y)
		#if you are erasing a river to make a lake, make the lake smaller
		if plot.isNOfRiver() == True or plot.isWOfRiver() == True:
			lakeSize -= 1
		makeChannel(currentLakePlot.x,currentLakePlot.y)
		#Add valid neighbors to lakeNeighbors
		for n in range(4):
			if n == 0:#N
				xx = currentLakePlot.x
				yy = currentLakePlot.y + 1
				ii = oceanMap.getIndex(xx,yy)
			elif n == 1:#S
				xx = currentLakePlot.x
				yy = currentLakePlot.y - 1
				ii = oceanMap.getIndex(xx,yy)
			elif n == 2:#E
				xx = currentLakePlot.x + 1
				yy = currentLakePlot.y
				ii = oceanMap.getIndex(xx,yy)
			elif n == 3:#W
				xx = currentLakePlot.x - 1
				yy = currentLakePlot.y 
				ii = oceanMap.getIndex(xx,yy)
			else:
				raise ValueError, "too many cardinal directions"
			if ii != -1:
				#if this neighbor is in water area, then quit
				areaID = oceanMap.areaMap[ii]
				if areaID == 0:
					raise ValueError, "areaID = 0 while generating lakes. This is a bug"
				for n in range(len(oceanMap.areaList)):
					if oceanMap.areaList[n].ID == areaID:
						if oceanMap.areaList[n].water == True:
#							print "lake touched waterID = %(id)3d with %(ls)3d squares unused" % {'id':areaID,'ls':lakeSize}
#							print "n = %(n)3d" % {"n":n}
#							print str(oceanMap.areaList[n])
							return
				if rm.riverMap[ii] != rm.L and mmap.plot(xx,yy).isWater() == False:
					lakeNeighbors.append(LakePlot(xx,yy,sm.heightMap[ii]))
		
		lakeSize -= 1
#	print "lake finished normally at %(x)2d,%(y)2d" % {"x":x,"y":y}
	return
			
def addLakes():
	print "Adding Lakes"
	gc = CyGlobalContext()
	mmap = gc.getMap()
	terrainCoast = gc.getInfoTypeForString("TERRAIN_COAST")
#	PrintFlowMap()
	oceanMap = Areamap(mc.width,mc.height,True,True)
	oceanMap.defineAreas(isSmallWaterMatch)
##	oceanMap.PrintList(oceanMap.areaList)
##	oceanMap.PrintAreaMap()
	for y in range(mc.height):
		for x in range(mc.width):
			i = GetIndex(x,y)
			if rm.flowMap[i] == rm.L:
				riversIntoLake = cleanUpLake(x,y)
				plot = mmap.plot(x,y)
				if len(riversIntoLake) > 0:
##					plot.setRiverID(-1)
##					plot.setNOfRiver(False,CardinalDirectionTypes.NO_CARDINALDIRECTION)
##					plot.setWOfRiver(False,CardinalDirectionTypes.NO_CARDINALDIRECTION)
##					#plot.setPlotType(PlotTypes.PLOT_OCEAN,True,True) setTerrain handles this already
##					plot.setTerrainType(terrainCoast,True,True)
					expandLake(x,y,riversIntoLake,oceanMap)
				else:
					#no lake here, but in that case there should be no rivers either
					plot.setRiverID(-1)
					plot.setNOfRiver(False,CardinalDirectionTypes.NO_CARDINALDIRECTION)
					plot.setWOfRiver(False,CardinalDirectionTypes.NO_CARDINALDIRECTION)
	oceanMap.defineAreas(isSmallWaterMatch)
##	oceanMap.PrintList(oceanMap.areaList)
##	oceanMap.PrintAreaMap()
	for y in range(mc.height):
		for x in range(mc.width):
			i = GetIndex(x,y)
			makeHarbor(x,y,oceanMap)
	return
		
def addFeatures():
	NiTextOut("Generating Features  ...")
	print "Adding Features"
	gc = CyGlobalContext()
	mmap = gc.getMap()
	featureIce = gc.getInfoTypeForString("FEATURE_ICE")
	featureJungle = gc.getInfoTypeForString("FEATURE_JUNGLE")
	featureForest = gc.getInfoTypeForString("FEATURE_FOREST")
	featureOasis = gc.getInfoTypeForString("FEATURE_OASIS")
	featureFloodPlains = gc.getInfoTypeForString("FEATURE_FLOOD_PLAINS")
	fScrub	   = gc.getInfoTypeForString("FEATURE_SCRUB")
	fMushrooms   = gc.getInfoTypeForString("FEATURE_HOTSPRINGS")
	fSoil1	   = gc.getInfoTypeForString("FERTILE_SOIL_GRASS")
	fSoil2	   = gc.getInfoTypeForString("FERTILE_SOIL_PLAINS")
	fSavannah	= gc.getInfoTypeForString("FEATURE_SAVANNA")
	fMarsh	   = gc.getInfoTypeForString("FEATURE_SWAMP")
	fReef		= gc.getInfoTypeForString("FEATURE_REEF")
	fIsland	  = gc.getInfoTypeForString("FEATURE_ISLAND")
	fIslandNorth = gc.getInfoTypeForString("FEATURE_ISLAND_NORTH")
	FORESTLEAFY = 0
	FORESTEVERGREEN = 1
	FORESTSNOWY = 2

	createIce()

	hotMarshTiles   = []
	hotMarshLength  = 0
	midMarshTiles   = []
	midMarshLength  = 0
	coldMarshTiles  = []
	coldMarshLength = 0
	for y in range(mc.height):
		for x in range(mc.width):
			i = GetIndex(x, y)
			if sm.plotMap[i] == mc.LAND:
				if sm.terrainMap[i] == mc.GRASS:
					if sm.averageTempMap[i] > mc.JungleTemp:
						hotMarshTiles.append(sm.rainFallMap[i])
						hotMarshLength += 1
					else:
						midMarshTiles.append(sm.rainFallMap[i])
						midMarshLength += 1
				elif sm.terrainMap[i] == mc.TUNDRA:
					coldMarshTiles.append(sm.rainFallMap[i])
					coldMarshLength += 1
	hotMarshThreshold  = FindValueFromPercentLen(hotMarshTiles,  hotMarshLength,  mc.HotMarshPercent,  True)
	midMarshThreshold  = FindValueFromPercentLen(midMarshTiles,  midMarshLength,  mc.MidMarshPercent,  True)
	coldMarshThreshold = FindValueFromPercentLen(coldMarshTiles, coldMarshLength, mc.ColdMarshPercent, True)
	
	#Now plant forest or jungle
##	PrintTempMap(tm,tm.tempMap)
##	PrintRainMap(rm,rm.rainMap,False)
	for y in range(mc.height):
		for x in range(mc.width):
			lat = cm.getLatitude(y)
			i = GetIndex(x,y)
			plot = mmap.plot(x,y)
			#RI features, floodplains and Oasis
			if not plot.isWater() and sm.terrainMap[i] != mc.DESERT and sm.terrainMap[i] != mc.SNOW and not plot.isPeak():
				if sm.terrainMap[i] == mc.GRASS and sm.plotMap[i] == mc.LAND and (sm.rainFallMap[i] * PRand.randint(50, 150) / 100) >= hotMarshThreshold and sm.averageTempMap[i] >= mc.JungleTemp:
					plot.setFeatureType(fMarsh, -1)
				elif sm.terrainMap[i] == mc.GRASS and sm.plotMap[i] == mc.LAND and (sm.rainFallMap[i] * PRand.randint(50, 150) / 100) >= midMarshThreshold and sm.averageTempMap[i] <  mc.JungleTemp:
					plot.setFeatureType(fMarsh, -1)
				elif sm.terrainMap[i] == mc.TUNDRA and sm.plotMap[i] == mc.LAND and (sm.rainFallMap[i] * PRand.randint(50, 150) / 100) >= coldMarshThreshold:
					plot.setFeatureType(fMarsh, -1)
				elif abs(lat) >= 60 and PRand.random() < mc.MushroomChance:
					plot.setFeatureType(fMushrooms, -1)
					set = True	
				elif sm.terrainMap[i] == mc.GRASS and sm.plotMap[i] == mc.LAND and abs(lat) <= 60 and PRand.random() < mc.Soil1Chance:
					plot.setFeatureType(fSoil1, -1)
					set = True
				elif sm.terrainMap[i] == mc.PLAINS and sm.plotMap[i] == mc.LAND and abs(lat) <= 60 and PRand.random() < mc.Soil2Chance:
					plot.setFeatureType(fSoil2, -1)
					set = True	
			elif sm.terrainMap[i] == mc.DESERT and sm.plotMap[i] != mc.HILLS and sm.plotMap[i] != mc.PEAK and plot.isWater() == False:
				if plot.isRiver() == True:
					plot.setFeatureType(featureFloodPlains,0)
				else:
					#is this square surrounded by desert?
					foundNonDesert = False
					foundWater = False
					#print "trying to place oasis"
					for yy in range(y - 1,y + 2):
						for xx in range(x - 1,x + 2):
							ii = GetIndex(xx,yy)
							surPlot = mmap.plot(xx,yy)
							if (sm.terrainMap[ii] != mc.DESERT and \
							sm.plotMap[ii] != mc.PEAK):
								#print "non desert neighbor"
								foundNonDesert = True
							elif surPlot == 0:
								#print "neighbor off map"
								foundNonDesert = True
							elif surPlot.isWater() == True:
								#print "water neighbor"
								foundNonDesert = True
								foundWater = True
							elif surPlot.getFeatureType() == featureOasis:
								#print "oasis neighbor"
								foundNonDesert = True
					if foundNonDesert == False:
						if PRand.random() < mc.OasisChance:
							#print "placing oasis"
							plot.setFeatureType(featureOasis,0)
					   # else:
							#print "oasis failed random check"
					if foundWater == False:
						if PRand.random() < mc.ScrubMinChance:
							plot.setFeatureType(fScrub,-1)
			#RI water features				
			elif sm.terrainMap[i] == mc.COAST and plot.getFeatureType() == FeatureTypes.NO_FEATURE:
				if PRand.random() < mc.ReefChance:
					plot.setFeatureType(fReef, -1)
					set = True
				if abs(lat) <= 69:
					if PRand.random() < mc.IslandChance:
						plot.setFeatureType(fIsland, -1)
						set = True
				if (abs(lat) > 69 and abs(lat) <= 90):
					if plot.isPotentialCityWork() and PRand.random() < mc.IslandChance / 2.0:
						plot.setFeatureType(fIslandNorth, -1)
						set = True
			#forest and jungle
			if plot.isWater() == False and sm.terrainMap[i] != mc.DESERT and plot.isPeak() == False and plot.getFeatureType() == FeatureTypes.NO_FEATURE:
				if sm.rainFallMap[i] > sm.plainsThreshold * mc.TreeFactor and PRand.random() < mc.MaxTreeChance:#jungle
					if sm.averageTempMap[i] > mc.JungleTemp:
						plot.setFeatureType(featureJungle,-1)
					elif sm.averageTempMap[i] > mc.ForestTemp:
						plot.setFeatureType(featureForest,FORESTLEAFY)
					elif sm.averageTempMap[i] > mc.TundraTemp:
						plot.setFeatureType(featureForest,FORESTEVERGREEN)
					elif sm.averageTempMap[i] > mc.SnowTemp:
						plot.setFeatureType(featureForest,FORESTSNOWY)
				elif sm.rainFallMap[i] > sm.desertThreshold:#forest
					if sm.rainFallMap[i] > PRand.random() * sm.plainsThreshold * mc.TreeFactor / mc.MaxTreeChance:
						if sm.averageTempMap[i] > mc.JungleTemp:
							if sm.terrainMap[i] == mc.PLAINS:
								plot.setFeatureType(fSavannah,-1)
						elif sm.averageTempMap[i] > mc.ForestTemp:
						   plot.setFeatureType(featureForest,FORESTLEAFY)
						elif sm.averageTempMap[i] > mc.TundraTemp:
							plot.setFeatureType(featureForest,FORESTEVERGREEN)
						elif sm.averageTempMap[i] > mc.SnowTemp * 0.8:
							plot.setFeatureType(featureForest,FORESTSNOWY)			
	return
	
def createIce():
	gc = CyGlobalContext()
	mmap = gc.getMap()
	featureIce = gc.getInfoTypeForString("FEATURE_ICE")
	iceChance = mc.iceChance
	iceRange = mc.iceRange
	iceSlope = mc.iceSlope
	signadded = 0 # We add the "Service Tag" sign while drawing ice
	if(ADD_SERVICE_TAG != 1):
		signadded = 1 # WARNING: NO SERVICE TAG MEANS NO SUPPORT
	print "SERVICE TAG: " + mc.serviceString # Always log it, of course
	for y in range(iceRange):
		for x in range(mc.width):
			plot = mmap.plot(x,y)
			if plot != 0 and plot.isWater() == True and PRand.random() < iceChance:
				plot.setFeatureType(featureIce,0)
		iceChance *= iceSlope
	iceChance = mc.iceChance
	for y in range(mc.height - 1,mc.height - 1 - iceRange,-1):
		for x in range(mc.width):
			plot = mmap.plot(x,y)
			if plot != 0 and plot.isWater() == True and PRand.random() < iceChance:
				plot.setFeatureType(featureIce,0)
				if signadded == 0:
					CyEngine().addSign(plot, -1, mc.serviceString)
			print "Sign added at %d %d" % (x,y)
			signadded = 1
		iceChance *= iceSlope
	# Make sure the service tag gets added to the map
	if signadded == 0:
		plot = mmap.plot(0,0)
		CyEngine().addSign(plot, -1, mc.serviceString)	
		print "Sign added at 0 0" % (x,y)

def addBonuses():
	bp.AddBonuses()
	return
def assignStartingPlots():
	gc = CyGlobalContext()
	gameMap = CyMap()
	iPlayers = gc.getGame().countCivPlayersEverAlive()
	spf.SetStartingPlots()
	
def beforeInit():
	print "Initializing Custom Map Options"
	mc.initInGameOptions()
	mc.initialize()

# Add huts to the map
# Use Civ4-specific code to place the hut
def placeHut(x,y):
	cigc = CyGlobalContext()
	gMap = CyMap()
	nativeHut = cigc.getInfoTypeForString("IMPROVEMENT_GOODY_HUT")
	hereGame = gMap.plot(x,y)
	hereGame.setImprovementType(nativeHut)

# Check to see if we can place a hut on a given square
def checkHut(hutSeen, x, y):
	if hutSeen[(y * mc.width) + x] != 0:
		return False
	# If we can place a hut, make sure we can not place any future huts
	# within two squares of this hut
	for xx in range(-2,3):
		if x + xx >= 0 and x + xx < mc.width:
			for yy in range(-2,3):
				if y + yy >= 0 and y + yy < mc.height:
					hutSeen[((y + yy) * mc.width) + (x + xx)] = 1 # No hut here
	hutSeen[(y * mc.width) + x] = 2 # Physical hut
	placeHut(x,y)
	return True 

def addGoodies():
	# Uncomment the following two lines to have PerfectWorld/Civ4 behavior
	# This means the huts will change every time the map is made
	CyPythonMgr().allowDefaultImpl()
	return
	#hutSeen = [0 for i in range(mc.width * mc.height)]
	#for x in range(mc.width):
	#	for y in range(mc.height):
	#		i = (y * mc.width) + x
	#		if(sm.plotMap[i] == mc.HILLS or sm.plotMap[i] == mc.LAND):
	#			# Different terrains have different hut chances
	#			if(sm.terrainMap[i] == mc.DESERT):
	#				if(PRand.randint(0,999) < mc.desertHutChance):
	#					checkHut(hutSeen, x, y)
	#			elif(sm.terrainMap[i] != mc.SNOW):
	#				if(PRand.randint(0,999) < mc.normalHutChance):
	#					checkHut(hutSeen, x, y)
			   
	
##mc.initialize()
##PRand.seed()
##hm.performTectonics()
##hm.generateHeightMap()
##hm.combineMaps()
##hm.calculateSeaLevel()
####hm.printHeightMap()
##hm.fillInLakes()
##pb.breakPangaeas()
####hm.printHeightMap()
####hm.Erode()
##hm.printHeightMap()
##hm.addWaterBands()
##cm.createClimateMaps()
##cm.printTempMap(cm.summerTempsMap)
##cm.printTempMap(cm.winterTempsMap)
##cm.printTempMap(cm.averageTempMap)
##cm.printRainFallMap(False)
##cm.printRainFallMap(True)
##sm.initialize()
##rm.generateRiverMap()
####sm.printHeightMap()
####rm.printRiverMap()
####sm.printPlotMap()
##sm.printTerrainMap()
##rm.printFlowMap()
##rm.printRiverMap()
##rm.printRiverAndTerrainAlign()

##sm.printHeightMap()

if __name__ == "__main__":
	IsStandAlone = True
	import sys
	mc.UsePythonRandom = True
	if len(sys.argv) > 1:
		if(len(sys.argv) > 2 and sys.argv[1] == '--test'):
			do_rg32_test(sys.argv[2])
			sys.exit(0)
		mc.totestra = int(sys.argv[1])
	if(mc.totestra):
		mySeed = str(mc.totestra)
	else:
		mySeed = "Unknown"
	mc.initialize()
	# This stuff has to be hard coded here
	mc.width = 144
	mc.height = 96
	mc.landPercent = 0.29
	mc.tropicsLatitude = 23
	mc.PeakPercent = 0.12
	mc.HillPercent = 0.35
	mc.HillChanceAtOne = .50
	mc.PeakChanceAtOne = .27
	mc.DesertPercent = 0.20
	mc.PlainsPercent = 0.42
	mc.SnowTemp = .30
	mc.TundraTemp = .35
	mc.ForestTemp = .50
	mc.JungleTemp = .6
	mc.iceChance = 1.0
	mc.iceRange = 4
	mc.iceSlope = 0.66
	if len(sys.argv) <= 2: # Arid map
		mc.DesertPercent = 0.40
		mc.PlainsPercent = 0.82
		mc.iceSlope = 0.33 # Less ice 
	mc.AllowPangeas = False
	mc.patience = 2
	mc.hmMaxGrain = 2 ** (2 + mc.patience)
	mc.hmWidth = (mc.hmMaxGrain * 3 * 3)
	mc.hmHeight =  (mc.hmMaxGrain * 2 * 3) + 1
	mc.WrapX = True
	mc.WrapY = False
	mc.BonusBonus = 1.5 # Full of resources
	mc.spreadResources = True # Full of resources
	mc.noRotate = 0
	mc.smoothPeaks = 1
	mc.northWaterBand = 10
	mc.southWaterBand = 10
	mc.eastWaterBand = 0
	mc.westWaterBand = 0
	mc.northCrop = 10
	mc.southCrop = 10
	mc.eastCrop = 0
	mc.westCrop = 0
	mc.maxMapWidth = int(mc.hmWidth / 4)
	mc.maxMapHeight = int(mc.hmHeight / 4)
	if(mc.width > mc.hmWidth):
		mc.width = mc.hmWidth
	if(mc.height > mc.hmHeight):
		mc.height = mc.hmHeight
	if(mc.patience == 1):
		mc.hmNumberOfPlates = int(float(mc.hmWidth * mc.hmHeight) * 0.0024)
	else: # Patience is assumed to be 2
		mc.hmNumberOfPlates = int(float(mc.hmWidth * mc.hmHeight) * 0.0016)

	mc.minimumMeteorSize = (1 + int(round(float(mc.hmWidth)/float(mc.width)))) * 3
	mc.AllowNewWorld = True
	mc.ShareContinent = True
	PRand.seed()
	hm.performTectonics()
	hm.generateHeightMap()
	hm.combineMaps()
	hm.calculateSeaLevel()
	hm.fillInLakes()
	pb.breakPangaeas()
##	hm.Erode()
##	hm.printHeightMap()
	hm.rotateMap()
	hm.addWaterBands()
##	hm.printHeightMap()
	cm.createClimateMaps()
	sm.initialize()
	rm.generateRiverMap()

	# Scan the map and give the user a summary of the map
	floodPlainCount = 0
	tally = {}
	bigAM = Areamap(mc.width,mc.height,True,True)
	bigAM.defineAreas(isNonCoastWaterMatch)
	maxLandAmount = -1
	maxLandArea = -1
	for x in range(mc.width):
		for y in range(mc.height):
			i = (y * mc.width) + x
			#area = continentMap.areaMap.areaMap[i]
			area = bigAM.areaMap[i]
			if not area in tally:
				tally[area] = {
					"Land": 0,
					"Desert": 0,
					"floodPlains": 0,
					"Tundra": 0
				}
			if sm.terrainMap[i] != mc.OCEAN and sm.terrainMap[i] != mc.COAST:
				tally[area]["Land"] += 1
				if(tally[area]["Land"] > maxLandAmount):
					maxLandAmount = tally[area]["Land"]
					maxLandArea = area
			if sm.terrainMap[i] == mc.DESERT:
				tally[area]["Desert"] += 1
				if rm.riverMap[i] != 5:
					floodPlainCount += 1
					tally[area]["floodPlains"] += 1
			if sm.terrainMap[i] == mc.TUNDRA:
				tally[area]["Tundra"] += 1
	print("Flood plain count: " + str(floodPlainCount))
	for area in tally:
		print("Tally for continent " + str(area) + ": " +
			  str(tally[area]))
	print("Biggest is " + str(maxLandArea) + " with :"+str(tally[maxLandArea]))
	if(maxLandArea >= 0 and tally[maxLandArea]["Tundra"] < 10 and
	   tally[maxLandArea]["floodPlains"] > 30 and
	   tally[maxLandArea]["Desert"] > 500 and
	   tally[maxLandArea]["Land"] > 1000):
		print("Nice land found seed " + mySeed)


