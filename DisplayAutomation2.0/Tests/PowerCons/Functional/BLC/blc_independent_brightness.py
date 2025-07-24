########################################################################################################################
# @file         blc_independent_brightness.py
# @brief        Contain tests to verify Independent brightness using IGCL
# @author       Ashish Tripathi
########################################################################################################################

import ctypes
import time

from Libs.Core.test_env import test_environment
from Libs.Core.wrapper import control_api_wrapper, control_api_args

from Libs.Feature.powercons import registry
from Tests.PowerCons.Functional.BLC.blc_base import *


##
# @brief        This class contains Tests for Independent Brightness
class BlcIndependentBrightness(BlcBase):
    ##
    # @brief        This class method is the exit point for DPST test cases. Helps to restore the applied parameters
    #               required for DPST test execution.
    # @return       None
    @classmethod
    def tearDownClass(cls):
        super(BlcIndependentBrightness, cls).tearDownClass()
        for adapter in dut.adapters.values():
            status = registry.delete(adapter.gfx_index, registry.RegKeys.BLC.INDEPENDENT_BRIGHTNESS_CTL)
            if status is False:
                assert False, f"FAILED to delete IndependentBrightnessControl regkey"
            if status is True:
                result, reboot_required = display_essential.restart_gfx_driver()
                assert result, "FAILED to restart the driver"
                logging.info(f"Successfully restarted the driver for {adapter.gfx_index}")

    ##
    # @brief        This function verifies Independent brightness with different value and different transition time
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["BASIC"])
    # @endcond
    def t_11_iblc_stress_test(self):
        # for set call
        set_brightness = control_api_args.ctl_set_brightness_t()
        set_brightness.Size = ctypes.sizeof(set_brightness)

        # for get call
        get_brightness = control_api_args.ctl_get_brightness_t()
        get_brightness.Size = ctypes.sizeof(get_brightness)

        status = True
        for adapter in dut.adapters.values():
            if adapter.lfp_count != 2:
                self.fail("IBLC test needs 2 LFPs (Planning issue)")

            for set_value, t_time in zip(BRIGHTNESS_LIST, TRANSITION_TIME_LIST):
                set_brightness.TargetBrightness = set_value * blc.BLC_PWM_HIGH_PRECISION_FACTOR
                set_brightness.SmoothTransitionTimeInMs = t_time
                target_id = adapter.panels['DP_B'].target_id

                logging.info(f"Applying {set_brightness.TargetBrightness} brightness with {t_time} ms transition time")
                if control_api_wrapper.set_brightness_via_igcl(set_brightness, target_id) is False:
                    self.fail("FAILED to do  Brightness call failed, unable to apply brightness")
                logging.info("\tSuccessfully completed SET brightness using escape call")

                time.sleep(10)

                logging.info(f"Doing GET operation for brightness to make sure that SET was done by driver")
                if control_api_wrapper.get_brightness_via_igcl(get_brightness, target_id) is False:
                    self.fail("FAILED to do GET brightness")
                logging.info("\tSuccessfully completed GET brightness using escape call")

                if set_brightness.TargetBrightness != get_brightness.CurrentBrightness:
                    logging.error(f"Brightness value Mismatch. Expected= {set_brightness.TargetBrightness}, "
                                  f"Actual= {get_brightness.CurrentBrightness}")
                    status = False

                logging.info(f"Brightness value match. Expected= {set_brightness.TargetBrightness}, "
                             f"Actual= {get_brightness.CurrentBrightness}")

        if status is False:
            self.fail("Independent brightness verification is failed")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(BlcIndependentBrightness))
    test_environment.TestEnvironment.cleanup(test_result)
