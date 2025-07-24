#######################################################################################################################
# @file         display_ddi_responsiveness_power_event.py
# @brief        Test to call functions to generate etl file
# @details      Test Scenario:
#                1. Boot the system with edp.
#                2. Invoke power event (CS, S3, S4) based on the command line.
#                3. Resume from power event and generate etl file.
#                4. Parse the etl file to Diana and verify the values based on fixed target values.
#                This test can be planned with MIPI and EDP
#
# @author       Nivetha B, Ravichandran M
#######################################################################################################################
from Libs import env_settings
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.gta import gta_state_manager
from Libs.Core.logger import display_logger
from Libs.Core import test_header
from Tests.DDI_Responsiveness.display_ddi_responsiveness_base import *


##
# @brief Contains the function calls for parsing etl to Diana
class ResponsivenessPowerEvent(ResponsivenessBase):

    ##
    # @brief Contains Responsiveness power event test steps
    # @return None
    def runTest(self):
        # Set the test name for logging
        self.test_name = "Adk_{0}_Test".format(self.power_event_str)
        logging.info("**************** {0} Started ****************".format(self.test_name))

        ##
        # Generates etl file by triggering the power event
        adk_etl_file = self.run_etl_file()

        ##
        # Generates the report by parsing etl file to diana
        self.run_diana(adk_etl_file)


if __name__ == '__main__':
    env_settings.set('SIMULATION', 'simulation_type', 'NONE')
    TestEnvironment.load_dll_module()
    display_logger._initialize(console_logging=True)
    test_header.initialize(sys.argv)
    etl_tracer._register_trace_scripts()
    gta_state_manager.create_gta_default_state()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
