#######################################################################################################################
# @file         hdcp_display_mode_change.py
# @brief        HDCP verification with display mode change
# @details      Test for verifying HDCP 1.4 & 2.2 activation & deactivation with the display resolution(Min/Mid/Max)
#               for all the display attached in the display config and verify the HDCP using OPM tool
#
# @author       Sridharan.V, Kumar Rohit, chandrakanth Reddy y
#######################################################################################################################

from Tests.HDCP.hdcp_base import *


##
# @brief        Contains HDCP tests with display mode change
class HDCPDisplayModeChange(HDCPBase):

    ##
    # @brief runTest function of Unit Test FrameWork.
    # @return None
    def runTest(self):
        status = False
        ##
        # Pruned modes dict will contain only the MIN, MID & MAX resolutions for all the display
        pruned_modes_dict = {}

        ##
        # target_list_modes[] is a list of target ids of all the displays used for applying modes
        target_list_modes = []

        # Apply the configuration passed in cmdline
        topology = eval("enum.%s" % (self.cmd_line_param['CONFIG']))
        if self.display_config.set_display_configuration_ex(topology, self.display_list,
                                                            self.enumerated_displays) is False:
            self.fail("FAIL: Failed to apply display configuration {} on displays {}".
                      format(self.cmd_line_param['CONFIG'], self.display_list))

        # wait for OPM Tool to re-initialize .
        time.sleep(OPM_LITE_RE_INTIALIZE_DURATION)

        # get the HDCP displays
        display_count = [self.display_list.index(port) for port in self.display_list if
                         display_utility.get_vbt_panel_type(port, 'gfx_0') not in
                         [display_utility.VbtPanelType.LFP_DP, display_utility.VbtPanelType.LFP_MIPI]]

        ##
        # Verify HDCP activation/deactivation
        logging.info("HDCP Verification started ....")
        if len(self.display_list) == 1:
            status = self.single_display_single_session()
        elif len(self.display_list) > 1:
            status = self.multi_display_single_session()

        if status is True:
            logging.info('PASS: HDCP verification passed successfully')

        ##
        # get the current display config from DisplayConfig
        config = self.display_config.get_current_display_configuration()
        if topology in [enum.EXTENDED, enum.SINGLE]:
            for index in range(config.numberOfDisplays):
                target_list_modes.append(config.displayPathInfo[index].targetId)
        else:
            target_list_modes.append(config.displayPathInfo[0].targetId)
        ##
        # supported_modes[] is a list of modes supported by the external display 
        supported_modes = self.display_config.get_all_supported_modes(target_list_modes, sorting_flag=True)
        for key, values in supported_modes.items():
            test_modes_list = list()
            test_modes_list.append(values[0])  # min
            test_modes_list.append(values[len(values) // 2])  # mid
            test_modes_list.append(values[-1])  # max

            pruned_modes_dict[key] = test_modes_list
        for key, values in pruned_modes_dict.items():

            for mode in values:
                # Apply mode one by one
                if self.display_config.set_display_mode([mode]) is False:
                    self.fail("FAIL: Failed to apply display mode {}. Exiting ...".format(mode))
                # wait for the OPM tool to get re-initialized
                time.sleep(OPM_LITE_RE_INTIALIZE_DURATION)
                # Verify HDCP Protection level
                if len(self.display_list) > 1:
                    for port in display_count:
                        if self.enable_hdcp(port) is False:
                            self.fail(" HDCP not Enabled on Port {}".format(port))
                else:
                    if self.enable_hdcp() is False:
                        self.fail(" HDCP not Enabled ")
                logging.info("PASS: HDCP verification passed successfully")
        #
        # wait for 30 sec before disable HDCP .
        # Some times link lost may occur after you enable HDCP due to link integrity check failure
        time.sleep(HDCP_ENABLE_CHECK_DURATION)

        logging.info(" STEP: Started HDCP Disable ")
        if len(self.display_list) > 1:
            for port in display_count:
                if self.disable_hdcp(port) is False:
                    self.fail(" HDCP not Disabled on port {} ".format(port))
                logging.info('PASS: HDCP Disabled successfully for port %r' % port)
        else:
            if self.disable_hdcp() is False:
                self.fail(" Failed to disable HDCP")
            logging.info(" PASS: HDCP Disabled Successfully")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
