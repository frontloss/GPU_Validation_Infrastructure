#################################################################################################################
# @file         drrs_power_events.py
# @addtogroup   PowerCons
# @section      DRRS_Tests
# @brief        Contains DRRS power events tests
#
# @author       Rohit Kumar
#################################################################################################################
from Libs.Core import display_power, enum
from Libs.Core.test_env import test_environment

from Tests.PowerCons.Functional.DRRS.drrs_base import *


##
# @brief        This class contains tests to verify DRRS before and after power events


class DrrsPowerEventsTest(DrrsBase):

    ##
    # @brief        This function verifies DRRS before and after power event S3
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["S3"])
    # @endcond
    def t_11_s3(self):
        if self.display_power_.is_power_state_supported(display_power.PowerEvent.S3) is False:
            gdhm.report_test_bug_os("[OsFeatures][DRRS] S3 test is scheduled on ConnectedStandby enabled system", gdhm.ProblemClassification.OTHER,gdhm.Priority.P3,
                gdhm.Exposure.E3)
            self.fail("DRRS S3 test scheduled on CS system")

        self.verify_drrs()

        if self.display_power_.invoke_power_event(display_power.PowerEvent.S3, common.POWER_EVENT_DURATION_DEFAULT) is False:
            self.fail('Failed to invoke power event S3')

        for gfx_index, adapter in dut.adapters.items():
            dut.refresh_panel_caps(adapter)

        self.verify_drrs()

    ##
    # @brief        This function verifies DRRS before and after power event CS
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["CS"])
    # @endcond
    def t_12_cs(self):
        if self.display_power_.is_power_state_supported(display_power.PowerEvent.CS) is False:
            gdhm.report_test_bug_os("[OsFeatures][DRRS] CS test is scheduled on ConnectedStandby disabled system",gdhm.ProblemClassification.OTHER,gdhm.Priority.P3,
                gdhm.Exposure.E3)
            self.fail("DRRS CS test scheduled on Non-CS system")

        self.verify_drrs()

        if self.display_power_.invoke_power_event(display_power.PowerEvent.CS, common.POWER_EVENT_DURATION_DEFAULT) is False:
            self.fail('Failed to invoke power event CS')

        for gfx_index, adapter in dut.adapters.items():
            dut.refresh_panel_caps(adapter)

        self.verify_drrs()

    ##
    # @brief        This function verifies DRRS before and after power event S4
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["S4"])
    # @endcond
    def t_13_s4(self):
        self.verify_drrs()

        if self.display_power_.invoke_power_event(display_power.PowerEvent.S4, common.POWER_EVENT_DURATION_DEFAULT) is False:
            self.fail('Failed to invoke power event S4')

        for gfx_index, adapter in dut.adapters.items():
            dut.refresh_panel_caps(adapter)

        self.verify_drrs()


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(DrrsPowerEventsTest))
    test_environment.TestEnvironment.cleanup(test_result)
