######################################################################################
# @file         dbuf_allocation.py
# @brief        The script validates DBUF allocation programming with HDR enabled
# @details      in all pipe combinations for 4 displays.
#               CommandLine :  python dbuf_allocation.py -hdmi_b -dp_d_tc -dp_e_tc -dp_f_tc
# @author       Sunaina Ashok, Bhargav adigarla
###############################################f#######################################
import logging
import sys
import unittest

from Libs.Core import enum
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core import cmd_parser
from Libs.Core import display_utility
from Libs.Core.display_config import display_config_enums as cfg_enum
from Libs.Feature.display_watermark import watermark
from Libs.Feature.display_engine.de_base import display_base
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.display_config.display_config import configure_hdr
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE
from Tests.Color.HDR.OSHDR import os_hdr_verification
from Tests.Color.color_common_utility import get_platform_info
from Libs.Core.Verifier.common_verification_args import VerifierCfg


##
# @brief        DbufAllocation Class
class DbufAllocation(unittest.TestCase):

    cmd_line_param = None
    connnector_port_list = []
    watermark = watermark.DisplayWatermark()
    config = DisplayConfiguration()
    topology = enum.EXTENDED
    os_hdr_verify = os_hdr_verification.OSHDRVerification()

    ##
    # Unplug pipe list, to obtain all the pipe comibinations mentioned in Bspec.
    # PipeA + PipeB + PipeC + PipeD enable
    unplug_pipe_sequence = ["PIPE_A",  # PipeB + PipeC + PipeD enable
                            "PIPE_B",  # PipeC + PipeD enable
                            "PIPE_C",  # PipeD enable
                            # Plug back all pipes
                            # PipeA + PipeB + PipeC + PipeD enable
                            "PIPE_B",  # PipeA + PipeC + PipeD enable
                            "PIPE_C",  # PipeA + PipeD enable
                            "PIPE_D",  # PipeA enable
                            # Plug back all pipes
                            # PipeA + PipeB + PipeC + PipeD enable
                            "PIPE_C",  # PipeA + PipeB + PipeD enable
                            "PIPE_D",  # PipeA + PipeB enable
                            "PIPE_A",  # PipeB enable
                            # Plug back all pipes
                            # PipeA + PipeB + PipeC + PipeD enable
                            "PIPE_D",  # PipeA + PipeB + PipeC enable
                            "PIPE_A",  # PipeB + PipeC enable
                            "PIPE_B",  # PipeC enable
                            # Plug back all pipes
                            # PipeA + PipeB + PipeC + PipeD enable
                            "PIPE_C",  # PipeA + PipeB + PipeD enable
                            "PIPE_A",  # PipeB + PipeD enable
                            "PIPE_B",  # PipeD enable
                            # Plug back all pipes
                            # PipeA + PipeB + PipeC + PipeD enable
                            "PIPE_B",  # PipeA + PipeC + PipeD enable
                            "PIPE_D",  # PipeA + PipeC enable
                            "PIPE_A"]  # PipeC enable

    ##
    # @brief        Setup Function
    # @return       None
    def setUp(self):
        logging.info("************** TEST  STARTS HERE*************************")

        ##
        # Parse cmd line
        self.cmd_line_param = cmd_parser.parse_cmdline(sys.argv)
        for key, value in self.cmd_line_param.items():
            if cmd_parser.display_key_pattern.match(key) is not None:
                if value['connector_port'] is not None:
                    self.connnector_port_list.insert(value['index'], value['connector_port'])

        # Check required cmdline parameters are passed
        if len(self.connnector_port_list) < 4:
            logging.error("4 display cmd line arguments are required to run the test")
            self.fail("FAILED")

        self.port_pipe_dict = dict([(x, None) for x in self.connnector_port_list])

        ##
        # Cache the platform information
        self.platform = get_platform_info()

        # This is to ensure that no displays are present before plug
        enumerated_displays = self.config.get_enumerated_display_info()
        logging.info("Enumerated Display Information: %s", enumerated_displays.to_string())
        for i in range(enumerated_displays.Count):
            display_port = cfg_enum.CONNECTOR_PORT_TYPE(
                enumerated_displays.ConnectedDisplays[i].ConnectorNPortType).name
            if display_utility.unplug(display_port) is False:
                logging.warning('Failed to unplug %s' % (display_port))
            else:
                logging.info('Unplug successful %s' % (display_port))

        # Verify and plug the display
        self.plugged_display, self.enumerated_displays = display_utility.plug_displays(self, self.cmd_line_param)

        # Applying EXTENDED Configurations on all the displays connected
        if self.config.set_display_configuration_ex(self.topology, self.connnector_port_list) is True:
            logging.info("Successfully applied EXTENDED Display configuration")

        for display_index in range(self.enumerated_displays.Count):
            port_type = str(CONNECTOR_PORT_TYPE(
                              self.enumerated_displays.ConnectedDisplays[display_index].ConnectorNPortType))
            if port_type in self.connnector_port_list:
                if self.enumerated_displays.ConnectedDisplays[display_index].IsActive:

                    hdr_error_code = configure_hdr(self.enumerated_displays.ConnectedDisplays[display_index].
                                                   DisplayAndAdapterInfo, enable=True)
                    ##
                    # Decode HDR Error Code and Verify
                    if self.os_hdr_verify.is_error("OS_HDR", hdr_error_code, "ENABLE") is False:
                        self.fail("Failed to enable HDR")

                    ##
                    # Verify PIPE_MISC for register verification
                    if self.os_hdr_verify.verify_hdr_mode(port_type,"ENABLE", self.platform) is False:
                        self.fail("HDR PIPE_MISC register verification failed")
                else:
                    self.fail("Plugged display: %s was inactive" % port_type)

        self.getport_pipe_mapping()

    ##
    # @brief        Test Run Function
    # @return       None
    def runTest(self):

        ##
        # WM and DBuf verification with all pipes enabled
        if self.watermark.verify_watermarks() is False:
            self.fail('Watermark error observed')
        else:
            logging.info("Watermark verification passed")

        ##
        # Unplug each port according to unplug_pipe_sequence list
        for pipevalue in self.unplug_pipe_sequence:
            port = self.getport(self.port_pipe_dict, pipevalue)
            if port is None:
                continue
            if display_utility.unplug(port) is False:
                logging.warning('Failed to unplug %s' % (port))
            else:
                logging.info('Unplug successful %s' % (port))

            self.getport_pipe_mapping()

            logging.info('Currently enabled pipes {0}'.format(self.port_pipe_dict))

            ##
            # WM verification after display Unplug
            if self.watermark.verify_watermarks() is not True:
                self.fail('Watermark error observed')
            else:
                logging.info("Watermark verification passed")

            # Plug all display when port_pipe_dict has only 1 plugged display remaining.
            # This is to avoid all display unplugged scenario
            none_count = sum(value is None for value in self.port_pipe_dict.values())
            if none_count == len(self.port_pipe_dict) - 1:
                # Verify and plug the display
                self.plugged_display, self.enumerated_displays = display_utility.plug_displays(self,
                                                                                                   self.cmd_line_param)

                # Applying EXTENDED Configurations on all the displays connected
                if self.config.set_display_configuration_ex(self.topology, self.connnector_port_list) is True:
                    logging.info("Successfully applied EXTENDED Display configuration")

                self.getport_pipe_mapping()

    ##
    # @brief        Tear Down Function
    # @return       None
    def tearDown(self):
        logging.info("Test Clean Up")
        ##
        # Unplug the displays and restore the configuration to the initial configuration
        for display in self.plugged_display:
            logging.info("Trying to unplug %s" % display)
            display_utility.unplug(display)
        logging.info("************** TEST  ENDS HERE*************************")

    ##
    # @brief        To get port value from dictionary for Pipe
    # @return       None
    def getport(self, portpipedict, pipe):
        for key, value in portpipedict.items():
            if pipe == value:
                return key

    ##
    # @brief        Pipe mapping for display port
    # @return       None
    def getport_pipe_mapping(self):
        for key, value in self.port_pipe_dict.items():
            display_obj = display_base.DisplayBase(key)
            if (display_obj.pipe == "PIPE_A") or \
                        (display_obj.pipe == "PIPE_B") or \
                        (display_obj.pipe == "PIPE_C") or \
                        (display_obj.pipe == "PIPE_D"):
                self.port_pipe_dict[key] = display_obj.pipe
            else:
                self.port_pipe_dict[key] = None


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
