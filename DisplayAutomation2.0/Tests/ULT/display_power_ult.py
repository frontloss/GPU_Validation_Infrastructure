############################################################################################################
# @file
# @brief This will show how to use APIs exposed from display_power.py
# @author Vinod D S, Beeresh
############################################################################################################

import os
import logging
import unittest

from Tests.ULT.system_utility_ult import is_postSi

from Libs.Core import test_header
from Libs.Core.display_power import *
from Libs.Core.gta import gta_state_manager
from Libs.Core.test_env.test_environment import *


class DisplayPowerUlt(unittest.TestCase):
    ##
    # Create DisplayPower object
    disp_power = DisplayPower()
    test_status = True
    log_handle = None

    def setUp(self):
        if self._testMethodName == "test_0_3_check_power_scheme":
            self.log_handle = None
        else:
            log_file = os.path.basename(__file__)
            self.log_handle = display_logger.add_file_handler(log_file)

    @unittest.skipUnless(is_postSi(), "Not supported on PreSi environment")
    def test_0_1_check_power_scheme(self):
        # Get Power Scheme
        pwr_scheme = self.disp_power.get_current_power_scheme()
        logging.info("Current Power Scheme = %s",pwr_scheme.name)

        # Set Power Scheme
        if self.disp_power.set_current_power_scheme(PowerScheme.BALANCED):
            logging.info("Switch Power scheme is successful for BALANCED")
        else:
            logging.error("Switch Power scheme is failed for BALANCED")
            self.test_status = False

    @unittest.skipUnless(is_postSi(), "Not supported on PreSi environment")
    def test_0_2_invoke_power_event_S3(self):
        if self.disp_power.is_power_state_supported(PowerEvent.S3) is False:
            logging.info("S3 is not supported")
            return

        if self.disp_power.invoke_power_event(PowerEvent.S3, 60) is False:
            self.test_status = False

    @unittest.skipUnless(is_postSi(), "Not supported on PreSi environment")
    def test_0_3_verify_monitor_turnoff(self):
        ##
        # Check whether system supports CS
        is_cs_supported = self.disp_power.is_power_state_supported(PowerEvent.CS)
        if is_cs_supported:
            logging.info("CS Supported")
        else:
            logging.info("CS Not Supported")

        if not is_cs_supported:
            ##
            # Monitor Turnoff
            if self.disp_power.invoke_monitor_turnoff(MonitorPower.OFF_ON, 30) is False:
                self.test_status = False
            time.sleep(20)

    @unittest.skipUnless(is_postSi(), "Not supported on PreSi environment")
    def test_0_4_lid_switch_power_state(self):
        ##
        # Get the lid switch supported or not
        if self.disp_power.is_lid_present():
            logging.info("Lid switch supported")

            ##
            # Set the power state for the lid switch
            if self.disp_power.set_lid_switch_power_state(
                    LidSwitchOption.DO_NOTHING,
                    power_plan=self.disp_power.get_current_power_scheme()
            ):
                logging.info("Set lid switch power state is success for LIDSWITCH_DONOTHING")
            else:
                self.fail("Set lid switch power state is failed for LIDSWITCH_DONOTHING")

            ##
            # Get the power state for the lid switch
            lid_switch_power_state = self.disp_power.get_lid_switch_power_state(
                power_plan=self.disp_power.get_current_power_scheme()
            )
            if lid_switch_power_state is not None:
                logging.info("Get lid switch power state is success: %s",lid_switch_power_state.name)
            else:
                self.fail("Getting lid switch power state is failed")
        else:
            logging.info("Lid switch not supported")

    @unittest.skipUnless(is_postSi(), "Not supported on PreSi environment")
    def test_0_5_power_line_status(self):
        if self.disp_power.is_wdtf_installed() is False:
            logging.error("WDTF is not installed")
            self.test_status = False
        else:
            logging.info("WDTF is installed")

            if self.disp_power.enable_disable_simulated_battery(True) is False:
                logging.error("Enable simulated battery: failed")
                self.test_status = False
            else:
                logging.info("Enable simulated batter: success")
                ##
                # Get power line status
                power_line_status = self.disp_power.get_current_powerline_status()
                if power_line_status == PowerSource.INVALID.value:
                    logging.error("Getting current Power Line status is failed")
                    self.test_status = False
                else:
                    logging.info("Get power line status success: %s", power_line_status.name)

                if power_line_status == PowerSource.DC.value:
                    power_line_status = PowerSource.AC
                else:
                    power_line_status = PowerSource.DC
                ##
                # Set current power line status
                if self.disp_power.set_current_powerline_status(power_line_status) is False:
                    self.test_status = False

                new_power_line_status = self.disp_power.get_current_powerline_status()
                if new_power_line_status != power_line_status:
                    logging.error("Power Line status set failed")
                    self.test_status = False
                else:
                    logging.info("New power line state is: %s", PowerSource(new_power_line_status).name)

                if self.disp_power.enable_disable_simulated_battery(False) is False:
                    logging.error("Failed to disable simulated battery")
                    self.test_status = False
                else:
                    logging.info("Disable simulated battery: success")

    @unittest.skipUnless(is_postSi(), "Not supported on PreSi environment")
    def test_0_6_invoke_power_event_CS(self):
        if self.disp_power.is_power_state_supported(PowerEvent.CS) is False:
            logging.info("CS is not supported")
            return

        if self.disp_power.invoke_power_event(PowerEvent.CS, 60) is False:
            self.test_status = False

    def test_0_8_wake_timers(self):
        ##
        # Set the wake timers
        if self.disp_power.set_wake_timers(WakeTimersStatus.IMPORTANT_WAKE_TIMERS_ONLY):
            logging.info("Set wake timers is success for IMPORTANT_WAKE_TIMERS_ONLY")
        else:
            self.fail("Set wake timers state is failed for IMPORTANT_WAKE_TIMERS_ONLY")

        ##
        # Get wake timers
        wake_timers_setting = self.disp_power.get_wake_timers()
        if wake_timers_setting is not None:
            logging.info("Get wake timers is success: %s", WakeTimersStatus(wake_timers_setting).name)
        else:
            self.fail("Getting wake timers is failed")

    def tearDown(self):
        if self.log_handle:
            self.log_handle.flush()
            self.log_handle.close()
            logging.getLogger().removeHandler(self.log_handle)

        if self.test_status is False:
            self.fail("Display Power ULT failed, refer the error(s) in log file")


if __name__ == '__main__':
    TestEnvironment.load_dll_module()
    display_logger._initialize(console_logging=True)
    gta_state_manager.create_gta_default_state()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    status = test_header.cleanup(outcome.result)
    gta_state_manager.update_test_result(outcome.result, status)
    display_logger._cleanup()
