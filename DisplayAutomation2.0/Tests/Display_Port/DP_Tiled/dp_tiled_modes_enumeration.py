#######################################################################################################################
# @file         dp_tiled_modes_enumeration.py
# @brief        This test applies modeset on tiled displays.
# @details      Verifies CUI/OS page should enumerate 5k/8K mode in SD and multi (Extended) mode
#               with 8K as one panel and other displays as non 8K panel.
# @author       Amanpreet Kaur Khurana, Ami Golwala, Veena Veluru
#######################################################################################################################

from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Display_Port.DP_Tiled.display_port_base import *


##
# @brief        This class contains a test function which implements the mentioned test scenario / test steps.
class DPTiledModesEnumeration(DisplayPortBase):

    ##
    # @brief        checks for enumerated modes by driver and then apply tiled modes with various RRs.
    # @return       None
    def performTest(self):
        refresh_rate_flag1 = None
        refresh_rate_flag2 = None
        ##
        # flag to tell whether plugged display is tiled or not
        tiled_flag = False
        ##
        # get the current display config from DisplayConfig
        config = self.display_config.get_current_display_configuration()

        for index in range(config.numberOfDisplays):
            tile_info = self.display_port.get_tiled_display_information(config.displayPathInfo[index].displayAndAdapterInfo)
            ##
            # check for tiled status
            if tile_info.TiledStatus is True:
                tiled_flag = True
                tile_target_list = [config.displayPathInfo[index].displayAndAdapterInfo]
                ##
                # supported_modes_tiled[] is a list of modes supported by the tiled display
                supported_modes_tiled = self.display_config.get_all_supported_modes(tile_target_list)
                ##
                # tile_modes_list[] is a list of modes supported by the tiled display
                if self.ma_flag:
                    tile_modes_list = supported_modes_tiled[(config.displayPathInfo[index].displayAndAdapterInfo.adapterInfo.gfxIndex, config.displayPathInfo[index].targetId)]
                else:
                    tile_modes_list = supported_modes_tiled[config.displayPathInfo[index].targetId]
                ##
                # tile_maximum_resolution is the maximum resolution of the tiled display taken form the tile_modes_list[]
                tile_modes_list = sorted(tile_modes_list, key=attrgetter('HzRes', 'VtRes', 'refreshRate'))
                tile_maximum_resolution = tile_modes_list[len(tile_modes_list) - 1]
                ##
                # check whether the resolution from list of modes is equal to the resolution from the tiled edid
                tiled_edid_hz_res = tile_info.HzRes
                tiled_edid_vt_res = tile_info.VtRes
                if (tiled_edid_hz_res == tile_maximum_resolution.HzRes) and (
                        tiled_edid_vt_res == tile_maximum_resolution.VtRes):
                    for key, values in supported_modes_tiled.items():
                        values = sorted(values, key=attrgetter('HzRes', 'VtRes', 'refreshRate'))
                        for mode in values:
                            ##
                            # set all modes with HzRes = 5k/8k and VtRes = 3k/4k with various refresh rates
                            if mode.HzRes == tiled_edid_hz_res and mode.VtRes == tiled_edid_vt_res and mode.refreshRate == 59:
                                refresh_rate_flag1 = True
                                logging.info("59Hz Refresh Rate is enumerated by the graphics driver")
                            if mode.HzRes == tiled_edid_hz_res and mode.VtRes == tiled_edid_vt_res and mode.refreshRate == 60:
                                refresh_rate_flag2 = True
                                logging.info("60Hz Refresh Rate is enumerated by the graphics driver")
                else:
                    logging.error(
                        "[Driver Issue]: Modes enumerated by the Graphics driver not matching with modes in EDID. Exiting .....")
                    gdhm.report_bug(
                        title="[Interfaces][DP_Tiled] Driver enumerated modes and edid modes are not matching",
                        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                        component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )
                    self.fail()
                ##
                # If the driver has enumerated 5k3k/8k4k with 59Hz and 60Hz Refresh Rates then apply all modes with 5k3k/8k4k @ different RRs
                if refresh_rate_flag1 is True and refresh_rate_flag2 is True:
                    ##
                    # Call apply_tiled_max_modes() from display_port_base.py
                    self.apply_tiled_max_modes()
                else:
                    if refresh_rate_flag1 is False:
                        logging.error(
                            "[Driver Issue]: 59Hz refresh rate didn't get enumerated by the graphics driver. Exiting .....")
                        gdhm.report_bug(
                            title="[Interfaces][DP_Tiled] Driver is not enumerating display mode at refresh rate 59Hz",
                            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                            component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                            priority=gdhm.Priority.P2,
                            exposure=gdhm.Exposure.E2
                        )
                        self.fail()
                    if refresh_rate_flag2 is False:
                        logging.error(
                            "[Driver Issue]: 60Hz refresh rate didn't get enumerated by the graphics driver. Exiting .....")
                        gdhm.report_bug(
                            title="[Interfaces][DP_Tiled]Driver is not enumerating display mode at refresh rate 60Hz",
                            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                            component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                            priority=gdhm.Priority.P2,
                            exposure=gdhm.Exposure.E2
                        )
                        self.fail()
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
    # @brief        This test plugs required displays, set config and perform actual test.
    # @return       None
    def runTest(self):
        ##
        # plug tiled display
        self.tiled_display_helper(action="PLUG")
        ##
        # get the target ids of the plugged displays
        plugged_target_ids = self.display_target_ids()
        logging.info("Target ids :%s" % plugged_target_ids)
        ##
        # set display configuration with topology as given in cmd line
        self.set_config(self.config, no_of_combinations=1)
        ##
        # check for driver enumerated RRs(59Hz/60Hz) and then apply all modes with 5k3k/8k4k @ different RRs
        self.performTest()


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
