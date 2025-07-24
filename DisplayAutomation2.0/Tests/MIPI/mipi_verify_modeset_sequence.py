######################################################################################
# @file         mipi_verify_modeset_sequence.py
# @brief        This file contains test to verify Mipi during modeset seqeunce
# @details      This test verifies whether all MIPI related register bits are programmed properly or not during modeset
#               sequence. It calls respective verification if applicable to the current panel connected. Using MIPI
#               panel simulation, test planner can plug different panels by passing in cmdline (prepare_display_setup
#               will take care of plug). Upon that plugged panel, this test does the verification.
#               CommandLine: python mipi_verify_modeset_sequence.py -mipi_a SINK_MIP001 -mipi_c SINK_MIP001
#               Test will pass only if all required register bits are programmed correctly, otherwise it fails.
# @note         Please note that this test case is meant for Python 2.7.8(64-bit)
# @author       Sri Sumanth Geesala
######################################################################################
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.MIPI.Verifiers import mipi_dual_link, mipi_command_mode, mipi_dsc, mipi_timings, mipi_dphy_config, \
    mipi_link_related, mipi_status

from Tests.MIPI.Verifiers.mipi_video_mode import verify_video_mode_enable_bits
from Tests.MIPI.mipi_base import *


##
# @brief        This class contains test to verify Mipi during modeset seqeunce
class MipiVerifyModesetSequence(MipiBase):

    ##
    # @brief        This function verifies Mipi during modeset seqeunce
    # @return       None
    def runTest(self):

        ##
        # MIPI Video mode enable bits verification
        logging.info('*************MIPI video mode verification - Start*************')
        for port in self.port_list:
            ##
            # skip test for this port if MIPI is not in video mode in VBT (VBT is golden)
            panel_index = self.mipi_helper.get_panel_index_for_port(port)
            if self.mipi_helper.get_mode_of_operation(panel_index) != mipi_helper.VIDEO_MODE:
                logging.info('Port %s: This verification is applicable for video mode only. '
                             'Current port is not configured to video mode. Skipping for this port.' % (port))
                continue

            verify_video_mode_enable_bits(self.mipi_helper, port)
        logging.info('*************MIPI video mode verification - End************* ')

        ##
        # MIPI Command mode enable bits verification
        logging.info('*************MIPI command mode verification - Start*************')
        for port in self.port_list:
            ##
            # skip test for this port if MIPI is not in command mode in VBT (VBT is golden)
            panel_index = self.mipi_helper.get_panel_index_for_port(port)
            if self.mipi_helper.get_mode_of_operation(panel_index) != mipi_helper.COMMAND_MODE:
                logging.info('Port %s: This verification applicable for command mode only. Current port is not '
                             'configured to command mode. Skipping for this port.' % (port))
                continue

            mipi_command_mode.verify_command_mode_enable_bits(self.mipi_helper, port)
        logging.info('*************MIPI command mode verification - End*************')

        ##
        # MIPI Dual link verification
        if self.mipi_helper.dual_link:
            logging.info('*************MIPI dual link verification - Start*************')
            mipi_dual_link.verify_dual_link_config(self.mipi_helper)
            logging.info('*************MIPI dual link verification - End*************')

        ##
        # Dual MIPI port sync verification
        if self.mipi_helper.dual_LFP_MIPI_port_sync:
            logging.info('*************Dual MIPI port sync verification - Start*************')
            port_sync_states = []
            for port in self.port_list:
                port_sync_states.append(mipi_dual_link.is_dual_mipi_port_sync_enabled(self.mipi_helper, port))
            # atleast one of the ports should have port sync bits enabled for port sync to establish.
            if True in port_sync_states:
                logging.info('PASS: Port Sync is established as required bits enabled on atleast one of the DSI ports')
            else:
                logging.error('FAIL: Port Sync is not established as required bits are not enabled on any'
                              ' of the DSI ports')
                self.fail_count += 1
            logging.info('*************Dual MIPI port sync verification - End*************')

        ##
        # MIPI DSC verification
        if self.mipi_helper.DSC_enabled:
            logging.info('*************MIPI DSC verification - Start*************')
            mipi_dsc.verify_dsc_config(self.mipi_helper, self.port_list)
            logging.info('*************MIPI DSC verification - End*************')

        ##
        # MIPI timings verification
        logging.info('*************MIPI timings verification - Start*************')
        for port in self.port_list:
            mipi_timings.verify_timings(self.mipi_helper, port)
        logging.info('*************MIPI timings verification - End*************')

        ##
        # MIPI DPHY verification
        logging.info('*************MIPI DPHY verification - Start*************')
        for port in self.port_list:
            mipi_dphy_config.verify_dphy_config(self.mipi_helper, port)
        logging.info('*************MIPI DPHY verification - End*************')

        ##
        # MIPI link related verification
        logging.info('*************MIPI link related verification - Start*************')
        for port in self.port_list:
            mipi_link_related.verify_pixel_format_data_lanes(self.mipi_helper, port)
            mipi_link_related.verify_link_config(self.mipi_helper, port)
            mipi_link_related.verify_timeouts(self.mipi_helper, port)
        logging.info('*************MIPI link related verification - End*************')

        ##
        # MIPI status bits verification
        logging.info('*************MIPI status bits verification - Start*************')
        if mipi_status.check_mipi_status_bits(self.mipi_helper, self.port_list) == False:
            logging.error('MIPI status verification failed')
            self.fail_count += 1
        else:
            logging.info('MIPI status verification Passed')
        logging.info('*************MIPI status bits verification - End*************')

        ##
        # report test failure if fail_count>0
        if (self.fail_count + self.mipi_helper.verify_fail_count) > 0:
            self.fail(f'Some checks in the test have failed. Check error logs. '
                      f'No. of failures= {(self.fail_count + self.mipi_helper.verify_fail_count)}')


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
