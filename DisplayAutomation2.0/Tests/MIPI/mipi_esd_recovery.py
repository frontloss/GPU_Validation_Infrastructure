########################################################################################################################
# @file         mipi_esd_recovery.py
# @brief        It verifies if ESD recovery done with generating TE signal and verifying full mode set.
# @details      CommandLine: python mipi_esd_recovery.py -mipi_a
#               Test will pass only if full mode set event done by driver after TE signal generation, otherwise it fails
# @author       Kruti Vadhavaniya
########################################################################################################################
import os
import shutil
import time

from Libs.Core.logger import etl_tracer, gdhm
from Libs.Core.sw_sim import driver_interface
from Libs.Core.test_env import test_context
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.LFP_Common.FMS import fms
from Tests.MIPI.mipi_base import *


##
# @brief        This class contains test to verify if ESD recovery is done with generating TE signal and
#               verifies modeset
class MipiEsdRecovery(MipiBase):

    ##
    # @brief        This function is used to get mipi port number for a given mipi port
    # @param[in]    port string, name of the port
    # @return       mipi port number
    def map_mipi_port(self, port):
        return 3 if self.mipi_helper.dual_LFP_MIPI else 1 if port[0] == 'MIPI_A' else 2 if port[0] == 'MIPI_C' else 0

    ##
    # @brief        This function is used to get adapter wise display list
    # @return       dict(display_list, adapter_index)
    def get_display_adapter_list(self):
        gfx_index_list = []
        topology, self.display_list, self.display_and_adapter_info_list = self.config.get_current_display_configuration_ex()

        # Extracting adapter wise display list dictionary form display list and adapter list of display and adapter info
        for each_display_and_adapter_info in self.display_and_adapter_info_list:
            gfx_index_list.append(each_display_and_adapter_info.adapterInfo.gfxIndex)
        gfx_index_list = map(str, gfx_index_list)

        gfx_display_dict = {k: v for k, v in zip(self.display_list, gfx_index_list)}

        flipped = {}

        for key, value in gfx_display_dict.items():
            if value not in flipped:
                flipped[value] = [key]
            else:
                flipped[value].append(key)

        gfx_display_dict = flipped
        return gfx_display_dict

    ##
    # @brief        This function verifies if ESD recovery is done with generating TE signal and
    #               verifies modeset
    # @return       None
    def runTest(self):
        status = True

        ##
        # Stop the ETL tracer started during TestEnvironment initialization
        etl_tracer.stop_etl_tracer()

        ##
        # Start ETL tracer for test scenario capture
        if etl_tracer.start_etl_tracer() is False:
            self.fail("Failed to start ETL Tracer (Test Issue)")

        display_adapter_dict = self.get_display_adapter_list()

        for key, value in display_adapter_dict.items():

            gfx_adapter = key
            display_list = value

            gfx_adapter_info = test_context.TestContext.get_gfx_adapter_details()[gfx_adapter]

            if driver_interface.DriverInterface().generate_mipi_te(gfx_adapter_info, self.map_mipi_port(display_list)):
                logging.info("Generating TE signal(for triggering ESD) successful for port:{}".format(display_list))
                time.sleep(2)
            else:
                self.fail("FAIL: Fail to generate TE signal for requested port:{}".format(display_list))

        ##
        # Stop ETL Tracer
        if etl_tracer.stop_etl_tracer() is False:
            self.fail("Failed to stop ETL Tracer (Test Issue)")

        file_name = "GfxTrace_esd_recovery_" + str(time.time()) + ".etl"
        new_boot_etl_file = os.path.join(test_context.LOG_FOLDER, file_name)

        ##
        # Make sure etl file is present
        if os.path.exists(etl_tracer.GFX_TRACE_ETL_FILE) is False:
            gdhm.report_bug(
                title="[MIPI][ESD_RECOVERY] Expected ETL file does not found",
                problem_classification=gdhm.ProblemClassification.LOG_FAILURE,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.error(etl_tracer.GFX_TRACE_ETL_FILE + " NOT found.")

        ##
        # Rename the ETL file to avoid overwriting
        shutil.move(etl_tracer.GFX_TRACE_ETL_FILE, new_boot_etl_file)

        for key, value in display_adapter_dict.items():
            display_list = value
            te_interrupt = self.map_mipi_port(display_list)
            if te_interrupt == 3:
                status_port1 = fms.verify_fms(new_boot_etl_file, "DSI0", self.platform)
                status_port2 = fms.verify_fms(new_boot_etl_file, "DSI1", self.platform)
                if status_port1 != "FULL_MODE_SET" or status_port2 != "FULL_MODE_SET":
                    self.fail(
                        "\tFAIL: ModeSet Expected= Full mode set,Actual= Port 1:{0} Port 2:{1}".format(status_port1,
                                                                                                       status_port2))
            elif te_interrupt == 1:
                status = fms.verify_fms(new_boot_etl_file, "DSI0", self.platform)
            elif te_interrupt == 2:
                status = fms.verify_fms(new_boot_etl_file, "DSI1", self.platform)

        if status != "FULL_MODE_SET":
            self.fail(
                "\tFAIL: ModeSet Expected= Full mode set, Actual= {}".format(status))
        else:
            logging.info("PASS: ModeSet Expected= Full mode set, Actual= Full mode set")

        ##
        # report test failure if fail_count>0
        if (self.fail_count + self.mipi_helper.verify_fail_count) > 0:
            self.fail(f'Some checks in the test have failed. Check error logs. '
                      f'No. of failures= {(self.fail_count + self.mipi_helper.verify_fail_count)}')



if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
