########################################################################################################################
# @file         dpst_threshold.py
# @brief        Test for DPST/OPST backlight threshold scenarios
#
# @author       Vinod D S, Ashish Tripathi
########################################################################################################################
import time

from Libs.Core.test_env import test_environment
from Libs.Feature.blc import brightness
from Tests.PowerCons.Functional.DPST.dpst_base import *
from Tests.PowerCons.Modules import windows_brightness


##
# @brief        This class contains test cases for DPST/OPST with backlight threshold
class DpstThreshold(DpstBase):
    ##
    # @brief        This function verifies DPST/OPST with backlight less than the threshold
    # @return       None
    # @cond
    @common.configure_test(repeat=True)
    # @endcond
    def t_11_dpst_with_backlight_outside_threshold(self):
        dpst_status = True
        # WA for 14010407547 - make brightness work after disable/enable gfx-driver (fix will be in build 19575)
        if dut.WIN_OS_VERSION < dut.WinOsVersion.WIN_COBALT:
            blc.restart_display_service()
        logging.info(f"Step: Verifying {0} with brightness outside threshold. Expectation= "
                     f"Not Working".format(self.xpst_feature_str))
        for level in self.level_without_dpst:
            self.set_brightness(level)
            dpst_status &= self.validate_xpst_threshold(positive_case=False)
        if dpst_status is False:
            self.fail("FAIL: {0} feature verification".format(self.xpst_feature_str))
        logging.info("PASS: {0} feature verification".format(self.xpst_feature_str))

    ##
    # @brief        This function verifies DPST/OPST with backlight more than the threshold
    # @return       None
    # @cond
    @common.configure_test(repeat=True)
    # @endcond
    def t_12_dpst_with_backlight_inside_threshold(self):
        dpst_status = True
        # WA for 14010407547 - make brightness work after disable/enable gfx-driver (fix will be in build 19575)
        if dut.WIN_OS_VERSION < dut.WinOsVersion.WIN_COBALT:
            blc.restart_display_service()
        # only old INF is present
        logging.info(f"Step: Verifying {0} with brightness inside threshold. Expectation= "
                     f"Working".format(self.xpst_feature_str))
        for level in self.level_with_dpst:
            self.set_brightness(level)
            dpst_status &= self.validate_xpst_threshold(positive_case=True)
        if dpst_status is False:
            self.fail("FAIL: {0} feature verification".format(self.xpst_feature_str))
        logging.info("PASS: {0} feature verification".format(self.xpst_feature_str))

    ##
    # @brief        API to set brightness level
    # @param[in]    level int level of brightness to be set
    # @return       None
    def set_brightness(self, level):
        logging.info(f"Step: Setting current brightness to {level}")
        if (self.is_high_precision or self.is_nits_supported) is False:
            retry_count = 0
            brightness_apply_status = True
            while retry_count < 2:
                brightness_apply_status = windows_brightness.set_current_brightness(level, 1)
                if brightness_apply_status is False:
                    logging.warning(f"FAILED to set current brightness to {level}. Retrying")
                retry_count += 1

            if brightness_apply_status is False:
                self.fail(f"FAILED to set current brightness to {level}")
            logging.info(f"\tSuccessfully set current brightness to {level}")
        else:
            brightness.load_library()
            for adapter in dut.adapters.values():
                for panel in adapter.panels.values():
                    for _ in range(2):  # OS requesting extra DDI after setting below one. So 2 times
                        if blc.set_brightness3(panel.gfx_index, panel.target_id, level, 200) is False:
                            self.fail(f"FAILED to apply milli-percent= {level}")
                        logging.info(f"\tSuccessfully applied milli-percent= {level}")
                        time.sleep(2)

    ##
    # @brief        This is helper function to verify DPST/OPST is working or not with threshold
    # @param[in]    positive_case [optional] indicating whether DPST working is expected or not
    # @return       None
    def validate_xpst_threshold(self, positive_case=True):
        dpst_etl_file = dpst.run_workload(dpst.WorkloadMethod.PSR_UTIL, polling_offsets=self.offsets)
        # Verify DPST/OPST for each adapter and LFP
        status = True
        skip_report_generate = False
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                # Skip the panel if not LFP
                if panel.is_lfp is False:
                    continue
                logging.info("Step: Verifying {0} on {1}-{2}".format(self.xpst_feature_str, adapter.name, panel.port))

                dpst_status = dpst.verify(adapter, panel, dpst_etl_file, skip_report_generate, self.xpst_feature, True)
                if dpst_status is None:
                    self.fail("FAILED to verify {0}".format(self.xpst_feature_str))
                skip_report_generate = True

                if positive_case is True:
                    if dpst_status:
                        logging.info(f"\t\tPASS: {self.xpst_feature_str} is working on "
                                     f"{panel.port}(PIPE_{panel.pipe})= EXPECTED")
                    else:
                        logging.error(f"\t\tFAIL: {self.xpst_feature_str} is NOT working on "
                                      f"{panel.port}(PIPE_{panel.pipe})= NOT EXPECTED")
                        status = False
                else:
                    if dpst_status:
                        logging.error(f"\t\tFAIL: {self.xpst_feature_str} is working on "
                                      f"{panel.port}(PIPE_{panel.pipe})= NOT EXPECTED")
                        status = False
                    else:
                        logging.info(f"\t\tPASS: {self.xpst_feature_str} is NOT working on "
                                     f"{panel.port}(PIPE_{panel.pipe})= EXPECTED")

        if status is False:
            return False
        return True


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.runner.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(DpstThreshold))
    test_environment.TestEnvironment.cleanup(test_result)
