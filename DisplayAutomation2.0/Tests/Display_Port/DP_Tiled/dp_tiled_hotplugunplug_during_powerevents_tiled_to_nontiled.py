#######################################################################################################################
# @file         dp_tiled_hotplugunplug_during_powerevents_tiled_to_nontiled.py
# @brief        This test verifies hot plug with power events
# @details      This test checks whether Hotplug works on all ports B /C /D /F before and after CS/S3 and S4.
#
# @author       Amanpreet Kaur Khurana, Ami Golwala
#######################################################################################################################


import os

from Libs.Core import display_power
from Libs.Core.test_env import test_context
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Display_Port.DP_Tiled.display_port_base import *


##
# @brief        This class contains a test function which implements the mentioned test scenario / test steps.
class DPTiledtoNonTiledHotplugUnplugDuringPM(DisplayPortBase):

    ##
    # @brief        plug/unplug tiled display,set_config, apply & verify mode etc.
    # @param[in]    power_event: str
    #                    power_event for RVP i.e. S3, S4, CS
    # @return       None
    def performTest(self, power_event):
        if power_event == display_power.PowerEvent.MonitorPowerOffOn:
            ##
            # plug tiled display
            self.tiled_display_helper(action="PLUG")
            ##
            # get the target ids of the plugged displays
            plugged_target_ids = self.display_target_ids()
            logging.info("Target ids :%s" % plugged_target_ids)
            ##
            # set display configuration with topology as SINGLE for Single Adapter case else EXTENDED
            if not self.ma_flag:
                self.set_config('SINGLE', no_of_combinations=1)
            else:
                self.set_config('EXTENDED', no_of_combinations=1)
            ##
            # Apply 5K3K/8k4k resolution and check for applied mode
            self.apply_tiled_max_modes()
            ##
            # Verify 5K3K/8k4k mode
            self.verify_tiled_mode()
            ##
            # UnPlugging slave port of Tiled Display to the system
            self.plug_master_or_unplug_slave(action="SLAVE_PORT_UNPLUG")
            ##
            # apply and verify whether non tiled 4k mode is applied or not
            self.apply_and_verify_non_tiled_max_mode()
            ##
            # Plugging master port of Tiled Display to the system
            self.tiled_display_helper(action="UNPLUG", low_power=True)
            ##
            # Get the waiting time for MonitorTurnOff from SB_DP_SST_MonitorTurnOff_WaitingTime.txt file
            file_name = 'DP_MonitorTurnOff_WaitingTime.txt'
            file_path = os.path.join(test_context.TestContext.root_folder(), 'Tests\\Display_Port\\' + file_name)
            if os.path.exists(file_path):
                file = open(file_path, 'r')
            else:
                logging.error("[Test Issue]: %s file does not exist. Exiting ...." % file_path)
                gdhm.report_bug(
                    title="[Interfaces][DP_Tiled] Failed to find file path:{} ".format(file_path),
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Test.DISPLAY_INTERFACES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                self.fail()
            ##
            # Read the waiting time for MonitorTurnOff
            waiting_time = int(file.read())
            file.close()
            ##
            # Invoke MonitorTurnOff
            return_val_monitor_off_on = self.display_power.invoke_monitor_turnoff(power_event,
                                                                                  waiting_time)
            if return_val_monitor_off_on is False:
                self.fail("[Test Issue]: System failed to enter into %s state. Exiting ...." %
                              power_event.name)
            time.sleep(Delay_After_Power_Event)
            ##
            # Plugging DP Display to the system after resuming from sleep
            self.tiled_display_helper(action="PLUG")
            time.sleep(Delay_5_Secs)
            ##
            # get the target ids of the plugged displays
            plugged_target_ids = self.display_target_ids()
            logging.info("Target ids :%s" % plugged_target_ids)
            time.sleep(Delay_5_Secs)
            ##
            # Apply 5K3K/8k4k resolution and check for applied resolution
            self.apply_tiled_max_modes()
            ##
            # Verify 5K3K/8k4k mode
            self.verify_tiled_mode()
        else:
            ##
            # plug tiled display
            self.tiled_display_helper(action="PLUG")
            ##
            # get the target ids of the plugged displays
            plugged_target_ids = self.display_target_ids()
            logging.info("Target ids :%s" % plugged_target_ids)
            ##
            # set display configuration with topology as SINGLE for Single Adapter case else EXTENDED
            if not self.ma_flag:
                self.set_config('SINGLE', no_of_combinations=1)
            else:
                self.set_config('EXTENDED', no_of_combinations=1)
            ##
            # Apply 5K3K/8k4k resolution and check for applied mode
            self.apply_tiled_max_modes()
            ##
            # Verify 5K3K/8k4k mode
            self.verify_tiled_mode()
            ##
            # UnPlugging slave port of Tiled Display to the system
            self.plug_master_or_unplug_slave(action="SLAVE_PORT_UNPLUG")
            ##
            # apply and verify whether non tiled 4k mode is applied or not
            self.apply_and_verify_non_tiled_max_mode()
            ##
            # Plugging master port of Tiled Display to the system
            self.tiled_display_helper(action="UNPLUG", low_power=True)
            time.sleep(Delay_5_Secs)
            ##
            # set power event to S3/S4
            self.power_event(power_event, Resume_Time)
            time.sleep(Delay_After_Power_Event)
            ##
            # Plugging DP Display to the system after resuming from sleep
            self.tiled_display_helper(action="PLUG")
            ##
            # get the target ids of the plugged displays
            plugged_target_ids = self.display_target_ids()
            logging.info("Target ids :%s" % plugged_target_ids)
            time.sleep(Delay_5_Secs)
            ##
            # Apply 5K3K/8k4k resolution and check for applied resolution
            self.apply_tiled_max_modes()
            ##
            # Verify 5K3K/8k4k mode
            self.verify_tiled_mode()

    ##
    # @brief        This test executes the actual test steps.
    # @return       None
    def runTest(self):
        logging.info("Performing Power event CS/S3")
        power_state = display_power.PowerEvent.CS if self.display_power.is_power_state_supported(display_power.PowerEvent.CS) else display_power.PowerEvent.S3
        self.performTest(power_state)
        '''
        ##
        # TODO: Currently, whenever S4(Hibernate) is invoked the GTA machine gets unresponsive.
        # Hence, commenting test steps related to S4(Hibernate).
        logging.info("Performing Power event S4")
        self.performTest(enum.POWER_STATE_S4)
        '''
        # Monitor turnoff does not work in connected standby enabled system
        if self.display_power.is_power_state_supported(display_power.PowerEvent.S3):
            logging.info("Performing Monitor TurnOff")
            self.performTest(display_power.PowerEvent.MonitorPowerOffOn)


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
