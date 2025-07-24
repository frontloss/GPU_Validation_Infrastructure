#
# @file dynamic_cdclk_disable_enable.py
# @brief The script do disable and enable dynamic CD CLK in VBT based on input parameter:
#       * Setup- Parse input command line parameter.
# @details Command line to enable/disable dynamic CD CLK value
#       * Tests\Clock\dynamic_cdclk_disable_enable.py -dynamic_cdclk Disable  - To Disable Dynamic CD CLK
#       * Tests\Clock\dynamic_cdclk_disable_enable.py -dynamic_cdclk Enable  - To Enable Dynamic CD CLK
# @author Doriwala, Nainesh P

import unittest
import logging
import sys
from Libs.Core.logger import gdhm
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.vbt.vbt import Vbt
from Libs.Core import system_utility, display_essential
from Libs.Core import reboot_helper, cmd_parser
from Libs.Core.machine_info.machine_info import SystemInfo

DYNAMIC_CDCLK_BIT = 7
DYNAMIC_CDCLK_BIT_ACCESS = 1 << (DYNAMIC_CDCLK_BIT-1)
DYNAMIC_CDCLK_ENABLE = 0x40

##
# @brief It contains the methods to Enable and disable Dynamic CD CLK bit in VBT.
class DynamicCdCLkEnableDisable(unittest.TestCase):
    connected_list = []
    obj_machine_info = SystemInfo()
    sys_util = system_utility.SystemUtility()
    custom_tags = ['-dynamic_cdclk']
    cdclk_enable = None

    ##
    # @brief Setup - Parse command lines input parameter.
    # @return - None
    @reboot_helper.__(reboot_helper.setup)
    def setUp(self):
        cdclk_request = None
        logging.info("************** TEST START **************")
        self.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, self.custom_tags)
        for key, value in self.cmd_line_param.items():
            if key == 'DYNAMIC_CDCLK':
                if value:
                    cdclk_request = str(value[0])

        if cdclk_request == 'ENABLE':
            self.cdclk_enable = True
        elif cdclk_request == 'DISABLE':
            self.cdclk_enable = False
        else:
            self.fail("Invalid argument pass.")

    ##
    # @brief test_setup - Verify and enable/disable Dynamic CD CLK in VBT and reboot system if request by OS.
    # @return - None
    def test_setup(self):
        logging.debug("Setup - Check for Dynamic CD CLK value bit in VBT and Update")
        status, reboot_required = self.enable_disable_dynamic_cdclk()
        if status:
            logging.info("VBT updated for dynamic cd clk and successfully restarted driver.")
        elif status is False and reboot_required is True:
            if reboot_helper.reboot(self, 'test_run') is False:
                self.fail("Failed to reboot the system")
        else:
            self.fail("Failed to restart display driver")

    ##
    # @brief RunTest - Get Current Dynamic CD CLK value and verify with requested value(Enable/Disable)
    # @return - None
    def test_run(self):
        # Verify
        current_status = self.get_dynamic_cdclk()
        if current_status == self.cdclk_enable:
            logging.info("Request Dynamic cdclk applied{}".format(current_status))
        else:
            logging.error("Request Dynamic cdclk not applied current{}, request{}".
                          format(current_status, self.cdclk_enable))
            self.fail("Dynamic CD CLK not change")

    ##
    # @brief test_cleanup  - Dummy function to call post reboot of system requested by OS.
    # @return - None
    def test_cleanup(self):
        logging.info("****************TEST ENDS HERE********************************")

    ##
    # @brief Function to Enable or Disable Dynamic CD CLK
    # @param[in] self
    # @return - bool - status True if able to update VBT else False
    #           Bool - reboot_required  True if reboot require else False
    def enable_disable_dynamic_cdclk(self):
        current_value = self.get_dynamic_cdclk()
        if current_value == self.cdclk_enable:
            logging.info("Dynamic CD request{} and current value{} are same".format(self.cdclk_enable, current_value))
            status = True
            reboot_required = False
        else:
            self.set_reset_dynamic_cdclk()
            status, reboot_required = display_essential.restart_gfx_driver()
        return status, reboot_required

    ##
    # @brief get_dynamic_cdclk_enable - Function to get Dynamic CD CLK current value
    # @param[in] self
    # @param[in] gfx_index - graphics adapter index like 'gfx_0'
    # @return Boolean - True - Dynamic cd clock enable , False- Dynamic CD clock disable
    def get_dynamic_cdclk(self, gfx_index= 'gfx_0'):
        current_status = False
        logging.debug('Getting VBT Block 1 : To Check for Dynamic CD Clock Enabled')
        current_value = Vbt(gfx_index).block_1.BmpBits2 & (DYNAMIC_CDCLK_BIT_ACCESS)
        if current_value:
            current_status = True
        return current_status

    ##
    # @brief set_dynamic_cdclk_enable - Function to set Dynamic CD CLK value
    # @param[in] self
    # @param[in] gfx_index - graphics adapter index like 'gfx_0'
    # @return Boolean - True - Dynamic cd clock enable , False- Dynamic CD clock disable
    def set_reset_dynamic_cdclk(self):
        logging.debug('Getting VBT Block 1 : To Check for Dynamic CD Clock Enabled')
        vbt = Vbt('gfx_0')
        logging.debug("before update Dynamic cdclk value{}".format(vbt.block_1.BmpBits2))
        vbt.block_1.BmpBits2 = vbt.block_1.BmpBits2 ^ (DYNAMIC_CDCLK_BIT_ACCESS)
        logging.debug("after updating dynamic cdclk value{}".format(vbt.block_1.BmpBits2))
        if vbt.apply_changes() is False:
            gdhm.report_bug(
                title="[Clock] Failure in setting VBT Block 1 for Dynamic CD Clock enabling/disabling "
                      "in gfx_0",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P3,
                exposure=gdhm.Exposure.E3
            )
            logging.error('Setting VBT block 1 for Dynamic CD CLK failed for GFX_0')
            return False
        else:
            logging.info('Setting VBT block 1 for Dynamic CD CLK Passed for GFX_0')
            return True

    ##
    # @brief Function to TearDown  and clean WinDod regkey which enable in setup
    # @param[in] self
    # @return - None
    @reboot_helper.__(reboot_helper.teardown)
    def tearDown(self):
        pass


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).\
        run(reboot_helper.get_test_suite('DynamicCdCLkEnableDisable'))
    TestEnvironment.cleanup(outcome)
