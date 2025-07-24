########################################################################################################################
# @file         pfn_modes.py
# @brief        Basic test to verify periodic frame notification after applying different modes.
#               * Apply display configuration as mentioned in the command line.
#               * Apply different modes.
#               * Run WHCK tool.
#               * Verify periodic frame notification.
# @author       Ilamparithi Mahendran
########################################################################################################################
from Libs.Core.display_config.display_config_enums import DisplayConfigTopology
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Flips.PeriodicFrameNotification.pfn_base import *

##
# @brief    Contains function to check basic periodic frame notification test applying different modes
class PeriodicFrameNotificationBaseModes(PeriodicFrameNotificationBase):

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):
        target_id_list = []
        ##
        # fetch the display configuration of all the displays connected
        display_info = self.display_config.get_all_display_configuration()

        ##
        # target_id_list is a list of all the target_ids of the displays connected
        for displays in range(display_info.numberOfDisplays):
            target_id_list.append(display_info.displayPathInfo[displays].targetId)

        for config_list in self.display_config_list:
            if not self.display_config.set_display_configuration_ex(config_list[0], config_list[1]):
                self.fail("Display Configuration failed")

            supported_modes = self.display_config.get_all_supported_modes(target_id_list)
            for key, values in supported_modes.items():

                mode = values[len(values) - 1]
                ##
                # set all the highest mode
                self.display_config.set_display_mode([mode])
                logging.info(
                    "Applied the configuration as %s %s" % (DisplayConfigTopology(config_list[0]).name,
                                                            self.get_display_configuration(
                                                                config_list[1])))

                self.run_test_tool()

                if not self.verify_periodic_frame_notification():
                    logging.critical("Periodic Frame Notification Test Failed for mode %s %s" % (
                        DisplayConfigTopology(config_list[0]).name,
                        self.get_display_configuration(
                            config_list[1])))
                    self.report_to_gdhm_periodic_frame_notification_failure()
                    self.fail("Periodic Frame Notification Test Failed")

                logging.info("Periodic Frame Notification Test Passed for mode %s %s" % (
                    DisplayConfigTopology(config_list[0]).name,
                    self.get_display_configuration(
                        config_list[1])))

                mode = values[len(values) // 2]
                ##
                # set an intermediate mode
                self.display_config.set_display_mode([mode])
                logging.info(
                    "Applied the configuration as %s %s" % (DisplayConfigTopology(config_list[0]).name,
                                                            self.get_display_configuration(
                                                                config_list[1])))

                self.run_test_tool()

                if not self.verify_periodic_frame_notification():
                    logging.critical("Periodic Frame Notification Test Failed for mode %s %s" % (
                        DisplayConfigTopology(config_list[0]).name,
                        self.get_display_configuration(
                            config_list[1])))
                    self.report_to_gdhm_periodic_frame_notification_failure()
                    self.fail("Periodic Frame Notification Test Failed")

                logging.info("Periodic Frame Notification Test Passed for mode %s %s" % (
                    DisplayConfigTopology(config_list[0]).name,
                    self.get_display_configuration(
                        config_list[1])))

                mode = values[0]
                ##
                # set the lowest mode
                self.display_config.set_display_mode([mode])
                logging.info(
                    "Applied the configuration as %s %s" % (DisplayConfigTopology(config_list[0]).name,
                                                            self.get_display_configuration(
                                                                config_list[1])))

                self.run_test_tool()

                if not self.verify_periodic_frame_notification():
                    logging.critical("Periodic Frame Notification Test Failed for mode %s %s" % (
                        DisplayConfigTopology(config_list[0]).name,
                        self.get_display_configuration(
                            config_list[1])))
                    self.report_to_gdhm_periodic_frame_notification_failure()
                    self.fail("Periodic Frame Notification Test Failed")

                logging.info("Periodic Frame Notification Test Passed for mode %s %s" % (
                    DisplayConfigTopology(config_list[0]).name,
                    self.get_display_configuration(
                        config_list[1])))


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
