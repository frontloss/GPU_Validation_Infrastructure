########################################################################################################################
# @file         port_sync_base.py
# @brief        This files contains base class for lfp port sync tests. It contains functions which are commonly used
#               by other tests.
# @details      This is base script for dual_lfp_port_sync feature tests. These tests verify whether port sync is
#               established between the two LFPs or not while displays are up and running, with various
#               display scenarios.
# @author       Sri Sumanth Geesala
########################################################################################################################
import logging
import os
import shutil
import sys
import time
import unittest

from Libs.Core import app_controls
from Libs.Core import cmd_parser
from Libs.Core import enum
from Libs.Core import reboot_helper
from Libs.Core import window_helper
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.display_power import DisplayPower
from Libs.Core.logger import etl_tracer
from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Core.test_env import test_context
from Libs.Core.vbt.vbt import Vbt
from Libs.Feature.mipi.mipi_helper import MipiHelper
from Tests.LFP_Common.Port_Sync import port_sync
from Tests.MIPI.Verifiers import mipi_dual_link


##
# @brief        Exposed Class for LFP Port Sync tests.
# @details       Any new LFP Port Sync test can inherit this class to use common setUp and tearDown functions.
#              This class also includes some functions used across all LFP Port Sync tests
class PortSyncBase(unittest.TestCase):
    display_power = DisplayPower()
    display_config = DisplayConfiguration()
    machine_info = SystemInfo()

    ##
    # @brief        This class method is the entry point for LFP Port Sync test cases which inherit this class.
    #               It does the initializations and setup required for LFP Port Sync test execution.
    # @details      This function gets the platform info, parses command line arguments for display list and custom tags
    # @return       None
    @reboot_helper.__(reboot_helper.setup)
    def setUp(self):
        logging.info("Starting Test Setup")
        self.test_result = True
        self.gfx_vbt = Vbt()
        self.cmd_line_param = cmd_parser.parse_cmdline(sys.argv)
        # Handle multi-adapter scenario. Since sync feature is for LFPs on same adapter,
        # we are interested with first adapter only.
        if isinstance(self.cmd_line_param, list):
            self.cmd_line_param = self.cmd_line_param[0]
        self.lfps_in_cmdline = []
        self.platform = None
        self.target_id_list = []
        self.mipi_helper = None
        self.enumerated_displays = self.display_config.get_enumerated_display_info()

        # get platform
        gfx_display_hwinfo = self.machine_info.get_gfx_display_hardwareinfo()
        # WA : currently test are execute on single platform. so loop break after 1st iteration.
        # once Enable MultiAdapter remove the break statement.
        for i in range(len(gfx_display_hwinfo)):
            self.platform = ("%s" % gfx_display_hwinfo[i].DisplayAdapterName).lower()
            break

        # process cmdline for display list
        for key, value in self.cmd_line_param.items():
            if cmd_parser.display_key_pattern.match(key) is not None:
                if ((value['connector_port'] is not None) and (
                        value['connector_port'].startswith('MIPI') or value['connector_port'].startswith('EDP'))):
                    self.lfps_in_cmdline.append(value['connector_port'])
        self.lfps_in_cmdline.sort()

        if 'MIPI' in self.lfps_in_cmdline[0]:
            self.mipi_helper = MipiHelper(self.platform)

        # apply clone mode between the two LFPs
        if len(self.lfps_in_cmdline) < 2:
            self.fail('Test requires two LFPs to be passed in cmdline. Only {0} passed. Aborting test.'
                      .format(len(self.lfps_in_cmdline)))
        else:
            result = self.display_config.set_display_configuration_ex(enum.CLONE, [self.lfps_in_cmdline[0],
                                                                                   self.lfps_in_cmdline[1]],
                                                                      self.enumerated_displays)
            self.assertNotEqual(result, False, "Aborting the test as applying CLONE {0} + {1} config failed."
                                .format(self.lfps_in_cmdline[0], self.lfps_in_cmdline[1]))

        # check whether port sync supported by both LFPs
        if port_sync.is_port_sync_supported_by_panel(self.lfps_in_cmdline[0], self.platform) and \
                port_sync.is_port_sync_supported_by_panel(self.lfps_in_cmdline[1], self.platform):
            logging.info('Port sync supported by both LFPs. So port sync feature can be enabled.')
        else:
            self.fail('Port sync not supported by LFPs. Test requires port sync to be supported. Aborting test.')

    ##
    # @brief        This method is the exit point for LFP Port Sync tests
    # @return       None
    @reboot_helper.__(reboot_helper.teardown)
    def tearDown(self):
        pass

    ##
    # @brief        Helper function to do video playback, capture ETL trace and then call port sync verification methods
    # @param[in]    is_full_screen Bool, True if fullscreen required or False if windowed mode required
    # @return       True if verification passed else False, Bool
    def capture_trace_and_verify_port_sync_during_playback(self, is_full_screen=True):
        ret = True
        media_fps = 24
        video_file = os.path.join(test_context.SHARED_BINARY_FOLDER, "TestVideos", "{0:.3f}.mp4".format(media_fps))

        # Stop the ETL tracer started during TestEnvironment initialization
        etl_tracer.stop_etl_tracer()

        # run video playback and verify port sync during video playback. We need to verify port sync during video
        # playback since during idle case, VBI OFF-ON keeps coming from OS on each pipe separately and we won't be able
        # to map VBIs of one pipe to another properly. In video playback case, VBI OFF won't come and hence we can map
        # VBIs. Also video playback is the right scenario where end-user visual experience can be smooth with port sync.
        logging.info('Running video playback with {0}'.format(video_file))
        app_controls.launch_video(video_file, is_full_screen=is_full_screen)

        # start ETL tracer
        if etl_tracer.start_etl_tracer() is False:
            self.fail('Failed to start ETL Tracer')
        else:
            logging.info('ETL Tracer Started Successfully')

        # verify dual LFP port sync register bits
        port_sync_states = []
        for lfp in self.lfps_in_cmdline:
            if 'MIPI' in lfp:
                port_sync_states.append(mipi_dual_link.is_dual_mipi_port_sync_enabled(self.mipi_helper,
                                                                                      '_DSI0' if lfp == 'MIPI_A' else '_DSI1'))
            elif 'EDP' in lfp:
                # TODO: need to write verification logic here once dual eDP port sync feature is enabled.
                pass
        if True in port_sync_states:
            logging.info('PASS: Port Sync is established as required bits enabled on atleast one of the ports')
        else:
            logging.error('FAIL: Port Sync is not established as required bits are not enabled on any'
                          ' of the ports')
            ret = False

        time.sleep(2)

        # stop ETL tracer
        if etl_tracer.stop_etl_tracer() is False:
            self.fail('Failed to stop ETL tracer')

        # stop video playback
        window_helper.close_media_player()

        # rename ETL trace file
        etl_file_name = "GfxTrace_dual_lfp_port_sync_{0}.etl".format(str(time.time()))
        new_etl_file = os.path.join(test_context.LOG_FOLDER, etl_file_name)
        if os.path.exists(etl_tracer.GFX_TRACE_ETL_FILE) is False:
            self.fail(etl_tracer.GFX_TRACE_ETL_FILE + " NOT found.")
        shutil.move(etl_tracer.GFX_TRACE_ETL_FILE, new_etl_file)
        logging.info("ETL dumped to: {0}".format(new_etl_file))

        # verify dual LFP port sync using VBI timestamps
        logging.info('Verifying Port sync using captured ETL trace')
        ret &= port_sync.verify_dual_lfp_port_sync_using_VBI(self.lfps_in_cmdline, new_etl_file, self.platform)

        # start ETL tracer again for normal execution
        if etl_tracer.start_etl_tracer() is False:
            self.fail('Failed to start ETL Tracer')

        return ret
