#################################################################################################
# @file         override_bpc_encoding_hdr_inf.py
# @brief        This is a custom script which can used to set the 10 bpc and encoding for an LFP panel
#               using OEM RegKey and verify the functionality
#               1.Set the BPC 10 and encoding for an LFP Panel
#               2.To perform register verification for bpc and encoding
#               3.Will configure  hdr enable/disable.
#               4.Verify the persistence after the event
# @author       Shivani Santoshi
#################################################################################################
from Libs.Core import display_power, display_essential, driver_escape
from Tests.Color import color_common_utility
from Tests.Color.Common.color_properties import FeatureCaps
from Tests.Color.Common.common_utility import apply_mode
from Tests.Color.Features.E2E_HDR.hdr_test_base import HDRTestBase
from Tests.Color.Features.OverrideBpcEncoding.override_bpc_encoding_test_base import *


##
# @brief - To perform persistence verification for bpc and encoding with HDR
class OverrideBpcEncodingPersistenceHdr(OverrideBpcEncodingBase):
    lfp_tid_pnp_pair = {}
    
    ##
    # @brief test_01_hdr_enable_disable function - Function to perform HDR enable disable with override bpc and encoding
    #                                              and perform register and verification on all panels
    #                                                  .
    # @param[in] self
    # @return None
    @unittest.skipIf(get_action_type() != "HDR",
                     "Skip the  test step as the action type is not HDR")
    def test_01_hdr_enable_disable(self):
        bpc = self.bpc
        encoding = "RGB"

        # Get PNP-ID and Panel properties
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active and panel.is_lfp:
                    edid_data = driver_escape.get_edid_data(panel.target_id)
                    self.lfp_tid_pnp_pair[panel.target_id] = "".join(format(i, '02x') for i in edid_data[1][8:18])

                    # Get panel_props_dict[] for teardown
                    bpc_encoding_caps = BpcEncoding()
                    status, combo_bpc_encoding, default_bpc, default_encoding = get_bpc_encoding(
                        panel.display_and_adapterInfo,
                        adapter.platform_type)
                    bpc_encoding_caps.DefaultBpc = default_bpc
                    bpc_encoding_caps.Encoding = default_encoding
                    bpc_encoding_caps.DefaultEncoding = default_encoding
                    self.panel_props_dict[gfx_index, port] = bpc_encoding_caps

        reg_args = registry_access.StateSeparationRegArgs(gfx_index="gfx_0")
        for i in self.lfp_tid_pnp_pair.keys():
            target_id_hex = hex(i)
            target_id_hex = str(target_id_hex).replace("0x", "")
            color_common_utility.clean_bpc_persistence_registry(target_id_hex, self.lfp_tid_pnp_pair[i])
            reg_name = "DefaultOutputFormatPreference_" + str(self.lfp_tid_pnp_pair[i])
            logging.debug("RegKey Name is {0}".format(reg_name))
            if registry_access.write(args=reg_args, reg_name=reg_name,
                                     reg_type=registry_access.RegDataType.DWORD, reg_value=int(bpc.replace("BPC", ""))) is False:
                logging.error("Registry key add to OutputBpcAndEncodingPreference Data failed")
                self.fail()
            else:
                logging.info("RegKey {0} applied successfully".format(reg_name))

        display_essential.restart_display_driver()

        time.sleep(5)

        for i in self.lfp_tid_pnp_pair.keys():
            reg_name = "DefaultOutputFormatPreference_" + str(self.lfp_tid_pnp_pair[i])
            output_bpc_encoding = registry_access.read(reg_args, reg_name)
            logging.debug("Key Values is {0}".format(output_bpc_encoding))
        
        # Verification
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active and panel.is_lfp:
                    plane_id = color_etl_utility.get_plane_id(panel.pipe, gfx_index)
                    if verify(adapter.gfx_index, adapter.platform, panel.pipe, plane_id,
                              panel.transcoder, bpc, encoding, conv_type=None) is False:
                        self.fail("Fail: Failed to verify the override bpc and encoding")
                    else:
                        logging.info("Successfully verified the override bpc {0} and encoding {1} before enabling HDR".format(bpc, encoding))
        
        # Verify if the Power Mode is in DC and switch to AC
        # This is to override the OS Policy to disable HDR
        # when running Windows HD Color content on battery Power for battery optimization
        status = common_utility.apply_power_mode(display_power.PowerSource.AC)
        if status is False:
            self.fail()
            
            ##
            # Update the Context object with Displays Caps of each panel, both HDR and SDR
            # Display Caps are updated into the context object by parsing the ETLs
        if HDRTestBase().toggle_hdr_on_all_supported_panels(enable=True) is False:
            self.fail()
        
        # Reading RegKey
        for i in self.lfp_tid_pnp_pair.keys():
            reg_name = "DefaultOutputFormatPreference_" + str(self.lfp_tid_pnp_pair[i])
            output_bpc_encoding = registry_access.read(reg_args, reg_name)
            logging.debug("Key Values is {0}".format(output_bpc_encoding))
        
        # Verification
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active and panel.is_lfp:
                    plane_id = color_etl_utility.get_plane_id(panel.pipe, gfx_index)
                    if verify(adapter.gfx_index, adapter.platform, panel.pipe, plane_id,
                              panel.transcoder, bpc, encoding, conv_type=None) is False:
                        self.fail("Fail: Failed to verify the override bpc and encoding")
                    else:
                        logging.info("Successfully verified the override bpc {0} and encoding {1} after enabling HDR".format(bpc, encoding))
         
        # HDR Disable
        if HDRTestBase().toggle_hdr_on_all_supported_panels(enable=False) is False:
            self.fail()
        
        # Reading RegKey
        for i in self.lfp_tid_pnp_pair.keys():
            reg_name = "DefaultOutputFormatPreference_" + str(self.lfp_tid_pnp_pair[i])
            output_bpc_encoding = registry_access.read(reg_args, reg_name)
            logging.debug("Key Values is {0}".format(output_bpc_encoding))
        
        # Verification
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active and panel.is_lfp:
                    plane_id = color_etl_utility.get_plane_id(panel.pipe, gfx_index)
                    if verify(adapter.gfx_index, adapter.platform, panel.pipe, plane_id,
                              panel.transcoder, bpc, encoding, conv_type=None) is False:
                        self.fail("Fail: Failed to verify the override bpc and encoding")
                    else:
                        logging.info("Successfully verified the override bpc {0} and encoding {1} after disabling HDR".format(bpc, encoding))
        
        ##
        # If the test enables HDR and fails in between, then HDR has to be disabled
    def tearDown(self):
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if feature_basic_verify.hdr_status(gfx_index, adapter.platform, panel.pipe):
                    if HDRTestBase().toggle_hdr_on_all_supported_panels(enable=False) is False:
                        self.fail()
                        
        reg_args = registry_access.StateSeparationRegArgs(gfx_index="gfx_0")
        for i in self.lfp_tid_pnp_pair.keys():
            target_id_hex = hex(i)
            target_id_hex = str(target_id_hex).replace("0x", "")
            color_common_utility.clean_bpc_persistence_registry(target_id_hex, self.lfp_tid_pnp_pair[i])
            reg_name = "DefaultOutputFormatPreference_" + str(self.lfp_tid_pnp_pair[i])
            logging.debug("RegKey Name is {0}".format(reg_name))
            if registry_access.delete(args=reg_args, reg_name=reg_name) is False:
                logging.error("Registry key Delete to OutputBpcAndEncodingPreference Data failed")
                self.fail()
            else:
                logging.info("RegKey {0} Deletion is successful".format(reg_name))
        super().tearDown()


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test purpose: Configure the bpc and encoding for the panel and verify the persistence with HDR "
                 "enable/disable and perform register verification")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
