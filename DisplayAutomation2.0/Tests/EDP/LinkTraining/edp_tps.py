########################################################################################################################
# @file         edp_tps.py
# @brief        The file contain test for TPS verification
# @author       Tulika
########################################################################################################################
from Libs.Core.logger import html
from Libs.Core.test_env import test_environment
from Tests.EDP.LinkTraining import edp_link_training
from Tests.EDP.LinkTraining.edp_link_training_base import *
from Libs.Core import etl_parser


##
# @brief        This class contains test to verify training pattern sequence during link training.
class EdpLinkTrainingtTps(EdpLinkTrainingBase):

    ##
    # @brief        This functions reboot the system to get link training data
    # @return       None
    def test_before_reboot(self):
        if reboot_helper.reboot(self, 'runTest') is False:
            self.fail("FAILED to reboot the system")

    ##
    # @brief        This functions get tps data from both dpcd and etl and compare for verification.
    # @return       None
    def runTest(self):
        edp = EdpLinkTrainingBase()
        dut.prepare()
        html.step_start("Verifying Training Pattern Sequence")
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                # Stop etl and get the etl file path
                etl_file_path = edp.stop_etl_get_etl_file_path()

                if etl_file_path is None:
                    html.step_end()
                    self.fail("FAILED to fetch the ETL File Path")

                # Generate Report
                if etl_parser.generate_report(etl_file_path, edp_link_training.ETL_PARSER_CONFIG) is False:
                    html.step_end()
                    self.fail("FAILED to generate ETL Parser report")
                logging.info("Successfully generated ETL Parser report")

                # Get diana log file
                diana_exe_path = os.path.join(test_context.SHARED_BINARY_FOLDER, "DiAna\\DiAna.exe")
                diana_log_file = edp.get_diana_file(diana_exe_path, etl_file_path)

                # Verify link training with diana ETL logs
                status = edp_link_training.verify_link_training(diana_log_file)
                if status is False:
                    html.step_end()
                    gdhm.report_driver_bug_di(f"{edp_link_training.GDHM_LT} Link Training Failed")
                    self.fail("FAIL: Link Training Failed")
                logging.info("PASS: Link Training Successful")

                # Training Pattern Sequence from DPCD
                training_seq = edp_link_training.get_training_pattern_sequence_from_dpcd(panel)
                logging.debug(f"Training Pattern Sequence from DPCD= TRAINING_PAT_{training_seq}")

                # Training Pattern Sequence from ETL
                training_data = etl_parser.get_event_data(etl_parser.Events.DP_RX_CAPS)
                if training_data is None:
                    html.step_end()
                    gdhm.report_driver_bug_di(f"{edp_link_training.GDHM_LT} Pattern Sequence NOT found in ETL")
                    self.fail("Training Pattern Sequence NOT found in ETL")

                # Compare Training Pattern Sequence from DPCD and ETL.
                for event_data in training_data:
                    logging.debug(
                        f"Training Pattern Sequence from ETL= TRAINING_PAT_{event_data.TrainingPattern}")
                    if edp_link_training.TrainingPatternSequence(event_data.TrainingPattern) != training_seq:
                        html.step_end()
                        gdhm.report_driver_bug_di(f"{edp_link_training.GDHM_LT} "
                                                  f"Training Pattern Sequence not matched.Expected= TRAINING_PAT_"
                                                  f"{training_seq} Actual= TRAINING_PAT_{event_data.TrainingPattern}")
                        self.fail(f"FAIL: Training Pattern Sequence not matched. Expected= TRAINING_PAT_{training_seq}"
                                  f"Actual= TRAINING_PAT_{event_data.TrainingPattern}")
                    logging.info(f"Training Pattern Sequence matched. Expected= TRAINING_PAT_{training_seq} "
                                 f"Actual= TRAINING_PAT_{event_data.TrainingPattern}")
                    html.step_end()


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('EdpLinkTrainingtTps'))
    test_environment.TestEnvironment.cleanup(outcome)
