##
# @file         detachable_LFP_manual.py
# @brief        This script can be used for manual testing.
# @details      cmd_line: test_display_python_automation
#               Tests\LFP_Common\Detachable_LFP\detachable_LFP_plug_unplug.py
#               -edp_A SINK_EDP012 VBT_INDEX_0 -MIPI_C SINK_MIP002 VBT_INDEX_1 -detach_lfp mipi_c
# @author       Goutham N
from Tests.LFP_Common.Detachable_LFP.detachable_LFP_base import *


##
##
# @brief        This class is for manual testing plug and unplug of
#               LFP_2 panel that inherits DetachableLFPBase for setup and _setHPD functionality.
class DetachableLFPManual(DetachableLFPBase):
    ##
    # @brief        Test case to test the plug or unplug LFP_2 panel manually.
    #               User will enter whether he wants to plug/unplug companion display then test does the operation,
    #               then user will check manually if the panel is plugged/unplugged
    # @return       None
    def runTest(self) -> None:
        user_input = None
        # Setting this flag to skip teardown phase.
        self.is_manual_scenario = True
        while user_input != 'quit':
            user_input = \
                input("Enter plug to plug the companion display, unplug to unplug the companion display, quit to quit ")
            if user_input == "plug":
                status = self._setHPD(self.mapped_port_to_detach, plug=True, port_type=self.port_type, gfx_index=self.gfx_index)
                if status == False:
                    self.fail("[Driver Issue]: Unable to plug")
                else:
                    logging.info("Successfully plugged companion display")
            elif user_input == "unplug":
                status = self._setHPD(self.mapped_port_to_detach, plug=False, port_type=self.port_type, gfx_index=self.gfx_index)
                if status == False:
                    self.fail("[Driver Issue]: Unable to unplug")
                else:
                    logging.info("Successfully unplugged companion display")
            elif user_input == "quit":
                break
            else:
                print("Invalid command!")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('DetachableLFPManual'))
    TestEnvironment.cleanup(outcome)
