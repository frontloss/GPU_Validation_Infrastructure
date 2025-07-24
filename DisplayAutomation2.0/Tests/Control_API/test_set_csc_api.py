########################################################################################################################
# @file         test_set_csc_api.py
# @brief        Test calls for Pixel Transformation API through Control Library and verifies return status of the API.
#               Set Pixel Transformation of CSC API.
# @author       Prateek Joshi, Pooja Audichya
########################################################################################################################

import ctypes

from Libs.Core.logger import gdhm
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.wrapper import control_api_wrapper
from Libs.Core.wrapper import control_api_args
from Tests.Control_API.control_api_test_base import *

##
# @brief - Set CSC Pixel Transformation Control Library Test
class TestSetCSCAPI(ControlAPITestBase):

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):

        pre_offset = [1, 0, 0]
        post_offset = [1, 0, 0]
        # RED_BLUE_SWAP_MATRIX
        matrix_info = [[0, 0, 1], [0, 1, 0], [1, 0, 0]]

        args_set_csc_args = control_api_args.ctl_pixtx_pipe_set_config_t()
        args_set_csc_args.Size = ctypes.sizeof(args_set_csc_args)
        args_set_csc_args.OpertaionType = control_api_args.ctl_pixtx_config_opertaion_type_v.SET_CUSTOM.value

        blk_cfg = control_api_args.ctl_pixtx_block_config_t()
        blk_cfg.BlockType = control_api_args.ctl_pixtx_block_type_v._3X3_MATRIX.value

        logging.debug("Matrix info {}".format(matrix_info))
        logging.debug("PreOffsets {}".format(pre_offset))
        logging.debug("PostOffsets {}".format(post_offset))

        for index in range(0, 3):
            blk_cfg.Config.MatrixConfig.PreOffsets[index] = pre_offset[index]
            blk_cfg.Config.MatrixConfig.PostOffsets[index] = post_offset[index]

        for row in range(0, 3):
            for column in range(0, 3):
                blk_cfg.Config.MatrixConfig.Matrix[row][column] = matrix_info[row][column]

        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active:
                    logging.info("Step_1: Set CSC Pixel Transformation")
                    if control_api_wrapper.set_csc(args_set_csc_args, blk_cfg, panel.target_id):
                        logging.info("Pass: Set CSC Pixel Transformation")
                    else:
                        logging.error("Fail: Set CSC Pixel Transformation")
                        gdhm.report_driver_bug_clib("Set CSC Pixel Transformation Failed via Control Library for "
                                                    "OperationType: {0} TargetId: {1}".format(
                                                        args_set_csc_args.OpertaionType, panel.target_id
                                                    ))
                        self.fail("Set CSC Pixel Transformation Failed")

    ##
    # @brief            Unittest tearDown function
    # @return           void
    def tearDown(self):
        logging.info(" TEARDOWN: TestSetCSCAPI ")

        args_restore_default_args = control_api_args.ctl_pixtx_pipe_set_config_t()
        args_restore_default_args.Size = ctypes.sizeof(args_restore_default_args)
        args_restore_default_args.OpertaionType = control_api_args.ctl_pixtx_config_opertaion_type_v.RESTORE_DEFAULT.value

        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active:
                    logging.info("Restore Default Values for Color API")
                    if control_api_wrapper.restore_default(args_restore_default_args, panel.target_id):
                        logging.info("Restore Default Values for Color API Successfully")
                    else:
                        logging.error("Restore Default Values for Color API Failed")

        super(TestSetCSCAPI, self).tearDown()


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info('Test purpose: Control Library Set CSC API Verification')
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
