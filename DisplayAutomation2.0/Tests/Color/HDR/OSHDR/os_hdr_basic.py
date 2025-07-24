#######################################################################################################################
# @file         os_hdr_basic.py
# @addtogroup   Test_Color
# @section      os_hdr_basic
# @remarks      @ref os_hdr_basic.py \n
#               The test script takes the HDR display info and configuration to be applied through command line.
#               Test script invokes the OS API DisplayConfigSetDeviceInfo() to enable\disable HDR for all the active
#               HDR displays
#               Basic register verification (HDR Mode in Pipe_Misc register) will be performed.
#               To-Do : Add ETL Parsing for Metadata
# CommandLine:  python os_hdr_basic.py -edp_a SINK_EDP50 -config SINGLE
#               python os_hdr_basic.py -hdmi_b  SamsungJS9500_HDR.bin -config SINGLE
#               python os_hdr_basic.py -dp_b  Benq_SW320.bin  DP_HDR_DPCD.txt -config SINGLE
# @author       Smitha B
#######################################################################################################################
import time
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Color.HDR.OSHDR.os_hdr_base import *
from Tests.Color.color_common_base import *


class OSHDRBasic(OSHDRBase):

    os_hdr_verify = os_hdr_verification.OSHDRVerification()

    def runTest(self):

        # Check Power Mode  for DC or AC to check the HDR Option temporarily disabled
        result, status = color_common_utility.check_and_apply_power_mode()
        if status:
            logging.info(result)
        else:
            self.fail(result)

        ##
        ##
        # Enable OS_HDR on all active displays
        self.enumerated_displays = self.config.get_enumerated_display_info()
        super().toggle_and_verify_hdr(toggle="ENABLE")

        time.sleep(5)

        ##
        # Disable HDR
        self.enumerated_displays = self.config.get_enumerated_display_info()
        super().toggle_and_verify_hdr(toggle="DISABLE")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
