#######################################################################################################################
# @file         port_sync_with_fms.py
# @addtogroup   Powercons
# @section      PORTSYNC
# @brief        Test for port sync in FMS scenario
#
# @author       Bhargav Adigarla
#######################################################################################################################
import os
import time
import shutil
from Libs.Core import app_controls
from Libs.Core.test_env import test_environment, test_context
from Libs.Core.logger import etl_tracer
from Tests.PowerCons.Modules import workload
from Tests.EDP.FMS import fms
from Tests.PowerCons.Functional.PORTSYNC.port_sync_base import *


##
# @brief        This class contains basic port sync tests with FMS
class TestBasicFms(PortSyncBase):
    ############################
    # Test Function
    ############################

    ##
    # @brief        this function verifies port sync before FMS
    # @return       None
    # @cond
    @common.configure_test(repeat=True)
    # @endcond
    def t_10_test_pre_fms_verify(self):
        self.verify_basic()

    ##
    # @brief        this function verifies FMS
    # @return       None
    def t_11_test_verify_fms(self):
        power_event = display_power.PowerEvent.S4
        if etl_tracer.start_etl_tracer() is False:
            self.fail("Failed to start ETL Tracer (Test Issue)")

        if self.display_power_.invoke_power_event(power_event, common.POWER_EVENT_DURATION_DEFAULT) is False:
            self.fail('Failed to invoke power event %s' % power_event.name)

        ##
        # Stop ETL Tracer
        if etl_tracer.stop_etl_tracer() is False:
            self.fail("Failed to stop ETL Tracer (Test Issue)")

        file_name = "GfxTrace_fms_" + str(time.time()) + ".etl"
        new_boot_etl_file = os.path.join(test_context.LOG_FOLDER, file_name)

        ##
        # Make sure etl file is present
        if os.path.exists(etl_tracer.GFX_TRACE_ETL_FILE) is False:
            logging.error(etl_tracer.GFX_TRACE_ETL_FILE + " NOT found.")

        ##
        # Rename the ETL file to avoid overwriting
        shutil.move(etl_tracer.GFX_TRACE_ETL_FILE, new_boot_etl_file)
        if fms.verify(new_boot_etl_file, {_: True for _ in self.lfp_panels}) is False:
            self.fail("FMS verification failed after {0}".format(power_event.name))

    ##
    # @brief        this function verifies port sync after FMS
    # @return       None
    def t_12_test_post_fms_verify(self):
        self.verify_basic()

    ############################
    # Helper Function
    ############################
    ##
    # @brief        this function verifies port sync
    # @return       None
    def verify_basic(self):
        for adapter in dut.adapters.values():
            if port_sync.verify(adapter, self.lfp_panels) is True:
                logging.info("\tPort sync programming verification successful")

                if len(self.lfp_panels) == 2:
                    monitors = app_controls.get_enumerated_display_monitors()
                    monitor_ids = [_[0] for _ in monitors]
                    etl_file, _ = workload.run(workload.SCREEN_UPDATE, [monitor_ids])

                    if port_sync.verify_vbis(self.lfp_panels, etl_file) is False:
                        self.fail("\tPort sync VBI timing verification Failed")

                    logging.info("\tPort sync functional verification successful")
            else:
                self.fail("\tPort sync verification failed")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.runner.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(TestBasicFms))
    test_environment.TestEnvironment.cleanup(test_result)