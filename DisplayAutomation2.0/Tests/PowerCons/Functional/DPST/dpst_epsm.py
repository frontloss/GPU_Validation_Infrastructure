########################################################################################################################
# @file         dpst_epsm.py
# @brief        Test for DPST/OPST verification with Enhanced Power Saving Mode
#
# @author       Ashish Tripathi
########################################################################################################################
import os
import subprocess
import time

from Libs.Core import winkb_helper as kb
from Libs.Core.test_env import test_environment

from Tests.PowerCons.Functional.DPST.dpst_base import *

APPLICATIONS_FOLDER = os.path.join(test_context.SHARED_BINARY_FOLDER, "Applications")


##
# @brief        This class contains basic test cases for DPST with Enhanced Power Saving Mode
class DpstEpsm(DpstBase):
    ##
    # @brief        This class method is the exit point for DPST test cases. Helps to restore the applied parameters
    #               required for DPST test execution.
    # @return       None
    @classmethod
    def tearDownClass(cls):
        super(DpstEpsm, cls).tearDownClass()
        for adapter in dut.adapters.values():
            epsm_status = dpst.set_epsm(adapter, disable_epsm=True)
            if epsm_status is False:
                assert False, "FAILED to configure EPSM status"
            if epsm_status is True:
                result, reboot_required = display_essential.restart_gfx_driver()
                if result is False:
                    assert False, f"FAILED to restart display driver for {adapter.name}"

    ##
    # @brief        This function verifies DPST with Enhanced Power Saving Mode using IGCL with DC power source
    #               1. Enable EPSM using RegKey
    #               2. Disable EPSM using IGCL when platform is Gen13+
    #               3. Enable EPSM using IGCL when platform is Gen13+
    #               4. Disabled EPSM using RegKey
    # @return       None
    # @cond
    @common.configure_test(repeat=True)
    # @endcond
    def t_11_dpst_epsm_with_igcl(self):
        power_source = self.display_power_.get_current_powerline_status()
        power_scheme = self.display_power_.get_current_power_scheme()
        test_status = True
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                logging.info("Verifying EPSM is enabled in driver when toggled using RegKey")
                epsm_status = dpst.set_epsm(adapter, disable_epsm=False)
                if epsm_status is False:
                    self.fail("FAILED to configure EPSM status")

                if epsm_status:
                    result, reboot_required = display_essential.restart_gfx_driver()
                    if result is False:
                        self.fail(f"FAILED to restart display driver for {adapter.name}")

                test_status &= self.validate_epsm(True)

                # use IGCL only when DPST is supported on panel and platform is Gen13+
                if adapter.name not in common.PRE_GEN_13_PLATFORMS and panel.hdr_caps.is_aux_only_brightness is False:
                    logging.info("Verifying EPSM is disabled in driver when toggled using IGCL")
                    if dpst.igcl_set_epsm(panel, False, power_source, power_scheme) is False:
                        self.fail("FAILED to configure EPSM status")

                    test_status &= self.validate_epsm(False)

                    logging.info("Verifying EPSM is enabled in driver when toggled using IGCL")
                    if dpst.igcl_set_epsm(panel, True, power_source, power_scheme) is False:
                        self.fail("FAILED to configure EPSM status")

                    test_status &= self.validate_epsm(True)

                    test_status &= self.verify_backlight_capping(adapter, panel, 70)
                    test_status &= self.verify_backlight_capping(adapter, panel, 80)
                    test_status &= self.verify_backlight_capping(adapter, panel, 90)

                logging.info("Verifying EPSM is disabled in driver when toggled using RegKey")
                epsm_status = dpst.set_epsm(adapter, disable_epsm=True)
                if epsm_status is False:
                    self.fail("FAILED to configure EPSM status")
                if epsm_status is True:
                    result, reboot_required = display_essential.restart_gfx_driver()
                    if result is False:
                        self.fail(f"FAILED to restart display driver for {adapter.name}")

                test_status &= self.validate_epsm(False)
                test_status &= self.verify_backlight_capping(adapter, panel, None)

            # currently DPST IGCL is global for all the panels so break after first iteration
            break

        if test_status is False:
            self.fail(f"FAIL: {self.xpst_feature_str} feature verification")
        logging.info(f"PASS: {self.xpst_feature_str} feature verification")

    ##
    # @brief        Helper function to run workload, verify and return status
    # @param[in]    expect_epsm_enable bool, flag to give expectation of EPSM
    # @return       bool, True is Successful, False otherwise
    def validate_epsm(self, expect_epsm_enable):
        etl_file = dpst.run_workload(dpst.WorkloadMethod.PSR_UTIL, polling_offsets=self.offsets)
        if etl_file is False:
            self.fail("FAILED to run the workload")

        return self.validate_xpst(etl_file, dpst.WorkloadMethod.PSR_UTIL, workload.PowerSource.DC_MODE,
                                  expect_epsm_enable)

    ##
    # @brief        Helper function to verify backlight capping
    # @param[in]    adapter object, Adapter object from DUT
    # @param[in]    panel bool, Panel object from DUT
    # @param[in]    epsm_weight bool, flag to give expectation of EPSM
    # @return       bool, True is Successful, False otherwise
    def verify_backlight_capping(self, adapter, panel, epsm_weight):
        if adapter.name in common.PRE_GEN_14_PLATFORMS or self.hdr_status:
            logging.info("EPSM Backlight capping check will be executed from MTL+ and for Non-HDR case")
            return True

        if epsm_weight is not None:
            weight_status = dpst.set_epsm_weight(adapter, epsm_weight)
            if weight_status is False:
                logging.error("FAILED to set EPSM weight")
                return False

            if weight_status:
                result, reboot_required = display_essential.restart_gfx_driver()
                if result is False:
                    logging.error(f"FAILED to restart display driver for {adapter.name}")
                    return False

        process = subprocess.Popen(os.path.join(APPLICATIONS_FOLDER, "TestImages.exe"))
        time.sleep(3)
        status, etl_file = workload.etl_tracer_stop_existing_and_start_new(f"GfxTraceBeforeWorkload")
        if status is False:
            process.kill()
            logging.error("FAILED to get ETL before Workload")
            return False

        # mountain image
        for count in range(3):
            kb.press('RIGHT')
            time.sleep(1)

        power_source = self.display_power_.get_current_powerline_status()
        power_scheme = self.display_power_.get_current_power_scheme()

        time.sleep(10)

        status, etl_file = workload.etl_tracer_stop_existing_and_start_new(f"GfxTraceDuringWorkload")
        process.kill()
        if status is None:
            logging.error("FAILED to get ETL during Workload")
            return False

        # Generate the etl report
        status, log_file = dpst.generate_report_kei(etl_file)
        if status is False:
            logging.error("FAILED to generate the report")
            return False

        status = True
        xpst_data = dpst.get_status(panel.target_id, power_source, power_scheme)
        capped_brightness = dpst.get_capped_dpst_brightness(adapter, xpst_data)
        status &= dpst.verify_dpst_brightness_capped(panel, log_file, capped_brightness)

        if status is False:
            logging.error(f"After setting EPSM weight {epsm_weight}, DPST brightness is not under capped value")
        else:
            logging.info(f"After setting EPSM weight {epsm_weight}, DPST brightness is under capped value")

        return status


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(DpstEpsm))
    test_environment.TestEnvironment.cleanup(test_result)
