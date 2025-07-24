######################################################################################
# @file         test_vbt_maxlinkrate_limit_override.py
# @brief        Validate Maxlinkrate Override in VBT for any display port
# @details      Displays are external displays dp_b, dp_c, hdmi_b, hdmi_c, etc
# @author       Veluru, Veena
######################################################################################

from Libs.Core import enum
from Libs.Core import display_utility, driver_escape
from Libs.Core.test_env import test_environment
from Libs.Feature.display_port import dpcd_helper
from Tests.VBT_Overrides.vbt_override_base import *

# vbt linkrate map
vbt_dp_linkrate_mapping = {
    'Default': (0b000, 0),
    'RBR': (0b001, 1.62),
    'HBR1': (0b010, 2.7),
    'HBR2': (0b011, 5.4),
    'HBR3': (0b100, 8.1),
    'UHBR': (0b101, 10),
    'UHBR2': (0b110, 13.5),
    'UHBR3': (0b111, 20),
}

# panel linkrate map
panel_linkrate_mapping = [
    ('Default', 0b0, 0),
    ('RBR', 0x6, 1.62),
    ('HBR1', 0xa, 2.7),
    ('HBR2', 0x14, 5.4),
    ('HBR3', 0x1E, 8.1),
    ('UHBR', 0x1, 10),
    ('UHBR2', 0x4, 13.5),
    ('UHBR3', 0x2, 20),
]
##
# @brief        TestVbtMaxLinkRateOverride base class : To be used in VBT Override tests
class TestVbtMaxLinkRateOverride(VbtOverrideBase):
    reset_vbt_values = []
    ##
    # @brief        test vbt max linkrate
    # @return       None
    def test_vbt_maxlinkrate(self):
        logging.debug("Entry: TestVbtMaxLinkRateOverride()")
        for display_port, gfx_index in zip(self.input_display_list, self.gfx_adapter_list):
            # Ignore HPD request for Internal Displays
            if display_utility.get_vbt_panel_type(display_port, gfx_index) in \
                    [display_utility.VbtPanelType.LFP_DP, display_utility.VbtPanelType.LFP_MIPI]:
                logging.debug("Skipping : Internal Display {} is not Pluggable Display".format(display_port))
                continue

            logging.info("Pre-Step : Get EFP support and index in VBT Block2 for {}".format(display_port))
            status, index = self.get_port_status_vbt(display_port)
            if status is True:
                logging.info("STEP 1 : Get current max Link rate defined for the mapped EFP and override with linkrate user requested to set".format(index))
                self.assertTrue(self.vbt_override_linkrate(index), "Step1 Failed")

                if self.cmd_line_param['PLUG_TOPOLOGIES'] == 'NONE':
                    logging.info("STEP 2 : Plug Display on {}".format(display_port))
                    self.assertTrue(display_utility.plug_display(display_port, self.cmd_line_param), "Step2 Failed")
                else:
                    logging.info("STEP 2 : Plug MST Display on {}".format(display_port))
                    self.assertTrue(self.plug_mst_topologies(), "Step2 Failed")

                logging.info("STEP 3: Set single display configuration on {}".format(display_port))
                self.assertTrue(self.config.set_display_configuration_ex(enum.SINGLE, [display_port]), "Step3 Failed")

                logging.info("STEP 4: Verify Linkrate set for {}".format(display_port))
                self.assertTrue(self.verify_programmed_linkrate(index, display_port, gfx_index), "Step4 Failed")


    ##
    # @brief        This method overrides DP Max linkrate in vbt for particular index
    # @param[in]    index - EFP panel index from VBT block 2
    # @return       None
    def vbt_override_linkrate(self, index):
        if self.restrict_linkrate[0] in vbt_dp_linkrate_mapping.keys():
            link_rate_info = vbt_dp_linkrate_mapping[self.restrict_linkrate[0]]
            logging.info("Requested Linkrate found in VBT mapping table{}".format(link_rate_info[0]))
            vbt_dp_max_lr = self.gfx_vbt.block_2.DisplayDeviceDataStructureEntry[index].DpMaxLinkRate
            logging.info("Default linkrate programmed in VBT {}".format(vbt_dp_max_lr, ))
            self.reset_vbt_values.append(vbt_dp_max_lr)
            # restrict vbt DP max linkrate field to the value passed in cmdline
            vbt_dp_max_lr = vbt_dp_max_lr & 0 | link_rate_info[0]
            logging.info("Linkrate to be programed in VBT ({}, {})".format(vbt_dp_max_lr, self.restrict_linkrate[0]))
            self.gfx_vbt.block_2.DisplayDeviceDataStructureEntry[index].DpMaxLinkRate = vbt_dp_max_lr

        return self.push_vbt_change()

    ##
    # @brief        This method verifies programmed linkrate against vbt set value
    # @param[in]    index - EFP panel index from VBT block 2
    # @param[in]    display Display.
    # @param[in]    gfx_index graphics adapter
    # @return       None
    def verify_programmed_linkrate(self, index, display, gfx_index = 'gfx_0'):
        display_and_adapter_info = display_config.DisplayConfiguration().get_display_and_adapter_info_ex(display,
                                                                                                         gfx_index)
        linkrate_trained = dpcd_helper.DPCD_getLinkRate(display_and_adapter_info)
        vbt_programmed_lr = 0

        # read max supported panel linkrate
        panel_max_lr = dpcd_helper.DPCD_getPanelMaxLinkRate(display_and_adapter_info)
        logging.info("Panel max supported linkrate {}".format(panel_max_lr))

        dp_max_linkrate_vbt = self.gfx_vbt.block_2.DisplayDeviceDataStructureEntry[index].DpMaxLinkRate
        for lr_value in vbt_dp_linkrate_mapping.values():
            if dp_max_linkrate_vbt == lr_value[0]:
                vbt_programmed_lr = lr_value[1]
        self.assertTrue(panel_max_lr >= vbt_programmed_lr, "VBT set linkrate {} exceeds max panel supported linkrate {}".format(dp_max_linkrate_vbt, panel_max_lr))

        logging.info("DP max link rate from VBT: {} Driver trained Link Rate: {}".format(vbt_programmed_lr, linkrate_trained))
        if linkrate_trained <= vbt_programmed_lr:
            logging.info("PASS: Linkrate trained {} is not greater than the max link rate set in the VBT {} for {}".format(
                linkrate_trained, vbt_programmed_lr, display))
            return True
        else:
            gdhm.report_bug(
                title="[Interfaces][VBT_Override]: Linkrate trained is greater than vbt set linkrate",
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.error(
                "ERROR: Linkrate trained {} is greater than the max vbt link rate set {} for the display {}".format(
                    linkrate_trained, vbt_programmed_lr, display))
            return False

    ##
    # @brief        Teardown method to reset vbt values
    # @return None
    def tearDown(self):

        # call base class teardown
        super(TestVbtMaxLinkRateOverride, self).tearDown()

        for display_port, gfx_index, reset_dp_lr_max in zip(self.input_display_list, self.gfx_adapter_list, self.reset_vbt_values):
            status, index = self.get_port_status_vbt(display_port)
            self.gfx_vbt.block_2.DisplayDeviceDataStructureEntry[index].DpMaxLinkRate = reset_dp_lr_max

        self.push_vbt_change()

        logging.info('Reset VBT passed')
        logging.info("Test Completed")
        logging.debug("EXIT: TearDown")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('TestVbtMaxLinkRateOverride'))
    test_environment.TestEnvironment.cleanup(outcome)
