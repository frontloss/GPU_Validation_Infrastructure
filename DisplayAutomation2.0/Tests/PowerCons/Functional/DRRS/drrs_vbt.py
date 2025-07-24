#################################################################################################################
# @file         drrs_vbt.py
# @brief        Contains DRRS VBT test
#
# @author       Rohit Kumar
#################################################################################################################
from Libs.Core.test_env import test_environment
from Libs.Core.vbt import vbt

from Tests.PowerCons.Functional.DRRS.drrs_base import *


##
# @brief        This class contains DRRS VBT tests


class DrrsVbtTest(DrrsBase):

    ##
    # @brief        This class method is the entry point for any DRRS VBT test cases. Helps to initialize some of the
    #               parameters required for the DRRS VBT test execution and checks for supported version of VBT
    # @return       None
    @classmethod
    def setUpClass(cls):
        super(DrrsVbtTest, cls).setUpClass()

        for gfx_index, adapter in dut.adapters.items():
            gfx_vbt = vbt.Vbt(gfx_index)
            if gfx_vbt.version < 228:
                gdhm.report_test_bug_os("[OsFeatures][DRRS] DRRS VBT test is running on unsupported system", gdhm.ProblemClassification.OTHER,gdhm.Priority.P3,
                    gdhm.Exposure.E3)
                raise Exception("DRRS VBT test is only supported on VBT 228 onwards")

    ##
    # @brief        This method is the exit point for all DRRS VBT test cases. This enables back DRRS in VBT
    # @return       None
    @classmethod
    def tearDownClass(cls):
        # Enable DRRS back in VBT
        for adapter in dut.adapters.values():
            drrs.enable(adapter)

        super(DrrsVbtTest, cls).tearDownClass()

    ##
    # @brief        This function verifies DRRS before and after disabling the LFP panels one by one
    # @return       None
    # @cond
    @common.configure_test(repeat=True)
    # @endcond
    def t_11_vbt(self):
        self.verify_drrs()

        # Disable DRRS one by one for each LFP panel and verify
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    continue
                try:
                    if drrs.set_drrs_in_vbt(adapter, panel, False) is False:
                        self.fail(f"FAILED to disable DRRS in VBT for {panel.port}")

                    dut.refresh_panel_caps(adapter)

                    self.verify_drrs(vbt_disabled_panels=[(adapter.gfx_index, panel.port)])
                except Exception as e:
                    self.fail(e)
                finally:
                    if drrs.set_drrs_in_vbt(adapter, panel, True) is False:
                        self.fail(f"FAILED to enable DRRS in VBT for {panel.port}")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.runner.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(DrrsVbtTest))
    test_environment.TestEnvironment.cleanup(test_result)
