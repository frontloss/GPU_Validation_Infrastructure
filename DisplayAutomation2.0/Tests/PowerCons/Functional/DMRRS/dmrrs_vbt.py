#################################################################################################################
# @file         dmrrs_vbt.py
# @addtogroup   PowerCons
# @section      DMRRS_Tests
# @brief        Contains DMRRS VBT test
#
# @author       Rohit Kumar
#################################################################################################################

from Libs.Core.test_env import test_environment
from Libs.Core.vbt import vbt

from Tests.PowerCons.Functional.DMRRS.dmrrs_base import *
from Tests.PowerCons.Modules import workload


##
# @brief        Contains DMRRS tests with VBT


class DmrrsVbtTest(DmrrsBase):

    ##
    # @brief        This class method is the entry point for any DMRRS VBT test cases. Helps to initialize some of the
    #               parameters required for the DMRRS VBT test execution and checks for supported version of VBT
    # @return       None
    @classmethod
    def setUpClass(cls):
        super(DmrrsVbtTest, cls).setUpClass()

        for gfx_index, adapter in dut.adapters.items():
            gfx_vbt = vbt.Vbt(gfx_index)
            if gfx_vbt.version < 228:
                gdhm.report_test_bug_os("[OsFeatures][DMRRS] DRRS VBT test is running on unsupported system",gdhm.ProblemClassification.OTHER, gdhm.Priority.P3,
                    gdhm.Exposure.E3)
                raise Exception("DMRRS VBT test is only supported on VBT 228 onwards")

    ##
    # @brief        This method is the exit point for all DMRRS VBT test cases. This enables back DMRRS in VBT
    # @return       None
    @classmethod
    def tearDownClass(cls):

        for adapter in dut.adapters.values():
            dmrrs.enable(adapter)

        super(DmrrsVbtTest, cls).tearDownClass()

    ##
    # @brief        This function verifies DMRRS before and after disabling the LFP panels one by one
    # @return       None
    # @cond
    @common.configure_test(repeat=True)
    # @endcond
    def t_11_vbt(self):
        media_fps = 24
        etl_file_path, _ = workload.run(workload.VIDEO_PLAYBACK, [media_fps, 30])
        status = True
        vbt_update_failed = []
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                self.dmrrs_hrr_verification(adapter, panel, etl_file_path, media_fps)

        # Disable DMRRS one by one for each LFP panel
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    continue
                if dmrrs.set_dmrrs_in_vbt(adapter, panel, False) is False:
                    logging.error(f"FAIL: DMRRS disabling in VBT failed for {panel.port}")
                    status = False
                    vbt_update_failed.append(panel.port)
                else:
                    logging.info(f"Step: DMRRS disabled in VBT for {panel.port}")
                    html.step_end()

        html.step_start("Verifying after disabling DMRRS VBT")
        html.step_end()
        etl_file_path, _ = workload.run(workload.VIDEO_PLAYBACK, [media_fps, 30])

        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                # for LFP if VBT update failed then skipped verification
                if panel.port in vbt_update_failed:
                    logging.error(f"Skipping Verification as DMRRS update in VBT failed for {panel.port}")
                    continue
                # for LFP if VBT updated then verification will be based on disable in VBT.
                # for EFP no VBT update so DMRRS should enable and working.
                self.dmrrs_hrr_verification(adapter, panel, etl_file_path, media_fps, is_disabled_in_vbt=panel.is_lfp)

        vbt_update_failed = []
        # Enable DMRRS one by one for each LFP panel and verify
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    continue
                if dmrrs.set_dmrrs_in_vbt(adapter, panel, True) is False:
                    logging.error(f"FAIL: DMRRS Enabling in VBT Failed on {panel.port}")
                    status = False
                    vbt_update_failed.append(panel.port)
                else:
                    html.step_start(f"PASS: DMRRS enabled back in VBT for panel on {panel.port}")
                    html.step_end()

        html.step_start("Verifying after enabling back DMRRS in VBT")
        html.step_end()
        etl_file_path, _ = workload.run(workload.VIDEO_PLAYBACK, [media_fps, 30])

        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.port in vbt_update_failed:
                    logging.error(f"Skipping Verification as DMRRS update in VBT failed on {panel.port}")
                    continue
                self.dmrrs_hrr_verification(adapter, panel, etl_file_path, media_fps)

        if status is False:
            self.fail("FAIL: DMRRS Verification with VBT changes failed")
        html.step("PASS:DMRRS Verification with VBT changes passed")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.runner.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(DmrrsVbtTest))
    test_environment.TestEnvironment.cleanup(test_result)
