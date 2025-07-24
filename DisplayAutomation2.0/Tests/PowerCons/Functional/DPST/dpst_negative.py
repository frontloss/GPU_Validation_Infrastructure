########################################################################################################################
# @file         dpst_negative.py
# @brief        Test for xPST negative cases
#
# @author       Simran Setia
########################################################################################################################
from Libs.Core.test_env import test_environment
from Tests.PowerCons.Functional.DPST.dpst_base import *

##
# @brief        This class contains tests for DPST/OPST post RegKey disable.
#               This class inherits the DpstBase class.


class DpstNegative(DpstBase):

    ############################
    # Test Function
    ############################

    ##
    # @brief        DPST verification post RegKey disable
    # @return       None
    # @cond
    @common.configure_test(selective=["DPST_REGKEY"])
    # @endcond
    def t_11_dpst_RegKey_disable(self):
        skip_report_generate = False
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():

                # disabling DPST via RegKey
                status = dpst.disable_dpst_in_regkey(adapter)
                if status is False:
                    self.fail(f"FAIL: Test ended due to failed to disable DPST")

                if status is True:
                    # driver restart after disabling DPST
                    status, reboot_required = display_essential.restart_gfx_driver()
                    if status is False:
                        self.fail("Failed to restart display driver post RegKey disable")

                etl_file = dpst.run_workload(self.workload_method, polling_offsets=self.offsets)
                if etl_file is False:
                    self.fail("Failed to run the workload")

                status = dpst.verify(adapter, panel, etl_file, skip_report_generate,
                                     dpst.XpstFeature.DPST, True)
                if status:
                    self.fail(f"FAIL: DPST is enabled post RegKey disable")
                else:
                    logging.info(f"PASS: DPST is disabled post RegKey disable")

    ##
    # @brief        OPST verification post RegKey disable
    # @return       None
    # @cond
    @common.configure_test(selective=["OPST_REGKEY"])
    # @endcond
    def t_12_Opst_RegKey_disable(self):
        skip_report_generate = False
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():

                # disabling OPST via RegKey
                status = dpst.disable_opst_in_regkey(adapter)
                if status is False:
                    self.fail(f"FAIL: Test ended due to failed to disable OPST")

                if status is True:
                    # driver restart after disabling OPST
                    status, reboot_required = display_essential.restart_gfx_driver()
                    if status is False:
                        self.fail("Failed to restart display driver post RegKey disable")

                etl_file = dpst.run_workload(self.workload_method, polling_offsets=self.offsets)
                if etl_file is False:
                    self.fail("Failed to run the workload")

                status = dpst.verify(adapter, panel, etl_file, skip_report_generate,
                                     dpst.XpstFeature.OPST, True)
                if status:
                    self.fail(f"FAIL: OPST is enabled post RegKey disable")
                else:
                    logging.info(f"PASS: OPST is disabled post RegKey disable")

    ##
    # @brief       This method is the exit point for DPST/OPST disable RegKey test case. This re-sets the environment
    #              changes done for execution of disable DPST/OPST RegKey test
    # @return       None

    @classmethod
    def tearDownClass(cls):
        super(DpstNegative, cls).tearDownClass()
        logging.info(" TEARDOWN: DPST Negative".center(common.MAX_LINE_WIDTH, "*"))
        do_driver_restart = False
        for adapter in dut.adapters.values():
            temp_status = dpst.enable_dpst_in_regkey(adapter)
            if temp_status is False:
                assert False, "FAILED to enable DPST"
            if temp_status is True:
                do_driver_restart = True
            temp_status = dpst.enable_opst_in_regkey(adapter)
            if temp_status is False:
                assert False, "FAILED to enable OPST"
            if temp_status is True:
                do_driver_restart = True

            if do_driver_restart is True:
                # driver restart after enabling DPST and OPST
                status, reboot_required = display_essential.restart_gfx_driver()
                if status is False:
                    assert False, "Failed to restart display driver post RegKey enable"


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(DpstNegative))
    test_environment.TestEnvironment.cleanup(test_result)
