########################################################################################################################
# @file         virtual_display_yangra_base.py
# @brief        The script implements unittest default functions for setUp and tearDown, and common test functions given below:
#              * Verify Virtual Display is enabled properly in Headless mode
#              * Verify Number of VideoPresentSources are reported correctly
#              * Helper function to Start/Stop ETL capture, Enable/Disable VirtualCRTSupport Registry
# @author       Prateek Joshi
########################################################################################################################

import logging
import os
import sys
import unittest

from Libs.Core import cmd_parser, display_utility, enum, etl_parser, registry_access, display_essential
from Libs.Core.display_config import display_config
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE
from Libs.Core.logger import etl_tracer, gdhm
from Libs.Core.machine_info import machine_info
from Libs.Core.test_env import test_context
from Libs.Feature.crc_and_underrun_verification import UnderRunStatus

LINE_WIDTH = 64
ETL_PARSER_CONFIG = etl_parser.EtlParserConfig()
ETL_PARSER_CONFIG.commonData = 1
PLATFORM_NAME = machine_info.SystemInfo().get_gfx_display_hardwareinfo()[0].DisplayAdapterName
SKU_NAME = machine_info.SystemInfo().get_gfx_display_hardwareinfo()[0].SkuName
VIDPNSOURCE_3 = ['ICLLP', 'RKL', 'JSL', 'ADLN', 'LNL']
VIDPNSOURCE_4 = ['ICLHP', 'LKF1', 'TGL', 'ADLP', 'ADLS', 'MTL', 'PTL']


##
# @brief  Base class for virtual display yangra tests
class VirtualDisplayYangraBase(unittest.TestCase):
    enumerated_displays = None
    connected_list = []
    plugged_display = []
    display_config = display_config.DisplayConfiguration()
    underrun_status = UnderRunStatus()

    ##
    # @brief       Unittest Setup function
    # @param[in]   self; Object of virtual display yangra base class
    # @return      void
    def setUp(self):
        logging.info(" TEST STARTS ".center(LINE_WIDTH, "*"))
        logging.info(" SETUP: VIRTUAL_DISPLAY_BASE ".center(LINE_WIDTH, "*"))
        self.cmd_line_param = cmd_parser.parse_cmdline(sys.argv)

        for key, value in self.cmd_line_param.items():
            if cmd_parser.display_key_pattern.match(key) is not None:
                if value['connector_port'] is not None:
                    self.connected_list.insert(value['index'], value['connector_port'])

        # Verify Virtual Display
        if self.verify_headless_virtual_display() is False:
            logging.warning(f" System is not in headless configuration hence Virtual Display is not enumerated, "
                            f"display enumerated details: {self.log_enumerated_status}")
        else:
            logging.info("Successfully verified virtual display in headless mode")

        # Plug the display
        self.plugged_display, self.enumerated_displays = display_utility.plug_displays(self, self.cmd_line_param)
        logging.info("Plugged displays list : {}".format(self.plugged_display))

        # Set the display config as SINGLE of the first display in command line
        if self.display_config.set_display_configuration_ex(enum.SINGLE,
                                                            [self.connected_list[0]],
                                                            self.enumerated_displays) is False:
            self.fail("Failed to set display configuration as SINGLE {}".format(self.connected_list[0]))
        logging.info("Successfully set the display configuration as SINGLE {}".format(self.connected_list[0]))

    ##
    # @brief        Verify if Virtual Display is enabled properly in headless
    # @param[in]    self; Object of virtual display yangra base class
    # @return       Bool; True, if verification is successful; False, otherwise
    def verify_headless_virtual_display(self):
        logging.info(" Function_Entry: verify_headless_virtual_display ".center(LINE_WIDTH, "*"))
        enumerated_displays = display_config.DisplayConfiguration().get_enumerated_display_info()
        logging.debug("Enumerated Display Information: {}".format(enumerated_displays.to_string()))

        for index in range(enumerated_displays.Count):
            display = enumerated_displays.ConnectedDisplays[index]
            connector_port = CONNECTOR_PORT_TYPE(display.ConnectorNPortType).name
            logging.info("connector_port {}".format(connector_port))

            if connector_port == 'VIRTUALDISPLAY' and enumerated_displays.Count == 1:
                logging.info("Virtual Display Enumerated - System in Headless {}, Port {}"
                             .format(enumerated_displays.Count, connector_port))
                return True
            else:
                logging.info("Virtual Display not Enumerated, Plugged display - {}".format(connector_port))
                return False

    ##
    # @brief        Verify if Virtual Display is enabled
    # @param[in]    self; Object of virtual display yangra base class
    # @return       Bool; True, if verification is successful; False, otherwise
    def verify_virtual_display(self):
        logging.info(" Function_Entry: verify_virtual_display ".center(LINE_WIDTH, "*"))
        connector_port = []
        enumerated_displays = display_config.DisplayConfiguration().get_enumerated_display_info()

        for index in range(enumerated_displays.Count):
            display = enumerated_displays.ConnectedDisplays[index]
            connector_port.append(CONNECTOR_PORT_TYPE(display.ConnectorNPortType).name)
            connector_type = display.PortType
            logging.debug("Connector_Port {}, Connector_Type {}".format(connector_port, connector_type))

        if 'VIRTUALDISPLAY' in connector_port:
            logging.info("Virtual Display Enumerated {}".format(enumerated_displays.to_string()))
            return True
        else:
            logging.error("Virtual Display is not Enumerated {}".format(connector_port))
            gdhm.report_bug(
                title="[OS Features][VirtualDisplay] Virtual Display is not Enumerated on {}".format(connector_port),
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            return False

    ##
    # @brief        Enable/Disables VirtualCRTSupport
    # @param[in]    self; Object of virtual display yangra base class
    # @param[in]    enable_support; Flag to enable/disable VirtualCRTSupport registry
    # @return       Bool; True, if enabling is successful
    def enable_disable_virtualcrtsupport(self, enable_support):
        logging.info(" Function_Entry: enable_disable_virtualcrtsupport ".center(LINE_WIDTH, "*"))
        value = 1 if enable_support is True else 0

        # Write into display driver registry path to enable VirtualCRTSupport
        registry_key = "VirtualCRTSupport"

        reg_args = registry_access.StateSeparationRegArgs(gfx_index="gfx_0")
        if registry_access.write(args=reg_args, reg_name=registry_key, reg_type=registry_access.RegDataType.DWORD,
                                 reg_value=value) is False:
            self.fail("Failed to write into registry with key {} and value {}".format(registry_key, value))
        logging.debug("Successfully written into registry with key {} and value {}".format(registry_key, value))

        # Check Under-run status
        if self.underrun_status.verify_underrun() is True:
            logging.error("Under-Run observed during regisrty addition in test")

        # Restart display driver to make the registry changes
        status, reboot_required = display_essential.restart_gfx_driver()
        if status is False:
            self.fail("Failed to restart driver after writing into registry")
        logging.debug("Display driver restarted successfully")

        # Verify virtual display
        if self.verify_virtual_display() is False:
            logging.error("Failed to verify virtual displays after restarting driver")
            return False
        logging.info("Successfully verified Virtual Display VirtualCRTSupport")
        return True

    ##
    # @brief        Helper function to Log Enumerated Display Status
    # @param[in]    self; Object of virtual display yangra base class
    # @return       void
    def log_enumerated_status(self):

        for display in self.connected_list:
            logging.debug("Display Connected - {}".format(display))

        enumerated_display = display_config.DisplayConfiguration().get_enumerated_display_info()
        logging.debug("Enumerated Display Information: {}".format(enumerated_display.to_string()))

    ##
    # @brief        Verify if VideoPresentSources are reported correct.
    # @param[in]    self; Object of virtual display yangra base class
    # @param[in]    etl_file
    # @return       Bool, True if VideoPresentSources is correct otherwise False
    def verify_videopresentsources(self, etl_file):
        logging.info(" Function_Entry: verify_videopresentsources ".center(LINE_WIDTH, "*"))

        if etl_parser.generate_report(etl_file, ETL_PARSER_CONFIG) is False:
            logging.error("\tFailed to generate EtlParser report [Test Issue]")
            return False

        start_device_output = etl_parser.get_event_data(etl_parser.Events.START_DEVICE)
        logging.debug("gfxStartDevice data {}".format(start_device_output))

        if start_device_output is None:
            logging.error("\tNo gfxStartDevice event found in ETL")
            return False
        else:
            start_device_output_list = []
            for data_field in range(len(start_device_output)):
                start_device_output_list.append(start_device_output[data_field])

            for index in range(len(start_device_output_list)):
                if start_device_output_list[index].VideoPresentSources == 3 and (
                        PLATFORM_NAME in VIDPNSOURCE_3 or SKU_NAME == 'ADLN'):
                    logging.info("Gfx Driver is reporting correct VideoPresentSources")
                    return True
                elif start_device_output_list[index].VideoPresentSources == 4 and PLATFORM_NAME in VIDPNSOURCE_4:
                    logging.info("Gfx Driver is reporting correct VideoPresentSources")
                    return True
                else:
                    logging.error("Gfx Driver is not reporting correct VideoPresentSources {} for platform {}".format(
                        start_device_output[index].VideoPresentSources, PLATFORM_NAME))
                    gdhm.report_bug(
                        title="[OS Features][VirtualDisplay] Gfx Driver is not reporting correct VideoPresentSources {} for platform {} ".format(
                            start_device_output[index].VideoPresentSources, PLATFORM_NAME),
                        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                        component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )
                    return False

    ##
    # @brief        Helper function to start ETL capture.
    # @param[in]    self; Object of virtual display yangra base class
    # @return       status, True if ETL started otherwise False
    def start_etl_capture(self):
        assert etl_tracer.stop_etl_tracer(), "Failed to Stop GfxTrace"

        if os.path.exists(etl_tracer.GFX_TRACE_ETL_FILE):
            file_name = 'GfxTrace_Before_DriverRestart.etl'
            etl_file_path = os.path.join(test_context.LOG_FOLDER, file_name)
            os.rename(etl_tracer.GFX_TRACE_ETL_FILE, etl_file_path)

        if etl_tracer.start_etl_tracer() is False:
            logging.error("Failed to Start Gfx Tracer")
            return False
        return True

    ##
    # @brief        Helper function to stop ETL capture
    # @param[in]    self; Object of virtual display yangra base class
    # @return       etl_file_path; Path to ETL file
    def stop_etl_capture(self):
        assert etl_tracer.stop_etl_tracer(), "Failed to Stop GfxTrace"
        etl_file_path = etl_tracer.GFX_TRACE_ETL_FILE

        if os.path.exists(etl_tracer.GFX_TRACE_ETL_FILE):
            file_name = 'GfxTrace_After_DriverRestart.etl'
            etl_file_path = os.path.join(test_context.LOG_FOLDER, file_name)
            os.rename(etl_tracer.GFX_TRACE_ETL_FILE, etl_file_path)

        if etl_tracer.start_etl_tracer() is False:
            logging.error("Failed to Start GfxTrace")
        return etl_file_path

    ##
    # @brief        Unittest Teardown function
    # @param[in]    self; Object of virtual display yangra base class
    # @return       void
    def tearDown(self):
        logging.info(" TEARDOWN: VIRTUAL_DISPLAY_BASE ".center(LINE_WIDTH, "*"))

        # Disable VirtualCRTSupport Display if enabled
        reg_args = registry_access.StateSeparationRegArgs(gfx_index="gfx_0")
        reg_value, reg_type = registry_access.read(args=reg_args, reg_name="VirtualCRTSupport")
        if reg_value is not None:
            if registry_access.write(args=reg_args, reg_name="VirtualCRTSupport",
                                     reg_type=registry_access.RegDataType.DWORD, reg_value=0) is False:
                self.fail("Failed to write into VirtualCRTSupport registry")
            logging.debug("Successfully disabled VirtualCRTSupport registry")

        # Unplug all plugged external displays
        for display in self.plugged_display:
            if display_utility.unplug(display) is False:
                self.fail("Failed to unplug display {}".format(display))
            logging.info("Successfully unplugged the display {}".format(display))
