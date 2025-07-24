###################################################################################################################
# @file     she_utility.py
# @brief    Python wrapper exposes API's related to SHE Utility DLL
# @author   Reeju Srivastava, Sanehadeep Kaur
########################################################################################################################
import ctypes
import os
from Lib.enum import IntEnum  # @Todo: Override with Built-in python3 enum script path

from Libs.Core import enum
from Libs.Core.core_base import singleton
from Libs.Core import display_power
from Libs.Core.test_env import test_context


##
# @brief Contains display types
class SheDisplayType(IntEnum):
    EDP = 0
    DP_1 = 1
    DP_2 = 2
    DP_3 = 3
    DP_4 = 4
    HDMI_1 = 5
    HDMI_2 = 6
    IO_PORT6 = 7
    IO_PORT9 = 8
    IO_PORT10 = 9
    IO_PORT11 = 10
    IO_PORT12 = 11
    EMULATOR_PORT1 = 12
    EMULATOR_PORT2 = 13
    EMULATOR_PORT3 = 14

##
# @brief Power line status
class PowerLine(IntEnum):
    AC = 11
    DC = 12
    PLUNKNOWN = 255

##
# @brief Lid Switch options
class LidSwitchState(IntEnum):
    CLOSE = 0
    OPEN = 1


##
# @brief    SHE UTILITY Class
@singleton
class SHE_UTILITY(object):

    ##
    # @brief    SHE Utility constructor.
    def __init__(self):
        # Load SHEUtility C library.
        self.sheDLL = None
        self.device_connected = None
        self.port = ctypes.c_int()
        self.com_port = ctypes.c_int()

        # Dictionary for opcode
        self.SHE_display_Type_opcode_dict = {0: [9, 10],
                                             1: [1, 2],
                                             2: [3, 4],
                                             3: [5, 6],
                                             4: [13, 14],
                                             5: [7, 8],
                                             6: [15, 16],
                                             7: [11, 12],
                                             8: [17, 18],
                                             9: [19, 20],
                                             10: [21, 22],
                                             11: [23, 24],
                                             12: [33, 34],
                                             13: [40, 41],
                                             14: [46, 47]
                                             }

    ##
    # @brief        Provide Enum for the Ports which are enabled on that device
    # @param[in]    port - The Port address of Connected Port
    # @return       dict[connected_port] - A dictionary of ports which are enabled in SHE tool
    def emu_port_id(self, port):
        connected_port = str(port)
        dict = {'c_long(0)': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                'c_long(1)': [12, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                'c_long(2)': [12, 13, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                'c_long(3)': [12, 13, 14, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                'c_long(4)': [12, 13, 14, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                'c_long(5)': [12, 13, 14, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                'c_long(6)': [12, 13, 14, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                'c_long(7)': [12, 13, 14, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                'c_long(8)': [12, 13, 14, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                'c_long(9)': [12, 13, 14, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                'c_long(10)': [12, 13, 14, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                'c_long(11)': [12, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                'c_long(12)': [12, 13, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                'c_long(13)': [12, 13, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                'c_long(14)': [14, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                'c_long(15)': [13, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                'c_long(16)': [13, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                'c_long(17)': [13, 14, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                'c_long(18)': [13, 14, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                'c_long(19)': [13, 14, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                'c_long(20)': [13, 14, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                'c_long(21)': [12, 14, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                'c_long(22)': [12, 14, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                'c_long(23)': [12, 14, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                'c_long(24)': [12, 14, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
                }
        return dict[connected_port]

    ##
    # @brief        Initialize method
    # @return       device_connected - The type of SHE Tool Connected and the port it is connected to.
    def intialize(self):

        self.sheDLL = ctypes.cdll.LoadLibrary(os.path.join(test_context.TestContext.bin_store(), 'SHEUtility.dll'))
        prototype = ctypes.PYFUNCTYPE(ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
        func = prototype(('GetSHEDeviceTypeandComPort', self.sheDLL))
        self.device_connected = func(ctypes.byref(self.port), ctypes.byref(self.com_port))
        return self.device_connected

    ##
    # @brief        Get SHE device connection status
    # @return       bool - True or False based on request success
    def get_dll_version(self):
        version = ctypes.c_ulong()
        prototype = ctypes.PYFUNCTYPE(ctypes.c_void_p, ctypes.POINTER(ctypes.c_ulong))
        func = prototype(('GetDLLVersion', self.sheDLL))
        func(ctypes.byref(version))
        return version.value

    ##
    # @brief        Plug  and unplug the display with specified delay for next operation.
    # @param[in]    dispType - SHE_DISPLAY_TYPE enum for connected Display
    # @param[in]    plugState -  True if connected, False for disconnected
    # @param[in]    delay - The delay in ms
    # @return       bool - True or False based on request success
    def hot_plug_unplug(self, dispType, plugState, delay):
        opcode = self.__get_display_type_opcode(dispType, plugState)
        prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.c_int, ctypes.c_int)
        func = prototype(('HotPlugUnplug', self.sheDLL))
        return func(ctypes.byref(self.com_port), opcode, delay)

    ##
    # @brief        Set/Switch power line to AC or DC mode.
    # @param[in]    reqType - POWER_LINE type ENUM. delay in ms
    # @param[in]    delay - The Delay in Switch Power Line
    # @return       bool - True or False based on request success
    def switch_powerline(self, reqType, delay):
        prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.c_int, ctypes.c_int)
        func = prototype(('HotPlugUnplug', self.sheDLL))
        return func(ctypes.byref(self.com_port), reqType, delay)

    ##
    # @brief        Perform Lid switch operation for EDP
    # @param[in]    action - LID_SWITCH_STATE type enum, delay in ms
    # @param[in]    delay - The Delay on lid switch button press
    # @return       bool - True or False based on request success
    def lid_switch_button_press(self, action, delay):
        prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.c_int, ctypes.c_int)
        func = prototype(('HotPlugUnplug', self.sheDLL))
        return func(ctypes.byref(self.com_port), action, delay)

    ##
    # @brief        Perform Lid switch operation for display hibernate and continuous hotplug or unplug
    # @param[in]    lid_switch_state - True if lid is open, False otherwise
    # @param[in]    delay -  The delay in lid_switch
    # @return       bool - True or False based on request success
    def lid_switch(self, lid_switch_state, delay=20):
        prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.c_int, ctypes.c_int,
                                      ctypes.c_int, ctypes.c_bool)
        func = prototype(('DisplayUnplugPLug', self.sheDLL))
        if lid_switch_state == display_power.LidSwitchOption.HIBERNATE:
            return func(ctypes.byref(self.com_port), 9, 10, delay, True)
        else:
            return func(ctypes.byref(self.com_port), 9, 10, delay, False)

    ##
    # @brief        this will generate opcode according to the display type and connection state
    # @param[in]    dispType - SHE_DISPLAY_TYPE enum for connected Display
    # @param[in]    plugState - True if connected, False otherwise
    # @return       int - SHE display type opcode
    def __get_display_type_opcode(self, dispType, plugState):
        if plugState is True:
            return self.SHE_display_Type_opcode_dict[dispType][0]
        else:
            return self.SHE_display_Type_opcode_dict[dispType][1]
