######################################################################################
# \file         lace_base.py
# \section      lace_base
# \remarks      This script contains helper functions that will be used by
#               LACE test scripts
# \ref          lace_base.py \n
# \author       Smitha B, Soorya R
######################################################################################
import sys
import unittest
import time
from Libs.Core import driver_escape, registry_access, display_essential, system_utility
from Libs.Core import display_power as disp_pwr, reboot_helper, cmd_parser, display_utility, enum
from Libs.Core.wrapper.driver_escape_args import CuiEscOperationType, PwrConsOperation, ComEscPowerConservationArgs, \
     PwrSrcEventArgs
from Libs.Core.display_config.display_config_enums import DisplayConfigTopology
from Libs.Core.flip import MPO, SB_PIXELFORMAT, MPO_BLEND_VAL, SURFACE_MEMORY_TYPE, MPO_RECT
from Libs.Core.flip import PLANE_INFO, MPO_PLANE_ORIENTATION, MPO_COLOR_SPACE_TYPE, PLANE
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Feature.crc_and_underrun_verification import UnderRunStatus
from Libs.Feature.powercons import registry
from Tests.Color.Common import color_constants, common_utility
from Tests.Color import color_common_utility
from Tests.Color.LACE.lace_utility import *
from Libs.Core.display_config import display_config
from Tests.Color.LACE.lace_verification import *

machine_info = SystemInfo()
os_info = machine_info.get_os_info()
##
# Get the platform info
platform = None
gfx_display_hwinfo = machine_info.get_gfx_display_hardwareinfo()
# WA : currently test are execute on single platform. so loop break after 1 st iteration.
# once Enable MultiAdapter remove the break statement.
for i in range(len(gfx_display_hwinfo)):
    platform = str(gfx_display_hwinfo[i].DisplayAdapterName).lower()
    break


class Aggressiveness_Levels(enum.Enum):
    _members_ = {
        'AGGR_LEVEL_LOW': 0,
        'AGGR_LEVEL_MODERATE': 1,
        'AGGR_LEVEL_HIGH': 2
    }


class LACEBase(unittest.TestCase):
    connected_list = []
    utility = system_utility.SystemUtility()
    driver_interface_ = driver_interface.DriverInterface()
    display_power = disp_pwr.DisplayPower()

    config = DisplayConfiguration()
    actual_lace_status = "DISABLED"
    expected_lace_status = "DISABLED"
    target_id = None
    lfp_target_ids = []
    lfp_pipe_ids = []
    underrun = UnderRunStatus()
    custom_tags = ["-IMAGEFILE"]
    lace1p0_reg_value = None
    lace1p0_status = None
    mpo = MPO()

    @reboot_helper.__(reboot_helper.setup)
    def setUp(self):
        self.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, self.custom_tags)

        for key, value in self.cmd_line_param.items():
            if cmd_parser.display_key_pattern.match(key) is not None:
                if value['connector_port'] is not None:
                    self.connected_list.insert(value['index'], value['connector_port'])

        ##
        # Verify and plug the display
        if len(self.connected_list) <= 0:
            logging.error("Minimum 1 display is required to run the test")
            self.fail()
        else:
            self.plugged_display, self.enumerated_displays = display_utility.plug_displays(self, self.cmd_line_param)

        ##
        # Verify if the test is targeted with a min 1 LFP panel
        lfp_panel = False
        for index in range(len(self.connected_list)):
            if display_utility.get_vbt_panel_type(self.connected_list[index], 'gfx_0') in \
                        [display_utility.VbtPanelType.LFP_DP, display_utility.VbtPanelType.LFP_MIPI]:
                lfp_panel = True
                break
        if lfp_panel is False:
            logging.error("LACE is supported only on LFPs .Minimum 1 LFP is required to run the test")
            self.fail()

        ##
        # Set display configuration
        topology = eval("enum.%s" % (self.cmd_line_param['CONFIG']))
        if self.config.set_display_configuration_ex(topology, self.connected_list) is False:
            self.fail('Failed to apply display configuration %s %s' %
                      (DisplayConfigTopology(topology).name, self.connected_list))

        logging.info('Successfully applied the display configuration as %s %s' %
                     (DisplayConfigTopology(topology).name, self.connected_list))

        # Get the LFP target and Pipe ID's
        for index in range(len(self.connected_list)):
            display_base_obj = DisplayBase(self.connected_list[index])
            target_id = self.config.get_target_id(self.connected_list[index], self.enumerated_displays)
            current_transcoder, current_pipe = display_base_obj.get_transcoder_and_pipe(self.connected_list[index])
            if display_utility.get_vbt_panel_type(self.connected_list[index], 'gfx_0') in \
                    [display_utility.VbtPanelType.LFP_DP, display_utility.VbtPanelType.LFP_MIPI]:
                self.lfp_pipe_ids.append(current_pipe)
                self.lfp_target_ids.append(target_id)

        exec_env = self.utility.get_execution_environment_type()
        feature_test_control = registry.FeatureTestControl('gfx_0')

        # HSD-18023973505- Handle condition to disable the HDR, if enabled in previous test or job
        status, reg_value = common_utility.read_registry(gfx_index="GFX_0", reg_name="ForceHDRMode")
        if reg_value:
            logging.info("ForceHDRMode registry key was enabled.Need to disable it to configure Lace")
            if common_utility.write_registry(gfx_index="GFX_0", reg_name="ForceHDRMode",
                                             reg_datatype=registry_access.RegDataType.DWORD, reg_value=0,
                                             driver_restart_required=True) is False:
                logging.error("Failed to disable ForceHDRMode registry key")
                self.fail("Failed to disable ForceHDRMode registry key")
            logging.info("Registry key add to disable ForceHDRMode is successful")
        else:
            logging.info("ForceHDRMode Registry key is either not preset or not enabled")

        # Enable Lace1.0 coverage for ARL
        self.lace1p0_status, self.lace1p0_reg_value = common_utility.read_registry(gfx_index="GFX_0",
                                                                                   reg_name="LaceVersion")
        if machine_info.get_sku_name('gfx_0') == 'ARL':
            if common_utility.write_registry(gfx_index="GFX_0", reg_name="LaceVersion",
                                             reg_datatype=registry_access.RegDataType.DWORD, reg_value=10,
                                             driver_restart_required=True) is False:
                logging.error("Failed to enable Lace1.0 registry key")
                self.fail("Failed to enable Lace1.0 registry key")
            logging.info("Registry key add to enable Lace1.0 is successful")
        else:
            logging.info("Lace1.0 Registry Key is either not present or not enabled")

        reg_args = registry_access.LegacyRegArgs(hkey=registry_access.HKey.LOCAL_MACHINE,
                                                 reg_path=r"SOFTWARE\Intel\Display")
        # Enable Lace1.0 coverage for ARL, MTL
        self.lace1p0_status, self.lace1p0_reg_value = common_utility.read_registry(gfx_index="GFX_0",
                                                                                   reg_name="LaceVersion")
        for gfx_index, adapter in self.context_args.adapters.items():
            if adapter.platform in ['ARL', 'MTL']:
                if common_utility.write_registry(gfx_index="GFX_0", reg_name="LaceVersion",
                                                 reg_datatype=registry_access.RegDataType.DWORD, reg_value=10,
                                                 driver_restart_required=True) is False:
                    logging.error("Failed to enable Lace1.0 registry key")
                    self.fail("Failed to enable Lace1.0 registry key")
                logging.info("Registry key add to enable Lace1.0 is successful")
            else:
                logging.info("Lace1.0 Registry Key is either not present or not enabled")

        if exec_env == 'POST_SI_ENV':

            if feature_test_control.lace_disable:
                logging.debug("FeatureTestControl registry key for Lace is Enabled")
                ##
                # Need to set BKPDisplayLACE Registry Key and fail the test if disabled
                registry_access.write(args=reg_args, reg_name="BKPDisplayLACE",
                                      reg_type=registry_access.RegDataType.DWORD, reg_value=1, sub_key=r"igfxcui\MISC")
                restart_status, reboot_required = display_essential.restart_gfx_driver()
                reg_val, reg_type = registry_access.read(args=reg_args, reg_name="BKPDisplayLACE", sub_key=r"igfxcui\MISC")
                if not reg_val:
                    self.fail("BKPDisplayLACE registry key is not enabled")
                else:
                    logging.info("BKPDisplayLACE registry key is enabled")
            else:
                logging.info("BKPDisplayLACE registry key is enabled")

        else:
            if feature_test_control.lace_disable:
                logging.debug("Lace is enabled in FeatureTestControl registry key")
                reg_val, reg_type = registry_access.read(args=reg_args, reg_name="BKPDisplayLACE", sub_key=r"igfxcui\MISC")
                if not reg_val:
                    self.fail("BKPDisplayLACE registry key is not set as part of the plugin for the GTA job/PreSi setup")
                else:
                    logging.info("BKPDisplayLACE registry key is enabled")
            else:
                logging.info("BKPDisplayLACE registry key is enabled")

        # Check Power Mode  for DC or AC. Lace works with both AC and DC
        # In Enable_pwrcons_feature, setted to default AC as the power source, in feature ,if user wants to
        # prefer power source,we need to modify the commandlines or script
        result, status = color_common_utility.check_and_apply_power_mode()
        if status:
            logging.info(result)
        else:
            self.fail(result)

    def enable_pwrcons_feature(self, gfx_index="gfx_0", power_source="AC", pwrcons_feature="LACE", Enable=1):

        # Below Set Escape API will be applicable till Gen12 to enable the support for Lace
        if platform.upper() in color_constants.PRE_GEN_13_PLATFORMS:
            feature_args = ComEscPowerConservationArgs()
            feature_args.Operation = PwrConsOperation.PWRCONS_OP_FEATURE_SETTINGS.value
            feature_args.PowerSourceType = PwrSrcEventArgs.PWR_AC.value if power_source == "AC" else PwrSrcEventArgs.PWR_DC.value
            feature_args.OpParameters.FeatureSettingsParam.Policy.Enabled.Lace = Enable
            feature_args.OpType = CuiEscOperationType.SET.value
            status, feature_args = driver_escape.get_set_display_pc_feature_state(gfx_index, feature_args)
            if status is False:
                logging.error("Failed to set Lace with pc feature state escape")
                return False
            logging.info("PASS : Successfully enabled {0}".format(pwrcons_feature))
        return True

    def display_staticimage(self, image_path=None, pixel_format=SB_PIXELFORMAT.SB_B8G8R8A8):
        result = 0
        pyPlanes = []
        for index in range(len(self.lfp_target_ids)):
            resolution = self.config.get_current_mode(self.lfp_target_ids[index])
            stMPOBlend = MPO_BLEND_VAL(0)
            tiling = SURFACE_MEMORY_TYPE.SURFACE_MEMORY_LINEAR
            if (image_path):
                file_name = image_path
            elif self.cmd_line_param['IMAGEFILE'] != 'NONE':
                file_name = self.cmd_line_param['IMAGEFILE'][0]
            else:
                logging.error("No image file input given !!")
                self.fail()
            path = os.path.join("Color\LACE\Images", file_name)

            sdimension = MPO_RECT(0, 0, resolution.HzRes, resolution.VtRes)
            ddimension = MPO_RECT(0, 0, resolution.HzRes, resolution.VtRes)
            pyPlanes = []
            out_file0 = convert_png_to_bin(path, resolution.HzRes,
                                           resolution.VtRes, pixel_format, index)
            # Check if source ID is correct
            Plane1 = PLANE_INFO(index, 0, 1, pixel_format, tiling, sdimension, ddimension,
                                ddimension, MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT, stMPOBlend,
                                MPO_COLOR_SPACE_TYPE.MPO_COLOR_SPACE_RGB_FULL_G22_NONE_P709, out_file0)
            pyPlanes.append(Plane1)
        planes = PLANE(pyPlanes)

        for index in range(0, planes.uiPlaneCount):
            result = self.mpo.check_mpo3(planes)
            if result == 0:
                logging.info("CheckMPO returned success")
            else:
                logging.error("Display Image Failed due to CheckMPO failure !!")
                self.fail()
            status = self.mpo.set_source_address_mpo3(planes)
            if status == 0:
                logging.info("Successfully flipped planes")
            else:
                logging.error("Display Image Failed due to flip submission failure !!")
                self.fail()

    def disable_ieenable_function(self):
        for index in range(len(self.lfp_pipe_ids)):
            str_pipe = chr(int(self.lfp_pipe_ids[index]) + 65)
            str_plane_pipe = "1_" + str_pipe

            module_name = "DPLC_CTL_REGISTER"
            reg_name = "DPLC_CTL" + "_" + str_pipe
            instance = reg_read.get_instance(module_name, reg_name, platform)
            dplc_ctl_offset = instance.offset
            dplc_ctl_reg_value = reg_read.read(module_name, reg_name, platform)
            dplc_ctl_reg_value.ie_enable = 0
            self.driver_interface_.mmio_write(dplc_ctl_offset, dplc_ctl_reg_value.asUint, 'gfx_0')
            dplc_ctl_reg_value = reg_read.read(module_name, reg_name, platform)

    def disable_color_pipeline_blocks(self):
        for index in range(len(self.lfp_pipe_ids)):
            str_pipe = chr(int(self.lfp_pipe_ids[index]) + 65)
            str_plane_pipe = "1_" + str_pipe

            module_name = "PLANE_COLOR_CTL_REGISTER"
            reg_name = "PLANE_COLOR_CTL" + "_" + str_plane_pipe
            instance = reg_read.get_instance(module_name, reg_name, platform)
            color_ctl_offset = instance.offset

            module_name = "GAMMA_MODE_REGISTER"
            reg_name = "GAMMA_MODE" + "_" + str_pipe
            instance = reg_read.get_instance(module_name, reg_name, platform)
            gamma_mode_offset = instance.offset

            module_name = "CSC_MODE_REGISTER"
            reg_name = "CSC_MODE" + "_" + str_pipe
            instance = reg_read.get_instance(module_name, reg_name, platform)
            csc_mode_offset = instance.offset

            self.driver_interface_.mmio_write(color_ctl_offset, 0x10002000, 'gfx_0')
            self.driver_interface_.mmio_write(gamma_mode_offset, 0x0, 'gfx_0')
            self.driver_interface_.mmio_write(csc_mode_offset, 0x0, 'gfx_0')

    ##
    # @brief            To get the no of tiles for the current pipe
    # @param[in]        Current pipe
    # @return           tiles per row,tiles per column
    def get_no_of_tiles(self, target_id):

        resolution = self.config.get_current_mode(target_id)
        tiles_per_row = ROUND_UP_DIV(resolution.HzRes, TILE_SIZE)
        tiles_per_col = ROUND_UP_DIV(resolution.VtRes, TILE_SIZE)
        return tiles_per_row, tiles_per_col

    ##
    # @brief check_primary_display - will check if the display is set as primary or not
    # @param[in] port - port_type
    # @return is_primary - True/False
    def check_primary_display(self, port):
        display_config_ = display_config.DisplayConfiguration()
        display_and_adapter_info = display_config_.get_display_and_adapter_info_ex(port, 'gfx_0')
        qdc_info = display_config_.query_display_config(display_and_adapter_info)
        disp_cordinates = qdc_info.sourceModeInfo.position
        is_primary = disp_cordinates.x == 0 and disp_cordinates.y == 0
        return is_primary

    @reboot_helper.__(reboot_helper.teardown)
    def tearDown(self):
        logging.info("Test Clean Up")
        ##
        # Unplug the displays and restore the configuration to the initial configuration
        for display in self.plugged_display:
            logging.debug("Trying to unplug %s", display)
            display_utility.unplug(display)
        ##
        # Disable DFT
        self.mpo.enable_disable_mpo_dft(False, 1)

        ##
        # Disable LACE as part of Test Clean-Up
        for display_index in range(len(self.lfp_target_ids)):
            for index in range(0, 3):
                if driver_escape.als_aggressiveness_level_override(
                        display_and_adapter_info=self.lfp_target_ids[display_index], lux=10,
                        lux_operation=True,
                        aggressiveness_level=index,
                        aggressiveness_operation=True):
                    current_pipe = chr(int(self.lfp_pipe_ids[display_index]) + 65)
                    self.actual_lace_status = get_actual_lace_status(current_pipe)
                    self.expected_lace_status = get_expected_lace_status(50, index)
                    if self.expected_lace_status == self.actual_lace_status:
                        logging.info("Successfully disabled LACE for aggressiveness level %s" %index)
        ##
        # Resetting BKPDisplayLACE reg key
        exec_env = self.utility.get_execution_environment_type()
        reg_args = registry_access.LegacyRegArgs(hkey=registry_access.HKey.LOCAL_MACHINE,
                                                 reg_path=r"SOFTWARE\Intel\Display")

        # Resetting LACE to default version
        if common_utility.write_registry(gfx_index="GFX_0", reg_name="LaceVersion",
                                         reg_datatype=registry_access.RegDataType.DWORD,
                                         reg_value=self.lace1p0_reg_value,
                                         driver_restart_required=True) is False:
            logging.error("Failed to enable default Lace2.0 registry key")
            self.fail("Failed to enable default Lace2.0 registry key")
        else:
            logging.info("Pass: Lace restored back to default Lace2.0 in TearDown")
        logging.info("Registry key add to enable default Lace2.0 is successful")

        if exec_env == 'POST_SI_ENV':
            ##
            # Need to set BKPDisplayLACE Registry Key
            registry_access.write(args=reg_args, reg_name="BKPDisplayLACE", reg_type=registry_access.RegDataType.DWORD,
                                  reg_value=0, sub_key=r"igfxcui\MISC")

            ##
            # If the registry keys to perform INF customization is added as part of the RCR
            # delete the registry keys as part of cleanup
            reg_key_list = ["LaceMinLuxForLowAggressiveness", "LaceMinLuxForModerateAggressiveness", "LaceMinLuxForModerateAggressiveness", "LaceMaxLuxValue"]
            for key_index in range(0, len(reg_key_list)):
                reg_val, reg_type = registry_access.read(args=reg_args, reg_name=reg_key_list[key_index])
                logging.debug(f"BKPDisplayLACE registry value - {reg_val} with type {reg_type}")
                if reg_val is not None:
                    registry_access.delete(args=reg_args, reg_name=reg_key_list[key_index])
                else:
                    logging.debug("No registry key for INF Customization is set")

            status, reboot_required = display_essential.restart_gfx_driver()

        if common_utility.write_registry(gfx_index="GFX_0", reg_name="LaceVersion",
                                         reg_datatype=registry_access.RegDataType.DWORD, reg_value=self.lace1p0_reg_value,
                                         driver_restart_required=True) is False:
            logging.error("Failed to enable default Lace2.0 registry key")
            self.fail("Failed to enable default Lace2.0 registry key")
        else:
            logging.info("Pass: Lace restored back to default Lace2.0 in TearDown")
        logging.info("Registry key add to enable default Lace2.0 is successful")
        super().tearDown()
