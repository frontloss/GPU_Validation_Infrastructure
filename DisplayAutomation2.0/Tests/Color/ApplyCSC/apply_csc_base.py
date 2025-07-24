import json
import os
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE
from Libs.Core import driver_escape, registry_access, display_essential
from enum import Enum
from copy import deepcopy
from Libs.Core.test_env import test_context
from Libs.Core.wrapper.driver_escape_args import CSCPipeMatrixParams
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Color.color_common_base import *
from Tests.Color.ApplyCSC import csc_utility
from Tests.Color import color_common_utility

input_csc_file_path = os.path.join(test_context.ROOT_FOLDER, "Tests\\Color\\ApplyCSC\\input_csc_matrix.json")


class LINEAR_CSC_OPERATION(enum.Enum):
    _members_ = {
        'OPERATION_GET': 0,
        'OPERATION_SET': 1,
    }


class CSC_MATRIX_TYPE(enum.Enum):
    _members_ = {
        'LINEAR_CSC': 0,
        'NON_LINEAR_CSC': 1,
    }


class ApplyCSCBase(ColorCommonBase):
    csc_type = None
    matrix_type = "NON_IDENTITY"
    matrix_info = []
    custom_tags = ["-CSC_CLIENT", "-MATRIX_INFO", "-YCBCR_SATURATION_SUPPORT"]
    csc_matrix_tag = ["CSC_CLIENT", "MATRIX_INFO", "YCBCR_SATURATION_SUPPORT"]
    ycbcr_saturation_support = False

    def setUp(self):
        self.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, self.custom_tags)

        for key, value in self.cmd_line_param.items():
            if cmd_parser.display_key_pattern.match(key) is not None:
                if value['connector_port'] is not None:
                    self.connected_list.insert(value['index'], value['connector_port'])
            if key in self.csc_matrix_tag and value != 'NONE':
                if self.cmd_line_param['CSC_CLIENT'] is not None:
                    self.csc_type = CSC_MATRIX_TYPE(0).value if self.cmd_line_param['CSC_CLIENT'][0] == 'LINEAR_CSC' \
                        else CSC_MATRIX_TYPE(1).value
                if self.cmd_line_param['MATRIX_INFO'] is not None:
                    with open(input_csc_file_path) as f:
                        csc_info = json.load(f)
                    for index in range(0, len(csc_info)):
                        if csc_info[index]['name'] == self.cmd_line_param['MATRIX_INFO'][0]:
                            self.matrix_info = csc_info[index]['matrix']
                if self.cmd_line_param['YCBCR_SATURATION_SUPPORT'] != "NONE":
                    self.ycbcr_saturation_support = True

        ##
        # Verify and plug the display
        if len(self.connected_list) <= 0:
            logging.error("Minimum 1 display is required to run the test")
            self.fail()
        else:
            self.plugged_display, self.enumerated_displays = display_utility.plug_displays(self, self.cmd_line_param)

        ##
        # Set display configuration
        topology = eval("enum.%s" % (self.cmd_line_param['CONFIG']))
        if self.config.set_display_configuration_ex(topology, self.connected_list) is False:
            self.fail('Failed to apply display configuration %s %s' % (DisplayConfigTopology(topology).name,
                                                                       self.connected_list))

        logging.info('Successfully applied the display configuration %s %s' % (DisplayConfigTopology(topology).name,
                                                                               self.connected_list))

        ##
        # Cache the platform information
        self.platform = get_platform_info()

        ##
        # On TGL, RCR: supports YCbCr+Saturation, hence if the command line arguments has
        # YCbCr+Saturation support as True,
        # test needs to set the registry key to enable YCbCr and Saturation together
        if self.ycbcr_saturation_support:
            reg_args = registry_access.StateSeparationRegArgs(gfx_index="gfx_0")
            if not registry_access.write(args=reg_args, reg_name="SupportYCbCrAndSaturationEnable",
                                         reg_type=registry_access.RegDataType.DWORD, reg_value=1):
                logging.error("Registry key add to enable SupportYCbCrAndSaturationEnable failed")
                self.fail()
            else:
                logging.info("Registry key add to enable SupportYCbCrAndSaturationEnable SUCCESS")
                status, reboot_required = display_essential.restart_gfx_driver()

    def tearDown(self):
        ##
        # Apply Identity Matrix at the end of the test
        identity_csc = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        identity_csc_param = csc_utility.create_15_16_format_csc_matrix(deepcopy(identity_csc))
        param = CSCPipeMatrixParams(1, identity_csc_param)
        for index in range(0, len(self.connected_list)):
            if str(CONNECTOR_PORT_TYPE(self.enumerated_displays.ConnectedDisplays[index].ConnectorNPortType)) in self.connected_list and self.enumerated_displays.ConnectedDisplays[index].IsActive:
                if driver_escape.apply_csc(self.enumerated_displays.ConnectedDisplays[index].DisplayAndAdapterInfo,
                                           enum.OPERATION_SET, self.csc_type, param) is True:
                    logging.info("Successfully applied %s Identity CSC after completion of the test on %s" % (CSC_MATRIX_TYPE(
                        self.csc_type).name, self.connected_list[index]))
                else:
                    logging.info("Failed to apply %s Identity CSC after completion of the test on %s" % (CSC_MATRIX_TYPE(
                        self.csc_type).name, self.connected_list[index]))
                    self.fail("Failed to apply Identity CSC after completion of the test on %s" %self.connected_list[index])
        ##
        # Disabling SupportYCbCrAndSaturationEnable registry key if already enabled
        if self.ycbcr_saturation_support:
            reg_args = registry_access.StateSeparationRegArgs(gfx_index="gfx_0")
            if not registry_access.write(args=reg_args, reg_name="SupportYCbCrAndSaturationEnable",
                                         reg_type=registry_access.RegDataType.DWORD, reg_value=0):
                logging.error("Registry key to disable SupportYCbCrAndSaturationEnable failed")
                self.fail()
            else:
                logging.info("Registry key to disable SupportYCbCrAndSaturationEnable SUCCESS")
                status, reboot_required = display_essential.restart_gfx_driver()
        super().tearDown()
