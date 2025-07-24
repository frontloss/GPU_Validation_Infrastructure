#######################################################################################################################
# @file                 hdr_with_csc.py
# @addtogroup           Test_Color
# @section              hdr_with_csc
# @remarks              @ref hdr_with_csc.py \n
#                       The test script enables HDR on eDP_HDR displays,
#                       which is an input parameter from the test command line.
#                       The script can handle both Aux and SDP variety of displays.
#                       The script invokes the API to set the OS Brightness Slider level
#                       to a value provided in the command line.
#                       If Brightness Slider level has not been given as an input, script sets the slider
#                       to a random value other than the Current Brightness value
#                       The script then iterates through a list of brightness levels,
#                       performing a stress test.
#                       Verification Details:
#                       The test script verifies the DisplayCaps from the ETL for HDR support in the EDID.
#                       Post enabling HDR, the status_code returned from the OS API is decoded and verified.
#                       Pipe_Misc register is also verified for HDR_Mode
#                       Plane and Pipe Verification is performed by iterating through each of the displays
#                       Metadata verification, by comparing the Default and Flip Metadata is performed,
#                       along with register verification; DPCD verification is performed.
#                       In case of Aux based panel, DPCD verification is performed.
# Sample CommandLines:  python hdr_with_csc.py -edp_a SINK_EDP50 -config SINGLE
# Sample CommandLines:  python hdr_with_csc.py -edp_a SINK_EDP76 -config SINGLE
# @author       Smitha B
#######################################################################################################################
import DisplayRegs
from Tests.Color.Features.E2E_HDR.hdr_test_base import *
from Tests.Color.Features.ApplyCSC.apply_csc_base import *
from Tests.Color.Common import color_mmio_interface

mmio_interface = color_mmio_interface.ColorMmioInterface()


class HDRWithCSC(HDRTestBase, ApplyCSCTestBase):

    def runTest(self):
        ##
        # Apply a csc matrix and verify before enabling HDR
        logging.info("*** Step 1 : Invoke the escape call to apply CSC input from Command Line and verify ***")
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if color_escapes.configure_pipe_csc(port, panel.display_and_adapterInfo, self.csc_type,
                                                    self.matrix_info, True) is False:
                    logging.error(
                        "FAIL : Driver failed to apply CSC on {0} connected to {1} on Adapter {2}".format(
                            port, panel.pipe, gfx_index))
                    self.fail()

        ##
        # Enable HDR on all the supported panels and perform verification
        logging.info("*** Step 2 : Enable HDR on all supported panels and verify ***")
        if self.toggle_hdr_on_all_supported_panels(enable=True) is False:
            self.fail()

        ##
        # Verify the CSC has has been disabled in HDR Mode
        logging.info(
            "*** Step 3 : Verify if Linear CSC has been disabled as HDR has been enabled ***") if self.csc_type == color_enums.CscMatrixType.LINEAR_CSC.value else logging.info(
            "*** Step 3 : Verify if Non_Linear CSC is persisting as HDR has been enabled ***")
        for gfx_index, adapter in self.context_args.adapters.items():
            regs = DisplayRegs.get_interface(adapter.platform, gfx_index)
            for port, panel in adapter.panels.items():
                color_ctl_offsets = regs.get_color_ctrl_offsets(panel.pipe)
                csc_mode_val = mmio_interface.read(gfx_index, color_ctl_offsets.CscMode)
                color_ctl_values = regs.get_colorctl_info(panel.pipe, ColorCtlOffsetsValues(
                    CscMode=csc_mode_val))
                if self.csc_type == color_enums.CscMatrixType.LINEAR_CSC.value and color_ctl_values.PipeCscEnable:
                    logging.error(
                        "FAIL : Linear CSC is persisting on {0} connected to {1} on Adapter {2} in HDR Mode".format(
                            port, panel.pipe, gfx_index))
                    gdhm.report_driver_bug_os("[{0}] Linear CSC is persisting on {0} connected to {1} on Adapter {2} in HDR Mode".format(
                           adapter.platform, port, panel.pipe, gfx_index))
                    self.fail()
                elif self.csc_type == color_enums.CscMatrixType.NON_LINEAR_CSC.value and color_ctl_values.PipeOutputCscEnable == 0:
                    logging.error(
                        "FAIL : Non_Linear CSC is not persisting on {0} connected to {1} on Adapter {2} in HDR Mode".format(
                            port, panel.pipe, gfx_index))
                    gdhm.report_driver_bug_os("[{0}] Non_Linear CSC is not persisting on {1} connected to {2} on Adapter {3} in HDR Mode".format(
                            adapter.platform,port, panel.pipe, gfx_index))
                    self.fail()
                csc_persistence = color_ctl_values.PipeCscEnable if self.csc_type == color_enums.CscMatrixType.LINEAR_CSC.value else color_ctl_values.PipeOutputCscEnable
                logging.info(
                    "PASS : {0} CSC persistence EXPECTED {1}; ACTUAL {2} on {3} connected to {4} on Adapter {5} "
                    "in HDR Mode".format(
                        color_enums.CscMatrixType(self.csc_type).name,
                        feature_basic_verify.BIT_MAP_DICT[int(csc_persistence)],
                        feature_basic_verify.BIT_MAP_DICT[int(csc_persistence)], port, panel.pipe, gfx_index))
                if self.csc_type == color_enums.CscMatrixType.NON_LINEAR_CSC.value:
                    if self.enable_and_verify(adapter.gfx_index, adapter.platform, panel.pipe,
                                              panel.display_and_adapterInfo, port, False) is False:
                        self.fail()

        ##
        # Apply a csc matrix and verify if CSC is disabled as HDR is enabled
        logging.info("*** Step 4 : Invoke the escape call to apply an Identity CSC in HDR Mode and verify ***")
        self.matrix_info = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                csc_persistence_with_hdr = color_escapes.configure_pipe_csc(port, panel.display_and_adapterInfo,
                                                                            self.csc_type,
                                                                            self.matrix_info, True)

                if self.csc_type == color_enums.CscMatrixType.LINEAR_CSC.value and csc_persistence_with_hdr:
                    logging.error(
                        "FAIL : {0} CSC is persisting on {1} connected to {2} on Adapter {3} in HDR Mode".format(
                            color_enums.CscMatrixType(self.csc_type).name, port, panel.pipe, gfx_index))
                    gdhm.report_driver_bug_os("[{0}] {1} CSC is persisting on {2} connected to {3} on Adapter {4} in HDR Mode".format(
                             adapter.platform,color_enums.CscMatrixType(self.csc_type).name, port, panel.pipe, gfx_index))
                    self.fail()
                elif self.csc_type == color_enums.CscMatrixType.NON_LINEAR_CSC.value and csc_persistence_with_hdr is False:
                    logging.error(
                        "FAIL : {0} CSC is not persisting on {1} connected to {2} on Adapter {3} in HDR Mode".format(
                            color_enums.CscMatrixType(self.csc_type).name, port, panel.pipe, gfx_index))
                    gdhm.report_driver_bug_os("[{0}] {1} CSC is not persisting on {2} connected to {3} on Adapter {4} in HDR Mode".format(
                            adapter.platform,color_enums.CscMatrixType(self.csc_type).name, port, panel.pipe, gfx_index))
                    self.fail()
                logging.info(
                    "PASS : {0} CSC persistence EXPECTED {1}; ACTUAL {2} on {3} connected to {4} on Adapter {5} "
                    "in HDR Mode".format(
                        self.csc_type,
                        feature_basic_verify.BIT_MAP_DICT[int(csc_persistence_with_hdr)],
                        feature_basic_verify.BIT_MAP_DICT[int(csc_persistence_with_hdr)], port, panel.pipe,
                        gfx_index))
                if self.csc_type == color_enums.CscMatrixType.NON_LINEAR_CSC.value:
                    if self.enable_and_verify(adapter.gfx_index, adapter.platform, panel.pipe,
                                              panel.display_and_adapterInfo, port, False) is False:
                        self.fail()

        ##
        # Disable HDR on all the supported panels and perform verification
        logging.info("*** Step 5 : Disable HDR on all supported panels and verify ***")
        if self.toggle_hdr_on_all_supported_panels(enable=False) is False:
            self.fail()

        ##
        # Verify the CSC has taken effect since HDR has been disabled
        logging.info("*** Step 4 : Verify the CSC has taken effect since HDR has been disabled ***")
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if self.enable_and_verify(adapter.gfx_index, adapter.platform, panel.pipe,
                                          panel.display_and_adapterInfo, port, configure_csc=False) is False:
                    logging.error(
                        "FAIL : Driver failed to apply Identity {0} which was applied while in HDR Mode on {1} "
                        "connected to {2} on Adapter {3}".format(
                            color_enums.CscMatrixType(self.csc_type).name, port, panel.pipe, gfx_index))
                    gdhm.report_driver_bug_os("[{0}] Driver failed to apply Identity {1} which was applied while in HDR Mode on {2} "
                        "connected to {3} on Adapter {4}".format(
                            adapter.platform,color_enums.CscMatrixType(self.csc_type).name, port, panel.pipe, gfx_index))
                    self.fail()
                logging.info(
                    "PASS : Driver successfully applied Identity {0} which was applied while in HDR Mode on {1} "
                    "connected to {2} on Adapter {3}".format(
                        color_enums.CscMatrixType(self.csc_type).name, port, panel.pipe, gfx_index))


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
