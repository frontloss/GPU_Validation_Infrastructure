######################################################################################
# @file         dp_sst_link_loss.py
# @brief        Verify whether link loss is triggered and re-link training is successful or not for DP SST config.
# @details      CommandLine: python dp_sst_link_loss.py <Display1 <SINK_<sinkName>> <dpcd_model<file_name> >
#               <Display2 <SINK_<sinkName> <dpcd_model_<fileName>> <Display3 .....> -iteration <> <-SIM/-EMU>
# Where param1 is main display and param2 is secondary displays and "-SIM" for Plug Mode.
# This test_script follows:
# 1. Hot Plug Display with link training data(Link Training data is Populated from xml)
# 2. Compare link training CR and EQ sequence from diana against expected value(populated from xml)
# 3. Clear DPCD Status register ( 0x00202, 0x00203, 0x00204), required to simulate link loss scenario
# 4. Trigger SPI, required to simulate link loss scenario
# 5. Wait for some time for panel to come up after re-link training.
# 6. Clear DPCD status register to fail re-link training (Optional)
# 7. Trigger SPI to simulate link loss once again (Optional)
# 8. Wait for some time for panel to come up after re-link training x2. (Optional)
# 9. Compare link training CR and EQ sequence from diana against expected value(populated from xml)
# 10. Follows same for other Displays
# 11. For iteration > 1, repeat step 1 to 6 as per iteration value
# @author       Ashish Kumar, Goutham N
######################################################################################

import logging
import os
import time
import Tests.Display_Port.DP_LinkTraining.display_link_training_base as disp_lt_base
from Libs.Core.sw_sim import driver_interface
from Libs.Core.wrapper import valsim_args
import Libs.Core.display_config.display_config as disp_conf
import Libs.Core.driver_escape as dri_escape
from Libs.Core.system_utility import SystemUtility
from Libs.Core.logger import gdhm


##
# @brief DpSstLinkLoss Class
class DpSstLinkLoss(disp_lt_base.DisplayLinkTrainingBase):

    ##
    # @brief    executes the actual test steps for DP SST Link Loss scenario.
    # @return   None
    def test_dp_sst_link_loss(self):
        """
        Description:
        This test step HotPlug and Unplug with link training data for given(input_display_list)
            display for given(iteration_count) iterations
        :return: None
        """
        logging.debug("Entry: test_dp_sst_link_loss()")
        diana_exe_path = os.path.join(disp_lt_base.test_context.SHARED_BINARY_FOLDER, "DiAna\\DiAna.exe")
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

            # Loop for iteration count provided in cmd line
            for counter in range(1, self.iteration_count + 1):
                logging.info("{0} Iteration Count: {1} for {2} {0}".format("*" * 20, counter, display_port))
                if display_port not in self.get_display_names().keys():
                    logging.info(
                        "STEP {} : Plugging Display on {} ".format(step_count, display_port))
                    step_count += 1

                    # Get xml file name
                    xml_file = self.get_xml_filename(display_port)
                    logging.debug("xml_file = {}".format(xml_file))
                    if xml_file is not None:
                        flt_xml_file = os.path.join(disp_lt_base.test_context.PANEL_INPUT_DATA_FOLDER,
                                                    'LINK_TRAINING_DATA',
                                                    xml_file)
                    else:
                        logging.error("[Test Issue]: xml input is not provided")
                        gdhm.report_test_bug_di(
                            title=f'[Interfaces][dp_sst_link_loss] xml input is not provided'
                        )
                        self.fail()

                    dp_dpcd_model_data = self.get_link_training_model_data(flt_xml_file)

                    dp_dpcd_model_data.uiPortNum = getattr(valsim_args.ValSimPort, display_port).value
                    dp_dpcd_model_data.eTopologyType = getattr(disp_lt_base.gfxvalsim.DpTopology, 'DPSST').value

                    panel_index = self.get_panel_index(display_port)
                    enum_display_dict = {}

                    # Plug Display
                    if disp_lt_base.disp_util.plug(port=display_port, panelindex=panel_index,
                                                   dp_dpcd_model_data=dp_dpcd_model_data):
                        enum_display_dict = self.get_display_names()
                        logging.info(
                            "STEP {} : Verifying Display Detection --> Display {} (Target ID : {}) Plug Successful".
                                format(step_count, display_port, enum_display_dict[display_port]))
                    else:
                        # Gdhm bug reporting handled in plug()
                        logging.error(
                            "STEP {} : Verifying Display Detection -->Display {} Plug Failed".
                                format(step_count, display_port))
                        result = False
                    step_count += 1
                    time.sleep(6)

                    # Stop etl and get the etl file path
                    etl_file_path = self.stop_etl_get_etl_file_path()

                    # Run diana on etl file and get log file
                    diana_log_file = None
                    if etl_file_path is not None:
                        diana_log_file = self.get_diana_file(diana_exe_path, etl_file_path)
                        logging.info("STEP {} : Get Diana Output file".format(step_count))
                    else:
                        # Gdhm bug reporting handled in get_diana_file()
                        logging.error("STEP {} : [Test Issue] Etl file generation failed".format(step_count))
                        result = False
                    step_count += 1

                    # Open media app and classicD3D app and perform link loss verification
                    for app in self.app_type:
                        # Skip video playback and classicD3D app in case of Presi environment
                        # as presi doesn't supports any of these.
                        execution_environment = SystemUtility().get_execution_environment_type()
                        is_pre_si_environment = True if execution_environment in ["SIMENV_FULSIM",
                                                                                  "SIMENV_PIPE2D"] else False
                        if not is_pre_si_environment:
                            app_instance = self.create_app_instance(app)
                            app_instance.open_app(is_full_screen=True, minimize=False)
                            ##
                            # Wait for app to stabilize
                            time.sleep(2)
                            logging.info(f"STEP {step_count}: {app} App is running successfully")
                            step_count += 1

                        # Get expected link training CR and EQ data from xml
                        link_training_exp_data = self.get_link_training_expected_data(flt_xml_file, display_port,
                                                                                      self.platform)

                        # Verify Expected link training CR and EQ sequence
                        if diana_log_file is not None:
                            if self.validate_link_training_sequence(diana_log_file, link_training_exp_data,
                                                                    display_port):
                                logging.info("STEP {} : Verifying Link Training CR and EQ sequence Successful".
                                             format(step_count))
                            else:
                                # Gdhm bug reporting handled in validate_link_training_sequence()
                                logging.error("STEP {} :  Verifying Link Training CR and EQ sequence Failed".
                                              format(step_count))
                                result = False
                        else:
                            logging.error("STEP {} : [Test Issue] Running Diana and getting the diana log failed".
                                          format(step_count))
                            gdhm.report_test_bug_di(
                                title=f'[Interfaces][dp_sst_link_loss] Running Diana and getting the diana log failed'
                            )
                            result = False
                        step_count += 1

                        # Start etl trace
                        if disp_lt_base.etl_tracer.start_etl_tracer() is False:
                            # Gdhm bug reporting handled in start_etl_tracer()
                            logging.error("[Test Issue]: Failed to start ETL Tracer")

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
                            gdhm.report_test_bug_di(
                                title=f'[Interfaces][dp_sst_link_loss] Display is not active on {display_port}'
                            )
                            result = False
                        else:
                            logging.info("Display is active before SPI on {}".format(display_port))

                        # Clear DPCD status Register
                        dpcd_offset = 0x00202
                        dpcd_status_data = [0x00, 0x00, 0x80]
                        flag = dri_escape.write_dpcd(enum_display_dict[display_port], dpcd_offset, dpcd_status_data)
                        if flag is True:
                            logging.info("DPCD Write on {0} for Offset: {1}".format(display_port, hex(dpcd_offset)))
                        else:
                            logging.error(
                                "Unable to write DPCD Data on {0} for Offset: {1}".format(display_port,
                                                                                          hex(dpcd_offset)))
                            gdhm.report_test_bug_di(
                                title=f'[Interfaces][dp_sst_link_loss] Unable to write DPCD Data on {display_port} for Offset: {hex(dpcd_offset)}'
                            )
                            result = False

                        # Trigger SPI
                        if driver_interface.DriverInterface().set_spi(gfx_adapter_dict[gfx_str], display_port,
                                                                      'NATIVE'):
                            logging.info(f'STEP {step_count} :SPI successfully triggered on display {display_port}')
                        else:
                            logging.error(f'STEP {step_count} : Failed to trigger SPI on display {display_port}')
                            gdhm.report_test_bug_di(
                                title=f'STEP {step_count} : Failed to trigger SPI on display {display_port}'
                            )
                            result = False
                        step_count += 1

                        # Sleep for some time for SPI and re-link training
                        time.sleep(8)

                        if self.fail_re_link_training:

                            # Clear DPCD status Register to fail re-link training and simulate link loss once again
                            flag = dri_escape.write_dpcd(enum_display_dict[display_port], dpcd_offset, dpcd_status_data)
                            if flag is True:
                                logging.info("DPCD Write on {0} for Offset: {1}".format(display_port, hex(dpcd_offset)))
                            else:
                                logging.error(
                                    "Unable to write DPCD Data on {0} for Offset: {1}".format(display_port,
                                                                                              hex(dpcd_offset)))
                                gdhm.report_test_bug_di(
                                    title=f'[Interfaces][dp_sst_link_loss] Unable to write DPCD Data on {display_port} for Offset: {hex(dpcd_offset)}'
                                )
                                result = False

                            # Trigger SPI
                            if driver_interface.DriverInterface().set_spi(gfx_adapter_dict[gfx_str], display_port,
                                                                          'NATIVE'):
                                logging.info(f'STEP {step_count} :SPI successfully triggered on display {display_port}')
                            else:
                                logging.error(f'STEP {step_count} : Failed to trigger SPI on display {display_port}')
                                gdhm.report_test_bug_di(
                                    title=f'STEP {step_count} : Failed to trigger SPI on display {display_port}'
                                )
                                result = False

                            # Sleep for some time for SPI and re-link training
                            time.sleep(8)

                        # compare ModeSet before and after SPI is triggered
                        curr_mode = display_config.get_current_mode(enum_display_dict[display_port])
                        if pre_mode != curr_mode:
                            logging.error("FAIL: ModeSet before({}x{}@{}Hz) and after({}x{}@{}Hz) SPI does not match"
                                          .format(pre_mode.HzRes, pre_mode.VtRes, pre_mode.refreshRate,
                                                  curr_mode.HzRes, curr_mode.VtRes, curr_mode.refreshRate))
                            gdhm.report_test_bug_di(
                                title=f'ModeSet before({pre_mode.HzRes}x{pre_mode.VtRes}@{pre_mode.refreshRate}Hz) and '
                                      f'after({curr_mode.HzRes}x{curr_mode.VtRes}@{curr_mode.refreshRate}Hz) SPI does not match'
                            )
                            result = False
                        else:
                            logging.info("PASS: ModeSet is same before({}x{}@{}Hz) and after({}x{}@{}Hz) the SPI "
                                         .format(pre_mode.HzRes, pre_mode.VtRes, pre_mode.refreshRate,
                                                 curr_mode.HzRes, curr_mode.VtRes, curr_mode.refreshRate))

                        # Checking if display is active or not after Re-link training
                        if disp_conf.is_display_active(display_port) is None or False:
                            logging.error("FAIL: Display is not active on {} after re-link training".format(display_port))
                            gdhm.report_test_bug_di(
                                title=f'Running Diana and getting the diana log failed'
                            )
                            result = False
                        else:
                            logging.info("PASS: Display is active on {} after re-link training".format(display_port))

                        if not is_pre_si_environment:
                            # Closing the app
                            logging.info(f'STEP {step_count} Closing {app} app..')
                            app_instance.close_app()
                            step_count += 1
                        else:
                            break

                    # UnPlug Display
                    logging.info("STEP {} : Un-Plugging Display on {}".format(step_count, display_port))
                    step_count += 1
                    if disp_lt_base.disp_util.unplug(port=display_port):
                        logging.info(
                            "STEP {} : Verifying Display Detection --> Display {} Unplug Successful".format(
                                step_count, display_port))
                    else:
                        # Gdhm bug reporting handled in disp_lt_base.disp_util.unplug()
                        logging.error(
                            "STEP {} : Verifying Display Detection --> Display {} Unplug Failed".format(
                                step_count, display_port))
                        result = False
                    step_count += 1
                    time.sleep(10)

                    # Stop etl and get the etl file path
                    etl_file_path = self.stop_etl_get_etl_file_path()

                    # Run diana on etl file and get log file
                    if etl_file_path is not None:
                        diana_log_file = self.get_diana_file(diana_exe_path, etl_file_path)
                        logging.info("STEP {} : Get Diana Output file".format(step_count))
                    else:
                        # Gdhm bug reporting handled in get_diana_file()
                        logging.error("STEP {} : [Test Issue] Etl file generation failed".format(step_count))
                        result = False
                    step_count += 1

                    # Verify Expected link training CR and EQ sequence
                    if diana_log_file is not None:
                        if self.validate_link_training_sequence(diana_log_file, link_training_exp_data,
                                                                display_port):
                            logging.info("STEP {} : After link loss, verifying re-link Training "
                                         "CR and EQ sequence Successful".format(step_count))
                        else:
                            # Gdhm bug reporting handled in validate_link_training_sequence()
                            logging.error("STEP {} : After link loss, verifying re-link Training "
                                          "CR and EQ sequence Failed".format(step_count))
                            result = False
                    else:
                        logging.error("STEP {} : [Test Issue] Running Diana and getting the diana log failed".
                                      format(step_count))
                        gdhm.report_test_bug_di(
                            title=f'[Interfaces][dp_sst_link_loss] Running Diana and getting the diana log failed'
                        )
                        result = False
                    step_count += 1

                    # Start etl trace
                    if disp_lt_base.etl_tracer.start_etl_tracer() is False:
                        # Gdhm bug reporting handled in start_etl_tracer()
                        logging.error("[Test Issue]: Failed to start ETL Tracer")

        if result is False:
            self.fail("DP SST link loss failure detected")
        logging.debug("Exit: dp_sst_link_loss()")

    ##
    # @brief    Teardown function that cleanups by unplugging EFP displays
    # @return   None
    def tearDown(self):
        logging.debug("ENTRY: TearDown")

        # Unplug all EFP displays
        logging.info("Unplugging all EFP Displays")
        enum_display_dict = self.get_display_names()

        for display_port in enum_display_dict.keys():
            if disp_lt_base.disp_util.get_vbt_panel_type(display_port, 'gfx_0') not in \
                    [disp_lt_base.disp_util.VbtPanelType.LFP_DP, disp_lt_base.disp_util.VbtPanelType.LFP_MIPI]:
                disp_lt_base.disp_util.unplug(port=display_port)

        logging.debug("EXIT: TearDown")


if __name__ == '__main__':
    disp_lt_base.TestEnvironment.initialize()
    outcome = disp_lt_base.unittest.TextTestRunner(verbosity=2).run(
        disp_lt_base.reboot_helper.get_test_suite('DpSstLinkLoss'))
    disp_lt_base.TestEnvironment.cleanup(outcome)
