#######################################################################################################################
# @file         fbc_base.py
# @brief        Contains FBC verification APIs
# @details      @ref fbc_base.py <br>
# #             This file implements unittest default functions for setUp and tearDown, common test functions used
# #             across all FBC tests, and helper functions.
#
# @author       Chandrakanth Reddy y
#######################################################################################################################

import logging
import sys
import unittest

from Libs.Feature.display_fbc import fbc
from Libs.Core import cmd_parser, display_essential
from Libs.Core.logger import gdhm
from Libs.Core.display_config.display_config import DisplayConfiguration
from Tests.PowerCons.Modules import common
from Tests.PowerCons.Modules import dut
from registers.mmioregister import MMIORegister


##
# @brief        Exposed Class to write FBC tests. Any new FBC test can inherit this class to use common setUp and
#               tearDown functions. FbcBase also includes some functions used across all FBC tests.
class FbcBase(unittest.TestCase):
    cmd_line_param = None
    source_id = []
    no_of_displays = 0
    pixel_format_p1 = None
    pixel_format_p2 = None
    pixel_format_p3 = None
    display_config_ = DisplayConfiguration()
    is_custom_plane_size_test = False

    ##
    # @brief        This class method is the entry point for FBC test cases. Helps to initialize some of the
    #               parameters required for FBC test execution.
    # @return       None
    @classmethod
    def setUpClass(cls):
        cls.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, custom_tags=common.CUSTOM_TAGS + ['-INPUT_PIXELFORMAT'])
        # Example for Pixel formats in command line : P1_B8G8R8A8 / P2_NV12YUV420
        if cls.cmd_line_param['INPUT_PIXELFORMAT'] != 'NONE':
            for pixel in cls.cmd_line_param['INPUT_PIXELFORMAT']:
                if "P1" in pixel:
                    cls.pixel_format_p1 = 'PIXEL_FORMAT_' + pixel.split('_')[1]
                elif "P2" in pixel:
                    cls.pixel_format_p2 = 'PIXEL_FORMAT_' + pixel.split('_')[1]
                elif "P3" in pixel:
                    cls.pixel_format_p3 = 'PIXEL_FORMAT_' + pixel.split('_')[1]

        if 'SELECTIVE' in cls.cmd_line_param:
            if "CUSTOM_PLANE_SIZE_TEST" in cls.cmd_line_param['SELECTIVE']:
                cls.is_custom_plane_size_test = True

        dut.prepare(pruned_mode_list=False)

        current_config = cls.display_config_.get_current_display_configuration()
        cls.no_of_displays = current_config.numberOfDisplays
        for index in range(0, cls.no_of_displays):
            cls.source_id.append(index)
        
        FbcBase.verify_test_control_flag()

    ##
    # @brief        This method is the exit point for FBC test cases. This resets the environment changes done
    #               for execution of FBC tests
    # @return       None
    @classmethod
    def tearDownClass(cls):
        dut.reset()
        FbcBase.verify_test_control_flag()

    ##
    # @brief        This function is used to verify test control flag
    # @return       None
    @staticmethod
    def verify_test_control_flag():
        for adapter in dut.adapters.values():
            fbc_enable_status = fbc.enable(adapter.gfx_index)
            if fbc_enable_status is False:
                assert fbc_enable_status, f"Failed to enable FBC on {adapter.gfx_index}"
            if fbc_enable_status is True:
                driver_restart_status, system_reboot_required = display_essential.restart_gfx_driver()
                assert driver_restart_status, "Failed to restart graphics driver"
            logging.info(f"SUCCESS : FBC enable on the adapter {adapter.gfx_index}")


    ##
    # @brief       API to verify FBC concurrency with PSR
    # @param[in]   adapter adapter object
    # @param[in]   panel panel object
    # @return      result - True if FBC is disabled when PSR2 panel is connected, False otherwise
    def check_fbc_psr_concurrency(self, adapter, panel):
        # For Pre-Gen15 platforms FBC should be disabled when PSR supported panel is connected
        if fbc.get_fbc_enable_status(adapter.gfx_index, panel.pipe):
            gdhm.report_driver_bug_pc(title="[Powercons] [FBC] FBC not disabled for PSR supported panel")
            logging.error("FAIL : FBC is not disabled in driver when PSR supported panel connected")
            return False
        logging.info("PASS : FBC is disabled when PSR panel is connected")
        return True


##
# @brief       verify FBC is supported on given panel & Adapter
# @param[in]   adapter adapter object
# @param[in]   panel panel object
# @return      result - True if FBC is supported, False otherwise
def check_fbc_support(adapter, panel):
    if adapter.name in ['MTL', 'ELG', 'LNL']:
        if panel.pipe not in ['A', 'B']:
            return False
    elif panel.pipe != 'A':
        return False
    return True


##
# @brief       Verify FBC status based on polling data
# @param[in]   adapter adapter object
# @param[in]   panel panel object
# @param[in]   polling_data FBC registers polling data
# @return      True if FBC is disabled otherwise False
def verify_fbc_with_flip_queue(adapter, panel, polling_data):
    fbc_ctl = get_fbc_reg_instance(adapter, panel)
    for val in polling_data[0][fbc_ctl.offset]:
        fbc_ctl.asUint = val
        if fbc_ctl.enable_fbc:
            logging.error("FBC is enabled with Flip Queue")
            gdhm.report_driver_bug_pc("[Powercons][FBC] FBC is enabled with Flip Queue")
            return False
    logging.info("PASS: FBC is disabled in driver")
    return True


##
# @brief       Get FBC resister instance for given Adapter
# @param[in]   adapter adapter object
# @param[in]   panel panel object
# @return      fbc_ctl_reg fbc register instance
def get_fbc_reg_instance(adapter, panel):
    if adapter.name in common.PRE_GEN_14_PLATFORMS:
        fbc_ctl_reg = MMIORegister.get_instance('FBC_CTL_REGISTER', 'FBC_CTL', adapter.name)
    else:
        fbc_ctl_reg = MMIORegister.get_instance('FBC_CTL_REGISTER', 'FBC_CTL_' + panel.pipe, adapter.name)
    return fbc_ctl_reg
