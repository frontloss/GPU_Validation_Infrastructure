########################################################################################################################
# @file         collage_persistence_power_event.py
# @brief        Test to verify collage persistence across different power events like S3, S4, S5 etc
# @details      Test Scenario:
#                   1. Apply Collage(say HC) and check if all displays are in collage mode and verify collage max mode.
#                   2. Invoke the power event based on the command line using -selective custom tag
#                       Supported Options - [CS, S3, S4, S5, MONITOR_ON_OFF]
#                   3. Resume from the power event check if collage display persists and verify if the same displays
#                      are in collage mode and verify collage max mode.
#
# @author       Krishnan, Praburaj
########################################################################################################################

import logging
import typing
import unittest

from Libs.Core import display_power, enum
from Libs.Core.logger import gdhm
from Libs.Core.wrapper.driver_escape_args import CollageType
from Libs.Core.test_env.test_environment import TestEnvironment

from Tests.Collage.yangra.collage_enum_constants import Action
from Tests.Collage.yangra.collage_yangra_base import CollageYangraBase
from Tests.PowerCons.Modules import common


##
# @brief        This class contains multiple tests to verify collage persistence in each of the power events
class CollagePersistence(CollageYangraBase):

    ##
    # @brief        This test verifies if collage state is retained after resuming back from CS
    # @return       None
    # @cond
    @common.configure_test(selective=['CS'])
    # @endcond
    def t_1_power_event_cs(self) -> None:
        logging.info(" TEST - Collage Persistence in CS begins here ".center(common.MAX_LINE_WIDTH, "*"))

        # Hot plug the displays based on the command line
        CollageYangraBase.hot_swap_display(self, action=Action.HOT_PLUG_ALL)

        for collage_type in [CollageType.HORIZONTAL, CollageType.VERTICAL]:
            display_info_list = CollageYangraBase.get_display_info_list_to_be_in_collage()
            self.assertTrue(display_info_list, 'DisplayInfo not found.')
            # Gdhm bug reporting handled in get_display_info_list_to_be_in_collage

            self.set_and_verify_collage_topology(collage_type, display_info_list)
            self.verify_persistence_in_low_power(display_power.PowerEvent.CS, "CS")

        logging.info(" TEST - Collage Persistence in CS ENDS HERE ".center(common.MAX_LINE_WIDTH, "*"))

    ##
    # @brief        This test verifies if collage state is retained after resuming back from S3
    # @return       None
    # @cond
    @common.configure_test(selective=['S3'])
    # @endcond
    def t_2_power_event_s3(self) -> None:
        logging.info(" TEST - Collage Persistence in S3 begins here ".center(common.MAX_LINE_WIDTH, "*"))

        # Hot plug the displays based on the command line
        CollageYangraBase.hot_swap_display(self, action=Action.HOT_PLUG_ALL)

        for collage_type in [CollageType.HORIZONTAL, CollageType.VERTICAL]:
            display_info_list = CollageYangraBase.get_display_info_list_to_be_in_collage()
            self.assertTrue(display_info_list, 'DisplayInfo not found.')
            # Gdhm bug reporting handled in get_display_info_list_to_be_in_collage

            self.set_and_verify_collage_topology(collage_type, display_info_list)
            self.verify_persistence_in_low_power(display_power.PowerEvent.S3, "S3")

        logging.info(" TEST - Collage Persistence in S3 ENDS HERE ".center(common.MAX_LINE_WIDTH, "*"))

    ##
    # @brief        This test verifies if collage state is retained after resuming back from S4
    # @return       None
    # @cond
    @common.configure_test(selective=['S4'])
    # @endcond
    def t_3_power_event_s4(self) -> None:
        logging.info(" TEST - Collage Persistence in S4 begins here ".center(common.MAX_LINE_WIDTH, "*"))

        # Hot plug the displays based on the command line
        CollageYangraBase.hot_swap_display(self, action=Action.HOT_PLUG_ALL)

        for collage_type in [CollageType.HORIZONTAL, CollageType.VERTICAL]:
            display_info_list = CollageYangraBase.get_display_info_list_to_be_in_collage()
            self.assertTrue(display_info_list, 'DisplayInfo not found.')
            # Gdhm bug reporting handled in get_display_info_list_to_be_in_collage

            self.set_and_verify_collage_topology(collage_type, display_info_list)
            self.verify_persistence_in_low_power(display_power.PowerEvent.S4,"S4")

        logging.info(" TEST - Collage Persistence in S4 ENDS HERE ".center(common.MAX_LINE_WIDTH, "*"))

    ##
    # @brief        This test verifies if collage state is retained after resuming back from Monitor Turn Off
    # @return       None
    # @cond
    @common.configure_test(selective=['MONITOR_ON_OFF'])
    # @endcond
    def t_4_power_event_monitor_on_off(self) -> None:
        logging.info(" TEST - Collage Persistence in MTO begins here ".center(common.MAX_LINE_WIDTH, "*"))

        # Hot plug the displays based on the command line
        CollageYangraBase.hot_swap_display(self, action=Action.HOT_PLUG_ALL)

        for collage_type in [CollageType.HORIZONTAL, CollageType.VERTICAL]:
            display_info_list = CollageYangraBase.get_display_info_list_to_be_in_collage()
            self.assertTrue(display_info_list, 'DisplayInfo not found.')
            # Gdhm bug reporting handled in get_display_info_list_to_be_in_collage

            self.set_and_verify_collage_topology(collage_type, display_info_list)

            self.verify_persistence_in_low_power(display_power.MonitorPower.OFF_ON,"OFF_ON")

        logging.info(" TEST - Collage Persistence in MTO ENDS HERE ".center(common.MAX_LINE_WIDTH, "*"))

    ##
    # @brief        Helps to invoke the power event based on the power state requested and verifies the collage
    #               persistence
    # @param[in]    power_state: IntEnum
    #                   Power State to be invoked
    # @param[in]    power_state_name: str
    #                   Name of the power state in string
    # @return       None
    def verify_persistence_in_low_power(self, power_state: typing.Union[display_power.PowerEvent, display_power.MonitorPower], power_state_name: str):

        if power_state.name == display_power.MonitorPower.OFF_ON.name:
            is_success = self.display_power.invoke_monitor_turnoff(power_state, common.POWER_EVENT_DURATION_DEFAULT)
        else:
            is_success = self.display_power.invoke_power_event(power_state, common.POWER_EVENT_DURATION_DEFAULT)

        if is_success is False:
            gdhm.report_bug(
                title="[Interfaces][Display_Collage] Failed To Invoke Power Event: {}".format(power_state_name),
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
        self.assertEquals(is_success, True, 'Failed To Invoke Power Event: {} [Driver issue]'.format(power_state_name))

        collage_display_info_list = CollageYangraBase.get_collage_display_info_list()
        if len(collage_display_info_list) == 0:
            gdhm.report_bug(
                title="[Interfaces][Display_Collage] Collage Display info not found ",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
        self.assertTrue(collage_display_info_list, 'Collage DisplayInfo not found after plugging back.')

        # Check if collage is enabled after hot plug in low power state.
        is_collage_enabled = CollageYangraBase.is_collage_display_enumerated(collage_display_info_list[0])
        if is_collage_enabled is True:
            logging.info('Collage Config persisted after power event: {}'.format(power_state_name))
            self.verify_displays_in_collage()
        else:
            gdhm.report_bug(
                title="[Interfaces][Display_Collage] Collage Config does not persist after power event: {}".format(
                    power_state_name),
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )

            self.fail('[Driver Issue] - Collage Config does not persist after power event: {}'.format(power_state_name))

        collage_display_info_list = CollageYangraBase.get_collage_display_info_list()
        if len(collage_display_info_list) == 0:
            gdhm.report_bug(
                title="[Interfaces][Display_Collage] Collage Display info not found ",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
        self.assertTrue(collage_display_info_list, 'Collage DisplayInfo not found. [Driver Issue]')

        self.disable_collage_and_verify(collage_display_info_list[0])


if __name__ == '__main__':
    TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(CollagePersistence))
    TestEnvironment.cleanup(test_result)
