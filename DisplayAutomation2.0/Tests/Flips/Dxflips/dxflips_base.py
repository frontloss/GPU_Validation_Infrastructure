##
# @file         dxflips_base.py
# @brief        The script consists of unittest setup and tear down classes for Dxflips.
#                   * Parse command line.
#                   * Plug and unplug of displays.
# @author       Sunaina Ashok


import logging
import unittest
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.display_power import DisplayPower
from Tests.Flips import flip_helper, per_process_helper
from Tests.test_base import TestBase

##
# @brief    Contains unittest setUp and tearDown functions to parse the command line, plug and unplug the displays.
class DxflipsBase(TestBase):
    connected_list = []
    display_config = DisplayConfiguration()
    display_pwr = DisplayPower()
    feature = None
    scenario = None
    app = None
    eg_control = None
    eg_mode = None
    per_app = None
    power_plan = None

    ##
    # @brief        Unittest Setup function
    # @return       None
    def setUp(self):
        logging.info(" TEST STARTS HERE ".center(flip_helper.flip_verification.MAX_LINE_WIDTH, "*"))

        self.custom_tags["-FEATURE"] = ['SPEEDFRAME', 'FRAMEPACING', 'ASYNCFLIPS', 'ENDURANCE_GAMING', 'VSYNC_OFF',
                                        'VSYNC_ON', 'SMOOTH_SYNC', 'PERPROCESS']
        self.custom_tags["-FPS"] = ['HIGHFPS', 'LOWFPS', 'HIGHLOWFPS', 'MAX_FPS']
        self.custom_tags["-APPEVENTS"] = ['FULLSCREEN_WINDOWED', 'VSYNCSWITCH', 'WINDOWED', '3DAPP_MEDIA',
                                          'FULLSCREEN']
        self.custom_tags["-APP"] = ["FLIPAT", "TRIVFLIP", "FLIPMODELD3D12", "CLASSICD3D"]
        self.custom_tags["-EG_CONTROL"] = ["TURN_ON", "TURN_OFF", "AUTO"]
        self.custom_tags["-EG_MODE"] = ["BETTER_PERFORMANCE", "BALANCED", "MAXIMUM_BATTERY"]
        self.custom_tags["-VERIFY"] = ['FLIPAT_SMOOTHSYNC', 'CLASSICD3D_VSYNCON', 'FLIPMODEL_SPEEDFRAME',
                                       'FLIPAT_CFPS', 'FLIPAT_VSYNCON_CLASSICD3D_SMOOTHSYNC',
                                       'FLIPAT_SPEEDFRAME_FLIPMODEL_VSYNCON',
                                       'FLIPMODEL_SPEEDFRAME_CLASSICD3D_CFPS',
                                       'FLIPAT_SMOOTHSYNC_CLASSICD3D_VSYNCON_FLIPMODEL_CFPS',
                                       'CLASSICD3D_VSYNCOFF', 'FLIPAT_VSYNCOFF_CLASSICD3D_VSYNCON']
        self.custom_tags["-POWER_PLAN"] = ['SAVER', 'BALANCE', 'PERFORMANCE']

        super().setUp()
        self.scenario = str(self.context_args.test.cmd_params.test_custom_tags["-SCENARIO"][0])
        self.feature = str(self.context_args.test.cmd_params.test_custom_tags["-FEATURE"][0])
        self.appevents = str(self.context_args.test.cmd_params.test_custom_tags["-APPEVENTS"][0])
        self.fps = str(self.context_args.test.cmd_params.test_custom_tags["-FPS"][0])
        self.app = str(self.context_args.test.cmd_params.test_custom_tags["-APP"][0])
        self.eg_control = str(self.context_args.test.cmd_params.test_custom_tags["-EG_CONTROL"][0])
        self.eg_mode = str(self.context_args.test.cmd_params.test_custom_tags["-EG_MODE"][0])
        self.feature_set = str(self.context_args.test.cmd_params.test_custom_tags["-VERIFY"][0])
        self.power_plan = str(self.context_args.test.cmd_params.test_custom_tags["-POWER_PLAN"][0])

        ##
        # Feature Enabling through IGCL
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if self.feature == 'ENDURANCE_GAMING':
                    # AC to DC power supply
                    if flip_helper.toggle_battery(self.display_pwr, ac_to_dc=True) is False:
                        self.fail("Failed to switch from AC to DC power mode.")

                    # registry changes for EG
                    if flip_helper.eg_registry_setup(set_key=True) is False:
                        self.fail("Failed to create EGSoCThrottling Registry Key ")

                    # enabling EG from the IGCL
                    if flip_helper.enable_disable_endurance_gaming_registry(self.eg_control, self.eg_mode) is False:
                        self.fail(f"FAIL: {self.feature} feature is not enabled via IGCL")
                    logging.info(f"PASS: {self.feature} feature is enabled in IGCL")
                elif self.feature not in ['ASYNCFLIPS', 'FRAMEPACING', 'PERPROCESS']:
                    if flip_helper.enable_disable_asyncflip_feature(self.feature, panel) is False:
                        self.fail(f"FAIL: {self.feature} feature is not enabled via IGCL")
                    logging.info(f"PASS: {self.feature} feature is enabled via IGCL")


    ##
    # @brief        unittest TearDown function
    # @return       None
    def tearDown(self):
        logging.info(" TEST ENDS HERE ".center(flip_helper.flip_verification.MAX_LINE_WIDTH, "*"))
        if self.feature == "ENDURANCE_GAMING":
            if flip_helper.eg_registry_setup(set_key=False) is False:
                self.fail("Failed to delete EGSoCThrottling Registry Key")
            if flip_helper.toggle_battery(self.display_pwr, dc_to_ac=True) is False:
                self.fail("Failed to switch from DC to AC power mode.")
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if self.feature not in ['ASYNCFLIPS', 'FRAMEPACING', 'PERPROCESS']:
                    if flip_helper.enable_disable_asyncflip_feature('APPLICATION_DEFAULT', panel) is False:
                        self.fail("FAIL: Application Default is not enabled via IGCL")
                    logging.info("PASS: Application Default is enabled via IGCL")
                elif self.feature in ["PERPROCESS"]:
                    app_feature_mapping = per_process_helper.FeatureMapping[self.feature_set].value
                    for key, value in app_feature_mapping.items():
                        self.per_app = key
                        if flip_helper.enable_disable_asyncflip_feature('APPLICATION_DEFAULT', panel,
                                                                        self.per_app) is False:
                            self.fail(f"FAIL: {self.feature} setting for feature {value} is not disabled via IGCL for "
                                      f"app {self.per_app}")
                        logging.info(f"PASS: {self.feature} setting for feature {value} is disabled via IGCL for app "
                                     f"{self.per_app}")

                # Workaround to enable Speed Frame till its enabled by default
                if self.feature == "SPEEDFRAME":
                    flip_helper.enable_disable_speed_sync(flip_helper.RegistryStatus.DISABLE, panel)
        super().tearDown()


dxflip_base = DxflipsBase()
if __name__ == '__main__':
    unittest.main()