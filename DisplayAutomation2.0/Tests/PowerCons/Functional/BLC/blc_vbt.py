########################################################################################################################
# @file         blc_vbt.py
# @brief        Test for BLC verification by fetching supported brightness from VBT
#
# @author       Ashish Tripathi
########################################################################################################################
import logging
import math

from Libs.Core.logger import gdhm
from Libs.Core.test_env import test_environment
from Libs.Core.vbt import vbt

from Tests.PowerCons.Functional.BLC.blc_base import *
from Tests.PowerCons.Modules import validator_runner

BRIGHTNESS_LIST = [1, 0, 100, 30, 0]


##
# @brief        This class contains BLC tests with VBT
class BlcVbt(BlcBase):
    min_brightness = 5500
    temp_adapter = None
    gfx_vbt = None

    ##
    # @brief        This class method is the entry point for BLC VBT test cases. Helps to initialize some of the
    #               parameters required for BLC VBT test execution. It is defined in unittest framework and being
    #               overridden here.
    # @details      This function checks for supported version of  VBT
    # @return       None
    @classmethod
    def setUpClass(cls):
        super(BlcVbt, cls).setUpClass()

        for gfx_index, adapter in dut.adapters.items():
            cls.gfx_vbt = vbt.Vbt(gfx_index)
            cls.vbt_version = cls.gfx_vbt.version
            if cls.vbt_version < 191:
                gdhm.report_bug(
                    f"[PowerCons][BLC] BLC VBT test is running on unsupported VBT version {cls.vbt_version}",
                    gdhm.ProblemClassification.OTHER,
                    gdhm.Component.Test.DISPLAY_POWERCONS,
                    gdhm.Priority.P3,
                    gdhm.Exposure.E3
                )
                assert False, f"BLC VBT test is unsupported VBT version {cls.vbt_version}"

    ##
    # @brief        This test function verifies BLC with VBT Configure and verify
    # @return       None
    def test_blc_vbt(self):
        self.setup_and_validate_blc()
        self.vbt_configure_and_verify()

    ##
    # @brief        This functionality for vbt workload and verify
    # @return       None
    def vbt_configure_and_verify(self):
        status = True
        # For VBT >=236, Driver can work for both VBT settings
        # 1. (0-65535, 16 bit), (0-255, 8 bit)
        # 2. Default setting (0-255, 8 bit)
        for adapter in dut.adapters.values():
            # verify with default settings
            if self.verify_vbt(adapter) is False:
                self.fail("Fail: Verify VBT Failed")

            # 1. (0-65535, 16 bit), (0 - 255, 8 bit)
            if self.vbt_version >= 236:
                self.min_brightness = 5500
                precision_bit = blc.VbtBlcPrecisionBit.BIT_PRECISION_16
            else:
                self.min_brightness = 15
                precision_bit = blc.VbtBlcPrecisionBit.BIT_PRECISION_8

            self.gfx_vbt, reboot_required, status = blc.configure_vbt(adapter, self.min_brightness, precision_bit)

            if status is False:
                assert False, "FAILED to restart display driver after VBT update"
            elif status and reboot_required:
                if reboot_helper.reboot(self, 'reboot_after_configuring_min_brightness') is False:
                    self.fail("Failed to reboot the system")
            elif status and reboot_required is False:
                # verify with updated settings
                if blc.verify_backlight_vbt(adapter, self.gfx_vbt,
                                            self.min_brightness) is False:
                    assert False, "\t Fail: Post Configure VBT, BLC VBT verification failed"

                if self.verify_vbt(adapter, self.min_brightness) is False:
                    assert False, "\t Fail: BLC VBT verification failed"

                # 2. Update default settings
                self.min_brightness = 6
                precision_bit = blc.VbtBlcPrecisionBit.BIT_PRECISION_8
                self.gfx_vbt, reboot_required, status = blc.configure_vbt(adapter, self.min_brightness, precision_bit)

                if status is False:
                    status = False
                    continue
                elif status and reboot_required:
                    if reboot_helper.reboot(self, 'reboot_after_default_min_brightness') is False:
                        self.fail("Failed to reboot the system")

                elif status and reboot_required is False:
                    # verify again with updated default settings
                    logging.info("Step 4 --------------------")
                    if blc.verify_backlight_vbt(adapter, self.gfx_vbt,
                                                self.min_brightness) is False:
                        self.fail("Fail: VBT verification failed")
                    if self.verify_vbt(adapter, self.min_brightness) is False:
                        self.fail("Fail: VBT verification failed")
                    if status is False:
                        self.fail("FAIL: VBT BLC feature verification")
                    logging.info("PASS: VBT BLC feature verification")

    ##
    # @brief        Reboot functionality to handle after configure vbt
    # @return       None
    def reboot_after_configuring_min_brightness(self):

        logging.info("reboot_after_configuring_min_brightness")
        dut.prepare()
        self.test_adapter = dut.adapters['gfx_0']
        if blc.verify_backlight_vbt(self.test_adapter, self.gfx_vbt,
                                    self.min_brightness) is False:
            status = False
            self.fail("Fail: VBT verification failed")
        if self.verify_vbt(self.test_adapter, self.min_brightness) is False:
            status = False
            self.fail("Fail: VBT verification failed")

        self.min_brightness = 6
        precision_bit = blc.VbtBlcPrecisionBit.BIT_PRECISION_8
        self.gfx_vbt, reboot_required, status = blc.configure_vbt(self.test_adapter, self.min_brightness, precision_bit)

        if status is False:
            self.fail("Fail: VBT verification failed")
        elif status and reboot_required:
            if reboot_helper.reboot(self, 'reboot_after_default_min_brightness') is False:
                self.fail("Failed to reboot the system")
        elif status and reboot_required is False:
            # verify with updated settings
            if blc.verify_backlight_vbt(self.test_adapter, self.gfx_vbt,
                                        self.min_brightness) is False:
                self.fail("Fail: VBT verification failed")
            if self.verify_vbt(self.test_adapter, self.min_brightness) is False:
                self.fail("Fail: VBT verification failed")
        if status is False:
            self.fail("FAIL: VBT BLC feature verification")
        logging.info("PASS: VBT BLC feature verification")

    ##
    # @brief        After reboot functionality
    # @return       None
    def reboot_after_default_min_brightness(self):
        status = True
        self.min_brightness = 6
        dut.prepare()
        self.test_adapter = dut.adapters['gfx_0']
        logging.info("reboot after default min brightness")
        # verify again with updated default settings
        if blc.verify_backlight_vbt(self.test_adapter, self.gfx_vbt,
                                    self.min_brightness) is False:
            self.fail("Fail: VBT verification failed")
        if self.verify_vbt(self.test_adapter, self.min_brightness) is False:
            self.fail("Fail: VBT verification failed")
        if status is False:
            self.fail("FAIL: VBT BLC feature verification")
        logging.info("PASS: VBT BLC feature verification")

    ##
    # @brief        This is a helper function to verify BLC with VBT
    # @param[in]    adapter Adapter object
    # @param[in]    expected_min_brightness [optional] indicates the minimum expected brightness
    # @return       status - True if passes, False otherwise
    def verify_vbt(self, adapter, expected_min_brightness=None):
        brightness_args = [self.is_pwm_based, self.nit_ranges, self.is_high_precision, self.hdr_state, BRIGHTNESS_LIST,
                           self.lfp1_port, self.disable_boost_nit_ranges, self.is_invalid_inf_nit_range,
                           self.disable_nits_brightness, self.independent_brightness]

        workload_status = blc.run_workload(adapter, blc.Scenario.AC_DC_SWITCH, brightness_args)
        if workload_status[1] is False:
            self.fail("FAILED to run the workload")

        if workload_status[0] is None:
            self.fail("ETL file not found")
        html.step_start("VERIFICATION PHASE")

        json_output = validator_runner.run_diana(self.cmd_test_name, workload_status[0], ['BLC'])
        if json_output is None:
            self.fail("JSON file not found")

        status = True
        vbt_precision_bits = blc.VbtBlcPrecisionBit.BIT_PRECISION_8.value
        comp_blc = blc.BlcEtlEvent.COMPUTE_BRIGHTNESS
        blc_value = blc.BlcEtlField.ACTUAL_BRIGHTNESS
        min_blc = blc.BlcEtlField.MIN_BRIGHTNESS
        compute_brightness_dict = validator_runner.parse_etl_events(adapter, json_output, comp_blc, blc_value)
        # whole ETL will have same calculated value for VBT so considering the first
        driver_min_brightness_dict = validator_runner.parse_etl_events(adapter, json_output, comp_blc, min_blc)

        self.gfx_vbt = vbt.Vbt(adapter.gfx_index)
        for panel in adapter.panels.values():
            logging.info(f"Verifying for {adapter.gfx_index} on {panel.port}")
            # Skip the panel if not LFP
            if panel.is_lfp is False:
                continue
            compute_brightness = compute_brightness_dict[panel.port]
            driver_min_brightness = driver_min_brightness_dict[panel.port][0]
            port = panel.port.split('_')[1]  # DP_A / MIPI_A -> A
            panel_index = self.gfx_vbt.get_lfp_panel_type(panel.port)
            logging.debug(f"\tPanel Index for {panel.port}= {panel_index}")
            if self.gfx_vbt.version < 234:
                vbt_min_brightness = self.gfx_vbt.block_43.BacklightFeaturesEntry[panel_index].MinimumBrightness
            elif 234 <= self.gfx_vbt.version < 236:
                vbt_min_brightness = self.gfx_vbt.block_43.MinBrightnessValue[panel_index]
            else:
                #  for version >= 236:
                vbt_min_brightness = self.gfx_vbt.block_43.MinBrightnessValue[panel_index]
                vbt_precision_bits = self.gfx_vbt.block_43.BrightnessPrecisionBits[panel_index]
                if (vbt_precision_bits == blc.VbtBlcPrecisionBit.BIT_PRECISION_8.value) and \
                        (vbt_min_brightness > 255):
                    error_title = "Invalid Min brightness in VBT for 8 precision bit. " \
                                  f"Expected= (0-255), Actual= {vbt_min_brightness}"
                    logging.error(error_title)
                    blc.report_gdhm_test(error_title, gdhm.ProblemClassification.OTHER)
                    status = False
            logging.info("\tBLC parameters from VBT version {0}[Min Brightness= {1}, Precision Bits= {2}]".format(
                self.gfx_vbt.version, vbt_min_brightness, vbt_precision_bits))

            if expected_min_brightness is not None and (vbt_min_brightness != expected_min_brightness):
                logging.error("VBT min brightness is different. Expected= {0}, Actual= {1}".format(
                    expected_min_brightness, vbt_min_brightness))
                status = False

            if status is False:
                return False

            min_brightness = (vbt_min_brightness * 100 * blc.BLC_PWM_LOW_PRECISION_FACTOR) / ((2 ** vbt_precision_bits) - 1)
            if (min_brightness - math.floor(min_brightness)) < 0.5:
                min_brightness = math.floor(min_brightness)
            else:
                min_brightness = math.ceil(min_brightness)

            # driver will know brightness HighPrecision when driver gets DDI call so at that time it will do (x * 10)
            if self.is_high_precision or panel.max_fall != 0:
                min_brightness *= 10
            logging.info(f"\tApplied Min brightness, Calculated= {min_brightness}, Driver= {driver_min_brightness}")
            if driver_min_brightness != min_brightness:
                logging.error("\tCalculated min brightness is not equal to driver applied min brightness "
                              "Expected= {0}, Actual= {1}".format(min_brightness, driver_min_brightness))
                status = False

            ##
            # B3 policy: Driver should apply OS requested values for B3 (all types -
            # includes high precision, mode - SDR/HDR, panel - PWM/Aux)
            is_b3_supported = False

            if self.is_high_precision or self.nit_ranges is not None or bool(self.hdr_state):
                is_b3_supported = True

            if is_b3_supported is False:
                for value in compute_brightness:
                    logging.debug(f"\tVBT calculated Min Brightness= {min_brightness}, Applied brightness=  {value}")
                    if value < min_brightness:
                        logging.error("Applied brightness is less than value in VBT.Expected>= {0}, Actual= {1}".format(
                            min_brightness, value))
                        status = False

                if status:
                    logging.info(f"\tPASS: Brightness applied is  >= VBT programmed brightness ({min_brightness})")
                else:
                    logging.error(f"\tFAIL: Brightness applied is NOT >= VBT programmed brightness ({min_brightness})")
            else:
                # B3 policy: driver will apply OS requested brightness only for B3.
                field = blc.BlcEtlField()
                event = blc.BlcEtlEvent()
                ddi_data = validator_runner.parse_etl_events(adapter, json_output, event.SET_B3_DDI,
                                                             field.DDI_MILLI_NITS, None)
                ddi_data = ddi_data['NONE']
                for panel in adapter.panels.values():
                    if not panel.is_lfp:
                        continue
                    os_requested_brightness = ddi_data
                    if adapter.lfp_count > 1:
                        # splitting set brightness DDI in half for both LFPs as B2 won't have any port details from OS
                        os_requested_brightness = ddi_data[round(len(ddi_data) / 2):]
                    logging.info(f"\tOS Requested Brightness:({os_requested_brightness})")
                    if panel.port == self.lfp1_port:
                        if blc.verify_brightness_ddi(BRIGHTNESS_LIST, os_requested_brightness,
                                                     event.SET_B3_DDI) is False:
                            status = False
        return status


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('BlcVbt'))
    test_environment.TestEnvironment.cleanup(outcome)
