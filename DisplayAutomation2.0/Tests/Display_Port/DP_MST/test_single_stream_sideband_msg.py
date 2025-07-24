#######################################################################################################################
# @file         test_single_stream_sideband_msg.py
# @brief        Test to check if single stream sideband message supported display is enumerated properly and not treated
#               as MST display
# @details      Test Scenario:
#               1. Plugs the SST Sideband Message Supported display
#               2. Applies SINGLE display configuration for SST Sideband Message Supported Display
#               3. Applies max mode for SST Sideband Message Supported Display
#               4. Verify SST Sideband Message Supported Display DPCD Programming
#               5. Verify display engine programming for SST Sideband Message Supported Display
#               This test can be planned with only SST Sideband Message Supported Displays
#
# @author       Praburaj Krishnan
#######################################################################################################################
import logging
import unittest

from Libs.Feature.vdsc import dsc_verifier
from Libs.Feature.vdsc.dsc_helper import DSCHelper
from Libs.Feature.display_engine.de_master_control import DisplayEngine
from Libs.Core.test_env import test_environment
from Libs.Core import enum
from Tests.Color.Common import color_escapes
from Tests.Color.HDR.OSHDR.os_hdr_verification import OSHDRVerification
from Tests.Display_Port.DP_MST.display_port_mst_base import DisplayPortMSTBase
from Tests.PowerCons.Modules import common


##
# @brief        Class that holds various test that verifies Single Stream Sideband Message Supported Display test cases.
class TestSingleStreamSidebandMessage(DisplayPortMSTBase):

    ##
    # @brief        This Functions Helps to Plug the SST SBM Supported Display and Verifies if its a SST SBM display.
    # @return       None
    def plug_display(self) -> None:
        index = 0
        cls = DisplayPortMSTBase

        # Get the port type from available free DP ports
        self.port_type = self.get_dp_port_from_availablelist(index)

        # Get Topology Type(MST/SST) from the command line
        topology_type = self.get_topology_type(index)

        # Get Topology XML file from command line
        xml_file = self.get_xmlfile(index)

        logging.info(f"Plugging SST Sideband MSG Supported Display at {self.port_type}")
        self.setnverifyMST(self.port_type, topology_type, xml_file)

        self.display_and_adapter_info = cls.display_config.get_display_and_adapter_info_ex(self.port_type)

        self.gfx_index = self.display_and_adapter_info.adapterInfo.gfxIndex
        index = int(self.gfx_index[-1])
        self.platform = str.lower(DSCHelper.DISPLAY_HARDWARE_INFO_LIST[index].DisplayAdapterName)

    ##
    # @brief        This Function Sets SINGLE Display Config on the SST SBM display, Verifies it, then Applies Max Mode
    #               for the Display and Verifies it.
    # @return       None
    def set_and_verify_max_mode(self) -> None:
        cls = DisplayPortMSTBase

        logging.info(f"Applying Single Display configuration on SST SBM Supported Display")
        is_success = cls.display_config.set_display_configuration_ex(enum.SINGLE, [self.display_and_adapter_info])
        self.assertTrue(is_success, f"Applying Single Display Config SST SBM Supported Display Failed")
        common.print_current_topology()

        max_mode = common.get_display_mode(self.display_and_adapter_info.TargetID)
        self.assertIsNotNone(max_mode, "[Test Issue] - Failed to Get Max Mode.")

        # Set Max Mode For Each of the Display
        logging.info(f"Applying Max Mode on SST SBM Supported Display at {self.port_type}")
        is_success = cls.display_config.set_display_mode([max_mode], False)
        self.assertTrue(is_success, f"[Driver Issue] - Failed to Apply Max Display Mode on {self.port_type}")
        common.print_current_topology()

    ##
    # @brief        This Function performs all the Verification required for SST SBM Display like DPCD programming by
    #               driver, Display Engine MMIO Programming and DSC is also Verified Whenever DSC is Required to Drive
    #               the mode.
    # @return       None
    def verify_sst_sbm_display(self) -> None:
        cls = DisplayPortMSTBase

        is_success = cls.verify_sst_sbm_dpcd_programming(self.display_and_adapter_info)
        self.assertTrue(is_success, f"[Driver Issue] - SST SBM Supported Display Verification Failed.")

        display_engine = DisplayEngine()
        is_success = display_engine.verify_display_engine()
        self.assertTrue(is_success, "[Driver Issue] - DE Verification failed for SST SBM Supported Display")

        is_success = dsc_verifier.verify_dsc_programming(self.gfx_index, self.port_type)
        self.assertTrue(is_success, f"[Driver Issue] - DSC Verification for SST SBM Supported Display Failed.")

    ##
    # @brief        Basic test case to verify if plugged SST Sideband Message Supported Display is up and running in its
    #               max mode.
    # @return       None
    # @cond
    @common.configure_test(selective=["BASIC"])
    # @endcond
    def t_11_basic(self) -> None:
        self.plug_display()
        self.set_and_verify_max_mode()
        self.verify_sst_sbm_display()

    ##
    # @brief        This test helps to verify if HDR is working fine with Single Stream Sideband Message Display
    # @return       None
    # @cond
    @common.configure_test(selective=["HDR_ON_OFF"])
    # @endcond
    def t_12_hdr_on_off(self) -> None:
        hdr_verifier = OSHDRVerification()

        self.plug_display()
        self.set_and_verify_max_mode()

        # Enable HDR and Verify programming
        is_success = color_escapes.configure_hdr(self.port_type, self.display_and_adapter_info, enable=True)
        self.assertTrue(is_success, f"[Driver Issue] - HDR Enable Failed for SST SBM Display")

        is_success = hdr_verifier.verify_hdr_mode(self.port_type, "ENABLE", self.platform)
        self.assertTrue(is_success, f"[Driver Issue] - HDR Verification (Enabled) Failed for SST SBM Display")

        self.verify_sst_sbm_display()

        # Disable HDR and Verify programming
        is_success = color_escapes.configure_hdr(self.port_type, self.display_and_adapter_info, enable=False)
        self.assertTrue(is_success, f"[Driver Issue] - HDR Disable Failed for SST SBM Display")

        is_success = hdr_verifier.verify_hdr_mode(self.port_type, "DISABLE", self.platform)
        self.assertTrue(is_success, f"[Driver Issue] - HDR Verification (Disabled) Failed for SST SBM Display")

        self.verify_sst_sbm_display()


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(TestSingleStreamSidebandMessage))
    test_environment.TestEnvironment.cleanup(test_result)
