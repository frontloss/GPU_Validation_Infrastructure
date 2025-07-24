#######################################################################################################################
# @file         c10_with_dc_state.py
# @brief      Tests for C10 check with DC5,DC6V and DC9
#
# @author       Bhargav Adigarla
#######################################################################################################################
import os
from Libs.Core import display_power
from Libs.Core.logger import etl_tracer
from Libs.Core.test_env import test_environment, test_context
from Tests.PowerCons.PnP.tools import socwatch
from Tests.PowerCons.Functional.DCSTATES import dc_state
from Tests.PowerCons.Functional.DCSTATES.dc_state_base import *

##
# @brief        This class contains basic tests for DC6/DC9 basic states
class TestC10WithDcState(DCStatesBase):
    ############################
    # Test Function
    ############################

    ##
    # @brief        This function DC6 with C10
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["DC6"])
    # @endcond
    def t_11_state_dc6_c10(self):
        for adapter in dut.adapters.values():
            if etl_tracer.start_etl_tracer() is False:
                logging.error("Failed to start ETL Tracer")
                return False

            log_file = socwatch.run_workload("IDLE", 30)

            if etl_tracer.stop_etl_tracer() is False:
                logging.error("Failed to stop ETL Tracer")
                return False

            if etl_tracer.start_etl_tracer() is False:
                logging.error("Failed to start ETL Tracer")
                return False

            file_name = "GfxTrace_dc6_" + str(time.time()) + ".etl"
            etl_file_path = os.path.join(test_context.LOG_FOLDER, file_name)
            os.rename(etl_tracer.GFX_TRACE_ETL_FILE, etl_file_path)

            if dc_state.verify_dc_state(adapter, 'DC6', etl_file_path) is False:
                self.fail("SW DC6 verification failed")

            if os.path.exists(log_file) is False:
                self.fail("{0} not found".format(log_file))

            c10 = socwatch.get_metric(log_file, 'PACKAGE_C10')

            if c10 == 0:
                self.fail("System not entering to PC10")
            logging.info(f"System is entering into C10 with DC6 IDLE Desktop- {c10}")

    ##
    # @brief        This function DC9 with CS/S3
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["DC9"])
    # @endcond
    def t_12_state_dc9_c10(self):
        for adapter in dut.adapters.values():
            if self.display_power_.is_power_state_supported(display_power.PowerEvent.CS) is False:
                self.fail("CS is NOT supported on the system(Planning Issue)")

            if etl_tracer.start_etl_tracer() is False:
                logging.error("Failed to start ETL Tracer")
                return False

            socwatch_output = socwatch.run_soc_watch_with_cs()

            if etl_tracer.stop_etl_tracer() is False:
                logging.error("Failed to stop ETL Tracer")
                return False

            if etl_tracer.start_etl_tracer() is False:
                logging.error("Failed to start ETL Tracer")
                return False

            c10_score = socwatch.get_metric(socwatch_output, 'PACKAGE_C10')

            file_name = "GfxTrace_dc9_" + str(time.time()) + ".etl"
            etl_file_path = os.path.join(test_context.LOG_FOLDER, file_name)
            os.rename(etl_tracer.GFX_TRACE_ETL_FILE, etl_file_path)

            if dc_state.verify_dc_state(adapter, 'DC9', etl_file_path) is False:
                self.fail("SW DC9 verification failed")

            if c10_score == 0:
                self.fail("System not entering to PC10")

    ##
    # @brief        This function verifies C10 with DC6v Video playback
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["DC6V"])
    # @endcond
    def t_13_state_dc6v_c10(self):
        for adapter in dut.adapters.values():
            dc6v_status = dc_state.enable_dc6v(adapter)
            if dc6v_status is False:
                self.fail("FAILED to enable DC6v in driver")
            if dc6v_status is True:
                status, reboot_required = display_essential.restart_gfx_driver()
                if status is False:
                    self.fail("FAILED to restart the driver")
            if len(self.lfp_panels) == 2:
                if self.enable_port_sync_in_vbt() is False:
                    self.fail("Failed to enable port sync in VBT")

            if etl_tracer.start_etl_tracer() is False:
                logging.error("Failed to start ETL Tracer")
                return False

            log_file = socwatch.run_workload("VIDEO", 24)

            if etl_tracer.stop_etl_tracer() is False:
                logging.error("Failed to stop ETL Tracer")
                return False

            if etl_tracer.start_etl_tracer() is False:
                logging.error("Failed to start ETL Tracer")
                return False

            file_name = "GfxTrace_dc6v_" + str(time.time()) + ".etl"
            etl_file_path = os.path.join(test_context.LOG_FOLDER, file_name)
            os.rename(etl_tracer.GFX_TRACE_ETL_FILE, etl_file_path)

            if dc_state.verify_dc_state(adapter, 'DC6V', etl_file_path) is False:
                self.fail("SW DC6V verification failed")
            else:
                logging.info("SW DC6V verification is successful")

            if os.path.exists(log_file) is False:
                self.fail("{0} not found".format(log_file))

            c10 = socwatch.get_metric(log_file, 'PACKAGE_C10')

            if c10 == 0:
                self.fail(f"System is not entering into C10 with DC6V video playback- {c10}")
            else:
                logging.info(f"System is entering into C10 with DC6V video playback- {c10}")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(TestC10WithDcState))
    test_environment.TestEnvironment.cleanup(test_result)
