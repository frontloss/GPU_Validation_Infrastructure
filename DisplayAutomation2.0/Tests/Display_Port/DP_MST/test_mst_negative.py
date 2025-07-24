################################################################################################################
# @file         test_mst_negative.py
# @brief        Verify if Driver gracefully exits from Negative Trigger Conditions.
# @author       Veena, Veluru
################################################################################################################
import logging
import unittest

from Libs.Core import enum
from Libs.Core.logger import gdhm
from Libs.Core.test_env import test_environment
from Tests.Display_Port.DP_MST.display_port_mst_base import DisplayPortMSTBase
from Tests.PowerCons.Modules import common


##
# @brief        This class has basic tests to verify MST Negative scenarios  
class TestDPMSTNegativeEvents(DisplayPortMSTBase):

    ##
    # @brief        Basic test case to verify if driver enumerates fake edid when faulty edid is plugged in.
    # @return       None
    # @cond
    @common.configure_test(selective=["FAULTY_EDID"])
    # @endcond
    def t_1_mst_faulty_edid_test(self) -> None:
        dp_port_index = 0

         # Get the port type from available free DP ports
        self.port_type = self.get_dp_port_from_availablelist(dp_port_index)

        # Get Topology XML file from command line
        self.xml_file = self.get_xmlfile(dp_port_index)

        # Get Topology Type(MST/SST) from the command line
        topology_type = self.get_topology_type(dp_port_index)

        self.plug_mst_display(self.port_type, topology_type, self.xml_file)

        display_and_adapter_info = self.display_config.get_display_and_adapter_info_ex(self.port_type, 'gfx_0')
        status = self.display_config.set_display_configuration_ex(enum.SINGLE, [display_and_adapter_info])
        self.assertTrue(status, "Set Display Configuration failed for SINGLE modeset of MST panel")

        # Get the current applied mode
        current_mode = self.display_config.get_current_mode(display_and_adapter_info)
        if current_mode.HzRes == 1920 and current_mode.VtRes == 1080:
            logging.info("PASS: If sink did not provide any information about Video fallback, Enumerate default timing of 19x10")
        else:
            gdhm.report_driver_bug_di(title="[Interfaces][DP_MST] MST Fake EDID Enumeration Failed")
            self.fail("MST Fake EDID Enumeration Failed. HActive: {} VActive: {}".format(current_mode.HzRes,current_mode.VtRes))            


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(TestDPMSTNegativeEvents))
    test_environment.TestEnvironment.cleanup(test_result)
