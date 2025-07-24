########################################################################################################################
# @file         state_machine_manager.py
# @brief        This module maintains the state of connected displays and DisplayAdapters which would be utilized to
#               re-enumerated by context.py. When there is a change(unplug/plug/config change),
#               libraries would be updating state by invoking this library.
# @author       Pabolu Chandrakanth , Soorya R
########################################################################################################################
from enum import IntEnum

from Libs.Core.core_base import singleton


##
# @brief        TestPhase enum
# @details      Set current phase of test, currently running (Setup/Test/TearDown).
#               Current test phase is handled in TestEnvironment
class TestPhase(IntEnum):
    SETUP = 0
    TEST = 1
    TEARDOWN = 2


##
# @brief        StateMachine Class
@singleton
class StateMachine:
    ##
    # @brief        Constructor
    def __init__(self):
        self.__init_adapters = False
        self.__adapter_display_change = False
        self.__adapter_state_change = False
        self.__adapter_state_dict = {}
        self.__display_inactive_change = False
        self.__vbt_state_change: dict = {}
        self.__test_phase: int = TestPhase.TEST
        self.__skip_gfx_driver_check: bool = False
        self.__simulation_type: str = ""

    ##
    # @brief        Adapter Initialisation
    # @return       Object
    @property
    def init_adapters(self):
        return self.__init_adapters

    ##
    # @brief        Adapter Display Changes
    # @return       Object
    @property
    def adapter_display_change(self):
        return self.__adapter_display_change

    ##
    # @brief        Adapter State Changes
    # @return       Object
    @property
    def adapter_state_change(self):
        return self.__adapter_state_change

    ##
    # @brief        Adapter State Dictionary
    # @return       Object
    @property
    def adapter_state_dict(self):
        return self.__adapter_state_dict

    ##
    # @brief        Display Inactive Changes
    # @return       Object
    @property
    def display_inactive_change(self):
        return self.__display_inactive_change

    ##
    # @brief        VBT Context Change Getter
    # @return       bool - True if VBT state has changed, False if unchanged
    @property
    def vbt_state_change(self) -> dict:
        return self.__vbt_state_change

    ##
    # @brief        Current Test Phase Getter
    # @return       Object
    @property
    def test_phase(self) -> TestPhase:
        return self.__test_phase

    ##
    # @brief        Current Test Phase Setter
    # @param[in]    value - Current Unittest Phase
    # @return       None
    @test_phase.setter
    def test_phase(self, value: TestPhase) -> None:
        self.__test_phase = value

    ##
    # @brief        Simulation Type Getter
    # @return       str - Returns simulation_type from config.ini
    @property
    def simulation_type(self) -> str:
        return self.__simulation_type

    ##
    # @brief        Simulation Type Setter
    # @param[in]    value - Identified simulation_type
    # @return       None
    @simulation_type.setter
    def simulation_type(self, value: str) -> None:
        self.__simulation_type = value

    ##
    # @brief        Skip Graphics Driver Check Setter
    # @return       bool - Returns True to skip Gfx driver checks, False otherwise
    @property
    def skip_gfx_driver_check(self) -> bool:
        return self.__skip_gfx_driver_check

    ##
    # @brief        Skip Graphics Driver Check Setter
    # @param[in]    state - parameter to skip graphics driver check
    # @return       None
    @skip_gfx_driver_check.setter
    def skip_gfx_driver_check(self, state: bool) -> None:
        self.__skip_gfx_driver_check = state

    ##
    # @brief        Init Adapters Context
    # @return       Object
    def init_adapters_context(self):
        self.__init_adapters = True

    ##
    # @brief        Update Adapter Display Context
    # @return       Object
    def update_adapter_display_context(self):
        self.__adapter_display_change = True

    ##
    # @brief        Update Adapter State in Context
    # @param[in]    gfx_index - Graphics Adapter Index
    # @param[in]    enable - status of Graphics Adapter to be set to
    # @return       Object
    def update_adapter_state_in_context(self, gfx_index, enable):
        self.__adapter_state_change = True
        self.__adapter_state_dict[gfx_index] = enable

    ##
    # @brief        Update Inactive Display in Context
    # @return       Object
    def update_inactive_display_in_context(self):
        self.__display_inactive_change = True

    ##
    # @brief        Update VBT Context Change
    # @param[in]    gfx_index - Graphics Adapter Index
    # @param[in]    state - Set VBT state change. True if VBT state is updated, False if unchanged
    # @return       None
    def update_vbt_state_change(self, gfx_index: str, state: bool) -> None:
        self.__vbt_state_change[gfx_index] = state

    ##
    # @brief        Reset Init Adapters
    # @return       Object
    def reset_init_adapters(self):
        self.__init_adapters = False

    ##
    # @brief        Reset Adapter Display Changes
    # @return       Object
    def reset_adapter_display_change(self):
        self.__adapter_display_change = False
        self.__display_inactive_change = False
        self.__init_adapters = False

    ##
    # @brief        Reset Adapter state Changes
    # @return       Object
    def reset_adapter_state_change(self):
        self.__adapter_state_change = False
        self.__adapter_state_dict = {}

    ##
    # @brief        Reset Display Inactive Changes
    # @return       Object
    def reset_display_inactive_change(self):
        self.__display_inactive_change = False
