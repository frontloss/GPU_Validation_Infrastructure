########################################################################################################################
# @file         igcl_set_ftr_sdr.py
# @brief        Test script which helps to set different blocks in SDR/HDR/WCG mode.
#               Script performs only SET and not Verify
# @author       Smitha B
########################################################################################################################
from Tests.Color.Features.Igcl_Set_Cc_Blk.igcl_color_test_base import *
from Tests.Color.Features.Igcl_Set_Cc_Blk import igcl_color_cc_block


##
# @brief - Set DeGamma Pixel Transformation Control Library Test
class test_igcl_color_csc(IGCLColorTestBase):

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):
        self.prepare_color_properties()
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                status, igcl_get_caps = fetch_igcl_color_ftrs_caps_and_verify(gfx_index,
                                                                              adapter.platform,
                                                                              panel.connector_port_type,
                                                                              panel.pipe,
                                                                              panel.target_id,
                                                                              self.user_req_color_blk)

                if status is False:
                    logging.error("FAIL : IGCL Support for {0} has not been reported by the driver on {1} connected "
                                  "to Pipe {2} on adapter {3} "
                                  .format(color_igcl_wrapper.IgclColorBlocks(self.user_req_color_blk).name,
                                          panel.connector_port_type, panel.pipe, gfx_index))
                    gdhm.report_driver_bug_os("[{0}] IGCL Support for {1} has not been reported by the driver on {2} connected "
                                  "to Pipe {3} on Adapter {4}"
                                  .format(adapter.platform, color_igcl_wrapper.IgclColorBlocks(self.user_req_color_blk).name,
                                          panel.connector_port_type, panel.pipe, gfx_index))
                    self.fail()

                igcl_set_args = color_igcl_wrapper.prepare_igcl_color_escapes_args_for_set(gfx_index, adapter.platform,
                                                                                           panel.connector_port_type,
                                                                                           panel.pipe,
                                                                                           igcl_get_caps,
                                                                                           self.user_req_color_blk,
                                                                                           self.num_blocks_to_be_set,
                                                                                           self.igcl_color_ftr_data,
                                                                                           self.igcl_color_ftr_index)
                mode_enabled = hdr_utility.fetch_enabled_mode(gfx_index, adapter.platform, panel.pipe)
                if color_igcl_escapes.set_igcl_color_feature(igcl_set_args, igcl_get_caps, panel.target_id,
                                                             self.user_req_color_blk, mode_enabled) is False:
                    logging.error("Set overall feature is failing")
                    self.fail()
                else:
                    logging.info("Set overall feature is successful")


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info('Test purpose: Control Library Set CSC API Verification')
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)