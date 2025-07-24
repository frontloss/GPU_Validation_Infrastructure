########################################################################################################################
# @file         control_api_test_base.py
# @brief        This script is a Base class for Control Library and comprises below functions.
#               1. setUp() - Invokes Common class's setUp() to perform basic functionalities
#                            and update the custom tags.
#               2. tearDown() - To unplug the display and restore to default configurations
# @author       Prateek Joshi, Pooja Audichya
########################################################################################################################
import logging
import unittest
import sys

from Tests.test_base import TestBase
from Libs.Feature.crc_and_underrun_verification import UnderRunStatus

MAX_LINE_WIDTH = 64


##
# @brief - Control Library Test Base
class ControlAPITestBase(TestBase):
    power_plan = None
    hw_modeset = False
    igcl_major_version = igcl_minor_version = None

    ##
    # @brief            Unittest setUp function
    # @return           void
    def setUp(self):
        ##
        # Updating the custom tags
        tags_list = ["-PSR_VERSION", "-MATRIX_INFO", "-HW_MODESET", "-EG_CONTROL", "-EG_MODE", "-DX_APP",
                     "-ASYNC_FEATURE",
                     "-IGCL_MAJOR_VERSION", "-IGCL_MINOR_VERSION", "-SAMPLE_APP", "-POWER_PLAN", "-DPST_FEATURE",
                     "-CONFIG_NUM", "-VBT_ENABLE", "-REG"]
        self.custom_tags.update(dict.fromkeys(tags_list, None))

        ##
        # Invoking Common BaseClass's setUp() to perform all the basic functionalities
        super().setUp()

        ##
        # Fetch the user input for control library
        self.psr_version = str(self.context_args.test.cmd_params.test_custom_tags["-PSR_VERSION"][0])
        self.matrix_info = str(self.context_args.test.cmd_params.test_custom_tags["-MATRIX_INFO"][0])
        self.hw_modeset = str(self.context_args.test.cmd_params.test_custom_tags["-HW_MODESET"][0])
        self.eg_control = str(self.context_args.test.cmd_params.test_custom_tags["-EG_CONTROL"][0])
        self.eg_mode = str(self.context_args.test.cmd_params.test_custom_tags["-EG_MODE"][0])
        self.dx_app = str(self.context_args.test.cmd_params.test_custom_tags["-DX_APP"][0])
        self.async_feature = str(self.context_args.test.cmd_params.test_custom_tags["-ASYNC_FEATURE"][0])
        self.igcl_major_version = str(self.context_args.test.cmd_params.test_custom_tags["-IGCL_MAJOR_VERSION"][0])
        self.igcl_minor_version = str(self.context_args.test.cmd_params.test_custom_tags["-IGCL_MINOR_VERSION"][0])
        self.sample_app = str(self.context_args.test.cmd_params.test_custom_tags["-SAMPLE_APP"][0])
        self.power_plan = str(self.context_args.test.cmd_params.test_custom_tags["-POWER_PLAN"][0])
        self.dpst_feature = str(self.context_args.test.cmd_params.test_custom_tags["-DPST_FEATURE"][0])
        self.config_number = str(self.context_args.test.cmd_params.test_custom_tags["-CONFIG_NUM"][0])
        self.vbt_feature_enable = self.context_args.test.cmd_params.test_custom_tags["-VBT_ENABLE"][0].split()
        self.registry = str(self.context_args.test.cmd_params.test_custom_tags["-REG"][0])

        self.underrun = UnderRunStatus()

    ##
    # @brief            Unittest tearDown function
    # @return           void
    def tearDown(self):
        logging.info(" TEARDOWN: CONTROL_API_TEST_BASE ".center(MAX_LINE_WIDTH, "*"))
        super().tearDown()
