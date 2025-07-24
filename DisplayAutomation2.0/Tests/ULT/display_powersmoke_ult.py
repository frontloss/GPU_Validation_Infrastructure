############################################################################################################
# @file     display_powersmoke_ult.py
# @brief    This file shall be used for the smoke test of any platform for platform stability to power events S3/S4/CS
#           usage:
#           test_display_python_automation Tests\ULT\display_powersmoke_ult.py -event S3/S4/CS -iteration iteration count
#           test_display_python_automation Tests\ULT\display_powersmoke_ult.py -event S3 -iteration 1
#           test_display_python_automation Tests\ULT\display_powersmoke_ult.py -event S4 -iteration 3
# @author Saradaa
############################################################################################################
import logging
import unittest

from Libs.Core import enum
from Libs.Core.display_power import DisplayPower, PowerSource, PowerEvent
from Libs.Core.test_env.test_environment import *
from Libs.Core.system_utility import *

##
# @brief        This function to verify environment is presi or postsi
# @return       True if postsi; False otherwise
def is_postSi():
    try:
        exec_env = SystemUtility().get_execution_environment_type()
        if exec_env and exec_env.upper() == "SIMENV_FULSIM":
            return False
    except Exception as e:
        logging.warning(str(e))
    return True

##
# @brief This class contains functions that helps to check powerstate
class DisplayPowerUlt(unittest.TestCase):
    # Create DisplayPower object
    disp_power = DisplayPower()

    ##
    # @brief        This class method is the entry point for display_powersmoke_ult.
    # @return       pass
    def setUp(self):
        pass

    ##
    # @brief        This function helps to check the powerstates
    # @param[in]    PowerState Enum value
    # @param[in]    PowerStateName : Event name like S3 S4 and CS
    # @return       True if pass; False otherwise
    def Check_PowerStates(self, PowerState, PowerStateName):
        if self.disp_power.is_power_state_supported(PowerState) is False:
            logging.error(str(PowerStateName) + " is not supported")
            self.fail()
        if self.disp_power.invoke_power_event(PowerState, 60) is False:
            logging.error(PowerStateName + " failure")
            self.fail()

    ##
    # @brief        This function will parse commandline and perform powerstate
    # @return       True if pass; False otherwise
    @unittest.skipUnless(is_postSi(), "Not supported on PreSi environment")
    def test_0_BaseCheck(self):

        # check for the validity of the command line
        if (len(sys.argv) != 5) or (str(sys.argv[1]) != "-EVENT") or (str(sys.argv[3]) != "-ITERATION"):
            logging.error("Invalid command")
            self.fail()
        else:
            EventParam = str(sys.argv[2])
            IterCount = sys.argv[4]
            if str(IterCount).isdigit():
                if EventParam == "S3" or EventParam == 'S4' or EventParam == 'CS':
                    PowerStateVal = PowerEvent[EventParam]
                    for x in range(int(IterCount)):
                        logging.info("Iteration : " + str(x + 1))
                        self.Check_PowerStates(PowerStateVal, EventParam)
                else:
                    logging.error(f"Invalid Parameter for event flag :{EventParam} : Expecting : S3/S4/CS")
                    self.fail()
            else:
                logging.error(f"Invalid Iteration count : {IterCount}")
                self.fail()

    ##
    # @brief        TearDown Function
    # @return       pass
    def tearDown(self):
        pass


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)