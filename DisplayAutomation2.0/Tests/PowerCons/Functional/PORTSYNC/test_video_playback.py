#######################################################################################################################
# @file         test_video_playback.py
# @addtogroup   Powercons
# @section      PORTSYNC
# @brief        Test for port sync in symmetric Dual eDP with 24fps video playback,
#
# @author       Bhargav Adigarla
#######################################################################################################################
from Libs.Core.test_env import test_environment
from Libs.Core import app_controls
from Tests.PowerCons.Modules import workload
from Tests.PowerCons.Functional.PORTSYNC.port_sync_base import *


##
# @brief        This class contains basic port sync tests with video playback
class TestBasic(PortSyncBase):

    ##
    # @brief        this function verifies port sync with video playback
    # @return       None
    def t_10_test_video_playback(self):
        self.verify_basic()

    ##
    # @brief        this function verifies port sync with video playback
    # @return       None
    def verify_basic(self):
        for adapter in dut.adapters.values():
            if port_sync.verify(adapter, self.lfp_panels) is True:
                logging.info("\tPort sync programming verification successful")

                if len(self.lfp_panels) == 2:
                    monitors = app_controls.get_enumerated_display_monitors()
                    monitor_ids = [_[0] for _ in monitors]
                    etl_file, _ = workload.run(workload.VIDEO_PLAYBACK, [24, 60])

                    if port_sync.verify_vbis(self.lfp_panels, etl_file) is False:
                        self.fail("\tPort sync VBI timing verification Failed")

                    logging.info("\tPort sync functional verification successful")
            else:
                self.fail("\tPort sync verification failed")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.runner.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(TestBasic))
    test_environment.TestEnvironment.cleanup(test_result)