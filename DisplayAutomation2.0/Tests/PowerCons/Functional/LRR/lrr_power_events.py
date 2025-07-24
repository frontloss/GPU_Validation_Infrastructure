#################################################################################################################
# @file         lrr_power_events.py
# @brief        Contains LRR power events tests
#
# @author       Rohit Kumar
#################################################################################################################
from Libs.Core import display_power, enum
from Libs.Core.display_config import display_config
from Libs.Core.test_env import test_environment

from Tests.PowerCons.Functional.LRR.lrr_base import *
from Tests.PowerCons.Functional.PSR import psr
from Tests.PowerCons.Modules import workload


##
# @brief        Contains LRR tests before/after power events
class LrrPowerEventsTest(LrrBase):
    display_config_ = display_config.DisplayConfiguration()
    display_power_ = display_power.DisplayPower()

    ##
    # @brief        Helper function containing the verification steps for LRR
    # @return       None
    def _verification_steps(self):
        test_status = True
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if self.method == Method.IDLE:
                    etl_file, polling_data = workload.run(
                        workload.IDLE_DESKTOP,
                        [self.duration_in_seconds],
                        [psr.get_polling_offsets(psr.UserRequestedFeature.PSR_2), self.polling_delay_in_seconds])
                else:
                    etl_file, polling_data = workload.run(
                        workload.VIDEO_PLAYBACK_USING_FILE,
                        [self.video_file, self.duration_in_seconds, False],
                        [psr.get_polling_offsets(psr.UserRequestedFeature.PSR_2), self.polling_delay_in_seconds]
                    )

                test_status &= lrr.verify(
                    adapter, panel, etl_file, polling_data, self.method, self.rr_switching_method, video=self.video_file)

        return test_status

    ##
    # @brief        Test function for LRR verification after S3 operation
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["S3"])
    # @endcond
    def t_11_s3(self):
        if self.display_power_.is_power_state_supported(display_power.PowerEvent.S3) is False:
            self.fail("Power Event (S3) test scheduled on CS enabled system. Needed Non-CS system")

        if self._verification_steps() is False:
            self.fail("FAIL: LRR verification before Power Event (S3)")
        logging.info("PASS: LRR verification before Power Event (S3)")

        if self.display_power_.invoke_power_event(display_power.PowerEvent.S3, common.POWER_EVENT_DURATION_DEFAULT) is False:
            self.fail('FAILED to invoke Power Event (S3)')
        logging.info("Successfully invoked from Power Event (S3)")

        count = int(self.cmd_line_param[0]['COUNT'][0]) if self.cmd_line_param[0]['COUNT'] != 'NONE' else 1

        test_status = True
        for iteration in range(0, count):
            if self._verification_steps() is False:
                test_status &= False
                logging.error(f"LRR verification after Power Event (S3) in iteration #{iteration}")
            logging.info(f"LRR verification after Power Event (S3) in iteration #{iteration}")

        if test_status is False:
            self.fail("FAIL: LRR verification after Power Event (S3)")
        logging.info("PASS: LRR verification after Power Event (S3)")

    ##
    # @brief        Test function for LRR verification after CS operation
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["CS"])
    # @endcond
    def t_12_cs(self):
        if self.display_power_.is_power_state_supported(display_power.PowerEvent.CS) is False:
            self.fail("Power Event (CS) test scheduled on Non-CS system. Needed CS enabled system")

        if self._verification_steps() is False:
            self.fail("FAIL: LRR verification before Power Event (CS)")
        logging.info("PASS: LRR verification before Power Event (CS)")

        if self.display_power_.invoke_power_event(display_power.PowerEvent.CS, common.POWER_EVENT_DURATION_DEFAULT) is False:
            self.fail('FAILED to invoke Power Event (CS)')
        logging.info("Successfully invoked from Power Event (CS)")

        count = int(self.cmd_line_param[0]['COUNT'][0]) if self.cmd_line_param[0]['COUNT'] != 'NONE' else 1

        test_status = True
        for iteration in range(0, count):
            if self._verification_steps() is False:
                test_status &= False
                logging.error(f"LRR verification after Power Event (CS) in iteration #{iteration}")
            logging.info(f"LRR verification after Power Event (CS) in iteration #{iteration}")

        if test_status is False:
            self.fail("FAIL: LRR verification after Power Event (CS)")
        logging.info("PASS: LRR verification after Power Event (CS)")

    ##
    # @brief        Test function for LRR verification after S4 operation
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["S4"])
    # @endcond
    def t_13_s4(self):
        if self._verification_steps() is False:
            self.fail("FAIL: LRR verification before Power Event (S4)")
        logging.info("PASS: LRR verification before Power Event (S4)")

        if self.display_power_.invoke_power_event(display_power.PowerEvent.S4, common.POWER_EVENT_DURATION_DEFAULT) is False:
            self.fail('FAILED to invoke Power Event (S4)')
        logging.info("Successfully invoked from Power Event (S4)")

        count = int(self.cmd_line_param[0]['COUNT'][0]) if self.cmd_line_param[0]['COUNT'] != 'NONE' else 1

        test_status = True
        for iteration in range(0, count):
            if self._verification_steps() is False:
                test_status &= False
                logging.error(f"LRR verification after Power Event (S4) in iteration #{iteration}")
            logging.info(f"LRR verification after Power Event (S4) in iteration #{iteration}")

        if test_status is False:
            self.fail("FAIL: LRR verification after Power Event (S4)")
        logging.info("PASS: LRR verification after Power Event (S4)")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(LrrPowerEventsTest))
    test_environment.TestEnvironment.cleanup(test_result)
