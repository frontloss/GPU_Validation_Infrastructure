########################################################################################################################
# @file         display_interop.py
# @brief        Function is to implement display Interop
# @details
#               CommandLine : Customise from display_interop.py APP
#               An occurrence of underrun leads to failure of test otherwise, test is considered to be passed.
# @author       Raghupathy, Dushyanth Kumar, Balaji Gurusamy
########################################################################################################################
from Libs.Core import reboot_helper
from Tests.Display_Interop.display_interop_base import *

from enum import Enum

# New level of logging for Test Sequence Flow
STEP = 25
logging.addLevelName(STEP, "STEP")

delay_between_events = 2


##
# @brief        List of Events available
class InteropEvents(Enum):
        TestVideoWithAudio = '1'
        TestAudioWithEndpoints = '2'
        TestModeSet = '3'
        TestCursor= '4'
        TestCS= '5'
        TestS3= '6'
        TestS4= '7'
        TestRotation= '8'
        TestHDCP= '9'
        TestHPD= '10'
        TestDriver= '11'


##
# @brief        Display Interop class : Inherited Display Interop Base test script
class DisplayInterop(DisplayInteropBase):
    config = ''
    displays = []
    display_ports = ''

    ##
    # @brief    refer doc string
    # @return   None
    def test_display_interop(self):

        # Check provided display ports are connected physically or not
        self.enumerated_displays = self.display_config.get_enumerated_display_info()
        logging.info("Enumerated Displays : {}".format(self.enumerated_displays.to_string()))

        for display in self.display_list:
            if display not in self.enumerated_displays.to_string():
                logging.error("Please Check Display Port : {} Physically Connected or NOT".format(display))
                self.fail("Issues with Physically Connected Displays")

        if self.topology == "NONE":
            # Apply Config from Sequence XML for Connected Display Ports
            self.set_config(topology="")
        else:
            for item in self.topology:
                if item == 'SD':
                    self.set_config(topology="SINGLE")
                elif item == 'ED':
                    self.set_config(topology="EXTENDED")
                elif item == 'CD':
                    self.set_config(topology="CLONE")

    ##
    # @brief        Sets Config based on Topology
    # @param[in]    topology
    # @return       None
    def set_config(self, topology):
        for sequence in self.sequence_list:
            self.config = list(dict(sequence))[0]
            flag = True
            for disp in str(list(dict(sequence).values())[0]).split(","):
                if len(self.display_list) < int(disp):
                    flag = False
            if flag:
                if topology in self.config:
                    self.seq_counter += 1
                    self.displays = self.map_seq_displays(list(dict(sequence).values())[0])
                    self.display_ports = self.map_seq_displays(list(dict(sequence).values())[0])

                    logging.info("******************** Setting {0} with Displays: {1} ********************".format(
                        self.config, self.displays))
                    logging.log(STEP, "Test Sequence: {0} : Applying Config {1} with Displays : {2}".format(
                        self.seq_counter, self.config, self.displays))
                    self.apply_config_and_verify(self.config, self.displays)
                    self.events_verification()

    ##
    # @brief        Events Verification Functions
    # @return       None
    def events_verification(self):
        for test_event_order in self.random_list:
            if test_event_order == InteropEvents.TestVideoWithAudio.value:
                time.sleep(delay_between_events)
                # Play Video clips and Verify MPO, DE Verification
                self.seq_counter += 1
                logging.log(STEP, "Test Sequence: {0} : Playing User Event MPO Video Clips".format(self.seq_counter))
                self.play_video_clip_and_verify_mpo(self.displays[0])

            elif test_event_order == InteropEvents.TestAudioWithEndpoints.value:
                time.sleep(delay_between_events)
                # Verify Audio Endpoints
                self.seq_counter += 1
                logging.log(STEP, "Test Sequence: {0} : Going to Verify Audio Endpoints".format(self.seq_counter))
                self.verify_audio_endpoints()

            elif test_event_order == InteropEvents.TestModeSet.value:
                time.sleep(delay_between_events)
                # Apply ModeSet and DE Verification
                self.seq_counter += 1
                target_id_list = []
                enumerated_displays = self.display_config.get_enumerated_display_info()
                for display_port in self.displays:
                    target_id = self.display_config.get_target_id(display_port, enumerated_displays)
                    target_id_list.append(target_id)
                logging.log(STEP,
                            "Test Sequence: {0} : Applying Mode Set for Enumerated Modes".format(self.seq_counter))
                self.apply_modes_and_verify(target_id_list, enumerated_displays)

            elif test_event_order == InteropEvents.TestCursor.value:
                time.sleep(delay_between_events)
                # Cursor Move
                self.seq_counter += 1
                logging.log(STEP, "Test Sequence: {0} : Performing Cursor Move Event".format(self.seq_counter))
                self.cursor_move()

            elif test_event_order == InteropEvents.TestCS.value:
                time.sleep(delay_between_events)
                # Trigger Power Events and DE Verification
                self.seq_counter += 1
                logging.log(STEP, "Test Sequence: {0} : Triggering Power Events".format(self.seq_counter))
                self.trigger_powerevents_and_verify('CS')

            elif test_event_order == InteropEvents.TestS3.value:
                time.sleep(delay_between_events)
                # Trigger Power Events and DE Verification
                self.seq_counter += 1
                logging.log(STEP, "Test Sequence: {0} : Triggering Power Events".format(self.seq_counter))
                self.trigger_powerevents_and_verify('S3')

            elif test_event_order == InteropEvents.TestS4.value:
                time.sleep(delay_between_events)
                # Trigger Power Events and DE Verification
                self.seq_counter += 1
                logging.log(STEP, "Test Sequence: {0} : Triggering Power Events".format(self.seq_counter))
                self.trigger_powerevents_and_verify('S4')

            elif test_event_order == InteropEvents.TestRotation.value:
                time.sleep(delay_between_events)
                # Window Rotation
                self.seq_counter += 1
                logging.log(STEP, "Test Sequence: {0} : Performing Window Rotation".format(self.seq_counter))
                self.window_rotation()

            elif test_event_order == InteropEvents.TestHDCP.value:
                time.sleep(delay_between_events)
                # Verify HDCP
                self.seq_counter += 1
                logging.log(STEP, "Test Sequence: {0} : Going to Verify HDCP".format(self.seq_counter))
                self.verify_hdcp()

            elif test_event_order == InteropEvents.TestHPD.value:
                time.sleep(delay_between_events)
                # Unplug and Plug HPD
                self.seq_counter += 1
                logging.log(STEP, "Test Sequence: {0} : Going to Unplug & Plug Displays, if SHE Tool Connected".format(
                    self.seq_counter))
                self.unplug_plug_HPD()

            elif test_event_order == InteropEvents.TestDriver.value:
                time.sleep(delay_between_events)
                # Disable and Enable Gfx Driver
                self.seq_counter += 1
                logging.log(STEP, "Test Sequence: {0} : Going to Disable & Enable GFX Driver".format(self.seq_counter))
                self.disable_enable_driver()


if __name__ == '__main__':
    TestEnvironment.initialize()
    results = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('DisplayInterop'))
    TestEnvironment.cleanup(results)
