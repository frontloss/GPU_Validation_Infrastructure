#################################################################################################
# @file         hdr_persistence_with_reboot.py
# @brief        This scripts enables HDR and performs verification on all the pipes
#               The script then performs a system reboot. After the system successfully reboots,
#               HDR persistence is verified by performing ETL and register level verification
#               Verification Details:
#               The test script verifies the DisplayCaps from the ETL for HDR support in the EDID.
#               Post enabling HDR, the status_code returned from the OS API is decoded and verified.
#               Pipe_Misc register is also verified for HDR_Mode
#               Plane and Pipe Verification is performed by iterating through each of the displays
#               Metadata verification, by comparing the Default and Flip Metadata is performed,
#               along with register verification
# Sample CommandLines:  python hdr_persistence_with_reboot.py -edp_a SINK_EDP050 -scenario POWER_EVENT_S3
# @author       Smitha B
#################################################################################################
from Libs.Core import reboot_helper
from Tests.Color.Features.E2E_HDR.hdr_test_base import *


##
# @brief - To perform persistence verification for Quantisation reboot scenario
class HDRPersistenceWithReboot(HDRTestBase):

    ##
    # @brief Unittest test_before_reboot function - To enable and verify before reboot scenario
    # @param[in] self
    # @return None
    def test_before_reboot(self):
        ##
        # Enable HDR on all the supported panels and perform verification
        logging.info("*** Step 1 : Enable HDR on all supported panels and verify ***")
        if self.enable_hdr_and_verify() is False:
            self.fail()

        if reboot_helper.reboot(self, 'test_after_reboot') is False:
            self.fail("Failed to reboot the system")

    ##
    # @brief Unittest test_after_reboot function - To perform register verification after reboot scenario
    # @param[in] self
    # @return None
    def test_after_reboot(self):
        metadata_scenario = color_properties.HDRMetadataScenario()
        metadata_scenario.reboot = 1

        if color_etl_utility.start_etl_capture() is False:
            logging.error("Failed to Start Gfx Tracer")
            return False
        logging.info("*** Step 2 : Resume from PowerEvent S5 and verify ***")
        logging.info("Successfully resumed from PowerEvent S5 state")
        color_properties.update_feature_caps_in_context(self.context_args)

        #panel_props = color_properties.HDRProperties()
        event = "System_Restart_TimeStmp_"
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                logging.info(
                    "Updating all color properties for Panel : {0} on Adapter : {1} attached to Pipe : {2}"
                    " after System Restart event".format(
                        port, gfx_index, panel.pipe))
                panel_props = color_properties.HDRProperties()
                self.panel_props_dict[gfx_index, port] = panel_props
                if self.update_common_color_props_for_all(event) is False:
                    self.fail()
                status, self.bpc = self.verify_feature_modeset_from_os(panel.pipe, True)
                if status is False:
                    return False
                panel_props.bpc = self.bpc

                self.panel_props_dict[gfx_index, port] = panel_props
                if panel.is_active:
                    plane_id = color_etl_utility.get_plane_id(panel.pipe, gfx_index)
                    if self.plane_verification(gfx_index, adapter.platform, panel, plane_id, port) is False:
                        self.fail()
                    if self.pipe_verification(gfx_index, adapter.platform, port, panel) is False:
                        self.fail()
        metadata_scenario.reboot = 0


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test purpose: Enable HDR and perform verification on all panels")
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('HDRPersistenceWithReboot'))
    TestEnvironment.cleanup(outcome)
