######################################################################################
# @file         dp_sst_b2b_link_loss.py
# @brief        Verify if back to back  link loss is successful or not for DP SST config.
# @details      CommandLine: python dp_sst_b2b_link_loss.py <Display1 <SINK_<sinkName>>
#               <Display2 <SINK_<sinkName>  <Display3 .....> -iteration <>
# Where param1 is main display and param2 is secondary displays and "-SIM" for Plug Mode.
# This test_script follows:
# 1. Hot Plug Display
# 2. Clear DPCD Status register ( 0x00202, 0x00203, 0x00204), required to simulate link loss scenario
# 3. Trigger SPI, required to simulate link loss scenario and check if panel is plugged properly or not.
# 4. Run step 2 and 3 in loop without any delay 10 times
# 5. Follows same for other Displays
# @author       Ashish Kumar
######################################################################################

import logging
import time
import Tests.Display_Port.DP_LinkTraining.display_link_training_base as disp_lt_base
from Libs.Core.sw_sim import driver_interface
from Libs.Core.wrapper import valsim_args
import Libs.Core.display_config.display_config as disp_conf
import Libs.Core.driver_escape as dri_escape


##
# @brief DpSstB2BLinkLoss Class
class DpSstB2BLinkLoss(disp_lt_base.DisplayLinkTrainingBase):

    ##
    # @brief    executes the actual test steps for DP SST Link Loss scenario.
    # @return   None
    def test_dp_sst_b2b_link_loss(self):
        """
        Description:
        This test step HotPlug and trigger Link Loss scenario back to back for given(input_display_list) display
        :return: None
        """
        logging.debug("Entry: test_dp_sst_b2b_link_loss()")
        result = True

        # For loop for number of displays provided in command
        logging.info("Display list : {}".format(self.panel_info.keys()))
        logging.info("Input Display list: {}".format(self.input_display_list))
        for display_port in self.input_display_list:
            step_count = 1
            # Skip if display is internal
            if disp_lt_base.disp_util.get_vbt_panel_type(display_port, 'gfx_0') in \
                    [disp_lt_base.disp_util.VbtPanelType.LFP_DP, disp_lt_base.disp_util.VbtPanelType.LFP_MIPI]:
                logging.debug("Skipping : Internal Display {} is not Pluggable Display".format(display_port))
                continue
            else:
                if display_port not in self.get_display_names().keys():
                    logging.info(
                        "STEP {} : Plugging Display on {} ".format(step_count, display_port))
                    step_count += 1

                    panel_index = self.get_panel_index(display_port)
                    enum_display_dict = {}

                    # Plug Display
                    if disp_lt_base.disp_util.plug(port=display_port, panelindex=panel_index,
                                                   dp_dpcd_model_data=None):
                        enum_display_dict = self.get_display_names()
                        logging.info(
                            "STEP {} : Verifying Display Detection --> Display {} (Target ID : {}) Plug Successful".
                            format(step_count, display_port, enum_display_dict[display_port]))
                    else:
                        logging.error(
                            "STEP {} : Verifying Display Detection -->Display {} Plug Failed".
                            format(step_count, display_port))
                        result = False
                    step_count += 1
                    time.sleep(6)

                    # DPCD status Register are set to 0x00, Trigger SPI to simulating link loss scenario
                    display_config = disp_lt_base.DisplayConfiguration()

                    gfx_str = None
                    gfx_adapter_dict = {}

                    gfx_adapter_details = display_config.get_all_gfx_adapter_details()
                    for adapter_index in range(gfx_adapter_details.numDisplayAdapter):
                        gfx_str = str(gfx_adapter_details.adapterInfo[adapter_index].gfxIndex)
                        gfx_adapter_dict[gfx_str] = gfx_adapter_details.adapterInfo[adapter_index]

                    logging.debug("gfx index: {}".format(gfx_adapter_dict[gfx_str].gfxIndex))

                    pre_mode = display_config.get_current_mode(enum_display_dict[display_port])
                    if disp_conf.is_display_active(display_port) is None or False:
                        logging.error("Display is not active on {}".format(display_port))
                        result = False
                    else:
                        logging.info("Display is active before SPI on {}".format(display_port))

                    # Clear DPCD status Register
                    dpcd_offset = 0x00202
                    dpcd_status_data = [0x00, 0x00, 0x80]

                    logging.info("STEP {} : Trigger Link Loss 10 times".format(step_count))
                    step_count += 1
                    # Trigger Link Loss 10 times
                    for item in range(10):
                        flag = dri_escape.write_dpcd(enum_display_dict[display_port], dpcd_offset, dpcd_status_data)
                        if flag is True:
                            logging.info("Cleared DPCD Status Register Offset: {0} and trigger SPI".
                                         format(hex(dpcd_offset)))
                        else:
                            logging.error(
                                "Unable to Clear DPCD Data on {0} for Offset: {1}".format(display_port, hex(dpcd_offset)))
                            result = False

                        # Trigger SPI
                        driver_interface.DriverInterface().set_spi(gfx_adapter_dict[gfx_str], display_port, 'NATIVE')

                        # Sleep for some time for SPI and re-link training
                        time.sleep(6)

                        # compare ModeSet before and after SPI is triggered
                        curr_mode = display_config.get_current_mode(enum_display_dict[display_port])
                        if pre_mode != curr_mode:
                            logging.error("ModeSet before({}x{}@{}Hz) and after({}x{}@{}Hz) SPI does not match".format(
                                          pre_mode.HzRes, pre_mode.VtRes, pre_mode.refreshRate,
                                          curr_mode.HzRes, curr_mode.VtRes, curr_mode.refreshRate))
                            result = False
                        else:
                            logging.info("ModeSet is same before({}x{}@{}Hz) and after({}x{}@{}Hz) the SPI".format(
                                          pre_mode.HzRes, pre_mode.VtRes, pre_mode.refreshRate,
                                          curr_mode.HzRes, curr_mode.VtRes, curr_mode.refreshRate))

                        # Checking if display is active or not after Re-link training
                        if disp_conf.is_display_active(display_port) is None or False:
                            logging.error("Display is not active on {} after link Loss".format(display_port))
                            result = False
                        else:
                            logging.debug("Display came up and active on {} after link loss".format(display_port))

        if result is False:
            self.fail("DP SST B2B link loss failure detected")
        logging.debug("Exit: dp_sst_b2b_link_loss()")

    ##
    # @brief    Teardown function that cleanups by unplugging EFP displays
    # @return   None
    def tearDown(self):
        logging.debug("ENTRY: TearDown")

        # Unplug all EFP displays
        logging.debug("Unplugging all Displays")
        enum_display_dict = self.get_display_names()

        for display_port in enum_display_dict.keys():
            if disp_lt_base.disp_util.get_vbt_panel_type(display_port, 'gfx_0') not in \
                    [disp_lt_base.disp_util.VbtPanelType.LFP_DP, disp_lt_base.disp_util.VbtPanelType.LFP_MIPI]:
                disp_lt_base.disp_util.unplug(port=display_port)

        logging.debug("EXIT: TearDown")


if __name__ == '__main__':
    disp_lt_base.TestEnvironment.initialize()
    outcome = disp_lt_base.unittest.TextTestRunner(verbosity=2).run(
        disp_lt_base.reboot_helper.get_test_suite('DpSstB2BLinkLoss'))
    disp_lt_base.TestEnvironment.cleanup(outcome)
