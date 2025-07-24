#################################################################################################
# @file         apply_csc_basic.py
# @brief        This scripts comprises of basic quantization test will perform below functionalities
#               1.test_01_basic() - Will apply the mode and bpc will be set based on commandline
#               and perform register verification OCSC,Coeff and gamma register
# @author       Vimalesh D
#################################################################################################
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.test_base import *
from Tests.Color.Features.ApplyCSC.apply_csc_base import *


##
# @brief - Apply csc basic test
class ApplyCscTestBasic(ApplyCSCTestBase):
    ##
    # @brief        test_01_basic() executes the actual test steps.
    # @return       None
    @unittest.skipIf(get_action_type() != "BASIC", "Skip the  test step as the action type is not basic")
    def test_01_basic(self):

        if self.matrix_name not in ["INVALID_MATRIX", "ALL_0_MATRIX"]:
            for gfx_index, adapter in self.context_args.adapters.items():
                for port, panel in adapter.panels.items():
                    if panel.is_active:
                        if self.enable_and_verify(gfx_index, adapter.platform, panel.pipe,
                                                  panel.display_and_adapterInfo, port, True) is False:
                            self.fail()
        else:
            for gfx_index, adapter in self.context_args.adapters.items():
                for port, panel in adapter.panels.items():

                    if panel.is_active:
                        ##
                        # apply identity csc
                        identity_csc = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
                        invalid_matrix = self.matrix_info

                        self.matrix_info = identity_csc
                        if self.enable_and_verify(gfx_index, adapter.platform, panel.pipe,
                                                  panel.display_and_adapterInfo, port, True) is False:
                            self.fail()

                        self.matrix_info = invalid_matrix
                        # Trying to send invalid CSC matrix to the escape call
                        # Expecting the Escape Call to fail, since the ValidateCSC() in driver will fail
                        if color_escapes.configure_pipe_csc(port, panel.display_and_adapterInfo, self.csc_type, self.matrix_info, True,
                                                            self.matrix_name):
                            logging.error("Driver applied an invalid CSC(Driver Issue)")
                            self.fail("Driver applied an invalid CSC(Driver Issue)")
                        else:
                            logging.info("Driver did not apply an invalid csc.")

                            self.matrix_info = identity_csc
                            ##
                            # Verifying if identity CSC is persisting
                            if self.enable_and_verify(adapter.gfx_index, adapter.platform, panel.pipe,
                                                      panel.display_and_adapterInfo, port, False) is False:
                                self.fail()


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)