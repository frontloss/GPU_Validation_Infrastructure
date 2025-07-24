##########################################################################################################################################################################
# @file         fbc_power_event.py
# @brief        Intention of this test is to verify FBC after Power Events
# @details      
#               * Test steps are as follows
#               * Verify FBC before the power event
#               * Invoke the power event as specified in the command line (Possible Power States - S3/S4/S5/CS)
#               * Verify FBC after resuming from Power event
#
# @author       Gowtham K L
##########################################################################################################################################################################
import time

from Libs.Core import display_power, reboot_helper
from Libs.Core.logger import gdhm, html
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.PowerCons.Functional.FBC.fbc_base import *

##
# @brief        This class contains FBC Power Event test
class FbcPowerEvent(FbcBase):
    display_power_ = display_power.DisplayPower()
    power_event = None
    power_state = None

    ##
    # @brief        API to setup things for FBC Power event test
    # @return       None
    @reboot_helper.__(reboot_helper.setup)
    def setUp(self):
        self.power_state = self.cmd_line_param['SELECTIVE'][0].upper()
        if self.power_state == 'S4':
            self.power_event = display_power.PowerEvent.S4
        elif self.power_state == 'S3':
            self.power_event = display_power.PowerEvent.S3
        elif self.power_state == 'S5':
            self.power_event = display_power.PowerEvent.S5
        elif self.power_state == 'CS':
            self.power_event = display_power.PowerEvent.CS

        if self.power_event is None:
            self.fail("Invalid Power State was specified for the test(Command line issue)")


    ##
    # @brief        Test to verify FBC with power event CS, S3 and S4
    # @return       None
    def test_11_fbc_with_s3_s4_cs(self):
        if self.power_state not in ['CS', 'S3', 'S4']:
            return
        # Sometimes S4 will not be enabled by default. If S4 is requested, API itself will enable it before invoking
        if self.power_state in ['CS', 'S3']:
            if self.display_power_.is_power_state_supported(self.power_event) is False:
                self.fail(f"{self.power_event.name} is NOT enabled in the system (Planning Issue)")

        for adapter in dut.adapters.values():
            html.step_start(f"FBC verification with Power Event {self.power_event.name}")

            if fbc.verify_adapter_fbc(adapter.gfx_index) is False:
                gdhm.report_driver_bug_pc(f"[FBC] FBC verification failed")
                self.fail(f"FAIL : FBC verification failed before Power Event {self.power_event.name}")
            logging.info(f"PASS : FBC verification before Power Event {self.power_event.name}")

            if self.display_power_.invoke_power_event(self.power_event, common.POWER_EVENT_DURATION_DEFAULT) is False:
                self.fail(f"FAILED to invoke power event {display_power.PowerEvent(self.power_event)}")

            if fbc.verify_adapter_fbc(adapter.gfx_index) is False:
                gdhm.report_driver_bug_pc(f"[FBC] FBC verification was failed after Power Event")
                self.fail(f"FAIL : FBC verification after Power Event {self.power_event.name}")
            logging.info(f"PASS : FBC verification after Power Event {self.power_event.name}")

            html.step_end()


    ##
    # @brief        Test to verify FBC with power event S5
    # @return       None
    def test_12_fbc_with_s5(self):
        if self.power_state not in ['S5']:
            return
        for adapter in dut.adapters.values():
            html.step_start(f"FBC WITH POWER EVENT {self.power_event.name}")

            if fbc.verify_adapter_fbc(adapter.gfx_index) is False:
                gdhm.report_driver_bug_pc(f"[FBC] FBC verification failed")
                self.fail(f"FAIL : FBC verification before Power Event {self.power_event.name}")
            logging.info(f"PASS : FBC verification before Power Event {self.power_event.name}")
            data = {'adapter': adapter}
            if reboot_helper.reboot(self, 'test_13_fbc_after_s5', data=data) is False:
                self.fail("Failed to reboot the system")

            html.step_end()


    ##
    # @brief    Test after power event S5
    # @return   None
    def test_13_fbc_after_s5(self):
        if self.power_state not in ['S5']:
            return
        data = reboot_helper._get_reboot_data()
        adapter = data['adapter']
        time.sleep(10)
        # Verify FBC after Power Event S5
        if fbc.verify_adapter_fbc(adapter.gfx_index) is False:
            gdhm.report_driver_bug_pc(f"[FBC] FBC verification was failed after Power Event")
            self.fail(f"FAIL : FBC verification after Power Event {self.power_event.name}")
        logging.info(f"PASS : FBC verification after Power Event {self.power_event.name}")


    ##
    # @brief        Teardown function
    # @return       None
    @reboot_helper.__(reboot_helper.teardown)
    def tearDown(self):
        pass



if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('FbcPowerEvent'))
    TestEnvironment.cleanup(outcome)
