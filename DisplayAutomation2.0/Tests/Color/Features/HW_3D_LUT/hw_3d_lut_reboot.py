#################################################################################################
# @file         hw_3d_lut_reboot.py
# @brief        This scripts comprises of test reboot scenario for hw3dlut, will perform below functionalities
#               1.To configure 3dlut for the display
#               2.To perform register verification for 3dlut ctl and data offsets
#               3.Will perform  reboot_event()
#               4.Verify the persistence after the event
# @author       Vimalesh D
#################################################################################################

import sys
from Libs.Core import reboot_helper
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Color.Features.HW_3D_LUT.hw_3d_lut_base import *


##
# @brief - Hw3DLut reboot test
class Hw3DLutReboot(Hw3DLUTBase):

    ##
    # @brief Unittest test_before_reboot function - To enable and verify before reboot scenario
    # @param[in] self
    # @return None
    def test_before_reboot(self):

        # Enable Hw3DLut feature in all supported panels and verify
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active:
                    if adapter.platform in ('TGL', 'DG1', 'RKL'):
                        if self.enable_and_verify(adapter.gfx_index, panel.connector_port_type, adapter.platform,
                                                  panel.pipe, panel.is_lfp,panel.transcoder,panel.display_and_adapterInfo, panel.target_id,
                                                  configure_dpp_hw_lut=True) is False:
                            self.fail()
                    else:
                        if self.enable_and_verify_via_igcl(adapter, panel, True) is False:
                            self.fail()

        if reboot_helper.reboot(self, 'test_after_reboot', {'three_dlut_enable_pipe':self.three_dlut_enable_pipe}) is False:
            self.fail("Failed to reboot the system")

    ##
    # @brief Unittest test_after_reboot function - To perform register verification after reboot scenario
    # @param[in] self
    # @return None
    def test_after_reboot(self):
        data = reboot_helper._get_reboot_data()
        if data is not None:
            self.three_dlut_enable_pipe = data['three_dlut_enable_pipe']
        logging.info("Successfully applied power event S5 state")

        ##
        # HW3DLUT should persist after reboot scenario in case if test is using IGCL API to enable 3DLUT. in case of
        # driver escape it should not persist
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active and panel.pipe in self.three_dlut_enable_pipe:
                    logging.info("Verifying 3DLUT support after system reboot for panel connected to port {0} pipe {1} on adapter {2}"
                                  .format(panel.connector_port_type, panel.pipe, adapter.gfx_index))
                    if adapter.platform in ('TGL', 'DG1', 'RKL'):
                        logging.info("Started 3DLUT verification for enabled pipe {0} available in the list".format(
                            panel.pipe))
                        if hw_3dlut.verify(adapter.gfx_index, adapter.platform, panel.connector_port_type, panel.pipe,
                                           panel.transcoder, panel.target_id, self.inputfile, panel.is_lfp,
                                           enable=False, via_igcl=False) is False:
                            logging.error(
                                "Verification failed for 3DLUT support after RESTART_DRIVER for panel connected to port {0} pipe {1} on adapter {2}"
                                .format(panel.connector_port_type, panel.pipe, adapter.gfx_index))
                            self.fail()
                    else:
                        if hw_3dlut.verify(adapter.gfx_index, adapter.platform, panel.connector_port_type,
                                           panel.pipe, panel.transcoder, panel.target_id, self.inputfile, panel.is_lfp,
                                           enable=True, via_igcl=True) is False:
                            logging.error(
                                "Verification failed for 3DLUT support via IGCL after RESTART_DRIVER for panel connected to port {0} pipe {1} on adapter {2}"
                                .format(panel.connector_port_type, panel.pipe, adapter.gfx_index))
                            self.fail()
                
                else:
                    logging.info("Skipping the 3DLUT verification, since pipe {0} is not in the enabled list".format(
                        panel.pipe))
                    

if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test purpose: To apply both SINGLE or CLONE display configuration and apply and verify 3dlut")
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('Hw3DLutReboot'))
    TestEnvironment.cleanup(outcome)
