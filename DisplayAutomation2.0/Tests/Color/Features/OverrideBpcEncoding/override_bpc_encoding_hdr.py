#################################################################################################
# @file         override_bpc_encoding_gfx_events.py
# @brief        This is a custom script which can used to display configurations with supported bpc and encoding
#               will perform below functionalities
#               1.To configure bpc and encoding through escape
#               2.To perform register verification for bpc and encoding
#               3.Will configure  hdr enable/disable.
#               4.Verify the persistence after the event
# @author       Vimalesh D
#################################################################################################
from Libs.Core import display_power
from Tests.Color.Common.color_properties import FeatureCaps
from Tests.Color.Common.common_utility import apply_mode
from Tests.Color.Features.E2E_HDR.hdr_test_base import HDRTestBase
from Tests.Color.Features.OverrideBpcEncoding.override_bpc_encoding_test_base import *

##
# @brief - To perform persistence verification for bpc and encoding with HDR
class OverrideBpcEncodingPersistenceHdr(OverrideBpcEncodingBase):

    ##
    # @brief test_01_hdr_enable_disable function - Function to perform HDR enable disable with override bpc and encoding
    #                                              and perform register and verification on all panels
    #                                                  .
    # @param[in] self
    # @return None
    @unittest.skipIf(get_action_type() != "HDR",
                     "Skip the  test step as the action type is not HDR")
    def test_01_hdr_enable_disable(self):
        bpc = None
        encoding = None
        feature_caps = FeatureCaps()
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active:

                    feature_caps.HDRSupport = True
                    setattr(self.context_args.adapters[gfx_index].panels[port], "FeatureCaps", feature_caps)

                    self.enable_and_verify(adapter.gfx_index,panel.display_and_adapterInfo,panel.pipe, panel.transcoder
                                           ,adapter.platform, adapter.platform_type,port,panel.is_lfp,panel.connector_port_type)


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

        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active:
                    plane_id = color_etl_utility.get_plane_id(panel.pipe, gfx_index)
                    if verify(adapter.gfx_index, adapter.platform, panel.pipe, plane_id, panel.transcoder,
                              self.panel_props_dict[gfx_index, port].Bpc, self.panel_props_dict[gfx_index,
                                                                                                port].Encoding) is False:
                        self.fail()

        if HDRTestBase().toggle_hdr_on_all_supported_panels(enable=False) is False:
            self.fail()

        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active:
                    plane_id = color_etl_utility.get_plane_id(panel.pipe, gfx_index)
                    if verify(adapter.gfx_index, adapter.platform, panel.pipe, plane_id, panel.transcoder,
                              self.panel_props_dict[gfx_index, port].Bpc,self.panel_props_dict[gfx_index,
                                                                                               port].Encoding) is False:
                        self.fail()

    ##
    # If the test enables HDR and fails in between, then HDR has to be disabled
    def tearDown(self):
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if feature_basic_verify.hdr_status(gfx_index, adapter.platform, panel.pipe):
                    if HDRTestBase().toggle_hdr_on_all_supported_panels(enable=False) is False:
                        self.fail()
        super().tearDown()


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test purpose: Configure the bpc and encoding for the panel and verify the persistence with HDR "
                 "enable/disable and perform register verification")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
