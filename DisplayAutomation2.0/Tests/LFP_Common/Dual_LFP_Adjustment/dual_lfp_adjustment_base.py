########################################################################################################################
# @file         dual_lfp_adjustment_base.py
# @brief        This file contains the base class for dual lfp adjustment test cases
# @details      This is a feature to fix the misalignment issue between the two panels. The misalignment is fixed by
#               adjusting the frame.It contains setUp and tearDown methods of unittest framework. In setUp, we parse
#               command_line arguments, plug displays, read necessary VBT blocks and check the scalar registers.
#               In tearDown, the changes done in VBT is reset to the previous state.
#
# @author       Sri Sumanth Geesala,Neha3 Kumari
########################################################################################################################
import logging
import sys
import unittest

from Libs.Core import cmd_parser
from Libs.Core import reboot_helper
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.display_power import DisplayPower
from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.vbt.vbt import Vbt
from Libs.Feature.display_engine.de_base.display_base import DisplayBase
from Libs.Feature.mipi import mipi_helper
from Tests.MIPI.Verifiers import mipi_dsc
from registers.mmioregister import MMIORegister


##
# @brief        This is a decorator class to determine number of calls for a method
class callcounted(object):

    ##
    # @brief        Initializer function to set count value
    # @param[in]    method - method whose calls are to be counted
    def __init__(self, method):
        self.method = method
        self.counter = 0

    ##
    # @brief        Method to increment the count whenever a method is called
    # @param[in]    *args - method arguments
    # @param[in]    *kwargs - method arguments
    # @return       None
    def __call__(self, *args, **kwargs):
        self.counter += 1
        return self.method(*args, **kwargs)


##
# @brief        Exposed Class for Dual LFP Adjustment tests. Any new Dual LFP Adjustment test can inherit this class
#               to use common setUp and tearDown functions. This class also includes some functions used across all
#               Dual LFP Adjustment tests.
class DualLfpAdjustmentBase(unittest.TestCase):
    display_power = DisplayPower()
    display_config = DisplayConfiguration()
    machine_info = SystemInfo()

    ##
    # @brief        This class method is the entry point for Dual LFP Adjustment test cases. Helps to initialize some
    #               of the parameters required for Dual LFP Adjustment test execution.
    # @details      This function gets the platform info, parses command line arguments for display list and custom tags
    # @return       None
    @reboot_helper.__(reboot_helper.setup)
    def setUp(self):
        logging.info("Starting Test Setup")
        self.my_custom_tags = ['-border', '-panel1', '-panel2']
        self.gfx_vbt = Vbt()
        logging.error = callcounted(logging.error)
        self.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, self.my_custom_tags)
        self.lfps_in_cmdline = []
        self.panel1_index = self.panel2_index = -1
        self.platform = None
        self.border_value = 0
        self.panel1_border_pos = ''
        self.panel2_border_pos = ''
        self.panel1_index = self.panel2_index = 0
        self.target_id_list = []
        self.DSC_enabled = 0
        # get platform
        gfx_display_hwinfo = self.machine_info.get_gfx_display_hardwareinfo()
        # WA : currently test are execute on single platform. so loop break after 1 st iteration.
        # once Enable MultiAdapter remove the break statement.

        for i in range(len(gfx_display_hwinfo)):
            self.platform = ("%s" % gfx_display_hwinfo[i].DisplayAdapterName).lower()
            break
        # process cmdline for display list and custom tags
        for key, value in self.cmd_line_param.items():
            if cmd_parser.display_key_pattern.match(key) is not None:
                if ((value['connector_port'] is not None) and (
                        value['connector_port'].startswith('MIPI') or value['connector_port'].startswith('EDP'))):
                    self.lfps_in_cmdline.append(value['connector_port'])
            if key == 'BORDER':
                self.border_value = int(value[0], 10)
            if key == 'PANEL1':
                self.panel1_border_pos = value[0].lower()
            if key == 'PANEL2':
                self.panel2_border_pos = value[0].lower()
        self.lfps_in_cmdline.sort()
        if self.lfps_in_cmdline.__contains__("MIPI_A") or self.lfps_in_cmdline.__contains__("MIPI_C"):
            self.DSC_enabled = self.gfx_vbt.block_2.DisplayDeviceDataStructureEntry[self.panel1_index].CompressionEnable
        elif self.lfps_in_cmdline.__contains__("EDP_A") or self.lfps_in_cmdline.__contains__("EDP_B"):
            # TODO: Add condition for eDP if DSC is enabled or not
            pass

        self.panel_borders_pos = [self.panel1_border_pos, self.panel2_border_pos]

    ##
    # @brief        This method is the exit point for Dual LFP Adjustment tests. This checks for errors in the test
    #               execution and reports if any
    # @return       None
    @reboot_helper.__(reboot_helper.teardown)
    def tearDown(self):
        logging.info("Starting Test Cleanup")
        # report test failure if fail_count>0
        if (logging.error.counter > 0):
            self.fail(
                "Some checks in the test have failed. Check error logs. No. of failures= %d" % logging.error.counter)

    ##
    # @brief        Function to get panel index for port
    # @param[in]    port - port to which the panel is attached
    # @return       panel_index - if found, -1 otherwise
    def get_panel_index_for_port(self, port):
        if port.upper() in ['MIPI_A', 'MIPI_C', 'EDP_A', 'EDP_B']:
            # WA: To be fixed as part of VSDI-22181
            port = port[1:].upper() if port in ['EDP_A', 'EDP_B'] else port.upper()
            panel_index = self.gfx_vbt.get_lfp_panel_type(port)
            logging.debug(f"\tPanel Index for {port}= {panel_index}")
            return panel_index
        return -1

    ##
    # @brief        Function to fill border values in vbt
    # @param[in]    port - port to which the panel is attached
    # @param[in]    top_border -  number
    # @param[in]    bottom_border - number
    # @param[in]    left_border - number
    # @param[in]    right_border - number
    # @return       bool - True if filling of values in vbt is successful, False otherwise
    def fill_border_values_in_vbt(self, port, top_border=0, bottom_border=0, left_border=0, right_border=0):
        # as per driver policy, border value is supported upto 127 only.
        if top_border > 127 or bottom_border > 127 or left_border > 127 or right_border > 127:
            return False
        panel_index = self.get_panel_index_for_port(port)
        self.gfx_vbt.block_42.DualLfpHingeAlignmentParamEntry[panel_index].TopBorder = top_border
        self.gfx_vbt.block_42.DualLfpHingeAlignmentParamEntry[panel_index].BottomBorder = bottom_border
        # left border  and right border are not yet exposed in vbt. Once they are exposed, we can add code here.

        return True

    ##
    # @brief        Function to verify scaler for Dual LFP Adjustment tests
    # @param[in]    port - port to which the panel is attached
    # @param[in]    top_border - number
    # @param[in]    bottom_border - number
    # @param[in]    left_border - number
    # @param[in]    right_border - number
    # @return       None
    def verify_scalar(self, port, top_border=0, bottom_border=0, left_border=0, right_border=0):
        display_base = DisplayBase(port, self.platform.upper())
        pipe = display_base.pipe.split('_')[1]
        # verify scalar enable bit. One of the two scalars of this pipe should be enabled for misalignment adjustment purpose.
        ps_ctrl_1 = MMIORegister.read("PS_CTRL_REGISTER", "PS_CTRL_1_" + pipe, self.platform)
        ps_ctrl_2 = MMIORegister.read("PS_CTRL_REGISTER", "PS_CTRL_2_" + pipe, self.platform)
        if ps_ctrl_1.enable_scaler == 0x1:
            scalar_num = 1
            logging.info('PASS: PS_CTRL_1_{0} - enable_scaler : Expected= enabled \t Actual= enabled'.format(pipe))
        elif ps_ctrl_2.enable_scaler == 0x1:
            scalar_num = 2
            logging.info('PASS: PS_CTRL_2_{0} - enable_scaler : Expected= enabled \t Actual= enabled'.format(pipe))
        else:
            logging.error(
                'FAIL: PS_CTRL for port {0} - enable_scaler : Expected= enabled \t Actual= disabled'.format(port))
            return
        logging.info("port {0} is connected to pipe {1}".format(port, pipe))
        trans = ""
        # verify scalar window size register
        if 'EDP_A' in port:
            trans = 'A'
        elif 'EDP_B' in port:
            trans = 'B'
        elif 'MIPI_A' in port:
            trans = 'DSI0'
        elif 'MIPI_C' in port:
            trans = 'DSI1'
        trans_htotal = MMIORegister.read("TRANS_HTOTAL_REGISTER", "TRANS_HTOTAL_" + trans, self.platform)
        trans_vtotal = MMIORegister.read("TRANS_VTOTAL_REGISTER", "TRANS_VTOTAL_" + trans, self.platform)
        # adding 1 since transcoder hactive and vactive are stored as zero-based values
        hactive = trans_htotal.horizontal_active + 1
        vactive = trans_vtotal.vertical_active + 1

        ps_win_sz = MMIORegister.read("PS_WIN_SZ_REGISTER", "PS_WIN_SZ_{0}_{1}".format(scalar_num, pipe), self.platform)
        expected_xsize = hactive - (left_border + right_border)
        expected_ysize = vactive - (top_border + bottom_border)
        # When the pipe scalar is configured, the X,Y must be even.
        expected_xsize = (expected_xsize - 1) if (expected_xsize % 2 != 0) else expected_xsize
        expected_ysize = (expected_ysize - 1) if (expected_ysize % 2 != 0) else expected_ysize
        if ps_win_sz.xsize == expected_xsize:
            logging.info('PASS: PS_WIN_SZ_{0}_{1} - xsize : Expected= {2} \t Actual= {3}'.format(scalar_num, pipe,
                                                                                                 expected_xsize,
                                                                                                 ps_win_sz.xsize))
        else:
            logging.error('FAIL: PS_WIN_SZ_{0}_{1} - xsize : Expected= {2} \t Actual= {3}'.format(scalar_num, pipe,
                                                                                                  expected_xsize,
                                                                                                  ps_win_sz.xsize))
        if ps_win_sz.ysize == expected_ysize:
            logging.info('PASS: PS_WIN_SZ_{0}_{1} - ysize : Expected= {2} \t Actual= {3}'.format(scalar_num, pipe,
                                                                                                 expected_ysize,
                                                                                                 ps_win_sz.ysize))
        else:
            logging.error('FAIL: PS_WIN_SZ_{0}_{1} - ysize : Expected= {2} \t Actual= {3}'.format(scalar_num, pipe,
                                                                                                  expected_ysize,
                                                                                                  ps_win_sz.ysize))

        # verify scalar window position register
        ps_win_pos = MMIORegister.read("PS_WIN_POS_REGISTER", "PS_WIN_POS_{0}_{1}".format(scalar_num, pipe),
                                       self.platform)
        expected_xpos = left_border
        expected_ypos = top_border
        # When the pipe scalar is configured, the X,Y must be even.
        expected_xpos = (expected_xpos - 1) if (expected_xpos % 2 != 0) else expected_xpos
        expected_ypos = (expected_ypos - 1) if (expected_ypos % 2 != 0) else expected_ypos
        if ps_win_pos.xpos == expected_xpos:
            logging.info('PASS: PS_WIN_POS_{0}_{1} - xpos : Expected= {2} \t Actual= {3}'.format(scalar_num, pipe,
                                                                                                 expected_xpos,
                                                                                                 ps_win_pos.xpos))
        else:
            logging.error('FAIL: PS_WIN_POS_{0}_{1} - xpos : Expected= {2} \t Actual= {3}'.format(scalar_num, pipe,
                                                                                                  expected_xpos,
                                                                                                  ps_win_pos.xpos))
        if ps_win_pos.ypos == expected_ypos:
            logging.info('PASS: PS_WIN_POS_{0}_{1} - ypos : Expected= {2} \t Actual= {3}'.format(scalar_num, pipe,
                                                                                                 expected_ypos,
                                                                                                 ps_win_pos.ypos))
        else:
            logging.error('FAIL: PS_WIN_POS_{0}_{1} - ypos : Expected= {2} \t Actual= {3}'.format(scalar_num, pipe,
                                                                                                  expected_ypos,
                                                                                                  ps_win_pos.ypos))

    ##
    # @brief        Function to fill vbt with border values as per the command line.
    # @return       None
    def configure_borders_in_vbt(self):
        # fill vbt with border values as per command line
        for index in range(len(self.lfps_in_cmdline)):
            top = 0
            bottom = 0
            if self.panel_borders_pos[index] == 'top':
                top = self.border_value
            elif self.panel_borders_pos[index] == 'bottom':
                bottom = self.border_value
            else:
                self.fail('{0} for border not supported'.format(self.panel_borders_pos[index]))
            self.fill_border_values_in_vbt(self.lfps_in_cmdline[index], top_border=top, bottom_border=bottom)
        # make vbt API call to set vbt with self.stBlock42
        logging.info('Setting border values in VBT')
        if self.gfx_vbt.apply_changes() is False:
            self.fail('Setting VBT block failed')

    ##
    # @brief        Function to verify scalar register programming
    # @return       None
    def verify_scalar_register_programming(self):  # verifying scalar registers
        # verify scalar registers
        for index in range(len(self.lfps_in_cmdline)):
            top = 0
            bottom = 0
            if self.panel_borders_pos[index] == 'top':
                top = self.border_value
            elif self.panel_borders_pos[index] == 'bottom':
                bottom = self.border_value
            else:
                self.fail('{0} for border not supported'.format(self.panel_borders_pos[index]))

            self.verify_scalar(self.lfps_in_cmdline[index], top_border=top, bottom_border=bottom)

    ##
    # @brief        Function to verify dsc
    # @return       None
    def verify_dsc(self):
        port_list = []
        if self.lfps_in_cmdline.__contains__("MIPI_A") or self.lfps_in_cmdline.__contains__("MIPI_C"):
            if "MIPI_A" in self.lfps_in_cmdline:
                port_list.append("_DSI0")
            if "MIPI_C" in self.lfps_in_cmdline:
                port_list.append("_DSI1")
        elif self.lfps_in_cmdline.__contains__("EDP_A") or self.lfps_in_cmdline.__contains__("EDP_B"):
            # TODO: Construct port_list based on verify dsc logic requirement for eDP
            pass

        if self.lfps_in_cmdline.__contains__("MIPI_A") or self.lfps_in_cmdline.__contains__("MIPI_C"):
            mipi_dsc.verify_dsc_config(mipi_helper.MipiHelper(self.platform), port_list)
        elif self.lfps_in_cmdline.__contains__("EDP_A") or self.lfps_in_cmdline.__contains__("EDP_B"):
            # TODO: Add verify dsc logic for eDP display
            pass


if __name__ == '__main__':
    TestEnvironment.initialize()
    results = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('DualLfpAdjustmentBase'))
    TestEnvironment.cleanup(results)
