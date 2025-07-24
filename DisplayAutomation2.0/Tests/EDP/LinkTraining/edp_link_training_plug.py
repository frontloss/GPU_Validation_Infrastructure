########################################################################################################################
# @file         edp_link_training_plug.py
# @addtogroup   EDP
# @section      EDP_Link_Training_Tests
# @brief        This file contains tests fo verify eDP link training by getting input DPCD model data
# @details      Test will get input DPCD model data and plug eDP display with input data.
#               Validates link training data by comparing expected response data from xml and actual data from
#               diana log file.
# @author       Kruti Vadhavaniya, Bhargav Adigarla
########################################################################################################################
import os
import unittest
import logging

from Libs.Core.display_config import display_config
from Libs.Core import reboot_helper
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.display_utility import driver_interface
from Libs.Core.display_utility import plug
from Libs.Core.test_env import test_context
from Tests.EDP.LinkTraining import edp_link_training_base


##
# @brief        This class contains test fo verify eDP link training by getting input DPCD model data
class EdpLinkTrainingPlug(edp_link_training_base.EdpLinkTrainingBase):

    config = display_config.DisplayConfiguration()
    driver_interface_ = driver_interface.DriverInterface()

    ##
    # @brief        This functions gets input DPCD model data and verifies plug of display
    # @return       None
    def test_plug(self):

        connector_port = "DP_A"

        # initialize required ports
        adapter_info = test_context.TestContext.get_gfx_adapter_details()["gfx_0"]
        self.driver_interface_.initialize_lfp_ports(adapter_info, [connector_port])

        get_dpcd_model_data = self.get_dpcd_model_data(self.xml_file_path)
        dpcd_model_data = self.set_dpcd_model(get_dpcd_model_data[0], get_dpcd_model_data[1], get_dpcd_model_data[2],
                                              get_dpcd_model_data[3], get_dpcd_model_data[4], get_dpcd_model_data[5])

        logging.info("Plugging display {0} with low_power by passing LT model data to plug".format(connector_port))
        plug(connector_port, edid="Acer_H277HK_DP.bin", dpcd="Acer_H277HK_nonVRR_DPCD.txt",
             dp_dpcd_model_data=dpcd_model_data, is_lfp=True)

        if reboot_helper.reboot(self, 'test_after_reboot') is False:
            self.fail("Failed to reboot the system")

    ##
    # @brief        This functions verifies link training after reboot
    # @return       None
    def test_after_reboot(self):
        logging.info("System boot back after plug")
        status = False

        # Stop etl and get the etl file path
        etl_file_path = self.stop_etl_get_etl_file_path()

        # Get diana log file
        diana_exe_path = os.path.join(test_context.SHARED_BINARY_FOLDER, "DiAna\\DiAna.exe")
        diana_log_file = self.get_diana_file(diana_exe_path, etl_file_path)

        # Verify training data sequence with diana ETL logs
        status = self.validate_dpcd_model_data(diana_log_file)

        if status is True:
            logging.info("PASS: Link Training Successful !!!")
        else:
            self.fail("FAIL: Link Training Failed !!!")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('EdpLinkTrainingPlug'))
    TestEnvironment.cleanup(outcome)
