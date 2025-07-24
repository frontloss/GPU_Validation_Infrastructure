##
# @file         detachable_LFP_power_events.py
# @brief        Contains test cases that covers various power events.
# @details      cmd_line:
#               test_display_python_automation Tests\LFP_Common\Detachable_LFP\detachable_LFP_power_events.py
#               -edp_A SINK_EDP012 VBT_INDEX_0 -MIPI_C  SINK_MIP002 VBT_INDEX_1 -power_state s5 -detach_LFP MIPI_C
# @author       Goutham N
from Libs.Core import display_power
from Tests.LFP_Common.Detachable_LFP.detachable_LFP_base import *


##
# @brief        This class is for performing various power events like S3, S4 and S5
#               that inherits DetachableLFPBase for setup and _setHPD functionality.
class DetachableLFPPowerEvents(DetachableLFPBase):
    ##
    # @brief        This method goes to specified power state
    #               and wakes up and then verifies if displays are enumerated after that.
    # @param[in]    power_state: str
    # @return       None
    def goto_powerstate_and_verify(self, power_state) -> bool:
        """
        WARM_UP required only for GTA environment.
         Due to multiple power cycles, heart beat of DUT will not reach runner within expected time frame and GTA Runner will
         interpret DUT as unreacheable and will abort the JOB.
        """
        self.POWER_CYCLE_WARM_UP_TIME = 60

        """
        Duration in seconds, DUT will be in specified power state for that duration.
        """
        self.POWER_CYCLE_DURATION = 60

        disp_power = DisplayPower()
        if power_state == 's3' and disp_power.is_power_state_supported(display_power.PowerEvent.S3):
            disp_power.invoke_power_event(display_power.PowerEvent.S3, self.POWER_CYCLE_DURATION)
        elif power_state == 's3' and disp_power.is_power_state_supported(display_power.PowerEvent.CS):
            disp_power.invoke_power_event(display_power.PowerEvent.CS, self.POWER_CYCLE_DURATION)
        elif power_state == 's4':
            disp_power.invoke_power_event(display_power.PowerEvent.S4, self.POWER_CYCLE_DURATION)
        elif power_state == 's5':
            ##
            # Invoke S5 power event
            logging.info("Step: Triggering power event POWER_STATE_S5 for {0} seconds".format(
                common.POWER_EVENT_DURATION_DEFAULT))
            if reboot_helper.reboot(self, callee="runTest") is False:
                self.fail("Failed to reboot the system(Test Issue)")
        else:
            logging.info(power_state)
            self.fail("FAIL: unknown power state")
        time.sleep(self.POWER_CYCLE_WARM_UP_TIME)

        enumerated_displays = DisplayConfiguration().get_enumerated_display_info()
        # printing enumerated displays info
        logging.debug('Enumerated display information: {}'.format(enumerated_displays.to_string()))
        # Checking if display is attached/detached
        ret = display_config.is_display_attached(enumerated_displays, self.port_to_detach)
        return ret

    ##
    # @brief        Performs various power events like S3, S4 and S5
    #               that inherits DetachableLFPBase for setup and _setHPD functionality
    # @return       None
    def runTest(self) -> None:
        # Reboot Scenario
        if reboot_helper.is_reboot_scenario() is True and self.power_state == 's5':
            logging.info("\tResumed from the power event POWER_STATE_S5 successfully")

            enumerated_displays = DisplayConfiguration().get_enumerated_display_info()
            # printing enumerated displays info
            logging.debug('Enumerated display information: {}'.format(enumerated_displays.to_string()))
            # Checking if display is attached/detached
            is_display_attached = display_config.is_display_attached(enumerated_displays, self.port_to_detach)
            if self.plug_status == True:
                # This is done because, In EDP case, LFP_2 will be enumerated after resuming from S5
                # whereas in MIPI case, LFP_2 is not enumerated after resuming from S5.
                if self.edp_as_companion_display:
                    if is_display_attached:
                        logging.info("PASS: LFP_2 is enumerated after resume from " + self.power_state + " state.")
                    else:
                        self.fail("FAIL: LFP_2 is not enumerated after resume from " + self.power_state + " state. ")
                else:
                    if not is_display_attached:
                        logging.info("PASS: LFP_2 is not enumerated after resume from " + self.power_state + " state.")
                    else:
                        self.fail("FAIL: LFP_2 is enumerated after resume from " + self.power_state + " state. ")
            else:
                if self.edp_as_companion_display:
                    if not is_display_attached:
                        logging.info("PASS: LFP_2 is not enumerated after resume from " + self.power_state + " state.")
                    else:
                        self.fail("FAIL: LFP_2 is enumerated after resume from " + self.power_state + " state. ")

            if self.plug_status == True and self.edp_as_companion_display:
                # unplug and trigger reboot
                # Checking only for EDP case. For MIPI case NA.
                logging.info("Hot unplugging LFP_2...")
                adapter_info = TestContext.get_gfx_adapter_details()[self.gfx_index]
                res = DriverInterface().simulate_unplug(adapter_info, self.mapped_port_to_detach, False,
                                                           self.port_type)
                # res = self._setHPD(self.mapped_port_to_detach, False, self.port_type, self.gfx_index)
                if res is False:
                    self.fail(f"FAIL: HPD-unplug failed on port={self.port_to_detach}")
                else:
                    logging.info(f"PASS: HPD-unplug successful on port={self.port_to_detach}")
                    self.plug_status = False
                # Delay
                status = self._dynamic_delay(self.port_to_detach, plug=False)
                self.assertTrue(status,
                                f"[Test Issue] - Timeout reached! Display is still enumerated on port "
                                f"{self.port_to_detach}")
                ret = self.goto_powerstate_and_verify(self.power_state)
            return

        # Non Reboot Scenario
        ##
        # Hot plugging LFP_2 and stress test power events
        logging.info("Hot plugging LFP_2...")
        res = self._setHPD(self.mapped_port_to_detach, True, self.port_type, self.gfx_index)
        if res is False:
            self.fail(f"FAIL: HPD-plug failed on port={self.port_to_detach}")
        else:
            logging.info(f"PASS: HPD-plug successful on port={self.port_to_detach}")
            self.plug_status = True
        # Delay
        status = self._dynamic_delay(self.port_to_detach, plug=True)
        self.assertTrue(status,
                        f"[Test Issue] - Timeout reached! Display is not enumerated on port "
                        f"{self.port_to_detach}")

        for i in range(0, self.iterations):
            ##
            # goto power state state and wake up. Expected result :- LFP_1+LFP_2 should be enumerated.
            logging.info("Iteration: " + str(i))
            ret = self.goto_powerstate_and_verify(self.power_state)

            if ret is False:
                self.fail(
                    "FAIL: LFP_2 is plugged but LFP_2 is not enumerated after resume from " +
                    self.power_state + " state.")
            else:
                logging.info(
                    "PASS: LFP_2 is plugged and LFP_2 successfully enumerated after resume from  " +
                    self.power_state + " state as expected.")

        ##
        # Hot unplugging and stress test power events
        logging.info("Hot unplugging LFP_2...")
        res = self._setHPD(self.mapped_port_to_detach, False, self.port_type, self.gfx_index)
        if res is False:
            self.fail(f"FAIL: HPD-unplug failed on port={self.port_to_detach}")
        else:
            logging.info(f"PASS: HPD-unplug successful on port={self.port_to_detach}")
        # Delay
        status = self._dynamic_delay(self.port_to_detach, plug=False)
        self.assertTrue(status,
                        f"[Test Issue] - Timeout reached! Display is still enumerated on port "
                        f"{self.port_to_detach}")
        for i in range(0, self.iterations):
            logging.info("Iteration: " + str(i))
            ##
            # goto power state and wake up. Expected result :-
            # LFP_2 should not be enumerated because LFP_2 is detached this time.
            ret = self.goto_powerstate_and_verify(self.power_state)

            if ret is False:
                logging.info(
                    "PASS: LFP_2 is unplugged this time and LFP_2 is not enumerated after resume from  "
                    + self.power_state + " state as expected.")
            else:
                self.fail(
                    "FAIL: LFP_2 is unplugged this time but LFP_2 enumerated after resume from  "
                    + self.power_state + " state.")


if __name__ == '__main__':
    TestEnvironment.initialize()
    results = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('DetachableLFPPowerEvents'))
    TestEnvironment.cleanup(results)
