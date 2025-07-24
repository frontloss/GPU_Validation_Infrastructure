########################################################################################################################
# @file         vdd_status_cs_s3.py
# @addtogroup   EDP
# @section      VDD
# @brief        Test to verify Vdd ststus with CS/S3 power event for eDP
# @details      @ref vdd_status_cs_s3.py <br>
#               This test also checks Vdd status for power event CS/S3.
#
# @author       Kruti Vadhavaniya
########################################################################################################################

from Tests.EDP.VDD.vdd_base import *


##
# @brief        This class contains test to verify Vdd status for CS/S3 power event
class VddStatusCheck(VDDBase):
    ############################
    # Test Function
    ############################

    ##
    # @brief        This test verifies VDD status with S3 power event
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["S3"])
    # @endcond
    def t_11_s3(self):
        if self.display_power_.is_power_state_supported(display_power.PowerEvent.S3) is False:
            self.fail("FAIL: S3 is NOT enabled in the system")

        if etl_tracer.start_etl_tracer() is False:
            self.fail(f"FAIL: Failed to start new ETL tracer (Test Issue)")
        logging.info(f"PASS: Started new ETL Tracer")

        if self.display_power_.invoke_power_event(display_power.PowerEvent.S3, common.POWER_EVENT_DURATION_DEFAULT) is False:
            self.fail('FAIL: Failed to invoke power event S3')

        status, etl_file_path = stop_existing_etl("GfxTrace_after_powerevent")
        if not status:
            self.fail("FAIL: Failed to stop ETL tracer")

        status = verify_vdd_status_powerevent(etl_file_path)
        if not status:
            self.fail("FAIL: Failed to verify VDD Status with power event")
        logging.info("PASS: Verified VDD Status with power event")


    ##
    # @brief        This test verifies VDD status with CS power event
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["CS"])
    # @endcond
    def t_12_cs(self):
        if self.display_power_.is_power_state_supported(display_power.PowerEvent.CS) is False:
            self.fail("FAIL: CS is NOT enabled in the system")

        if etl_tracer.start_etl_tracer() is False:
            self.fail("FAIL: Failed to start new ETL tracer (Test Issue)")
        logging.info("PASS: Started new ETL Tracer")

        if self.display_power_.invoke_power_event(display_power.PowerEvent.CS, common.POWER_EVENT_DURATION_DEFAULT) is False:
            self.fail('FAIL: Failed to invoke power event CS')

        status, etl_file_path = stop_existing_etl("GfxTrace_after_powerevent")
        if not status:
            self.fail("FAIL: FAILED to stop ETL tracer")

        status = verify_vdd_status_powerevent(etl_file_path)
        if not status:
            self.fail("FAIL: Failed to verify VDD Status with power event")
        logging.info("PASS: Verified VDD Status with power event")


if __name__ == '__main__':
    TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(VddStatusCheck))
    TestEnvironment.cleanup(test_result)
