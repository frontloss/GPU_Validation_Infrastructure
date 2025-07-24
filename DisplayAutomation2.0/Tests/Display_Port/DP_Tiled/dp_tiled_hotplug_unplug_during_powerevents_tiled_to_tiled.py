#######################################################################################################################
# @file         dp_tiled_hotplug_unplug_during_powerevents_tiled_to_tiled.py
# @brief        This test verifies hot plug/unplug with power events
# @details      This test checks whether Hotplug/unplug works on all ports during CS/S3 and S4.
#
# @author       Amanpreet Kaur Khurana, Ami Golwala, Veena Veluru, Supriya Krishnamurthi
#######################################################################################################################

from Libs.Core import display_power, enum
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Display_Port.DP_Tiled.display_port_base import *
from Tests.PowerCons.Modules import common


##
# @brief        This class contains a test function which implements the mentioned test scenario / test steps.
class DPTiledHotplugUnplugDuringPowerEventsTiledToTiled(DisplayPortBase):

    ##
    # @brief        plugs/unplugs displays during power event.
    # @param[in]    power_state: str
    #                    power_state for RVP i.e. S3, S4 etc
    # @return       None
    def performTest(self, power_state):

        logging.info(f'Performing hot plug of Tiled display during {power_state.name}')

        # plug tiled display
        self.tiled_display_helper(action="PLUG", low_power=True)

        # set power event S3/S4
        self.power_event(power_state, common.POWER_EVENT_DURATION_DEFAULT)

        # get the target ids
        plug_target_ids = self.display_target_ids()
        logging.info(f'Target Ids after hot-plug of tiled display during {power_state.name}: {plug_target_ids}')

        # Verify if the display plugged on each adapter is tiled or not.The first DP display mentioned in cmd line will
        # be the port type for Master Tile Display which will have the Master EDID and the DPCD passed along with it
        for i in range(len(self.ma_dp_panels)):
            gfx_index = self.ma_dp_panels[i][0]['gfx_index']
            port = self.ma_dp_panels[i][0]['connector_port']

            if self.is_tiled_target(gfx_index, port):
                logging.info(f"The display plugged at {port} on {gfx_index} is Tiled Display")
            else:
                logging.error(f"The display plugged at {port} on {gfx_index} is not detected as Tiled Panel")
                gdhm.report_bug(
                    title="[Interfaces][DP_Tiled] The display plugged at {} on {} is not detected as Tiled "
                          "Panel".format(self.ma_dp_panels[i][0]['connector_port'], gfx_index),
                    problem_classification=gdhm.ProblemClassification.OTHER,
                    component=gdhm.Component.Test.DISPLAY_INTERFACES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                self.fail()

        logging.info(f'Performing hot unplug of Tiled display during {power_state.name}')

        # unplug tiled display
        self.tiled_display_helper(action="UNPLUG", low_power=True)

        # set power event S3/S4
        self.power_event(power_state, common.POWER_EVENT_DURATION_DEFAULT)

        # get the target ids
        plug_target_ids = self.display_target_ids()
        logging.info(f'Target Ids after hot-unplug of tiled display during {power_state.name}: {plug_target_ids}')

    ##
    # @brief        This test executes the actual test steps.
    # @return       None
    def runTest(self):

        for event in self.power_events:
            if event.upper() == 'CS':
                is_cs_supported = self.display_power.is_power_state_supported(display_power.PowerEvent.CS)
                self.assertTrue(is_cs_supported, "[Planning Issue] - CS is not supported in the current setup")
                logging.info("Performing Power event CS")
                self.performTest(display_power.PowerEvent.CS)
            elif event.upper() == 'S3':
                is_s3_supported = self.display_power.is_power_state_supported(display_power.PowerEvent.S3)
                self.assertTrue(is_s3_supported, "[Planning Issue] - S3 is not supported in the current setup")
                logging.info("Performing Power event S3")
                self.performTest(display_power.PowerEvent.S3)
            elif event.upper() == 'S4':
                logging.info("Performing Power event S4")
                self.performTest(display_power.PowerEvent.S4)


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
