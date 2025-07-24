#######################################################################################################################
# @file         rgb_power_events.py
# @addtogroup   Test_Color
# @section      RGBPowerEvents
# @remarks      @ref rgb_power_events.py \n
#               The test script applies PC Modeset : 1280*1024 and CEA Modeset : 1920*1080 and invokes the driver escape
#               call to set different quantisation ranges and perform register level verification
#               Expectations :
#               When PC Mode is applied : Default range -> Full range, Limited range -> Limited range, Full range - > Full range
#               When CEA Mode is applied :Default range -> Limited range, Limited range -> Limited range, Full range -> Full range
#               Persistence of quantisation range, oCSC Enable, oCSC Coeff, Post offsets and Pre offsets are verified
#               with Power events  S3,S4 and S5
#
# CommandLine:  python rgb_power_events.py  -HDMI_B HDMI_DELL.EDID -CONFIG SINGLE -LOGLEVEL DEBUG
# @author       Vimalesh D
#######################################################################################################################
import time
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.display_config import display_config
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE
from Libs.Core import display_power
from Libs.Core.wrapper.driver_escape_args import AviInfoFrameArgs
from Tests.Color.color_common_base import *
from Tests.Color import color_common_utility
from Tests.Color.RGBQuantisation import rgb_verification


class RGBPowerEvents(ColorCommonBase):

    power_states_list = [display_power.PowerEvent.S3, display_power.PowerEvent.S4, display_power.PowerEvent.S5]
    quantisation_range = rgb_verification.RgbQuantisationRange
    refresh_rate = 60
    modeset_status = None
    status = False
    pipe = 0
    res_conv_type_dict = {0:{"modeset":[1920,1080],"expected_conv_type":[("STUDIO_TO_STUDIO", quantisation_range.LIMITED.value)]},
                                1:{"modeset": [1920, 1080],"expected_conv_type":[("STUDIO_TO_FULL", quantisation_range.FULL.value)]},
                                2:{"modeset":[1280,1024],"expected_conv_type":[("FULL_TO_STUDIO", quantisation_range.LIMITED.value)]}}
    set_quant_list = [quantisation_range.LIMITED.value, quantisation_range.FULL.value, quantisation_range.LIMITED.value]
    temp_pipe_output_csc_status = 0
    bpc = 8
    index = 0
    disp_config = display_config.DisplayConfiguration()
    avi_info = AviInfoFrameArgs()
    supported_modes = None

    def test_before_reboot(self):

        self.enumerated_displays = self.config.get_enumerated_display_info()
        for display_index in range(self.enumerated_displays.Count):

            if self.enumerated_displays.ConnectedDisplays[display_index].IsActive:
                target_id = self.enumerated_displays.ConnectedDisplays[display_index].TargetID
                self.supported_modes = self.disp_config.get_all_supported_modes([target_id])
                self.pipe = color_common_utility.get_current_pipe(
                    str(CONNECTOR_PORT_TYPE(self.enumerated_displays.ConnectedDisplays[display_index].ConnectorNPortType)))
                ##
                # Apply PC AND CEA mode

                for index in range(0, len(self.res_conv_type_dict)):
                    for key, values in self.supported_modes.items():
                        for mode in values:
                            if mode.HzRes == self.res_conv_type_dict[index]["modeset"][0] and mode.VtRes == self.res_conv_type_dict[index]["modeset"][1] and mode.scaling == enum.MDS:
                                mode.refreshRate = self.refresh_rate
                                self.modeset_status = self.disp_config.set_display_mode([mode])
                                break

                    time.sleep(5)
                    if self.modeset_status is not None:
                        ##
                        # Apply Default range
                        # Limited range
                        # and Full range
                        # verify Ocsc

                        output, status = color_common_utility.get_set_avi_info(self.enumerated_displays, display_index,
                                                                               self.avi_info, self.set_quant_list[index])
                        if status:
                            logging.info(output)
                        else:
                            self.fail("Failed to set the quantisation range")

                        output, status = color_common_utility.verify_quantisation_range_and_ocsc(self.platform, self.pipe, self.bpc,self.set_quant_list[index],self.res_conv_type_dict[index]["expected_conv_type"][0][1],self.res_conv_type_dict[index]["expected_conv_type"][0][0])
                        if status is False:
                            self.fail(output)

                        self.power_event = "power_state_" + str(self.power_states_list[index])
                        if color_common_utility.start_etl_capture(self.power_event) is False:
                            self.fail("GfxTrace failed to start")
                        if self.power_states_list[index] == display_power.PowerEvent.S5:

                            if reboot_helper.reboot(self, "test_after_reboot") is False:
                                color_common_utility.stop_etl_capture(self.power_event)
                                self.fail("Failed to reboot the system")
                        else:
                            if color_common_utility.invoke_power_states(self.power_states_list[index]) is False:
                                color_common_utility.stop_etl_capture(self.power_event)
                                self.fail("Failed to invoke power event")
                            else:
                                logging.info("Finished power event")

                                ##
                                # Persistence check for quantisation,ocsc,ocsc coeff ,pre and post with ref_values
                                logging.info(
                                    "Verification for persistence check for quantisation,ocsc ,ocsc coeff ,pre and post with ref_values started")
                                output, status = color_common_utility.verify_quantisation_range_and_ocsc(self.platform,self.pipe, self.bpc,self.set_quant_list[index],self.res_conv_type_dict[index]["expected_conv_type"][0][1],self.res_conv_type_dict[index]["expected_conv_type"][0][0])
                                if status:
                                    logging.info(output)
                                    logging.info("Verification for persistence check was successful")
                                else:
                                    self.fail(output)
                    else:
                        self.fail("Failed to apply required modeset")

    def test_after_reboot(self):

        logging.info("Successfully applied reboot event")
        output, status = color_common_utility.verify_quantisation_range_and_ocsc(self.platform, self.pipe, self.bpc,self.set_quant_list[2],self.res_conv_type_dict[2]["expected_conv_type"][0][1],self.res_conv_type_dict[2]["expected_conv_type"][0][0])
        if status:
            logging.info(output)
            logging.info("Verification for persistence check was successful")
        else:
            self.fail(output)


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('RGBPowerEvents'))
    TestEnvironment.cleanup(outcome)
