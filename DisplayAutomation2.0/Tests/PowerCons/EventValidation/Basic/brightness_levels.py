########################################################################################################################
# @file         brightness_levels.py
# @brief        This file implements brightness levels scenario for all display pc feature testing.
#
# @author       Vinod D S
########################################################################################################################

from Libs.Core.test_env import test_environment
from Libs.Feature.blc import brightness

from Tests.PowerCons.EventValidation.Basic.event_validation_base import *
from Tests.PowerCons.Functional.BLC import blc
from Tests.PowerCons.Modules import windows_brightness


##
# @brief        This class contains tests for brightness levels scenario
class BrightnessLevels(EventValidationBase):
    ##
    # @brief        This function verifies the application of different brightness levels
    # @return       None
    def test_brightness_levels(self):

        # WA for 14010407547 - make brightness work after disable/enable gfx-driver (fix will be in build 19575)
        if dut.WIN_OS_VERSION < dut.WinOsVersion.WIN_COBALT:
            blc.restart_display_service()

        logging.info("Getting current brightness")
        init_brightness_level = windows_brightness.get_current_brightness()
        if init_brightness_level is None:
            self.fail("Failed to get current brightness")
        logging.info("\tCurrent brightness level = {0}".format(init_brightness_level))

        if self.precision_ranges_values is None:
            if self._set_brightness_slider() is False:
                self.fail()
            if self._set_brightness_slider(True) is False:
                self.fail()
        else:
            no_error = 0
            min_range = int(self.precision_ranges_values[0])
            max_range = int(self.precision_ranges_values[1]) + 1
            mid_range = min_range + (max_range-min_range)//2
            transition_time = int(self.precision_ranges_values[2])

            brightness.load_library()
            logging.info("Applying milli-percent from ({0}-{1})% with 1% change and transition time= {2}ms".format(
                min_range, mid_range, transition_time))

            for adapter in dut.adapters.values():
                for panel in adapter.panels.values():
                    if panel.is_lfp:
                        for milli_percent in range(min_range, mid_range):
                            # Applying milli percentage values
                            logging.info("\tApplying milli-percent= {0}".format(milli_percent))
                            if blc.set_brightness3(
                                    panel.gfx_index, panel.target_id, milli_percent, transition_time) is False:
                                logging.error("\tFAILED to apply milli-percent= {0}".format(milli_percent))
                                no_error += 1
                            else:
                                logging.info("\tSuccessfully applied milli-percent= {0}".format(milli_percent))
                            time.sleep(2)   # breather for immediate

                        # Apply 5 change milli percent if delta > 5 else apply delta
                        delta = max_range - mid_range
                        step = 5 if (delta > 5) else delta
                        logging.info(
                            "Applying milli-percent from ({0}-{1})% with {2}% change and transition time= {3}ms".format(
                                mid_range, max_range, step, transition_time))
                        for milli_percent in range(mid_range, max_range + 1, step):
                            # Applying milli percentage values
                            logging.info("\tApplying milli-percent= {0}".format(milli_percent))

                            if blc.set_brightness3(panel.gfx_index, panel.target_id, milli_percent, transition_time) is False:
                                logging.error("\tFAILED to apply milli-percent= {0}".format(milli_percent))
                                no_error += 1
                            else:
                                logging.info("\tSuccessfully applied milli-percent= {0}".format(milli_percent))
                            time.sleep(5)   # breather for phasing

                    # Keeping only for first LFP target id to avoid refactor for companion display
                    break

        # Restoring the brightness to initial
        logging.info("Restoring current brightness to {0}".format(init_brightness_level))
        if windows_brightness.set_current_brightness(init_brightness_level) is False:
            self.fail("Failed to restore current brightness to {0}".format(init_brightness_level))
        logging.info("\tRestored current brightness to {0} successfully".format(init_brightness_level))

        self.check_validators()

    ##
    # @brief        This function verifies the setting of different brightness levels
    # @return       None
    @staticmethod
    def _set_brightness_slider(reverse=False):
        brightness_apply_status = True
        failed_levels = []
        do_retry = True
        brightness_levels = range(100, -1, -1) if reverse else range(0, 101)
        for level in brightness_levels:
            logging.info("Step: Setting current brightness to {0}".format(level))
            if windows_brightness.set_current_brightness(level, 1) is False:
                logging.error("\tFailed to set current brightness to {0}".format(level))
                brightness_apply_status = False
                failed_levels.append(level)
            else:
                logging.info("\tSet current brightness to {0} successfully".format(level))

            # Try only one more time if setting brightness is failed
            if brightness_apply_status is False:
                if do_retry is True:
                    do_retry = False
                    brightness_apply_status = True
                    failed_levels = failed_levels[:-1]  # remove last element added as second try is there below
                    logging.info("\tDoing second try for setting brightness to {0}".format(level))
                    if windows_brightness.set_current_brightness(level, 1) is False:
                        logging.error("\tFailed to set current brightness to {0}".format(level))
                        brightness_apply_status = False
                        failed_levels.append(level)
                    else:
                        logging.info("\tSet current brightness to {0} successfully".format(level))

            logging.info("Delay of 1 second..")

        if brightness_apply_status is False:
            logging.error("Failed to set brightness levels - {0}(Test Issue)".format(
                ', '.join([str(x) for x in failed_levels])))
            return False
        return True


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    test_environment.TestEnvironment.cleanup(outcome.result)
