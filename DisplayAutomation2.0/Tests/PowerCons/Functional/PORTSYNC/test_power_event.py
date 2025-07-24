#######################################################################################################################
# @file         test_power_event.py
# @addtogroup   Powercons
# @section      PORTSYNC
# @brief        Test for port sync with CS/S3/S4 power events,
#
# @author       Bhargav Adigarla
#######################################################################################################################
from Libs.Core.test_env import test_environment
from Libs.Core import app_controls
from Tests.PowerCons.Modules import workload
from Tests.PowerCons.Functional.PORTSYNC.port_sync_base import *


##
# @brief        This class contains basic port sync tests with power events
class TestPowerEvent(PortSyncBase):
    ##
    # @brief        this function verifies port sync in CS, S4
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["CS", "S4"])
    # @endcond
    def t_10_power_cs_s4(self):
        if self.display_power_.is_power_state_supported(display_power.PowerEvent.CS) is False:
            self.fail("CS is NOT supported on the system(Planning Issue)")
        self.validate_feature(display_power.PowerEvent.CS)
        self.validate_feature(display_power.PowerEvent.S4)

    ##
    # @brief        this function verifies port sync in S3, S4
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["S3", "S4"])
    # @endcond
    def t_11_power_s3_s4(self):
        if self.display_power_.is_power_state_supported(display_power.PowerEvent.S3) is False:
            self.fail("S3 is NOT supported on the system(Planning Issue)")
        self.validate_feature(display_power.PowerEvent.S3)
        self.validate_feature(display_power.PowerEvent.S4)

    ##
    # @brief        this function verifies port sync in power events
    # @param[in]    power_event: CS/S3/S4
    # @return       None
    def validate_feature(self, power_event):
        if self.display_power_.invoke_power_event(power_event, common.POWER_EVENT_DURATION_DEFAULT) is False:
            self.fail('Failed to invoke power event {0}'.format(power_event.name))

        for adapter in dut.adapters.values():
            if cmtg.verify_cmtg_status(adapter) is True:
                panels = list(adapter.panels.values())
                panel1_slave_status = cmtg.verify_cmtg_slave_status(adapter, panels[0])
                panel2_slave_status = cmtg.verify_cmtg_slave_status(adapter, panels[1])
                if panel1_slave_status == 1 and panel2_slave_status == 1:
                    self.fail(f"\tCMTG slave status enabled after power event "
                              f"panel1 {panel1_slave_status} panel2 {panel2_slave_status}")
            else:
                self.fail("\tCMTG status disabled")

            logging.info("PortSync verification successful")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.runner.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(TestPowerEvent))
    test_environment.TestEnvironment.cleanup(test_result)