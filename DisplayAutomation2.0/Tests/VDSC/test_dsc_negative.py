########################################################################################################################
# @file         test_dsc_negative.py
# @brief        This file will contain all the negative test cases related to VDSC feature.
#
# @author       Rabbani Syed, Goutham N
########################################################################################################################
import logging
import unittest

from Libs.Core import display_utility, enum
from Libs.Core.test_env import test_environment
from Libs.Core.logger import gdhm
from Libs.Feature.vdsc.dsc_helper import DSCHelper
from Tests.PowerCons.Modules import common
from Tests.VDSC.vdsc_base import VdscBase


##
# @brief        This class contains a test function which implements the mentioned test scenario / test steps.
class TestDscNegative(VdscBase):

    ##
    # @brief    This test method is overridden from VDSC base class.
    #           In the base class this method will set display configuration to all the active displays.
    #           It is a negative test we expect a successful modeset with FEC disabled when FEC_DECODE_EN_DETECTED/FEC_RUNNING_INDICATOR
    #           register is 0x0 in case of SST and mode set to fail in case of MST
    #           This method will not set display configuration and helps to identify VDSC displays.
    # @return   None
    # @cond
    @common.configure_test(critical=True)
    # @endcond
    def t_01_update_panel_info(self) -> None:
        enumerated_displays = VdscBase._display_config.get_enumerated_display_info()
        self.assertIsNotNone(enumerated_displays, "[Test Issue] - API get_enumerated_display_info() FAILED")

        for adapter_display_dict in VdscBase.cmd_line_displays:
            # Each dictionary inside vdsc_panel list will be of length 1, hence iterating over it is not needed
            [(gfx_index, port)] = adapter_display_dict.items()

            target_id = VdscBase._display_config.get_target_id(port, enumerated_displays)
            self.assertNotEqual(target_id, 0, "[Test Issue] - Target ID for {0} is 0 ".format(port))

            if display_utility.get_vbt_panel_type(port, gfx_index) == display_utility.VbtPanelType.LFP_DP:
                VdscBase.edp_panels.append({gfx_index: port})
                VdscBase.update_vdsc_panel_target_info(gfx_index, port, target_id, panel_filter="EDP")
            else:
                VdscBase.external_panels.append({gfx_index: port})
                VdscBase.update_vdsc_panel_target_info(gfx_index, port, target_id)

        logging.info('VDSC Supported Panels: {}'.format(VdscBase.vdsc_target_ids))

    ##
    # @brief        This test checks if the modeset is successful with FEC disabled if the sink doesn’t set
    #               the FEC_DECODE_EN_DETECTED/FEC_RUNNING_INDICATOR bit for SST displays.
    #               This test checks if the modeset fails if the sink doesn’t set
    #               the FEC_DECODE_EN_DETECTED/FEC_RUNNING_INDICATOR bit for MST displays.
    # @details      Test Scenario:
    #               1. Applies the mode set to the DP VDSC panel.
    #               2. In case of SST display, checks if the modeset is successful and verifies if FEC & DSC are disabled
    #                  when the FEC_DECODE_EN_DETECTED/FEC_RUNNING_INDICATOR is not set by the DPRX device.
    #                  In case of MST display, checks if modeset fails when FEC_DECODE_EN_DETECTED/FEC_RUNNING_INDICATOR
    #                  is not set by DPRX device.
    #               This test should be planned with DP VDSC displays.
    # @return       None
    # @cond
    @common.configure_test(selective=["FEC_STATUS"])
    # @endcond
    def t_11_fec_status(self) -> None:

        # Each dictionary inside vdsc_panel list will be of length 1, hence iterating over it is not needed
        [(gfx_index, port)] = VdscBase.vdsc_panels[0].items()

        logging.info(f'Applying Display Config at port: {port}')
        is_success = VdscBase._display_config.set_display_configuration_ex(enum.SINGLE, [port])

        # As of now, driver won't allow FEC/DSC fallbacks for MST case.
        # Hence, we expect modeset to fail.
        if VdscBase.get_cmd_line_param_values('PLUG_TOPOLOGIES') != 'NONE':
            self.assertFalse(is_success, "[Driver issue] - Mode set passed with FEC_RUNNING_INDICATOR bit set as 0x0")

        # SST case
        else:
            self.assertTrue(is_success, "[Driver issue] - Mode set failed")

            is_fec_dsc_disabled = DSCHelper.is_fec_dsc_disabled(gfx_index, port)

            if not is_fec_dsc_disabled:
                self.assertTrue(is_fec_dsc_disabled, "[Driver issue] - FEC negative verification failed!")
                gdhm.report_driver_bug_di(f"FEC negative verification failed")

            logging.info(f"Pass: FEC & VDSC is not Enabled when the sink hasn't set FEC_DECODE_EN_DETECTED bit for port {port}")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(TestDscNegative))
    test_environment.TestEnvironment.cleanup(test_result)
