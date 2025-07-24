######################################################################################
# @file     optical_sensor_modeset.py
# @brief    Optical Sensor Modeset
# @remarks
# @ref      Base_class: optical_sensor_base.py
#           Validate modeset event using optical sensor
# @author   ashishk2
##########################################################################################################

import logging
import sys
import time

import Tests.OpticalSensor.optical_sensor_base as opt_sensor
from Libs.Core.logger import gdhm
from Libs.Core.test_env import test_environment


##
# @brief        OpticalSensorModeSet
class OpticalSensorModeSet(opt_sensor.OpticalSensorBase):
    ##
    # @brief        Test Optical Sensor EDP Modeset
    # @return       None
    def test_optical_sensor_edp_modeset(self):

        result = None
        opt_obj = opt_sensor.OpticalSensorBase()

        # Thread is created to capture sensor data, so that ModeSet and data capturing can be done in parallel
        thread = opt_sensor.ThreadWithReturnValue(target=opt_obj.capture_sensor_data_thread,
                                                  args=(self.analog_input_index, self.sample_rate,
                                                        self.duration_in_seconds, result))
        thread.start()
        # Here mode set event is triggered
        mode = None
        current_config, display_list, display_and_adapter_info_list = \
            self.display_config_.get_current_display_configuration_ex()

        logging.info("Current Config: {}".format(current_config))

        mode_list = []
        target_list = []
        for display_index in range(len(self.input_display_list)):
            target = display_and_adapter_info_list[display_index].TargetID
            logging.info("Target: {}".format(target))

            mode = self.display_config_.get_current_mode(target)
            logging.info("Current Mode ({}x{}@{}Hz)".format(mode.HzRes, mode.VtRes, mode.refreshRate))
            target_list.append(target)
            supported_mode_dict = self.display_config_.get_all_supported_modes(target_list)
            for key, value in supported_mode_dict.items():
                if key == target:
                    for supported_mode in value:
                        if mode.refreshRate != supported_mode.refreshRate:
                            mode_list.append(supported_mode)
                            time.sleep(3)
                            logging.info("Applying ModeSet ({}x{}@{}Hz)".format(supported_mode.HzRes,
                                                                                supported_mode.VtRes,
                                                                                supported_mode.refreshRate))
                            self.display_config_.set_display_mode(mode_list)
                            break
            mode = self.display_config_.get_current_mode(target)
        if mode is None:
            logging.warning("Could not find the mode of the edp panel")
        result = thread.join()
        logging.info("Test Finished: Both the threads executed")
        if not result:
            gdhm.report_bug(
                title="[OpticalSensor] More than 1 blankout is seen in Optical Sensor Validation",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            self.fail("")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    outcome = opt_sensor.unittest.main(exit=False, argv=[sys.argv[0]])
    test_environment.TestEnvironment.cleanup(outcome.result)
