######################################################################################
# @file         mipi_status_with_all_display_config.py
# @brief        It verifies MIPI transcoder and powerwell status for various display config :
#               SD MIPI, TED MIPI+display2+display3, TDC MIPI+display2+display3
# @details      CommandLine: python mipi_status_with_all_display_config.py -mipi_a -dp_b -hdmi_c
#               param1 is first display, param2 is second display and param3 is third display.
#               Test will pass only if MIPI status is as expected in various display config, otherwise it fails.
#               All combinations of displays will be done for TED and TDC.
# @author       Sri Sumanth Geesala
######################################################################################
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.MIPI.Verifiers import mipi_status
from Tests.MIPI.mipi_base import *


##
# @brief        This class contains test to verify MIPI status for various display config
class MipiStatusWithAllDisplayConfig(MipiBase):

    ##
    # @brief        This function verifies MIPI transcoder and powerwell status and the test checks for the expected
    #               MIPI statusfor various display config
    # @return       None
    def runTest(self):
        num_displays = 1  # mipi is 1st display
        if (self.mipi_helper.dual_LFP_MIPI):
            num_displays += 1
        num_displays += len(self.plugged_display)

        if (num_displays < 3):
            self.fail(
                "Minimum 3 displays are required to run this test. Current num_displays= %d. Aborting the test." % (
                    num_displays))

        display1 = self.mipi_master_port
        sd_mipi_config_list = [[display1]]
        if (self.mipi_helper.dual_LFP_MIPI):
            display2 = self.mipi_second_display
            display3 = self.plugged_display[0]
            sd_mipi_config_list.append([display2])
        else:
            display2 = self.plugged_display[0]
            display3 = self.plugged_display[1]
        config_combination_list = [[display1, display2, display3],
                                   [display2, display1, display3],
                                   [display2, display3, display1]]

        # SD MIPI
        for config in sd_mipi_config_list:
            logging.info('Applying SD %s config' % (config[0]))
            result = self.config.set_display_configuration_ex(enum.SINGLE, config, self.enumerated_displays)
            self.assertNotEquals(result, False, "Aborting the test as applying SD %s config failed." % (config[0]))

            if (self.mipi_helper.dual_LFP_MIPI and (config[0] == 'MIPI_A')):
                custom_port_list = ["_DSI0"]
            elif (self.mipi_helper.dual_LFP_MIPI and (config[0] == 'MIPI_C')):
                custom_port_list = ["_DSI1"]
            else:
                custom_port_list = self.port_list

            if (mipi_status.check_mipi_status_bits(self.mipi_helper, custom_port_list) is False):
                logging.error('MIPI status failed for SD %s config' % (config[0]))
                self.fail_count += 1
            else:
                logging.info('MIPI status is proper for SD %s config' % (config[0]))

        # TED configs
        for config in config_combination_list:
            logging.info('Applying TED %s+%s+%s config' % (config[0], config[1], config[2]))
            result = self.config.set_display_configuration_ex(enum.EXTENDED, config, self.enumerated_displays)
            self.assertNotEquals(result, False, "Aborting the test as applying TED %s+%s+%s config failed." % (
                config[0], config[1], config[2]))

            if (mipi_status.check_mipi_status_bits(self.mipi_helper, self.port_list) is False):
                logging.error('MIPI status failed for TED %s+%s+%s config' % (config[0], config[1], config[2]))
                self.fail_count += 1
            else:
                logging.info('MIPI status is proper for TED %s+%s+%s config' % (config[0], config[1], config[2]))

        # TDC configs
        for config in config_combination_list:
            logging.info('Applying TDC %s+%s+%s config' % (config[0], config[1], config[2]))
            result = self.config.set_display_configuration_ex(enum.CLONE, config, self.enumerated_displays)
            self.assertNotEquals(result, False, "Aborting the test as applying TDC %s+%s+%s config failed." % (
                config[0], config[1], config[2]))

            if (mipi_status.check_mipi_status_bits(self.mipi_helper, self.port_list) is False):
                logging.error('MIPI status failed for TDC %s+%s+%s config' % (config[0], config[1], config[2]))
                self.fail_count += 1
            else:
                logging.info('MIPI status is proper for TDC %s+%s+%s config' % (config[0], config[1], config[2]))

        ##
        # report test failure if fail_count>0
        if (self.fail_count + self.mipi_helper.verify_fail_count) > 0:
            self.fail(f'Some checks in the test have failed. Check error logs. '
                      f'No. of failures= {(self.fail_count + self.mipi_helper.verify_fail_count)}')



if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
