#######################################################################################################################
# @file         hdcp_power_event.py
# @brief        hdcp verification with power event
# @details      Test for verifying HDCP 1.4 & 2.2 activation/deactivation before & after TDR
#
# @author       chandrakanth Reddy y
#######################################################################################################################

from Libs.Core import display_essential
from Libs.Core.Verifier.common_verification_args import VerifierCfg, Verify
from Tests.HDCP.hdcp_base import *


##
# @brief        Contains HDCP tests with TDR
class HdcpTDR(HDCPBase):
    ##
    # @brief        Method to reboot the system with SD EDP
    # @return       None
    def test_reboot_with_Edp(self):
        ##
        # Set display configuration to SINGLE
        if self.display_config.set_display_configuration_ex(enum.SINGLE, [self.display_list[0]],
                                                            self.enumerated_displays) is False:
            self.fail("FAIL: Failed to apply SD on display {}".format(self.display_list[0]))

        if reboot_helper.reboot(self, 'test_after_reboot') is False:
            self.fail("Failed to reboot the system")

    ##
    # @brief        Method to verify HDCP after reboot with TDR
    # @return       None
    def test_after_reboot(self):
        logging.info("--------------------- HDCP & TDR verification After Reboot--------------------- ")
        ##
        # Set Display Configuration
        topology = eval("enum.%s" % (self.cmd_line_param['CONFIG']))
        if self.display_config.set_display_configuration_ex(topology,
                                                            self.display_list, self.enumerated_displays) is False:
            self.fail("Failed to apply display config {} on displays {} ".format(self.cmd_line_param['CONFIG'],
                                                                                 self.display_list))

        time.sleep(OPM_LITE_RE_INTIALIZE_DURATION)

        # get the HDCP display list
        display_count = [self.display_list.index(port) for port in self.display_list if
                         display_utility.get_vbt_panel_type(port, 'gfx_0') not in
                         [display_utility.VbtPanelType.LFP_DP, display_utility.VbtPanelType.LFP_MIPI]]
        status = False
        ##
        # Verify HDCP activation/deactivation
        logging.info("HDCP Verification started ....")
        if len(self.display_list) == 1:
            status = self.single_display_single_session()
        elif len(self.display_list) > 1:
            status = self.multi_display_single_session()

        if status is False:
            self.fail('HDCP verification failed')
        logging.info('HDCP verification passed successfully')

        VerifierCfg.tdr = Verify.SKIP
        logging.debug("Updated config under-run:{}, tdr:{}".format(VerifierCfg.underrun.name, VerifierCfg.tdr.name))
        ##
        # Generate TDR 3 times and verify HDCP
        for i in range(3):
            # Generate & Verify TDR
            if not display_essential.generate_tdr(gfx_index='gfx_0', is_displaytdr=True):
                self.fail('Iteration {} : Failed to generate TDR'.format(i + 1))
            if display_essential.detect_system_tdr(gfx_index='gfx_0') is True:
                logging.info('Iteration {} : TDR generated successfully'.format(i + 1))
            # Wait time for OPM to re-initialize the session
            time.sleep(OPM_LITE_RE_INTIALIZE_DURATION)

            ##
            # Verify HDCP Protection level
            if len(self.display_list) > 1:
                for port in display_count:
                    status = self.enable_hdcp(port)
            else:
                status = self.enable_hdcp()
            if status is False:
                self.fail('Iteration {} : HDCP Protection verification failed'.format(i + 1))
            logging.info('Iteration {} : HDCP verification passed successfully'.format(i + 1))
            time.sleep(HDCP_ENABLE_CHECK_DURATION)

        # disable HDCP
        if len(self.display_list) > 1:
            for port in display_count:
                status = self.disable_hdcp(port)
        else:
            status = self.disable_hdcp()
        if status is False:
            self.fail("HDCP Disable Failed")
        logging.info("HDCP Disable successful")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('HdcpTDR'))
    TestEnvironment.cleanup(outcome)
