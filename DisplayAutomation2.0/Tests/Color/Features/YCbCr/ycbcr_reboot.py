#################################################################################################
# @file         ycbcr_reboot.py
# @brief        This scripts comprises of Test_before_reboot() and test_after_reboot ()
#               and will perform below functionalities
#               1.enable/disable ycbcr feature
#               2.To perform register verification OCSC,Coeff,Pre/post off and quantisation range
#               3.Will do restart display driver and reboot event
#               4.Verify the persistence after the event
# @author       Vimalesh D
#################################################################################################
import unittest
from Libs.Core import reboot_helper
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Color.Features.YCbCr.ycbcr_test_base import *

##
# @brief - To perform persistence verification for ycbcr reboot scenario
class YcbcrReboot(YcbcrBase):

    ##
    # @brief Unittest test_before_reboot function - To enable and verify before reboot scenario
    # @param[in] self
    # @return None
    def test_before_reboot(self):
        self.enable_and_verify()
        if reboot_helper.reboot(self, 'test_after_reboot') is False:
            self.fail("Failed to reboot system")

    ##
    # @brief Unittest test_after_reboot function - To perform register verification after reboot scenario
    # @param[in] self
    # @return None
    def test_after_reboot(self):
        logging.info("successfully applied power event S5 state")
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                update_ycbcr_caps_in_context(panel.connector_port_type, panel.display_and_adapterInfo,
                                             self.context_args.adapters[gfx_index].panels[port])
                if panel.FeatureCaps.YCbCrSupport and panel.is_active and panel.is_lfp is False:
                    plane_id = color_etl_utility.get_plane_id(panel.pipe, gfx_index)
                    if verify(port, adapter.platform, panel.display_and_adapterInfo, panel.pipe, plane_id,
                              panel.transcoder, self.sampling, True):
                        logging.info(
                            "Pass: Register verification for YCbCr for panel {0} on {1} passed ".format(
                            panel.connector_port_type, adapter.gfx_index))
                    else:
                        self.fail("Register verification for YCbCr panel {0} on {1} failed".format
                                  (panel.connector_port_type, adapter.gfx_index))

if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('YcbcrReboot'))
    TestEnvironment.cleanup(outcome)
