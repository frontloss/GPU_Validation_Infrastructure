########################################################################################################################
# @file         blc_sdr_hdr_toggle.py
# @brief        Test for BLC with SDR HDR toggle in OS aware way
#
# @author       Ashish Tripathi
########################################################################################################################
import math
from collections import Counter

from Libs.Core.test_env import test_environment

from Tests.PowerCons.Functional.BLC.blc_base import *
from Tests.PowerCons.Modules.validator_runner import parse_etl_events, run_diana

PRECISION_FACTOR = 100000
scenario_str = blc.Scenario.TOGGLE_SDR_HDR.name


##
# @brief        This class contains BLC tests with HDR SDR toggle
class BlcSdrHdrToggle(BlcBase):
    ##
    # @brief        This test verifies BLC with HDR SDR toggle
    # @return       None
    def test_sdr_hdr_toggle(self):
        # For reg keys update from setup
        self.setup_and_validate_blc()
        brightness_args = [self.is_pwm_based, self.nit_ranges, self.is_high_precision, self.hdr_state, BRIGHTNESS_LIST,
                           self.lfp1_port, self.disable_boost_nit_ranges, self.is_invalid_inf_nit_range,
                           self.disable_nits_brightness, self.independent_brightness]
        for adapter in dut.adapters.values():
            workload_status = blc.run_workload(adapter, blc.Scenario.TOGGLE_SDR_HDR, brightness_args)
            if workload_status[1] is False:
                self.fail("FAILED to run the workload")

            if workload_status[0] is None:
                self.fail("ETL file not found")
            html.step_start("VERIFICATION PHASE")

            json_output = run_diana(self.cmd_test_name, workload_status[0], ['BLC'])
            if json_output is None:
                self.fail("JSON file not found")
            self.verify(adapter, json_output)

    ##
    # @brief        This is a helper function to verify BLC with HDR SDR toggle
    # @param[in]    adapter Adapter object
    # @param[in]    json_file etl file
    # @return       None
    def verify(self, adapter, json_file):
        status = True
        max_fall = {}
        min_cll = {}
        max_nits = 1
        field = blc.BlcEtlField()
        event = blc.BlcEtlEvent()
        not_happening_str = f"NOT happening for SetBrightness3 during {scenario_str}"
        ddi_data = parse_etl_events(adapter, json_file, event.SET_B3_DDI, field.DDI_MILLI_NITS, None)
        client_event_list = parse_etl_events(adapter, json_file, event.CLIENT_EVENT, field.B2_TARGET)
        b3_transition_hdr_list = parse_etl_events(adapter, json_file, event.B3_TRANSITION, field.HDR_ACTIVE)
        b3_transition_target_list = parse_etl_events(adapter, json_file, event.B3_TRANSITION, field.MILLI_NITS_TARGET)

        count = 0
        ddi_data = ddi_data['NONE']
        for panel in adapter.panels.values():
            if not panel.is_lfp:
                continue
            os_requested_brightness = ddi_data
            client_event_value = client_event_list[panel.port]
            b3_transition_hdr_mode = b3_transition_hdr_list[panel.port]
            b3_transition_target = b3_transition_target_list[panel.port]
            max_fall[panel.port] = panel.max_fall
            min_cll[panel.port] = panel.min_cll

            if adapter.lfp_count > 1:
                # splitting set brightness DDI in half for both LFPs as B2 won't have any port details from OS
                os_requested_brightness = ddi_data[round(len(ddi_data) / 2):]
                if count == 1:
                    os_requested_brightness = ddi_data[:round(len(ddi_data) / 2)]
            if panel.port == self.lfp1_port:
                if blc.verify_brightness_ddi(BRIGHTNESS_LIST, os_requested_brightness, event.SET_B3_DDI) is False:
                    status = False
                min_milli_nits = min_cll[self.lfp1_port]
                if self.nit_ranges is not None:
                    min_milli_nits = blc.convert_nits_to_milli_nits(int(self.nit_ranges[0][0]))
                    # Fetching max range residing at 2nd index of end list ([[1, 2 ,4], [1, 4, 5], [8, 7, 6]] --> 7)
                    max_nits = int(self.nit_ranges[-1][1])
                    max_milli_nits = blc.convert_nits_to_milli_nits(max_nits)
                else:
                    max_nits = max_fall[self.lfp1_port]
                    #   if disable_boost_ranges, do 100% else 80%:20% as MSFT recommended
                    if self.disable_boost_nit_ranges:
                        max_milli_nits = blc.convert_nits_to_milli_nits(max_nits)
                    else:
                        max_milli_nits = blc.convert_nits_to_milli_nits((max_nits * 80) // 100)

                # count the int 100 in the list
                max_brightness_count = Counter(BRIGHTNESS_LIST)[100]
                args = [False, os_requested_brightness, min_milli_nits, max_milli_nits]
                if blc.verify_nits_ranges(args, max_brightness_count, scenario_str) is False:
                    status = False

                sdr_mode_target = []
                hdr_mode_target = []
                for idx, value in enumerate(b3_transition_hdr_mode):
                    if value == 1:
                        # append target values for HDR mode
                        hdr_mode_target.append(b3_transition_target[idx])
                    else:
                        sdr_mode_target.append(b3_transition_target[idx])

                # check for target brightness is max in HDR mode
                hdr_milli_nits = blc.convert_nits_to_milli_nits(max_nits)
                if all(val == hdr_milli_nits for val in hdr_mode_target) is False:
                    logging.error(f"\tFAIL: All target is not {hdr_milli_nits} milli-nits. Actual= {hdr_mode_target}")
                    status = False
                else:
                    logging.info(f"\tPASS: All target brightness for HDR enable is {hdr_milli_nits} milli-nits")

                for itr in range(len(sdr_mode_target)):
                    brightness = ((sdr_mode_target[itr] * PRECISION_FACTOR) / max_nits) / 1000
                    # 46.5 -> 47, 82.7 -> 83, 1.2 -> 1
                    converted_brightness = math.floor(brightness)

                    if client_event_value[itr] != converted_brightness:
                        logging.error("FAIL: NitsToPwm calculation mismatch. Expected= {0}, Actual= {1}".format(
                            converted_brightness, client_event_value[itr]))
                        blc.report_gdhm_driver("[PowerCons][BLC] NitsToPwm calculation mismatch during SDR_HDR")
                        status = False
                    else:
                        logging.info("PASS: NitsToPwm calculation matched. Expected= {0}, Actual= {1}".format(
                            converted_brightness, client_event_value[itr]))

                # B3Transition will be converting the value NITStoPWM i.e. SDR only
                # For HDR it will send full brightness so ignoring for HDR and comparing those brightness
                # conversion required in SDR mode
                title = f"[PowerCons][BLC] B3Transition(NitsToPwm) is {not_happening_str}"
                if blc.verify_b3_transition(sdr_mode_target, os_requested_brightness[::2], title) is False:
                    status = False

            # client event will be for SDR mode so checking for alternate values applied [start_index:end_index:step]
            ##
            # In Independent Brightness path there is no relative brightness path for LFP2
            if panel.port in ["DP_B", "MIPI_C"] and self.independent_brightness:
                logging.info("LFP2 is external to OS.So no OS DDI will be reported as part of set brightness event")
            else:
                title = f"[PowerCons][BLC] BlcClientEvent is {not_happening_str}"
                os_requested_brightness = blc.convert_milli_nits_to_milli_percent(os_requested_brightness[::2], max_nits)
                if blc.verify_blc_client(
                        client_event_value, os_requested_brightness, event.SET_B3_DDI, title, panel) is False:
                    status = False
        count += 1

        if status is False:
            self.fail("FAIL: BLC SDR-HDR verification")
        logging.info("PASS: BLC SDR-HDR verification")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('BlcSdrHdrToggle'))
    test_environment.TestEnvironment.cleanup(outcome)
