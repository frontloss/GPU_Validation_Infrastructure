########################################################################################################################
# @file         dmrrs_reg_key.py
# @addtogroup   PowerCons
# @section      DMRRS_Tests
# @brief        Contains DMRRS test to check if the DMRRS is getting disabled using the reg key
#
# @author       Mukesh
########################################################################################################################

import random

from Libs.Core.test_env import test_environment

from Tests.PowerCons.Functional.DMRRS.dmrrs_base import *
from Tests.PowerCons.Modules import workload


##
# @brief        Contains tests to check DMRRS disabling through registry
class DmrrsRegKeyTest(DmrrsBase):

    ##
    # @brief        This function verifies DMRRS before and after disabling it in the external registry key
    #               DisplayPcFeatureControl
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["EXTERNAL_REG_KEY", "23.976", "29.970", "59.940", "24", "25", "30"])
    # @endcond
    def t_11_external_reg_key_test(self):

        # Choose fps of the video randomly if it's not specified in command line
        if self.is_fractional_rr:
            if self.cmd_line_param[0]['SELECTIVE2'][0] in ["23.976", "29.970", "59.940"]:
                media_fps = float(self.cmd_line_param[0]['SELECTIVE2'][0])
            else:
                media_fps = random.choice(self.FRACTIONAL_FPS)
        else:
            if self.cmd_line_param[0]['SELECTIVE2'][0] in ["24", "25", "30"]:
                media_fps = int(self.cmd_line_param[0]['SELECTIVE2'][0])
            else:
                media_fps = random.choice(self.NORMAL_FPS)

        etl_file_path, _ = workload.run(workload.VIDEO_PLAYBACK, [media_fps, 30])

        is_lfp = False
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                is_lfp = True if panel.is_lfp else False
                self.dmrrs_hrr_verification(adapter, panel, etl_file_path, media_fps)

        status = True
        # List of adapters where the DMRRS is disabled by default
        dmrrs_disabled_in_adapters = []

        # Disable DMRRS in the reg key
        for adapter in dut.adapters.values():
            # disable DMRRS through reg key and check if we are getting a non-zero duration or not.
            dmrrs_disable_status = dmrrs.configure_dmrrs_exposed_reg_key(adapter, False, is_lfp)
            if dmrrs_disable_status is False:
                logging.error(f"FAILED to disable DMRRS on {adapter.gfx_index}")
                status &= False
            elif dmrrs_disable_status is None:
                # DMRRS is already disabled on adapter
                dmrrs_disabled_in_adapters.append(adapter.gfx_index)
            else:
                logging.info(f"DMRRS is disabled on {adapter.gfx_index}")

        # Play a video
        etl_file_path, _ = workload.run(workload.VIDEO_PLAYBACK, [media_fps, 30])

        html.step_start("Verifying Non-Zero duration flips after DMRRS disable")
        # Add Check to ensure OS is not sending any non-zero duration
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                # Check if there are any non-zero duration flips in the ETL after DMRRS disable
                if dmrrs.is_non_zero_duration_flip_present(panel, etl_file_path):
                    logging.error(f"FAIL: Non-zero duration flip present after disabling DMRRS for {panel.port}")
                    status &= False
                else:
                    logging.info(f"PASS: No non-zero duration flips found after disabling DMRRS for {panel.port}")
        html.step_end()

        # Enable DMRRS in registry
        for adapter in dut.adapters.values():
            # Check if DMRRS was disabled by default in adapter
            if adapter.gfx_index in dmrrs_disabled_in_adapters:
                continue
            # Enable DMRRS through reg key and check if we are getting a non-zero duration or not
            elif dmrrs.configure_dmrrs_exposed_reg_key(adapter, True, is_lfp) is False:
                logging.error(f"Failed to enable DMRRS on {adapter}")
                status &= False

        # Play a video
        etl_file_path, _ = workload.run(workload.VIDEO_PLAYBACK, [media_fps, 30])

        # Verify dmrrs after enabling the DMRRS in registry
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                self.dmrrs_hrr_verification(adapter, panel, etl_file_path, media_fps)

        # Fail after enabling DMRRS, else next test in job might be affected
        if status is False:
            self.fail("FAIL: DMRRS verification with reg key changes failed")
        logging.info("PASS: DMRRS verification with reg key changes passed")

    ##
    # @brief        This function verifies DMRRS before and after disabling it in the internal registry key
    #               MediaRefreshRateSupport
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["INTERNAL_REG_KEY", "23.976", "29.970", "59.940", "24", "25", "30"])
    # @endcond
    def t_12_internal_reg_key_test(self):
        # Choose fps of the video randomly
        if self.is_fractional_rr:
            if self.cmd_line_param[0]['SELECTIVE2'][0] in ["23.976", "29.970", "59.940"]:
                media_fps = float(self.cmd_line_param[0]['SELECTIVE2'][0])
            else:
                media_fps = random.choice(self.FRACTIONAL_FPS)
        else:
            if self.cmd_line_param[0]['SELECTIVE2'][0] in ["24", "25", "30"]:
                media_fps = int(self.cmd_line_param[0]['SELECTIVE2'][0])
            else:
                media_fps = random.choice(self.NORMAL_FPS)

        etl_file_path, _ = workload.run(workload.VIDEO_PLAYBACK, [media_fps, 30])

        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                self.dmrrs_hrr_verification(adapter, panel, etl_file_path, media_fps)

        # Disabling DMRRS through reg key and check if we are getting a non-zero duration or not.
        for adapter in dut.adapters.values():
            dmrrs_status = dmrrs.configure_dmrrs_internal_reg_key(adapter, enable_dmrrs=False)
            if dmrrs_status is False:
                self.fail(f"Failed to disable DMRRS for {adapter.name}")
            logging.info(f"DMRRS is disabled on {adapter.name}")
            if dmrrs_status is True:
                result, reboot_required = display_essential.restart_gfx_driver()
                if result is False:
                    self.fail(f"Failed to restart display driver for {adapter.name}")
                logging.info(f"\tSuccessfully to restart display driver for {adapter.name}")

        # Play a video
        etl_file_path, _ = workload.run(workload.VIDEO_PLAYBACK, [media_fps, 30])

        status = True
        html.step_start("Verifying Non-Zero duration flips after DMRRS disable")
        # Add Check to ensure OS is not sending any non-zero duration
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                # Check if there are any non-zero duration flips in the ETL after DMRRS disable
                if dmrrs.is_non_zero_duration_flip_present(panel, etl_file_path):
                    logging.error(f"FAIL: Non-zero duration flip present after disabling DMRRS for {panel.port}")
                    status &= False
                else:
                    logging.info(f"PASS: No non-zero duration flips found after disabling DMRRS for {panel.port}")
        html.step_end()

        # Enable DMRRS in registry
        for adapter in dut.adapters.values():
            # Enable DMRRS through reg key and check if we are getting a non-zero duration or not
            if dmrrs.enable(adapter) is False:
                logging.error(f"Failed to enable DMRRS on {adapter} through the MediaRefreshRate Support Reg Key")
                status &= False

        # Play a video
        etl_file_path, _ = workload.run(workload.VIDEO_PLAYBACK, [media_fps, 30])

        # Verify dmrrs after enabling the DMRRS in registry
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                self.dmrrs_hrr_verification(adapter, panel, etl_file_path, media_fps)

        # Fail after enabling DMRRS, else next test in job might be affected
        if status is False:
            self.fail("FAIL: DMRRS verification with reg key changes failed")
        logging.info("PASS: DMRRS verification with reg key changes passed")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.runner.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(DmrrsRegKeyTest))
    test_environment.TestEnvironment.cleanup(test_result)
