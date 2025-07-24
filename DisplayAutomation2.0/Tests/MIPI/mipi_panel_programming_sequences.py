######################################################################################
# @file         mipi_panel_programming_sequences.py
# @brief        Test applies MIPI panel sequences on VBT (like panel power on/off, DCS commands, display on/off) using
#               supplied XML file. It boots with this modified MIPI panel and checks whether MIPI display has come up
#               fine or not.
#
# @author       Sri Sumanth Geesala
######################################################################################
import subprocess
import time

from Libs.Core.logger import gdhm
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.vbt.vbt import Vbt
from Tests.MIPI.mipi_base import *

##
# @brief        This class contains test to verify if the mipi panel has come up successfully after applying the panel
#               sequences from the Xml file
class MipiPanelProgrammingSequences(MipiBase):

    ##
    # @brief        This function verifies if mipi panel is up after applying the panel sequences on VBT before a reboot
    # @return       None
    def test_1_before_reboot(self):

        vbt_file = os.path.join(test_context.LOG_FOLDER, 'pps_modified_VBT.bin')
        mipi_sequence_tool = os.path.join(test_context.TEST_SPECIFIC_BIN_FOLDER, 'MIPI\\MIPISeqTool.exe')

        # get current VBT and dump to a file
        gfx_vbt = Vbt()
        if gfx_vbt._dump(vbt_file):
            logging.info('Got current VBT and dumped into {0}'.format(vbt_file))
        else:
            gdhm.report_bug(
                title="[MIPI][PPS] Error dumping current VBT into file",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P3,
                exposure=gdhm.Exposure.E2
            )
            logging.error('Error dumping current VBT into file')

        # run mipi sequence tool command to make the modified VBT
        # Syntax: MIPISeqTool.exe patch-vbt <input_xml_file> <output_vbt_bin_file>
        cmd_proc = subprocess.Popen('{0} patch-vbt {1} {2}'.format(mipi_sequence_tool, self.mipi_pps_xml, vbt_file))
        time.sleep(5)
        cmd_proc.terminate()
        logging.info('Ran MIPI sequence tool and patched the VBT with the MIPI PPS xml in cmdline.')

        # make Vbt object by loading this modified VBT file. Apply changes so that it write to registry.
        gfx_vbt = Vbt(file_path=vbt_file)
        if gfx_vbt.apply_changes():
            logging.info('Successfully applied the MIPI PPS modified VBT file.')
        else:
            self.fail("Failed to apply VBT")

        # restart system for booting with new MIPI panel configuration we applied in VBT.
        logging.info("Performing S5 power event")
        if reboot_helper.reboot(self, 'test_2_after_reboot') is False:
            self.fail("Failed to reboot the system")

    ##
    # @brief        This function verifies if MIPI display is active after application of the panel sequence and reboot
    # @return       None
    def test_2_after_reboot(self):
        logging.info("After Reboot")

        # apply display config with MIPI displays
        if self.mipi_helper.dual_LFP_MIPI:
            ##
            # apply ED MIPI LFP1 + MIPI LFP2, in case of dual LFP MIPI
            result = self.config.set_display_configuration_ex(enum.EXTENDED,
                                                              [self.mipi_master_port, self.mipi_second_display],
                                                              self.enumerated_displays)
            self.assertNotEquals(result, False, "Aborting the test as applying ED MIPI LFP1 + MIPI LFP2 config failed.")
        else:
            ##
            # apply SD MIPI configuration, in case single LFP MIPI
            result = self.config.set_display_configuration_ex(enum.SINGLE, [self.mipi_master_port],
                                                              self.enumerated_displays)
            self.assertNotEquals(result, False, "Aborting the test as applying SD MIPI display config failed.")

        # verify if MIPI display is active. This makes sure the new MIPI panel configuration we applied (after
        # modifying with MIPI PPS xml in cmdline) has brought up display properly.
        for display in self.displays_in_cmdline:
            if 'MIPI' not in display:
                continue
            if display_config.is_display_active(display):
                logging.info('PASS: Display {0} has been successfully brought up after MIPI PPS '
                             'modification'.format(display))
            else:
                gdhm.report_bug(
                    title="[MIPI][PPS] MIPI Display not brought up properly (not active) after MIPI PPS modification",
                    problem_classification=gdhm.ProblemClassification.UNDER_RUN,
                    component=gdhm.Component.Test.DISPLAY_INTERFACES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                logging.error('FAIL: Display {0} is not brought up properly (not active) after MIPI PPS '
                              'modification'.format(display))
                self.fail_count += 1

        ##
        # report test failure if fail_count>0
        if (self.fail_count + self.mipi_helper.verify_fail_count) > 0:
            self.fail(f'Some checks in the test have failed. Check error logs. '
                      f'No. of failures= {(self.fail_count + self.mipi_helper.verify_fail_count)}')



if __name__ == '__main__':
    TestEnvironment.initialize()
    results = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('MipiPanelProgrammingSequences'))
    TestEnvironment.cleanup(results)
