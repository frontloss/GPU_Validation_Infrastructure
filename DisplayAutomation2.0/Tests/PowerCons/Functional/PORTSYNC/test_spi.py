#######################################################################################################################
# @file         test_spi.py
# @addtogroup   Powercons
# @section      PORTSYNC
# @brief        Test for port sync in symmetric Dual eDP after spi trigger,
#
# @author       Bhargav Adigarla
#######################################################################################################################
import time
from Libs.Core.test_env import test_environment
from Libs.Core import app_controls
from Tests.PowerCons.Modules import workload
from Tests.PowerCons.Functional import pc_external
from Tests.PowerCons.Functional.PORTSYNC.port_sync_base import *


##
# @brief        This class contains basic port sync tests with SPI
class TestSpi(PortSyncBase):

    ##
    # @brief        this function verifies port sync with SPI
    # @return       None
    def t_10_test_basic(self):
        self.verify_basic()
        for adapter in dut.adapters.values():
            for panel in self.lfp_panels:
                # Trigger SPI in IDLE Case
                time.sleep(3)
                logging.info("Triggering SPI in IDLE Case for {}".format(panel))
                if pc_external.trigger_spi(adapter, panel, 1, 1) is False:
                    self.fail("SPI simulation Failed")
                self.verify_basic()

    ##
    # @brief        this function verifies port sync with SPI
    # @return       None
    def verify_basic(self):
        for adapter in dut.adapters.values():
            if port_sync.verify(adapter, self.lfp_panels) is True:
                logging.info("\tPort sync programming verification successful")

                if len(self.lfp_panels) == 2:
                    monitors = app_controls.get_enumerated_display_monitors()
                    monitor_ids = [_[0] for _ in monitors]
                    etl_file, _ = workload.run(workload.SCREEN_UPDATE, [monitor_ids])

                    if port_sync.verify_vbis(self.lfp_panels, etl_file) is False:
                        self.fail("\tPort sync VBI timing verification Failed")

                    logging.info("\tPort sync functional verification successful")
            else:
                self.fail("\tPort sync verification failed")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.runner.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(TestSpi))
    test_environment.TestEnvironment.cleanup(test_result)