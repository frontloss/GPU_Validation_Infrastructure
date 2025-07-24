########################################################################################################################
# @file         mso_concurrency.py
# @brief        Test for MSO verification with concurrent features
#
# @author       Akshaya Nair
########################################################################################################################

from Libs.Core.test_env import test_environment
from Libs.Feature.vdsc import dsc_verifier
from Tests.EDP.MSO.mso_base import *
from Tests.PowerCons.Functional.DPST import dpst
from Tests.PowerCons.Functional import pc_external


##
# @brief        This class contains basic test cases for MSO verification with 3DLUT, VDSC, PSR1, PSR2 and DPST
class MsoConcurrency(MsoBase):

    ##
    # @brief        This function verifies MSO with 3DLUT
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["3DLUT"])
    # @endcond
    def t_01_mso_3dlut(self):
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                feature_status = pc_external.verify_3dlut(adapter, panel)
                if not feature_status[0]:
                    self.fail("Failed to enable 3DLUT")
                logging.info("3DLUT enabled successfully")

                mso_status = mso.verify(panel)
                if not mso_status:
                    self.fail("FAIL: MSO verification on {0} with 3DLUT failed".format(panel.port))
                logging.info("MSO verification on {0} with 3DLUT successful".format(panel.port))

    ##
    # @brief        This function verifies MSO with VDSC
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["VDSC"])
    # @endcond
    def t_02_mso_vdsc(self):
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if not panel.vdsc_caps.is_vdsc_supported:
                    self.fail("VDSC is NOT supported on {0}".format(panel.port))

                if dsc_verifier.verify_dsc_programming(adapter.gfx_index, panel.port) is False:
                    self.fail(f"FAIL: DSC programming verification failed")
                mso_status = mso.verify(panel)
                if not mso_status:
                    self.fail("FAIL: MSO verification with VDSC failed on {0}".format(panel.port))
                logging.info("MSO verification with VDSC successful on {0}".format(panel.port))

    ##
    # @brief        This function verifies MSO with PSR1
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["PSR1"])
    # @endcond
    def t_03_mso_psr1(self):
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if not panel.psr_caps.is_psr_supported:
                    self.fail("PSR1 is NOT supported on {0}".format(panel.port))

                mso_status = mso.verify(panel)
                if not mso_status:
                    self.fail("FAIL: MSO verification failed on {0}".format(panel.port))

                psr1_register_instance = MMIORegister.read("SRD_CTL_REGISTER",
                                                           "SRD_CTL_" + panel.transcoder,
                                                           adapter.name)
                element_value = psr1_register_instance.__getattribute__(str("srd_enable"))
                psr_status = bool(element_value)
                if not psr_status:
                    self.fail("FAIL: MSO verification with PSR1 failed on {0}".format(panel.port))

                logging.info("MSO verification with PSR1 successful on {0}".format(panel.port))

    ##
    # @brief        This function verifies MSO with PSR2
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["PSR2"])
    # @endcond
    def t_04_mso_psr2(self):
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if not panel.psr_caps.is_psr2_supported:
                    self.fail("PSR2 is NOT supported on {0}".format(panel.port))

                mso_status = mso.verify(panel)
                if not mso_status:
                    self.fail("FAIL: MSO verification failed on {0}".format(panel.port))

                psr2_register_instance = MMIORegister.read("PSR2_CTL_REGISTER",
                                                           "PSR2_CTL_" + panel.transcoder,
                                                           adapter.name)
                element_value = psr2_register_instance.__getattribute__(str("psr2_enable"))
                psr_status = bool(element_value)
                if not psr_status:
                    self.fail("FAIL: MSO verification with PSR2 failed on {0}".format(panel.port))

                logging.info("MSO verification with PSR2 successful on {0}".format(panel.port))

    ##
    # @brief        This function verifies MSO with DPST
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["DPST"])
    # @endcond
    def t_05_mso_dpst(self):
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if workload.change_power_source(workload.PowerSource.DC_MODE) is False:
                    self.fail("Failed to switch powerline to DC")
                etl_file = dpst.run_workload(dpst.WorkloadMethod.PSR_UTIL)
                dpst_status = dpst.verify(adapter, panel, etl_file)
                if not dpst_status:
                    self.fail("DPST not enabled on {0}".format(panel.port))

                mso_status = mso.verify(panel)
                if not mso_status:
                    self.fail("FAIL: MSO verification with DPST failed on {0}".format(panel.port))
                logging.info("MSO verification with DPST successful on {0}".format(panel.port))


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(MsoConcurrency))
    test_environment.TestEnvironment.cleanup(test_result)
