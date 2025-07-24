######################################################################################
# @file         plug_unplug_with_link_training.py
# @brief        Validate Hotplug and Hotunplug by passing link training data populated from XML file.
# @details      CommandLine: python plug_unplug_with_link_training.py <Display1 <SINK_<sinkName>> <dpcd_model<file_name> >
#               <Display2 <SINK_<sinkName> <dpcd_model_<fileName>> <Display3 .....> -iteration <> <-SIM/-EMU>
# Where param1 is main display and param2 is secondary displays and "-SIM" for Plug Mode.
# This test_script follows:
# 1. Hot Plug Display with link training data(Link Training data is Populated from xml)
# 2. Unplug Display
# 3. Stop ETL, run diana on etl log and get diana log
# 4. Compare link training CR and EQ sequence from diana against expected value(populated from xml)
# 5. Follows same for other Displays
# 6. For iteration > 1, repeat step 1 to 5 as per iteration value
# @author       Ashish Kumar
######################################################################################

import logging
import os
import time
from Libs.Core import enum
from Libs.Core.wrapper.valsim_args import ValSimPort
import Libs.Core.display_config.display_config as disp_conf
from Libs.Core.logger import gdhm
import Tests.Display_Port.DP_LinkTraining.display_link_training_base as disp_lt_base


##
# @brief PlugUnplugWithLinkTraining Class
class PlugUnplugWithLinkTraining(disp_lt_base.DisplayLinkTrainingBase):

    ##
    # @brief    executes the actual test steps for plug unplug with link training data scenario.
    # @return   None
    def test_plug_unplug_with_link_training(self):
        """
        Description:
        This test step HotPlug and Unplug with link training data for given(input_display_list)
            display for given(iteration_count) iterations
        :return: None
        """
        logging.debug("Entry: test_plug_unplug_with_link_training()")
        diana_exe_path = os.path.join(disp_lt_base.test_context.SHARED_BINARY_FOLDER, "DiAna\\DiAna.exe")
        result = True

        # Loop for number of displays provided in command
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
                # Loop for iteration count provided in cmd line
                for counter in range(1, self.iteration_count + 1):
                    logging.info("{0} Iteration Count: {1} for {2} {0}".format("*" * 20, counter, display_port))
                    if display_port not in self.get_display_names().keys():
                        logging.info(
                            "STEP {} : Plugging Display on {} with Link Training".format(step_count, display_port))
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
                            gdhm.report_bug(
                                title="[Interfaces][DP_LT] Invalid XML filename provided in the cmd",
                                problem_classification=gdhm.ProblemClassification.OTHER,
                                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                                priority=gdhm.Priority.P2,
                                exposure=gdhm.Exposure.E2
                            )
                            self.fail()

                        dp_dpcd_model_data = self.get_link_training_model_data(flt_xml_file)

                        dp_dpcd_model_data.uiPortNum = getattr(ValSimPort, display_port).value
                        dp_dpcd_model_data.eTopologyType = getattr(disp_lt_base.gfxvalsim.DpTopology, 'DPSST').value

                        panel_index = self.get_panel_index(display_port)

                        # Plug Display
                        if disp_lt_base.disp_util.plug(port=display_port, panelindex=panel_index,
                                                       dp_dpcd_model_data=dp_dpcd_model_data):
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

                        # Checking if display is active or not
                        enumerated_displays = self.config.get_enumerated_display_info()
                        config_displays = [enumerated_displays.ConnectedDisplays[index].DisplayAndAdapterInfo for index
                                           in range(enumerated_displays.Count)]
                        if self.config.set_display_configuration_ex(
                                enum.EXTENDED if len(config_displays) > 1 else enum.SINGLE,
                                config_displays, enumerated_displays) is False:
                            self.fail("SetDisplayConfigurationEX returned false")
                        if disp_conf.is_display_active(display_port) is None or False:
                            logging.error(
                                "FAIL: Display is not active on {}".format(display_port))
                            self.fail("FAIL: Display is not active on {}".format(display_port))
                        else:
                            logging.info("PASS: Display is active on {}".format(display_port))

                        # UnPlug Display
                        logging.info("STEP {} : Un-Plugging Display on {}".format(step_count, display_port))
                        step_count += 1
                        if disp_lt_base.disp_util.unplug(port=display_port):
                            logging.info(
                                "STEP {} : Verifying Display Detection --> Display {} Unplug Successful".format(
                                    step_count, display_port))
                        else:
                            logging.error(
                                "STEP {} : Verifying Display Detection --> Display {} Unplug Failed".format(
                                    step_count, display_port))
                            result = False
                        time.sleep(10)

                        # Stop etl and get the etl file path
                        etl_file_path = self.stop_etl_get_etl_file_path()

                        # Run diana on etl file and get log file
                        step_count += 1
                        diana_log_file = None
                        if etl_file_path is not None:
                            diana_log_file = self.get_diana_file(diana_exe_path, etl_file_path)
                            logging.info("STEP {} : Get Diana Output file".format(step_count))
                        else:
                            logging.error("STEP {} : [Test Issue] Etl file generation failed".format(step_count))
                            # Gdhm bug reporting handled in stop_etl_get_etl_file_path
                            result = False

                        # Get expected link training CR and EQ data from xml
                        link_training_exp_data = self.get_link_training_expected_data(flt_xml_file, display_port,
                                                                                      self.platform)

                        # Verify Expected link training CR and EQ sequence
                        step_count += 1
                        if diana_log_file is not None:
                            if self.validate_link_training_sequence(diana_log_file, link_training_exp_data,
                                                                    display_port):
                                logging.info("STEP {} : Verifying Link Training CR and EQ sequence Successful".
                                             format(step_count))
                            else:
                                # Gdhm bug reporting handled in validate_link_training_sequence
                                logging.error("STEP {} :  Verifying Link Training CR and EQ sequence Failed".
                                              format(step_count))
                                result = False
                        else:
                            # Gdhm bug reporting handled in get_diana_file
                            logging.error("STEP {} : [Test Issue] Running Diana and getting the diana log failed".
                                          format(step_count))
                            result = False

                        # Start etl trace
                        if disp_lt_base.etl_tracer.start_etl_tracer() is False:
                            # Gdhm bug reporting handled in start_etl_tracer
                            logging.error("[Test Issue]: Failed to start ETL Tracer")

        if result is False:
            self.fail("Plug/Unplug with Link Training failure detected")
        logging.debug("Exit: test_plug_unplug_with_link_training()")

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
        disp_lt_base.reboot_helper.get_test_suite('PlugUnplugWithLinkTraining'))
    disp_lt_base.TestEnvironment.cleanup(outcome)
