########################################################################################################################
# @file         test_get_set_sharpness.py
# @brief        Test calls for Get, Set Sharpness and Get Sharpness Caps through Control Library.
#                   * Get Sharpness API.
#                   * Set Sharpness API.
#                   * Get Sharpness Caps API.
# @author       Prateek Joshi
########################################################################################################################

import ctypes
import sys
import unittest
import logging

from Libs.Core import enum
from Libs.Core.logger import gdhm
from Libs.Core.machine_info import machine_info
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.wrapper import control_api_wrapper
from Libs.Core.wrapper import control_api_args
from Libs.Core.display_config import display_config
from Tests.Control_API.control_api_test_base import ControlAPITestBase

# Current Platform name
PLATFORM_NAME = machine_info.SystemInfo().get_gfx_display_hardwareinfo()[0].DisplayAdapterName
ADAPTIVE = ['LNL']


##
# @brief - Verify Get-Set Sharpness API Control Library Test
class TestSharpnessAPI(ControlAPITestBase):

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):
        target_id_list = []
        logging.info("Test: Get-Set Sharpness via Control Library")
        filter_type = control_api_args.ctl_sharpness_filter_type_flags_t.ADAPTIVE.value \
            if PLATFORM_NAME in ADAPTIVE else control_api_args.ctl_sharpness_filter_type_flags_t.NON_ADAPTIVE.value

        setSharpness = control_api_args.ctl_sharpness_settings()
        setSharpness.Size = ctypes.sizeof(setSharpness)
        setSharpness.FilterType = filter_type
        setSharpness.Enable = 1
        setSharpness.Intensity = 85
        logging.info("Step_1: Set Sharpness")
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active:
                    if control_api_wrapper.set_sharpness(setSharpness, panel.target_id):
                        logging.info("Pass: Set Sharpness Intensity-{} via Control Library"
                                     .format(setSharpness.Intensity))
                    else:
                        logging.error("Fail: Set Sharpness via Control Library")
                        gdhm.report_driver_bug_clib("Set Sharpness Failed via Control Library - "
                                                    "Sharpness Enable: {0} Intensity: {1} FilterType: {2}"
                                                    .format(setSharpness.Enable, setSharpness.Intensity,
                                                            setSharpness.FilterType))
                        self.fail("Set Sharpness Failed via Control Library")

        logging.info("Apply native mode with Zero Rotation")
        ##
        # fetch the display configuration of all the displays connected
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active:
                    target_id_list.append(panel.target_id)

        # fetch all the modes supported by each of the displays connected
        supported_modes = display_config.DisplayConfiguration().get_all_supported_modes(target_id_list)
        for key, values in supported_modes.items():
            mode = values[0]
            mode.rotation = enum.ROTATE_0
            # Apply Native mode with zero rotation
            display_config.DisplayConfiguration().set_display_mode([mode], virtual_mode_set_aware=False,
                                                                   force_modeset=True)
            logging.info("Successfully applied display mode {0} X {1} @ {2} Scaling : {3} Rotation: {4}".format(
                mode.HzRes, mode.VtRes, mode.refreshRate, mode.scaling, mode.rotation))

        getSharpness = control_api_args.ctl_sharpness_settings()
        getSharpness.Size = ctypes.sizeof(getSharpness)
        getSharpness.FilterType = filter_type

        logging.info("Step_2: Get Sharpness")
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active:
                    if control_api_wrapper.get_sharpness(getSharpness, panel.target_id):
                        logging.info("Pass: Get Sharpness via Control Library")
                        if getSharpness.Intensity == setSharpness.Intensity:
                            logging.info("Pass: Get Sharpness Intensity-{} matched with Set Sharpness via Control "
                                         "Library".format(getSharpness.Intensity))
                        else:
                            gdhm.report_driver_bug_clib("Get Sharpness Intensity Failed to match Set Sharpness via "
                                                        "Control Library Expected: {0} Actual: {1}"
                                                        .format(setSharpness.Intensity, getSharpness.Intensity))
                            self.fail("Get Sharpness Intensity failed to match via Control Library")
                    else:
                        logging.error("Fail: Get Sharpness via Control Library")
                        gdhm.report_driver_bug_clib("Get Sharpness Failed via Control Library for "
                                                    "Sharpness Enable: {0} Intensity: {1} FilterType: {2}"
                                                    .format(getSharpness.Enable, getSharpness.Intensity,
                                                            getSharpness.FilterType))
                        self.fail("Get Sharpness Failed via Control Library")

        logging.info("Step_3: Negative verification for Set Sharpness")
        setSharpness = control_api_args.ctl_sharpness_settings()
        setSharpness.Size = ctypes.sizeof(setSharpness)
        setSharpness.FilterType = filter_type
        setSharpness.Enable = 1
        setSharpness.Intensity = 220

        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active:
                    if not control_api_wrapper.set_sharpness(setSharpness, panel.target_id):
                        logging.info("Pass: Negative Test to Set Sharpness Intensity-{} via Control Library".format(
                            setSharpness.Intensity))
                    else:
                        logging.error("Fail: Negative Test to Set Sharpness via Control Library")
                        gdhm.report_driver_bug_clib("Negative verification to Set Sharpness Failed via Control "
                                                    "Library - Sharpness Enable: {0} Intensity: {1} FilterType: {2}"
                                                    .format(setSharpness.Enable, setSharpness.Intensity,
                                                            setSharpness.FilterType))
                        self.fail("Set Sharpness Failed via Control Library")

    ##
    # @brief            Unittest tearDown function
    # @return           void
    def tearDown(self):
        logging.info(" TEARDOWN: testSharpnessAPI ")
        super(TestSharpnessAPI, self).tearDown()


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info('Test purpose: Control Library Sharpness Verification')
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
