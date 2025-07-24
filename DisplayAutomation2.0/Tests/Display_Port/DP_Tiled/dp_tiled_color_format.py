#######################################################################################################################
# @file         dp_tiled_color_format.py
# @brief        This test applies and verifies YUV color formats mentioned by the user
# @author       Supriya Krishnamurthi
#######################################################################################################################

from Libs.Core.display_config import display_config
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Feature.display_mode_enum.mode_enum_xml_parser import ModeEnumHelper
from Tests.Color.Common import color_enums
from Tests.Color.Verification import feature_basic_verify
from Tests.Color.color_common_utility import get_platform_info, get_current_pipe
from Tests.Display_Port.DP_Tiled.display_port_base import *

display_config = display_config.DisplayConfiguration()


##
# @brief        This class contains a test function which implements the mentioned test scenario / test steps.
class DPTiledColorFormat(DisplayPortBase):

    ##
    # @brief        This test plugs required displays, set config, applies max modes, applies the color format given by
    #               the user and verifies if the given mode is successfully enabled by the driver.
    # @return       None
    def runTest(self):

        ##
        # Currently test is designed to plug only one tiled display
        is_required_no_of_panel = len(self.cmd_line_displays) == 2
        self.assertTrue(is_required_no_of_panel, "[Planning Issue] : Test is supporting only 1 Tiled display. ")

        gfx_index = 'gfx_0'
        platform = get_platform_info().upper()
        pipe_list = []

        ##
        # Plug the Tiled display
        self.tiled_display_helper(action="PLUG")

        ##
        # Get current pipe of tiled panel's master port after the plug
        pipe_list.append(get_current_pipe(self.cmd_line_displays[0]))

        ##
        # Fetch the pipe associated with slave port of the tiled panel
        pipe_list.append(chr(ord(pipe_list[0]) + 1))

        ##
        # get the target ids of the plugged displays
        plugged_target_ids = self.display_target_ids()
        logging.info(f"Target ids of plugged displays : {plugged_target_ids}")

        ##
        # set display configuration with topology as given in cmd line
        self.set_config(self.config, no_of_combinations=1)

        ##
        # Apply 5K3K/8k4k resolution and check for applied mode
        self.apply_tiled_max_modes()

        ##
        # Enabling yuv420/yuv422/yuv44 mode given by the user
        if '-COLOR_FORMAT' in sys.argv:
            logging.info(f"Color format given by the user {self.color_format}")
            if self.color_format.lower() == "yuv422":
                is_success = ModeEnumHelper.enable_yuv422_mode('gfx_0', 1)
                self.assertTrue(is_success, "Enabling YUV422 Mode in driver using reg key failed.")
                logging.info("Force Applying YUV422 mode using reg key succeeded")

                # Verify if YUV422 mode is successfully enabled by the driver for each pipe involved in tiled display
                for pipe in pipe_list:
                    is_success = feature_basic_verify.verify_ycbcr_feature(gfx_index, platform, pipe, 1,
                                                                           color_enums.YuvSampling.YUV422)
                    self.assertTrue(is_success, "YUV422 color format verification at {} for {} Expected = PASS "
                                                "Actual = FAIL".format(gfx_index, pipe))

                logging.info("YUV422 mode is successfully enabled by the driver")

            else:
                ##
                # YUV444 currently is supported via YCbCr option and Override Encoding escape and it is supported for
                # HDMI and EDP only. So cannot enable this for DP Tiled
                # TODO: Read and verify YUV420 color format Register. Currently YUV420 block provided in DID extension
                #  block of edid is not parsable by driver. So enable this only after driver supports
                logging.error("[Planning Issue] - Currently only YUV422 can be passed")
                self.fail()

    ##
    # @brief        teardown function
    # @details      reset the regkey set in setup
    # @return       None
    def tearDown(self):
        super().tearDown()
        if self.color_format.lower() == "yuv422":
                is_success = ModeEnumHelper.enable_yuv422_mode('gfx_0', 0)
                self.assertTrue(is_success, "Disabling YUV422 Mode in driver using reg key failed.")
                logging.info("Disabling YUV422 mode using reg key succeeded")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
