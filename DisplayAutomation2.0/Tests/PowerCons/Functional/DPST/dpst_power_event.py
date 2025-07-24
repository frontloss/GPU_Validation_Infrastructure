########################################################################################################################
# @file         dpst_power_event.py
# @brief        Test for DPST/OPST power event (CS/S3/S4) scenario
#
# @author       Ashish Tripathi
########################################################################################################################
from Libs.Core.test_env import test_environment

from Tests.PowerCons.Functional.DPST.dpst_base import *


##
# @brief        This class contains test cases for DPST/OPST with power events
class DpstPowerEvent(DpstBase):
    ##
    # @brief        This function verifies DPST/OPST with S3 power event
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["S3"])
    # @endcond
    def t_11_dpst_s3(self):
        test_status = True
        if self.display_power_.is_power_state_supported(display_power.PowerEvent.S3) is False:
            self.fail("Test needs CS disabled system, but it is having CS enabled (Planning Issue)")

        etl_file = dpst.run_workload(dpst.WorkloadMethod.PSR_UTIL, polling_offsets=self.offsets)
        if etl_file is False:
            self.fail("Failed to run the workload")
        test_status &= self.validate_xpst(etl_file, dpst.WorkloadMethod.PSR_UTIL, workload.PowerSource.DC_MODE)

        invoke_power_event("S3")

        etl_file = dpst.run_workload(dpst.WorkloadMethod.PSR_UTIL, polling_offsets=self.offsets)
        if etl_file is False:
            self.fail("Failed to run the workload")
        test_status &= self.validate_xpst(etl_file, dpst.WorkloadMethod.PSR_UTIL, workload.PowerSource.DC_MODE)
        if test_status is False:
            self.fail("FAIL: DPST feature verification with S3")
        logging.info("PASS: DPST feature verification with S3")

    ##
    # @brief        This function verifies DPST/OPST with CS power event
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["CS"])
    # @endcond
    def t_12_dpst_cs(self):
        test_status = True
        if self.display_power_.is_power_state_supported(display_power.PowerEvent.S3) is True:
            self.fail("Test needs CS enabled system, but it is having CS disabled (Planning Issue)")

        etl_file = dpst.run_workload(dpst.WorkloadMethod.PSR_UTIL, polling_offsets=self.offsets)
        if etl_file is False:
            self.fail("Failed to run the workload")
        test_status &= self.validate_xpst(etl_file, dpst.WorkloadMethod.PSR_UTIL, workload.PowerSource.DC_MODE)

        invoke_power_event("CS")

        etl_file = dpst.run_workload(dpst.WorkloadMethod.PSR_UTIL, polling_offsets=self.offsets)
        if etl_file is False:
            self.fail("Failed to run the workload")
        test_status &= self.validate_xpst(etl_file, dpst.WorkloadMethod.PSR_UTIL, workload.PowerSource.DC_MODE)
        if test_status is False:
            self.fail("FAIL: DPST feature verification with CS")
        logging.info("PASS: DPST feature verification with CS")

    ##
    # @brief        This function verifies DPST/OPST with S4 power event
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["S4"])
    # @endcond
    def t_13_dpst_s4(self):
        test_status = True
        etl_file = dpst.run_workload(dpst.WorkloadMethod.PSR_UTIL, polling_offsets=self.offsets)
        if etl_file is False:
            self.fail("Failed to run the workload")
        test_status &= self.validate_xpst(etl_file, dpst.WorkloadMethod.PSR_UTIL, workload.PowerSource.DC_MODE)

        invoke_power_event("S4")

        etl_file = dpst.run_workload(dpst.WorkloadMethod.PSR_UTIL, polling_offsets=self.offsets)
        if etl_file is False:
            self.fail("Failed to run the workload")
        test_status &= self.validate_xpst(etl_file, dpst.WorkloadMethod.PSR_UTIL, workload.PowerSource.DC_MODE)
        if test_status is False:
            self.fail("FAIL: DPST feature verification with S4")
        logging.info("PASS: DPST feature verification with S4")


##
# @brief        This is a helper function to verify DPST/OPST with the provided power event
# @param[in]    event_type enum PowerEvent
# @return       None
def invoke_power_event(event_type):
    display_power_ = display_power.DisplayPower()
    power_event = display_power.PowerEvent[event_type]
    logging.info(f"\tInitiating power event {event_type}")
    if display_power_.invoke_power_event(power_event, common.POWER_EVENT_DURATION_DEFAULT) is False:
        assert False, f"FAILED to initiate and resume from {event_type} (Test Issue)"
    logging.info(f"\tSuccessfully resumed from {event_type}")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(DpstPowerEvent))
    test_environment.TestEnvironment.cleanup(test_result)
