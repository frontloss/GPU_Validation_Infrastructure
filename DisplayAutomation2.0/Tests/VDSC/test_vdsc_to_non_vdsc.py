#######################################################################################################################
# @file         test_vdsc_to_non_vdsc.py
# @brief        Test performs VDSC verification for connected VDSC panel and unplug it.Plugs Non VDSC panel to same port
#               and makes sure VDSC is not enabled by the driver and unplugs it.Plugs back the VDSC panel to same port
#               and performs VDSC verification
# @details      Test Scenario:
#               1. Perform vdsc verification for the VDSC panel connected.Unplug if successful
#               2. Plug the non vdsc panel to the same port, and make sure vdsc is not enabled by driver and unplug it
#               3. Plug back vdsc panel to the same port and perform vdsc verification
#               This test can be planned with single vdsc panel with panel index, single port and single non vdsc panel
#               with panel index
#
# @author       Supriya Krishnamurthi
#######################################################################################################################

import logging
import unittest

from Libs.Core import display_utility
from Libs.Core.test_env import test_environment
from Libs.Feature.vdsc import dsc_verifier
from Libs.Feature.vdsc.dsc_helper import DSCHelper
from Tests.PowerCons.Modules import common
from Tests.VDSC.vdsc_base import VdscBase


##
# @brief        This class contains a test function which implements the mentioned test scenario / test steps.
class TestVdscToNonVdsc(VdscBase):
    vdsc_panel_plugged_gfx_index = vdsc_panel_plugged_port = ''

    ##
    # @brief        This method verifies if single vdsc display is connected and performs VDSC Verification for it.If
    #               successful, vdsc panel is unplugged from the port
    # @return       None
    # @cond
    @common.configure_test(critical=True)
    # @endcond
    def t_11_verify_vdsc_panel(self) -> None:

        if len(VdscBase.vdsc_panels) != 1:
            self.fail("[Planning Issue] - Only single display should be connected")

        # fetching port name, gfx_index to which vdsc panel is connected and save them in class variable
        [(gfx_index, port)] = VdscBase.vdsc_panels[0].items()
        TestVdscToNonVdsc.vdsc_panel_plugged_gfx_index = gfx_index
        TestVdscToNonVdsc.vdsc_panel_plugged_port = port

        is_success = VdscBase._display_config.set_display_configuration_ex(self.topology, [port])
        self.assertTrue(is_success, "Failed to apply display configuration")

        r_status = dsc_verifier.verify_dsc_programming(gfx_index, port)
        self.assertTrue(r_status, "VDSC verification at {} on {} Expected = PASS Actual = FAIL".format(port, gfx_index))

        logging.info("VDSC verification at {} on {} Expected = PASS Actual = PASS".format(port, gfx_index))

        r_status = display_utility.unplug(port, gfx_index=gfx_index)
        self.assertTrue(r_status, "Failed to unplug display at {} on {}".format(port, gfx_index))

    ##
    # @brief        This method plugs the non vdsc panel supplied through custom argument to the same port used before
    #               and checks if vdsc is supported for that panel by the driver.VDSC should not be supported for
    #               non vdsc panel.If supported, fail the test, else unplug the display
    # @return       None
    # @cond
    @common.configure_test(critical=True)
    # @endcond
    def t_12_plug_and_verify_nonvdsc_panel(self) -> None:
        # port name, gfx_index to which vdsc panel is connected
        gfx_index, port = TestVdscToNonVdsc.vdsc_panel_plugged_gfx_index, TestVdscToNonVdsc.vdsc_panel_plugged_port

        # Single Panel_index should be passed for custom tag
        non_vdsc_details = VdscBase.get_cmd_line_param_values(field='NON_VDSC')
        self.assertEqual(len(non_vdsc_details), 1, "[Planning Issue] - Single Panel Index should be passed")

        # fetching panel_index of non vdsc panel
        non_vdsc_panel_index = non_vdsc_details[0].upper().replace('SINK_', '')

        # plug non-vdsc panel to the same port on same adapter to which vdsc panel was connected
        r_status = display_utility.plug(port=port, panelindex=non_vdsc_panel_index, gfx_index=gfx_index)
        self.assertTrue(r_status, "Failed to plug NON VDSC display at {} on {}".format(port, gfx_index))

        logging.info("Plugged NON VDSC display at {} on {}: {}".format(port, gfx_index, non_vdsc_panel_index))

        # making display active
        is_success = VdscBase._display_config.set_display_configuration_ex(self.topology, [port])
        self.assertTrue(is_success, "Failed to apply display configuration")

        enumerated_displays = VdscBase._display_config.get_enumerated_display_info()
        target_id = VdscBase._display_config.get_target_id(port, enumerated_displays)
        self.assertNotEqual(target_id, 0, "[Test Issue] - Target ID for {0} is 0 ".format(port))

        # update vdsc, nonvdsc panel and target info
        VdscBase.update_vdsc_panel_target_info(gfx_index, port, target_id)

        # Make sure VDSC is disabled for non-vdsc panel
        r_status = DSCHelper.is_vdsc_enabled_in_driver(gfx_index, port)
        self.assertFalse(r_status, "VDSC Engine status in driver for Non-VDSC/Non-FEC panel at {} on {} Expected: "
                                   "Disabled Actual: Enabled".format(port, gfx_index))

        logging.info("VDSC Engine status in driver for Non-VDSC/Non-FEC panel at {} on {} Expected: Disabled Actual: "
                     "Disabled".format(port, gfx_index))

        # Make sure FEC is disabled for non-vdsc panel
        r_status = DSCHelper.get_fec_status_ex(gfx_index, port)
        self.assertFalse(r_status, "FEC status in driver for Non-VDSC/Non-FEC panel at {} on {} Expected: Disabled "
                                   "Actual: Enabled".format(port, gfx_index))

        logging.info("FEC status in driver for Non-VDSC/Non-FEC panel at {} on {} Expected: Disabled Actual: "
                     "Disabled".format(port, gfx_index))

        r_status = display_utility.unplug(port, gfx_index=gfx_index)
        self.assertTrue(r_status, "Failed to unplug NON VDSC display at {} on {}".format(port, gfx_index))

        logging.info("Unplugged NON VDSC display {}: {}".format(port, non_vdsc_panel_index))

    ##
    # @brief        This method plugs back the vdsc panel to the same port and performs vdsc verification
    # @return       None
    def t_13_plug_back_and_verify_vdsc_panel(self) -> None:
        # port name, gfx_index to which vdsc panel is connected
        gfx_index, port = TestVdscToNonVdsc.vdsc_panel_plugged_gfx_index, TestVdscToNonVdsc.vdsc_panel_plugged_port

        # fetching panel_index of vdsc panel
        vdsc_dp_panel_index = VdscBase.get_cmd_line_param_values(field='panel_index', gfx_index=gfx_index, port=port)
        self.assertNotEqual(vdsc_dp_panel_index, None, "[Planning Issue] - Single Panel Index should be passed")

        # Plug back vdsc panel on same port and same adapter
        r_status = display_utility.plug(port=port, panelindex=vdsc_dp_panel_index, gfx_index=gfx_index)
        self.assertTrue(r_status, "Failed to plug VDSC display at {} on {}".format(port, gfx_index))

        logging.info("Plugged VDSC display at {}: {}".format(port, vdsc_dp_panel_index))

        # making display active
        is_success = VdscBase._display_config.set_display_configuration_ex(self.topology, [port])
        self.assertTrue(is_success, "Failed to apply display configuration")

        enumerated_displays = VdscBase._display_config.get_enumerated_display_info()
        target_id = VdscBase._display_config.get_target_id(port, enumerated_displays)
        self.assertNotEqual(target_id, 0, "[Test Issue] - Target ID for {0} is 0 ".format(port))

        # update vdsc, nonvdsc panel and target info
        VdscBase.update_vdsc_panel_target_info(gfx_index, port, target_id)

        r_status = dsc_verifier.verify_dsc_programming(gfx_index, port)
        self.assertTrue(r_status, "VDSC verification at {} on {} Expected = PASS Actual = FAIL".format(port, gfx_index))

        logging.info("VDSC verification at {} on {} Expected = PASS Actual = PASS".format(port, gfx_index))


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(TestVdscToNonVdsc))
    test_environment.TestEnvironment.cleanup(test_result)
