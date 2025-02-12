cmake_minimum_required(VERSION 3.16.0 FATAL_ERROR)

project(CvGameCoreDLL.BtS CXX)

################################################################################
# Set target arch type if empty. Visual studio solution generator provides it.
################################################################################
if(NOT CMAKE_VS_PLATFORM_NAME)
    set(CMAKE_VS_PLATFORM_NAME "x64")
endif()
message("${CMAKE_VS_PLATFORM_NAME} architecture in use")

################################################################################
# Include headers dirs
################################################################################

if (CMAKE_CXX_COMPILER_ID STREQUAL "GNU")

    # find python package
    find_package(PythonLibs REQUIRED)
    include_directories(${PYTHON_INCLUDE_DIRS})

endif()


################################################################################
# Global configuration types
################################################################################
set(CMAKE_CONFIGURATION_TYPES
    "Assert"
    "Assertfast"
    "Debug"
    "Profile"
    "Release"
    "Releasefast"
    "ReleaseOpti"
    CACHE STRING "" FORCE
)

################################################################################
# Global compiler options
################################################################################
if (CMAKE_CXX_COMPILER_ID STREQUAL "GNU")

    # find flags

    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 -DHAVE_INTTYPES_NETINET_IN_H")

    # detect undefined symbol error
    #set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -shared -Wl,-soname,libpython3.9.so.1.0 -Wl,--no-undefined")
elseif(MSVC)
    # To Doo
endif()

################################################################################
# Global linker options
################################################################################
if (CMAKE_CXX_COMPILER_ID STREQUAL "GNU")

    # find flags

    set(CMAKE_EXE_LINKER_FLAGS "-std=c++11 -DHAVE_INTTYPES_NETINET_IN_H")
    set(CMAKE_SHARED_LINKER_FLAGS "-std=c++11 -DHAVE_INTTYPES_NETINET_IN_H")

    # detect undefined symbol error for python library
    #set(CMAKE_EXE_LINKER_FLAGS "-shared -Wl,-soname,libpython3.9.so.1.0 -Wl,--no-undefined")
    #set(CMAKE_SHARED_LINKER_FLAGS "-shared -Wl,-soname,libpython3.9.so.1.0 -Wl,--no-undefined")
elseif(MSVC)
    # To Doo
endif()

################################################################################
# Nuget packages function stub.
################################################################################
function(use_package TARGET PACKAGE VERSION)
    message(WARNING "No implementation of use_package. Create yours. "
                    "Package \"${PACKAGE}\" with version \"${VERSION}\" "
                    "for target \"${TARGET}\" is ignored!")
endfunction()

################################################################################
# Common utils
################################################################################

################################################################################
# Additional Global Settings(add specific info there)
################################################################################

################################################################################
# Use solution folders feature
################################################################################
set_property(GLOBAL PROPERTY USE_FOLDERS ON)

################################################################################
# Sub-projects
################################################################################

set(PROJECT_NAME CvGameCoreDLL)

################################################################################
#options suported by the cmake builder
################################################################################
option(WITH_LOG_AI "Logging AI enable" OFF)


###############################################################################
# Project variables
###############################################################################

if(WITH_LOG_AI)
  set(LOG_AI True)
endif(WITH_LOG_AI)

################################################################################
# Source groups
################################################################################
source_group("" FILES ${no_group_source_files})

set(Headers
    "CvDepends.h"
    "AI_Defines.h"
    "CvArea.h"
    "CvArtFileMgr.h"
    "CvCity.h"
    "CvCityAI.h"
    "CvDeal.h"
    "CvDefines.h"
    "CvDiploParameters.h"
    "CvDLLButtonPopup.h"
    "CvDLLDataStreamIFaceBase.h"
    "CvDLLEngineIFaceBase.h"
    "CvDLLEntity.h"
    "CvDLLEntityIFaceBase.h"
    "CvDLLEventReporterIFaceBase.h"
    "CvDLLFAStarIFaceBase.h"
    "CvDLLFlagEntityIFaceBase.h"
    "CvDLLIniParserIFaceBase.h"
    "CvDLLInterfaceIFaceBase.h"
    "CvDLLPlotBuilderIFaceBase.h"
    "CvDllPythonEvents.h"
    "CvDLLPythonIFaceBase.h"
    "CvDLLSymbolIFaceBase.h"
    "CvDllTranslator.h"
    "CvDLLUtilityIFaceBase.h"
    "CvDLLWidgetData.h"
    "CvDLLXMLIFaceBase.h"
    "CvEnums.h"
    "CvEventReporter.h"
    "CvFractal.h"
    "CvGame.h"
    "CvGameAI.h"
    "CvGameCoreDLL.h"
    "CvGameCoreDLLDefNew.h"
    "CvGameCoreDLLUndefNew.h"
    "CvGameCoreUtils.h"
    "CvGameTextMgr.h"
    "CvGlobals.h"
    "CvHallOfFameInfo.h"
    "CvInfos.h"
    "CvInfoWater.h"
    "CvInitCore.h"
    "CvMap.h"
    "CvMapGenerator.h"
    "CvMessageControl.h"
    "CvMessageData.h"
    "CvPlayer.h"
    "CvPlayerAI.h"
    "CvPlot.h"
    "CvPlotGroup.h"
    "CvPopupInfo.h"
    "CvPopupReturn.h"
    "CvRandom.h"
    "CvReplayInfo.h"
    "CvReplayMessage.h"
    "CvSelectionGroup.h"
    "CvSelectionGroupAI.h"
    "CvStatistics.h"
    "CvString.h"
    "CvStructs.h"
    "CvTalkingHeadMessage.h"
    "CvTeam.h"
    "CvTeamAI.h"
    "CvUnit.h"
    "CvUnitAI.h"
    "CvXMLLoadUtility.h"
    "CyArea.h"
    "CyArgsList.h"
    "CyArtFileMgr.h"
    "CyCity.h"
    "CyDeal.h"
    "CyGame.h"
    "CyGameCoreUtils.h"
    "CyGameTextMgr.h"
    "CyGlobalContext.h"
    "CyHallOfFameInfo.h"
    "CyMap.h"
    "CyMapGenerator.h"
    "CyMessageControl.h"
    "CyPlayer.h"
    "CyPlot.h"
    "CyReplayInfo.h"
    "CySelectionGroup.h"
    "CyTeam.h"
    "CyUnit.h"
    "FAssert.h"
    "FAStarNode.h"
    "FDataStreamBase.h"
    "FDialogTemplate.h"
    "FFreeListArray.h"
    "FFreeListArrayBase.h"
    "FFreeListTrashArray.h"
    "FInputDevice.h"
    "FProfiler.h"
    "FVariableSystem.h"
    "FVariableSystem.inl"
    "LinkedList.h"
    "interfaceDirtyBits.inl"
    "resource.h"
    "UnofficialPatch.h"
)
source_group("Headers" FILES ${Headers})

set(Sources
    "_precompile.cpp"
    "CvArea.cpp"
    "CvArtFileMgr.cpp"
    "CvCity.cpp"
    "CvCityAI.cpp"
    "CvDeal.cpp"
    "CvDiploParameters.cpp"
    "CvDLLButtonPopup.cpp"
    "CvDLLEntity.cpp"
    "CvDLLPython.cpp"
    "CvDllPythonEvents.cpp"
    "CvDllTranslator.cpp"
    "CvDLLWidgetData.cpp"
    "CvEventReporter.cpp"
    "CvFractal.cpp"
    "CvGame.cpp"
    "CvGameAI.cpp"
    "CvGameCoreDLL.cpp"
    "CvGameCoreUtils.cpp"
    "CvGameInterface.cpp"
    "CvGameTextMgr.cpp"
    "CvGlobals.cpp"
    "CvHallOfFameInfo.cpp"
    "CvInfos.cpp"
    "CvInfoWater.cpp"
    "CvInitCore.cpp"
    "CvMap.cpp"
    "CvMapGenerator.cpp"
    "CvMessageControl.cpp"
    "CvMessageData.cpp"
    "CvPlayer.cpp"
    "CvPlayerAI.cpp"
    "CvPlot.cpp"
    "CvPlotGroup.cpp"
    "CvPopupInfo.cpp"
    "CvPopupReturn.cpp"
    "CvRandom.cpp"
    "CvReplayInfo.cpp"
    "CvReplayMessage.cpp"
    "CvSelectionGroup.cpp"
    "CvSelectionGroupAI.cpp"
    "CvStatistics.cpp"
    "CvStructs.cpp"
    "CvTalkingHeadMessage.cpp"
    "CvTeam.cpp"
    "CvTeamAI.cpp"
    "CvUnit.cpp"
    "CvUnitAI.cpp"
    "CvXMLLoadUtility.cpp"
    "CvXMLLoadUtilityGet.cpp"
    "CvXMLLoadUtilityInit.cpp"
    "CvXMLLoadUtilitySet.cpp"
    "CyArea.cpp"
    "CyAreaInterface.cpp"
    "CyArgsList.cpp"
    "CyArtFileMgr.cpp"
    "CyArtFileMgrInterface.cpp"
    "CyCity.cpp"
    "CyCityInterface1.cpp"
    "CyDeal.cpp"
    "CyEnumsInterface.cpp"
    "CyGame.cpp"
    "CyGameCoreUtils.cpp"
    "CyGameCoreUtilsInterface.cpp"
    "CyGameInterface.cpp"
    "CyGameTextMgr.cpp"
    "CyGameTextMgrInterface.cpp"
    "CyGlobalContext.cpp"
    "CyGlobalContextInterface1.cpp"
    "CyGlobalContextInterface2.cpp"
    "CyGlobalContextInterface3.cpp"
    "CyGlobalContextInterface4.cpp"
    "CyHallOfFameInfo.cpp"
    "CyHallOfFameInterface.cpp"
    "CyInfoInterface1.cpp"
    "CyInfoInterface2.cpp"
    "CyInfoInterface3.cpp"
    "CyMap.cpp"
    "CyMapGenerator.cpp"
    "CyMapGeneratorInterface.cpp"
    "CyMapInterface.cpp"
    "CyMessageControl.cpp"
    "CyMessageControlInterface.cpp"
    "CyPlayer.cpp"
    "CyPlayerInterface1.cpp"
    "CyPlayerInterface2.cpp"
    "CyPlot.cpp"
    "CyPlotInterface1.cpp"
    "CyRandomInterface.cpp"
    "CyReplayInfo.cpp"
    "CySelectionGroup.cpp"
    "CySelectionGroupInterface.cpp"
    "CyStructsInterface1.cpp"
    "CyTeam.cpp"
    "CyTeamInterface.cpp"
    "CyUnit.cpp"
    "CyUnitInterface1.cpp"
    "FAssert.cpp"
    "FDialogTemplate.cpp"
)
source_group("Sources" FILES ${Sources})

set(ALL_FILES
    ${Headers}
    ${Sources}
)

################################################################################
# Depands
################################################################################
set (BOOST_Depends
   "boost_program_options"
   "boost_system"
   "boost_python39"
)

################################################################################
# Target
################################################################################
if (CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
    add_library(

        # create python module
        ${PROJECT_NAME} MODULE ${ALL_FILES}
    )
    set_target_properties(${PROJECT_NAME} PROPERTIES PREFIX "")
elseif(MSVC)
    # To Doo
endif()

################################################################################
# Compile definitions
################################################################################

################################################################################
# Compile and link options
################################################################################
if (CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
    target_link_libraries(
        ${PROJECT_NAME} ${BOOST_Depends} ${PYTHON_LIBRARIES}
    )
elseif(MSVC)
    # To Doo
endif()

