#######################################################################################################################
# @file         hdcp_power_event.py
# @brief        hdcp verification with power event
# @details      Test verify HDCP 2.2 with attached 2.2 panel and Prompts user to remove HDCP 2.2 Panel
#               and plug HDCP 1.4 panel on same port and verify HDCP 1.4 after re-plug
#
# @author       chandrakanth Reddy y
#######################################################################################################################

from Tests.HDCP.hdcp_base import *


##
# @brief        Contains HDCP tests using North Gate
class HDCPUnplug(HDCPBase):
    ##
    # @brief runTest function of Unit Test FrameWork.
    # @return None
    def runTest(self):
        hdcp_type = None
        # Apply the configuration passed in cmdline
        topology = eval("enum.%s" % (self.cmd_line_param['CONFIG']))
        if self.display_config.set_display_configuration_ex(topology, self.display_list,
                                                            self.enumerated_displays) is False:
            self.fail("FAIL: Failed to apply display configuration {} on displays {}".
                      format(self.cmd_line_param['CONFIG'], self.display_list))

        time.sleep(OPM_LITE_RE_INTIALIZE_DURATION)
        external_displays = [port for port in self.display_list if display_utility.get_vbt_panel_type(port, 'gfx_0')
                             not in [display_utility.VbtPanelType.LFP_DP, display_utility.VbtPanelType.LFP_MIPI]]
        logging.info("\t STEP : Verify HDCP on {}".format(external_displays))
        if self.multi_display_single_session() is False:
            self.fail("HDCP verification Failed")
        logging.info("\tPASS : HDCP verification successful")

        alert.info("Please remove {} and Connect HDCP 1.4 Supported Panel".format(external_displays[0]))
        time.sleep(2)

        while True:
            enumerated_displays = self.display_config.get_enumerated_display_info()
            if disp_cfg.is_display_attached(enumerated_displays, external_displays[0]) is True:
                logging.info("{} PLUG Successful".format(external_displays[0]))
                break
            else:
                alert.error("{} display not connected. Please connect again".format(external_displays[0]))
        # Apply the configuration passed in cmdline
        topology = eval("enum.%s" % (self.cmd_line_param['CONFIG']))
        if self.display_config.set_display_configuration_ex(topology, self.display_list,
                                                            self.enumerated_displays) is False:
            self.fail("FAIL: Failed to apply display configuration {} on displays {}".
                      format(self.cmd_line_param['CONFIG'], self.display_list))

        time.sleep(OPM_LITE_RE_INTIALIZE_DURATION)

        for port in external_displays:
            # update protection level to HDCP 1.4 for HDCP 1.4 panel port
            if port == external_displays[0]:
                hdcp_type = self.hdcp_type
                self.hdcp_type = HDCPType.HDCP_1_4
            if self.enable_hdcp(port_id=self.display_list.index(port)) is False:
                self.fail("HDCP verification Failed for {}".format(port))
            if hdcp_type:
                # reset the protection level to previous HDCP protection level
                self.hdcp_type = hdcp_type
                hdcp_type = None
        logging.info("\tPASS : HDCP verification successful")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
