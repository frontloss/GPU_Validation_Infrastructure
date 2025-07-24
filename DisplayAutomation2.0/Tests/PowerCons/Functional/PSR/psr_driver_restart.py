#######################################################################################################################
# @file             psr_driver_restart.py
# @brief            PSR driver restart Tests
# @details          Tests for verifying PSR with driver restart
#
# @author           Chandrakanth Reddy
#######################################################################################################################

from Libs.Core.test_env import test_environment
from Tests.PowerCons.Functional.PSR.psr_base import *


##
# @brief        This class contains tests to verify PSR with driver restarts
class DriverRestart(PsrBase):
    ##
    # @brief        This function verifies PSR after DriverRestart operation
    # @return       None
    # @cond
    @common.configure_test(repeat=True)
    # @endcond
    def t_11_driver_restart(self):
        for adapter in dut.adapters.values():
            feature, feature_str = self.get_feature(adapter)
            for panel in adapter.panels.values():
                if panel.psr_caps.is_psr_supported is False and (panel.pr_caps.is_pr_supported is False):
                    continue
                if panel.psr_caps.is_psr_supported:
                    status = psr.verify_psr_setup_time(adapter, panel, self.feature)
                    if status is None:
                        continue
                    elif status is False:
                        self.fail("PSR restriction check failed")
                logging.info("Step: Restart display driver for {0}".format(adapter.name))
                if start_capture() is False:
                    self.fail("ETL Trace start Failed")
                h_total = MMIORegister.read(
                    "TRANS_HTOTAL_REGISTER", "TRANS_HTOTAL_" + panel.transcoder, adapter.name,
                    gfx_index=adapter.gfx_index)
                if adapter.name in machine_info.PRE_GEN_16_PLATFORMS:
                    v_total = MMIORegister.read(
                        "TRANS_VTOTAL_REGISTER", "TRANS_VTOTAL_" + panel.transcoder, adapter.name,
                        gfx_index=adapter.gfx_index)
                else:
                    v_total = MMIORegister.read(
                        'TRANS_VRR_VMAX_REGISTER', 'TRANS_VRR_VMAX_' + panel.transcoder, adapter.name,
                        gfx_index=adapter.gfx_index)
                try:
                    if display_essential.disable_driver(adapter.gfx_index) is False:
                        self.fail("Failed to disable display driver for {0}".format(adapter.gfx_index))
                    driver_disable_etl = end_capture('GfxTrace_during_driver_disable')
                except Exception as e:
                    self.fail(e)
                finally:
                    if display_essential.enable_driver(adapter.gfx_index) is False:
                        self.fail("Failed to enable display driver for {0}".format(adapter.gfx_index))
                logging.info("\tPASS: Restarted display driver successfully")
                etl_file = end_capture('GfxTrace_during_driver_enable')
                logging.info("Step: Verifying {0} on {1} during driver disable".format(feature_str, panel.port))
                if self.feature > psr.UserRequestedFeature.PSR_1:
                    if psr.verify_psr2_pr_disable_sequence(adapter, panel, driver_disable_etl, h_total, v_total, False) is False:
                        error_title = f"{self.feature_str} disable sequence check during driver disable is Failed"
                        _report_gdhm(error_title)
                        self.fail(error_title)
                    logging.info("PASS: {0} verification on {1} during driver disable".format(feature_str, panel.port))
                    logging.info("Step: Verifying {0} on {1} after driver restart".format(feature_str, panel.port))
                    if psr.verify_psr2_pr_enable_sequence(adapter, panel, etl_file) is False:
                        error_title = f"{self.feature_str} enable sequence check during driver enable is Failed"
                        _report_gdhm(error_title)
                        self.fail(error_title)
                else:
                    if psr.verify_psr1_disable_sequence(adapter, panel, driver_disable_etl, h_total, v_total, False) is False:
                        error_title = "PSR1 Disable sequence check during driver disable is Failed"
                        _report_gdhm(error_title)
                        self.fail(error_title)
                    logging.info("PASS: {0} verification on {1} during driver disable".format(feature_str, panel.port))
                    logging.info("Step: Verifying {0} on {1} after driver restart".format(feature_str, panel.port))
                    if psr.verify_psr1_enable_sequence(adapter, panel, etl_file) is False:
                        error_title = "PSR1 enable sequence check during driver enable is Failed"
                        _report_gdhm(error_title)
                        self.fail(error_title)
                self.validate_feature()
                logging.info("PASS: {0} verification on {1} after driver restart".format(feature_str, panel.port))


##
# @brief        Helper function to start the etl tracer
# @return       True if ETL tracer start tis successful, False otherwise
def start_capture():
    assert etl_tracer.stop_etl_tracer(), "Failed to stop etl trace"
    if os.path.exists(etl_tracer.GFX_TRACE_ETL_FILE):
        file_name = 'GfxTraceBefore_driver_disable_' + str(time.time()) + '.etl'
        etl_file_path = os.path.join(test_context.LOG_FOLDER, file_name)
        os.rename(etl_tracer.GFX_TRACE_ETL_FILE, etl_file_path)
    if etl_tracer.start_etl_tracer() is False:
        logging.error("Failed to start ETL Tracer")
        return False
    return True


##
# @brief        Helper function to stop the etl tracer
# @param[in]    name string name of the etl file
# @return       True if ETL tracer stop tis successful, False otherwise
def end_capture(name):
    assert etl_tracer.stop_etl_tracer(), "Failed to start etl trace"
    etl_file_path = etl_tracer.GFX_TRACE_ETL_FILE
    if os.path.exists(etl_tracer.GFX_TRACE_ETL_FILE):
        file_name = name + '_' + str(time.time()) + '.etl'
        etl_file_path = os.path.join(test_context.LOG_FOLDER, file_name)
        os.rename(etl_tracer.GFX_TRACE_ETL_FILE, etl_file_path)

    if etl_tracer.start_etl_tracer() is False:
        logging.error("Failed to start ETL Tracer after driver disable")
    return etl_file_path


def _report_gdhm(error_title):
    gdhm.report_bug(
        title="[PowerCons][PSR] " + error_title,
        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
        component=gdhm.Component.Driver.DISPLAY_POWERCONS,
        priority=gdhm.Priority.P2,
        exposure=gdhm.Exposure.E2
    )


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(DriverRestart))
    test_environment.TestEnvironment.cleanup(test_result)
