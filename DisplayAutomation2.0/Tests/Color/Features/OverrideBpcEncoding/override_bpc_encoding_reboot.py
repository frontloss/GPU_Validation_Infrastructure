#################################################################################################
# @file         override_bpc_encoding_reboot.py
# @brief        This is a custom script which can used to display configurations with supported bpc and encoding
#               will perform below functionalities
#               1.To configure bpc and encoding through escape
#               2.To perform register verification for bpc and encoding
#               3.Will perform  reboot event
#               4.Verify the persistence after the event
# @author       Vimalesh D
#################################################################################################
import time

from Libs.Core import reboot_helper
from Tests.Color.Features.OverrideBpcEncoding.override_bpc_encoding_test_base import *


##
# @brief - To perform persistence verification for BPC and Encoding
class OverrideBpcEncodingreboot(OverrideBpcEncodingBase):

   ##
    # @brief Unittest test_before_reboot function - To enable and verify before reboot scenario
    # @param[in] self
    # @return None
    def test_before_reboot(self):

        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active:
                    self.enable_and_verify(adapter.gfx_index,panel.display_and_adapterInfo,panel.pipe,panel.transcoder
                                           ,adapter.platform, adapter.platform_type,port,panel.is_lfp,panel.connector_port_type)

        if reboot_helper.reboot(self, 'test_after_reboot') is False:
            self.fail("Failed to reboot the system")

    ##
    # @brief Unittest test_after_reboot function - To perform register verification after reboot scenario
    # @param[in] self
    # @return None
    def test_after_reboot(self):

        logging.info("Successfully applied power event S5 state")
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active:
                    plane_id = color_etl_utility.get_plane_id(panel.pipe, gfx_index)
                    if verify(adapter.gfx_index, adapter.platform, panel.pipe, plane_id, panel.transcoder,
                              self.panel_props_dict[gfx_index, port].Bpc,self.panel_props_dict[gfx_index,
                                                                                               port].Encoding) is False:
                        self.fail()


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test purpose: Configure the bpc and encoding range and perform verification on all panels")
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('OverrideBpcEncodingreboot'))
    TestEnvironment.cleanup(outcome)

