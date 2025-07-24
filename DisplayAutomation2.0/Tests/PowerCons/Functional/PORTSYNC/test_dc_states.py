#######################################################################################################################
# @file         test_dc_states.py
# @addtogroup   Powercons
# @section      PORTSYNC
# @brief        Test for port sync with DC states
#
# @author       Bhargav Adigarla
#######################################################################################################################
from Libs.Core.test_env import test_environment
from Libs.Core import app_controls
from Tests.PowerCons.Modules import workload
from Tests.PowerCons.Functional.DCSTATES import dc_state
from Tests.PowerCons.Functional.PORTSYNC.port_sync_base import *


##
# @brief        This class contains basic port sync tests with DC States
class TestDcStates(PortSyncBase):

    ##
    # @brief        this function verifies port sync with DCSTATES
    # @return       None
    def t_10_test_basic(self):
        self.verify_basic()

    ##
    # @brief        This function DC5/6 with Idle desktop
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["DC5", "DC6"])
    # @endcond
    def t_11_state_dc5_dc6_basic(self):
        for adapter in dut.adapters.values():
            logging.info("STEP 1: Verifying DC5/6 with Idle desktop")
            if dc_state.verify_dc5_dc6(adapter, method='IDLE') is True:
                logging.info("\tDC5/6 verification is successful")
            else:
                self.fail("DC5/6 verification failed")

    ##
    # @brief        This function DC9 with CS/S3
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["DC9"])
    # @endcond
    def t_12_state_dc9_basic(self):
        for adapter in dut.adapters.values():
            if dc_state.verify_dc9(adapter) is False:
                self.fail("DC9 verification failed")
            logging.info("\tDC9 verification is successful")

    ##
    # @brief        This function DC6V with APP
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["DC6V"])
    # @endcond
    def t_13_state_dc6v_basic(self):
        for adapter in dut.adapters.values():
            dc6v_status = dc_state.enable_dc6v(adapter)
            if dc6v_status is False:
                self.fail("FAILED to enable DC6v in driver")
            if dc6v_status is True:
                status, reboot_required = display_essential.restart_gfx_driver()
                if status is False:
                    self.fail("FAILED to restart the driver")
            logging.info("STEP 1: Verifying DC6v with App")
            if dc_state.verify_dc6v(adapter, method='APP') is False:
                self.fail("DC6V verification failed")
            logging.info("\tDC6V verification is successful")

    ##
    # @brief        this function verifies port sync
    # @return       None
    # @cond
    @common.configure_test(repeat=True)
    # @endcond
    def t_14_test_basic(self):
        self.verify_basic()

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
    test_result = runner.run(common.get_test_suite(TestDcStates))
    test_environment.TestEnvironment.cleanup(test_result)