#######################################################################################################################
# @file         test_lt_params.py
# @addtogroup   Powercons
# @section      PORTSYNC
# @brief        Test for port sync in symmetric Dual eDP and verify link training params,
#
# @author       Bhargav Adigarla
#######################################################################################################################
from Libs.Core.test_env import test_environment
from Libs.Core import app_controls
from Tests.PowerCons.Modules import workload, dpcd
from Tests.PowerCons.Functional.PORTSYNC.port_sync_base import *


##
# @brief        This class contains basic tests to check link training params
class TestLtParams(PortSyncBase):
    ##
    # @brief        this function verifies port sync link training params
    # @return       None
    def t_10_test_lt_params(self):
        self.verify_basic()

    ##
    # @brief        this function verifies port sync link training params
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
                    lfp0_link_rate = dpcd.get_link_rate(self.lfp_panels[0].target_id, True)
                    lfp1_link_rate = dpcd.get_link_rate(self.lfp_panels[1].target_id, True)
                    logging.info(f"lfp0 linkrate {lfp0_link_rate}  lfp1 linkrate{lfp1_link_rate}")

                    lfp0_lane_count = dpcd.LaneCountSet(self.lfp_panels[0].target_id)
                    lfp1_lane_count = dpcd.LaneCountSet(self.lfp_panels[1].target_id)
                    logging.info(f"lfp0 lane count {lfp0_lane_count.lane_count_set}  lfp1 lane count{lfp1_lane_count.lane_count_set}")

                    if lfp0_link_rate == lfp1_link_rate and lfp0_lane_count.lane_count_set == lfp1_lane_count.lane_count_set:
                        logging.info("\tLink training params verification successful")
                    else:
                        self.fail("\tLink training params verification failed")
            else:
                self.fail("\tPort sync verification failed")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.runner.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(TestLtParams))
    test_environment.TestEnvironment.cleanup(test_result)