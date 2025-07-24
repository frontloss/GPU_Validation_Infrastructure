########################################################################################################################
# @file         vdd_base.py
# @brief        This file contains common setUp and tearDown steps for all VDD tests.
#
# @author       Akshaya Nair
########################################################################################################################


import unittest

from Libs.Core.display_config import display_config
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.EDP.VDD.vdd import *

##
# @brief         Exposed Class to write VDD tests. Any new VDD test class can inherit this class to use common setUp and
#                tearDown functions
class VDDBase(unittest.TestCase):
    cmd_line_param = None  # Used to store command line parameters
    display_list = []  # Used to store all displays given in command line
    edp_panels = []  # Used to store eDP panels given in command line
    external_panels = []  # Used to store external panels given in command line
    edp_target_ids = {}  # Used to store target IDs for eDP panels {'DP_A': 456}
    topology = None
    display_config_ = display_config.DisplayConfiguration()
    display_power_ = display_power.DisplayPower()

    ############################
    # Default UnitTest Functions
    ############################

    ##
    # @brief        This method initializes and prepares the setup required for execution of tests in this class
    # @details      It parses the command line checks for eDP connections and sets display configuration
    # @return       None
    @reboot_helper.__(reboot_helper.setup)
    def setUp(self):
        logging.info(" SETUP: VDD_BASE ".center(common.MAX_LINE_WIDTH, "*"))
        dut.prepare()
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if not panel.is_lfp:
                    self.external_panels.append(panel.port)
                else:
                    self.edp_panels.append(panel.port)

    ##
    # @brief        This function logs the teardown phase
    # @return       None
    @reboot_helper.__(reboot_helper.teardown)
    def tearDown(self):
        logging.info(" TEARDOWN: VDD_BASE ".center(common.MAX_LINE_WIDTH, "*"))
        dut.reset()

