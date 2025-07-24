#######################################################################################################################
# @file         lace_aggrlevel_stress.py
# @addtogroup   Test_Color
# @section      lace_aggrlevel_stress
# @remarks      @ref lace_aggrlevel_stress.py \n
#               The test script performs the driver PCEscape call to enable LACE using Lux and Aggressiveness levels
#               in a stress scenario.
#               Register verification is performed to verify if LACE is enabled/disabled appropriately.
# CommandLine:  python lace_aggrlevel_stress.py -edp_a
# @author       Smitha B
#######################################################################################################################
import random

from Tests.Color.Common import color_igcl_escapes
from Tests.Color.LACE.lace_base import *
from Tests.Color.Verification import feature_basic_verify


class LACEAggressivenessLevelStress(LACEBase):

    def runTest(self):

        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active and panel.is_lfp:
                    if self.check_primary_display(port):
                        for i in range(0, 50):
                            lux = random.randint(1, 100)
                            if color_igcl_escapes.get_lace_config(0, panel.display_and_adapterInfo):
                                time.sleep(1)

                            if color_igcl_escapes.set_lace_config(self.triggerType, self.setOperation, lux,
                                                             panel.display_and_adapterInfo):
                                time.sleep(2)

                            ##
                            # verify_lace_feature
                            if feature_basic_verify.verify_lace_feature(gfx_index, adapter.platform, panel.pipe, True,
                                                                        "LEGACY") is False:
                                self.fail("Lace verification failed")

                    # Lace should not be enabled for 2nd LFP which is not set as primary
                    else:
                        if self.enable_and_verify(gfx_index, adapter.platform, panel.pipe, panel.display_and_adapterInfo,
                                                  panel, False):
                            logging.info("Pass: Lace was disabled and verified successfully for second LFP on pipe_{0}".format(panel.pipe))
                        else:
                            self.fail("Lace is enabled for second LFP on pipe_{0}".format(panel.pipe))

if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
