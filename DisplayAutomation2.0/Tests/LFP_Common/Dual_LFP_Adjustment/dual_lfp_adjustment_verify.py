########################################################################################################################
# @file         dual_lfp_adjustment_verify.py
# @brief        This file contains helper functions for dual lfp adjustment verification tests.
# @details      It sets the border value for dual LFP panels in VBT, and verifies scalar registers programming.
#               This is a feature to fix the misalignment issue between the two panels.
#               The misalignment is fixed by adjusting the frame.
#               CommandLine: python dual_lfp_adjustment_verify.py -mipi_a -mipi_c -border 100 -panel1 top -panel2 bottom
# @author       Sri Sumanth Geesala
########################################################################################################################
import logging
import sys
import time
import unittest

from Libs.Core import cmd_parser, reboot_helper
from Libs.Core.display_power import DisplayPower
from Libs.Core.logger import gdhm
from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.vbt.vbt import Vbt
from Libs.Feature.display_engine.de_base.display_base import DisplayBase
from registers.mmioregister import MMIORegister


##
# @brief        This is a decorator class to determine number of calls for a method
class callcounted(object):
    """Decorator to determine number of calls for a method"""

    ##
    # @brief        Initializer function to set count value
    # @param[in]    method - method whose calls are to be counted
    def __init__(self, method):
        self.method = method
        self.counter = 0

    ##
    # @brief        Method to increment the count whenever a method is called
    # @param[in]    *args method arguments
    # @param[in]    *kwargs method arguments
    # @return       method
    def __call__(self, *args, **kwargs):
        self.counter += 1
        return self.method(*args, **kwargs)


##
# @brief        Exposed Class for Dual LFP Adjustment tests. Any new Dual LFP Adjustment test can inherit this class
#               to use common setUp and tearDown functions. This class also includes some functions used across all
#               Dual LFP Adjustment tests.
class DualLfpAdjustmentVerify(unittest.TestCase):
    display_power = DisplayPower()
    machine_info = SystemInfo()

    ##
    # @brief        This class method is the entry point for Dual LFP Adjustment test cases which inherit this class.
    #               It helps to initialize some of the parameters required for Dual LFP Adjustment test execution.
    # @details      This function gets the platform info, parses command line arguments for display list and custom tags
    # @return       None
    @reboot_helper.__(reboot_helper.setup)
    def setUp(self):
        logging.info("Starting Test Setup")
        self.my_custom_tags = ['-border', '-panel1', '-panel2']
        self.gfx_vbt = Vbt()
        logging.error = callcounted(logging.error)
        self.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, self.my_custom_tags)
        self.displays_in_cmdline = []
        self.panel1_index = -1
        self.panel2_index = -1
        self.platform = None
        self.border_value = 0
        self.panel1_border_pos = ''
        self.panel2_border_pos = ''
        self.panel1_index = 0
        self.panel2_index = 0

        ##
        # get platform
        gfx_display_hwinfo = self.machine_info.get_gfx_display_hardwareinfo()
        # WA : currently test are execute on single platform. so loop break after 1 st iteration.
        # once Enable MultiAdapter remove the break statement.
        for i in range(len(gfx_display_hwinfo)):
            self.platform = ("%s" % gfx_display_hwinfo[i].DisplayAdapterName).lower()
            break

        ##
        # process cmdline for display list and custom tags
        for key, value in self.cmd_line_param.items():
            if cmd_parser.display_key_pattern.match(key) is not None:
                if value['connector_port'] is not None:
                    self.displays_in_cmdline.append(value['connector_port'])
            if key == 'BORDER':
                self.border_value = int(value[0], 10)
            if key == 'PANEL1':
                self.panel1_border_pos = value[0].lower()
            if key == 'PANEL2':
                self.panel2_border_pos = value[0].lower()
        self.panel_borders_pos = [self.panel1_border_pos, self.panel2_border_pos]

    ##
    # @brief        This method is the exit point for Dual LFP Adjustment tests. This checks for errors in the test
    #               execution and reports if any
    # @return       None
    @reboot_helper.__(reboot_helper.teardown)
    def tearDown(self):
        logging.info("Starting Test Cleanup")

        ##
        # report test failure if fail_count>0
        if (logging.error.counter > 0):
            self.fail(
                "Some checks in the test have failed. Check error logs. No. of failures= %d" % logging.error.counter)

    ##
    # @brief        Function to get panel index for port
    # @param[in]    port port to which the panel is attached
    # @return       panel_index if found, -1 otherwise
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
    # @param[in]    port port to which the panel is attached
    # @param[in]    top_border  number
    # @param[in]    bottom_border number
    # @param[in]    left_border number
    # @param[in]    right_border number
    # @return       True if filling of values in vbt is successful, False otherwise
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
    # @param[in]    port port to which the panel is attached
    # @param[in]    top_border  number
    # @param[in]    bottom_border number
    # @param[in]    left_border number
    # @param[in]    right_border number
    # @return       None
    def verify_scalar_registers(self, port, top_border=0, bottom_border=0, left_border=0, right_border=0):

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
            gdhm.report_bug(
                title="[LFP][DUAL_LFP_ADJUSTMENT] PS_CTRL enable-scalar field is disabled which is not expected",
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.error(
                'FAIL: PS_CTRL for port {0} - enable_scaler : Expected= enabled \t Actual= disabled'.format(port))
            return
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
            gdhm.report_bug(
                title="[LFP][DUAL_LFP_ADJUSTMENT] PS_WIN_SZ xsize field is programmed wrong",
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.error('FAIL: PS_WIN_SZ_{0}_{1} - xsize : Expected= {2} \t Actual= {3}'.format(scalar_num, pipe,
                                                                                                  expected_xsize,
                                                                                                  ps_win_sz.xsize))
        if ps_win_sz.ysize == expected_ysize:
            logging.info('PASS: PS_WIN_SZ_{0}_{1} - ysize : Expected= {2} \t Actual= {3}'.format(scalar_num, pipe,
                                                                                                 expected_ysize,
                                                                                                 ps_win_sz.ysize))
        else:
            gdhm.report_bug(
                title="[LFP][DUAL_LFP_ADJUSTMENT] PS_WIN_SZ ysize field is programmed wrong",
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
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
            gdhm.report_bug(
                title="[LFP][DUAL_LFP_ADJUSTMENT] PS_WIN_POS xpos field is programmed wrong",
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.error('FAIL: PS_WIN_POS_{0}_{1} - xpos : Expected= {2} \t Actual= {3}'.format(scalar_num, pipe,
                                                                                                  expected_xpos,
                                                                                                  ps_win_pos.xpos))
        if ps_win_pos.ypos == expected_ypos:
            logging.info('PASS: PS_WIN_POS_{0}_{1} - ypos : Expected= {2} \t Actual= {3}'.format(scalar_num, pipe,
                                                                                                 expected_ypos,
                                                                                                 ps_win_pos.ypos))
        else:
            gdhm.report_bug(
                title="[LFP][DUAL_LFP_ADJUSTMENT] PS_WIN_POS ypos field is programmed wrong",
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.error('FAIL: PS_WIN_POS_{0}_{1} - ypos : Expected= {2} \t Actual= {3}'.format(scalar_num, pipe,
                                                                                                  expected_ypos,
                                                                                                  ps_win_pos.ypos))

    ##
    # @brief        Function to fill vbt with border values as per the command line.
    # @return       None
    def test_configure_borders_in_vbt(self):

        # fill vbt with border values as per command line
        for index in range(len(self.displays_in_cmdline)):
            top = 0
            bottom = 0
            if self.panel_borders_pos[index] == 'top':
                top = self.border_value
            elif self.panel_borders_pos[index] == 'bottom':
                bottom = self.border_value
            else:
                self.fail('{0} for border not supported'.format(self.panel_borders_pos[index]))

            self.fill_border_values_in_vbt(self.displays_in_cmdline[index], top_border=top, bottom_border=bottom)

        # make vbt API call to set vbt with self.gfx_vbt.block_42
        logging.info('Setting border values in VBT')
        if self.gfx_vbt.apply_changes() is False:
            self.fail('Setting VBT block failed')

        # do system reboot
        if reboot_helper.reboot(self, 'test_verify_scalar_registers') is False:
            self.fail("Failed to reboot the system")

    ##
    # @brief        Function to verify scalar register programming
    # @return       None
    def test_verify_scalar_registers(self):

        # verify scalar registers
        for index in range(len(self.displays_in_cmdline)):
            top = 0
            bottom = 0
            if self.panel_borders_pos[index] == 'top':
                top = self.border_value
            elif self.panel_borders_pos[index] == 'bottom':
                bottom = self.border_value
            else:
                self.fail('{0} for border not supported'.format(self.panel_borders_pos[index]))

            self.verify_scalar_registers(self.displays_in_cmdline[index], top_border=top, bottom_border=bottom)

        logging.info("Test sleeping for 10 sec. Please check visual verification of border during this time !!")
        time.sleep(10)

        # reset vbt
        logging.info('Resetting VBT to default state')
        if Vbt().reset() is False:
            self.fail('Reset Vbt failed')

        if reboot_helper.reboot(self, 'test_after_vbt_reset') is False:
            self.fail("Failed to reboot the system")

    ##
    # @brief        Function to verify dsc
    # @return       None
    def test_after_vbt_reset(self):
        logging.info('Verification ended')


if __name__ == '__main__':
    TestEnvironment.initialize()
    results = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('DualLfpAdjustmentVerify'))
    TestEnvironment.cleanup(results)
