########################################################################################################################
# @file     dsb_base.py
# @brief    It contains setUp and tearDown methods of unittest framework. 
# @details  In setUp, we parse command_line arguments and then calling 
#           PlugDisplays function of display_utility to plug displays which are there in command_line and not plugged.
#           In tearDown, the displays which were plugged in the setUp phase will be unplugged and the previous
#           configuration settings will be applied.
# @author   Amit Sau, Suraj Gaikwad
########################################################################################################################

import logging
import sys
import time
import unittest
from xml.etree import ElementTree

from Libs.Core import cmd_parser
from Libs.Core import display_utility
from Libs.Core import enum
from Libs.Core.display_config import display_config as disp_cfg
from Libs.Core.display_config.display_config_enums import DisplayConfigTopology
from Libs.Core.logger import gdhm
from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Core.sw_sim import driver_interface
from Libs.Core.test_env import test_context
from Libs.Feature import dsb as dsb_feature
from Libs.Feature.crc_and_underrun_verification import UnderRunStatus
from Libs.Feature.display_engine.de_base.display_base import DisplayBase

dsb_test_cfg_path = test_context.TestContext.root_folder() + '\Tests\DSB\dsb_test_config.xml'

WAIT_FOR_U_SEC = 1024

dsb_pipe_dict = {
    'PIPE_A': {
        'MODE': '3D_LUT',
        'PIPE_INDEX': 0,
        'DATA_REG_OFFSET': 0x490AC,
        'INDEX_REG_OFFSET': 0x490A8,
        'INDEX_REG_VALUE': None,
        'DATA_PAIR_REG_VALUE': None,
        'DATA_CTL_REG_OFFSET': 0x490A4,
        'DATA_CTL_REG_VALUE': None,
        'PIPE_SCANLINE_OFFSET': 0x70000,
        'PIPE_FRMCNT_OFFSET': 0x70040
    },
    'PIPE_B': {
        'MODE': '3D_LUT',
        'PIPE_INDEX': 1,
        'DATA_REG_OFFSET': 0x491AC,
        'INDEX_REG_OFFSET': 0x491A8,
        'INDEX_REG_VALUE': None,
        'DATA_PAIR_REG_VALUE': None,
        'DATA_CTL_REG_OFFSET': 0x491A4,
        'DATA_CTL_REG_VALUE': None,
        'PIPE_SCANLINE_OFFSET': 0x71000,
        'PIPE_FRMCNT_OFFSET': 0x71040
    },
    'PIPE_C': {
        'MODE': 'GAMMA',
        'PIPE_INDEX': 2,
        'DATA_REG_OFFSET': 0x4B404,
        'INDEX_REG_OFFSET': 0x4B400,
        'INDEX_REG_VALUE': None,
        'DATA_PAIR_REG_VALUE': None,
        'DATA_CTL_REG_OFFSET': 0x4B480,
        'DATA_CTL_REG_VALUE': None,
        'PIPE_SCANLINE_OFFSET': 0x72000,
        'PIPE_FRMCNT_OFFSET': 0x72040
    },
    'PIPE_D': {
        'MODE': 'GAMMA',
        'PIPE_INDEX': 3,
        'DATA_REG_OFFSET': 0x4BC04,
        'INDEX_REG_OFFSET': 0x4BC00,
        'INDEX_REG_VALUE': None,
        'DATA_PAIR_REG_VALUE': None,
        'DATA_CTL_REG_OFFSET': 0x4BC80,
        'DATA_CTL_REG_VALUE': None,
        'PIPE_SCANLINE_OFFSET': 0x73000,
        'PIPE_FRMCNT_OFFSET': 0x73040
    }
}

dsb_mmio_range = {
    'PIPE': 10,
    'LACE': 10,
    'HDR': 10}


##
# @brief        DsbBase
# @param[in]    unittest.TestCase - Test Case
# @return       None
class DsbBase(unittest.TestCase):
    custom_tags = ['-TEST_TYPE', '-SINGLE_TRIGGER']
    enumerated_displays = None
    platform = None
    display_list = list()
    display_port_pipe_mapping = dict()
    dsb_test_config = dict()
    display_config = disp_cfg.DisplayConfiguration()
    driver_interface_ = driver_interface.DriverInterface()
    under_run_status = UnderRunStatus()
    dsb = dsb_feature.DisplayStateBuffer()
    machine_info = SystemInfo()
    gfx_display_hwinfo = machine_info.get_gfx_display_hardwareinfo()
    # WA : currently test are execute on single platform. so loop break after 1 st iteration.
    # once Enable MultiAdapter remove the break statement.
    for i in range(len(gfx_display_hwinfo)):
        platform = str(gfx_display_hwinfo[i].DisplayAdapterName).lower()
        break
    test_cfg_xml = ElementTree.parse(dsb_test_cfg_path)
    fail_count = 0

    ##
    # @brief        Setup Function
    # @return       None
    def setUp(self):
        self.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, custom_tags=self.custom_tags)

        # connected_list[] is a list of Port Names of the connected Displays
        for key, value in self.cmd_line_param.items():
            if cmd_parser.display_key_pattern.match(key) is not None:
                if value['connector_port'] is not None:
                    self.display_list.insert(value['index'], value['connector_port'])

        # Get Enumerated displays details
        self.plugged_display, self.enumerated_displays = display_utility.plug_displays(self, self.cmd_line_param)

        # Set Display Configuration
        topology = eval("enum.%s" % (self.cmd_line_param['CONFIG']))
        logging.info("Applying Display Configuration as %s : %s"
                     % (DisplayConfigTopology(topology).name, self.display_list))
        if self.display_config.set_display_configuration_ex(topology, self.display_list,
                                                            self.enumerated_displays) is False:
            self.fail('Failed to apply display config as %s on %s'
                      % (DisplayConfigTopology(topology).name, self.display_list))
        # Todo: Remove as part of VSDI-31759
        time.sleep(6)

        # get all active pipes
        for display in self.display_list:
            display_base = DisplayBase(display, self.platform.upper())
            pipe, ddi = display_base.GetPipeDDIAttachedToPort(display)
            self.display_port_pipe_mapping[pipe] = display

        # Fetch the DSB Selector from CMD Args
        if self.cmd_line_param['TEST_TYPE'][0] is not None:
            self.parse_dsb_test_config(self.cmd_line_param['TEST_TYPE'][0], self.display_port_pipe_mapping.keys())
            if self.dsb_test_config.__len__() == 0:
                gdhm.report_bug(
                    title='[DSB] Invalid DSB test configuration provided as command line argument',
                    problem_classification=gdhm.ProblemClassification.OTHER,
                    component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                    priority=gdhm.Priority.P3,
                    exposure=gdhm.Exposure.E3)
                self.fail('Invalid DSB test configuration provided as command line argument')
        else:
            gdhm.report_bug(
                title='[DSB] Invalid DSB test configuration provided as command line argument',
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                priority=gdhm.Priority.P3,
                exposure=gdhm.Exposure.E3)
            self.fail('Invalid DSB test configuration provided as command line argument')

        self.configure_control_register(is_disable=True)
        self.configure_data_register(is_save=True)

        # Verify Under-run
        self.verify_underrun()

    ##
    # @brief        TearDown Function
    # @return       None
    def tearDown(self):
        logging.info("Test Clean Up")
        self.configure_data_register(is_save=False)
        self.configure_control_register(is_disable=False)

        # Unplug the displays and restore the configuration to the initial configuration
        for display in self.plugged_display:
            display_utility.unplug(display)
            self.enumerated_displays = self.display_config.get_enumerated_display_info()
            if not disp_cfg.is_display_attached(self.enumerated_displays, display):
                logging.info("Successfully unplugged %s", display)
            else:
                logging.error("Unable to unplug %s", display)
        if self.fail_count > 0:
            self.fail('Test Failed!!!')

    ##
    # @brief        parse dsb test config
    # @param[in]    test - DSB test parameter
    # @param[in]    pipe_list - List of pipes
    # @return       None
    def parse_dsb_test_config(self, test, pipe_list):
        for pipe in pipe_list:
            self.dsb_test_config[pipe] = {}
            self.__get_generic_info(pipe)
            self.__get_test_config_info(test, pipe)

    ##
    # @brief        get test configuration generic info across all test
    # @param[in]    pipe - Input pipes
    # @return       None
    def __get_generic_info(self, pipe):
        selector = dsb_feature.SimDrvDsbSelector[self.test_cfg_xml.find('./generic_info/dsb_selector/%s' % pipe).text]
        self.dsb_test_config[pipe].update({'dsb_selector': selector})

        generate_interrupt = True if self.test_cfg_xml.find(
            './generic_info/interrupt_on_completion').text.upper() == 'TRUE' else False
        self.dsb_test_config[pipe].update({'interrupt_on_completion': generate_interrupt})

        delta_frm_count = int(self.test_cfg_xml.find('./generic_info/delta_frame_count').text)
        self.dsb_test_config[pipe].update({'delta_frame_count': delta_frm_count})

        delay = int(self.test_cfg_xml.find('./generic_info/delay_in_verification').text)
        self.dsb_test_config[pipe].update({'delay_in_verification': delay})

    ##
    # @brief get test configuration info
    # @param[in]    pipe - Input pipes
    # @param[in]    test - test case
    # @return       None
    def __get_test_config_info(self, test, pipe):
        test_xml = self.test_cfg_xml.find("./test_config/.[@name='%s']" % test.lower())
        if test_xml is None:
            gdhm.report_bug(
                title='[DSB] Invalid Test Config provided in dsb_test_config.xml',
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                priority=gdhm.Priority.P3,
                exposure=gdhm.Exposure.E3)
            self.fail('Invalid Test Config')

        for test_parameter in test_xml:
            if test_parameter.tag == 'dsb_sync_type':
                self.dsb_test_config[pipe].update(
                    {test_parameter.tag: dsb_feature.SimDrvDsbSyncType[test_parameter.text]})
            elif test_parameter.tag == 'dsb_trigger_mode':
                self.dsb_test_config[pipe].update(
                    {test_parameter.tag: dsb_feature.SimDrvDsbTriggerMode[test_parameter.text]})
            elif test_parameter.tag == 'auto_increment':
                auto_increment = True if test_parameter.text.upper() == 'TRUE' else False
                self.dsb_test_config[pipe].update({'auto_increment': auto_increment})
            elif test_parameter.tag == 'contiguous_dsb_trigger':
                contiguous_dsb_trigger = True if test_parameter.text.upper() == 'TRUE' else False
                self.dsb_test_config[pipe].update({'contiguous_dsb_trigger': contiguous_dsb_trigger})
            elif test_parameter.tag == 'no_of_trigger':
                self.dsb_test_config[pipe].update({'no_of_trigger': int(test_parameter.text)})
            elif test_parameter.tag == 'wait_time':
                self.dsb_test_config[pipe].update({'wait_time': int(test_parameter.text)})

    ##
    # @brief        configure (save & restore) control register
    # @param[in]    is_disable - Control register state
    # @return       None
    def configure_control_register(self, is_disable):
        if is_disable is True:
            for pipe, data in dsb_pipe_dict.items():
                if pipe in self.display_port_pipe_mapping.keys():
                    value = self.driver_interface_.mmio_read(data['DATA_CTL_REG_OFFSET'], 'gfx_0')
                    data['DATA_CTL_REG_VALUE'] = value  # Store register value.
                    # set initial value to 0
                    self.driver_interface_.mmio_write(data['DATA_CTL_REG_OFFSET'], 0x0, 'gfx_0')
                    # enable 10 bit gamma mode and disable gamma
                    if data['MODE'] == 'GAMMA':
                        self.driver_interface_.mmio_write(data['DATA_CTL_REG_OFFSET'], 0x1, 'gfx_0')
                        logging.info('Disable %s %s CTRL_REG %s (Bit31:0) & Enable 10 Bit gamma (Bit0&1:1)'
                                     % (pipe, data['MODE'], hex(data['DATA_CTL_REG_OFFSET']).upper()))
                    # disable 3d LUT
                    elif data['MODE'] == '3D_LUT':
                        logging.info('Disable %s %s CTRL_REG %s (Bit31:0)'
                                     % (pipe, data['MODE'], hex(data['DATA_CTL_REG_OFFSET']).upper()))
        else:
            ##
            # Restore the register values for 3D LUT and Gamma CTL registers
            for pipe, data in dsb_pipe_dict.items():
                if pipe in self.display_port_pipe_mapping.keys():
                    self.driver_interface_.mmio_write(data['DATA_CTL_REG_OFFSET'], data['DATA_CTL_REG_VALUE'], 'gfx_0')
                    logging.info('Restore %s %s CTRL_REG %s value = %s'
                                 % (pipe, data['MODE'], hex(data['DATA_CTL_REG_OFFSET']).upper(),
                                    hex(data['DATA_CTL_REG_VALUE'])))

    ##
    # @brief        configure (save & restore) DSB Data pair offset
    # @param[in]    display_pipe - Display Pipe
    # @param[in]    is_save - Index register saved value state
    # @return       None
    def configure_index_register(self, display_pipe, is_save):
        if is_save is True:
            for pipe, data in dsb_pipe_dict.items():
                if pipe in self.display_port_pipe_mapping.keys():
                    if pipe == display_pipe:
                        value = self.driver_interface_.mmio_read(data['INDEX_REG_OFFSET'], 'gfx_0')
                        data['INDEX_REG_VALUE'] = value  # Store register value.
                        # set initial value to 0
                        self.driver_interface_.mmio_write(data['INDEX_REG_OFFSET'], 0x0, 'gfx_0')
        else:
            ##
            # Restore the register values for 3D LUT and Gamma index registers
            for pipe, data in dsb_pipe_dict.items():
                if pipe in self.display_port_pipe_mapping.keys():
                    if pipe == display_pipe:
                        self.driver_interface_.mmio_write(data['INDEX_REG_OFFSET'], data['INDEX_REG_VALUE'], 'gfx_0')

    ##
    # @brief        configure (save & restore) DSB Data pair offset
    # @param[in]    is_save - Index register saved value state
    # @return       None
    def configure_data_register(self, is_save):
        if is_save is True:
            for pipe, data in dsb_pipe_dict.items():
                if pipe in self.display_port_pipe_mapping.keys():
                    value = self.driver_interface_.mmio_read(data['DATA_REG_OFFSET'], 'gfx_0')
                    data['DATA_PAIR_REG_VALUE'] = value  # Store register value.
                    self.driver_interface_.mmio_write(data['DATA_REG_OFFSET'], 0, 'gfx_0')
        else:
            for pipe, data in dsb_pipe_dict.items():
                if pipe in self.display_port_pipe_mapping.keys():
                    self.driver_interface_.mmio_write(data['DATA_REG_OFFSET'], data['DATA_PAIR_REG_VALUE'], 'gfx_0')

    ##
    # @brief        verify pipe under-run
    # @return       None
    def verify_underrun(self):
        if self.under_run_status.verify_underrun() is True:
            logging.error('Underrun Occured')
