######################################################################################
# \file
# \section underrun_base
# \remarks
# \ref underrun_ult.py \n
# Each function in this base will verify the functionality of underrun.dll API's.
# Commandline : python Tests\ULT\underrun_ult.py
# \author   Raghupathy, Dushyanth Kumar
######################################################################################
from Libs.Core.test_env.test_environment import *
from Libs.Feature.crc_and_underrun_verification import *

def initUnderRunCounter():
    try:
        under_run.clear_underrun_registry()
        logging.info("Initiated UnderRun Counter")
    except Exception as ex:
        logging.error("Exception: {}".format(ex))

def getUnderRunStatus():
    try:
        result = under_run.verify_underrun()

        if result:
            logging.debug("UnderRun Found")
        else:
            logging.debug("No UnderRun Seen")

        logging.info("Pass: Verify UnderRun Status")
    except Exception as ex:
        logging.error("Exception: {}".format(ex))

if __name__ == '__main__':
    # Initializing test environment
    TestEnvironment.initialize()

    under_run = UnderRunStatus()

    initUnderRunCounter()
    getUnderRunStatus()
