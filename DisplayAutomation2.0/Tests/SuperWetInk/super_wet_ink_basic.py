########################################################################################################################
# @file         super_wet_ink_basic.py
# @brief        Contains basic functional tests for SuperWetInk
# @details      Basic functional tests are covering below scenarios:
#               * Super WetInk verification in MAXIMIZED/WINDOWED mode
#
# @author       Nivetha B
########################################################################################################################

from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.SuperWetInk.super_wet_ink import *
from Tests.SuperWetInk.super_wet_ink_base import *


##
# @brief        This class contains basic SuperWetInk tests
#               This class inherits the SuperWetInkBase class.
class SuperWetInkBasic(SuperWetInkBase):

    ############################
    # Test Function
    ############################

    ##
    # @brief        SuperWetInk verification with Snipping tool in windowed mode
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["WINDOWED"])
    # @endcond
    def t_11_super_wet_ink_windowed(self):
        test_status = True
        status, etl_files = workload.execute(
            [
                # start tracer-> Minimize windows-> Launch snipping tool -> Draw -> stop tracer
                workload.Etl(workload.Etl.START),
                workload.KeyBoardPress(keyboard_action=workload.KeyBoardPress.WIN_M),
                workload.DxSnipAndSketchApplication(workload.DxSnipAndSketchApplication.LAUNCH_SNIPTOOL_IN_WINDOWED),
                workload.DxSnipAndSketchApplication(workload.DxSnipAndSketchApplication.DRAW_RANDOM),
                workload.DxSnipAndSketchApplication(workload.DxSnipAndSketchApplication.CLOSE),
                workload.Etl(workload.Etl.STOP, file_name="WorkloadTraceSnipTool"),
            ]
        )

        if status is False or bool(etl_files[workload.Etl.STOP]) is False:
            self.fail("FAILED to run the workload")
        for index, etl in enumerate(etl_files[workload.Etl.STOP]):
            test_status &= validate_superwetink(etl)
        if not test_status:
            self.fail(f"FAIL :SuperWetInk basic verification failed")
        logging.info(f"PASS: SuperWetInk basic verification passed")

    ##
    # @brief        SuperWetInk verification with Snipping tool in maximized mode
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["MAXIMIZED"])
    # @endcond
    def t_12_super_wet_ink_maximized(self):
        test_status = True
        status, etl_files = workload.execute(
            [
                # start tracer-> Minimize windows-> Launch snipping tool -> Draw -> stop tracer
                workload.Etl(workload.Etl.START),
                workload.KeyBoardPress(keyboard_action=workload.KeyBoardPress.WIN_M),
                workload.DxSnipAndSketchApplication(workload.DxSnipAndSketchApplication.LAUNCH_SNIPTOOL_IN_MAXIMIZED),
                workload.DxSnipAndSketchApplication(workload.DxSnipAndSketchApplication.DRAW_RANDOM),
                workload.DxSnipAndSketchApplication(workload.DxSnipAndSketchApplication.CLOSE),
                workload.Etl(workload.Etl.STOP, file_name="WorkloadTraceSnipTool"),
            ]
        )

        if status is False or bool(etl_files[workload.Etl.STOP]) is False:
            self.fail("FAILED to run the workload")
        for index, etl in enumerate(etl_files[workload.Etl.STOP]):
            test_status &= validate_superwetink(etl)
        if not test_status:
            self.fail(f"FAIL :SuperWetInk basic verification failed")
        logging.info(f"PASS: SuperWetInk basic verification passed")


if __name__ == '__main__':
    TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(SuperWetInkBasic))
    TestEnvironment.cleanup(test_result)
