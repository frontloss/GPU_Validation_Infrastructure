########################################################################################################################
# @file         fms_hibernate.py
# @brief        This file contains tests for FMS verification after S4 power event
# @author       Tulika
########################################################################################################################

import os
import shutil
import time

from Libs.Core.logger import etl_tracer, gdhm
from Libs.Core.test_env import test_context
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.LFP_Common.FMS import fms
from Tests.LFP_Common.FMS.fms_base import *
from Tests.PowerCons.Functional.CMTG import cmtg
from Tests.PowerCons.Functional.PSR import psr
from Tests.PowerCons.Modules import common


##
# @brief        This class contains tests for FMS verification after S4 power event


class LfpFmsHibernate(LfpFmsBase):
    display_power_ = display_power.DisplayPower()

    ############################
    # Test Function
    ############################

    ##
    # @brief        This test verfies FMS after S4 power event
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["S4", "POST_SI"])
    # @endcond
    def runTest(self):
        power_event = display_power.PowerEvent.S4
        if etl_tracer.start_etl_tracer() is False:
            self.fail("Failed to start ETL Tracer")

        if self.display_power_.invoke_power_event(power_event, common.POWER_EVENT_DURATION_DEFAULT) is False:
            self.fail('Failed to invoke power event %s' % power_event.name)

        ##
        # Stop ETL Tracer
        if etl_tracer.stop_etl_tracer() is False:
            self.fail("Failed to stop ETL Tracer")

        file_name = "GfxTrace_fms_" + str(time.time()) + ".etl"
        new_boot_etl_file = os.path.join(test_context.LOG_FOLDER, file_name)

        ##
        # Make sure etl file is present
        if os.path.exists(etl_tracer.GFX_TRACE_ETL_FILE) is False:
            logging.error(etl_tracer.GFX_TRACE_ETL_FILE + " NOT found.")
        ##
        # Rename the ETL file to avoid overwriting
        shutil.move(etl_tracer.GFX_TRACE_ETL_FILE, new_boot_etl_file)

        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                result = fms.verify_fms_during_power_events(new_boot_etl_file, panel.transcoder, adapter.name,
                                                            panel.target_id, True)
                if result is False:
                    gdhm.report_driver_bug_di(f"{fms.GDHM_FMS} Display is not active")
                    self.fail("FAIL: Display is not active")

                # VSDI-48114 - GOP display will be disabled from S4 resume Xe3 onward
                if adapter.name not in common.PRE_GEN_16_PLATFORMS:
                    self.__check_full_mode_set_status(result)
                elif adapter.name in common.PRE_GEN_13_PLATFORMS:
                    self.__check_fast_mode_set_status(result)
                else:
                    self.verify_fms_based_on_psr_status(adapter, panel, result)

    ##
    # @brief        This function checks fast mode set status
    # @param[in]    adapter
    # @param[in]    panel
    # @param[in]    result
    # @return       None
    def verify_fms_based_on_psr_status(self, adapter, panel, result):
        # Check for Non-PSR/PSR1 panel (For Non-PSR/PSR1 panel CMTG cannot be enabled. GOP will not enable
        # CMTG, driver will do FMS).
        if not panel.psr_caps.is_psr2_supported:
            self.__check_fast_mode_set_status(result)
        else:
            psr_status = psr.is_psr_enabled_in_driver(adapter, panel, psr.UserRequestedFeature.PSR_2)
            cmtg_status = cmtg.verify_cmtg_status(adapter)
            logging.info(f"Feature Status: PSR= {psr_status}, CMTG= {cmtg_status}")
            # As per Bspec, Switching between the local timing generator within the eDP and the CMTG will a
            # modeset. GOP enables CMTG, makes eDP transcoder as slave to CMTG for PSR2 panels. Driver will
            # do full mode set as it is transitioning from non-Cmtg to Cmtg mode and PLL0 will be assigned.

            # Added check for GEN_15_PLATFORMS(LNL), as a part of DCN - 14016406797, HW added capability to
            # enable Cmtg dynamically outside of mode set without PSR2 deep sleep requirement.
            if ((psr_status is False) or (cmtg_status is False)) and (adapter.name in common.PRE_GEN_15_PLATFORMS):
                self.__check_full_mode_set_status(result)
            else:
                self.__check_fast_mode_set_status(result)

    ##
    # @brief        This function checks fast mode set status
    # @param[in]    fms_status
    # @return       None
    def __check_fast_mode_set_status(self, fms_status):
        if fms_status != "FAST_MODE_SET":
            gdhm.report_driver_bug_di(
                f"{fms.GDHM_FMS} ModeSet Expected= FAST_MODE_SET, Actual= {fms_status}")
            self.fail(f"FAIL: ModeSet Expected= FAST_MODE_SET, Actual= {fms_status}")
        logging.info("PASS: ModeSet Expected= FAST_MODE_SET, Actual= FAST_MODE_SET")

    ##
    # @brief        This function checks full mode set status
    # @param[in]    fms_status
    # @return       None
    def __check_full_mode_set_status(self, fms_status):
        if fms_status != "FULL_MODE_SET":
            gdhm.report_driver_bug_di(
                f"{fms.GDHM_FMS} ModeSet Expected= FULL_MODE_SET, Actual= {fms_status}")
            self.fail(f"FAIL: ModeSet Expected= FULL_MODE_SET, Actual= {fms_status}")
        logging.info("PASS: ModeSet Expected= FULL_MODE_SET, Actual= FULL_MODE_SET")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
