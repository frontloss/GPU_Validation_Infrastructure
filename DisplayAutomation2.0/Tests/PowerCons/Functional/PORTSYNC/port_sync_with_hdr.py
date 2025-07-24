#######################################################################################################################
# @file         port_sync_with_hdr.py
# @addtogroup   Powercons
# @section      PORTSYNC
# @brief        Test to check HDR when CMTG enabled,
#
# @author       Bhargav Adigarla
#######################################################################################################################
from Libs.Core.test_env import test_environment
from Libs.Core import app_controls
from Tests.PowerCons.Modules import workload
from Libs.Core.display_config.display_config import configure_hdr
from Tests.Color.HDR.OSHDR import os_hdr_verification
from Tests.PowerCons.Functional.PORTSYNC.port_sync_base import *


##
# @brief        This class contains basic port sync tests with HDR
class PortSyncWithHdr(PortSyncBase):
    ##
    # @brief        this function verifies port sync
    # @return       None
    def t_10_test_basic(self):
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

    ##
    # @brief        this function verifies HDR after port sync
    # @return       None
    def t_11_verify_hdr(self):
        os_hdr_verify = os_hdr_verification.OSHDRVerification()
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                hdr_error_code = configure_hdr(panel.display_info.DisplayAndAdapterInfo, enable=True)
                ##
                # Decode HDR Error Code and Verify
                if os_hdr_verify.is_error("OS_HDR", hdr_error_code, "ENABLE") is False:
                    self.fail("Failed to enable HDR")

                ##
                # Verify PIPE_MISC for register verification
                if os_hdr_verify.verify_hdr_mode(panel,"ENABLE", common.PLATFORM_NAME) is False:
                    self.fail("HDR PIPE_MISC register verification failed")
                else:
                    self.fail("HDR Verification successful")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.runner.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(PortSyncWithHdr))
    test_environment.TestEnvironment.cleanup(test_result)