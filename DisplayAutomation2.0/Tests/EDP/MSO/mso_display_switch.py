#######################################################################################################################
# @file         mso_display_switch.py
# @addtogroup   EDP
# @section      MSO tests
# @brief        This file contains test for MSO in display switch scenarios SD eDP + External displays, Dual eDP,
#               Dual eDP + External displays
#
# @author       Bhargav Adigarla
#######################################################################################################################
from Libs.Core import enum
from Libs.Core.test_env import test_environment
from Tests.EDP.MSO.mso_base import *


##
# @brief        This class contains test for MSO in display switch scenarios
class TestDisplaySwitch(MsoBase):
    ############################
    # Test Function
    ############################

    ##
    # @brief        This test verifies the requirements mso tests with display switch.
    # @return       None
    # @cond
    @common.configure_test(critical=True)
    # @endcond
    def t_01_display_switch_requirements(self):
        if len(self.external_panels) == 0:
            self.fail("At least one external display is required for mso_display_switch (Command Line Issue)")

    ##
    # @brief        This test verifies mso with display switch
    # @return       None
    # @cond
    @common.configure_test(repeat=True)
    # @endcond
    def t_10_display_switch(self):
        self.__verify_mso_with_display_switch()

    ##
    # @brief        This is a internal function for verifying mso with various display configs
    # @return       None
    def __verify_mso_with_display_switch(self):

        if len(self.edp_panels) > 1:
            ##
            # Dual eDP case
            if len(self.external_panels) == 0:
                ##
                # Dual eDP only
                self.config_list = [(enum.SINGLE, [self.edp_panels[0]]),
                                    (enum.EXTENDED, [self.edp_panels[0], self.edp_panels[1]]),
                                    (enum.SINGLE, [self.edp_panels[0]])]
            else:
                ##
                # Dual eDP with external panel
                self.config_list = [(enum.SINGLE, [self.edp_panels[0]]),
                                    (enum.EXTENDED, [self.edp_panels[0], self.edp_panels[1], self.external_panels[0]]),
                                    (enum.SINGLE, [self.edp_panels[0]]),
                                    (enum.EXTENDED, [self.edp_panels[0], self.edp_panels[1]]),
                                    (enum.SINGLE, [self.edp_panels[0]])]

        else:
            ##
            # Single eDp with single external panel
            self.config_list = [(enum.SINGLE, [self.edp_panels[0]]),
                                (enum.EXTENDED, [self.edp_panels[0], self.external_panels[0]]),
                                (enum.SINGLE, [self.edp_panels[0]]),
                                (enum.EXTENDED, [self.external_panels[0], self.edp_panels[0]]),
                                (enum.SINGLE, [self.edp_panels[0]])]

        for config in self.config_list:
            if self.display_config_.set_display_configuration_ex(config[0], config[1]) is False:
                self.fail("Applying Display config {0} Failed"
                          .format(str(config[0]) + " " + " ".join(str(x) for x in config[1])))
            for panel in self.mso_panels:
                if panel.port in config[1]:
                    if mso.verify(panel) is True:
                        logging.info("\tPASS: MSO verification successful for {0}".format(panel.port))
                    else:
                        self.fail("\tFAIL: MSO verification failed for {0}".format(panel.port))
                else:
                    logging.info("Current config doesn't have MSO supported panels")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(TestDisplaySwitch))
    test_environment.TestEnvironment.cleanup(test_result)
