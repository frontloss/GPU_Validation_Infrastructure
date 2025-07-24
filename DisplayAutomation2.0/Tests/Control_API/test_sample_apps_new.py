##
# @file test_sample_apps_new.py
# @brief The script implements unittest default functions for setUp and tearDown, and common test functions given below:
# @details * run_executable_and_capture_log: To run different sample app and capture the logs
#          * runTest: Iterate offer all the apps of particular configuration and parse the logs for ERROR checking
# @author Saurya Suman

import os
import sys
import logging
import unittest
import re
import subprocess

from typing import List
from Libs.Core import display_essential
from Libs.Core.test_env import test_context
from Libs.Feature.powercons import registry
from Libs.Core.test_env.context import Adapter, Panel
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Control_API.control_api_test_base import ControlAPITestBase
from Libs.Core.logger import html
from Libs.Core.vbt import vbt


class Feature:
    APD = "APD"
    ELP = "ELP"
    OPST = "OPST"
    PIXOPTIX = "PIXOPTIX"
    CABC = "CABC"
    NONE = None


# Define the macro for the shared binary folder path
SAMPLE_APPS_PATH = os.path.join(test_context.SHARED_BINARY_FOLDER, r"ControlApi\Release\SampleApp\dump64")


# Dictionary where each configuration maps to a single panel,
# and each panel maps to a list of application executables.
configurations = {
    "config1": {
        "panel": "EDP265",
        "apps": ["PowerFeature_Sample_App.exe", "Color_Sample_App.exe",
                 "ScalingFeature_Sample_App.exe", "DisplaySettings_Sample_App.exe"]
    },
    "config2": {
        "panel": "EDP305",
        "apps": ["PowerFeature_Sample_App.exe"]
    },
    "config3": {
        "panel": "EDP076",
        "apps": ["PowerFeature_Sample_App.exe", "CustomMode_Sample_App.exe"]
    },
    "config4": {
        "panel": "EDP321",
        "apps": ["PowerFeature_Sample_App.exe", "SwPsr_Sample_App"]
    },
    "config5": {
        "panel": "EDP338",
        "apps": ["PowerFeature_Sample_App.exe", "Color_Sample_App.exe"]
    },
    "config6": {
        "panel": "EDP044",
        "apps": ["Scaling_Sample_App.exe"]
    }
}


def run_executable_and_capture_log(executable_path):
    """
        This function runs an executable located at the provided path and captures its log output.
        It logs the captured output and returns it as a string.
        Parameters:
        executable_path (str): The path to the executable file to be run.
        Returns:
        str: The combined standard output and standard error output from running the executable.
    """
    try:
        result = subprocess.run(executable_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
        log_data = result.stdout + result.stderr
        logging.info(log_data)
        return log_data
    except Exception as e:
        logging.error(f"Error running the executable: {e}")
        return ""


def enable_feature_in_vbt(adapter: Adapter.gfx_index, panel: Panel.port_type, feature_list: List[Feature]):
    """
        This function enables specific features in the Video BIOS Table (VBT) for a given adapter and panel.
        It checks the VBT version and feature status before enabling the requested features.
        Returns:
        tuple: A tuple containing a boolean indicating success or failure, and a boolean indicating
         if a driver restart is required.
    """
    do_driver_restart = False

    gfx_vbt = vbt.Vbt(adapter)
    panel_index = gfx_vbt.get_lfp_panel_type(panel)
    html.step_start(f"Enabling {feature_list} feature in VBT for {panel}")

    if Feature.ELP in feature_list:
        if gfx_vbt.version < 247:
            logging.error(f"VBT version of ELP Expected: >247 and current:{gfx_vbt.version}")
            html.step_end()
            return False, do_driver_restart
        # Fetching the initial VBT status
        if bool((gfx_vbt.block_44.ELP[0] & (1 << panel_index)) >> panel_index) is True:
            logging.info(f"{Feature.ELP} feature already enabled in VBT ")
            html.step_end()
        else:
            gfx_vbt.block_44.ELP[0] |= (1 << panel_index)
            do_driver_restart = True

    if Feature.APD in feature_list:
        if gfx_vbt.version < 253:
            logging.error(f"VBT version of APD Expected: >253 and current:{gfx_vbt.version}")
            html.step_end()
            return False, do_driver_restart
        # Fetching the initial VBT status
        if bool((gfx_vbt.block_44.APD[0] & (1 << panel_index)) >> panel_index) is True:
            logging.info(f"{Feature.APD} feature already enabled in VBT")
            html.step_end()
        else:
            gfx_vbt.block_44.APD[0] |= (1 << panel_index)
            do_driver_restart = True

    if Feature.OPST in feature_list:
        if gfx_vbt.version < 247:
            logging.error(f"VBT version of OPST Expected: >247 and current:{gfx_vbt.version}")
            html.step_end()
            return False, do_driver_restart
        # Fetching the initial VBT status
        if bool((gfx_vbt.block_44.OPST[0] & (1 << panel_index)) >> panel_index) is True:
            logging.info(f"{Feature.OPST} feature already enabled in VBT")
            html.step_end()
        else:
            gfx_vbt.block_44.OPST[0] |= (1 << panel_index)
            # With OPST enable, disable DPST in VBT
            gfx_vbt.block_44.DpstEnable[0] &= (0 << panel_index)
            do_driver_restart = True

    if Feature.PIXOPTIX in feature_list:
        if gfx_vbt.version < 247:
            logging.error(f"VBT version of PIXOPTIX Expected: >247 and current:{gfx_vbt.version}")
            html.step_end()
            return False, do_driver_restart
        # Fetching the initial VBT status
        if bool((gfx_vbt.block_44.PixOptix[0] & (1 << panel_index)) >> panel_index) is True:
            logging.info(f"{Feature.PIXOPTIX} feature already enabled in VBT")
            html.step_end()
        else:
            gfx_vbt.block_44.PixOptix[0] |= (1 << panel_index)
            do_driver_restart = True

    if Feature.CABC in feature_list:
        if gfx_vbt.version < 247:
            logging.error(f"VBT version of CABC Expected: >247 and current:{gfx_vbt.version}")
            html.step_end()
            return False, do_driver_restart
        # Fetching the initial VBT status
        if bool((gfx_vbt.block_44.TconBasedBacklightOptimization[0] & (1 << panel_index)) >> panel_index) is True:
            logging.info(f"{Feature.CABC} feature already enabled in VBT")
            html.step_end()
        else:
            gfx_vbt.block_44.TconBasedBacklightOptimization[0] |= (1 << panel_index)
            do_driver_restart = True

    # apply VBT changes when any of the field is updated( i.e. do_driver_restart = True)
    if do_driver_restart:
        if gfx_vbt.apply_changes() is False:
            logging.error(f"{feature_list} Feature changes failed in VBT")
            html.step_end()
            return False, do_driver_restart

    html.step_end()
    return True, do_driver_restart


def disable_feature_in_vbt(adapter, panel, feature_list: List[Feature]):
    """
        This function disables specific features in the Video BIOS Table (VBT) for a given adapter and panel.
        It checks the VBT version and feature status before disabling the requested features.
        Returns:
        tuple: A tuple containing a boolean indicating success or failure, and a boolean indicating
        if a driver restart is required.
    """
    do_driver_restart = True
    gfx_vbt = vbt.Vbt(adapter)
    panel_index = gfx_vbt.get_lfp_panel_type(panel)
    html.step_start(f"Disabling {feature_list} feature in VBT for {panel}")

    if Feature.ELP in feature_list:
        if gfx_vbt.version < 247:
            logging.error(f"VBT version of ELP Expected: >247 and current:{gfx_vbt.version}")
            html.step_end()
            return False, do_driver_restart
        # Fetching the initial VBT status
        if bool((gfx_vbt.block_44.ELP[0] & (1 << panel_index)) >> panel_index) is False:
            logging.info(f"{Feature.ELP} feature already disabled in VBT")
            html.step_end()
            return None, do_driver_restart
        else:
            gfx_vbt.block_44.ELP[0] &= (0 << panel_index)
            do_driver_restart = True

    if Feature.APD in feature_list:
        if gfx_vbt.version < 253:
            logging.error(f"VBT version of APD Expected: >253 and current:{gfx_vbt.version}")
            html.step_end()
            return False, do_driver_restart
        # Fetching the initial VBT status
        if bool((gfx_vbt.block_44.APD[0] & (1 << panel_index)) >> panel_index) is False:
            logging.info(f"{Feature.APD} feature already disabled in VBT")
            html.step_end()
            return None, do_driver_restart
        else:
            gfx_vbt.block_44.APD[0] &= (0 << panel_index)
            do_driver_restart = True

    if Feature.OPST in feature_list:
        if gfx_vbt.version < 247:
            logging.error(f"VBT version of OPST Expected: >247 and current:{gfx_vbt.version}")
            html.step_end()
            return False, do_driver_restart
        # Fetching the initial VBT status
        if bool((gfx_vbt.block_44.OPST[0] & (1 << panel_index)) >> panel_index) is False:
            logging.info(f"{Feature.OPST} feature already disabled in VBT")
            html.step_end()
            return None, do_driver_restart
        else:
            gfx_vbt.block_44.OPST[0] &= (0 << panel_index)
            # With OPST disable, Enable DPST
            gfx_vbt.block_44.DpstEnable[0] |= (1 << panel_index)
            do_driver_restart = True

    if Feature.PIXOPTIX in feature_list:
        if gfx_vbt.version < 253:
            logging.error(f"VBT version of PIXOPTIX Expected: >253 and current:{gfx_vbt.version}")
            html.step_end()
            return False, do_driver_restart
        # Fetching the initial VBT status
        if bool((gfx_vbt.block_44.PixOptix[0] & (1 << panel_index)) >> panel_index) is False:
            logging.info(f"{Feature.PIXOPTIX} feature already disabled in VBT")
            html.step_end()
            return None, do_driver_restart
        else:
            gfx_vbt.block_44.PixOptix[0] &= (0 << panel_index)
            do_driver_restart = True

    if Feature.CABC in feature_list:
        if gfx_vbt.version < 253:
            logging.error(f"VBT version of CABC Expected: >253 and current:{gfx_vbt.version}")
            html.step_end()
            return False, do_driver_restart
        # Fetching the initial VBT status
        if bool((gfx_vbt.block_44.TconBasedBacklightOptimization[0] & (1 << panel_index)) >> panel_index) is False:
            logging.info(f"{Feature.CABC} feature already disabled in VBT")
            html.step_end()
            return None, do_driver_restart
        else:
            gfx_vbt.block_44.TconBasedBacklightOptimization[0] &= (0 << panel_index)
            do_driver_restart = True

    if gfx_vbt.apply_changes() is False:
        logging.error(f"{feature_list} Feature changes failed in VBT")
        html.step_end()
        return False, do_driver_restart

    html.step_end()
    return True, do_driver_restart


class IgclSampleAppTest(ControlAPITestBase):

    ##
    # @brief            Unittest setUp function
    # @return           void
    def setUp(self):

        ##
        # Invoking Common BaseClass's setUp() to perform all the basic functionalities
        super().setUp()

        do_driver_restart = False

        if self.vbt_feature_enable != ['N']:
            for gfx_index, adapter in self.context_args.adapters.items():
                for port, panel in adapter.panels.items():
                    status, do_driver_restart = enable_feature_in_vbt(gfx_index, panel.connector_port_type,
                                                                      self.vbt_feature_enable)
                    if status is False:
                        self.fail(f"FAILED to enable {self.vbt_feature_enable} in VBT")

                if do_driver_restart is True:
                    status, reboot_required = display_essential.restart_gfx_driver()
                    if status is False:
                        logging.error("Failed to restart display driver after VBT update")
                        return False
                vbt.Vbt(gfx_index).reload()

        if self.registry == "ALRR_ENABLE":
            for gfx_index, adapter in self.context_args.adapters.items():
                idt_alrr = registry.DisplayPcFeatureControl(gfx_index)
                if idt_alrr.DisableAlrr != 0:
                    idt_alrr.DisableAlrr = 0
                    status = idt_alrr.update(gfx_index)
                    if status is False:
                        logging.error("\tFAILED to enable ALRR(30th bit) via DisplayPcFeatureControl registry")
                    else:
                        alrr_status, reboot_required = display_essential.restart_gfx_driver()
                        if alrr_status is False:
                            self.fail(f"Failed to do Driver restart post Regkey updates")
                        logging.info("Successfully restarted display driver")
                logging.info("\tSuccessfully enabled ALRR(30th bit) via DisplayPcFeatureControl registry")

    def runTest(self):
        """
            This method executes the test by running specified sample applications based on the configuration.
            It captures log data for each application, checks for errors in the logs, and summarizes the test results.
        """
        config = "config" + self.config_number.lower()

        # Main code
        panel_info = configurations.get(config, None)
        apps = panel_info.get("apps", [])

        logging.info(f"Selected Configuration: {config}")
        logging.info(f"Sample Apps to run: {', '.join(apps)}")

        status = True  # Variable to track overall status
        error_dict = {}  # Dictionary to store errors for each app
        total_apps = len(apps)
        failed_apps = 0
        passed_apps = 0

        for app in apps:
            logging.info(f"---------------------------{app} execution start.---------------------------")
            executable_path = os.path.join(SAMPLE_APPS_PATH, app)
            if app == "Scaling_Sample_App.exe":
                command = f"{executable_path} 1920 1080"
            else:
                command = executable_path
            log_data = run_executable_and_capture_log(command)

            logging.info(f"---------------------------{app} execution end.---------------------------")

            error_dict[app] = []  # Initialize an empty list to store errors for the current app

            for line in log_data.splitlines():
                error_match = re.search(r'\[ERROR\](.*)', line)
                if error_match:
                    error_message = error_match.group(1).strip()
                    logging.error(f"Error detected in log: {error_message}")
                    error_dict[app].append(error_message)
                    status = False  # Set status to False if any error is detected
            if error_dict[app]:
                failed_apps += 1
            else:
                passed_apps += 1

        # Print summary of test results
        logging.info("Test Summary:")
        logging.info(f"Total Apps Run: {total_apps}")
        logging.info(f"Total Apps Passed: {passed_apps}")
        logging.info(f"Total Apps Failed: {failed_apps}")

        # Initialize a list to store the names of apps with no errors
        no_error_apps = []

        # Loop through the error_dict and log errors as needed
        for app, errors in error_dict.items():
            if errors:
                logging.info(f"Errors for {app}:")
                for error in errors:
                    logging.info(f"  - {error}")
            else:
                no_error_apps.append(app)

        # After looping through the dictionary, log the names of all apps with no errors in a single line
        if no_error_apps:
            logging.info(f"No Error : {', '.join(no_error_apps)}")

        if not status:
            self.fail("Test failed due to error in log")

        pass

    ##
    # @brief            Unittest tearDown function
    # @return           void
    def tearDown(self):

        do_driver_restart = False

        if self.vbt_feature_enable != ['N']:
            for gfx_index, adapter in self.context_args.adapters.items():
                for port, panel in adapter.panels.items():

                    status, do_driver_restart = disable_feature_in_vbt(gfx_index,
                                                                       panel.connector_port_type,
                                                                       self.vbt_feature_enable)
                    if status is False:
                        self.fail(f"FAILED to disable {self.vbt_feature_enable} in VBT")

                if do_driver_restart is True:
                    status, reboot_required = display_essential.restart_gfx_driver()
                    if status is False:
                        logging.error("Failed to restart display driver after VBT update")
                        return False
                vbt.Vbt(gfx_index).reload()

        if self.registry == "ALRR_ENABLE":
            for gfx_index, adapter in self.context_args.adapters.items():
                idt_alrr = registry.DisplayPcFeatureControl(gfx_index)
                if idt_alrr.DisableAlrr != 1:
                    idt_alrr.DisableAlrr = 1
                    status = idt_alrr.update(gfx_index)
                    if status is False:
                        logging.error("\tFAILED to Disable ALRR(30th bit) via DisplayPcFeatureControl registry")
                    else:
                        alrr_status, reboot_required = display_essential.restart_gfx_driver()
                        if alrr_status is False:
                            self.fail(f"Failed to do Driver restart post Regkey updates")
                        logging.info("Successfully restarted display driver")
                logging.info("\tSuccessfully disabled ALRR(30th bit) via DisplayPcFeatureControl registry")

        super().tearDown()


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
