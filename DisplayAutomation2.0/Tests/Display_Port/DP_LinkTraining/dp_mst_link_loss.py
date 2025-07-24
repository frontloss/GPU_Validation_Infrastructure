################################################################################################################
# @file         dp_mst_link_loss.py
# @brief        Verify whether link loss is triggered and re-link training is successful or not for DP MST config.
# @details      commandline: python.exe dp_mst_link_loss.py \<portName> -PLUG_TOPOLOGIES \<topology name>
#               e.g. dp_mst_link_loss.py -EDP_A -DP_B -PLUG_TOPOLOGIES MST_LT_1B1M
# This test_script follows:
# 1. Hot Plug MST Hub/Display with link training data(Link Training data is Populated from xml)
# 2. Verify if MST plug is successful and display is up.
# 2. Compare link training CR and EQ sequence from diana against expected value(populated from xml)
# 3. Clear DPCD Status register ( 0x00202, 0x00203, 0x00204), required to simulate link loss scenario
# 4. Trigger SPI, required to simulate link loss scenario
# 5. Wait for some time(8 seconds) for MST display to come up after re-link training.
# 6. Check if MST Display is Active or not, Modeset is same as before(pre SPI) or not.
# 7. Compare link training CR and EQ sequence from diana against expected value(populated from xml)
# @author       Ashish Kumar
################################################################################################################

import sys
import os

from Libs.Core.sw_sim import driver_interface
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Display_Port.DP_MST.display_port_mst_base import *
import xml.etree.ElementTree as xml_ET
from Tests.Display_Port.DP_LinkTraining.display_link_training_base import DisplayLinkTrainingBase
from Libs.Core.test_env import test_context
from Libs.Core.logger import etl_tracer
import Libs.Core.display_config.display_config as disp_conf
import Libs.Core.driver_escape as dri_escape
from Libs.Core.system_utility import SystemUtility

##
# @brief DpMstLinkLoss Class
class DpMstLinkLoss(DisplayPortMSTBase):

    ##
    # @brief    executes the actual test steps for DP MST Link Loss scenario.
    # @return   None
    def runTest(self):
        # Variable for DP Port Number Index
        dp_port_index = 0
        step_count = 1
        result = True
        diana_exe_path = os.path.join(test_context.SHARED_BINARY_FOLDER, "DiAna\\DiAna.exe")
        dp_lt_base = DisplayLinkTrainingBase()
        app_type = ['MEDIA', 'CLASSICD3D']

        # Requested ports should be present in free port list
        if not set(self.dp_ports_to_plug).issubset(set(self.free_port_list)):
            logging.error("[Test Issue]: Not Enough free ports available. Exiting....")
            gdhm.report_bug(
                title="[Interfaces][DP_MST] Requested ports not present in free port list",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            self.fail()

        # Get the port type from available free DP ports
        port_type = self.get_dp_port_from_availablelist(dp_port_index)

        # Get Topology Type(MST/SST) from the command line
        topology_type = self.get_topology_type(dp_port_index)

        # Get Topology XML file from command line
        xml_file = self.get_xmlfile(dp_port_index)

        # Get Platform name
        platform = self.get_platform_name()

        # Read xml File and get dpcd model file
        if not os.path.exists(xml_file):
            logging.error("[Test Issue]: {} not found".format(xml_file))
            gdhm.report_bug(
                title="[Interfaces][DP_LT] Topology xml is not found",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            self.fail()

        xml_path = open(xml_file, 'r')
        line = xml_path.readline()
        dpcd_model_file = None
        if line.startswith('<?xml'):
            data = '<MST>' + xml_path.read() + '</MST>'
            xml_root = xml_ET.fromstring(data)
            root_iter = 0
            for child in xml_root:
                if child.tag == 'DPCDModel':
                    try:
                        dpcd_model_file = xml_root[root_iter][0].text
                        logging.debug("DPCD Model file: {}".format(xml_root[root_iter][0].text))
                    except IndexError:
                        logging.error("Index Out of Range")
                        dpcd_model_file = None
                root_iter = root_iter + 1
        if dpcd_model_file is not None:
            flt_xml_file = os.path.join(test_context.PANEL_INPUT_DATA_FOLDER,
                                        'LINK_TRAINING_DATA',
                                        dpcd_model_file)
        else:
            logging.error("[Test Issue]: DPCD model file is not provided in topology xml")
            gdhm.report_bug(
                title="[Interfaces][DP_LT] DPCD model file is not provided in topology xml",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            self.fail()

        # Function call to set DP1.2 topology
        logging.info(f'STEP {step_count} : Plugging Display in MST on {port_type}')
        step_count += 1
        self.setnverifyMST(port_type, topology_type, xml_file)

        display_and_adapter_info_list = self.get_current_display_and_adapter_info_list(is_lfp_info_required=False)
        no_of_displays = len(display_and_adapter_info_list)

        # WA: HSD-15015314084;
        # Apply single display config. on external panel, Since we do a set display config (EDP) as part of tear down, so in the next test, the state will be persisted from SV3 OS onwards. .
        logging.info("Applying single display config. on external panel")
        if no_of_displays == 1:
            is_success = self.display_config.set_display_configuration_ex(enum.SINGLE, display_and_adapter_info_list)
            self.assertTrue(is_success, "Set Display Configuration Single (External panel) Failed")

        # Stop etl and get the etl file path
        etl_file_path = dp_lt_base.stop_etl_get_etl_file_path()

        enum_display_dict = dp_lt_base.get_display_names()
        logging.info(
            f'STEP {step_count} :Verifying Display Detection --> Display : {port_type} (Target ID '
            f': {enum_display_dict[port_type]}) Plug Successful')
        step_count += 1

        # Run diana on etl file and get log file
        diana_log_file = None
        if etl_file_path is not None:
            diana_log_file = dp_lt_base.get_diana_file(diana_exe_path, etl_file_path)
            logging.debug(f'STEP {step_count} : Diana Output file: {diana_log_file}')
        else:
            logging.error(f'STEP {step_count} : [Test Issue] Etl file generation failed')
            # Gdhm bug reporting handled in stop_etl_get_etl_file_path
            result = False
        step_count += 1

        # Get expected link training CR and EQ data from xml
        link_training_exp_data = dp_lt_base.get_link_training_expected_data(flt_xml_file, port_type, platform)

        # Verify Expected link training CR and EQ sequence
        if diana_log_file is not None:
            if dp_lt_base.validate_link_training_sequence(diana_log_file, link_training_exp_data, port_type):
                logging.info(f'STEP {step_count} : Verifying Link Training CR and EQ sequence Successful')
            else:
                # Gdhm bug reporting handled in validate_link_training_sequence
                logging.error(f'STEP {step_count} : Verifying Link Training CR and EQ sequence Failed')
                result = False
        else:
            # Gdhm bug reporting handled in get_diana_file
            logging.error(f'STEP {step_count} : [Test Issue] Running Diana and getting the diana log failed')
            result = False
        step_count += 1

        # Open media app and classicD3D app and perform link loss verification
        for app in app_type:
            # Skipping video playback and classicD3D app in case of Presi environment
            # as presi doesn't supports any of these.
            execution_environment = SystemUtility().get_execution_environment_type()
            is_pre_si_environment = True if execution_environment in ["SIMENV_FULSIM",
                                                                      "SIMENV_PIPE2D"] else False
            if not is_pre_si_environment:
                app_instance = dp_lt_base.create_app_instance(app)
                app_instance.open_app(is_full_screen=True, minimize=False)
                ##
                # Wait for app to stabilize
                time.sleep(2)
                logging.info(f"STEP {step_count}: {app} App is running successfully")
                step_count += 1

            # Start etl trace
            if etl_tracer.start_etl_tracer() is False:
                # Gdhm bug reporting handled in start_etl_tracer
                logging.error("[Test Issue]: Failed to start ETL Tracer")

            # DPCD status Register are set to 0x00, Trigger SPI to simulating link loss scenario
            display_conf = disp_conf.DisplayConfiguration()

            gfx_str = None
            gfx_adapter_dict = {}

            gfx_adapter_details = display_conf.get_all_gfx_adapter_details()
            for adapter_index in range(gfx_adapter_details.numDisplayAdapter):
                gfx_str = str(gfx_adapter_details.adapterInfo[adapter_index].gfxIndex)
                gfx_adapter_dict[gfx_str] = gfx_adapter_details.adapterInfo[adapter_index]

            logging.debug("gfx index: {}".format(gfx_adapter_dict[gfx_str].gfxIndex))

            pre_mode = display_conf.get_current_mode(enum_display_dict[port_type])
            if disp_conf.is_display_active(port_type) is None or False:
                logging.error("Display is not active on {}".format(port_type))
                gdhm.report_test_bug_di(
                    title=f'[Interfaces][dp_mst_link_loss] Display is not active on {port_type}'
                )
                result = False
            else:
                logging.info("Display is active before SPI on {}".format(port_type))

            # Clear DPCD status Register
            dpcd_offset = 0x00202
            dpcd_status_data = [0x00, 0x00, 0x80]
            flag = dri_escape.write_dpcd(enum_display_dict[port_type], dpcd_offset, dpcd_status_data)
            if flag is True:
                logging.info("DPCD Write on {0} for Offset: {1}".format(port_type, hex(dpcd_offset)))
            else:
                logging.error("Unable to write DPCD Data on {0} for Offset: {1}".format(port_type, hex(dpcd_offset)))
                gdhm.report_test_bug_di(
                    title=f'[Interfaces][dp_mst_link_loss] Unable to write DPCD Data on {port_type} for Offset: {hex(dpcd_offset)}'
                )
                result = False

            # Trigger SPI
            if driver_interface.DriverInterface().set_spi(gfx_adapter_dict[gfx_str], port_type, 'NATIVE'):
                logging.info(f'STEP {step_count} :SPI successfully triggered on display {port_type}')
            else:
                logging.error(f'STEP {step_count} : Failed to trigger SPI on display {port_type}')
                gdhm.report_test_bug_di(
                    title=f'[Interfaces][dp_mst_link_loss] Failed to trigger SPI on display {port_type}'
                )
                result = False
            step_count += 1

            # Sleep for some time for SPI and re-link training
            time.sleep(8)

            # compare ModeSet before and after SPI is triggered
            curr_mode = display_conf.get_current_mode(enum_display_dict[port_type])
            if pre_mode != curr_mode:
                logging.error("FAIL: ModeSet before({}x{}@{}Hz) and after({}x{}@{}Hz) SPI does not match".format(
                    pre_mode.HzRes, pre_mode.VtRes, pre_mode.refreshRate,
                    curr_mode.HzRes, curr_mode.VtRes, curr_mode.refreshRate))
                gdhm.report_test_bug_di(
                    title=f'ModeSet before({pre_mode.HzRes}x{pre_mode.VtRes}@{pre_mode.refreshRate}Hz) and '
                          f'after({curr_mode.HzRes}x{curr_mode.VtRes}@{curr_mode.refreshRate}Hz) SPI does not match'
                )
                result = False
            else:
                logging.info("PASS: ModeSet is same before({}x{}@{}Hz) and after({}x{}@{}Hz) the SPI".format(
                    pre_mode.HzRes, pre_mode.VtRes, pre_mode.refreshRate,
                    curr_mode.HzRes, curr_mode.VtRes, curr_mode.refreshRate))

            # Checking if display is active or not after Re-link training
            if disp_conf.is_display_active(port_type) is None or False:
                logging.error("Display is not active on {} after re-link training".format(port_type))
                gdhm.report_test_bug_di(
                    title=f'Display is not active on {port_type} after re-link training'
                )
                result = False
            else:
                logging.info("Display is active on {} after re-link training".format(port_type))

            # Stop etl and get the etl file path
            etl_file_path = dp_lt_base.stop_etl_get_etl_file_path()

            # Run diana on etl file and get log file
            if etl_file_path is not None:
                diana_log_file = dp_lt_base.get_diana_file(diana_exe_path, etl_file_path)
                logging.info(f'STEP {step_count} : Get Diana Output file')
            else:
                # Gdhm bug reporting handled in get_diana_file()
                logging.error(f'STEP {step_count} : [Test Issue] Etl file generation failed')
                result = False
            step_count += 1

            # Verify Expected link training CR and EQ sequence
            if diana_log_file is not None:
                if dp_lt_base.validate_link_training_sequence(diana_log_file, link_training_exp_data, port_type):
                    logging.info(f'STEP {step_count} : After link loss, verifying re-link Training CR and EQ sequence '
                                 f'Successful')
                else:
                    # Gdhm bug reporting handled in validate_link_training_sequence()
                    logging.error(f'STEP {step_count} : After link loss, verifying re-link Training CR and EQ sequence '
                                  f'Failed')
                    result = False
            else:
                logging.error(f'STEP {step_count} : [Test Issue] Running Diana and getting the diana log failed')
                gdhm.report_test_bug_di(
                    title=f'Running Diana and getting the diana log failed'
                )
                result = False
            step_count += 1

            # Start etl trace
            if etl_tracer.start_etl_tracer() is False:
                # Gdhm bug reporting handled in start_etl_tracer()
                logging.error("[Test Issue]: Failed to start ETL Tracer")

            if result is False:
                self.fail(f"DP MST link loss failure detected")
            logging.debug("Exit: dp_mst_link_loss()")

            if not is_pre_si_environment:
                # Closing the app
                logging.info(f'STEP {step_count} Closing {app} app..')
                app_instance.close_app()
                step_count += 1
            else:
                break


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
