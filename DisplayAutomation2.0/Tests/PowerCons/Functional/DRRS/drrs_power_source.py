#################################################################################################################
# @file         drrs_power_source.py
# @addtogroup   PowerCons
# @section      DRRS_Tests
# @brief        Contains DRRS power source tests
#
# @author       Ashish Tripathi
#################################################################################################################
from Libs.Core import etl_parser, enum
from Libs.Core import display_power
from Libs.Core.test_env import test_environment

from Tests.PowerCons.Functional.DRRS.drrs_base import *


##
# @brief        This class contains tests to verify DRRS before and after power source
class DrrsPowerSourceTest(DrrsBase):

    ##
    # @brief        This function verifies DRRS with AC_DC switch
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["AC_DC"])
    # @endcond
    def t_11_ac_dc(self):
        status = True
        count = int(self.cmd_line_param[0]['COUNT'][0]) if self.cmd_line_param[0]['COUNT'] != 'NONE' else 1
        is_cs_supported = self.display_power_.is_power_state_supported(display_power.PowerEvent.CS)

        for index in range(count):
            for power_source in [workload.PowerSource.AC_MODE, workload.PowerSource.DC_MODE]:

                if self.method == "IDLE":
                    etl_file, _ = workload.run(
                        workload.IDLE_DESKTOP,
                        [10, False, False, False, power_source])
                else:
                    monitor_ids = [_[0] for _ in app_controls.get_enumerated_display_monitors()]
                    etl_file, _ = workload.run(workload.SCREEN_UPDATE, [monitor_ids])

                if etl_file is False:
                    self.fail("\tFAILED to run the workload")

                logging.info(f"\tGenerating EtlParser Report for {etl_file}")
                if etl_parser.generate_report(etl_file, drrs.ETL_PARSER_CONFIG) is False:
                    self.fail("\tFAILED to generate ETL Parser report")
                logging.info("\tSuccessfully generated ETL Parser report")

                power_source_name = workload.PowerSource(power_source).name
                power_scheme_name = self.display_power_.get_current_power_scheme().name

                for adapter in dut.adapters.values():
                    html.step_start(f"Verifying Static DRRS on {adapter.name}")
                    for panel in adapter.panels.values():
                        if adapter.name not in common.PRE_GEN_13_PLATFORMS + ['DG2']:
                            # static drrs is not supported from ADL-P+
                            expected_rr = 0
                        else:
                            if power_source == workload.PowerSource.AC_MODE:
                                expected_rr = panel.drrs_caps.max_rr
                            else:
                                expected_rr = panel.drrs_caps.min_rr

                            if is_cs_supported:
                                expected_rr = 0

                        logging.info(f"Restrictions: CS Supported= {is_cs_supported}, "
                                     f"PowerSource= {power_source_name}, PowerPlan= {power_scheme_name} , "
                                     f"Expected RR= {'NO Change' if expected_rr == 0 else expected_rr}")

                        status &= drrs.verify_static_drrs(expected_rr)

                        # Due to known bug from CUI behavior avoiding the failure
                        # DC -> Driver restart -> Hi-RR SetTiming (issue) -> AC -> No SetTiming -> works as usual
                        if index == 0 and status is False:
                            status = True

                    if adapter.name not in common.PRE_GEN_13_PLATFORMS + ['DG2']:
                        if status is True:
                            self.fail("FAIL: Static DRRS is Functional (Unexpected)")
                        logging.info("PASS: Statis DRRS is not Functional (Expected)")
                    else:
                        if status is False:
                            self.fail("FAIL: Static DRRS is NOT functional (Unexpected)")
                        logging.info("PASS: Static DRRS is functional (Expected)")
                    html.step_end()


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(DrrsPowerSourceTest))
    test_environment.TestEnvironment.cleanup(test_result)
