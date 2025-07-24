################################################################################################################################
# @file              audio_endpoint_mode_set.py
# @brief             Verify audio endpoint enumeration and audio register programs for each display mode set operation
# @details           Test scenario:
#                                 1. Boot the system with edp
#                                 2. Hotplug external panel and apply config
#                                 3. Verify endpoints after each modest
#                                 4. Sample command line: audio_endpoint_mode_set.py -edp_a -hdmi_b -config extended
# @author            Sridharan.V
################################################################################################################################

from Libs.Core.display_config.display_config_enums import Scaling
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Audio.EndpointVerification.audio_endpoint_base import *

##
# @class AudioEndpointModeSet
# @brief Verifies audio endpoint enumeration and audio register programs
class AudioEndpointModeSet(AudioEndpointBase):

    ##
    # @brief runtest
    # @return None
    def runTest(self):
        lfp_present = False

        # Set the test name for logging
        self.test_name = "Audio Mode Set Test"
        self.is_test_step = True

        logging.info("******* {0} Started *******".format(self.test_name))
        self.print_current_topology()

        # supported_modes[] is a list of modes supported by the display
        supported_modes = []
        # Pruned modes dict will contain only the MIN, MID & MAX resolutions for all the display
        supported_modes_dict = {}

        # target_list_modes[] is a list of target ids of all the displays used for applying modes
        target_list_modes = []

        # Verify that the audio endpoints are enumerated correctly
        self.verify_audio_endpoints()

        # get the current display config from DisplayConfig
        config = self.display_config.get_current_display_configuration()

        if self.topology in [enum.EXTENDED, enum.SINGLE]:
            for index in range(config.numberOfDisplays):
                target_list_modes.append(config.displayPathInfo[index].targetId)
        else:
            target_list_modes.append(config.displayPathInfo[0].targetId)

        # supported_modes[] is a list of modes supported by the display in sorted order
        supported_modes = self.display_config.get_all_supported_modes(target_list_modes, sorting_flag=True)

        if len(supported_modes) == 0:
            gdhm.report_driver_bug_audio(
                title="[Audio] Failed to retrieve supported modes for {0}".format(target_list_modes))
            self.fail("Failed to retrieve supported modes for {0}".format(target_list_modes))

        for key, values in supported_modes.items():
            test_modes_list = list()
            test_modes_list.append(values[0])
            test_modes_list.append(values[len(values) // 2])
            test_modes_list.append(values[-1])

            supported_modes_dict[key] = test_modes_list

        for target_id, supported_mode_list in supported_modes_dict.items():
            logging.debug("List of supported modes for Target id: {}".format(target_id))
            for display_mode in supported_mode_list:
                logging.debug('HRes:{} VRes:{} RR:{} BPP:{}, SamplingMode: {}, ScanlineOrdering: {}'.format(
                    display_mode.HzRes, display_mode.VtRes, display_mode.refreshRate, display_mode.BPP,
                    display_mode.samplingMode.Value, display_mode.scanlineOrdering
                ))

        for key, values in supported_modes_dict.items():

            for mode in values:

                # Apply mode one by one
                mode_str = ""
                for display_index in range(self.enumerated_displays.Count):
                    if mode.targetId == self.enumerated_displays.ConnectedDisplays[display_index].TargetID:
                        mode_str = (CONNECTOR_PORT_TYPE(
                            self.enumerated_displays.ConnectedDisplays[display_index].ConnectorNPortType)).name
                        mode_str += ": " + str(mode.HzRes) + "x" + str(mode.VtRes) + "@" + str(mode.refreshRate) + "Hz"
                        mode_str += " Scaling " + (Scaling(mode.scaling)).name

                logging.info("Step{0}: Set Mode= {1}".format(self.step_counter, mode_str))
                self.step_counter += 1

                set_display_mode_status = self.display_config.set_display_mode([mode])
                time.sleep(5)
                self.enumerated_displays = self.display_config.get_enumerated_display_info()
                for display_index in range(self.enumerated_displays.Count):
                    if mode.targetId == self.enumerated_displays.ConnectedDisplays[display_index].TargetID:
                        current_mode = self.display_config.get_current_mode(mode.targetId)
                        logging.info("\tPASS: Applied the mode ({1}x{2}@{3}Hz) on port {0} successfully".format(
                            (CONNECTOR_PORT_TYPE(
                                self.enumerated_displays.ConnectedDisplays[display_index].ConnectorNPortType)).name,
                            current_mode.HzRes,
                            current_mode.VtRes,
                            current_mode.refreshRate))


                # Verify vdsc if the status is True
                if self.vdsc_status is True:
                    self.verify_vdsc_audio()

                # Verify that the audio endpoints are enumerated correctly
                self.verify_audio_endpoints()


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
