#################################################################################################
# @file         lace_base.py
# @brief        This scripts comprises of below functions.
#               1.setUp() -  To apply the display config and update the feature caps based on panel capabilities
#               2.enable_and_verify() - To Configure and verify functionality
# @author       Vimalesh D, Pooja Audichya
#################################################################################################
import time
import logging
import sys
from Libs.Core.wrapper import control_api_args
from Libs.Core.test_env import test_context
from Libs.Core import registry_access, display_essential, driver_escape
from Libs.Feature.powercons import registry
from Libs.Core.display_config import display_config
from DisplayRegs.DisplayArgs import TranscoderType
from Tests.test_base import TestBase
from Tests.Color.Common import color_escapes, common_utility, color_enums, color_igcl_escapes
from Tests.Color.Common.color_escapes import get_bpc_encoding, set_bpc_encoding
from Tests.Color.Verification import gen_verify_pipe, feature_basic_verify
from Libs.Core.logger import gdhm
from Libs.Core.machine_info.machine_info import SystemInfo

##
# @brief get_action_type
# @param[in] None
# @return argument value
def get_action_type():
    tag_list = [custom_tag.strip().upper() for custom_tag in sys.argv]
    if '-SCENARIO' in tag_list:
        for i in range(0, len(tag_list)):
            if tag_list[i] == '-SCENARIO':
                if str(tag_list[i + 1]).startswith("-") is False:
                    return sys.argv[i + 1]
    else:
        assert False, "Wrong Commandline!! Usage: Test_name.py -SCENARIO SCENARIO_NAME -SAMPLING SAMPLING_TYPE"


class LACEBase(TestBase):
    scenario = None
    aggrpercent = None
    triggerType = None
    setoperation = None
    enable_regkey_dithering = False
    lace1p0_status = None
    lace1p0_reg_value = None

    ##
    # @brief Unittest Setup function
    # @param[in] self
    # @return None
    def setUp(self):

        self.custom_tags["-AGGRPERCENT"] = None
        self.custom_tags["-TRIGGERTYPE"] = None
        self.custom_tags["-SETOPERATION"] = None
        self.custom_tags['-ENABLE_REGKEY_DITHERING'] = False
        super().setUp()
        self.scenario = str(self.context_args.test.cmd_params.test_custom_tags["-SCENARIO"][0])
        self.aggrpercent = int(self.context_args.test.cmd_params.test_custom_tags["-AGGRPERCENT"][0])
        self.triggerType = str(self.context_args.test.cmd_params.test_custom_tags["-TRIGGERTYPE"][0])
        self.setOperation = str(self.context_args.test.cmd_params.test_custom_tags["-SETOPERATION"][0])
        if len(self.context_args.test.cmd_params.test_custom_tags["-ENABLE_REGKEY_DITHERING"][0]) > 1:
            self.enable_regkey_dithering = bool(self.context_args.test.cmd_params.test_custom_tags["-ENABLE_REGKEY_DITHERING"][0])
        else:
            self.enable_regkey_dithering = False

        # HSD-18023973505- Handle condition to disable the HDR, if enabled in previous test or job
        logging.info("Verify the HDR Regkey status before configuring Lace")

        if self.enable_regkey_dithering:
            for gfx_index, adapter in self.context_args.adapters.items():
                reg_args = registry_access.StateSeparationRegArgs(gfx_index=gfx_index)

                key_name = "ForceDitheringEnable"
                value = 1
                if registry_access.write(args=reg_args, reg_name=key_name, reg_type=registry_access.RegDataType.DWORD,
                                         reg_value=value) is False:
                    self.fail("Registry key add to enable SelectBPC  failed")
                logging.info(" ForceDitheringEnable set to 1 on GFX_{0}".format(gfx_index))
                ##
                # restart display driver for regkey to take effect.
                status, reboot_required = common_utility.restart_display_driver(gfx_index)
                if status is False:
                    self.fail('Fail: Failed to Restart Display driver')


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

        #Enable Lace1.0 coverage for ARL
        self.lace1p0_status, self.lace1p0_reg_value = common_utility.read_registry(gfx_index="GFX_0",
                                                                                   reg_name="LaceVersion")
        if SystemInfo().get_sku_name('gfx_0') == 'ARL':
            if common_utility.write_registry(gfx_index="GFX_0", reg_name="LaceVersion",
                                             reg_datatype=registry_access.RegDataType.DWORD, reg_value=10,
                                             driver_restart_required=True) is False:
                logging.error("Failed to enable Lace1.0 registry key")
                self.fail("Failed to enable Lace1.0 registry key")
            logging.info("Registry key add to enable Lace1.0 is successful")
        else:
            logging.info("Lace1.0 Registry Key is either not present or not enabled")

        # Verify FeatureTestControl
        for gfx_index, adapter in self.context_args.adapters.items():
            feature_test_control = registry.FeatureTestControl(adapter.gfx_index)
            if feature_test_control.lace_disable:
                gdhm.report_driver_bug_os("Lace feature was not enabled as part of "
                                        "FeatureTestControl on adapter: {0} platform: {1}"
                                        .format(adapter.gfx_index, adapter.platform))
                self.fail("Lace feature was not enabled")

    ##
    # @brief         Wrapper to - configure lace and verify the register for lace function enable/disable and IE bit
    # @param[in]     trigger_type - Ambient mode or aggressiveness percent
    # @return        True on Success ,False on Failure.
    def enable_and_verify(self, gfx_index, platform, pipe, display_and_adapterInfo, panel, configure_lace):

        if panel.is_active and panel.is_lfp:
            if color_igcl_escapes.get_power_caps(panel.target_id,
                                                 control_api_args.ctl_power_optimization_flags_v.LACE.value):
                if color_igcl_escapes.get_lace_config(0, display_and_adapterInfo):
                    time.sleep(1)

                if configure_lace:
                    # enable lace
                    if color_igcl_escapes.set_lace_config(self.triggerType, self.setOperation, 100, display_and_adapterInfo):
                        time.sleep(2)

                    if feature_basic_verify.verify_lace_feature(gfx_index, platform, pipe, configure_lace, "LEGACY") \
                            is False:
                        self.fail("Lace verification failed")
                    if self.enable_regkey_dithering:
                        if feature_basic_verify.verify_dithering_feature(gfx_index, platform, panel.pipe, panel.transcoder,
                                                                         True) is False:
                            self.fail()
                    return True
                else:
                    # disable lace
                    if color_igcl_escapes.set_lace_config(self.triggerType, 1, 0, display_and_adapterInfo):
                        time.sleep(2)
                    # Currently there was a bug with lace Disable - Where IE Bit is not getting disabled when
                    # tried to disable Lace. HSD-16020217639- Post bug fix, need to uncomment the verification.

                    if feature_basic_verify.verify_lace_feature(gfx_index, platform, pipe, configure_lace, "LEGACY") \
                            is False:
                        self.fail("Lace verification failed")
                    if self.enable_regkey_dithering:
                        if feature_basic_verify.verify_dithering_feature(gfx_index, platform, panel.pipe,
                                                                         panel.transcoder,
                                                                         True) is False:
                            self.fail()
                    return True

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

    def tearDown(self):
        # Disable lace in teardown.
        for gfx_index, adapter in self.context_args.adapters.items():
            if self.enable_regkey_dithering:
                if common_utility.write_registry(gfx_index=gfx_index, reg_name="ForceDitheringEnable",
                                                 reg_datatype=registry_access.RegDataType.DWORD, reg_value=0,
                                                 driver_restart_required=True) is False:
                    logging.error("Failed to enable ForceDitheringEnable registry key")
                    self.fail("Failed to disable ForceDitheringEnable registry key")
                logging.info("Registry key add to disable ForceDitheringEnable is successful")

            for port, panel in adapter.panels.items():
                if panel.is_active and panel.is_lfp:
                    if color_igcl_escapes.get_lace_config(2, panel.display_and_adapterInfo):
                        time.sleep(1)
                    self.triggerType = control_api_args.ctl_lace_operation_mode_type_v.CTL_LACE_TRIGGER_FLAG_AMBIENT_LIGHT
                    if color_igcl_escapes.set_lace_config(self.triggerType,1,0,panel.display_and_adapterInfo):
                        time.sleep(2)
                        if driver_escape.als_aggressiveness_level_override(
                                display_and_adapter_info=panel.target_id, lux=0,
                                lux_operation=True,
                                aggressiveness_level=0,
                                aggressiveness_operation=False):
                            logging.info("Successfully disabled LACE")
                            time.sleep(2)
                            if feature_basic_verify.verify_lace_feature(gfx_index, adapter.platform, panel.pipe, False, "LEGACY") is False:
                                self.fail("Lace verification failed")
                    else:
                        self.fail("Failed to set Lace config to restore default")
                    logging.info("Pass: Lace restored back to default in TearDown")

        if common_utility.write_registry(gfx_index="GFX_0", reg_name="LaceVersion",
                                         reg_datatype=registry_access.RegDataType.DWORD, reg_value=self.lace1p0_reg_value,
                                         driver_restart_required=True) is False:
            logging.error("Failed to enable default Lace2.0 registry key")
            self.fail("Failed to enable default Lace2.0 registry key")
        else:
            logging.info("Pass: Lace restored back to default Lace2.0 in TearDown")
        logging.info("Registry key add to enable default Lace2.0 is successful")

        super().tearDown()
