###############################################################################
# \ref plug_unplug_testcontext_ult.py
# \remarks 
# plug_unplug_testcontext_ult.py imports test_environment and test_context as module
# and verifies plug/unplug based on testcontext XML.  
# \author   Gopal, Beeresh Patil, Devendrasing, Praburaj Krishnan
###############################################################################

import os
import unittest
from Libs.Core.test_env.test_context import TestContextPersistence
from Libs.Core.test_env import test_context
from Libs.Core import display_utility
from Libs.Core.test_env.test_environment import TestEnvironment
import sys
import time
import logging
from Libs.Core.display_config.display_config import *


def get_supported_external_ports():
    supported_ports = get_supported_ports()
    external_ports = [port_name for port_name in supported_ports if '_A' not in port_name.upper()]
    return external_ports


def get_hdmi_ports():
    ports = get_supported_external_ports()
    hdmi_ports = [port for port in ports if "HDMI_" in port.upper()]
    return hdmi_ports


def get_dp_ports():
    ports = get_supported_external_ports()
    dp_ports = [port for port in ports if "DP_" in port.upper()]
    return dp_ports


def get_external_free_ports():
    free_ports = get_free_ports()
    external_ports = [port_name for port_name in free_ports if '_A' not in port_name.upper()]
    return external_ports


class TestContextPersistenceULT(unittest.TestCase):

    def test_1_sanity_check(self):
        test_context_persistence = TestContextPersistence()
        context_file = test_context_persistence.test_context_xml_path
        if os.path.exists(context_file):
            logging.info("PASS: Context file created successfully")
        else:
            self.fail("Context file creation failed")

    def test_2_plug_unplug_basic(self):
        test_context_persistence = TestContextPersistence()
        hdmi_panel = {'EDID': 'HDMI_DELL.EDID'}
        free_ports = get_hdmi_ports()

        # This will be changed in future once all API's are updated and will get adapter details from
        # get_gfx_device_info_table. This has been done to keep changes minimal
        adapter_name = 'gfx_0'

        for port in free_ports:
            display_utility.plug(port, hdmi_panel['EDID'], None)
            time.sleep(5)
            plugged_ports_dict = test_context_persistence._get_plugged_ports(adapter_name)
            plugged_ports = plugged_ports_dict[adapter_name].keys()
            if port in plugged_ports:
                logging.info("Recording of plug event is successful")

            display_utility.unplug(port)
            time.sleep(5)
            plugged_ports = test_context.plugged_ports().keys()
            if port not in plugged_ports:
                logging.info("Recording of unplug event is successful")

    def test_3_plug_unplug_back_2_back(self):
        test_context_persistence = TestContextPersistence()
        hdmi_panel = {'EDID': 'HDMI_DELL.EDID'}

        # This will be changed in future once all API's are updated and will get adapter details from
        # get_gfx_device_info_table. This has been done to keep changes minimal
        adapter_name = 'gfx_0'

        free_ports = get_hdmi_ports()
        plugged_ports = []

        for port in free_ports:
            display_utility.plug(port, hdmi_panel['EDID'], None)
            time.sleep(2)
            plugged_ports_dict = test_context_persistence._get_plugged_ports(adapter_name)
            plugged_ports = plugged_ports_dict[adapter_name].keys()
            if port in plugged_ports:
                logging.info("Recording of plug event was successful")
                plugged_ports.append(port)
            else:
                self.fail("Recording of plug event failed")

        for port in plugged_ports:
            display_utility.unplug(port)
            time.sleep(2)
            plugged_ports_dict = test_context_persistence._get_plugged_ports(adapter_name)
            plugged_ports = plugged_ports_dict[adapter_name].keys()
            if port not in plugged_ports:
                logging.info("Recording of unplug event was successful")


if __name__ == "__main__":
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
