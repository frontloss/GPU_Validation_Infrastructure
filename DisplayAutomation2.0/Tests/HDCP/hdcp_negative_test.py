#######################################################################################################################
# @file         hdcp_negative_test.py
# @brief        HDCP negative test
# @details      Test for verifying HDCP with Non-HDCP panel using OPM tool
#
# @author       chandrakanth Reddy y
#######################################################################################################################

from Tests.HDCP.hdcp_base import *
from Libs.Core.vbt.vbt import Vbt
from Libs.Core import display_utility, display_essential


##
# @brief        Contains HDCP tests with Non-HDCP Panel
class HdcpNegative(HDCPBase):
    ##
    # @brief runTest function of Unit Test FrameWork.
    # @return None
    def runTest(self):
        displays = [port for port in self.display_list if display_utility.get_vbt_panel_type(port, 'gfx_0')
                    not in [display_utility.VbtPanelType.LFP_DP, display_utility.VbtPanelType.LFP_MIPI]]
        # Hot plug external display
        for ext_panel in displays:
            logging.info("Step:plug display {}".format(ext_panel))
            if display_utility.plug(ext_panel) is False:
                self.fail("Failed to plug display {}".format(ext_panel))
            logging.info("Pass:{} display plug success".format(ext_panel))
        # Apply the configuration passed in cmdline
        topology = eval("enum.%s" % (self.cmd_line_param['CONFIG']))
        if self.display_config.set_display_configuration_ex(topology, self.display_list,
                                                            self.enumerated_displays) is False:
            self.fail("FAIL: Failed to apply display configuration {} on displays {}".
                      format(self.cmd_line_param['CONFIG'], self.display_list))

        gfx_vbt = Vbt()
        ##
        # From 243 VBT onwards, Driver enable "Integrated Display Port only Internal to Chassis" field
        if gfx_vbt.version >= 243:
            for ext_panel in displays:
                if (ext_panel == 'DP_B'):
                    gfx_vbt.block_2.DisplayDeviceDataStructureEntry[0].DeviceClass = 0x4846

                    #Added new device class "Integrated Display Port only Internal to Chassis (0x4846)" in Block-2
                    if gfx_vbt.apply_changes() is False:
                        logging.error('VBT apply changes failed')
                    else:
                        # Restart Display driver for changes to take effect
                        status, reboot_required = display_essential.restart_gfx_driver()
                        if status is False:
                            logging.error('Failed to Restart Display driver')
                        logging.info('VBT apply changes passed')

                    # re flashing the vbt and restart
                    gfx_vbt.reload()
                    if(gfx_vbt.version >= 243):
                        logging.info("Pass : VBT version is {}.".format(gfx_vbt.version))
                    else:
                        self.fail("Fail : VBT version is {}".format(gfx_vbt.version))


        logging.info("\tSTEP : Verify HDCP on Non-HDCP Panels")
        if len(self.display_list) > 1:
            if self.multi_display_single_session(disable=False, is_negative=True):
                self.fail("HDCP is enabled on Non-HDCP Panels")
        else:
            if self.single_display_single_session(disable=False, is_negative=True):
                self.fail("HDCP is enabled on Non-HDCP Panel {}".format(displays[0]))
        logging.info("\tPASS : HDCP is not enabled on Non-HDCP Panels")

        ##
        # Report the EFP ConnectorType to DISPLAYPORT_EMBEDDED to skip HDCP when the EFP is the embedded display of AIO
        # Checking the connector type of port DP_B if VBT version is >= 243
        # Connector type for DP_B should come as DISPLAYPORT_EMBEDDED if VBT version >=243
        if gfx_vbt.version >= 243:
            for port,connector_type in port_connector_type.items():
                if port == 'DP_B' and connector_type == 'DISPLAYPORT_EMBEDDED':
                    logging.info("Pass : Connector type for port {} is {}".format(port,connector_type))
                elif port == 'DP_B' and connector_type != 'DISPLAYPORT_EMBEDDED':
                    self.fail("Fail : Connector type for port {} is {}".format(port,connector_type))

        # unplug external display
        for ext_panel in displays:
            logging.info("Step:Unplug display {}".format(ext_panel))
            if display_utility.unplug(ext_panel) is False:
                self.fail("Failed to unplug display {}".format(ext_panel))
            logging.info("Pass:{} display Unplug success".format(ext_panel))

        time.sleep(OPM_LITE_RE_INTIALIZE_DURATION)


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)