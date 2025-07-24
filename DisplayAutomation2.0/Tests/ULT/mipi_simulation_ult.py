############################################################################################################
# @file
# @brief This is ult for MIPI simulation
# @author Golwala ami
############################################################################################################
import unittest

from Libs.Core import display_essential
from Libs.Core.display_config.display_config import *
from Libs.Core.test_env.test_environment import *
from Libs.Core.display_utility import *
from Libs.Core.system_utility import *
from Libs.Core.vbt.vbt import Vbt

class MipiSimulationUlt(unittest.TestCase):

    def setUp(self):
        self.disp_config = DisplayConfiguration()
        self.utility = SystemUtility()
        self.gfx_vbt = Vbt()
        ##
        # Getting Enumerated display information
        self.enumerated_displays = self.disp_config.get_enumerated_display_info()
        logging.info("Enumerated Display Information: %s", self.enumerated_displays.to_string())
        ##
        # Getting current VBT
        is_vbt_get = self.gfx_vbt._dump('Vbt_glk_default_vbt.bin')
        if is_vbt_get:
            logging.info("Current VBT get successfully")
        else:
            logging.info("Current VBT get failed")
    
    def runTest(self):
        ##
        # Setting VBT
        is_vbt_set = self.gfx_vbt.reload(file_path='Vbt_glk_AuoMipi.bin')
        if is_vbt_set:
            logging.info("VBT for MIPI simulation is set successfully")
        else:
            logging.info("VBT for MIPI simulation set failed")

        self.gfx_vbt.apply_changes()

        ##
        # Restart the driver to make changes take effect
        result, reboot_required = display_essential.restart_gfx_driver()
        if result:
            logging.info("Driver restart is successful")
        else:
            logging.info("Driver restart is unsuccessful")
        
        ##
        # Getting Enumerated display information
        self.enumerated_displays = self.disp_config.get_enumerated_display_info()
        logging.info("Enumerated Display Information: %s",self.enumerated_displays.to_string())

        ##
        # Checking mipi panel is connected or not
        mipi_panel = None
        internal_display_list = self.disp_config.get_internal_display_list(self.enumerated_displays)
        if len(internal_display_list) != 0:
            for i in range(len(internal_display_list)):
                mipi_panel = internal_display_list[i][1]
                break
        if mipi_panel != 'MIPI_A':
            logging.info("MIPI is not connected")
        else:
            logging.info("MIPI is connected")

        ##
        # Set display config
        result = self.disp_config.set_display_configuration_ex(enum.CLONE, ['MIPI_A', 'HDMI_C'], self.enumerated_displays)
        self.assertEquals(result, True, "Aborting the test as failed to apply display config")

        ##
        # Set display config
        result = self.disp_config.set_display_configuration_ex(enum.SINGLE, ['MIPI_A'], self.enumerated_displays)
        self.assertEquals(result, True, "Aborting the test as failed to apply display config")

        ##
        # Set display config
        result = self.disp_config.set_display_configuration_ex(enum.SINGLE, ['HDMI_C'], self.enumerated_displays)
        self.assertEquals(result, True, "Aborting the test as failed to apply display config")

    def tearDown(self):

        ##
        # Setting VBT stored before executing test
        is_vbt_set = self.gfx_vbt.reload(file_path='Vbt_glk_default_vbt.bin')
        if is_vbt_set:
            logging.info("Current VBT set successfully")
        else:
            logging.info("Current VBT set failed")

        self.gfx_vbt.apply_changes()

        ##
        # Restart the driver to make changes take effect
        result, reboot_required = display_essential.restart_gfx_driver()
        if result:
            logging.info("Driver restart is successful")
        else:
            logging.info("Driver restart is unsuccessful")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
