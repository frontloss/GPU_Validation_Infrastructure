################################################################################################################
# @file          mst_plug_unplug_multiple_times.py
# @brief         Verify whether Hotplug/unplug works properly for DP Ports for multiple iterations
# @author        Praveen Bademi
################################################################################################################

import os
import sys
import xml.etree.ElementTree as ET

from Libs.Core.test_env import test_context
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Display_Port.DP_MST.display_port_mst_base import *


##
# @brief        This class contains runTest() method that alternatively does hotplug/unplug multiple times and verifies
#               the MST topology
class DPMSTHotUnplug(DisplayPortMSTBase):

    ##
    # @brief        This method executes the actual test steps.It applies the MST topology mentioned in the command line
    #               and alternatively performs hotplug/unplug for multiple iterations.If final iteration is plug action
    #               then it first plugs and verifies the MST topology and then unplugs and verifies the topology.If
    #               final iteration is unplug action, then it simply unplugs the topology and verifies it.
    # @return       None
    def runTest(self):

        # Variable for DP Port Number Index
        dp_port_index = 0

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

        # Get Topology type from the command line
        topology_type = self.get_topology_type(dp_port_index)

        # Get Topology XML file from command line
        xml_file_path = self.get_xmlfile(dp_port_index)

        # Initialize the DP Port
        self.initialize_dp(port_type, topology_type)

        # Parse and Send Topology(MST)
        self.parse_send_topology(port_type, topology_type, xml_file_path)

        iterations = 0

        # find the TEST NAME ie HPD,SWITCHING etc
        for test_name in root:

            # this tests is for HPD, validate it
            if test_name.tag != 'HPD':
                continue

            # Iterate for number of tests in XML file
            for tests in test_name:
                logging.info("TEST ITERATION NAME: %s" % tests.tag)

                # Iterate through the child to get interations, plug/unplug delay
                for child in tests:

                    # Get he number of iterations for Plug/Unplug
                    if child.tag == "Cycles":
                        iterations = child.text
                        logging.info("TOTAL ITERATION NUMBER: %s" % iterations)

                    # Get the delay time for plug
                    elif child.tag == "PlugDelay":
                        plug_delay = child.text

                    # Get the delay time for unplug
                    elif child.tag == "UnPlugDelay":
                        unplug_delay = child.text

                # Run the plug/unplug events for number of cycles times
                for index in range(int(iterations) - 1):

                    logging.info("TEST ITERATION NUMBER; %s" % (index + 1))
                    # switch between PLUG and UNPLUG events
                    # based on the odd and even case
                    # even case : PLUG Event
                    # odd case; UNPLUG Event

                    if (index % 2) == 0:
                        logging.info("HOT PLUG")

                        self.parse_send_topology(port_type, topology_type, xml_file_path)
                        # Issue HPD (Hotplug interrupt) to Graphics driver
                        self.set_hpd(port_type, True)

                        # plug_delay in Milli Seconds
                        time.sleep(int(plug_delay) / DELAY_1000_MILLISECONDS)

                    else:
                        logging.info("HOT UNPLUG")

                        # Issue HPD (Hotunplug interrupt) to Graphics driver
                        self.set_hpd(port_type, False)

                        # unplug_delay in Milli Seconds
                        time.sleep(int(unplug_delay) / DELAY_1000_MILLISECONDS)

                # in case the total number of cycles is odd, then last HPD event should be PLUG
                if (int(iterations) % 2) == 1:
                    logging.info("FINAL HOT PLUG")

                    self.parse_send_topology(port_type, topology_type, xml_file_path)
                    # Issue HPD (Hotplug interrupt) to Graphics driver
                    self.set_hpd(port_type, True)

                    # plug_delay in Milli Seconds
                    time.sleep(DELAY_5000_MILLISECONDS / DELAY_1000_MILLISECONDS)

                    # Verify the MST Topology being created
                    self.verifyTopology(port_type)

                    # Read the DPCD 600h & check the HPD status
                    nativeDPCDRead = True
                    dpcd_length = 1
                    ##
                    # Read the DPCD 600h to verify Sink detected or not
                    dpcd_address = DPCD_SINK_CONTROL

                    self.dpcd_read(port_type, nativeDPCDRead, dpcd_length, dpcd_address, None, action="PLUG")

                    # Issue HPD (Hotunplug interrupt) to Graphics driver
                    self.set_hpd(port_type, False)

                    # unplug_delay in Milli Seconds
                    time.sleep(DELAY_5000_MILLISECONDS / DELAY_1000_MILLISECONDS)

                    # Verify the MST Topology being unplugged
                    self.verifyTopology(port_type, action="UNPLUG")

                # in case the total number of cycles is even, then last HPD event should be UNPLUG
                else:
                    logging.info("FINAL HOT UNPLUG")

                    # Issue HPD (Hotunplug interrupt) to Graphics driver
                    self.set_hpd(port_type, False)

                    # unplug_delay in Milli Seconds
                    time.sleep(DELAY_5000_MILLISECONDS / DELAY_1000_MILLISECONDS)

                    # Verify the MST Topology being unplugged
                    self.verifyTopology(port_type, action="UNPLUG")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
