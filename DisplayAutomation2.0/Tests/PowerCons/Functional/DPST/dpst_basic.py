########################################################################################################################
# @file         dpst_basic.py
# @brief        Test for DPST/OPST basic scenarios
#
# @author       Ashish Tripathi, Neha Kumari
########################################################################################################################

from Libs.Core.test_env import test_environment

from Tests.PowerCons.Functional.DPST.dpst_base import *
from Tests.PowerCons.Modules.workload import change_power_source, PowerSource


##
# @brief        This class contains basic test cases for DPST/OPST
class DpstBasic(DpstBase):
    ##
    # @brief        This function verifies DPST/OPST with AC power source
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["AC"])
    # @endcond
    def t_11_dpst_basic_ac(self):
        if change_power_source(PowerSource.AC_MODE) is False:
            self.fail("Failed to switch power source to AC mode")

        etl_file = dpst.run_workload(self.workload_method, polling_offsets=self.offsets)
        if etl_file is False:
            self.fail("Failed to run the workload")
        if self.validate_xpst(etl_file, self.workload_method, PowerSource.AC_MODE) is False:
            self.fail("FAIL: {0} feature verification with AC mode".format(self.xpst_feature_str))
        logging.info("PASS: {0} feature verification with AC mode".format(self.xpst_feature_str))

    ##
    # @brief        This function verifies DPST/OPST with DC power source
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["DC"])
    # @endcond
    def t_12_dpst_basic_dc(self):
        etl_file = dpst.run_workload(self.workload_method, polling_offsets=self.offsets)

        if etl_file is False:
            self.fail("Failed to run the workload")
        if self.validate_xpst(etl_file, self.workload_method, PowerSource.DC_MODE) is False:
            self.fail("FAIL: {0} feature verification with DC mode".format(self.xpst_feature_str))
        logging.info("PASS: {0} feature verification with DC mode".format(self.xpst_feature_str))


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(DpstBasic))
    test_environment.TestEnvironment.cleanup(test_result)
