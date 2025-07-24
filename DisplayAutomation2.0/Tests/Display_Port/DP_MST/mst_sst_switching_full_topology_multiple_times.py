################################################################################################################
# @file          mst_sst_switching_full_topology_multiple_times.py
# @brief         Verify whether topology switched properly from MST to SST for multiple iterations
# @author        Praveen Bademi
################################################################################################################

import os
import sys
import xml.etree.ElementTree as ET

from Libs.Core.test_env import test_context
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Display_Port.DP_MST.display_port_mst_base import *


##
# @brief        This class contains runTest() method that perform full topology switch from MST to SST for multiple
#               iterations
class DPMSTtoSSTSwitchingMultipleTimes(DisplayPortMSTBase):

    ##
    # @brief        This method executes the actual test steps.For a multiple number of iterations, it sets and verifies
    #               MST topology, unplugs it and after some delay it sets and verifies SST topology
    # @return       None
    def runTest(self):

        # Variable for DP Port Number Index
        dp_port_index = 0

        # list to store the delays
        plug_delay = []

        # Get the Iterations, Plug and Unplug delay time from HotPlugUnplugDelay_CyclesCount.xml file
        file_name = 'HotPlugUnplugDelay_CyclesCount.xml'
        file_path = os.path.join(test_context.TestContext.root_folder(), 'Tests\\Display_Port\\DP_MST\\' + file_name)
        if os.path.exists(file_path):
            tree = ET.parse(file_path)
        else:
            logging.error("[Test Issue]: %s file does not exist. Exiting ...." % file_path)
            self.fail()

        # Get the root node of xml file
        root = tree.getroot()

        # Get the port type from available free DP ports
        port_type = self.get_dp_port_from_availablelist(dp_port_index)

        # Get Topology Type from the command line
        topology_type = self.get_topology_type(dp_port_index)

        # Get Topology XML file from command line
        xml_file = self.get_xmlfile(dp_port_index)

        # Set index pointing to 2nd set of arguments
        dp_port_index = dp_port_index + 1

        # Get Topology Type from the command line
        topology_type2 = self.get_topology_type(dp_port_index)

        # Get Topology XML file from command line
        xml_file2 = self.get_xmlfile(dp_port_index)

        # Find the TEST NAME ie HPD,SWITCHING etc
        for test_name in root:

            # this tests is for SWITCHING, validate it
            if test_name.tag != 'SWITCH':
                continue

            counter_delay = 0
            logging.info("TEST NAME: %s" % test_name.tag)

            iterations = 0

            # Iterate for number of tests ie ITERATION1,ITERATION2 etc in XML file
            for tests in test_name:

                logging.info("TEST ITERATION NAME: %s" % tests.tag)
                # Iterate through the child to get cycles, delay1, delay2, delay3

                for child in tests:

                    # Get he number of iterations for Plug/Unplug
                    if child.tag == "Cycles":
                        iterations = child.text
                        logging.info("TOTAL CYCLES: %s" % iterations)
                    # Get the delay time for Switching
                    else:
                        counter_delay = counter_delay + 1
                        plug_delay.append(int(child.text))

                # Run the Switching for number of cycles times
                for index in range(int(iterations)):

                    logging.info("TEST ITERATION NUMBER: %s" % (index + 1))

                    for counter in range(counter_delay):
                        # Function call to set DP1.2 topology
                        self.setnverifyMST(port_type, topology_type, xml_file)

                        # Function call to hot-unplug DP MST panel
                        self.set_hpd(port_type, False)

                        logging.info("TIME: %s" % plug_delay[counter])

                        # Wait for the simulation driver to reflect the MST connection status in CUI
                        time.sleep(plug_delay[counter] / DELAY_1000_MILLISECONDS)

                        logging.info("Unplug MST")

                        # Function call to hot-plug DP SST panel needed for MST <--> SST switching
                        self.setnverifySST(port_type, topology_type2, xml_file2)


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
