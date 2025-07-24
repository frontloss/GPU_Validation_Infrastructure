########################################################################################################################
# @file         psr_base.py
# @brief        Contains base class for all PSR tests
# @details      @ref psr_base.py <br>
#               This file implements unittest default functions for setUp and tearDown, common test functions used
#               across all PSR tests, and helper functions.
#
# @author       Rohit Kumar
########################################################################################################################

import logging
import os
import sys
import time
import unittest

from Libs.Core import cmd_parser, enum, window_helper, app_controls, display_essential, registry_access
from Libs.Core import system_utility
from Libs.Core import winkb_helper as kb
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.display_power import DisplayPower, PowerSource
from Libs.Core.logger import etl_tracer, gdhm
from Libs.Core.machine_info import machine_info
from Libs.Core.sw_sim import driver_interface
from Libs.Core.test_env import test_context
from Libs.Core.wrapper import valsim_args
from Libs.Feature.display_fbc import fbc
from Libs.Feature.powercons import registry
from Tests.Color.Common import common_utility
from registers.mmioregister import MMIORegister
from Tests.PowerCons.Functional import pc_external

from Tests.PowerCons.Functional.PSR import pr, psr, psr_util, sfsu
from Tests.PowerCons.Modules import common, desktop_controls, dut, polling, dpcd


##
# @brief        Exposed Class to write PSR tests. Any new PSR test can inherit this class to use common setUp and
#               tearDown functions. PsrBase also includes some functions used across all LRR tests.
class PsrBase(unittest.TestCase):
    cmd_line_param = None  # Used to store command line parameters
    method = 'APP'  # Method used for feature verification APP/VIDEO
    feature = None
    feature_str = None
    power_source = None
    toggle_power_source = False

    is_negative_test = False
    is_performance_test = False
    is_pause_video_test = False

    no_of_displays = 0

    display_config_ = DisplayConfiguration()
    display_power_ = DisplayPower()
    driver_interface_ = driver_interface.DriverInterface()
    lace1p0_status = None
    lace1p0_reg_value = None
    ############################
    # Default UnitTest Functions
    ############################

    ##
    # @brief        This class method is the entry point for PSR test cases. Helps to initialize some of the
    #               parameters required for PSR test execution.
    # @details      This function checks for feature support and initialises parameters to handle
    #               multi-adapter scenarios in test cases
    # @return       None
    @classmethod
    def setUpClass(cls):
        #Read registry for LACE
        cls.lace1p0_status, cls.lace1p0_reg_value = common_utility.read_registry(gfx_index="GFX_0",
                                                                                   reg_name="LaceVersion")

        logging.info(" SETUP: PSR_BASE ".center(common.MAX_LINE_WIDTH, "*"))

        cls.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, custom_tags=common.CUSTOM_TAGS)
        current_config = cls.display_config_.get_current_display_configuration()

        cls.no_of_displays = current_config.numberOfDisplays

        # Handle multi-adapter scenario
        if not isinstance(cls.cmd_line_param, list):
            cls.cmd_line_param = [cls.cmd_line_param]

        if cls.cmd_line_param[0]['METHOD'] != 'NONE' and cls.cmd_line_param[0]['METHOD'][0] != 'APP':
            cls.method = cls.cmd_line_param[0]['METHOD'][0]
            if len(cls.cmd_line_param[0]['METHOD']) > 1:
                if cls.cmd_line_param[0]['METHOD'][1] == 'PAUSE':
                    cls.is_pause_video_test = True
                if 'FPS' in cls.cmd_line_param[0]['METHOD'][1]:
                    fps = cls.cmd_line_param[0]['METHOD'][1]
                    if fps == 'FPS_30':
                        psr.DEFAULT_MEDIA_FPS = 30
                    elif fps == 'FPS_29.97':
                        psr.DEFAULT_MEDIA_FPS = 29.970
                    elif fps == 'FPS_59.94':
                        psr.DEFAULT_MEDIA_FPS = 59.94
                    elif fps == 'FPS_23.97':
                        psr.DEFAULT_MEDIA_FPS = 23.976
                    elif fps == 'FPS_25':
                        psr.DEFAULT_MEDIA_FPS = 25
                    else:
                        assert False, "Invalid Media fps value :{} passed in cmd-line".format(fps)
                if 'AC_DC' in cls.cmd_line_param[0]['METHOD'][1]:
                    cls.toggle_power_source = True
                if cls.cmd_line_param[0]['COUNT'] != 'NONE':
                    cls.spi_count = int(cls.cmd_line_param[0]['COUNT'][0])

        if cls.cmd_line_param[0]['FEATURE'] != 'NONE':
            cls.feature = psr.UserRequestedFeature.by_str(cls.cmd_line_param[0]['FEATURE'][0])
            cls.feature_str = psr.UserRequestedFeature(cls.feature).name

        assert cls.feature, "Invalid Feature {0} given in command line. Possible values are " \
                            "PSR1/PSR2(Commandline Issue)".format(cls.feature)

        if cls.method == 'VIDEO' and cls.feature in ['PSR1']:
            assert False, "Video playback verification is not supported for {0} tests".format(cls.feature)

        dut.prepare()

        if common.IS_PRE_SI:
            cls.pre_si_setup()

        logging.info("Enabling Simulated Battery")
        assert cls.display_power_.enable_disable_simulated_battery(True), "Failed to enable Simulated Battery"
        logging.info("\tPASS: Expected Simulated Battery Status= ENABLED, Actual= ENABLED")
        cls.power_source = cls.display_power_.get_current_powerline_status()

    ##
    # @brief        This method is the exit point for PSR test cases. This resets the environment changes done
    #               for execution of LRR tests
    # @return       None
    @classmethod
    def tearDownClass(cls):
        logging.info(" TEARDOWN: PSR_BASE ".center(common.MAX_LINE_WIDTH, "*"))
        psr_status = None
        for adapter in dut.adapters.values():
            # reset the reg key value
            psr_ac = psr.enable_disable_psr_in_ac(adapter, enable_in_ac=True)
            if psr_ac is False:
                assert False, "Failed to update the PsrDisableInAC reg key"
            # Enable back PSR2 in REGKEY for PSR1 test
            if cls.feature == psr.UserRequestedFeature.PSR_1:
                psr_status = psr.enable(adapter.gfx_index, psr.UserRequestedFeature.PSR_2)
                if psr_status is False:
                    assert False, "Failed to update the Psr2Disable reg key"
            if psr_ac or psr_status:
                status, reboot_required = display_essential.restart_gfx_driver()
                if status is False:
                    logging.warning("Failed to do driver restart post the psr reg key update")
                logging.info("Successfully restarted driver post Psr reg key update")
            if adapter.name in common.GEN_13_PLATFORMS + common.GEN_14_PLATFORMS:
                for panel in adapter.panels.values():
                    if panel.psr_caps.is_psr_supported and (panel.pr_caps.is_pr_supported is False):
                        status = pc_external.update_panel_dpcd(adapter.gfx_index, panel.port,
                                                               dpcd.Offsets.SINK_DEVICE_PSR_STATUS, 0x0)
                        if status is False:
                            logging.warning("Failed to reset DPCD 2008H")
                            gdhm.report_test_bug_pc("Failed to reset dpcd 2008H")
                        logging.info("Successfully reset dpcd 2008H to 0x0")

        # Resetting LACE to default version
        if common_utility.write_registry(gfx_index="GFX_0", reg_name="LaceVersion",
                                         reg_datatype=registry_access.RegDataType.DWORD,
                                         reg_value=cls.lace1p0_reg_value,
                                         driver_restart_required=True) is False:
            logging.error("Failed to enable default Lace2.0 registry key")
            cls.fail(PsrBase(),"Failed to enable default Lace2.0 registry key")
        else:
            logging.info("Pass: Lace restored back to default Lace2.0 in TearDown")
        logging.info("Registry key add to enable default Lace2.0 is successful")

        dut.reset()
        window_helper.toggle_task_bar(window_helper.Visibility.SHOW)
        cls.display_power_.enable_disable_simulated_battery(False)

    ############################
    # Test Function
    ############################

    ##
    # @brief        Common requirement test for PSR test cases. All requirement tests will start with 't_0'.
    #               Verifies common hardware and software requirements for all the tests.
    # @note         This is a critical test. Failure of this test will stop the execution of other tests.
    # @return       None
    # @cond
    @common.configure_test(critical=True)
    # @endcond
    def t_00_requirements(self):
        psr_pr_support = False
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.psr_caps.is_psr_supported is False and panel.pr_caps.is_pr_supported is False:
                    continue
                psr_pr_support = True
                logging.info("Verifying test requirements for {0}({1})".format(panel.port, adapter.name))
                logging.info(f"\t{panel.psr_caps}")
                logging.info(f"\t{panel.pr_caps}")
                if panel.is_lfp:
                    # Make sure required PSR version is supported on connected eDP panel
                    if self.feature == psr.UserRequestedFeature.PSR_1 and panel.psr_caps.is_psr_supported is False:
                        self.fail(f"PSR is NOT supported on connected {panel.port} (Planning Issue)")
                    elif psr.UserRequestedFeature.PSR_2 <= self.feature < psr.UserRequestedFeature.PANEL_REPLAY and \
                            panel.psr_caps.is_psr2_supported is False:
                        self.fail(f"PSR2 is NOT supported on connected {panel.port} (Planning Issue)")
                # Make sure PR is supported on connected eDP panel
                if self.feature == psr.UserRequestedFeature.PANEL_REPLAY and panel.pr_caps.is_pr_supported is False:
                    self.fail(f"PR is NOT supported on connected {panel.port} (Planning Issue)")

                # PSR is supported only on Pipe-A and Pipe-B
                if panel.psr_caps.is_psr_supported and panel.pipe not in ['A', 'B']:
                    logging.warning(f"Skipping the verification as PSR is not supported on Pipe-{panel.pipe}.")
                    continue

                logging.info("\tPASS: {0} status Expected= SUPPORTED, Actual= SUPPORTED".format(self.feature_str))
                if self.feature == psr.UserRequestedFeature.PANEL_REPLAY:
                    continue
                psr_status = psr.is_psr_enabled_in_driver(adapter, panel, self.feature)
                if self.feature >= psr.UserRequestedFeature.PSR_2 and self.is_psr2_possible(adapter, panel):
                    # Make sure PSR2 and VDSC/FBC/HDR are not enabled simultaneously
                    if panel.vdsc_caps.is_vdsc_supported:
                        if adapter.name in common.PRE_GEN_12_PLATFORMS:
                            edp_dss_ctl2 = MMIORegister.read('DSS_CTL2_REGISTER', 'DSS_CTL2', adapter.name,
                                                             gfx_index=adapter.gfx_index)
                        else:
                            edp_dss_ctl2 = MMIORegister.read('PIPE_DSS_CTL2_REGISTER', 'PIPE_DSS_CTL2_P' + panel.pipe,
                                                             adapter.name, gfx_index=adapter.gfx_index)
                        if adapter.name in common.PRE_GEN_13_PLATFORMS + ['DG2']:
                            if psr_status and edp_dss_ctl2.left_branch_vdsc_enable == 0x1:
                                self.fail("PSR2 and VDSC co-existence NOT supported in HW/SW policy on {0}"
                                          .format(panel.port))

                    if panel.hdr_caps.is_hdr_supported and adapter.name in common.GEN_11_PLATFORMS:
                        pipe_misc = MMIORegister.read('PIPE_MISC_REGISTER', 'PIPE_MISC_' + panel.pipe, adapter.name,
                                                      gfx_index=adapter.gfx_index)
                        if psr_status and pipe_misc.hdr_mode == 0x1:
                            self.fail(f"PSR2 and HDR co-existence NOT supported in HW/SW policy on {panel.port}")
                    # Always VRR enable for MTL+ on VRR panel
                    if panel.vrr_caps.is_always_vrr_mode and not common.IS_PRE_SI:
                        logging.info("Checking for VRR CTL register to confirm always in VRR Mode")
                        vrr_ctl = MMIORegister.read('TRANS_VRR_CTL_REGISTER', 'TRANS_VRR_CTL_' + panel.pipe,
                                                    adapter.name, gfx_index=adapter.gfx_index)
                        if psr_status and vrr_ctl.vrr_enable is False:
                            logging.error("VRR disable post Mode Set for Always in VRR mode")
                            self.fail("VRR disable post Mode Set for Always in VRR mode")
                        else:
                            logging.info("VRR enable Post Mode Set for Always in VRR mode")
        if psr_pr_support is False:
            self.fail(f"At least one panel should support {self.feature_str} (Planning issue)")

    ##
    # @brief        This is test function to verify the enabling of feature
    # @note         This is a critical test. Failure of this test will stop the execution of other tests.
    # @return       None
    # @cond
    @common.configure_test(critical=True)
    # @endcond
    def t_10_enable_feature(self):
        retry_counter = 0
        for adapter in dut.adapters.values():
            logging.info("Step: Enabling {0} on {1}".format(self.feature_str, adapter.name))

            psr_status = None
            psr2_status = None
            if self.feature == psr.UserRequestedFeature.PSR_1:
                psr_status = psr.enable(adapter.gfx_index, self.feature)
                if psr_status is False:
                    self.fail(f"FAILED to enable PSR in {adapter.name}")

                psr2_status = psr.disable(adapter.gfx_index, psr.UserRequestedFeature.PSR_2)
                if psr2_status is False:
                    self.fail(f"Failed to disable PSR2 in {adapter.name}")
            else:
                feature, feature_str = self.get_feature(adapter)
                psr_status = psr.enable(adapter.gfx_index, feature)
                if psr_status is False:
                    self.fail(f"Failed to enable {feature_str} in {adapter.name}")

            if psr_status or psr2_status:
                result, reboot_required = display_essential.restart_gfx_driver()
                if result is False:
                    self.fail("FAILED to restart the driver")

            if adapter.lfp_count > 1:
                dut.refresh_panel_caps(adapter)
            for panel in adapter.panels.values():
                if panel.psr_caps.is_psr_supported is False and panel.pr_caps.is_pr_supported is False:
                    continue
                if panel.pr_caps.is_pr_supported and self.feature == psr.UserRequestedFeature.PANEL_REPLAY:
                    if panel.is_lfp:
                        restriction = pr.verify_pr_timing_support(adapter, panel)
                        if restriction is None:
                            logging.info(f"Timing not supported. Skipping PR check on {panel.port}")
                            continue
                        elif restriction is False:
                            self.fail("PR restriction check failed")
                    while True:
                        if pr.is_enabled_in_driver(adapter, panel) is True:
                            break
                        else:
                            retry_counter += 1
                            logging.debug(f"{self.feature_str} is not enabled in driver, trying again..")
                            time.sleep(1)

                        if retry_counter > 3:
                            gdhm.report_driver_bug_pc(f"[Powercons][PR] {self.feature_str} is not enabled in the driver")
                            logging.error(f"\t{self.feature_str} is not enabled in driver")
                            self.fail(f"Panel Replay not enabled in driver on {panel}")
                    logging.info(
                        f"\tPASS: {self.feature_str} driver status on PIPE_{panel.pipe} "
                        f"Expected= ENABLED, Actual= ENABLED")
                    # PSR is supported only on Pipe-A and Pipe-B
                elif panel.psr_caps.is_psr_supported:
                    if panel.pipe not in ['A', 'B']:
                        logging.warning(f"Skipping the verification as PSR is not supported on Pipe-{panel.pipe}.")
                        continue
                    status = psr.verify_psr_setup_time(adapter, panel, self.feature)
                    if status is None:
                        continue
                    elif status is False:
                        self.fail("PSR restriction check failed")
                    feature, feature_str = self.get_feature(adapter)
                    if psr.UserRequestedFeature.PSR_2 <= feature < psr.UserRequestedFeature.PANEL_REPLAY:
                        restriction = psr.verify_psr2_vblank_support(adapter, panel)
                        restriction &= psr.verify_psr2_hblank_requirement(adapter, panel)
                        if restriction is False:
                            logging.info("PSR2 restrictions failed. Falling back to PSR1")
                        if (self.is_psr2_possible(adapter, panel) is False) or (restriction is False):
                            feature = psr.UserRequestedFeature.PSR_1
                            feature_str = psr.UserRequestedFeature(feature).name

                    # Make sure required PSR version is enabled in driver for connected eDP panel
                    if psr.is_psr_enabled_in_driver(adapter, panel, feature) is False:
                        #checking psr status in VBT
                        gfx_vbt = psr.vbt.Vbt(adapter.gfx_index)
                        panel_index = gfx_vbt.get_lfp_panel_type(panel.port)
                        psr_status = (gfx_vbt.block_44.PsrEnable[0] & (1 << panel_index)) >> panel_index
                        logging.info(f"Status of {self.feature_str} in VBT : {psr_status}")
                        #If PSR is disabled in VBT, report out the error(dont fail the test)
                        if psr_status != 1:
                            gdhm.report_driver_bug_pc(f"[PowerCons]][PSR_SFSU] {feature_str} is not enabled by the driver")
                        #Enable PSR in VBT
                        logging.info(f"STEP: Enable {self.feature_str} in VBT")
                        if psr.update_vbt(adapter, panel, True) is False:
                            self.fail(f"Failed to update {self.feature_str} settings in VBT")
                        #Check PSR status in driver
                        if psr.is_psr_enabled_in_driver(adapter, panel, self.feature) is False:
                            self.fail(f"{self.feature_str} is not enabled")
                        logging.info(f"PASS: {self.feature_str} is enabled in driver with VBT enable")

                    logging.info(
                        "\tPASS: {0} driver status on PIPE_{1} .Expected= ENABLED, Actual= ENABLED".format(feature_str,
                                                                                                           panel.pipe))

    ############################
    # Helper Functions
    ############################

    ##
    # @brief        Helper function to set up pre-si changes required for verification and do some basic checks
    # @return       None
    @classmethod
    def pre_si_setup(cls):
        # In case of Pre-Silicon, enable "change_mask_for_vblank_vsync_int" in PIPE_MISC_REGISTER
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    continue
                pipe_misc = MMIORegister.read(
                    "PIPE_MISC_REGISTER", "PIPE_MISC_" + panel.pipe, adapter.name, gfx_index=adapter.gfx_index)
                if pipe_misc.change_mask_for_vblank_vsync_int != 1:
                    pipe_misc.change_mask_for_vblank_vsync_int = 1
                    if cls.driver_interface_.mmio_write(
                            pipe_misc.offset, pipe_misc.asUint, gfx_index=adapter.gfx_index) is False:
                        assert False, "Failed to write MMIO Offset= {0}({1})".format(pipe_misc.offset, panel.port)
                    logging.info(
                        "\tPASS: Write MMIO Offset= {0}({1}) successful".format(pipe_misc.offset, panel.port))

        # Hiding the task-bar to make sure that there's no update on screen
        if window_helper.toggle_task_bar(window_helper.Visibility.HIDE):
            logging.info("Task-bar is hidden successfully")
        else:
            logging.error("Failed to hide the task-bar")

        # Clear OS display off timeout values
        if desktop_controls.set_time_out(desktop_controls.TimeOut(0), 0, PowerSource.AC) is False:
            logging.warning("Failed to reset display off timeout values in AC")
        if desktop_controls.set_time_out(desktop_controls.TimeOut(0), 0, PowerSource.DC) is False:
            logging.warning("Failed to reset display off timeout values in DC")

    ##
    # @brief        Function to perform feature validation
    # @param[in]    power_source enum member of PowerSource
    # @param[in]    power_event [optional], enum member of PowerEvent
    # @param[in]    is_negative [optional], boolean indicates if it's a negative test
    # @return       True if feature validation is successful, False otherwise
    def validate_feature(self, power_source=None, power_event=None, is_negative=False):
        if power_source is not None:
            self.power_source = power_source
            if not self.display_power_.set_current_powerline_status(power_source):
                self.fail("Failed to switch power line status to {0}(Test Issue)".format(power_source.name))
            for adapter in dut.adapters.values():
                if adapter.name in common.PRE_GEN_15_PLATFORMS:
                    if self.power_source == PowerSource.DC and (common.IS_PRE_SI is False):
                        if self.feature != psr.UserRequestedFeature.PANEL_REPLAY:
                            for adapter in dut.adapters.values():
                                psr_ac = psr.enable_disable_psr_in_ac(adapter, enable_in_ac=False)
                                if psr_ac is False:
                                    return False
                                if psr_ac is True:
                                    result, reboot_required = display_essential.restart_gfx_driver()
                                    if result is False:
                                        return False


        if power_event is not None:
            logging.info("Step: Verifying {0} before power event {1}".format(self.feature_str, power_event.name))
            status = self.__verify()
            if status is False and is_negative is False:
                self.fail("{0} verification failed".format(self.feature_str))
            elif status is True and is_negative is True:
                logging.error("\t Expected verification status : False . Actual :{0}".format(status))
                self.fail("{0} verification Failed for Negative Tests".format(self.feature_str))

            if self.display_power_.invoke_power_event(power_event, common.POWER_EVENT_DURATION_DEFAULT) is False:
                self.fail('Failed to invoke power event {0}'.format(power_event.name))

            logging.info("Step: Verifying {0} after power event {1}".format(self.feature_str, power_event.name))
            time.sleep(5)
        status = self.__verify()
        if status is False and is_negative is False:
            self.fail("{0} verification failed".format(self.feature_str))
        elif status is True and is_negative is True:
            logging.error("\t Expected verification status : False . Actual :{0}".format(status))
            self.fail("{0} verification Failed for Negative Tests".format(self.feature_str))

    ##
    # @brief        Helper API to get workload traces
    # @param[in]    workload string, VIDEO/APP
    # @param[in]    workload_args list
    #                   VIDEO = [media_fps, duration, pause=False, power_source]
    #                   APP = [monitor_ids]
    # @param[in]    polling_args [optional], list, [poll_offset_list=None, poll_delay=0.01]
    # @param[in]    monitor_id_map [optional], list of monitor ids
    # @param[in]    port [optional], of the panel
    # @param[in]    full_screen [optional], boolean indicating if video playback should be in full screen mode
    # @return       result tuple, (etl_file, polling_data)
    def __get_workload_traces(self, workload, workload_args, polling_args=None, monitor_id_map=None, port='DP_A',
                              full_screen=True, adapter=None):
        polling_timeline = None
        polling_time_stamps = None
        utility_timeline = None
        utility_time_stamps = None

        etl_tracer.stop_etl_tracer()
        if os.path.exists(etl_tracer.GFX_TRACE_ETL_FILE):
            file_name = 'GfxTraceBeforeWorkload.' + str(time.time()) + '.etl'
            etl_file_path = os.path.join(test_context.LOG_FOLDER, file_name)
            os.rename(etl_tracer.GFX_TRACE_ETL_FILE, etl_file_path)

        kb.press('WIN+M')
        initial_pwr_rsc = self.power_source

        # Hiding the task-bar to make sure that there's no update on screen
        logging.info("STEP: Hiding the task-bar")
        assert window_helper.toggle_task_bar(window_helper.Visibility.HIDE), "FAILED to hide the task-bar"
        logging.info("\tSuccessfully hide the task-bar")

        panel_index = list(monitor_id_map.keys()).index(port)
        current_config = self.display_config_.get_current_display_configuration()
        if etl_tracer.start_etl_tracer() is False:
            self.fail("Failed to start ETL Tracer")

        logging.info("Step: Running Workload {0}".format(workload))
        if workload == 'VIDEO':
            logging.info("\tVideo Playback started : {0:.3f}.mp4".format(workload_args[0]))
            app_controls.launch_video(os.path.join(common.TEST_VIDEOS_PATH, "{0:.3f}.mp4".format(workload_args[0])),
                                      is_full_screen=full_screen)
            # Move the video player to respective ports in Extended mode
            if current_config.topology == enum.EXTENDED and port != 'DP_A':
                window_helper.drag_app_across_screen('Movies & TV', port, adapter.gfx_index)

        if polling_args is not None:
            logging.info("\tPolling started. Delay= {0}, Offsets= {1}".format(polling_args[1], polling_args[0]))
            polling.start(polling_args[0], polling_args[1])

        if workload == 'APP':
            logging.info("\tPSR utility started")
            utility_timeline, utility_time_stamps = psr_util.run(workload_args[0], wait_time=2500)
            logging.info("\tPSR utility closed")

        if workload == 'VIDEO':
            if workload_args[3] is not None:
                power_source_str = workload_args[3].name
                logging.info(f"changing power source to {power_source_str}")
                if not self.display_power_.set_current_powerline_status(workload_args[3]):
                    self.fail("Failed to switch power line status to {0}(Test Issue)".format(power_source_str))
            if workload_args[2] is True:
                time.sleep(int(workload_args[1] / 2) + 20)
                # Pause
                kb.press(' ')
                time.sleep(5)
                logging.info("\tPaused video for 5 seconds")
                # Play
                kb.press(' ')
                time.sleep(int(workload_args[1] / 2))
            else:
                # Due to Win Qual sighting - DMRRS won't hit for ~20seconds
                time.sleep(workload_args[1] + 20)
        if workload == 'VIDEO_CURSOR':
            # Launch video app in right side and do mouse event in left side of screen
            app_controls.launch_video(
                os.path.join(common.TEST_VIDEOS_PATH, "{0:.3f}.mp4".format(psr.DEFAULT_MEDIA_FPS)),
                is_full_screen=False)
            if panel_index >= 1:
                app_controls.move_windows('Movies & TV', monitor_id_map[port])
            kb.snap_right()
            kb.press("ENTER")
            kb.press("ENTER")
            time.sleep(2)
            sfsu.check_psr_with_util_app(sfsu.EventType.CURSOR_MOVE, panel_index, 10)

        if workload == 'CURSOR':
            sfsu.check_psr_with_util_app(sfsu.EventType.CURSOR_MOVE, panel_index, 20)

        if polling_args is not None:
            polling_timeline, polling_time_stamps = polling.stop()
            logging.info("\tPolling stopped")

        if workload == 'VIDEO' or workload == 'VIDEO_CURSOR':
            window_helper.close_media_player()
            logging.info("\tClosing video playback")

        if etl_tracer.stop_etl_tracer() is False:
            self.fail("Failed to stop ETL Tracer")
        # Un-hiding the task-bar to restore the previous state
        logging.info("Un-hiding the task-bar")
        if window_helper.toggle_task_bar(window_helper.Visibility.SHOW):
            logging.info("\tSuccessfully un-hide the task-bar")
        else:
            logging.warning("\tFAILED to un-hide the task-bar")
        etl_file_path = etl_tracer.GFX_TRACE_ETL_FILE
        if os.path.exists(etl_tracer.GFX_TRACE_ETL_FILE):
            file_name = 'GfxTraceDuringWorkload.' + str(time.time()) + '.etl'
            etl_file_path = os.path.join(test_context.LOG_FOLDER, file_name)
            os.rename(etl_tracer.GFX_TRACE_ETL_FILE, etl_file_path)

        if etl_tracer.start_etl_tracer() is False:
            self.fail("Failed to start ETL Tracer")
        logging.info(f"Applying previous power source {initial_pwr_rsc}")
        if not self.display_power_.set_current_powerline_status(initial_pwr_rsc):
            self.fail("Failed to switch power line status to {0}(Test Issue)".format(initial_pwr_rsc))

        return etl_file_path, (polling_timeline, polling_time_stamps, utility_timeline, utility_time_stamps)

    ##
    # @brief        internal API to verify PSR
    # @return       status True if all PSR verification passed, False otherwise
    def __verify(self):
        status = True
        full_screen = True
        etl_file = None
        new_pwr_src = None
        retry_counter = 0
        system_utility_ = system_utility.SystemUtility()

        logging.info(f"Current power source = {PowerSource(self.power_source).name}")
        monitor_ids = [_[0] for _ in app_controls.get_enumerated_display_monitors()]
        execution_environment = system_utility_.get_execution_environment_type()

        for adapter in dut.adapters.values():
            # From TGL onwards PIPE assignment is dynamic, refresh panel caps after mode set/power event/driver restart
            if adapter.lfp_count > 1:
                dut.refresh_panel_caps(adapter)
            monitor_id_map = self.__get_monitor_id_map(adapter, monitor_ids)
            for panel in adapter.panels.values():
                feature, feature_str = self.get_feature(adapter)
                logging.info(f"validating feature = {feature_str}")
                # During Dual EDP -> SD EDP_A config switch, EDP_B becomes inactive
                # Make sure PSR verify called only for active displays in topology
                if panel.is_active is False:
                    continue
                if panel.psr_caps.is_psr_supported is False and panel.pr_caps.is_pr_supported is False:
                    continue
                # SFSU will not be enabled for non-MDS modes. Skipping SFSU verification for the same
                if feature > psr.UserRequestedFeature.PSR_1:
                    mode = self.display_config_.get_current_mode(panel.target_id)
                    if mode.scaling != enum.MDS:
                        logging.info(f"Skipping {feature_str} verification for Non-MDS mode")
                        continue
                # PSR is supported only on Pipe-A and Pipe-B
                if panel.psr_caps.is_psr_supported:
                    if panel.pipe not in ['A', 'B']:
                        logging.warning(f"Skipping the verification as PSR is not supported on Pipe-{panel.pipe}.")
                        continue
                    status = psr.verify_psr_setup_time(adapter, panel, self.feature)
                    if status is None:
                        continue
                    elif status is False:
                        self.fail("PSR restriction check failed")
                if panel.pr_caps.is_pr_supported and panel.is_lfp and feature == psr.UserRequestedFeature.PANEL_REPLAY:
                    restriction = pr.verify_pr_timing_support(adapter, panel)
                    if restriction is None:
                        logging.info(f"Timing not supported. Skipping PR check on {panel.port}")
                        continue
                if psr.UserRequestedFeature.PSR_2 <= feature < psr.UserRequestedFeature.PANEL_REPLAY:
                    psr2_support = self.is_psr2_possible(adapter, panel)
                    restriction = psr.verify_psr2_vblank_support(adapter, panel)
                    # Hblank restrictions are applicable only for ADL-P
                    if adapter.name in common.GEN_13_PLATFORMS:
                        restriction &= psr.verify_psr2_hblank_requirement(adapter, panel)
                    if (psr2_support is False) or (restriction is False):
                        feature = psr.UserRequestedFeature.PSR_1
                        feature_str = psr.UserRequestedFeature(feature).name
                logging.info("Step: Verifying {0} on {1} on for {2}".format(feature_str, panel, adapter.name))
                while True:
                    if psr.is_psr_enabled_in_driver(adapter, panel, feature) is True:
                        break
                    else:
                        retry_counter += 1
                        logging.debug(f"{feature_str} is not enabled in driver, trying again..")
                        time.sleep(1)

                    if retry_counter > 2:
                        gdhm.report_driver_bug_pc(f"[Powercons][PSR] {feature_str} is not enabled in the driver")
                        logging.error(f"\t{feature_str} is not enabled in driver")
                        return False
                # Get list of offsets to poll during workload (app or video or idle desktop)
                offsets = psr.get_polling_offsets(feature)
                if self.method in ['VIDEO', 'CURSOR', 'VIDEO_CURSOR']:
                    # change the power source
                    if self.toggle_power_source:
                        if self.power_source == PowerSource.DC:
                            new_pwr_src = PowerSource.AC
                        else:
                            new_pwr_src = PowerSource.DC
                    # For FFSU/SFSU video playback should be in windowed mode
                    if feature > psr.UserRequestedFeature.PSR_2 and self.toggle_power_source is False:
                        full_screen = False
                    etl_file, polling_data = self.__get_workload_traces(
                        self.method,
                        [psr.DEFAULT_MEDIA_FPS, psr.DEFAULT_PLAYBACK_DURATION, self.is_pause_video_test,
                         new_pwr_src],
                        [offsets, psr.DEFAULT_POLLING_DELAY], monitor_id_map, panel.port, full_screen=full_screen,
                        adapter=adapter)
                else:
                    if execution_environment in ["SIMENV_PIPE2D"]:
                        logging.info(f"Step: Verifying {feature_str} in {execution_environment} environment")
                        status = psr.verify_pre_si(feature, monitor_ids)
                        if status is True:
                            logging.info(f"Step: Verifying {feature_str} in {execution_environment} environment")
                        else:
                            logging.error(
                                f"\tFAIL: {feature_str} verification failed in {execution_environment} environment")
                        return status
                    else:
                        etl_file, polling_data = self.__get_workload_traces(
                            'APP', [[monitor_id_map[panel.port]]], [offsets, psr.DEFAULT_POLLING_DELAY], monitor_id_map,
                            panel.port, full_screen=full_screen, adapter=adapter)

                is_vsync_disable_expected = False
                current_config = self.display_config_.get_current_display_configuration()
                # VSYNC disable calls are expected in the following scenarios :-
                #       - Display Switch scenarios in EXTENDED mode - Video Player will be dragged across the screens and one of the screens can be in deep sleep
                #       - Full screen video playback scenario - Video Player will be switched from Windowed to Full Screen mode
                # As the PSR might get into Deep Sleep and then goes into Idle state in the mentioned scenarios, we should skip Idle state check and Deep sleep checks during VPB
                if self.method in ['VIDEO'] and ((self.toggle_power_source is True) or (current_config.topology == enum.EXTENDED)):
                    is_vsync_disable_expected = True

                if (self.toggle_power_source is False) or (new_pwr_src is None):
                    new_pwr_src = self.power_source
                dpst_enable = is_dpst_possible(panel, new_pwr_src)
                if self.method in ['APP', 'VIDEO'] and common.IS_PRE_SI is False:
                    if psr.verify(adapter, panel, feature, etl_file, polling_data, self.method,
                                  self.is_pause_video_test, is_vsync_disable_expected=is_vsync_disable_expected) is False:
                        logging.error("\tFAIL: {0} verification failed on {1}".format(feature_str, panel))
                        status = False
                    else:
                        logging.info("\tPASS: {0} verification passed on {1}".format(feature_str, panel))
                if feature == psr.UserRequestedFeature.PANEL_REPLAY:
                    if panel.is_lfp:
                        restriction = pr.verify_pr_timing_support(adapter, panel)
                        if restriction is None:
                            logging.info(f"Timing not supported. Skipping PR check on {panel.port}")
                            continue
                        elif restriction is False:
                            self.fail("PR restriction check failed")
                    status &= pr.verify(adapter, panel)
                if psr.UserRequestedFeature.PSR_2 <= feature < psr.UserRequestedFeature.PANEL_REPLAY:
                    if sfsu.verify_sfsu(adapter, panel, etl_file, self.method, feature, dpst_enable) is False:
                        status = False
                if psr.is_psr_enabled_in_driver(adapter, panel, feature) is False:
                    logging.error(f"\t{feature_str} is disabled after workload {self.method}")
                    status = False
        return status

    ##
    # @brief        Exposed function to get the supported psr feature based on the platform.
    # @param[in]    adapter Adapter
    # @return       tuple of feature, feature name
    def get_feature(self, adapter):
        feature = self.feature
        if psr.UserRequestedFeature.PSR_2 <= feature < psr.UserRequestedFeature.PANEL_REPLAY:
            if adapter.name not in common.PRE_GEN_12_PLATFORMS:
                display_pc = registry.DisplayPcFeatureControl(adapter.gfx_index)
                if display_pc.DisableSelectiveFetch == 1:
                    logging.info("Selective Fetch is currently disabled in DisplayPCFeatureControl")
                    feature = psr.UserRequestedFeature.PSR2_FFSU
                else:
                    # For all Gen12+ platforms SFSU is default
                    feature = psr.UserRequestedFeature.PSR2_SFSU
        return feature, psr.UserRequestedFeature(feature).name

    ##
    # @brief        Internal Helper Function to get monitor id map
    # @param[in]    adapter Adapter
    # @param[in]    monitor_ids list of the monitor id's
    # @return       mapping dictionary {port: _id}
    def __get_monitor_id_map(self, adapter, monitor_ids):
        current_config = self.display_config_.get_current_display_configuration()
        if current_config.topology == enum.CLONE:
            mapping = {panel.port: monitor_ids[0] for panel in adapter.panels.values()}
        else:
            panel_list = [panel.port for panel in adapter.panels.values() if panel.is_active]
            mapping = {port: _id for (port, _id) in zip(panel_list, monitor_ids)}

        return mapping

    ##
    # @brief        Function to check if PSR2 is supported on the panel based on the platform
    # @param[in]    adapter Adapter
    # @param[in]    panel Panel
    # @return       True if PSR2 is supported, False otherwise
    @staticmethod
    def is_psr2_possible(adapter, panel):
        # PSR2 is supported only on PIPE A in PRE_Gen12 + DG2. Otherwise it will fallback to PSR1
        if adapter.name in common.PRE_GEN_12_PLATFORMS + common.GEN_12_PLATFORMS + ['DG2'] and panel.pipe != 'A' and \
                panel.psr_caps.is_psr2_supported:
            return False
        return True


##
# @brief        Function to check if dpst is enabled
# @param[in]    panel Panel
# @param[in]    power_source enum member of PowerSource
# @return       True if DPST is enabled, False otherwise
def is_dpst_possible(panel, power_source):
    # check DPST restrictions
    if panel.bpc < 8 or power_source == PowerSource.AC:
        return False
    return True