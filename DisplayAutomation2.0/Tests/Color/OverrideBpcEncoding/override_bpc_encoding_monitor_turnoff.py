#######################################################################################################################
# @file         override_bpc_encoding_monitor_turnoff.py
# @addtogroup   Test_Color
# @section      override_Bpc_encoding
# @remarks      @ref override_bpc_encoding_monitor_turnoff.py \n
#               The test script applies the modeset as 19*10 or 4K invokes the driver escape
#               call to set different bpc and encoding and perform register level verification
#               Expectations :
#               When supported BPC and Encoding are applied -> Expect the applied BPC and Encoding
#               to persist after performing after monitor turn off
# CommandLine:  python override_bpc_encoding_basic.py -HDMI_B SamsungJS9500_HDR.bin -CONFIG SINGLE -LOGLEVEL debug
#               python override_bpc_encoding_basic.py -HDMI_B HDMI_DELL_U2711.EDID -CONFIG SINGLE -LOGLEVEL debug
# @author       Vimalesh D
#######################################################################################################################
import time
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.wrapper.driver_escape_args import CuiDeepColorInfo, IGCCSupportedEncoding, IGCCSupportedBpc, CuiEscOperationType, AviEncodingMode
from Libs.Core import driver_escape
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE
from Tests.Color.OverrideBpcEncoding.override_bpc_encoding_verification import get_bpc_encoding_pair, verify_bpc_pixel_encoding_register_programming
from Tests.Color import color_common_utility
from Tests.Color.color_common_base import *


class OverrideBpcEncodingMonitorTurnOffOn(ColorCommonBase):

    def runTest(self):

        self.enumerated_displays = self.config.get_enumerated_display_info()
        avi_encoding_mode = AviEncodingMode
        for display_index in range(self.enumerated_displays.Count):

            if self.enumerated_displays.ConnectedDisplays[display_index].IsActive:
                target_id = self.enumerated_displays.ConnectedDisplays[display_index].TargetID
                pipe = color_common_utility.get_current_pipe(str(
                    CONNECTOR_PORT_TYPE(self.enumerated_displays.ConnectedDisplays[display_index].ConnectorNPortType)))

                cui_override_deep_color_info_set = CuiDeepColorInfo()
                cui_override_deep_color_info_set.opType = CuiEscOperationType.GET.value
                cui_override_deep_color_info_set.display_id = target_id

                ##
                # Get escape call
                status, cui_override_deep_color_info_set = driver_escape.get_set_output_format(
                    self.enumerated_displays.ConnectedDisplays[display_index].DisplayAndAdapterInfo,
                    cui_override_deep_color_info_set)
                if status:
                    logging.info("Successfully get the override bpc and encoding through escape")
                else:
                    self.fail("Failed to get the override bpc and encoding")

                combo_bpc_encoding = get_bpc_encoding_pair(cui_override_deep_color_info_set)

                cui_override_deep_color_info_set.opType = CuiEscOperationType.SET.value

                for index in range(len(combo_bpc_encoding)):
                    bpc = str(combo_bpc_encoding[index][0])
                    encoding = str(combo_bpc_encoding[index][1])

                    cui_override_deep_color_info_set.overrideBpcValue = IGCCSupportedBpc[bpc].value
                    cui_override_deep_color_info_set.overrideEncodingFormat = IGCCSupportedEncoding[encoding].value

                    ##
                    # Set escape call
                    status, cui_override_deep_color_info_set = driver_escape.get_set_output_format(
                        self.enumerated_displays.ConnectedDisplays[display_index].DisplayAndAdapterInfo,
                        cui_override_deep_color_info_set)

                    if status:
                        logging.info("Pass: Successfully set the override bpc and encoding through escape")
                        time.sleep(5)

                        ##
                        # Verify before and after event to log the if any failure
                        if verify_bpc_pixel_encoding_register_programming(pipe, self.platform, avi_encoding_mode, bpc,
                                                                          encoding):
                            logging.info("Pass: Register verification success for current BPC and Encoding")
                        else:
                            self.fail("Fail: Register verification failed for current BPC and Encoding")

                        ##
                        # Monitor Turnoff/Turn on
                        if color_common_utility.monitor_turn_off_on_events() is False:
                            self.fail("Fail: Failed to perform Monitor Turn Off-On Event")
                        logging.info("Successfully performed the Monitor Turn Off-On Event")
                        time.sleep(5)

                        if verify_bpc_pixel_encoding_register_programming(pipe,self.platform, avi_encoding_mode, bpc, encoding):
                            logging.info("Pass: Register verification success after performing monitor turn off-on event for current BPC and Encoding")
                        else:
                            self.fail("Fail: Register verification failed after performing monitor turn off-on event for current BPC and Encoding")
                    else:
                        self.fail("Failed to set the override bpc and encoding")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)