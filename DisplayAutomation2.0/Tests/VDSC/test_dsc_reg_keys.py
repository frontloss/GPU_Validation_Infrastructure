#######################################################################################################################
# @file         test_dsc_reg_keys.py
# @brief        This file will contain all the reg key related test cases of VDSC feature.
#
# @author       Praburaj Krishnan, Syed Rabbani, Goutham N
#######################################################################################################################

import logging
import unittest

from Libs.Core.logger import gdhm
from Libs.Core.test_env import test_environment
from Libs.Feature.display_engine.de_master_control import DisplayEngine
from Libs.Feature.vdsc.dsc_helper import DSCHelper, RegKey
from Libs.Feature.vdsc.dsc_enum_constants import DPCDOffsets
from Libs.Feature.vdsc import dsc_verifier
from Tests.VDSC.vdsc_base import VdscBase
from Tests.PowerCons.Modules import common


##
# @brief        This class contains a test function which implements the mentioned test scenario / test steps.
class TestDscRegKeys(VdscBase):

    # Dictionary contains Reg key name and value as key:value pairs.
    reg_keys_tested = {}

    # Below two lists contain expected DPCD values for Panamera (A2/B1) series of MST hubs - VSRI-6293
    expected_ieee_oui = [0x90, 0xCC, 0x24]
    expected_device_identification_string = [0x53, 0x59, 0x4E, 0x41, 0x53, 0x31]

    actual_ieee_oui = []
    actual_device_identification_string = []
    actual_hardware_revision = None

    ##
    # @brief        This test method checks VDSC is disabled after setting edp compression disable Reg Key to 1.
    # @details      Test Scenario:
    #               1. Verify the VDSC programming for the plugged edp panel.
    #               2. Set edpCompressionDisable reg key value to 1 and restart the gfx driver.
    #               3. Check whether the VDSC is disabled. If not fail the test.
    #               4. Set edpCompressionDisable reg key value to 0 and restart the gfx driver.
    #               5. Verify the VDSC programming for the plugged edp panel.
    #               This test can be planned with one EDP VDSC panel.
    # @return       None
    # @cond
    @common.configure_test(selective=["EDP_DSC_DISABLE"])
    # @endcond
    def t_11_validate_edp_dsc_reg_key(self) -> None:

        # Each dictionary inside vdsc_panel list will be of length 1, hence iterating dictionary is not needed.
        [(gfx_index, port)] = VdscBase.vdsc_panels[0].items()

        is_success = dsc_verifier.verify_dsc_programming(gfx_index, port)
        self.assertTrue(is_success, "[Driver issue] - DSC Verification Failed at {} on {}".format(port, gfx_index))

        display_engine = DisplayEngine()
        is_success = display_engine.verify_display_engine()
        self.assertTrue(is_success, "[Driver Issue] - Display Engine Verification Failed")

        # Disable VDSC for connected edp display by setting the reg key value to 1.
        is_success, is_reboot_required = RegKey.write(gfx_index, RegKey.VDSC.EDP_COMPRESSION_DISABLE, 0x01)
        self.assertTrue(is_success, "[Test issue] - eDPCompressionDisable Reg Key is not set")
        TestDscRegKeys.reg_keys_tested[(gfx_index, RegKey.VDSC.EDP_COMPRESSION_DISABLE)] = 0

        # Check VDSC is disabled for connected edp panel.
        is_dsc_enabled_in_driver = DSCHelper.is_vdsc_enabled_in_driver(gfx_index, port)
        is_dsc_enabled_in_panel = DSCHelper.is_vdsc_enabled_in_panel(gfx_index, port)
        is_dsc_enabled = is_dsc_enabled_in_driver or is_dsc_enabled_in_panel
        if is_dsc_enabled:
            gdhm.report_driver_bug_di(
                "[Display_Interfaces][VDSC] DSC is not disabled after setting eDPCompressionDisable")
        self.assertFalse(is_dsc_enabled, "[Driver issue] - DSC is not disabled after setting "
                                         "eDPCompressionDisable to 1")

        logging.info("VDSC is disabled after setting the edp compression disable reg key to 1")

        is_success = display_engine.verify_display_engine()
        self.assertTrue(is_success, "[Driver Issue] - Display Engine Verification Failed")

        # Enable VDSC for connected edp display by setting the reg key value to 0.
        is_success, is_reboot_required = RegKey.write(gfx_index, RegKey.VDSC.EDP_COMPRESSION_DISABLE, 0x00)
        self.assertTrue(is_success, "[Test issue] - eDPCompressionDisable Reg Key is not set")

        is_success = dsc_verifier.verify_dsc_programming(gfx_index, port)
        self.assertTrue(is_success, "[Driver issue] - DSC Verification Failed at {} on {}".format(port, gfx_index))

        is_success = display_engine.verify_display_engine()
        self.assertTrue(is_success, "[Driver Issue] - Display Engine Verification Failed")

    ##
    # @brief        This test method checks VDSC is disabled / enabled based on SINK_PREFERENCE DPCD (0x30Ch) bit 0
    #               after setting DPMstDscDisable Reg Key to either 0x1 or 0x2.
    # @details      Test Scenario:
    #               1. Set DPMstDscDisable reg key value to either 0x1 or 0x2 based on Reg Key value provided in the
    #               cmd line and restart the gfx driver.
    #               2. Check Reg Key Value
    #                   For Reg Key value 0x1
    #                   +-----------+--------+------------------++--------------------+---------+
    #                   | SINK_PREF | Is MST | Is DSC supported ||      DSC ENABLE    | Covered |
    #                   +===========+========+==================++====================+=========+
    #                   |     T     |   T    |        T         ||        F           |   NO    |
    #                   +-----------+--------+------------------++--------------------+---------+
    #                   |     T     |   T    |        F         ||        F           |   NO    |
    #                   +-----------+--------+------------------++--------------------+---------+
    #                   |     T     |   F    |        T         ||        T           |   NO    |
    #                   +-----------+--------+------------------++--------------------+---------+
    #                   |     T     |   F    |        F         ||        F           |   NO    |
    #                   +-----------+--------+------------------++--------------------+---------+
    #                   |     F     |   T    |        T         ||        F           |   YES   |
    #                   +-----------+--------+------------------++--------------------+---------+
    #                   |     F     |   T    |        F         ||        F           |   NO    |
    #                   +-----------+--------+------------------++--------------------+---------+
    #                   |     F     |   F    |        T         ||        T           |   NO    |
    #                   +-----------+--------+------------------++--------------------+---------+
    #                   |     F     |   F    |        F         ||        F           |   NO    |
    #                   +-----------+--------+------------------++--------------------+---------+
    #                   For Reg Key value 0x2
    #                   +-----------+--------+------------------++--------------------+---------+
    #                   | SINK_PREF | Is MST | Is DSC supported ||      DSC ENABLE    | Covered |
    #                   +===========+========+==================++====================+=========+
    #                   |     T     |   T    |        T         ||        T           |   YES   |
    #                   +-----------+--------+------------------++--------------------+---------+
    #                   |     T     |   T    |        F         ||        F           |   YES   |
    #                   +-----------+--------+------------------++--------------------+---------+
    #                   |     T     |   F    |        T         ||        T           |   NO    |
    #                   +-----------+--------+------------------++--------------------+---------+
    #                   |     T     |   F    |        F         ||        F           |   NO    |
    #                   +-----------+--------+------------------++--------------------+---------+
    #                   |     F     |   T    |        T         ||        F           |   YES   |
    #                   +-----------+--------+------------------++--------------------+---------+
    #                   |     F     |   T    |        F         ||        F           |   NO    |
    #                   +-----------+--------+------------------++--------------------+---------+
    #                   |     F     |   F    |        T         ||        T           |   YES   |
    #                   +-----------+--------+------------------++--------------------+---------+
    #                   |     F     |   F    |        F         ||        F           |   NO    |
    #                   +-----------+--------+------------------++--------------------+---------+
    #                   For reg key value 0x4
    #                   +-----------+--------+------------------++--------------------+-----------------+---------+
    #                   | SINK_PREF | Is MST | Is DSC supported |     IS PANAMERA    ||   DSC ENABLE    | COVERED |
    #                   +===========+========+==================++===================++=================+=========+
    #                   |     T     |   T    |        T         |         T          ||       F         |   YES   |
    #                   +-----------+--------+------------------+--------------------++-----------------+---------+
    #                   |     T     |   T    |        T         |         F          ||       T         |   YES   |
    #                   +-----------+--------+------------------+--------------------++-----------------+---------+
    #                   |     T     |   T    |        F         |         T          ||       F         |    NO   |
    #                   +-----------+--------+------------------+--------------------++-----------------+---------+
    #                   |     T     |   T    |        F         |         F          ||       F         |    NO   |
    #                   +-----------+--------+------------------++-------------------++-----------------+---------+
    #                   |     T     |   F    |        T         |         T          ||       T         |    NO   |
    #                   +-----------+--------+------------------+--------------------++-----------------+---------+
    #                   |     T     |   F    |        T         |         F          ||       T         |    NO   |
    #                   +-----------+--------+------------------+--------------------++-----------------+---------+
    #                   |     T     |   F    |        F         |         T          ||       F         |    NO   |
    #                   +-----------+--------+------------------+--------------------++-----------------+---------+
    #                   |     T     |   F    |        F         |         F          ||       F         |    NO   |
    #                   +-----------+--------+------------------+--------------------++-----------------+---------+
    #                   |     F     |   T    |        T         |         T          ||       F         |   YES   |
    #                   +-----------+--------+------------------+--------------------++-----------------+---------+
    #                   |     F     |   T    |        T         |         F          ||       T         |   YES   |
    #                   +-----------+--------+------------------+--------------------++-----------------+---------+
    #                   |     F     |   T    |        F         |         T          ||       F         |    NO   |
    #                   +-----------+--------+------------------+--------------------++-----------------+---------+
    #                   |     F     |   T    |        F         |         F          ||       F         |    NO   |
    #                   +-----------+--------+------------------+--------------------++-----------------+---------+
    #                   |     F     |   F    |        T         |         T          ||       T         |    NO   |
    #                   +-----------+--------+------------------+--------------------++-----------------+---------+
    #                   |     F     |   F    |        T         |         F          ||       T         |    NO   |
    #                   +-----------+--------+------------------+--------------------++-----------------+---------+
    #                   |     F     |   F    |        F         |         T          ||       F         |    NO   |
    #                   +-----------+--------+------------------+--------------------++-----------------+---------+
    #                   |     F     |   F    |        F         |         F          ||       F         |    NO   |
    #                   +-----------+--------+------------------+--------------------++-----------------+---------+
    #               3. Set DPMstDscDisable reg key value to 0 and restart the gfx driver.
    #               This test can be planned with DP MST/SST VDSC panel.
    # @return       None
    # @cond
    @common.configure_test(selective=["DP_MST_DSC_DISABLE"])
    # @endcond
    def t_11_validate_dp_mst_dsc_reg_key(self) -> None:

        # Each dictionary inside vdsc_panels/non_vdsc_panels list will be of length 1, hence iterating dictionary
        # is not needed.
        [(gfx_index, port)] = VdscBase.vdsc_panels[0].items() if len(VdscBase.vdsc_target_ids) == 1 else \
            VdscBase.non_vdsc_panels[0].items()

        # Get the Reg Key Value from the cmd line
        dp_mst_dsc_disable = int(VdscBase.get_cmd_line_param_values(field='REG_KEY_VALUE')[0])

        # Disable / Enable VDSC for connected dp mst/sst VDSC display by setting the reg key value.
        is_success, is_reboot_required = RegKey.write(gfx_index, RegKey.VDSC.DP_MST_DSC_DISABLE, dp_mst_dsc_disable)
        self.assertTrue(is_success, f"[Test issue] - DPMstDscDisable Reg Key is not set to {dp_mst_dsc_disable}")
        TestDscRegKeys.reg_keys_tested[(gfx_index, RegKey.VDSC.DP_MST_DSC_DISABLE)] = 0

        # Read the DPCD 21h offset for checking if connected panel is MST capable
        is_mst = bool(DSCHelper.read_dpcd(gfx_index, port, DPCDOffsets.MSTM_CAP)[0])

        # Read the DPCD 60h offset for checking if connected MST / SST panel is DSC capable
        is_dsc_supported = bool(DSCHelper.read_dpcd(gfx_index, port, DPCDOffsets.DSC_SUPPORT)[0])

        is_sink_prefers_mst_dsc = DSCHelper.read_dpcd(gfx_index, port, DPCDOffsets.SINK_PREFERENCE_DPCD)[0]

        # Read the DPCD from 500h-509h (SYNAPTIC_DP_BRANCH_IEEE_OUT_ID, SYNAPTIC_PANAMERA_DP_BRANCH_DEVICE_ID, DP_BRANCH_HW_REV_ID_INDEX) for checking if connected MST hub is Panamera series
        TestDscRegKeys.actual_ieee_oui = DSCHelper.read_dpcd(gfx_index, port, DPCDOffsets.IEEE_OUI, 3)
        TestDscRegKeys.actual_device_identification_string =  DSCHelper.read_dpcd(gfx_index, port, DPCDOffsets.DEVICE_IDENTIFICATION_STRING, 6)
        TestDscRegKeys.actual_hardware_revision = DSCHelper.read_dpcd(gfx_index, port, DPCDOffsets.HARDWARE_REVISION, 1)

        is_panamera_oui_id = (TestDscRegKeys.actual_ieee_oui == TestDscRegKeys.expected_ieee_oui and
                           TestDscRegKeys.actual_device_identification_string == TestDscRegKeys.expected_device_identification_string and
                           TestDscRegKeys.actual_hardware_revision[0] < 0x20)

        # We decide whether the test has to enable dsc / disable dsc based on 4 parameters. They are,
        # SINK_PREFERENCE DPCD (0x30Ch) bit 0, connected display is DSC supported, MST supported and IS_PANAMERA_OUI_ID.
        # By using these parameters, with the help of K-map, formulated an equation which helps the test to enable / disable dsc.
        # Formula = (DSC SUPPORTED) and (is_mst is False) - For reg_key = 0x1
        # Formula = (DSC SUPPORTED) and (SINK_PREF or is_mst is False) - For reg_key = 0x2
        # Formula = (DSC_SUPPORTED) and not (OUI_ID_MAT and IS_MST) - For reg_key = 0x4
        if dp_mst_dsc_disable == 1:
            is_dsc_preferred = is_dsc_supported and (is_mst is False)
        elif dp_mst_dsc_disable == 2:
            is_dsc_preferred = is_dsc_supported and (is_sink_prefers_mst_dsc or is_mst is False)
        elif dp_mst_dsc_disable == 4:
            is_dsc_preferred = is_dsc_supported and not (is_panamera_oui_id and is_mst)
        else:
            gdhm.report_test_bug_di("[VDSC][Test Issue]: Wrong reg key value is passed in command line for DP_MST_DSC_SUPPORTED.")
            self.assertTrue(False, "[VDSC][Test Issue]: Wrong reg key value is passed in command line for DP_MST_DSC_SUPPORTED.")

        # Check DSC is enabled in the driver
        is_dsc_enabled = DSCHelper.is_vdsc_enabled_in_driver(gfx_index, port)

        if is_dsc_preferred:
            # Check DSC is enabled for connected MST/SST VDSC panel.
            if not is_dsc_enabled:
                gdhm.report_driver_bug_di(
                    "[Display_Interfaces][VDSC]DSC not enabled for sink with MST DSC Sink preference set")
            self.assertTrue(
                is_dsc_enabled, f"[Driver issue] - DSC is not enabled for sink with MST DSC Sink Preference as "
                                f"{is_sink_prefers_mst_dsc}, MST DSC Disable Reg Value set to {dp_mst_dsc_disable}, "
                                f"MST Sink as {is_mst} and DSC Support as {is_dsc_supported}"
            )
            logging.info(
                f"DSC is enabled for sink with MST DSC Sink Preference as {is_sink_prefers_mst_dsc}, "
                f"MST DSC Disable Reg Value set to {dp_mst_dsc_disable}, MST Sink as {is_mst} and DSC Support as "
                f"{is_dsc_supported}"
            )
        else:
            if is_dsc_enabled:
                gdhm.report_driver_bug_di(
                    "[Display_Interfaces][VDSC]DSC not Disabled for sink with MST DSC Sink preference not Set")
            # Check DSC is disabled for connected MST/SST VDSC panel.
            self.assertFalse(
                is_dsc_enabled, f"[Driver issue] - DSC is not disabled for sink with MST DSC Sink Preference as "
                                f"{is_sink_prefers_mst_dsc}, MST DSC Disable Reg Value set to {dp_mst_dsc_disable}, "
                                f"MST Sink as {is_mst} and DSC Support as {is_dsc_supported}"
            )

            logging.info(
                f"DSC is disabled for sink with MST DSC Sink Preference as {is_sink_prefers_mst_dsc}, "
                f"MST DSC Disable Reg Value set to {dp_mst_dsc_disable}, MST Sink as {is_mst} and DSC Support as "
                f"{is_dsc_supported}"
            )

    ##
    # @brief        This test method will reset all the reg key values.
    # @return       None
    def t_19_disable_reg_keys(self) -> None:
        logging.info("Resetting the Reg Keys...")
        for key, reg_value in TestDscRegKeys.reg_keys_tested.items():
            gfx_index, reg_key = key
            is_success, is_reboot_required = RegKey.write(gfx_index, reg_key, reg_value)
            self.assertTrue(is_success, "[Test Issue] - Failed to reset the reg key")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.runner.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(TestDscRegKeys))
    test_environment.TestEnvironment.cleanup(test_result)
