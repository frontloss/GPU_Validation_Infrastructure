#######################################################################################################################
# @file         dp_tiled_rotation.py
# @brief        This test applies rotations on tiled display.
# @details      This test applies rotation 0/90/180/270 to the tiled display.
# @author       Amanpreet Kaur Khurana, Ami Golwala
#######################################################################################################################

from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Display_Port.DP_Tiled.display_port_base import *


##
# @brief        This class contains a test function which implements the mentioned test scenario / test steps.
class DPTiledRotation(DisplayPortBase):
    tiled_edid_hz_res = None
    tiled_edid_vt_res = None

    ##
    # @brief        sets mode and perform rotation.
    # @return       None
    def set_mode_rotation(self):
        ##
        # flag to tell whether plugged display is tiled or not
        tiled_flag = False
        ##
        # tile_target_list[] is a list of tile target id
        tile_adapter_list = []
        ##
        # get the enumerated displays fro, SystemUtility
        enumerated_displays = self.display_config.get_enumerated_display_info()
        ##
        # get the current display config from DisplayConfig
        config = self.display_config.get_current_display_configuration()

        for index in range(config.numberOfDisplays):
            tile_info = self.display_port.get_tiled_display_information(config.displayPathInfo[index].displayAndAdapterInfo)
            ##
            # check for tiled status
            if tile_info.TiledStatus is True:
                tiled_flag = True
                tile_adapter_list.append(config.displayPathInfo[index].displayAndAdapterInfo)
                ##
                # supported_modes_tiled[] is a list of modes supported by the tiled display
                supported_modes = self.display_config.get_all_supported_modes(tile_adapter_list)
                ##
                # tile_modes_list[] is a list of modes supported by the tiled display
                if self.ma_flag:
                    tile_modes_list = supported_modes[(config.displayPathInfo[
                            index].DisplayAndAdapterInfo.adapterInfo.gfxIndex, config.displayPathInfo[index].targetId)]
                else:
                    tile_modes_list = supported_modes[config.displayPathInfo[index].targetId]
                ##
                # tile_maximum_resolution is the maximum resolution of the tiled display taken from the tile_modes_list[]
                tile_modes_list = sorted(tile_modes_list, key=attrgetter('HzRes', 'VtRes', 'refreshRate'))
                tile_maximum_resolution = tile_modes_list[len(tile_modes_list) - 1]
                ##
                # check whether the resolution from list of modes is equal to the resolution from the tiled edid
                tiled_edid_hz_res = tile_info.HzRes
                tiled_edid_vt_res = tile_info.VtRes
                if self.config == 'EXTENDED' or self.config == 'SINGLE':
                    if tile_maximum_resolution.HzRes == tiled_edid_hz_res and \
                            tile_maximum_resolution.VtRes == tiled_edid_vt_res:
                        for key, values in supported_modes.items():
                            values = sorted(values, key=attrgetter('HzRes', 'VtRes', 'refreshRate'))
                            for mode in values:
                                if mode.HzRes == tiled_edid_hz_res and mode.VtRes == tiled_edid_vt_res:
                                    ##
                                    # Apply mode with rotation = 90
                                    mode.rotation = enum.ROTATE_90
                                    self.log_mode_info(mode, enumerated_displays, rotation=True)
                                    modes_flag = self.display_config.set_display_mode([mode])
                                    if modes_flag is False:
                                        logging.error("[Driver Issue]: Failed to apply display mode. Exiting ...")
                                        # Gdhm bug reporting handled in display_config.set_display_mode
                                        self.fail()
                                    time.sleep(Delay_5_Secs)
                                    self.current_mode_info(mode, enumerated_displays, rotation=True)
                                    ##
                                    # Check for CRC amd Underrun
                                    self.verify_underrun_and_crc()
                                    ##
                                    # Apply mode with rotation = 180
                                    mode.rotation = enum.ROTATE_180
                                    self.log_mode_info(mode, enumerated_displays, rotation=True)
                                    modes_flag = self.display_config.set_display_mode([mode])
                                    if modes_flag is False:
                                        logging.error("[Driver Issue]: Failed to apply display mode. Exiting ...")
                                        # Gdhm bug reporting handled in display_config.set_display_mode
                                        self.fail()
                                    time.sleep(Delay_5_Secs)
                                    self.current_mode_info(mode, enumerated_displays, rotation=True)
                                    ##
                                    # Check for CRC amd Underrun
                                    self.verify_underrun_and_crc()
                                    ##
                                    # Apply mode with rotation = 270
                                    mode.rotation = enum.ROTATE_270
                                    self.log_mode_info(mode, enumerated_displays, rotation=True)
                                    modes_flag = self.display_config.set_display_mode([mode])
                                    if modes_flag is False:
                                        logging.error("[Driver Issue]: Failed to apply display mode. Exiting ...")
                                        # Gdhm bug reporting handled in display_config.set_display_mode
                                        self.fail()
                                    time.sleep(Delay_5_Secs)
                                    self.current_mode_info(mode, enumerated_displays, rotation=True)
                                    ##
                                    # Check for CRC amd Underrun
                                    self.verify_underrun_and_crc()
                                    ##
                                    # Apply mode with rotation = 0
                                    mode.rotation = enum.ROTATE_0
                                    self.log_mode_info(mode, enumerated_displays, rotation=True)
                                    modes_flag = self.display_config.set_display_mode([mode])
                                    if modes_flag is False:
                                        logging.error("[Driver Issue]: Failed to apply display mode. Exiting ...")
                                        # Gdhm bug reporting handled in display_config.set_display_mode
                                        self.fail()
                                    time.sleep(Delay_5_Secs)
                                    self.current_mode_info(mode, enumerated_displays, rotation=True)
                                    ##
                                    # Check for CRC amd Underrun
                                    self.verify_underrun_and_crc()
                    else:
                        logging.error(
                            "[Test Issue]: Modes enumerated by the Graphics  driver not matching with modes in EDID. Exiting .....")
                        gdhm.report_bug(
                            title="[Interfaces][DP_Tiled] Driver enumerated modes and edid modes are not matching",
                            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                            component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                            priority=gdhm.Priority.P2,
                            exposure=gdhm.Exposure.E2
                        )
                        self.fail()

                else:
                    for key, values in supported_modes.items():
                        values = sorted(values, key=attrgetter('HzRes', 'VtRes', 'refreshRate'))
                        for mode in values:
                            ##
                            # Apply mode with rotation = 90
                            mode.rotation = enum.ROTATE_90
                            self.log_mode_info(mode, enumerated_displays, rotation=True)
                            modes_flag = self.display_config.set_display_mode([mode])
                            if modes_flag is False:
                                logging.error("[Driver Issue]: Failed to apply display mode. Exiting ...")
                                # Gdhm bug reporting handled in display_config.set_display_mode
                                self.fail()
                            time.sleep(Delay_5_Secs)
                            self.current_mode_info(mode, enumerated_displays, rotation=True)
                            ##
                            # Check for CRC amd Underrun
                            self.verify_underrun_and_crc()
                            ##
                            # Apply mode with rotation = 180
                            mode.rotation = enum.ROTATE_180
                            self.log_mode_info(mode, enumerated_displays, rotation=True)
                            modes_flag = self.display_config.set_display_mode([mode])
                            if modes_flag is False:
                                logging.error("[Driver Issue]: Failed to apply display mode. Exiting ...")
                                # Gdhm bug reporting handled in display_config.set_display_mode
                                self.fail()
                            time.sleep(Delay_5_Secs)
                            self.current_mode_info(mode, enumerated_displays, rotation=True)
                            ##
                            # Check for CRC amd Underrun
                            self.verify_underrun_and_crc()
                            ##
                            # Apply mode with rotation = 270
                            mode.rotation = enum.ROTATE_270
                            self.log_mode_info(mode, enumerated_displays, rotation=True)
                            modes_flag = self.display_config.set_display_mode([mode])
                            if modes_flag is False:
                                logging.error("[Driver Issue]: Failed to apply display mode. Exiting ...")
                                # Gdhm bug reporting handled in display_config.set_display_mode
                                self.fail()
                            time.sleep(Delay_5_Secs)
                            self.current_mode_info(mode, enumerated_displays, rotation=True)
                            ##
                            # Check for CRC amd Underrun
                            self.verify_underrun_and_crc()
                            ##
                            # Apply mode with rotation = 0
                            mode.rotation = enum.ROTATE_0
                            self.log_mode_info(mode, enumerated_displays, rotation=True)
                            modes_flag = self.display_config.set_display_mode([mode])
                            if modes_flag is False:
                                logging.error("[Driver Issue]: Failed to apply display mode. Exiting ...")
                                # Gdhm bug reporting handled in display_config.set_display_mode
                                self.fail()
                            time.sleep(Delay_5_Secs)
                            self.current_mode_info(mode, enumerated_displays, rotation=True)
                            ##
                            # Check for CRC amd Underrun
                            self.verify_underrun_and_crc()
        ##
        # check for tiled_flag
        if tiled_flag is False:
            logging.error("[Test Issue]: Display doesn't support Tiled modes. Exiting .....")
            gdhm.report_bug(
                title="[Interfaces][DP_Tiled] DP Tiled tests are running on non-tiled displays",
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            self.fail()

    ##
    # @brief        This test plugs required displays, set config and perform test.
    # @return       None
    def runTest(self):
        ##
        # plug tiled display
        self.tiled_display_helper(action="PLUG")
        ##
        # get plugged target ids
        plugged_target_ids = self.display_target_ids()
        logging.info("Target ids :%s" % plugged_target_ids)
        ##
        # set config from the command line with only one combination of displays
        self.set_config(self.config, no_of_combinations=1)
        ##
        # set tiled mode with various rotations i.e. 0/90/180/270
        self.set_mode_rotation()


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
