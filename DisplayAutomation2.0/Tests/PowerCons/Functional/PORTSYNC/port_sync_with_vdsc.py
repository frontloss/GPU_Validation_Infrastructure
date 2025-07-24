#######################################################################################################################
# @file         port_sync_with_vdsc.py
# @addtogroup   Powercons
# @section      PORTSYNC
# @brief        Test for port sync in symmetric Dual eDP with VDSC,
#
# @author       Bhargav Adigarla
#######################################################################################################################
from Libs.Core.test_env import test_environment
from Libs.Core import app_controls
from Tests.PowerCons.Modules import workload
from Libs.Feature.vdsc import dsc_verifier
from Tests.PowerCons.Functional.PORTSYNC.port_sync_base import *


##
# @brief        This class contains basic port sync tests with VDSC
class PortSyncWithVdsc(PortSyncBase):

    ##
    # @brief        this function verifies port sync with VDSC
    # @return       None
    def t_10_test_port_sync_vdsc(self):
        self.verify_basic()

    ##
    # @brief        this function verifies port sync with VDSC
    # @return       None
    def verify_basic(self):
        for adapter in dut.adapters.values():
            if port_sync.verify(adapter, self.lfp_panels) is True:
                logging.info("\tPort sync programming verification successful")

                if len(self.lfp_panels) == 2:
                    monitors = app_controls.get_enumerated_display_monitors()
                    monitor_ids = [_[0] for _ in monitors]
                    etl_file, polling_data = workload.run(workload.SCREEN_UPDATE, [monitor_ids])

                    if port_sync.verify_vbis(self.lfp_panels, etl_file) is False:
                        self.fail("\tPort sync VBI timing verification Failed")

                    logging.info("\tPort sync functional verification successful")
                    for panel in self.lfp_panels:
                        if panel.vdsc_caps.is_vdsc_supported:
                            if dsc_verifier.verify_dsc_programming(adapter.gfx_index, panel.port) is False:
                                self.fail("VDSC verification failed with port sync")
                            logging.info("VDSC verification successful with port sync mode")
                        else:
                            self.fail("\tNon VDSC panel connected(Planning Issue)")
            else:
                self.fail("\tPort sync verification failed")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.runner.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(PortSyncWithVdsc))
    test_environment.TestEnvironment.cleanup(test_result)