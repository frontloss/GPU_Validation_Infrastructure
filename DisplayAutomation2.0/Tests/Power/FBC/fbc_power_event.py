######################################################################################
# @file     fbc_power_event.py
# @brief    Description: To verify FBC with power events.
#           Execution Command(s) :
#                   python fbc_power_event.py -edp_a -power_event CS
#           Test Failure Case(s) :
#                   FBC verification failure.
#                   Failed to generate/recover from power events
# @author   Suraj Gaikwad, Amit Sau
######################################################################################
import datetime
import time

from Libs.Core.display_config.display_config_enums import DisplayConfigTopology
from Libs.Core import display_power
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Power.FBC.fbc_base import *


class FbcPowerEvent(FbcBase):
    ##
    # Verify persistence of FBC across different Power events i.e. S3/CS, S4 and S5
    display_power = display_power.DisplayPower()
    duration = 60
    power_events_list = []

    ##
    # @brief        Test FBC with CS/S3
    # @return       None
    def test_1_fbc_s3_cs_s4(self):
        # check FBC status if PSR2 edp panel is connected
        if self.check_psr2_support():
            return
        # Set Display Configuration
        topology = eval("enum.%s" % (self.cmd_line_param['CONFIG']))
        if self.display_config.set_display_configuration_ex(topology,
                                                            self.display_list,
                                                            self.enumerated_displays) is False:
            self.fail('Failed to apply display configuration %s %s' %
                      (DisplayConfigTopology(topology).name, self.display_list))

        logging.info('Successfully applied the display configuration as %s %s' %
                     (DisplayConfigTopology(topology).name, self.display_list))

        if self.power_event is None:
            self.fail('-POWER_EVENT CS/S3 not mentioned in the command-line. Aborting the test')

        cs_status = self.display_power.is_power_state_supported(display_power.PowerEvent.CS)

        ##
        # Verify system support for the power event specified
        if self.power_event == display_power.PowerEvent.CS:
            self.assertEqual(cs_status, True, 'System does not supports Connected Standby.')
        else:
            self.assertEqual(cs_status, False, 'System does not supports S3 sleep.')

        ##
        # Append S3 or CS power event to the power events list based on command line
        self.power_events_list.insert(0, self.power_event)
        self.power_events_list.insert(1, display_power.PowerEvent.S4)

        ##
        # Verify FBC before power event
        if fbc.verify_fbc(is_display_engine_test=False) is False:
            self.fail('FAIL : FBC verification before power event!')
        logging.info('PASS : FBC verification before power event')

        for power_event in self.power_events_list:

            logging.info('===================== FBC WITH {} POWER EVENT ====================='
                         .format(power_event.name))

            # Invoke power event
            if self.display_power.invoke_power_event(power_event, self.duration) is False:
                self.fail('Test failed to invoke %s power event' % power_event.name)

            # Verify FBC after power event
            if fbc.verify_fbc(is_display_engine_test=False) is False:
                self.fail('FAIL : FBC verification after %s power event!' % power_event.name)
            logging.info('PASS : FBC verification after %s power event!' % power_event.name)

    ##
    # @brief    Check FBC status if PSR2 edp panel is connected
    # @return   void
    def test_2_fbc_s5(self):
        if self.check_psr2_support():
            return
        logging.info('===================== FBC WITH S5 POWER EVENT =====================')

        if reboot_helper.reboot(self, 'test_3_fbc_after_s5') is False:
            self.fail("Failed to reboot the system")

    ##
    # @brief    Test FBC with S5(Phase after reboot)
    # @return   None
    def test_3_fbc_after_s5(self):
        # check FBC status if PSR2 edp panel is connected
        if self.check_psr2_support():
            return
        time.sleep(10)
        power_event = display_power.PowerEvent.S5
        logging.info("Successfully resume from %s @ %s" %
                     (power_event.name, datetime.datetime.now().time()))

        # Verify FBC after power event
        if fbc.verify_fbc(is_display_engine_test=False) is False:
            self.fail('FAIL : FBC verification after %s power event!' % power_event.name)
        logging.info('PASS : FBC verification after %s power event!' % power_event.name)


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('FbcPowerEvent'))
    TestEnvironment.cleanup(outcome)
