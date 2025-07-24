############################################################################################################
# @file     reboot_helper_ult.py
# @brief    This will show how to use APIs exposed from reboot_helper_ult.py
# @author   Rohit Kumar
############################################################################################################
import unittest

from Libs.Core.display_power import *
from Libs.Core.test_env.test_environment import *
from Libs.Core import reboot_helper
from Libs.Core import test_header
from Libs.Core.gta import gta_state_manager


class RebootHelperUlt(unittest.TestCase):
    sample_class_data = 10

    @reboot_helper.__(reboot_helper.setup)
    def setUp(self):
        logging.info("ULT Start")

    def test_0_1_before_reboot(self):
        logging.info("Sample class data value in setup: {0}".format(self.sample_class_data))
        self.sample_class_data += 10
        logging.info("Before Reboot")
        status = reboot_helper.reboot(self, 'test_0_2_after_reboot', data={'sample_local_data': 100})
        if status is False:
            self.fail("Failed to reboot the system")

    def test_0_2_after_reboot(self):
        logging.info("Resumed from the power event POWER_STATE_S5 successfully")
        data = reboot_helper._get_reboot_data()
        logging.info("Data stored before reboot: {0}".format(data['sample_local_data']))
        if data['sample_local_data'] != 100:
            self.fail("Failed to restore data saved before reboot")
        logging.info("Class Data stored before reboot: {0}".format(self.sample_class_data))
        if self.sample_class_data != 20:
            self.fail("Failed to restore class data")

    @reboot_helper.__(reboot_helper.teardown)
    def tearDown(self):
        logging.info("ULT Complete")


if __name__ == '__main__':
    TestEnvironment.load_dll_module()
    display_logger._initialize(console_logging=True)
    gta_state_manager.create_gta_default_state()
    test_runner = unittest.TextTestRunner(verbosity=2)
    result = test_runner.run(reboot_helper.get_test_suite('RebootHelperUlt'))
    status = test_header.cleanup(result)
    gta_state_manager.update_test_result(result, status)
    display_logger._cleanup()

