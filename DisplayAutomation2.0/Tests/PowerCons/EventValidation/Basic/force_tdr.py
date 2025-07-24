########################################################################################################################
# @file         force_tdr.py
# @details      @ref force_tdr.py <br>
#               This file implements force tdr scenario for all display pc feature testing.
#
# @author       Vinod D S
########################################################################################################################

from Libs.Core.test_env import test_environment
from Libs.Core.Verifier.common_verification_args import VerifierCfg, Verify
from Tests.PowerCons.EventValidation.Basic.event_validation_base import *


##
# @brief        This class contains tests for events with forced TDR scenario
class ForceTdr(EventValidationBase):
    ##
    # @brief        This function verifies if generation and detection of forced TDR is successful
    # @return       None
    def test_force_tdr(self):
        VerifierCfg.tdr = Verify.SKIP
        logging.debug("Updated config under-run:{}, tdr:{}".format(VerifierCfg.underrun.name, VerifierCfg.tdr.name))

        for adapter in dut.adapters.values():
            #  Check any TDR by now
            self.assertNotEquals(display_essential.detect_system_tdr(gfx_index=adapter.gfx_index), True,
                                 "TDR found while running the test")

            #  Generate TDR
            self.assertEquals(display_essential.generate_tdr(gfx_index=adapter.gfx_index, is_displaytdr=True), True,
                              "TDR generation failed")

            #  detect tdr generation
            self.assertEquals(display_essential.detect_system_tdr(gfx_index=adapter.gfx_index), True, "TDR not generated")

            logging.info("Waiting for 10 seconds after TDR")
            time.sleep(10)

            self.check_validators()

        ##
        # Clear TDR dumps from system
        if display_essential.clear_tdr() is True:
            logging.info("TDR cleared successfully post TDR generation")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    test_environment.TestEnvironment.cleanup(outcome.result)
