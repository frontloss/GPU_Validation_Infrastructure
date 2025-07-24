#######################################################################################################################
# @file         workload_context.py
# @brief        Contains object definitions used in workload.py module
#
# @author       Ashish Tripathi, Rohit Kumar
#######################################################################################################################
import os

from enum import IntEnum

from Libs.Core.test_env import test_context

GAME_STATE = os.path.join(test_context.ROOT_FOLDER, "game_state.pickle")
VRR_BIN_FOLDER = os.path.join(test_context.TEST_SPECIFIC_BIN_FOLDER, "VRR")
ANGRY_BOTS_FOLDER = os.path.join(test_context.SHARED_BINARY_FOLDER, "AngryBots")


##
# @brief        Exposed object class for all VRR apps
class Apps:
    MovingRectangleApp = "MovingRectangleApp.exe"
    AngryBotsGame = "AngryBotsGame.exe"
    Classic3DCubeApp = "Classic3DCubeApp.exe"


##
# @brief        Exposed object class for workloads
class Workload:
    IDLE_DESKTOP = "IDLE_DESKTOP"
    SCREEN_UPDATE = "SCREEN_UPDATE"
    GAME_PLAYBACK = "GAME_PLAYBACK"
    VIDEO_PLAYBACK = "VIDEO_PLAYBACK"
    VIDEO_PLAYBACK_WITH_MOUSE_MOVE = "VIDEO_PLAYBACK_WITH_MOUSE_MOVE"


##
# @brief        Exposed enum class for common App actions
class AppActions(IntEnum):
    OPEN = 0
    CLOSE = 1
    ENABLE_FULL_SCREEN = 2
    DISABLE_FULL_SCREEN = 3
    FORCE_FULL_SCREEN = 4
    INCREASE_SPEED = 5
    DECREASE_SPEED = 6
    INCREASE_FPS = 7
    DECREASE_FPS = 8
    ENABLE_VSYNC = 9
    DISABLE_VSYNC = 10
    APP_ACTION_MAX = 11


##
# @brief        Exposed enum class for AngryBots graphics settings
class AngryBotsGraphicsSettings(IntEnum):
    FASTEST = 0
    FAST = 1
    SIMPLE = 2
    GOOD = 3
    BEAUTIFUL = 4
    FANTASTIC = 5


##
# @brief        Exposed enum class for AngryBots actions
class AngryBotsActions(IntEnum):
    MOVE_UP = 0
    MOVE_DOWN = 1
    MOVE_RIGHT = 2
    MOVE_LEFT = 3
    ACTION_MAX = 4


##
# @brief        Exposed enum class for Presentation model
class PresentationModel(IntEnum):
    DXGI_SWAP_EFFECT_DISCARD = 0
    DXGI_SWAP_EFFECT_SEQUENTIAL = 1
    DXGI_SWAP_EFFECT_FLIP_SEQUENTIAL = 3


##
# @brief        Helper object class for all VRR app window titles. These titles are used to search for the app window
#               and make it active.
class AppWindowTitles:
    MovingRectangleApp = "D3D12 Fullscreen sample"
    AngryBotsGameConfiguration = "AngryBots Configuration"
    AngryBotsGame = "AngryBots"
    Classic3DCubeApp = "ClassicD3D: Window"


##
# @brief        Helper object class for all the 3D cube app configuration parameters
class Classic3DCubeAppConfig:
    adapter = 0
    gdi_compatible = False  # Render a string GDI text that blends with D3D content
    gpu_priority = 0  # Set a scheduling priority for the application D3D device
    interval = 0  # Sets present interval
    buffers = 2  # Sets number of buffers in the swap chain
    presentation_model = PresentationModel.DXGI_SWAP_EFFECT_FLIP_SEQUENTIAL
    dcomp = False  # Use DComp (Direct Composition Technology) composition and effects
    rotation_speed = 1
    object_y_position = None
    window_count = 1
    test_display_mode_change = False
    test_window_device_destruction = False
    test_full_screen = False
