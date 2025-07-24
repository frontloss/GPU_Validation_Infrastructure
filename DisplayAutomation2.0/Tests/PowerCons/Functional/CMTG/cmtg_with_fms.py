########################################################################################################################
# @file         cmtg_with_fms.py
# @brief        Contains basic functional tests covering below scenarios:
#               * CMTG verification with FMS concurrency.
# @author       Bhargav Adigarla
########################################################################################################################
import os
import time
import shutil

from Libs.Core import display_power, enum
from Libs.Core.test_env import test_environment, test_context
from Libs.Core.logger import etl_tracer
from Libs.Feature.powercons import registry
from Tests.PowerCons.Functional.CMTG.cmtg_base import *
from Tests.EDP.FMS import fms


##
# @brief        Contains CMTG with FMS tests
class CmtgFms(CmtgBase):

    ##
    # @brief        This function verifies CMTG with FMS
    # @return       None
    def t_10_cmtg_fms(self):
        for adapter in dut.adapters.values():
            lfp_panels = []
            for panel in adapter.panels.values():
                if panel.is_lfp:
                    if panel.port not in ["MIPI_A", "MIPI_C"]:
                        lfp_panels.append(panel)

            logging.info("CMTG verification before S4 power event")
            self.verify_cmtg()

            if etl_tracer.start_etl_tracer() is False:
                self.fail("Failed to start ETL Tracer (Test Issue)")

            if self.display_power_.invoke_power_event(display_power.PowerEvent.S4,
                                                      common.POWER_EVENT_DURATION_DEFAULT) is False:
                self.fail('Failed to invoke power event S4')

            if etl_tracer.stop_etl_tracer() is False:
                self.fail("Failed to stop ETL Tracer (Test Issue)")

            file_name = "GfxTrace_fms_" + str(time.time()) + ".etl"
            new_boot_etl_file = os.path.join(test_context.LOG_FOLDER, file_name)

            ##
            # Rename the ETL file to avoid overwriting
            shutil.move(etl_tracer.GFX_TRACE_ETL_FILE, new_boot_etl_file)
            if fms.verify(new_boot_etl_file, True) is False:
                self.fail("FMS verification failed after S4")

            logging.info("CMTG verification after S4 power event")
            self.verify_cmtg()

    ##
    # @brief        This function verifies CMTG with FMS disable
    # @return       None
    def t_11_cmtg_fms_cmtg_disable(self):
        for adapter in dut.adapters.values():
            lfp_panels = []
            for panel in adapter.panels.values():
                if panel.is_lfp:
                    if panel.port not in ["MIPI_A", "MIPI_C"]:
                        lfp_panels.append(panel)

            logging.info("CMTG verification before S4 power event")
            self.verify_cmtg()

            display_feature_control = registry.DisplayFeatureControl(adapter.gfx_index)
            display_feature_control.disable_cmtg = 1
            status = display_feature_control.update(adapter.gfx_index)
            if status is False:
                logging.error("\tFailed to update DisplayFeatureControlFields Registry")
                return False

            if not cmtg.verify_cmtg_status(adapter):
                self.fail("CMTG disabled after updating regkey without driver disable/enable")

            logging.info("CMTG enabled as expected")

            if etl_tracer.start_etl_tracer() is False:
                self.fail("Failed to start ETL Tracer (Test Issue)")

            if self.display_power_.invoke_power_event(display_power.PowerEvent.S4,
                                                      common.POWER_EVENT_DURATION_DEFAULT) is False:
                self.fail('Failed to invoke power event S4')

            if etl_tracer.stop_etl_tracer() is False:
                self.fail("Failed to stop ETL Tracer (Test Issue)")

            file_name = "GfxTrace_fms_" + str(time.time()) + ".etl"
            new_boot_etl_file = os.path.join(test_context.LOG_FOLDER, file_name)

            ##
            # Rename the ETL file to avoid overwriting
            shutil.move(etl_tracer.GFX_TRACE_ETL_FILE, new_boot_etl_file)
            if fms.verify(new_boot_etl_file, True) is True:
                self.fail("FMS not expected after S4 with CMTG disable")
            logging.info("Full Mode Set happened as expected")

            if cmtg.verify_cmtg_status(adapter):
                self.fail("CMTG disabled as expected")

            display_feature_control = registry.DisplayFeatureControl(adapter.gfx_index)
            display_feature_control.disable_cmtg = 0
            status = display_feature_control.update(adapter.gfx_index)
            if status is False:
                self.fail("\tFailed to update DisplayFeatureControlFields Registry")

    ##
    # @brief        This function verifies CMTG after driver restart
    # @return       None
    def t_12_cmtg_fms_cmtg_disable_driver_restart(self):
        for adapter in dut.adapters.values():
            lfp_panels = []
            for panel in adapter.panels.values():
                if panel.is_lfp:
                    if panel.port not in ["MIPI_A", "MIPI_C"]:
                        lfp_panels.append(panel)

            logging.info("CMTG verification before S4 power event")
            self.verify_cmtg()

            cmtg_status = cmtg.disable(adapter)
            if cmtg_status is False:
                self.fail("FAILED to disable CMTG")
            if cmtg_status is True:
                status, reboot_required = display_essential.restart_gfx_driver()
                if status is False:
                    self.fail("FAILED to restart the driver")

            if cmtg.verify_cmtg_status(adapter):
                self.fail("CMTG disabled as expected")

            if etl_tracer.start_etl_tracer() is False:
                self.fail("Failed to start ETL Tracer (Test Issue)")

            if self.display_power_.invoke_power_event(display_power.PowerEvent.S4,
                                                      common.POWER_EVENT_DURATION_DEFAULT) is False:
                self.fail('Failed to invoke power event {0}'.format(display_power.PowerEvent.S4.name))

            if etl_tracer.stop_etl_tracer() is False:
                self.fail("Failed to stop ETL Tracer (Test Issue)")

            file_name = "GfxTrace_fms_" + str(time.time()) + ".etl"
            new_boot_etl_file = os.path.join(test_context.LOG_FOLDER, file_name)

            ##
            # Rename the ETL file to avoid overwriting
            shutil.move(etl_tracer.GFX_TRACE_ETL_FILE, new_boot_etl_file)
            if fms.verify(new_boot_etl_file, True) is False:
                self.fail("FMS verification failed after S4")

            if cmtg.verify_cmtg_status(adapter):
                self.fail("CMTG disabled as expected")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(CmtgFms))
    test_environment.TestEnvironment.cleanup(test_result)