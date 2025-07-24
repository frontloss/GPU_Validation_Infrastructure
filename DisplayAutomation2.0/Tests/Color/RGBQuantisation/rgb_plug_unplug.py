#######################################################################################################################
# @file         rgb_plug_unplug.py
# @addtogroup   Test_Color
# @section      RGBPlugUnplug
# @remarks      @ref rgb_plug_unplug.py \n
#               The test script applies PC Modeset : 1280*1024 and CEA Modeset : 1920*1080 and invokes the driver escape
#               call to set different quantisation ranges and perform register level verification
#               Expectations :
#               When PC Mode is applied : Default range -> Full range, Limited range -> Limited range, Full range - > Full range
#               When CEA Mode is applied :Default range -> Limited range, Limited range -> Limited range, Full range -> Full range
#               Persistence of quantisation range, oCSC Enable, oCSC Coeff, Post offsets and Pre offsets are verified
#               with events such as HotUnplug and Plug
# CommandLine:  python rgb_plug_unplug.py  -HDMI_B HDMI_DELL.EDID -CONFIG SINGLE -LOGLEVEL DEBUG
# @author       Vimalesh D
#######################################################################################################################
import time
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.display_config import display_config
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE
from Libs.Core.wrapper.driver_escape_args import AviInfoFrameArgs
from Tests.Color.color_common_base import *
from Tests.Color import color_common_utility
from Tests.Color.RGBQuantisation import rgb_verification


class RGBPlugUnplug(ColorCommonBase):
    disp_config = display_config.DisplayConfiguration()
    avi_info = AviInfoFrameArgs()
    quantisation_range = rgb_verification.RgbQuantisationRange
    refresh_rate = 60
    modeset_status = None
    status = False
    res_conv_type_dict = {0:{"modeset":[1920,1080],"expected_conv_type":[("STUDIO_TO_STUDIO", quantisation_range.LIMITED.value), ("STUDIO_TO_STUDIO", quantisation_range.LIMITED.value), ("STUDIO_TO_FULL", quantisation_range.FULL.value)]},
                                1:{"modeset":[1280,1024],"expected_conv_type":[("FULL_TO_FULL", quantisation_range.FULL.value), ("FULL_TO_STUDIO", quantisation_range.LIMITED.value),("FULL_TO_FULL",  quantisation_range.FULL.value)]}}

    def HotplugUnplug(self):

        self.cmd_line_param = cmd_parser.parse_cmdline(sys.argv)

        for key, value in self.cmd_line_param.items():
            if cmd_parser.display_key_pattern.match(key) is not None:
                if value['connector_port'] is not None:
                    self.connected_list.insert(value['index'], value['connector_port'])

        if color_common_utility.start_etl_capture("Hot_Unplug_and_plug") is False:
            self.fail("GfxTrace failed to start")

        if color_common_utility.hotunplug_plug_display_etl_trace(self.cmd_line_param, cmd_parser,
                                                                 self.connected_list) is False:
            color_common_utility.stop_etl_capture("Hot_Unplug_and_plug")
            self.fail("Failed to hotunplug and  plug display event")

    def runTest(self):
        set_quant_list = [self.quantisation_range.DEFAULT.value, self.quantisation_range.LIMITED.value, self.quantisation_range.FULL.value]
        bpc = 8

        self.enumerated_displays = self.config.get_enumerated_display_info()
        for display_index in range(self.enumerated_displays.Count):

            if self.enumerated_displays.ConnectedDisplays[display_index].IsActive:
                target_id = self.enumerated_displays.ConnectedDisplays[display_index].TargetID
                supported_modes = self.disp_config.get_all_supported_modes([target_id])
                pipe = color_common_utility.get_current_pipe(str(CONNECTOR_PORT_TYPE(
                    self.enumerated_displays.ConnectedDisplays[display_index].ConnectorNPortType)))

                ##
                # Apply PC AND CEA mode

                for resolution in range(0, len(self.res_conv_type_dict)):
                    for key, values in supported_modes.items():
                        for mode in values:
                            if mode.HzRes == self.res_conv_type_dict[resolution]["modeset"][0] and mode.VtRes == self.res_conv_type_dict[resolution]["modeset"][1] and mode.scaling == enum.MDS:
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
                        for set_range in range(0, len(set_quant_list)):

                            output, status = color_common_utility.get_set_avi_info(self.enumerated_displays,
                                                                                   display_index, self.avi_info,
                                                                                   set_quant_list[set_range])
                            if status:
                                logging.info(output)
                            else:
                                self.fail("Failed to set the quantisation range")

                            output, status = color_common_utility.verify_quantisation_range_and_ocsc(self.platform,pipe, bpc,set_quant_list[set_range],self.res_conv_type_dict[resolution]["expected_conv_type"][set_range][1],self.res_conv_type_dict[resolution]["expected_conv_type"][set_range][0])
                            if status is False:
                                self.fail(output)

                            time.sleep(5)
                            self.HotplugUnplug()

                            ##
                            # Persistence check for quantisation,ocsc,ocsc coeff ,pre and post with ref_values
                            logging.info(
                                "Verification for persistence check for quantisation,ocsc ,ocsc coeff ,pre and post with ref_values started")
                            output, status = color_common_utility.verify_quantisation_range_and_ocsc(self.platform,pipe, bpc,set_quant_list[set_range],self.res_conv_type_dict[resolution]["expected_conv_type"][set_range][1],self.res_conv_type_dict[resolution]["expected_conv_type"][set_range][0])

                            if status:
                                logging.info(output)
                                logging.info("Verification for persistence check was successful")
                            else:
                                self.fail(output)
                    else:
                        self.fail("Failed to apply required modeset")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
