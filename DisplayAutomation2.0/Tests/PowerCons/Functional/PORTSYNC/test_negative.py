#######################################################################################################################
# @file         test_negative.py
# @addtogroup   Powercons
# @section      PORTSYNC
# @brief        Test for port sync in negative scenario.
#
# @author       Bhargav Adigarla
#######################################################################################################################
from Libs.Core.test_env import test_environment
from Tests.PowerCons.Functional.PORTSYNC.port_sync_base import *


##
# @brief        This class contains port sync negative tests
class TestNegative(PortSyncBase):
    ##
    # @brief        this function verifies negative port sync test
    # @return       None
    def t_10_test_basic(self):
        status = True
        for adapter in dut.adapters.values():
            cmtg_status = cmtg.disable(adapter)
            if cmtg_status is False:
                self.fail("FAILED to disable CMTG")
            if cmtg_status is True:
                result, reboot_required = display_essential.restart_gfx_driver()
                if result is False:
                    self.fail("FAILED to restart the driver")
            panels = [adapter.panels.values()]
            if cmtg.verify_cmtg_status(adapter) is True:
                logging.info("CMTG status expected = False actual = True")
                status = False
            if cmtg.verify_cmtg_slave_status(adapter, panels[0]) is True:
                logging.info("CMTG slave status expected = False actual = True")
                status = False
            if cmtg.verify_cmtg_slave_status(adapter, panels[1]) is True:
                logging.info("CMTG slave status expected = False actual = True")
                status = False

        if status is False:
            self.fail("Port sync negative verification failed")
        logging.info("Port sync negative verification successful")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.runner.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(TestNegative))
    test_environment.TestEnvironment.cleanup(test_result)