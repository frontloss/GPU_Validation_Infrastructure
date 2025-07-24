########################################################################################################################
# @file         crc_and_underrun_verification.py
# @brief        This module is used to monitor under-runs generated on all the pipes.
# @note         clear_underrun_registry - clear and monitor under-run\n
#               verify_underrun - verify and detect under-run on display Pipes.
# @author       Pabolu, Chandrakanth, Praburaj Krishnan
########################################################################################################################
import time
from Libs.Core.Verifier import underrun_verification


##
# @brief        Under Run Status Object
class UnderRunStatus(object):

    ##
    # @brief        API to enable and monitor under-run. Resets the under-run counter register to zero for all adapters.
    # @return       None
    @staticmethod
    def clear_underrun_registry():
        # type: () -> None

        underrun_verification._clear_underrun_registry()

    ##
    # @brief        Logs and returns underrun status for each gfx adapter, if underrun is observed in any of the pipe.
    # @return       is_underrun_observed: bool
    #                   Returns True if underrun is observed is at least one of the gfx adapter else False.
    @staticmethod
    def verify_underrun():
        # type: () -> bool

        return underrun_verification._verify_underrun_with_registry()


if __name__ == "__main__":
    UnderRunStatus.clear_underrun_registry()
    UnderRunStatus.verify_underrun()
    time.sleep(60)
    UnderRunStatus.verify_underrun()
