#######################################################################################################################
# @file         interface_context.py
# @brief        Contains object definitions used in interface.py module
#
# @author       Ashish Tripathi, Rohit Kumar
#######################################################################################################################
from Libs.Core import enum

from enum import Enum, IntEnum

DEFAULT_DURATION_IN_SEC = 30


##
# @brief        Exposed object class for all VRR apps
class Apps:
    MovingRectangleApp = "MovingRectangleApp.exe"
    AngryBotsGame = "AngryBotsGame.exe"
    Classic3DCubeApp = "Classic3DCubeApp.exe"


##
# @brief        Exposed enum class for return status
class ReturnStatus(IntEnum):
    SUCCESS = 0


##
# @brief        Exposed enum class for power line status
class PowerLineStatus(IntEnum):
    POWER_LINE_DC = 1
    POWER_LINE_AC = 0


##
# @brief        Exposed object class for power events
class PowerEvent:
    S3 = "SLEEP"
    S4 = "HIBERNATE"
    CS = "CONNECTED_STANDBY"


##
# @brief        Exposed object class for different scenarios
class Scenario:
    IDLE_DESKTOP = "IDLE_DESKTOP"
    SCREEN_UPDATE = "SCREEN_UPDATE"
    FEATURE_TOGGLE = "FEATURE_TOGGLE"
    POWER_EVENT_S3 = "POWER_EVENT_S3"
    POWER_EVENT_S4 = "POWER_EVENT_S4"
    POWER_EVENT_CS = "POWER_EVENT_CS"
    POWER_SOURCE_AC = "POWER_SOURCE_AC"
    POWER_SOURCE_DC = "POWER_SOURCE_DC"
    GAME_PLAYBACK = "GAME_PLAYBACK"
    VIDEO_PLAYBACK = "VIDEO_PLAYBACK"
    VIDEO_PLAYBACK_WITH_MOUSE_MOVE = "VIDEO_PLAYBACK_WITH_MOUSE_MOVE"


##
# @brief        Exposed object class for different status
class Status:
    TRUE = "TRUE"
    FALSE = "FALSE"


##
# @brief        Exposed object class for various triage events
class TriageEvents:
    GAME_PLAYBACK = "GAME_PLAYBACK"
    VIDEO_PLAYBACK = "VIDEO_PLAYBACK"
    IDLE_DESKTOP = "IDLE_DESKTOP"
    SCREEN_UPDATE = "SCREEN_UPDATE"
    ENABLE_DISPLAY_FEATURE = "ENABLE_DISPLAY_FEATURE"
    DISABLE_DISPLAY_FEATURE = "DISABLE_DISPLAY_FEATURE"
    SET_POWER_SOURCE = "SET_POWER_SOURCE"
    INVOKE_POWER_EVENT = "INVOKE_POWER_EVENT"
    REPEAT = "REPEAT"
    HOT_PLUG = "HOT_PLUG"
    UNPLUG = "UNPLUG"
    SET_DISPLAY_CONFIG = "SET_DISPLAY_CONFIG"
    DRIVER_RESTART = "DRIVER_RESTART"


##
# @brief        Exposed enum class for Psr version
class PsrVersion(IntEnum):
    PSR_1 = 1
    PSR_2 = 2
    PSR2_FFSU = 3
    PSR2_SFSU = 4


##
# @brief        Exposed enum class for different lrr version
class LrrVersion(Enum):
    LRR1 = 1
    LRR2 = 2
    LRR2_5 = 2.5


##
# @brief        Exposed object class for requested feature reg key
class RequestedFeature:
    DRRS_REG_KEY = "DRRS_REG_KEY"
    DMRRS_REG_KEY = "DMRRS_REG_KEY"
    FBC_REG_KEY = "FBC_REG_KEY"
    LRR_REG_KEY = "LRR_REG_KEY"
    PSR1_REG_KEY = "PSR1_REG_KEY"
    PSR2_REG_KEY = "PSR2_REG_KEY"
    PSR2_FFSU_REG_KEY = "PSR2_FFSU_REG_KEY"
    PSR2_SFSU_REG_KEY = "PSR2_SFSU_REG_KEY"
    VRR_ESCAPE_CALL = "VRR_ESCAPE_CALL"
    CFPS_ESCAPE_CALL = "CFPS_ESCAPE_CALL"


##
# @brief        Exposed object class for registries based on platforms
class Registry:
    DISPLAY_PC_FEATURE_CONTROL = "DisplayPcFeatureControl"
    DISPLAY_FEATURE_CONTROL = "DisplayFeatureControl"
    FEATURE_TEST_CONTROL = "FeatureTestControl"
    PSR2_DRRS_ENABLE = "Psr2DrrsEnable"
    PSR2_DISABLE = "PSR2Disable"
    # below data collected from igdlh64.inf
    SKU_DEFAULT = {
        'ICLLP': {
            DISPLAY_PC_FEATURE_CONTROL: 0x30000,
            DISPLAY_FEATURE_CONTROL: 0x3E7,
            FEATURE_TEST_CONTROL: 0x200,
            PSR2_DRRS_ENABLE: 0x1,
            PSR2_DISABLE: 0x0
        },
        'LKF': {
            DISPLAY_PC_FEATURE_CONTROL: 0x30000,
            DISPLAY_FEATURE_CONTROL: 0x3E7,
            FEATURE_TEST_CONTROL: 0x200,
        },
        'RYF': {
            DISPLAY_PC_FEATURE_CONTROL: 0x20000,
            FEATURE_TEST_CONTROL: 0xB373,
        },
        'EHL': {
            DISPLAY_PC_FEATURE_CONTROL: 0x30000,
            DISPLAY_FEATURE_CONTROL: 0x3E7,
            FEATURE_TEST_CONTROL: 0x200,
            PSR2_DRRS_ENABLE: 0x1,
            PSR2_DISABLE: 0x0
        },
        'JSL': {
            DISPLAY_PC_FEATURE_CONTROL: 0x30000,
            DISPLAY_FEATURE_CONTROL: 0x3E7,
            FEATURE_TEST_CONTROL: 0x200,
            PSR2_DRRS_ENABLE: 0x1,
            PSR2_DISABLE: 0x0
        },
        'TGL': {
            DISPLAY_PC_FEATURE_CONTROL: 0x21000,
            DISPLAY_FEATURE_CONTROL: 0x3E7,
            FEATURE_TEST_CONTROL: 0x1200,
            PSR2_DRRS_ENABLE: 0x1,
            PSR2_DISABLE: 0x0
        },
        'RKL': {
            DISPLAY_PC_FEATURE_CONTROL: 0x21000,
            DISPLAY_FEATURE_CONTROL: 0x3E7,
            FEATURE_TEST_CONTROL: 0x1200,
            PSR2_DRRS_ENABLE: 0x1,
            PSR2_DISABLE: 0x0
        },
        'ADLS': {
            DISPLAY_PC_FEATURE_CONTROL: 0x21000,
            DISPLAY_FEATURE_CONTROL: 0x3E7,
            FEATURE_TEST_CONTROL: 0x1200,
            PSR2_DRRS_ENABLE: 0x1,
            PSR2_DISABLE: 0x0
        },
        'ADLP': {
            DISPLAY_PC_FEATURE_CONTROL: 0x61000,
            DISPLAY_FEATURE_CONTROL: 0x3E7,
        }
    }
