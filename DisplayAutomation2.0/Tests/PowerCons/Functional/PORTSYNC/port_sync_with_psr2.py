#######################################################################################################################
# @file         port_sync_with_psr2.py
# @addtogroup   Powercons
# @section      PORTSYNC
# @brief        Test for port sync in symmetric Dual eDP with PSR2,
#
# @author       Bhargav Adigarla
#######################################################################################################################
from Libs.Core.test_env import test_environment
from Libs.Core import app_controls
from Tests.PowerCons.Modules import workload
from Tests.PowerCons.Functional.PSR import psr
from Tests.PowerCons.Functional.PORTSYNC.port_sync_base import *


##
# @brief        This class contains basic port sync tests with PSR2
class PortSyncWithPsr2(PortSyncBase):
    ##
    # @brief        this function verifies port sync with PSR2
    # @return       None
    def t_10_test_port_sync_psr2(self):
        self.verify_basic()

    ##
    # @brief        this function verifies port sync with PSR2
    # @return       None
    def verify_basic(self):
        offsets = psr.get_polling_offsets(psr.UserRequestedFeature.PSR_2)
        for adapter in dut.adapters.values():
            if port_sync.verify(adapter, self.lfp_panels) is True:
                logging.info("\tPort sync programming verification successful")

                if len(self.lfp_panels) == 2:
                    monitors = app_controls.get_enumerated_display_monitors()
                    monitor_ids = [_[0] for _ in monitors]
                    etl_file, polling_data = workload.run(workload.SCREEN_UPDATE, [monitor_ids],
                                                          [offsets, psr.DEFAULT_POLLING_DELAY])

                    if port_sync.verify_vbis(self.lfp_panels, etl_file) is False:
                        self.fail("\tPort sync VBI timing verification Failed")

                    logging.info("\tPort sync functional verification successful")
                    for panel in self.lfp_panels:
                        if panel.psr_caps.is_psr2_supported:
                            if psr.verify(adapter, panel, psr.UserRequestedFeature.PSR_2 , etl_file, polling_data, 'APP',
                                          False) is False:
                                logging.error("\tFAIL: PSR2 verification failed on {0}".format(panel))
                                self.fail("\tPSR verification failed failed with port sync")
                        else:
                            self.fail("\tNon Psr2 panel connected(Planning Issue)")
            else:
                self.fail("\tPort sync verification failed")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.runner.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(PortSyncWithPsr2))
    test_environment.TestEnvironment.cleanup(test_result)