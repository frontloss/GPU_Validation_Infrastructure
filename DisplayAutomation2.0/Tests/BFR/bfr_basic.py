########################################################################################################################
# @file         bfr_basic.py
# @brief        Contains basic functional tests for BFR
# @details      Basic functional tests are covering below scenarios:
#               * BFR verification in MAXIMIZED mode
#               * All tests will be executed on VRR panel with VRR enabled. BFR is expected to be working in all above
#               scenarios.
#
# @author       Gopikrishnan R, Nivetha B
########################################################################################################################
import os
from Libs.Core import registry_access
from Libs.Core.test_env import test_context
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.BFR.bfr_base import *

WIKIPEDIA_URL = "https://en.wikipedia.org/wiki/Wikipedia"
WORDPAD_PATH = os.path.join(test_context.SHARED_BINARY_FOLDER, "BFR\BFR_randomText.rtf")

##
# @brief        This class contains basic BFR tests
#               This class inherits the BfrBase class.
class BfrBasic(BfrBase):

    ############################
    # Test Function
    ############################

    ##
    # @brief        BFR verification in MAXIMIZED mode
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["MAXIMIZED"])
    # @endcond
    def t_11_bfr_basic_maximized(self):
        if not self.bfr_basic(True):
            self.fail(f"FAIL : Basic Test : BFR verification failed")

    ##
    # @brief        BFR verification in WINDOWED mode
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["WINDOWED"])
    # @endcond
    def t_12_bfr_basic_windowed(self):
        if not self.bfr_basic(False):
            self.fail(f"FAIL : Basic Test : BFR verification failed")

    ##
    # @brief        BFR verification with mouse movement on desktop
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["MOUSE_MOVE"])
    # @endcond
    def t_13_bfr_basic_mouse_move(self):
        test_status = True
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.bfr_caps.is_bfr_supported:
                    if not bfr.is_dynamic_rr(panel):
                        bfr.set_dynamic_rr(panel)
                    status, etl_files = workload.execute(
                        [
                            # start tracer-> Minimize windows-> random mouse move-> stop tracer
                            workload.Etl(workload.Etl.START),
                            workload.KeyBoardPress(keyboard_action=workload.KeyBoardPress.WIN_M),
                            workload.KeyBoardPress(keyboard_action=workload.KeyBoardPress.WIN_A),
                            workload.Mouse(workload.Mouse.CURSOR_MOVE_RANDOM),
                            workload.Etl(workload.Etl.STOP, file_name="WorkloadTraceMouseMove"),
                        ]
                    )

                    if status is False or bool(etl_files[workload.Etl.STOP]) is False:
                        self.fail("FAILED to run the workload")
                    for index, etl in enumerate(etl_files[workload.Etl.STOP]):
                        test_status &= bfr.verify(adapter, panel, etl, None, False)
        if not test_status:
            self.fail(f"FAIL : Basic Mouse movement Test : BFR verification failed")
        logging.info(f"PASS: Basic Mouse movement Test: BFR verification passed")

    ##
    # @brief        BFR verification with windows movement on desktop
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["WINDOWS_MOVEMENT"])
    # @endcond
    def t_14_bfr_windows_movement(self):
        test_status = True
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.bfr_caps.is_bfr_supported:
                    if not bfr.is_dynamic_rr(panel):
                        bfr.set_dynamic_rr(panel)
                    status, etl_files = workload.execute(
                        [
                            # start tracer-> Minimize windows-> Open a window-> windows move-> close App-> stop tracer
                            workload.Etl(workload.Etl.START),
                            workload.KeyBoardPress(keyboard_action=workload.KeyBoardPress.WIN_M),
                            workload.KeyBoardPress(keyboard_action=workload.KeyBoardPress.WIN_I),
                            workload.WindowApplication(workload.WindowApplication.MOVE_WINDOW_RANDOM_SAME_SCREEN),
                            workload.WindowApplication(workload.WindowApplication.CLOSE,
                                                       workload.AppProcessName.SYSTEM_SETTINGS),
                            workload.Etl(workload.Etl.STOP, file_name="WorkloadTraceWindowMove"),
                        ]
                    )

                    if status is False or bool(etl_files[workload.Etl.STOP]) is False:
                        self.fail("FAILED to run the workload")
                    for index, etl in enumerate(etl_files[workload.Etl.STOP]):
                        test_status &= bfr.verify(adapter, panel, etl, None, False)
        if not test_status:
            self.fail(f"FAIL : Basic Windows movement Test : BFR verification failed")
        logging.info(f"PASS: Basic Windows movement Test: BFR verification passed")

    ##
    # @brief        BFR verification with scrolling on Edge browser
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["BROWSER_SCROLL"])
    # @endcond
    def t_15_bfr_browser_scroll(self):
        reg_args = registry_access.LegacyRegArgs(hkey=registry_access.HKey.LOCAL_MACHINE,
                                                 reg_path=r"SOFTWARE\Policies")
        registry_access.write(args=reg_args, reg_name="HideFirstRunExperience",
                              reg_type=registry_access.RegDataType.DWORD,
                              reg_value=1, sub_key=r"Microsoft\Edge")
        test_status = True
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.bfr_caps.is_bfr_supported:
                    if not bfr.is_dynamic_rr(panel):
                        bfr.set_dynamic_rr(panel)
                    status, etl_files = workload.execute(
                        [
                            # start tracer-> Minimize windows-> Launch browser-> scroll-> close browser-> stop tracer
                            workload.Etl(workload.Etl.START),
                            workload.KeyBoardPress(keyboard_action=workload.KeyBoardPress.WIN_M),
                            workload.WindowApplication(workload.WindowApplication.LAUNCH_IN_WINDOWED,
                                                       workload.AppType.BROWSER, WIKIPEDIA_URL),
                            workload.Wait(delay=5),
                            workload.Mouse(workload.Mouse.SCROLL_RANDOM),
                            workload.WindowApplication(workload.WindowApplication.CLOSE,
                                                       workload.AppProcessName.BROWSER),
                            workload.Etl(workload.Etl.STOP, file_name="WorkloadTraceBrowserScroll"),
                        ]
                    )

                    if status is False or bool(etl_files[workload.Etl.STOP]) is False:
                        self.fail("FAILED to run the workload")
                    for index, etl in enumerate(etl_files[workload.Etl.STOP]):
                        test_status &= bfr.verify(adapter, panel, etl, None, False)
        if not test_status:
            self.fail(f"FAIL : Basic Browser scrolling Test : BFR verification failed")
        logging.info(f"PASS: Basic Browser scrolling Test: BFR verification passed")

    ##
    # @brief        BFR verification with scrolling on Wordpad
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["WORDPAD_SCROLL"])
    # @endcond
    def t_16_bfr_wordpad_scroll(self):
        test_status = True
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.bfr_caps.is_bfr_supported:
                    if not bfr.is_dynamic_rr(panel):
                        bfr.set_dynamic_rr(panel)
                    status, etl_files = workload.execute(
                        [
                            # start tracer-> Minimize windows-> Launch browser-> scroll-> close browser-> stop tracer
                            workload.Etl(workload.Etl.START),
                            workload.KeyBoardPress(keyboard_action=workload.KeyBoardPress.WIN_M),
                            workload.WindowApplication(workload.WindowApplication.LAUNCH_IN_WINDOWED,
                                                       workload.AppType.WORDPAD, WORDPAD_PATH),
                            workload.Wait(delay=5),
                            workload.Mouse(workload.Mouse.SCROLL_RANDOM),
                            workload.WindowApplication(workload.WindowApplication.CLOSE,
                                                       workload.AppProcessName.WORDPAD),
                            workload.Etl(workload.Etl.STOP, file_name="WorkloadTraceWordpadScroll"),
                        ]
                    )

                    if status is False or bool(etl_files[workload.Etl.STOP]) is False:
                        self.fail("FAILED to run the workload")
                    for index, etl in enumerate(etl_files[workload.Etl.STOP]):
                        test_status &= bfr.verify(adapter, panel, etl, None, False)
        if not test_status:
            self.fail(f"FAIL : Basic Wordpad scrolling Test : BFR verification failed")
        logging.info(f"PASS: Basic Wordpad scrolling Test: BFR verification passed")


if __name__ == '__main__':
    TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(BfrBasic))
    TestEnvironment.cleanup(test_result)
