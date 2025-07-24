########################################################################################################################
# @file         collage_disable_enable_gfxdriver.py
# @brief        Verify the collage feature during disable/enable of Graphics driver.
#
# @author       Praveen Bademi
########################################################################################################################

import logging
import sys
import time
import unittest

from Libs.Core import display_essential
from Libs.Core.test_env.test_environment import TestEnvironment

from Tests.Collage.display_collage_base import DisplayCollageBase, DELAY_1000_MILLISECONDS, DELAY_5000_MILLISECONDS


##
# @brief        This class contains runTest function to verify the collage feature during disable/enable of gfx driver.
class CollageDisableEnableGfxDriver(DisplayCollageBase):

    ##
    # @brief        runTest() executes the actual test steps.
    # @return       None
    def runTest(self) -> None:

        dp_port_list = self.get_dp_ports_to_plug()

        if (self.get_number_of_free_dp_ports() >= self.get_number_of_ports()) is False:
            logging.error("Not Enough free ports available.. Exiting....")
            self.fail()

        for index, port_type in enumerate(dp_port_list):

            # Get Topology Type(MST/SST) from the command line
            topology_type = self.get_topology_type(index)

            if topology_type == 'MST' or topology_type == 'SST':
                # Get Topology XML file from command line
                xml_file = self.get_xmlfile(index)

                # Function call to set DP1.2 topology
                self.setnverifydp(port_type, topology_type, xml_file)

        # Function call to get the collage information
        self.get_collage_info()

        # Function call to get the supported configuration
        supported_config = self.get_supported_config()

        # Function call to apply collage mode
        self.apply_collage_mode(supported_config)

        # Wait for the simulation driver to reflect the MST connection status in CUI
        time.sleep(DELAY_5000_MILLISECONDS / DELAY_1000_MILLISECONDS)

        # Disable graphics driver
        disable_status = display_essential.disable_driver()

        # Wait for the graphics driver to be disabled and reflect the changes in device manager
        time.sleep(DELAY_5000_MILLISECONDS / DELAY_1000_MILLISECONDS)

        if disable_status:
            logging.info("Graphics driver was disabled Successfully ....")
        else:
            logging.error("Graphics driver failed to be disabled. Exiting !!!!")
            self.fail()

        # Wait for the graphics driver to be enabled and reflect the changes in device manager
        time.sleep(DELAY_5000_MILLISECONDS / DELAY_1000_MILLISECONDS)

        # Enable graphics driver
        enable_status = display_essential.enable_driver()

        if enable_status:
            logging.info("Graphics driver was enabled Successfully ....")
        else:
            logging.error("Graphics driver failed to be enabled. Exiting !!!!")
            self.fail()

        # Wait for the graphics driver to be enabled and reflect the changes in device manager
        time.sleep(DELAY_5000_MILLISECONDS / DELAY_1000_MILLISECONDS)

        # Function call to check if Collage is enabled
        self.is_collage_enabled()


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
