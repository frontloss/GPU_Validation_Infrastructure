########################################################################################################################
# @file         darkscreen_detection_singleplane.py
# @brief        This script contains test to flip single plane on single or multiple displays with different plane
#               parameters.Test verifies display color pipeline programming and also checks for underrun.
# @author       Nivetha.B
########################################################################################################################

from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Darkscreen_Detection.darkscreen_detection_base import *


##
# @brief   Contains functions to verify display single plane dark screen detection
class DarkScreenSinglePlane(DarkScreenDetectionBase):

    ##
    # @brief     Set desktop background to black and detect
    # @return    None
    # @cond
    @common.configure_test(selective=['BLACK'])
    # @endcond
    def t_11_black(self) -> None:
        # set desktop background to solid black and verify if black screen is detected
        environment = system_utility.SystemUtility().get_execution_environment_type()
        images = ["dark_screen.png", "dark_screen_1920_1200.png", "dark_screen_4096_2160"]
        if environment in ["SIMENV_FULSIM", "SIMENV_PIPE2D"]:
            presi_crc_env_settings.set_hdwm_properties_show_cfg_msg_on(action=True)
            self.set_background_pre_si(color=Color.BLACK)
        width, height = self.apply_native_mode()
        self.convert_bin_to_png(width, height, 'black.txt')
        max_trials = 3
        result = False
        for trial in range(max_trials):
            self.set_background(images[trial])
            result = self.verify_dark_screen(black_bg=True)
            if result:
                break
        if not result:
            self.fail(f"Black screen is not detected when screen is black")
        logging.info(f"PASS: Black screen is detected")

    ##
    # @brief     Set desktop background to white and detect
    # @return    None
    # @cond
    @common.configure_test(selective=['WHITE'])
    # @endcond
    def t_12_white(self) -> None:
        environment = system_utility.SystemUtility().get_execution_environment_type()
        # set desktop background to solid white and verify if black screen is not detected
        if environment in ["SIMENV_FULSIM", "SIMENV_PIPE2D"]:
            presi_crc_env_settings.set_hdwm_properties_show_cfg_msg_on(action=True)
            self.set_background_pre_si(color=Color.WHITE)
        self.set_background(image="white.png")
        if not self.verify_dark_screen(black_bg=False):
            self.fail(f"Black screen is detected when screen is not black")
        logging.info(f"PASS: Black screen is not detected")

    ##
    # @brief     Set desktop background to red and detect
    # @return    None
    # @cond
    @common.configure_test(selective=['RED'])
    # @endcond
    def t_13_red(self) -> None:

        # set desktop background to solid red and verify if black screen is not detected
        environment = system_utility.SystemUtility().get_execution_environment_type()
        if environment in ["SIMENV_FULSIM", "SIMENV_PIPE2D"]:
            presi_crc_env_settings.set_hdwm_properties_show_cfg_msg_on(action=True)
            self.set_background_pre_si(color=Color.RED)
        self.set_background(image="wallpaper.png")
        if not self.verify_dark_screen(black_bg=False):
            self.fail(f"Black screen is detected when screen is not black")
        logging.info(f"PASS: Black screen is not detected")

    ##
    # @brief     Set desktop background to black with desktop icons and detect
    # @return    None
    # @cond
    @common.configure_test(selective=['PATTERN'])
    # @endcond
    def t_14_black_desktop_icons(self) -> None:

        # set desktop background to black and desktop icons and verify if black screen is not detected
        environment = system_utility.SystemUtility().get_execution_environment_type()
        if environment in ["SIMENV_FULSIM", "SIMENV_PIPE2D"]:
            presi_crc_env_settings.set_hdwm_properties_show_cfg_msg_on(action=True)
            self.set_background_pre_si(color=Color.BLACK, plain_bg=False)
        self.set_background(image="color_ramp_12bpc.png")
        if not self.verify_dark_screen(black_bg=False):
            self.fail(f"Black screen is detected when screen is not black")
        logging.info(f"PASS: Black screen is not detected")

    ##
    # @brief     Set desktop background to grey and detect
    # @return    None
    # @cond
    @common.configure_test(selective=['GREY'])
    # @endcond
    def t_15_grey(self) -> None:
        # set desktop background to solid black and verify if black screen is detected
        environment = system_utility.SystemUtility().get_execution_environment_type()
        if environment in ["SIMENV_FULSIM", "SIMENV_PIPE2D"]:
            presi_crc_env_settings.set_hdwm_properties_show_cfg_msg_on(action=True)
            self.set_background_pre_si(color=Color.GREY)
        self.set_background(image="grey.png")
        if not self.verify_dark_screen(black_bg=False):
            self.fail(f"Black screen is detected when screen is not black")
        logging.info(f"PASS: Black screen is not detected")

    ##
    # @brief     Set YCbCr mode and desktop background to black and detect
    # @return    None
    # @cond
    @common.configure_test(selective=['BLACK_YCBCR420'])
    # @endcond
    def t_16_ycbcr420_black(self) -> None:
        # set desktop background to solid black and verify if black screen is detected
        for gfx_index, adapter in TestBase.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                # Enable YCbCr420
                if not ycbcr.enable_disable_ycbcr(port, panel.display_and_adapterInfo, True, YuvSampling.YUV420):
                    self.fail("Failed to enable YCbCr 420")
        self.set_background(image="dark_screen_4096_2160.png")
        result = self.verify_dark_screen(black_bg=True)
        if not result:
            self.fail(f"Black screen is not detected when screen is black")
        logging.info(f"PASS: Black screen is detected")

    ##
    # @brief     Set YCbCr mode and desktop background to black and detect
    # @return    None
    # @cond
    @common.configure_test(selective=['BLACK_YCBCR422'])
    # @endcond
    def t_17_ycbcr422_black(self) -> None:
        # set desktop background to solid black and verify if black screen is detected
        images = ["dark_screen.png", "dark_screen_1920_1200.png", "dark_screen_4096_2160"]
        width, height = self.apply_native_mode()
        for gfx_index, adapter in TestBase.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                # Enable YCbCr422
                if not ycbcr.enable_disable_ycbcr(port, panel.display_and_adapterInfo, True, YuvSampling.YUV422):
                    self.fail("Failed to enable YCbCr 422")
        self.convert_bin_to_png(width, height, 'black.txt')
        max_trials = 3
        result = False
        for trial in range(max_trials):
            self.set_background(images[trial])
            result = self.verify_dark_screen(black_bg=True)
            if result:
                break
        if not result:
            self.fail(f"Black screen is not detected when screen is black")
        logging.info(f"PASS: Black screen is detected")

    ##
    # @brief     Set YCbCr mode and desktop background to black and detect
    # @return    None
    # @cond
    @common.configure_test(selective=['BLACK_YCBCR444'])
    # @endcond
    def t_18_ycbcr444_black(self) -> None:
        # set desktop background to solid black and verify if black screen is detected
        images = ["dark_screen.png", "dark_screen_1920_1200.png", "dark_screen_4096_2160"]
        width, height = self.apply_native_mode()
        for gfx_index, adapter in TestBase.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                # Enable YCbCr444
                if not ycbcr.enable_disable_ycbcr(port, panel.display_and_adapterInfo, True, YuvSampling.YUV444):
                    self.fail("Failed to enable YCbCr 444")
        self.convert_bin_to_png(width, height, 'black.txt')
        max_trials = 3
        result = False
        for trial in range(max_trials):
            self.set_background(images[trial])
            result = self.verify_dark_screen(black_bg=True)
            if result:
                break
        if not result:
            self.fail(f"Black screen is not detected when screen is black")
        logging.info(f"PASS: Black screen is detected")

    ##
    # @brief     Set YCbCr mode and desktop background to grey and detect
    # @return    None
    # @cond
    @common.configure_test(selective=['GREY_YCBCR444'])
    # @endcond
    def t_19_ycbcr444_grey(self) -> None:
        # set desktop background to solid grey and verify if black screen is not detected
        for gfx_index, adapter in TestBase.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                # Enable YCbCr444
                if not ycbcr.enable_disable_ycbcr(port, panel.display_and_adapterInfo, True, YuvSampling.YUV444):
                    self.fail("Failed to enable YCbCr 444")
        self.set_background(image="grey.png")
        if not self.verify_dark_screen(black_bg=False):
            self.fail(f"Black screen is detected when screen is not black")
        logging.info(f"PASS: Black screen is not detected")

    ##
    # @brief     Set YCbCr mode and desktop background to pattern and detect
    # @return    None
    # @cond
    @common.configure_test(selective=['PATTERN_YCBCR420'])
    # @endcond
    def t_20_ycbcr420_pattern(self) -> None:
        # set desktop background to solid pattern and verify if black screen is not detected
        for gfx_index, adapter in TestBase.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                # Enable YCbCr420
                if not ycbcr.enable_disable_ycbcr(port, panel.display_and_adapterInfo, True, YuvSampling.YUV420):
                    self.fail("Failed to enable YCbCr 420")
        self.set_background(image="color_ramp_12bpc.png")
        if not self.verify_dark_screen(black_bg=False):
            self.fail(f"Black screen is detected when screen is not black")
        logging.info(f"PASS: Black screen is not detected")


if __name__ == '__main__':
    TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(DarkScreenSinglePlane))
    TestEnvironment.cleanup(test_result)
