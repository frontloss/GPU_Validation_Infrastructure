########################################################################################################################
# @file         matrox_base.py
# @brief        Base module for Matrox
# @author       akumarv
########################################################################################################################
import sys
import os
import logging
import ctypes
import time
import json

from unittest import TestCase
from Libs.Core import cmd_parser
from Libs.Core import display_utility
from Libs.Core import enum
from Libs.Core import display_essential
from Libs.Core.display_config import display_config
from Libs.Core.display_config import display_config_struct
from Libs.Core import driver_escape
from Libs.Core.test_env.test_context import TestContext
from Libs.Core.wrapper import control_api_wrapper
from Libs.Core.wrapper import control_api_args
from enum import IntEnum

mcd_data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mcd.json')
MAX_SUPPORTED_DISPLAYS = 16

##
# @brief        Exposed enum class for common App actions
class TestAction(IntEnum):
    PLUG = 0
    UNPLUG = 1
    LOCK = 2
    UNLOCK = 3
    OVERRIDE = 4
    REMOVE = 5
    LOCK_AND_OVERRIDE = 6
    READ_EDID = 7
    UNKNOWN_ACTION = 8

##
# @brief - Matrox Base Class
class MatroxBase(TestCase):
    EDID_BLOCK_SIZE = 128
    cmd_line_param = None
    plugged_disp_list = []
    mcd_config_data = {}
    matrox_tags = ["-MCD_CONFIG"]

    ##
    # @brief        Parse command line args for display ports requested
    # @return       None
    @classmethod
    def setUpClass(cls) -> None:
        cls.cmd_line_param = cmd_parser.parse_cmdline(args_list=sys.argv, custom_tags=cls.matrox_tags)
        for key, value in cls.cmd_line_param.items():
            if cmd_parser.display_key_pattern.match(key) is not None:
                if value['connector_port'] is not None:
                    cls.plugged_disp_list.append((key, value))
            if key == "MCD_CONFIG":
                cls.mcd_config_data = cls.get_mcd_args(mcd_config_names=value)
        if len(cls.plugged_disp_list) > 0:
            logging.info("{0} Displays read from command line".format(len(cls.plugged_disp_list)))
            logging.debug("Command line displays : {0}".format(cls.plugged_disp_list))
        else:
            logging.error("Display list from command line is empty")

    ##
    # @brief
    # @return       None
    @classmethod
    def tearDownClass(cls) -> None:
        pass

    ##
    # @brief        API to plug or unplug display
    # @param[in]    gfx - Graphics adapter index string
    # @param[in]    port - eg DP_B , HDMI_B string
    # @param[in]    action to be performed PLUG / UNPLUG
    # @return       None
    def disp_plug_unplug(self, gfx, port, action):
        gfx = gfx.lower()
        panel_index = None

        # Check if any custom edid / dpcd has been requested through command line arguments
        for key, value in self.plugged_disp_list:
            if value['connector_port'] == port and value['gfx_index'].lower() == gfx:
                panel_index = value['panel_index']
                break

        if action == TestAction.PLUG:
            if (True == display_utility.plug(port=port, panelindex=panel_index, gfx_index=gfx)):
                logging.info("INFO : Plug Success")
            else:
                logging.error("ERROR : Plug Failed")
                self.fail()
        elif action == TestAction.UNPLUG:
            if (True == display_utility.unplug(port, gfx_index=gfx)):
                logging.info("INFO : UnPlug Success")
            else:
                logging.error("ERROR : UnPlug Failed")
                self.fail()
        else:
            logging.error("ERROR: Unknown action for display hot plug")

    ##
    # @brief        Verify function for lock display feature
    # @param[in]    gfx - Graphics adapter index
    # @param[in]    port - eg DP_B , HDMI_B
    # @param[in]    case True to verify lock, False to verify unlock
    # @return       Bool
    def verify_lock(self, gfx, port, case):
        out_status = True
        # Locked (= True) display , unplug display, check connection status , expected Status = Plugged
        # Locked (= False) display , unplug display, check connection status , expected Status = Unplugged
        self.disp_plug_unplug(port=port, gfx=gfx, action=TestAction.UNPLUG)
        # Need to give 5 second delay (arbitrary) to allow driver and OS states to record unplug
        time.sleep(5)
        enum_disp = display_config.DisplayConfiguration().get_enumerated_display_info()
        is_display_attached = display_config.is_display_attached(enumerated_displays=enum_disp, connector_port=port, gfx_index=gfx)

        if case is True:
            if is_display_attached:
                logging.info("PASS - Display {0} status is attached even after unplug".format(port))
            else:
                logging.error("FAIL - Display {0} status is removed after unplug".format(port))
                out_status = False

        if case is False:
            # For discrete platforms, for last display unplug, OS API always returns display status as plugged
            # Skip check For tests where only 1 display is used, display count is 1 after unplug, platform is DGPU
            is_dgpu = display_essential.is_discrete_graphics_driver(gfx)
            if enum_disp.Count == 1 and len(self.plugged_disp_list) == 1 and is_dgpu:
                logging.info("WARN - In DGPU, skipping unplug status check for UNLOCK case where OS "
                             "always returns status as plugged for last display")
            else:
                if is_display_attached:
                    logging.error("FAIL - Display {0} status is attached even after unplug".format(port))
                    out_status = False
                else:
                    logging.info("PASS - Display {0} status is removed after unplug".format(port))

        # Plug back the display which was unplugged earlier
        for key, value in self.plugged_disp_list:
            if port == value['connector_port'] and gfx == value['gfx_index']:
                self.disp_plug_unplug(port=value['connector_port'], gfx=value['gfx_index'], action=TestAction.PLUG)

        return out_status

    ##
    # @brief        Verify function for edid override feature
    # @param[in]    gfx - Graphics adapter index
    # @param[in]    port - eg DP_B , HDMI_B
    # @param[in]    case True to verify edid override, False to verify edid remove
    # @return       Bool
    def verify_edid_override(self, gfx, port, case):
        out_status = True
        # Verify EDID override works by comparing edid supplied from test and edid read from driver
        input_edid = self.__get_edid_used_during_plug(gfx=gfx, port=port)
        driver_edid = self.__get_edid_from_driver_escape(gfx=gfx, port=port)

        # WA: driver escape may return larger binary data than actual edid data with zero padding, so trim to input
        # edid length before comparing both data
        input_edid_length = len(input_edid)
        driver_edid = driver_edid[0:input_edid_length]

        logging.info("EDID from test is {0}".format(input_edid))
        logging.info("EDID from driver is {0}".format(driver_edid))

        if case is True:
            status = False
            # Override (= True) display,get EDID from driver, expected to get custom override edid provided through IGCL

            for index in range(len(input_edid)):
                if input_edid[index] != driver_edid[index]:  # any 1 byte is not same , then edid is overridden, todo
                    status = True

            if status:
                logging.info("PASS - EDID override works as expected")
            else:
                logging.error("FAIL - EDID override verification failure")
                out_status = False

        if case is False:
            status = True
            # Override( = False) display,get EDID from driver, expected to get regular EDID used during plug of display

            if len(input_edid) == len(driver_edid):
                for index in range(len(input_edid)):
                    if input_edid[index] != driver_edid[index]:
                        status = False
            else:
                status = False
                logging.error("EDID length mismatch between test and driver")

            if status:
                logging.info("PASS - EDID remove case works as expected")
            else:
                logging.error("FAIL - EDID remove verification failure")
                out_status = False

        return out_status

    ##
    # @brief        To get edid used in command line argument for plug
    # @param[in]    gfx - Graphics adapter index
    # @param[in]    port - eg DP_B , HDMI_B
    # @return       None
    def __get_edid_used_during_plug(self, gfx, port):

        panel_index = None
        edid_file_name = None
        edid_root_folder = None
        edid_data = []

        # Get EDID supplied by test

        for key, value in self.plugged_disp_list:
            if value['connector_port'] == port and value['gfx_index'] == gfx:
                panel_index = value['panel_index']

        # Get the edid file name by parsing panel index data sent in command line args
        input_data = display_utility.get_panel_edid_dpcd_info(port=port, panel_index=panel_index)

        if input_data is None:
            logging.error("EDID read failed to get input data provided by test for {0} on {1}".format(port, gfx))
        else:
            edid_file_name = input_data['edid']

        # input_edid holds the file name of EDID. Now to get the path to EDID files and then read the binary data

        if 'HDMI' in port:
            if os.path.exists(os.path.join(TestContext.panel_input_data(), 'HDMI', edid_file_name)):
                edid_root_folder = 'HDMI'
            else:
                logging.error("EDID File [{0}] not found in HDMI sub-folder of [{1}]".format(edid_file_name,
                                                                                             TestContext.panel_input_data()))
        elif 'DP' in port:
            if os.path.exists(os.path.join(TestContext.panel_input_data(), 'eDP_DPSST', edid_file_name)):
                edid_root_folder = 'eDP_DPSST'
            elif os.path.exists(os.path.join(TestContext.panel_input_data(), 'DP_MST_TILE', edid_file_name)):
                edid_root_folder = 'DP_MST_TILE'
            else:
                logging.error("EDID File [{0}] not found in [eDP_DPSST \ DP_MST_TILE] sub-folder of [{1}]".format(
                    edid_file_name, TestContext.panel_input_data()))

        edid_path = os.path.join(TestContext.panel_input_data(), edid_root_folder, edid_file_name)

        try:
            with open(edid_path.encode(), 'rb') as file:
                edid_byte_stream = file.read()
                for index in range(len(edid_byte_stream)):
                    edid_data.append(edid_byte_stream[index])
        except FileNotFoundError:
            logging.error("EDID file not found")

        logging.debug("Size of edid used during plug is {0}".format(len(edid_data)))
        assert(self.__validate_edid_size(edid_data=edid_data))
        return edid_data

    ##
    # @brief        To get edid from driver using driver escape
    # @param[in]    gfx - Graphics adapter index
    # @param[in]    port - eg DP_B , HDMI_B
    # @return       None
    def __get_edid_from_driver_escape(self, gfx, port):

        display_data = display_config.DisplayConfiguration().get_display_and_adapter_info_ex(port=port, gfx_index=gfx)
        edid_flag, edid_data, _ = driver_escape.get_edid_data(display_data)
        if not edid_flag:
            logging.error(f"Failed to get Driver Escape EDID data for {0} on {1}".format(port, gfx))
            assert edid_flag, "Failed to get EDID data"
        assert edid_data

        logging.debug("Size of edid read from driver escape is {0}".format(len(edid_data)))
        assert (self.__validate_edid_size(edid_data=edid_data))
        return edid_data

    ##
    # @brief        To validate edid size , should be multiple of 128
    # @param[in]    edid_data list / array
    # @return       None
    def __validate_edid_size(self, edid_data):
        if len(edid_data) != 0 and len(edid_data) % self.EDID_BLOCK_SIZE == 0:
            return True
        else:
            logging.error("Provided EDID size {0} is not divisible by 128".format(len(edid_data)))
            return False

    ##
    # @brief        Method which will prepare edid management arguments and call API in wrapper
    # @param[in]    gfx - Graphics adapter index
    # @param[in]    port - eg DP_B , HDMI_B
    # @param[in]    action to be performed LOCK / UNLOCK, OVERRIDE / REMOVE
    # @return       Bool
    def perform_edid_management(self, gfx, port, action):
        display_data = display_config.DisplayConfiguration().get_display_and_adapter_info_ex(port=port, gfx_index=gfx)

        args = control_api_args.ctl_edid_management_args_t()
        args.Size = ctypes.sizeof(args)
        args.Version = 0  # dummy value
        args.OpType = control_api_args.ctl_edid_management_optype_v.MAX.value
        args.EdidType = control_api_args.ctl_edid_type_v.EDID_TYPE_CURRENT.value
        args.EdidSize = 0
        args.pEdidBuf = 0

        if action == TestAction.LOCK:
            args.OpType = control_api_args.ctl_edid_management_optype_v.LOCK_EDID.value
            args.EdidType = control_api_args.ctl_edid_type_v.EDID_TYPE_MONITOR.value

        if action == TestAction.UNLOCK:
            args.OpType = control_api_args.ctl_edid_management_optype_v.UNLOCK_EDID.value
            args.EdidType = control_api_args.ctl_edid_type_v.EDID_TYPE_MONITOR.value

        if action == TestAction.OVERRIDE:
            # EDID override buffer and size will be updated in DLL
            args.OpType = control_api_args.ctl_edid_management_optype_v.OVERRIDE_EDID.value
            args.EdidType = control_api_args.ctl_edid_type_v.EDID_TYPE_OVERRIDE.value

        if action == TestAction.REMOVE:
            args.OpType = control_api_args.ctl_edid_management_optype_v.REMOVE_EDID.value
            args.EdidType = control_api_args.ctl_edid_type_v.EDID_TYPE_MONITOR.value

        if action == TestAction.LOCK_AND_OVERRIDE:
            args.OpType = control_api_args.ctl_edid_management_optype_v.LOCK_EDID.value
            args.EdidType = control_api_args.ctl_edid_type_v.EDID_TYPE_OVERRIDE.value

        if action == TestAction.READ_EDID:
            args.OpType = control_api_args.ctl_edid_management_optype_v.READ_EDID.value
            args.EdidType = control_api_args.ctl_edid_type_v.EDID_TYPE_CURRENT.value

        status, out_args = control_api_wrapper.edid_mgmt(edid_mgmt_args=args, display_and_adapter_info=display_data)

        # Todo output arg not passing from C dll to python layer, need to check this later, to enhance verification
        output = out_args.value
        logging.info("Output : {0}".format(hex(output)))

        if status is True:
            logging.info("PASS: EDID mgmt called for action {0} on port {1}".format(TestAction(action).name, port))
            return True
        else:
            logging.error("FAIL: EDID mgmt called for action {0} on port {1}".format(TestAction(action).name, port))
            return False

    ##
    # @brief        Method which will prepare edid management arguments and call API in wrapper for unplugged displays
    # @param[in]    display_data of type DisplayAndAdaptorInfo
    # @param[in]    port - eg DP_B , HDMI_B
    # @param[in]    action to be performed PLUG / UNPLUG
    # @return       Bool
    def perform_edid_management_unplugged_display(self, display_data, port, action):
        # Just supporting this method for lock / unlock and override / remove operations for removed/ unplugged displays
        # In this case display_data cannot be fetched from get_enumerate_displays, so caller has to send it
        args = control_api_args.ctl_edid_management_args_t()
        args.Size = ctypes.sizeof(args)
        args.Version = 0  # dummy value
        args.OpType = control_api_args.ctl_edid_management_optype_v.MAX.value
        args.EdidType = control_api_args.ctl_edid_type_v.EDID_TYPE_CURRENT.value
        args.EdidSize = 0
        args.pEdidBuf = 0

        if action == TestAction.LOCK:
            args.OpType = control_api_args.ctl_edid_management_optype_v.LOCK_EDID.value
            args.EdidType = control_api_args.ctl_edid_type_v.EDID_TYPE_MONITOR.value

        if action == TestAction.UNLOCK:
            args.OpType = control_api_args.ctl_edid_management_optype_v.UNLOCK_EDID.value
            args.EdidType = control_api_args.ctl_edid_type_v.EDID_TYPE_MONITOR.value

        if action == TestAction.OVERRIDE:
            # EDID override buffer and size will be updated in DLL
            args.OpType = control_api_args.ctl_edid_management_optype_v.OVERRIDE_EDID.value
            args.EdidType = control_api_args.ctl_edid_type_v.EDID_TYPE_OVERRIDE.value

        if action == TestAction.REMOVE:
            args.OpType = control_api_args.ctl_edid_management_optype_v.REMOVE_EDID.value
            args.EdidType = control_api_args.ctl_edid_type_v.EDID_TYPE_MONITOR.value

        status, out_args = control_api_wrapper.edid_mgmt(edid_mgmt_args=args, display_and_adapter_info=display_data)

        # Todo output arg not passing from C dll to python layer, need to check this later, to enhance verification
        output = out_args.value
        logging.info("Output : {0}".format(hex(output)))

        if status is True:
            logging.info("PASS: EDID mgmt called for action {0} on port {1}".format(TestAction(action).name, port))
            return True
        else:
            logging.error("FAIL: EDID mgmt called for action {0} on port {1}".format(TestAction(action).name, port))
            return False

    ##
    # @brief        To set all connected displays in extended and make them active
    # @return       None
    def enable_plugged_disp(self):
        display_adapter_list = []
        enumerated_displays = display_config.DisplayConfiguration().get_enumerated_display_info()
        for index in range(enumerated_displays.Count):
            display_adaptor_info = enumerated_displays.ConnectedDisplays[index].DisplayAndAdapterInfo
            target_id = display_config_struct.TARGET_ID(Value= enumerated_displays.ConnectedDisplays[index].TargetID)
            if not target_id.InternalDisplay:
                display_adapter_list.append(display_adaptor_info)

        if display_config.DisplayConfiguration().set_display_configuration_ex(enum.EXTENDED, display_adapter_list) is False:
            logging.error("FAIL: Unable to apply extended config on all plugged displays")
            self.fail()
        else:
            logging.info("PASS: Applied extended config on all plugged displays")

    ##
    # @brief        To set all connected displays in extended and make them active
    # @param[in]    mcd_args
    # @param[in]    adaptor_info_list is a list containing DisplayAndAdapterInfo objects
    # @return       Bool
    def perform_get_set_combined_display(self, mcd_args=None, adaptor_info_list=None):
        status = True

        args = control_api_args.ctl_combined_display_args_t()
        args.Size = ctypes.sizeof(args)
        args.Version = 0  # dummy value
        args.OpType = control_api_args.ctl_combined_display_optype_v.CTL_COMBINED_DISPLAY_OPTYPE_MAX.value
        optype_list = mcd_args["OpType"]  # if more than 1 optype , then need to do multiple combined display ops

        args.IsSupported = 0
        args.NumOutputs = mcd_args["NumOutputs"]
        args.CombinedDesktopWidth = mcd_args["CombinedDesktopWidth"]
        args.CombinedDesktopHeight = mcd_args["CombinedDesktopHeight"]
        child_info_buffer_type = control_api_args.ctl_combined_display_child_info_t * args.NumOutputs
        child_info_buffer = child_info_buffer_type()
        child_info_input_list = mcd_args["child_info_list"]

        index = 0
        for child_info in child_info_input_list:
            child_info_buffer[index].FbSrc.Left = child_info["FbSrc"][0]
            child_info_buffer[index].FbSrc.Top = child_info["FbSrc"][1]
            child_info_buffer[index].FbSrc.Right = child_info["FbSrc"][2]
            child_info_buffer[index].FbSrc.Bottom = child_info["FbSrc"][3]
            child_info_buffer[index].FbPos.Left = child_info["FbPos"][0]
            child_info_buffer[index].FbPos.Top = child_info["FbPos"][1]
            child_info_buffer[index].FbPos.Right = child_info["FbPos"][2]
            child_info_buffer[index].FbPos.Bottom = child_info["FbPos"][3]
            child_info_buffer[index].DisplayOrientation = child_info["DisplayOrientation"]
            child_info_buffer[index].TargetMode.Width = child_info["TargetMode"][0]
            child_info_buffer[index].TargetMode.Height = child_info["TargetMode"][1]
            child_info_buffer[index].TargetMode.RefreshRate = child_info["TargetMode"][2]
            index = index + 1
            logging.info("FbSrc: ({0},{1},{2},{3}), FbPos: ({4},{5},{6},{7}), Orient: {8},"
                          " WidthxHeightxRR: {9}x{10}x{11}".format(child_info["FbSrc"][0],
                                                                   child_info["FbSrc"][1],
                                                                   child_info["FbSrc"][2],
                                                                   child_info["FbSrc"][3],
                                                                   child_info["FbPos"][0],
                                                                   child_info["FbPos"][1],
                                                                   child_info["FbPos"][2],
                                                                   child_info["FbPos"][3],
                                                                   child_info["DisplayOrientation"],
                                                                   child_info["TargetMode"][0],
                                                                   child_info["TargetMode"][1],
                                                                   child_info["TargetMode"][2]))
        args.pChildInfo = child_info_buffer

        display_adaptor_buffer = display_config_struct.MultiDisplayAndAdapterInfo()

        buffer_index = 0

        for key, value in self.plugged_disp_list:
            if adaptor_info_list is None:
                display_adaptor_info = display_config.DisplayConfiguration().get_display_and_adapter_info_ex(port=value['connector_port'], gfx_index=value['gfx_index'])
                display_adaptor_buffer.displayAndAdapterInfo[buffer_index] = display_adaptor_info
            else:
                display_adaptor_buffer.displayAndAdapterInfo[buffer_index] = adaptor_info_list[buffer_index]
            logging.info("Display Selected for Combined display: {}".format(key))
            logging.debug("Details of selected display: {} {}".format(key, value))
            buffer_index = buffer_index + 1

        logging.info("buffer index = {}".format(buffer_index))

        if buffer_index != args.NumOutputs:
            logging.error("ERROR: Display count mismatch between command line and MCD config file")

        display_adaptor_buffer.Count = buffer_index

        for optype in optype_list:
            args.OpType = optype
            logging.debug("OpType: {} Optype_List: {}".format(optype, optype_list))
            status = control_api_wrapper.get_set_combined_display(combined_display_args=args,
                                                                  display_adaptor_buffer=display_adaptor_buffer)
            if status is True:
                logging.info("PASS: Combined display passed for Optype {}".format(optype))
            else:
                logging.error("FAIL: Combined display failed for Optype {}".format(optype))

        return status

    ##
    # @brief        To get MCD arguments from JSON file for a given config
    # @param[in]    mcd_config_names - list of config names from command line that maps to mcd.json
    # @return       output dictionary with key as config name and value as config data extracted from JSON
    @classmethod
    def get_mcd_args(cls, mcd_config_names : list):
        mcd_dict = {}  # type: dict
        output = {}

        try:
            logging.debug('MCD Data Path: {}'.format(mcd_data_path))
            with open(mcd_data_path) as mcd_file:
                mcd_dict = json.load(mcd_file)  # convert all MCD configs in JSON to a dictionary
                logging.debug("MCD file: {}".format(mcd_file))
                logging.debug("MCD_dictionary: {}".format(mcd_dict))
        except EnvironmentError as error:
            logging.error(error.strerror)

        # from the MCD configs , identify the required one, key is config name (as provided in command line)
        # value is a dictionary of mcd args
        for key, value in mcd_dict.items():
            logging.debug("key: {}".format(key))
            logging.debug("value: {}".format(value))
            if key in mcd_config_names:
                logging.info("MCD_CONFIG match: {}".format(key))
                output[key] = value

        return output

    ##
    # @brief        Check if genlock testing is required based on command line arguments and setup
    # @return       None
    def is_genlock_combined_display_config(self):
        if len(self.mcd_config_data) != 2:
            logging.info("2 MCD configs required for this test")
            return False
        if 'GENLOCK' not in next(iter(self.mcd_config_data)):
            logging.info("MCD config name in command line and mcd.json should contain GENLOCK")
            return False
        is_dgpu = display_essential.is_discrete_graphics_driver(gfx_index='gfx_0')
        if not is_dgpu:
            logging.info("Not DGPU case")
            return False
        return True