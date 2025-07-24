#################################################################################################################
# @file         lrr_power_source.py
# @brief        Contains LRR power source tests
#
# @author       Rohit Kumar
#################################################################################################################
from Libs.Core import display_power
from Libs.Core.display_config import display_config
from Libs.Core.test_env import test_environment

from Tests.PowerCons.Functional.LRR.lrr_base import *
from Tests.PowerCons.Functional.PSR import psr
from Tests.PowerCons.Modules import workload


##
# @brief        Contains LRR power source tests
class LrrPowerSourceTest(LrrBase):
    display_config_ = display_config.DisplayConfiguration()
    display_power_ = display_power.DisplayPower()

    ##
    # @brief        Test function for LRR verification after power source switch
    # @return       None
    # @cond
    @common.configure_test(repeat=True)
    # @endcond
    def t_11_power_source(self):
        status = True

        def _verify(adapter_):
            test_status = True

            for panel in adapter_.panels.values():
                if self.method == Method.IDLE:
                    etl_file, polling_data = workload.run(
                        workload.IDLE_DESKTOP,
                        [self.duration_in_seconds],
                        [psr.get_polling_offsets(psr.UserRequestedFeature.PSR_2), self.polling_delay_in_seconds]
                    )
                else:
                    etl_file, polling_data = workload.run(
                        workload.VIDEO_PLAYBACK_USING_FILE,
                        [self.video_file, self.duration_in_seconds, False],
                        [psr.get_polling_offsets(psr.UserRequestedFeature.PSR_2), self.polling_delay_in_seconds]
                    )
                test_status &= lrr.verify(
                    adapter_, panel, etl_file, polling_data, self.method, self.rr_switching_method, video=self.video_file)

            return test_status

        for adapter in dut.adapters.values():
            status &= _verify(adapter)

        if status is False:
            self.fail("FAIL: LRR verification in DC mode")
        logging.info("PASS: LRR verification in DC mode")

        if workload.change_power_source(PowerSource.AC_MODE) is False:
            self.fail("FAILED to switch power line status to AC mode (Test Issue)")

        for adapter in dut.adapters.values():
            status &= _verify(adapter)

        if status is False:
            self.fail("FAIL: LRR verification in AC mode")
        logging.info("PASS: LRR verification in AC mode")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(LrrPowerSourceTest))
    test_environment.TestEnvironment.cleanup(test_result)
