from Tests.Color.color_common_base import *
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE
from Libs.Core.display_config.display_config import configure_hdr
from Tests.Color import color_common_utility
from Tests.Color.HDR.OSHDR import os_hdr_verification


class OSHDRBase(ColorCommonBase):

    os_hdr_verify = os_hdr_verification.OSHDRVerification()

    def toggle_and_verify_hdr(self, toggle):
        hdr_enable = True if toggle == "ENABLE" else False
        for display_index in range(self.enumerated_displays.Count):
            if str(CONNECTOR_PORT_TYPE(
                self.enumerated_displays.ConnectedDisplays[
                    display_index].ConnectorNPortType)) in self.connected_list:
                if self.enumerated_displays.ConnectedDisplays[display_index].IsActive:
                    hdr_error_code = configure_hdr(self.enumerated_displays.ConnectedDisplays[display_index].
                                               DisplayAndAdapterInfo, enable=hdr_enable)
                    ##
                    # Decode HDR Error Code and Verify
                    if self.os_hdr_verify.is_error("OS_HDR", hdr_error_code, toggle) is False:
                        self.fail()

                    ##
                    # Verify PIPE_MISC for register verification
                    if self.os_hdr_verify.verify_hdr_mode(str(CONNECTOR_PORT_TYPE(
                            self.enumerated_displays.ConnectedDisplays[display_index].ConnectorNPortType)),
                            toggle, self.platform) is False:
                        self.fail()
                else:
                    logging.error("Plugged display: %s was inactive" % (CONNECTOR_PORT_TYPE(
                        self.enumerated_displays.ConnectedDisplays[display_index].ConnectorNPortType)))
                    self.fail("Plugged display was inactive")

    def apply_native_mode(self, refresh_rate=60):
        for display_index in range(self.enumerated_displays.Count):
            if str(CONNECTOR_PORT_TYPE(self.enumerated_displays.ConnectedDisplays[display_index].ConnectorNPortType)) in self.connected_list:
                if self.enumerated_displays.ConnectedDisplays[display_index].IsActive:
                    if color_common_utility.apply_native_mode(str(CONNECTOR_PORT_TYPE(self.enumerated_displays.ConnectedDisplays[display_index].ConnectorNPortType)),self.enumerated_displays, refresh_rate) is False:
                        self.fail("Failed to apply the required modeset")
                else:
                    logging.error("Plugged display %s was  inactive" % (CONNECTOR_PORT_TYPE(
                        self.enumerated_displays.ConnectedDisplays[display_index].ConnectorNPortType)))
                    self.fail("Plugged display was  inactive")

    def setUp(self):
        ##
        # Invoking the Base Class's setUp() to set up common utilities like plugging the display and applying the desired configuration
        super().setUp()

    def tearDown(self):
        self.toggle_and_verify_hdr(toggle="DISABLE")
        super().tearDown()
