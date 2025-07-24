##
# @file nnis_scaling_base.py
# @brief The script implements unittest default functions for setUp and tearDown, and common test functions given below:
# @details * process_cmdline: To parse the command line and get the input data
#          * parse_xml_and_plug: To parse the XML file for EDID and DPCD and mode to apply
#          * plug_display: To Plug EDID and DPCD for input display
#          * apply_mode_and_verify_scaling: To Apply a particular mode and checks whether scaling is applied or not
#          * Verify different scaling register
# @author Nainesh Doriwala
import ctypes
import logging
import os
import platform
import sys
import time
import unittest
import xml.etree.ElementTree as ET

from Libs.Core import cmd_parser, registry_access, display_essential, etl_parser
from Libs.Core import display_utility
from Libs.Core import driver_escape
from Libs.Core import enum
from Libs.Core import reboot_helper
from Libs.Core import system_utility as sys_util
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE
from Libs.Core.display_config.display_config_struct import DisplayMode
from Libs.Core.display_power import DisplayPower
from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Core.machine_info import machine_info
from Libs.Core.test_env import test_context
from Libs.Core.wrapper import control_api_wrapper, control_api_args
from Libs.Core.wrapper.driver_escape_args import NNArgs, ScalingOperation, NNScalingState, CustomModeArgs
from Libs.Feature.display_engine.de_base import display_scalar
from Libs.Feature.display_port.dpcd_helper import GetConnectorPort
from Tests.Planes.Common import planes_verification
from registers.mmioregister import MMIORegister
from Libs.Core.logger import gdhm, etl_tracer

scalar_coff = 0


##
# @brief It contains methods to setUp and tearDown methods of unittest framework and different verify function
class ScalingBase(unittest.TestCase):
    disp_count = 0
    xml_file = dispConfig = scalar = scaling = None
    is_integer_scaling = False
    virtual_mode_set_aware = False
    display_list = []
    os_mode_list = []
    scalar_config_dict = {}
    platform = None
    display_config = DisplayConfiguration()
    system_utility = sys_util.SystemUtility()
    machine_info = SystemInfo()
    nn_args = NNArgs()
    display_power = DisplayPower()
    is_teardown_required = False
    ss_reg_args = registry_access.StateSeparationRegArgs(gfx_index='gfx_0')
    SCALE_DICT = {'Unsupported': 0, 'CI': 1, 'FS': 2, 'MAR': 4, 'CAR': 8, 'MDS': 64}
    RSCALE_DICT = {0: 'Unsupported', 1: 'CI', 2: 'FS', 4: 'MAR', 8: 'CAR', 64: 'MDS'}
    RROTATION_DICT = {1: '0Deg', 2: '90Deg', 3: '180Deg', 4: '270Deg'}
    SCANLINE_DICT = {'Progressive': 1, 'Interlaced': 2}
    targetid = None

    ##
    # @brief Unit-test setup function
    # @return None
    @reboot_helper.__(reboot_helper.setup)
    def setUp(self):
        enum_value = None
        val = None
        logging.info(" TEST START ".center(64, "*"))
        gfx_display_hwinfo = self.machine_info.get_gfx_display_hardwareinfo()

        self.platform = gfx_display_hwinfo[0].DisplayAdapterName

        # parse command lines
        self.process_cmdline()
        logging.info(" Setup Completed ".center(64, "*"))

    ##
    # @brief Check and add NNScalingState registry and reset display driver.
    # @return - bool - status True if able to update regkey else False
    #           Bool - reboot_required  True if reboot require else False
    def check_and_add_nnis_scaling_registry(self):

        # parse XML ,plug display and add mode info for enumerate display
        self.parse_xml_and_plug()

        enumerated_displays = self.display_config.get_enumerated_display_info()
        logging.debug("config {}display {}".format(self.dispConfig, self.display_list))
        # Apply display configuration for self.display_list
        if not self.display_config.set_display_configuration_ex(self.dispConfig, self.display_list,
                                                                enumerated_displays):
            logging.error("Set Display Configuration failed")
            self.fail()

        ##
        # Add NNScalingState register to enable feature, as it is not enable by default untill IGCC install
        val, reg_type = registry_access.read(args=self.ss_reg_args, reg_name="NNScalingState")
        if val is None:
            if registry_access.write(args=self.ss_reg_args, reg_name="NNScalingState",
                                     reg_type=registry_access.RegDataType.BINARY,
                                     reg_value=bytes([0x00, 0x00, 0x00, 0x00])) is False:
                gdhm.report_bug(
                    title="[NN/IS] Failed to add regkey to enable NN/IS scaling",
                    problem_classification=gdhm.ProblemClassification.LOG_FAILURE,
                    component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                logging.error("Registry key add to enable NN/IS scaling feature failed")
                self.fail("Registry key add to enable NN/IS scaling feature failed")

            # Disable enable driver to effect register in driver.
            status, reboot_required = display_essential.restart_gfx_driver()

            logging.info("sleep for 5 sec")
            time.sleep(5)
        else:
            logging.debug("NNScalingState register already available, gfx driver restart not require.")
            status = True,
            reboot_required = True
        return status, reboot_required

    ##
    # @brief Process input command line and custom tags supported ('-xml','-scalar','-scaling_type')
    # @return - None
    def process_cmdline(self):
        # Parse the command line arguments
        self.my_custom_tags = ['-xml', '-scalar', '-scaling_type']
        self.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, self.my_custom_tags)

        for key, value in self.cmd_line_param.items():
            if cmd_parser.display_key_pattern.match(key) is not None:
                if value['connector_port'] is not None:
                    if not (self.display_list.__contains__(value['connector_port'])):
                        self.display_list.append(value['connector_port'])
                else:
                    gdhm.report_bug(
                        title="[NN/IS] Failed - Displays are not passed in command line ",
                        problem_classification=gdhm.ProblemClassification.LOG_FAILURE,
                        component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )
                    self.fail("Aborting the test as displays are not passed in the command line")
                logging.info("key:%s\t value :%s" % (key, value))

        self.disp_count = len(self.display_list)
        logging.info("number of display connected: %s" % self.disp_count)

        if self.cmd_line_param['XML'] != 'NONE':
            logging.info("display plug required :%s" % self.cmd_line_param['XML'][0])
            self.xml_file = self.cmd_line_param['XML'][0]
        else:
            logging.info("No display plug, As no xml file in command line")

        if self.cmd_line_param['SCALAR'] == 'NONE':
            self.fail("aborting the test as scalar is not provided in command-line - Opt Pipe or plane")
        self.scalar = self.cmd_line_param['SCALAR'][0]
        if self.scalar == 'PLANE':
            self.virtual_mode_set_aware = True

        if self.cmd_line_param['SCALING_TYPE'] == 'NONE':
            self.fail("aborting the test as scaling is not provided in command-line- opt NN or IS")
        self.scaling = self.cmd_line_param['SCALING_TYPE'][0]
        if self.scaling == 'IS':
            self.is_integer_scaling = True

        self.dispConfig = eval('enum.%s' % self.cmd_line_param['CONFIG'])

    ##
    # @brief Parse the XML file for EDID and DPCD and the mode to apply
    # @return - None
    def parse_xml_and_plug(self):
        sup_platform = []
        tree = ET.parse(self.xml_file)
        target_id = None
        Platform = tree.getroot()
        for plat_temp in Platform:
            if plat_temp.tag == "Platform" and self.platform == plat_temp.get('Name'):
                sup_platform.append(plat_temp.get('Name'))
                # Fetch the EDID/DPCD from XML and fetch the scalar mode to be applied, copy to self.scalar_config_dict
                for index in range(0, len(self.display_list)):
                    display_node = plat_temp.find('GoldenDisplayConfig')

                    for displayConfig in display_node:
                        logging.info("{}, {}".format(self.display_list[index], displayConfig.get('Port')))
                        if self.display_list[index] == displayConfig.get('Port'):
                            modes_list = []
                            edid = displayConfig.get('edid')
                            dpcd = displayConfig.get('dpcd')
                            logging.info("display:{}".format(self.display_list[index]))
                            if display_utility.get_vbt_panel_type(self.display_list[index], 'gfx_0') not in \
                                    [display_utility.VbtPanelType.LFP_DP, display_utility.VbtPanelType.LFP_MIPI]:
                                target_id = self.plug_display(self.display_list[index], edid, dpcd)
                            else:
                                enumerated_displays = self.display_config.get_enumerated_display_info()
                                # Get Target-ID for connected port
                                for display_index in range(enumerated_displays.Count):
                                    enum_port = (
                                        CONNECTOR_PORT_TYPE(
                                            enumerated_displays.ConnectedDisplays[
                                                display_index].ConnectorNPortType)).name
                                    if display_utility.get_vbt_panel_type(enum_port, 'gfx_0') in \
                                            [display_utility.VbtPanelType.LFP_DP, display_utility.VbtPanelType.LFP_MIPI]:
                                        target_id = enumerated_displays.ConnectedDisplays[display_index].TargetID
                                        logging.info("DP_A/MIPI_A target ID:{}".format(target_id))
                                        break

                            display = self.display_list[index].split("_")
                            mode_list = plat_temp.find(display[0] + "ScalarModes")
                            for modeInstance in mode_list:
                                if modeInstance.tag == "EDIDInstance":
                                    mode = DisplayMode()
                                    mode.targetId = target_id
                                    mode.HzRes = int(modeInstance.get('HActive'))
                                    mode.VtRes = int(modeInstance.get('VActive'))
                                    mode.refreshRate = int(modeInstance.get('RefreshRate'))
                                    mode.BPP = 4  # Assuming RGB888
                                    mode.rotation = 1
                                    mode.scanlineOrdering = 1
                                    mode.scaling = self.SCALE_DICT[modeInstance.get('Scaling')]
                                    modes_list.append(mode)
                                    logging.debug("{},Added mode {} X {}".format(self.display_list[index], mode.HzRes,
                                                                                 mode.VtRes))

                            self.scalar_config_dict[self.display_list[index]] = modes_list
                            break

        # If platform supported is not part of XML file, fail the test
        if self.platform not in sup_platform:
            gdhm.report_bug(
                title="[NN/IS] {0} Platform not enable in XML ".format(self.platform),
                problem_classification=gdhm.ProblemClassification.LOG_FAILURE,
                component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.error(
                "ERROR : XML file : %s specified is not valid for the %s platform" % (self.xml_file, self.platform))
            self.fail()

    ##
    # @brief Plug EDID and DPCD for input display
    # @param[in] port - Port on which display to plug
    # @param[in] edid_file - file that contains data about edid
    # @param[in] dpcd_file - file that contains data about dpcd
    # @return targetId - targeID value of the connected port
    def plug_display(self, port, edid_file, dpcd_file):
        targetId = None
        logging.info("INFO : Plug %s with EDID : %s DPCD : %s" % (port, edid_file, dpcd_file))
        if dpcd_file == "None":
            display_utility.plug(port, edid_file)
        else:
            display_utility.plug(port, edid_file, dpcd_file)

        enumerated_displays = self.display_config.get_enumerated_display_info()
        # Get Target-ID for connected port
        for display_index in range(enumerated_displays.Count):
            enum_port = (
                CONNECTOR_PORT_TYPE(
                    enumerated_displays.ConnectedDisplays[display_index].ConnectorNPortType)).name
            if enum_port == port:
                targetId = enumerated_displays.ConnectedDisplays[display_index].TargetID
        logging.info("INFO : Target-id for %s - %s" % (port, targetId))
        if targetId is None:
            gdhm.report_bug(
                title="[NN/IS] Display not found in connected display list",
                problem_classification=gdhm.ProblemClassification.LOG_FAILURE,
                component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.error("FAIL : No target-id found for %s. Check if display is connected" % port)
            self.fail()

        return targetId

    ##
    # @brief Check plane scalar status
    # @param[in] key - display_adapter_info or target id
    # @param[in] mode_list - list that contains the mode
    # @param[in] duration - Times to loop
    # @return status-boolean value true or false
    def check_plane_scalar_status(self, key, mode_list, duration):
        scalar_list = []
        for mode in mode_list:
            port = GetConnectorPort(key)
            scaling = self.RSCALE_DICT[mode.scaling]
            scalar_list.append(display_scalar.DisplayScalar(port, scaling))
        for scalarObj in scalar_list:
            pipe = scalarObj.pipe.split("PIPE_")
            PLATFORM = scalarObj.platform
            for i in range(1, 3):
                scalar_reg = MMIORegister.read("PS_CTRL_REGISTER", "PS_CTRL_%s_%s" % (i, pipe[1]), PLATFORM)
                if (scalar_reg.enable_scaler and (
                        scalar_reg.scaler_binding != 0) and self.virtual_mode_set_aware):
                    return True
                elif not scalar_reg.enable_scaler:
                    for dur in range(duration):
                        time.sleep(5)
                        scalar_reg = MMIORegister.read("PS_CTRL_REGISTER", "PS_CTRL_%s_%s" % (i, pipe[1]), PLATFORM)
                        if (scalar_reg.enable_scaler and (
                                scalar_reg.scaler_binding != 0) and self.virtual_mode_set_aware):
                            return True
        return False

    ##
    # @brief Applies Native Mode
    # @return status-boolean value true
    def apply_native_mode(self):
        logging.debug("FUNC_ENTRY: apply_native_mode ")
        enumerated_displays = self.display_config.get_enumerated_display_info()
        for index in range(enumerated_displays.Count):
            target_id = enumerated_displays.ConnectedDisplays[index].TargetID
            native_mode = self.display_config.get_native_mode(target_id)
            if native_mode is None:
                logging.error(f"Failed to get native mode for {target_id}")
                return False
            edid_hz_res = native_mode.hActive
            edid_vt_res = native_mode.vActive
            edid_RR = native_mode.refreshRate
            supported_modes = self.display_config.get_all_supported_modes([target_id])
            for key, values in supported_modes.items():
                for mode in values:
                    if mode.HzRes == edid_hz_res and mode.VtRes == edid_vt_res and mode.refreshRate == edid_RR:
                        if self.display_config.set_display_mode([mode]):
                            logging.info(f"Successfully applied {mode} mode")
                        else:
                            logging.error(f"Failed to apply {mode} Mode")
        return True

    ##
    # @brief Verify Integer scaling is supported for particular resolution or not
    # @param[in] key - dictionary that contains the configurations
    # @param[in] mode_list - True (IS scaling) False (NN scaling)
    # @return status-boolean value true or false
    def verify_Intergerscaling_support(self, key, mode_list):
        status = False
        scalar_list = []
        for mode in mode_list:
            port = GetConnectorPort(key)
            logging.debug("Hz{}, vt{}".format(mode.HzRes, mode.VtRes))
            scaling = self.RSCALE_DICT[mode.scaling]
            scalar_list.append(display_scalar.DisplayScalar(port, scaling))
            for scalarObj in scalar_list:
                pipe = scalarObj.pipe.split("PIPE_")
                PLATFORM = scalarObj.platform
                for j in range(5):  # With the latest Cobalt OS Scalar is getting enabled in delay
                    for i in range(1, 3):
                        scalar_reg = MMIORegister.read("PS_CTRL_REGISTER", "PS_CTRL_%s_%s" % (i, pipe[1]), PLATFORM)
                        if (scalar_reg.scaler_binding != 0) and self.virtual_mode_set_aware:
                            scalar_flag = i
                            status = self.verify_integer_multiplier(scalarObj, scalar_flag)
                            return status
                        else:
                            time.sleep(0.1)
                return status

    ##
    # @brief Applies a particular mode and checks whether scaling is supported or not
    # @param[in] config_dict - dictionary that contains the configurations
    # @param[in] virtual_mode_set_aware - virtual Mode Set Aware flag - True (PLANE scalar) False (PIPE scalar)
    # @return status-boolean value true or false
    def apply_mode_and_verify_scaling(self, config_dict, virtual_mode_set_aware):
        status = True
        enumerated_displays = self.display_config.get_enumerated_display_info()
        for scalarkey, scalarvalue in config_dict.items():
            for index in range(0, len(scalarvalue)):
                # apply the user requested mode
                # To Force PLANE Scalar set "virtual_mode_set_aware" parameter as True.
                # To Force PIPE Scalar set "virtual_mode_set_aware" parameter as False (Default).
                logging.debug(f"virtual_mode_set_aware - {virtual_mode_set_aware}")
                status = self.display_config.set_display_mode([scalarvalue[index]], virtual_mode_set_aware,
                                                              enumerated_displays=None)
                if status is False:
                    logging.error("ERROR : Failed to apply display mode. Exiting ...")
                    self.fail("Failed to Apply display mode. Exiting")
                logging.info("INFO : Requested Mode is successfully applied")
                if self.virtual_mode_set_aware:
                    status = self.verify_Intergerscaling_support(scalarvalue[index].targetId, [scalarvalue[index]])
                    if status is True and self.skip_plane_scaler is False:
                        status = self.check_plane_scalar_status(scalarvalue[index].targetId, [scalarvalue[index]], 20)
                        if status is False:
                            logging.error("ERROR: Plane scalar is not enabled")
                            self.fail("Failed to enable Plane Scalar")
                    else:
                        logging.warning("Integer scaling is not supported for this resolution")
                        return True
                # Verification started
                status = self.verify_nn_is_scaling(scalarvalue[index].targetId, [scalarvalue[index]])
                if status is False:
                    logging.error("ERROR : Failed to verify scaling. Exiting..")
                    self.fail("Failed to verify scaling. Exiting")
            self.apply_native_mode()
        return status

    ##
    # @brief Applies NN or IS scaling
    # @param[in] is_integer_scaling - True (IS scaling) False (NN scaling)
    # @return status-boolean value true or false
    def apply_nn_is_scaling(self, is_integer_scaling):
        enumerated_displays = self.display_config.get_enumerated_display_info()
        self.targetid = enumerated_displays.ConnectedDisplays[0].TargetID
        status = True
        # implement apply NN/IS scaling
        if self.platform in machine_info.PRE_GEN_13_PLATFORMS:
            self.nn_args.opCode = ScalingOperation.GET_NN_SCALING_STATE.value
            status, self.nn_args = driver_escape.get_set_nn_scaling(self.targetid, self.nn_args)
            if status is False:
                gdhm.report_bug(
                    title="[NN/IS] Escape call failed : get_set_nn_scaling()",
                    problem_classification=gdhm.ProblemClassification.LOG_FAILURE,
                    component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                logging.error(f"Escape call failed : get_set_nn_scaling() for {self.targetid}")
                return status
            else:
                status = self.nn_args.NNScalingSupport.isNNScalingSupport and \
                        self.nn_args.NNScalingSupport.forceIntegerScalingSupport
                if status:
                    logging.info("PASS: NN/IS scaling supported")
                    if is_integer_scaling is True:
                        self.nn_args.NNScalingState = NNScalingState.FORCE_INTEGER_SCALING_ENABLE.value
                    else:
                        self.nn_args.NNScalingState = NNScalingState.NN_SCALING_ENABLE.value
                    self.nn_args.opCode = ScalingOperation.SET_NN_SCALING_STATE.value
                    # enabling NN scaling
                    status, self.nn_args = driver_escape.get_set_nn_scaling(self.targetid, self.nn_args)
                    if status is False:
                        gdhm.report_bug(
                            title="[NN/IS] Escape call failed : get_set_nn_scaling()",
                            problem_classification=gdhm.ProblemClassification.LOG_FAILURE,
                            component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                            priority=gdhm.Priority.P2,
                            exposure=gdhm.Exposure.E2
                        )
                        logging.error(f'Escape call failed : get_set_nn_scaling() for {self.targetid}')
                        return status
                    status = self.verify_nnscalingstate_registry(self.nn_args.NNScalingState)
                    if status is False:
                        logging.error("ERROR: NN/IS scaling enable verification fail")
                        return status
                else:
                    logging.error("ERROR: NN/IS scaling not supported")
                    gdhm.report_bug(
                        title="[NN/IS] NN/IS scaling not supported : get_set_nn_scaling()",
                        problem_classification=gdhm.ProblemClassification.LOG_FAILURE,
                        component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )
                    return status
        else:
            getRetroScalingArgsCaps = control_api_args.ctl_retro_scaling_caps_t()
            getRetroScalingArgsCaps.Size = ctypes.sizeof(getRetroScalingArgsCaps)
            logging.info("Step-1 Check RetroScaling Capability")
            status = control_api_wrapper.get_retro_scaling_caps(getRetroScalingArgsCaps, self.targetid)

            if status is False:
                gdhm.report_bug(
                    title="Control API Get Retro Scaling Caps failed",
                    problem_classification=gdhm.ProblemClassification.LOG_FAILURE,
                    component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                logging.error(f"Control API Get Retro Scaling Caps failed for {self.targetid}")
                return status
            else:
                logging.info("PASS: NN/IS scaling supported")
                logging.info("Supported retroScalingCaps - {}".format(getRetroScalingArgsCaps.SupportedRetroScaling))
                setRetroScalingArgs = control_api_args.ctl_retro_scaling_settings_t()
                setRetroScalingArgs.Size = ctypes.sizeof(setRetroScalingArgs)
                setRetroScalingArgs.Enable = True
                setRetroScalingArgs.Get = False
                if is_integer_scaling is True:
                    setRetroScalingArgs.RetroScalingType = control_api_args.ctl_retro_scaling_type_flags_v.INTEGER.value
                else:
                    setRetroScalingArgs.RetroScalingType = (control_api_args.ctl_retro_scaling_type_flags_v.
                                                            NEAREST_NEIGHBOUR.value)
                logging.info("Step-2 Set Retro Scaling via Control Library")
                status = control_api_wrapper.get_set_retro_scaling(setRetroScalingArgs, self.targetid)
                if status:
                    logging.info("Set Retro Scaling Enable: {}, Type: {}".format(setRetroScalingArgs.Enable,
                                                                                   setRetroScalingArgs.RetroScalingType))
                    getRetroScalingArgs = control_api_args.ctl_retro_scaling_settings_t()
                    getRetroScalingArgs.Size = ctypes.sizeof(getRetroScalingArgs)
                    getRetroScalingArgs.Enable = True
                    getRetroScalingArgs.Get = True
                    logging.info("Step-3  Get Retro Scaling via Control Library")
                    status = control_api_wrapper.get_set_retro_scaling(getRetroScalingArgs, self.targetid)
                    if status:
                        logging.info("Get Retro Scaling Enable: {}, Type: {}".format(getRetroScalingArgs.Enable,
                                                                                getRetroScalingArgs.RetroScalingType))

                        logging.info("Step-4  Verify the enabling of NN/IS scaling through the Control Library")

                        setvalue = int.from_bytes(setRetroScalingArgs.RetroScalingType, byteorder='little')
                        getvalue = int.from_bytes(getRetroScalingArgs.RetroScalingType, byteorder='little')
                        status = setvalue == getvalue

                        if status:
                            logging.info("PASS: NN/IS scaling enabled via Control Library")
                        else:
                            logging.error("ERROR: NN/IS scaling not enabled via Control Library")
                            return status
                    else:
                        logging.error("ERROR: Get Retro Scaling via Control Library")
                        gdhm.report_driver_bug_clib("Get Retro Scaling Failed via Control Library for "
                                                    "RetroScaling: {0} Enable: {1} TargetId: {2}"
                                                    .format(getRetroScalingArgs.RetroScalingType,
                                                            getRetroScalingArgs.Enable, self.targetid))
                        return status
                else:
                    logging.error("ERROR: Set Retro Scaling via Control Library")
                    gdhm.report_driver_bug_clib("Set Retro Scaling Failed via Control Library for "
                                                "RetroScaling: {0} Enable: {1} TargetId: {2}"
                                                .format(setRetroScalingArgs.RetroScalingType,
                                                        setRetroScalingArgs.Enable, self.targetid))
                    return status

        return status

    ##
    # @brief TO verify whether nn/is scaling
    # @param[in] key - display_adapter_info or target id
    # @param[in] mode_list - list that contains the mode
    # @return status-boolean value true or false
    def verify_nn_is_scaling(self, key, mode_list):
        status = True
        logging.debug("FUNC_ENTRY: verify_nn_is_scaling")
        status = self.verify_scaling_register_programming(key, mode_list)
        if status is False:
            logging.error("ERROR: MMIO register verification failed")
        return status

    ##
    # @brief To verify nn scaling state registry value
    # @param[in] exp_state - expected registry value
    # @return boolean value true or false
    def verify_nnscalingstate_registry(self, exp_state):

        # verify NNScalingState register value 0 disable , 1 NN scaling, 2 Force IS scaling
        NNscalingState, reg_type = registry_access.read(args=self.ss_reg_args, reg_name="NNScalingState")
        logging.debug(f"NNScalingState = {NNscalingState}, reg_type = {reg_type}, expected = {exp_state}")
        if registry_access.RegDataType.BINARY is registry_access.RegDataType(reg_type):
            NNscalingState = int.from_bytes(NNscalingState, byteorder="little")
        if NNscalingState != exp_state:
            gdhm.report_bug(
                title="[NN/IS] NNScalingState regkey verification failed",
                problem_classification=gdhm.ProblemClassification.LOG_FAILURE,
                component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.error(
                "ERROR: NNScalingState registry Actual value:{} expected: {}".format(NNscalingState, exp_state))
            return False
        return True

    ##
    # @brief To verify integer multiplier for IS scaling
    # @param[in] scalarObj - Scalar object which used for scaling
    # @param[in] scalar_flag - to specify if scalar 1 or scalar 2 is enabled
    # @return boolean value true or false
    def verify_integer_multiplier(self, scalarObj, scalar_flag):
        status = False
        expected_multiplier = 0
        actual_multiplier = 0
        logging.info(" Integer multiplier verification ".center(64, "*"))
        # calculate max value using timing and current mode.

        source_mode = self.display_config.get_current_mode(scalarObj.targetId)
        src_hactive = source_mode.HzRes
        src_vactive = source_mode.VtRes

        target_mode = self.display_config.get_display_timings(scalarObj.targetId)
        tgt_hactive = target_mode.hActive
        tgt_vactive = target_mode.vActive

        logging.info(
            "INFO : Source Mode (HActive x VActive) : %sx%s Target Mode (HActive x VActive) : %sx%s Scaling Mode : %s"
            % (src_hactive, src_vactive, tgt_hactive, tgt_vactive, scalarObj.scaling_mode))

        expected_multiplier = min(tgt_hactive // src_hactive, tgt_vactive // src_vactive)

        # calculate integer value with register
        pipe = scalarObj.pipe.split("PIPE_")
        PLATFORM = scalarObj.platform

        scalar_size = MMIORegister.read("PS_WIN_SZ_REGISTER", "PS_WIN_SZ_%s_%s" % (scalar_flag, pipe[1]), PLATFORM)
        logging.debug("PS_WIN_SZ_%s_%s" % (scalar_flag, pipe[1]) + "--> Offset : "
                      + format(scalar_size.offset, '08X') + " Value :" + format(scalar_size.asUint, '08X'))

        scalar1_reg = MMIORegister.read("PS_CTRL_REGISTER", "PS_CTRL_%s_%s" % (scalar_flag, pipe[1]), PLATFORM)
        plane = scalar_flag if scalar1_reg.scaler_binding == 0 else scalar1_reg.scaler_binding
        logging.info("Plane Scaler Binding enable: {}".format(plane))

        # Check for Layer Reordering in case of supported platforms
        if not planes_verification.check_layer_reordering():
            time.sleep(20)  # Win2024 OS is causing sporadic failures post reading PLANE size register
            plane_size = MMIORegister.read("PLANE_SIZE_REGISTER", "PLANE_SIZE_3_%s" % (pipe[1]), PLATFORM)
            logging.debug("PLANE_SIZE_3_%s" % (pipe[1]) + "--> Offset : "
                          + format(plane_size.offset, '08X') + " Value :" + format(plane_size.asUint, '08X'))
        else:
            time.sleep(20)  # Win2024 OS is causing sporadic failures post reading PLANE size register
            plane_size = MMIORegister.read("PLANE_SIZE_REGISTER", "PLANE_SIZE_%s_%s" % (plane, pipe[1]), PLATFORM)
            logging.debug("PLANE_SIZE_%s_%s" % (plane, pipe[1]) + "--> Offset : "
                          + format(plane_size.offset, '08X') + " Value :" + format(plane_size.asUint, '08X'))

        # Calculate expected multiplier
        actual_multiplier = scalar_size.xsize // plane_size.width
        if actual_multiplier == expected_multiplier:
            if (actual_multiplier and expected_multiplier == 1) and self.virtual_mode_set_aware:
                self.skip_plane_scaler = True
            logging.info("PASS: Integer multiplication verified expected:{}, actual:{}".format(expected_multiplier,
                                                                                               actual_multiplier))
            return True
        else:
            gdhm.report_bug(
                title="[NN/IS] Integer multiplication verification failed",
                problem_classification=gdhm.ProblemClassification.LOG_FAILURE,
                component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.error("ERROR: Integer multiplication verified expected:{}, actual:{}".format(expected_multiplier,
                                                                                                 actual_multiplier))
            return False

    ##
    # @brief To verify scaling register programming
    # @param[in] key - display_adapter_info or target id
    # @param[in] mode_list - list that contains the mode
    # @return status which returns true or false
    def verify_scaling_register_programming(self, key, mode_list):
        logging.debug("FUNC_ENTRY: scaling_register_programming verification ")
        status = False
        logging.info(" scaling_register_programming verification ".center(64, "*"))
        scalar_list = []
        for mode in mode_list:
            port = GetConnectorPort(key)
            if mode.scaling == 1:  # ignore CI as no scaling applied from driver side.
                return True
            logging.debug("Hz{}, Vt{}".format(mode.HzRes, mode.VtRes))

            scaling = self.RSCALE_DICT[mode.scaling]
            scalar_list.append(display_scalar.DisplayScalar(port, scaling))

            # PS_CTRL register verification
            status = self.VerifyScalarProgramming(scalar_list)
            if status is True:
                # PS_Coeff_data register verification
                status = self.VerifyCoeffDataRegister(scalar_list)

        logging.debug("FUNC_EXIT: scaling_register_programming verification ")
        return status

    ##
    # @brief To verify Scalar programming
    # @param[in] scalarList - DisplayScalar() instance to specify display_port and scalar mode
    # @return status which returns true or false
    def VerifyScalarProgramming(self, scalarList):
        status = False
        for scalarObj in scalarList:
            scalar_flag = 0
            if scalarObj.pipe is None:
                gdhm.report_bug(
                    title="[NN/IS] {0} is not connected to any Pipe.".format(scalarObj.display_port),
                    problem_classification=gdhm.ProblemClassification.LOG_FAILURE,
                    component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                logging.error(
                    "ERROR : " + scalarObj.display_port + " is not connected to any Pipe. Check if it is connected")
                return False
            pipe = scalarObj.pipe.split("PIPE_")
            PLATFORM = scalarObj.platform

            scalar1_reg = MMIORegister.read("PS_CTRL_REGISTER", "PS_CTRL_1_%s" % (pipe[1]), PLATFORM)
            scalar2_reg = MMIORegister.read("PS_CTRL_REGISTER", "PS_CTRL_2_%s" % (pipe[1]), PLATFORM)

            # Pipe Scalar verification
            if scalar1_reg.enable_scaler and (scalar1_reg.scaler_binding == 0) and not self.virtual_mode_set_aware:
                # Pipe scalar enabled on scalar1
                scalar_flag = 1
                logging.info("INFO : %s - PIPE Scalar 1 is enabled on Pipe%s" % (scalarObj.display_port, pipe[1]))
            elif scalar2_reg.enable_scaler and (scalar2_reg.scaler_binding == 0) and not self.virtual_mode_set_aware:
                # Pipe scalar enabled on scalar2
                scalar_flag = 2
                logging.info("INFO : %s - PIPE Scalar 2 is enabled on Pipe%s" % (scalarObj.display_port, pipe[1]))
            elif not self.virtual_mode_set_aware:
                gdhm.report_bug(
                    title="[NN/IS] Pipe Scalar not enabled",
                    problem_classification=gdhm.ProblemClassification.LOG_FAILURE,
                    component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                logging.error("ERROR : Pipe Scalar is not enabled")
                return False

            logging.info("{}".format(self.virtual_mode_set_aware))
            # Plane Scalar verification
            if scalar1_reg.enable_scaler and (scalar1_reg.scaler_binding != 0) and self.virtual_mode_set_aware:
                # Plane scalar enabled on Scalar 1
                scalar_flag = 1
                logging.info("INFO : %s - PLANE Scalar 1 is enabled on Pipe%s" % (scalarObj.display_port, pipe[1]))
            elif scalar2_reg.enable_scaler and (scalar2_reg.scaler_binding != 0) and self.virtual_mode_set_aware:
                # Plane scalar enabled on Scalar 2
                scalar_flag = 2
                logging.info("INFO : %s - PLANE Scalar 2 is enabled on Pipe%s" % (scalarObj.display_port, pipe[1]))
            elif self.virtual_mode_set_aware:
                gdhm.report_bug(
                    title="[NN/IS] Plane scalar not enabled",
                    problem_classification=gdhm.ProblemClassification.LOG_FAILURE,
                    component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                logging.error("ERROR : Plane Scalar is not enabled")
                return False

            status = self.VerifyFilterSelection(pipe[1], PLATFORM, is_prgm_mode_enable=True, scalarflag=scalar_flag)
            if status is False:
                self.fail("Program mode is still disable")
            # Get Scalar Size -position and verify it.
            if self.is_integer_scaling is False:
                status = display_scalar.get_scalar_size_position(scalarObj)
            else:
                self.get_Intergerscalar_size_position(scalarObj)
            if status is False:
                return status
            status = display_scalar.VerifyScalarSizePosition(scalarObj, scalar_flag)
            # With the latest Cobalt OS Position is getting reflected after few sec
            if status is False:
                for i in range(5):
                    time.sleep(0.1)
                    status = display_scalar.VerifyScalarSizePosition(scalarObj, scalar_flag)
                    if status is True:
                        break
                return status

            # verify Integer multiplication for IS scaling only
            if self.is_integer_scaling is True:
                status = self.verify_integer_multiplier(scalarObj, scalar_flag)
            if status is False:
                return status
        return status

    ##
    # @brief To verify filter selection
    # @param[in] pipe - the name of the pipe
    # @param[in] PLATFORM - the name of the Platform
    # @param[in] is_prgm_mode_enable - tells whether program mode enabled or not
    # @param[in] scalarflag  - to specify if scalar 1 or scalar 2 is enabled
    # @return boolean value true or false
    def VerifyFilterSelection(self, pipe, PLATFORM, is_prgm_mode_enable=True, scalarflag=1):
        scalar_reg = MMIORegister.read("PS_CTRL_REGISTER", "PS_CTRL_%s_%s" % (scalarflag, pipe), PLATFORM)
        logging.debug("PS_CTRL_1_" + pipe + "--> Offset : "
                      + format(scalar_reg.offset, '08X') + " Value :" + format(scalar_reg.asUint, '08X'))

        if is_prgm_mode_enable:
            if scalar_reg.filter_select != 1:
                gdhm.report_bug(
                    title="[NN/IS] Program mode is still disable, expected enable",
                    problem_classification=gdhm.ProblemClassification.LOG_FAILURE,
                    component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                logging.error("ERROR : Programmed mode is not enabled on Pipe%s" % (pipe))
                return False
            else:
                logging.info("INFO : Programmed mode is enabled on Pipe%s" % (pipe))
                return True
        else:
            if scalar_reg.filter_select == 1:
                gdhm.report_bug(
                    title="[NN/IS] Program mode is still enable, expected disable",
                    problem_classification=gdhm.ProblemClassification.LOG_FAILURE,
                    component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                logging.error("ERROR : Programmed mode is enabled on Pipe%s" % (pipe))
                return False
            else:
                logging.info("INFO : Programmed mode is not enabled on Pipe%s" % (pipe))
                return True

    ##
    # @brief To verify Coefficient data value
    # @param[in] etl_file_name - Captured ETL Data file
    # @param[in] scalar_reg - Scalar register instances
    # @return boolean value true or false
    def verify_coefficient_data(self, etl_file_name, scalar_reg):
        global scalar_reg_data
        start_mmio = None
        end_mmio = None

        if etl_file_name is None:
            logging.error("ETL Failed to generate")
            self.fail("Failed to generate ETL")
        loop_index = 0
        co_eff_data_value = []
        co_eff_data = [0X30003000, 0X08003000, 0X30003000, 0X30003000, 0X30003000, 0x30000800, 0x30003000]

        offset = scalar_reg.offset

        if etl_parser.generate_report(etl_file_name) is False:
            logging.error("Failed to generate EtlParser report")
            return False

        scaler_data = etl_parser.get_event_data(etl_parser.Events.SCALER_INFO)
        scaler_plane_data = etl_parser.get_event_data(etl_parser.Events.SCALER_PLANE)

        if scaler_data is not None:
            logging.debug(f"Scaler Data - {scaler_data}")
            for scaler_enable_flag in scaler_data:
                if scaler_enable_flag.EnableFlag:
                    logging.debug(f"Scaler Timestamp - {scaler_enable_flag.TimeStamp}")
                    start_mmio = scaler_enable_flag.TimeStamp
        elif scaler_plane_data is not None:
            for scaler_plane_enable_flag in scaler_plane_data:
                if scaler_plane_enable_flag.EnableFlag:
                    logging.debug(f"Scaler Timestamp - {scaler_plane_enable_flag.TimeStamp}")
                    start_mmio = scaler_plane_enable_flag.TimeStamp
        else:
            logging.warning("\tWARNING: Event scaler_data/scaler_plane_data missing from ETL ")
            start_mmio = None

        logging.debug(f"DEBUG: co_eff_data_offset - {offset}")
        if self.platform not in machine_info.PRE_GEN_15_PLATFORMS and self.scalar == 'PLANE':
            scalar_reg_data = etl_parser.get_mmio_data(offset, is_write=True, start_time=start_mmio, end_time=end_mmio,
                                                       is_cpu_mmio=False)
            logging.debug("Considering Scalar MMIO data from DSB Path as FlipQ is enabled")
        else:
            scalar_reg_data = etl_parser.get_mmio_data(offset, is_write=True, is_cpu_mmio=True)
            logging.debug("Considering Scalar MMIO data from CPU MMIO Path as FlipQ is disabled")

        if scalar_reg_data is None:
            logging.error("Scalar_reg MMIO data is Empty")
            return False

        for status in scalar_reg_data:
            if status.Offset == offset:
                scalar_reg.asUint = status.Data
                co_eff_data_value.append(scalar_reg.asUint)
        logging.debug(f"DEBUG: co_eff_data_offset - {offset}")
        logging.debug(f"DEBUG: co_eff_data_value_list - {co_eff_data_value}")

        for index in range(0, 60):
            logging.debug(f"DEBUG: Act-index/co_eff_data_value - {index}/{hex(co_eff_data_value[index])},"
                          f" Exp-loop_index/co_eff_data - {loop_index}/{hex(co_eff_data[loop_index])}")
            if co_eff_data_value[index] != co_eff_data[loop_index]:
                logging.error(f"ERROR: Co_eff_data value mismatch at index {index} actual:" +
                              format(scalar_reg.asUint, '08X') + "expected:" + format(co_eff_data[loop_index]), '08X')
                gdhm_title = f"[NN/IS] Co_eff_data value mismatch at Index - {index}, actual:" \
                             + format(scalar_reg.asUint, '08X') + "expected:" + format(co_eff_data[loop_index], '08X')
                gdhm.report_bug(
                    title=gdhm_title,
                    problem_classification=gdhm.ProblemClassification.LOG_FAILURE,
                    component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                return False
            else:
                logging.debug("DEBUG: Co_eff_data match for loop index:" + format(loop_index) + " value:" + format(
                    scalar_reg.asUint, '08X'))
            loop_index += 1
            if loop_index == 7:
                loop_index = 0
        return True

    ##
    # @brief To verify Coefficient data register
    # @param[in] scalarList - DisplayScalar() instance to specify display_port and scalar mode
    # @return boolean value true or false
    def VerifyCoeffDataRegister(self, scalarList):
        global scalar_coff
        logging.debug("FUNC_ENTRY: VerifyCoeffDataRegister")

        for scalarObj in scalarList:
            if scalarObj.pipe is None:
                gdhm.report_bug(
                    title="[NN/IS] {0} is not connected to any Pipe.".format(scalarObj.display_port),
                    problem_classification=gdhm.ProblemClassification.LOG_FAILURE,
                    component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                logging.error(
                    "ERROR : " + scalarObj.display_port + " is not connected to any Pipe. Check if it is connected")
                return False
            pipe = scalarObj.pipe.split("PIPE_")
            PLATFORM = scalarObj.platform
            for index in range(0, 60):
                coef_index_reg = MMIORegister.read("PS_COEF_INDEX_REGISTER", "PS_COEF_SET_0_INDEX_1_%s" % (pipe[1]),
                                                   PLATFORM)
                logging.debug("DEBUG: PS_COEF_SET_0_INDEX_1_%s" + pipe[1] + "--> Offset : "
                              + format(coef_index_reg.offset, '08X') + " Value :" + format(coef_index_reg.asUint,
                                                                                           '08X'))
                if coef_index_reg.index_value == 0:
                    break

            scalar1_reg = MMIORegister.read("PS_CTRL_REGISTER", "PS_CTRL_1_%s" % (pipe[1]), PLATFORM)
            scalar2_reg = MMIORegister.read("PS_CTRL_REGISTER", "PS_CTRL_2_%s" % (pipe[1]), PLATFORM)

            if scalar1_reg.enable_scaler:
                scalar_coff = MMIORegister.get_instance("PS_COEF_DATA_REGISTER", "PS_COEF_SET_0_DATA_1_%s" % (pipe[1]),
                                                        PLATFORM)
            if scalar2_reg.enable_scaler:
                scalar_coff = MMIORegister.get_instance("PS_COEF_DATA_REGISTER", "PS_COEF_SET_0_DATA_2_%s" % (pipe[1]),
                                                        PLATFORM)

            file_name = 'GfxTrace_verify_coeff' + str(time.time()) + '.etl'
            etl_file_path = os.path.join(test_context.LOG_FOLDER, file_name)

            if etl_tracer.stop_etl_tracer():
                if os.path.exists(etl_tracer.GFX_TRACE_ETL_FILE):
                    os.rename(etl_tracer.GFX_TRACE_ETL_FILE, etl_file_path)
                elif os.path.exists(etl_tracer.GFX_BOOT_TRACE_ETL_FILE):
                    os.rename(etl_tracer.GFX_BOOT_TRACE_ETL_FILE, etl_file_path)
            else:
                self.fail("Failed to stop etl trace")

            if self.verify_coefficient_data(etl_file_path, scalar_coff) is False:
                logging.error("Error Mismatch in coefficient data value")
                return False

            if etl_tracer.start_etl_tracer() is False:
                self.fail("Failed to start etl trace")

        return True

    ##
    # @brief Calculate scalar plane size and position based on scalar mode (CI,FS,MAR)
    # @param[in] scalarObj - scalar object which need to fill
    # @return Fill scalarObj (xsize, ysize, xpos, ypos)
    def get_Intergerscalar_size_position(self, scalarObj):
        ISFactor = None

        source_mode = self.display_config.get_current_mode(scalarObj.targetId)
        src_hactive = source_mode.HzRes
        src_vactive = source_mode.VtRes

        target_mode = self.display_config.get_display_timings(scalarObj.targetId)
        tgt_hactive = target_mode.hActive
        tgt_vactive = target_mode.vActive

        logging.info(
            "INFO : Source Mode (Hactive x Vactive) : %sx%s Target Mode (Hactive x Vactive) : %sx%s Scaling Mode : %s"
            % (src_hactive, src_vactive, tgt_hactive, tgt_vactive, scalarObj.scaling_mode))

        ISFactor = min(tgt_hactive // src_hactive, tgt_vactive // src_vactive)
        scalarObj.xsize = src_hactive * ISFactor
        scalarObj.ysize = src_vactive * ISFactor
        scalarObj.xpos = (tgt_hactive - scalarObj.xsize) // 2
        scalarObj.ypos = (tgt_vactive - scalarObj.ysize) // 2

        # Scalar size and position has to be an even number for YUV420 format, if computed size is odd then reduce to 1
        # as increasing can cause the size to become more than pipe size which is wrong.
        # Keeping the logic common for all color formats and putting changes only for GEN11 to keep in sync with driver
        # TODO:Need to implement for legacy platforms
        if self.system_utility.is_ddrw():
            scalarObj.xsize = (scalarObj.xsize - 1) if (scalarObj.xsize % 2 != 0) else scalarObj.xsize
            scalarObj.ysize = (scalarObj.ysize - 1) if (scalarObj.ysize % 2 != 0) else scalarObj.ysize
            scalarObj.xpos = (scalarObj.xpos - 1) if (scalarObj.xpos % 2 != 0) else scalarObj.xpos
            scalarObj.ypos = (scalarObj.ypos - 1) if (scalarObj.ypos % 2 != 0) else scalarObj.ypos

    ##
    # @brief tearDown Function for NNIS scaling
    # @return - None
    @reboot_helper.__(reboot_helper.teardown)
    def tearDown(self):
        logging.info("CleanUp of Scaling base")
        ##
        # Unplug the displays and restore the configuration to the initial configuration
        if self.is_teardown_required:
            enumerated_displays = self.display_config.get_enumerated_display_info()
            self.targetid = enumerated_displays.ConnectedDisplays[0].TargetID
            self.nn_args.NNScalingState = NNScalingState.NN_SCALING_DISABLE.value
            self.nn_args.opCode = ScalingOperation.SET_NN_SCALING_STATE.value
            status, self.nn_args = driver_escape.get_set_nn_scaling(self.targetid, self.nn_args)  # enabling NN scaling
            if status is False:
                gdhm.report_bug(
                    title="[NN/IS] Escape call failed : get_set_nn_scaling()",
                    problem_classification=gdhm.ProblemClassification.LOG_FAILURE,
                    component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                logging.error(f'Escape call failed : get_set_nn_scaling() for {self.targetid}')
            for display in self.display_list:
                if display_utility.get_vbt_panel_type(display, 'gfx_0') not in \
                        [display_utility.VbtPanelType.LFP_DP, display_utility.VbtPanelType.LFP_MIPI]:
                    logging.info("Trying to unplug %s", display)
                    self.assertEquals(display_utility.unplug(display), True,
                                      "Aborting the test as display unplug failed")
                    logging.info("Successfully  unplugged %s", display)
                else:
                    logging.info("unplugged of {} display skipped".format(display))
        else:
            logging.debug("Unplug of displays not required")


if __name__ == '__main__':
    unittest.main()
