########################################################################################################################
# @file         igcl_restore_default_sdr.py
# @brief        Test script restores default of all the color blocks
#               Script performs only SET and not verify
# @author       Smitha B
########################################################################################################################
from Tests.Color.Features.Igcl_Set_Cc_Blk.igcl_color_test_base import *
from Tests.Color.Features.Igcl_Set_Cc_Blk import igcl_color_cc_block
from Tests.Color.Common import color_igcl_wrapper, color_igcl_escapes


##
# @brief - Set DeGamma Pixel Transformation Control Library Test
class test_igcl_color_csc(IGCLColorTestBase):

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):
        self.prepare_color_properties()
        igcl_esc_restore_default = color_igcl_wrapper.prepare_igcl_color_esc_args_for_restore_default()
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if color_igcl_escapes.perform_restore_default(igcl_esc_restore_default, panel.target_id):
                    logging.info("PASS: Restore Default Values for Color Blocks")
                else:
                    logging.error("FAIL: Restore Default Values for Color Blocks")
                    gdhm.report_driver_bug_os("[{0}] Restore Default Values for Color Blocks failed for Adapter: {1} "
                                                "Pipe: {2}".format(adapter.platform, gfx_index, panel.pipe))
                    self.fail()
        super().tearDown()


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info('Test purpose: Control Library Set CSC API Verification')
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)