########################################################################################################################
# @file         test_display_switch.py
# @brief        Contains display switch functional tests for VRR
# @details      Display switch functional tests are covering below scenarios:
#               * VRR verification in WINDOWED modes with LOW_HIGH_FPS settings in multiple display modes.
#               * All tests will be executed on VRR/NON VRR panel with VRR enabled. VRR is expected to be working in
#               Vrr supported panel in all above scenarios.
#
# @author       Nainesh Doriwala
########################################################################################################################

from Libs.Core import enum, window_helper
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.PowerCons.Functional.DMRRS import dmrrs
from Tests.VRR.vrr_base import *


##
# @brief        This class contains Display modes functional tests. This class inherits the VrrBase class.
#               Tests verify VRR in WINDOWED and FULL_SCREEN mode with different FPS settings in different display
#               modes.
class TestDisplaySwitch(VrrBase):
    status = True

    ############################
    # Test Function
    ############################

    ##
    # @brief        VRR verification in WINDOWED mode with LOW_HIGH_FPS setting
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["LOW_HIGH_FPS"])
    # @endcond
    def t_41_display_switch_windowed(self):
        panel_list = []
        for adapter in dut.adapters.values():
            panel_list = list(adapter.panels.values())
            break
        if len(panel_list) < 2:
            self.fail("invalid display passed, command line require two display")
        # Updating setup config before running test case to avoid sporadic failure

        # Apply Single display - Display 1 and apply native mode
        if self.display_config_.set_display_configuration_ex(enum.SINGLE, [panel_list[0].port]) is False:
            self.fail("Applying Display config SINGLE Failed"
                      .format("SINGLE" + " " + " ".join(str(x) for x in [panel_list[0].port])))
        logging.info("Applying Display config {0}"
                         .format("SINGLE" + " " + " ".join(str(x) for x in [panel_list[0].port])))
        if self.display_config_.set_display_mode([panel_list[0].native_mode], False) is False:
            assert False, "Failed to set native display mode (Test Issue)"
        logging.info(f"\tSuccessfully applied native mode on {panel_list[0].port}")
        # Apply ED mode with Display 2 + Display 1 and apply native on both panel
        if self.display_config_.set_display_configuration_ex(enum.EXTENDED, [panel_list[1].port,
                                                                             panel_list[0].port]) is False:
            self.fail("Applying Display config {0} Failed"
                      .format("EXTENDED" + " " + " ".join(str(x) for x in [panel_list[1].port,
                                                                                   panel_list[0].port])))
        if self.display_config_.set_display_mode([panel_list[0].native_mode], False) is False:
            assert False, "Failed to set native display mode (Test Issue)"
        logging.info(f"\tSuccessfully applied native mode on {panel_list[0].port}")
        if self.display_config_.set_display_mode([panel_list[1].native_mode], False) is False:
            assert False, "Failed to set native display mode (Test Issue)"
        logging.info(f"\tSuccessfully applied native mode on {panel_list[1].port}")

        # Apply SD display 2 and apply native mode on display 2
        if self.display_config_.set_display_configuration_ex(enum.SINGLE, [panel_list[1].port]) is False:
            self.fail("Applying Display config {0} Failed"
                      .format("SINGLE" + " " + " ".join(str(x) for x in [panel_list[1].port])))
        logging.info("Applying Display config {0}"
                     .format("SINGLE" + " " + " ".join(str(x) for x in [panel_list[1].port])))
        if self.display_config_.set_display_mode([panel_list[1].native_mode], False) is False:
            assert False, "Failed to set native display mode (Test Issue)"
        logging.info(f"\tSuccessfully applied native mode on {panel_list[1].port}")
        logging.info("******* pre-requisite end for modeset*********")
        # Apply Single display Display 1 and verify VRR for single Display 1.
        if self.display_config_.set_display_configuration_ex(enum.SINGLE, [panel_list[0].port]) is False:
            self.fail("Applying Display config {0} Failed"
                      .format("SINGLE" + " " + " ".join(str(x) for x in [panel_list[0].port])))
        logging.info("Applying Display config {0}"
                     .format("SINGLE" + " " + " ".join(str(x) for x in [panel_list[0].port])))

        etl_file, _ = workload.run(workload.GAME_PLAYBACK, [self.app, self.duration, True, None, None, None])
        self.status &= self.verify_vrr_for_each_panel(etl_file)
        if self.status is False:
            self.fail("VRR verification failed in FULL_SCREEN mode with LOW_HIGH_FPS setting for single display "
                      "{}".format(panel_list[0].port))
        logging.info("PASS: VRR verification passed successfully in FULL_SCREEN mode for single display"
                     "{}".format(panel_list[0].port))


        '''@ todo currently failing if we drag from EDP to External DP due to OS is not sending VRR flip.
        ##
        # Run Workload on single display 1 and then Apply ED.
        # Drag application from display 1 to display 2 and run application on display 2 for 30sec.
        # Close existing running Workload and then verify VRR on both display.

        # Run workload and don't close workload
        status , _ = workload.run(workload.GAME_PLAYBACK_WITH_CUSTOM_EVENTS, 
                                  [self.app, self.duration, False, False, True, None])
        if not status:
            self.fail("Failed to run workload")
        # Apply Extended display with Display 1 and display 2
        if self.display_config_.set_display_configuration_ex(enum.EXTENDED, [panel_list[0].port,
                                                                             panel_list[1].port]) is False:
            self.fail("Applying Display config {0} Failed"
                      .format(str(enum.EXTENDED) + " " + " ".join(str(x) for x in [panel_list[0].port, 
                      panel_list[1].port])))
        # 10 sec delay to run application on display 1
        time.sleep(10)
        # Move Classic3D application from display 1 to display 2
        window_helper.drag_app_across_screen('ClassicD3D', panel_list[1].port, "gfx_0")
        
        # 30 sec delay to run application on display 2
        time.sleep(30)
        
        # Close Running classic3d Application
        status, etl_file = workload.run(workload.GAME_PLAYBACK_WITH_CUSTOM_EVENTS,
                                [self.app, self.duration, False, True, False, None])
        if not status or etl_file is None:
            self.fail("Failed to close workload or fail to generate etl file")

        # verify VRR on both panel.
        self.status &= self.verify_vrr_for_each_panel(etl_file)
        if self.status is False:
            self.fail("VRR verification failed in FULL_SCREEN mode with LOW_HIGH_FPS setting for extended display "
                      "{} + {}".format(panel_list[0].port, panel_list[1].port))
        logging.info("PASS: VRR verification passed successfully in FULL_SCREEN mode for single display"
                     "{} + {}".format(panel_list[0].port, panel_list[1].port))]'''

        ##
        # Apply ED mode with Display 2 + Display 1 and launch workload without closing it.
        # Drag application from display 2 to display 1 and run application on display 1 for 30sec.
        # Close existing running Workload and then verify VRR on both display.

        # Apply ED mode with Display 2 + Display 1
        if self.display_config_.set_display_configuration_ex(enum.EXTENDED, [panel_list[1].port,
                                                                             panel_list[0].port]) is False:
            self.fail("Applying Display config {0} Failed"
                      .format("EXTENDED" + " " + " ".join(str(x) for x in [panel_list[1].port,
                                                                                   panel_list[0].port])))
        # launch workload
        status, _ = workload.run(workload.GAME_PLAYBACK_WITH_CUSTOM_EVENTS, [self.app, self.duration, False, False,
                                                                             True, None])
        if not status:
            self.fail("Failed to run workload")

        # running content for 10sec on display 2
        time.sleep(10)

        # drag workload from display 2 to display 1.
        window_helper.drag_app_across_screen('ClassicD3D', panel_list[0].port, "gfx_0")

        # running content for 30sec on display 1
        time.sleep(30)

        # Close Running classic3d Application
        status, etl_file = workload.run(workload.GAME_PLAYBACK_WITH_CUSTOM_EVENTS,
                                        [self.app, self.duration, False, True, False, None])

        if not status or etl_file is None:
            self.fail("Failed to close workload or fail to generate etl file")

        # verify VRR on both panel.
        self.status &= self.verify_vrr_for_each_panel(etl_file)
        if self.status is False:
            self.fail("VRR verification failed in FULL_SCREEN mode with LOW_HIGH_FPS setting for extended display "
                      "{} + {}".format(panel_list[1].port, panel_list[0].port))
        logging.info("PASS: VRR verification passed successfully in FULL_SCREEN mode for extended display"
                     "{} + {}".format(panel_list[1].port, panel_list[0].port))

        ##
        # Run Workload and then Apply SD display 2
        # Close existing running Workload and then verify VRR on display 2 display.

        # Run workload and don't close workload
        status, _ = workload.run(workload.GAME_PLAYBACK_WITH_CUSTOM_EVENTS,
                                 [self.app, self.duration, False, False, True, None])
        if not status:
            self.fail("Failed to run workload")

        # Apply SD display 2
        if self.display_config_.set_display_configuration_ex(enum.SINGLE, [panel_list[1].port]) is False:
            self.fail("Applying Display config {0} Failed"
                      .format("SINGLE" + " " + " ".join(str(x) for x in [panel_list[1].port])))
        logging.info("Applying Display config {0}"
                     .format("SINGLE" + " " + " ".join(str(x) for x in [panel_list[1].port])))

        # Close Running classic3d Application
        status, etl_file = workload.run(workload.GAME_PLAYBACK_WITH_CUSTOM_EVENTS,
                                        [self.app, self.duration, False, True, False, None])

        if not status or etl_file is None:
            self.fail("Failed to close workload or fail to generate etl file")

        # verify VRR on both panel.
        self.status &= self.verify_vrr_for_each_panel(etl_file)
        if self.status is False:
            self.fail("VRR verification failed in FULL_SCREEN mode with LOW_HIGH_FPS setting for single display "
                      "{}".format(panel_list[1].port))
        logging.info("PASS: VRR verification passed successfully in FULL_SCREEN mode for single display"
                     "{}".format(panel_list[1].port))

        # apply Extended mode for proper tear down and make both display active. s
        self.display_config_.set_display_configuration_ex(enum.EXTENDED, [panel_list[1].port, panel_list[0].port])

    ##
    # @brief        Verify VRR for each connected panel
    # @param[in]    etl_file
    # @return       True if verification pass else False
    @staticmethod
    def verify_vrr_for_each_panel(etl_file):
        is_os_aware_vrr = dut.WIN_OS_VERSION >= dut.WinOsVersion.WIN_19H1
        # verify
        status = True
        for adapter in dut.adapters.values():
            if adapter.is_vrr_supported is False:
                continue
            dut.refresh_panel_caps(adapter)
            for panel in adapter.panels.values():
                expected_vrr = True if panel.vrr_caps.is_vrr_supported else False
                negative = False if panel.vrr_caps.is_vrr_supported else True
                if display_config.is_display_active(panel.port, panel.gfx_index):
                    status &= vrr.verify(adapter, panel, etl_file, None, negative, is_os_aware_vrr, expected_vrr, True)
        return status


if __name__ == '__main__':
    TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(TestDisplaySwitch))
    TestEnvironment.cleanup(test_result)
