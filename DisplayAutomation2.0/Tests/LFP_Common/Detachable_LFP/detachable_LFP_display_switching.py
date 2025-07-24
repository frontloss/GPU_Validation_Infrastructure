##
# @file         detachable_LFP_display_switching.py
# @brief        Test covers display switching from SD to ED and vice versa.
# @details      cmd_line:
#               test_display_python_automation Tests\LFP_Common\Detachable_LFP\detachable_LFP_display_switching.py
#               -edp_A SINK_EDP012 VBT_INDEX_0 -MIPI_C SINK_MIP002 VBT_INDEX_1 -detach_LFP MIPI_C -repeat 5
# @author       Goutham N

from Tests.LFP_Common.Detachable_LFP.detachable_LFP_base import *


##
# @brief        This class applies single display configuration
#               then does a unplug and plug then applies extended display configuration for n iterations.
class DetachableLFPDisplaySwitching(DetachableLFPBase):
    ##
    # @brief    This function performs display switching from SD to ED and vice versa.
    # @return   None
    def runTest(self) -> None:
        ##
        # N iterations
        for i in range(0, self.iterations):
            ##
            # plugging and performing display switch from Single Display to Extended and vice versa
            logging.info("Iteration:- " + str(i))

            # Hot plug LFP_2 and verify single display configuration on LFP2.
            logging.info("hot plugging LFP_2...")
            res = self._setHPD(self.mapped_port_to_detach, True, self.port_type, self.gfx_index)
            if res is False:
                logging.error(f"FAIL: HPD-plug failed on port={self.port_to_detach}")
            else:
                logging.info(f"PASS: HPD-plug is successful on port={self.port_to_detach}")
            # Delay
            status = self._dynamic_delay(self.port_to_detach, plug=True)
            self.assertTrue(status,
                            f"[Test Issue] - Timeout reached! Display is not enumerated on port "
                            f"{self.port_to_detach}")

            logging.info("Applying Single Display Configuration...")
            config = enum.SINGLE
            enumerated_displays = DisplayConfiguration().get_enumerated_display_info()
            # printing enumerated displays info
            logging.debug('Enumerated display information: {}'.format(enumerated_displays.to_string()))
            # Checking if display is attached/detached
            if DisplayConfiguration().set_display_configuration_ex(config,
                                                                   [self.port_to_detach],
                                                                   enumerated_displays) is False:
                self.fail(f'Failed to set the display configuration as SD {self.port_to_detach}')
            logging.info(f'Successfully set the display configuration as SD {self.port_to_detach}')
            ##
            # checking if display is enumerated after setting single display config.
            enumerated_displays = DisplayConfiguration().get_enumerated_display_info()
            # printing enumerated displays info
            logging.debug('Enumerated display information: {}'.format(enumerated_displays.to_string()))
            # Checking if display is attached/detached
            ret = display_config.is_display_attached(enumerated_displays, self.port_to_detach)
            if ret is False:
                logging.info("FAIL: LFP_2 is plugged but LFP_2 is not enumerated.")
            else:
                logging.info("PASS: LFP_2 is plugged and LFP_2 successfully enumerated.")

            ##
            # unplug and plug back LFP_2, then verify extended display configuration.
            logging.info("Hot unplugging LFP_2...")
            res = self._setHPD(self.mapped_port_to_detach, False, self.port_type, self.gfx_index)
            if res is False:
                logging.error(f"FAIL: HPD-unplug failed on port={self.port_to_detach}")
            else:
                logging.info(f"PASS: HPD-unplug successful on port={self.port_to_detach}")
            logging.info("Hot plugging LFP_2")
            # Delay
            status = self._dynamic_delay(self.port_to_detach, plug=False)
            self.assertTrue(status,
                            f"[Test Issue] - Timeout reached! Display is still enumerated on port "
                            f"{self.mapped_port_to_detach}")

            res = self._setHPD(self.mapped_port_to_detach, True, self.port_type, self.gfx_index)
            if res is False:
                logging.error(f"FAIL: HPD-plug failed on port={self.port_to_detach}")
            else:
                logging.info(f"PASS: HPD-plug successful on port={self.port_to_detach}")
            # Delay
            status = self._dynamic_delay(self.port_to_detach, plug=True)
            self.assertTrue(status,
                            f"[Test Issue] - Timeout reached! Display is not enumerated on port "
                            f"{self.port_to_detach}")

            logging.info("Applying Extended Display Configuration...")
            config = enum.EXTENDED
            enumerated_displays = DisplayConfiguration().get_enumerated_display_info()
            # printing enumerated displays info
            logging.debug('Enumerated display information: {}'.format(enumerated_displays.to_string()))
            # Checking if display is attached/detached
            if DisplayConfiguration().set_display_configuration_ex(config,
                                                                   self.displays_in_cmdline,
                                                                   enumerated_displays) is False:
                self.fail(f'Failed to set the display configuration as ED {self.displays_in_cmdline}')
            logging.info(f'Successfully set the display configuration as ED {self.displays_in_cmdline}')

            ##
            # unplug LFP_2 in the end.
            logging.info("Hot unplugging LFP_2...")
            res = self._setHPD(self.mapped_port_to_detach, False, self.port_type, self.gfx_index)
            if res is False:
                logging.error(f"FAIL: HPD-unplug failed on port={self.port_to_detach}")
            else:
                logging.info(f"PASS: HPD-unplug successful on port={self.port_to_detach}")
            # Delay
            status = self._dynamic_delay(self.port_to_detach, plug=False)
            self.assertTrue(status,
                            f"[Test Issue] - Timeout reached! Display is still enumerated on port "
                            f"{self.mapped_port_to_detach}")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('DetachableLFPDisplaySwitching'))
    TestEnvironment.cleanup(outcome)
