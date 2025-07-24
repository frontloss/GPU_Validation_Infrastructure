#######################################################################################################################
# @file         dp_mst_manual_config.py
# @brief        MST display config switching semi - auto test file
#
# @author       Praburaj Krishnan
#######################################################################################################################

from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Display_Port.ManualTests.dp_mst_manual_base import *

##
# @brief    Test Class for Setup, Run test and Teardown
class DPMSTConfigSwitching(DisplayPortMSTManualBase):

    ##
    # @brief        This method executes the actual test steps. Building MST Topology on all ports/ports mentioned in
    #               command line. Applying the specified configuration on enumerated display.
    #               Verifying the applied configuration.
    #
    # @return       None
    def runTest(self):
        ##
        # Check for the valid display_config before proceeding.
        if self.display_config in self.SUPPORTED_CONFIG_LIST:
            ##
            # Contains supported dp port list[all dp ports/dp ports from command line]
            port_list = self.get_dp_port_list()

            # Build the MST topology and apply display config on all available/given ports.
            for dp_port in port_list:
                toRunOnPort = alert.warning(
                    "Do you want to build MST topology on port {0}".format(dp_port),
                    alert_type=alert.AlertTypes.confirm)
                if toRunOnPort is True:
                    self.build_mst_topology(port_type=dp_port)
                    all_configuration_list = self.get_possible_configurations()
                    '''
                    Incase of SINGLE configuration apply display configuration on all connected displays.
                    Incase of OTHER configuration apply SINGLE display configuration on all connected displays and 
                    then apply the display configuration passed in the command line.
                    '''
                    if self.display_config == 'SINGLE':
                        self.apply_display_config_and_verify(self.display_config, all_configuration_list['enum.SINGLE'])
                    elif self.display_config in self.SUPPORTED_CONFIG_LIST:
                        self.apply_display_config_and_verify('SINGLE', all_configuration_list['enum.SINGLE'])
                        self.apply_display_config_and_verify(self.display_config,
                                                             all_configuration_list['enum.' + self.display_config])
                else:
                    logging.info("User has skipped building MST topology on port {0}".format(dp_port))
        else:
            logging.info("{0} configuration is not supported..Exiting..".format(self.display_config))


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
