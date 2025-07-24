#################################################################################################
# @file         override_bpc_encoding_reboot_inf.py
# @brief        This is a custom script which can used to set the 10 bpc and encoding for an LFP panel
#               using OEM RegKey and verify the functionality
#               1.Set the BPC 10 and encoding for an LFP Panel
#               2.To perform register verification for bpc and encoding
#               3.Will perform  reboot event
#               4.Verify the persistence after the event
# @author       Shivani Santoshi
#################################################################################################
import time

from Libs.Core import reboot_helper, display_essential, driver_escape
from Tests.Color import color_common_utility
from Tests.Color.Features.OverrideBpcEncoding.override_bpc_encoding_test_base import *


##
# @brief - To perform persistence verification for BPC and Encoding
class OverrideBpcEncodingreboot(OverrideBpcEncodingBase):
    lfp_tid_pnp_pair = {}

   ##
    # @brief Unittest test_before_reboot function - To enable and verify before reboot scenario
    # @param[in] self
    # @return None
    def test_before_reboot(self):
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
            target_id_hex = str(target_id_hex).replace("0x","")
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

        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active and panel.is_lfp:
                    plane_id = color_etl_utility.get_plane_id(panel.pipe, gfx_index)
                    if verify(adapter.gfx_index, adapter.platform, panel.pipe, plane_id,
                              panel.transcoder, bpc, encoding, conv_type=None) is False:
                        self.fail("Fail: Failed to verify the override bpc and encoding")
                    else:
                        logging.info("Successfully verified the override bpc {0} and encoding {1} before reboot".format(bpc, encoding))
                        
        if reboot_helper.reboot(self, 'test_after_reboot') is False:
            self.fail("Failed to reboot the system")

    ##
    # @brief Unittest test_after_reboot function - To perform register verification after reboot scenario
    # @param[in] self
    # @return None
    def test_after_reboot(self):
        bpc = self.bpc
        encoding = "RGB"

        logging.info("Successfully applied power event S5 state")
        
        # Get PNP-ID
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
            reg_name = "DefaultOutputFormatPreference_" + str(self.lfp_tid_pnp_pair[i])
            output_bpc_encoding = registry_access.read(reg_args, reg_name)
            logging.debug("Key Values is {0}".format(output_bpc_encoding))
        
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active and panel.is_lfp:
                    plane_id = color_etl_utility.get_plane_id(panel.pipe, gfx_index)
                    if verify(adapter.gfx_index, adapter.platform, panel.pipe, plane_id,
                              panel.transcoder, bpc, encoding, conv_type=None) is False:
                        self.fail("Fail: Failed to verify the override bpc and encoding")
                    else:
                        logging.info(
                            "Successfully verified the override bpc {0} and encoding {1} after reboot".format(bpc,
                                                                                                               encoding))
                        
    def tearDown(self):
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
    logging.info("Test purpose: Configure 10 BPC and encoding for the LFP panel using OEM RegKey and "
                 "verify the persistence for reboot scenario")
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('OverrideBpcEncodingreboot'))
    TestEnvironment.cleanup(outcome)
    