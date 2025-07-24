#######################################################################################################################
# @file         display_modeset_custom_modes.py
# @brief        This test adds custom modes through driver escape, applies various modes and verifes DE.
# @details      This test adds custom modes using driver escape and applies them one by one and verifeis DE for each of them.
#
# @author       Ami Golwala
#######################################################################################################################

from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.ModeEnumAndSet.display_mode_enumeration_base import *

##
# @brief        A class which has test method to apply modeset.
class DisplayModeSetCustomModes(ModeEnumAndSetBase):
    ##
    # @brief        Unit-test runTest function. Adding custom modes and Checking Mode enumeration and Modeset.
    # @return       None
    def runTest(self):

        display_and_adapter_info = display_cfg.DisplayConfiguration().get_display_and_adapter_info(self.targetId)
        ##
        # Parsing custom modes xml
        tree = ET.parse(self.custom_mode_xml_file)
        ##
        # custom_mode_handle is the handle for CustomModeTable in the custom modes xml.
        custom_mode_handle = tree.getroot()

        ##
        # Parsing through each EDID instance to create mode structure.
        for EDIDInstance in custom_mode_handle:
            modeIndex = EDIDInstance.get('ModeIndex')
            mode = DisplayMode()
            modeInfo = DisplayModeBlock()
            mode.targetId = self.targetId
            mode.HzRes = int(EDIDInstance.get('HActive'))
            mode.VtRes = int(EDIDInstance.get('VActive'))
            mode.rotation = 1
            mode.refreshRate = int(EDIDInstance.get('RefreshRate'))
            mode.BPP = 4  # Assuming RGBA8888
            mode.scanlineOrdering = self.SCANLINE_DICT[EDIDInstance.get('Scanline')]
            mode.scaling = self.SCALE_DICT[EDIDInstance.get('Scaling')]
            mode.samplingMode = 1  # Assigning default value to RGB
            mode.pixelClock_Hz = int(EDIDInstance.get('PixelCLK'))
            modeInfo.DisplayMode = mode
            modeInfo.PixelClk = int(EDIDInstance.get('PixelCLK'))
            modeControlFlag = DisplayModeControlFlags()
            modeControlFlag.as_int = 0x8
            if ('HDMI' in self.display) and self.dpDongle and modeControlFlag.data.bpc > 1:
                bpc_multiplier = float(bpc_mapping[modeControlFlag.data.bpc]) / float(8)
                if (modeInfo.PixelClk * bpc_multiplier) > 300000000:
                    logging.debug(
                       "ModeIndex: {0} Pixel Clock exceeds 300MHz. Setting 8 BPC as expected".format(modeIndex))
                    modeControlFlag.data.bpc = 1  # 8 BPC

            modeInfo.DisplayModeControlFlag = modeControlFlag

            ##
            # Adding custom modes to previously created apply_mode_list
            if driver_escape.add_custom_mode(display_and_adapter_info, mode.HzRes, mode.VtRes) is True:
                logging.info("Added custom mode: {} X {} for targetID: {}".format(mode.HzRes, mode.VtRes, mode.targetId))
                self.apply_mode_list[modeIndex] = modeInfo

            else:
                gdhm.report_bug(
                    title="Escape call failed : add_custom_mode()",
                    problem_classification=gdhm.ProblemClassification.LOG_FAILURE,
                    component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                logging.error(f"Escape call failed : add_custom_mode() for {mode.targetId}")

        ##
        # Apply and verify mode set.
        self.verify_mode_enum_and_modeset()


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)