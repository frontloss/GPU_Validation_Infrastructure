#################################################################################################
# @file         override_bpc_encoding_power_events_inf.py
# @brief        This is a custom script which can used to set the 10 bpc and encoding for an LFP panel
#               using OEM RegKey and verify the functionality
#               1.Set the BPC 10 and encoding for an LFP Panel
#               2.To perform register verification for bpc and encoding
#               3.Will perform  power_events(),restart_display_driver(),monitor_turn_off_on()
#               4.Verify the persistence after the event
# @author       Shivani Santoshi
#################################################################################################
import time
from Libs.Core import display_power, display_essential, driver_escape
from Tests.Color import color_common_utility
from Tests.Color.Features.OverrideBpcEncoding.override_bpc_encoding_test_base import *


##
# @brief - To perform persistence verification for BPC and Encoding
class OverrideBpcEncodingPersistenceGfxEvents(OverrideBpcEncodingBase):
    lfp_tid_pnp_pair = {}
    
    ############################
    # Test Function
    ############################
    
    ##
    # @brief test_01_power events function - Function to perform
    #                                        power events S3,CS,S4 and perform register verification on all panels.
    # @param[in] self
    # @return None
    @unittest.skipIf(get_action_type() not in ["POWER_EVENT_S3", "POWER_EVENT_S4", "POWER_EVENT_CS"],
                     "Skip the  test step as the action type is not power event S3/CS/S4")
    def test_01_power_events(self):
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
                                     reg_type=registry_access.RegDataType.DWORD,
                                     reg_value=int(bpc.replace("BPC", ""))) is False:
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
        
        power_state_dict = {
            "POWER_EVENT_S3": display_power.PowerEvent.S3, "POWER_EVENT_CS": display_power.PowerEvent.CS,
            "POWER_EVENT_S4": display_power.PowerEvent.S4}
        
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active and panel.is_lfp:
                    plane_id = color_etl_utility.get_plane_id(panel.pipe, gfx_index)
                    if verify(adapter.gfx_index, adapter.platform, panel.pipe, plane_id,
                              panel.transcoder, bpc, encoding, conv_type=None) is False:
                        self.fail("Fail: Failed to verify the override bpc and encoding")
                    else:
                        logging.info("Successfully verified the override bpc {0} and encoding {1} before invoking power event".format(bpc, encoding))
        
        ##
        # Invoke power event
        if invoke_power_event(power_state_dict[self.scenario]) is False:
            self.fail(" Fail: Failed to invoke power event {0}".format(power_state_dict[self.scenario]))
        else:
            for gfx_index, adapter in self.context_args.adapters.items():
                for port, panel in adapter.panels.items():
                    if panel.is_active and panel.is_lfp:
                        plane_id = color_etl_utility.get_plane_id(panel.pipe, gfx_index)
                        if verify(adapter.gfx_index, adapter.platform, panel.pipe, plane_id,
                                  panel.transcoder, bpc, encoding, conv_type=None) is False:
                            self.fail("Fail: Failed to verify the override bpc and encoding")
                        else:
                            logging.info(
                                "Successfully verified the override bpc {0} and encoding {1} after invoking power event".format(
                                    bpc, encoding))
    
    ##
    # @brief test_02_restart display driver function - Function to perform restart display driver and perform register
    #                                                  verification on all supported panels.
    # @param[in] self
    # @return None
    @unittest.skipIf(get_action_type() != "RESTART_DRIVER",
                     "Skip the  test step as the action type is not Restart driver")
    def test_02_restart_display_driver(self):
        bpc = self.bpc
        encoding = "RGB"
        
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
                                     reg_type=registry_access.RegDataType.DWORD,
                                     reg_value=int(bpc.replace("BPC", ""))) is False:
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
                        logging.info(
                            "Successfully verified the override bpc {0} and encoding {1} before driver restart".format(bpc,
                                                                                                                  encoding))
            
        ##
        # restart display driver
        status, reboot_required = common_utility.restart_display_driver(adapter.gfx_index)
            
        # reading registry key
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
                            "Successfully verified the override bpc {0} and encoding {1} after driver restart".format(
                                bpc, encoding))
    
    ##
    # @brief test_03_monitor_turnoffon function - Function to perform monitor turnoff_on and perform register
    #                                             verification on all supported panels
    #                                                  .
    # @param[in] self
    # @return None
    @unittest.skipIf(get_action_type() != "MONITOR_TURNOFFON",
                     "Skip the  test step as the action type is not Monitor Turnoff_on")
    def test_03_monitor_turn_off_on(self):
        
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
                                     reg_type=registry_access.RegDataType.DWORD,
                                     reg_value=int(bpc.replace("BPC", ""))) is False:
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
                        logging.info("Successfully verified the override bpc {0} and encoding {1} before monitor turnoffon".format(bpc, encoding))
        
        ##
        # monitor turn off-on
        if common_utility.invoke_monitor_turnoffon() is False:
            self.fail("Failed to Turned Off-On Monitor event")
        
        # reading registry key after monitor turn off-on
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
                        logging.info("Successfully verified the override bpc {0} and encoding {1} after monitor turnoffon".format(bpc, encoding))
                        
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
                 "verify the persistence after the power events")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
