#######################################################################################################################
# @file                 hdr_with_media_decomp.py
# @addtogroup           Test_Color
# @section              hdr_with_media_decomp
# @remarks              @ref hdr_with_media_decomp.py \n
#                       Test scenario includes enabling HDR on all the panels,
#                       1. Verify if E2ECompression is enabled and if the platform supports Media Decompression
#                       2. Enable HDR on all the supported panels and perform verification of Plane and Pipe Blocks
#                       2. Start an ETL Capture and launch a video playback in Fullscreen
#                       3. Verify Media decompression by post processing the ETL which has been captured.
#                       Verification Details:
#                       The test script verifies the DisplayCaps from the ETL for HDR support in the EDID.
#                       Post enabling HDR, the status_code returned from the OS API is decoded and verified.
#                       Pipe_Misc register is also verified for HDR_Mode
#                       Plane and Pipe Verification is performed by iterating through each of the displays
#                       Metadata verification, by comparing the Default and Flip Metadata is performed,
#                       along with register verification;
#                       Media Decompression verification is performed
# Sample CommandLines:  python hdr_with_media_decomp.py -edp_a SINK_EDP50 -config SINGLE
# Sample CommandLines:  python hdr_with_media_decomp.py -edp_a SINK_EDP76 -config SINGLE
# @author       Smitha B
#######################################################################################################################
import DisplayRegs
from Libs.Core import winkb_helper, registry_access
from Tests.Color.Features.E2E_HDR.hdr_test_base import *
from Tests.Display_Decompression.Playback import decomp_verifier

MAX_LINE_WIDTH = 64


##
class HDRWithMediaDecomp(HDRTestBase):
    ##
    # Check all the pre-requisites required for Media Decompression
    def media_decomp_setup(self):
        ##
        # Check for master registry key - DisableE2ECompression (TGL+)
        if decomp_verifier.PLATFORM_NAME in decomp_verifier.GEN12_PLUS_PLATFORM:
            legacy_reg_args = registry_access.LegacyRegArgs(hkey=registry_access.HKey.LOCAL_MACHINE,
                                                            reg_path=decomp_verifier.INTEL_GMM_PATH)
            registry_value, _ = registry_access.read(legacy_reg_args, "DisableE2ECompression", sub_key="GMM")
            if registry_value == 0:
                logging.info("E2ECompression is enabled")
            elif registry_value == 1:
                logging.error("E2ECompression is disabled")
                self.fail("E2ECompression is disabled - DisableE2ECompression [{}]".format(registry_value))
            else:
                logging.info(f"E2ECompression Master Registry path/key is not available. Returned value - "
                             f"{registry_value}")

        ##
        # Check whether Platform supports Media Decompression
        assert decomp_verifier.is_feature_supported('MEDIA_DECOMP'), "Platform does not support Media " \
                                                                     "Decompression [Planning Issue]"

    def runTest(self):
        media_file_path = os.path.join(test_context.SHARED_BINARY_FOLDER, "MediaDecomp\Media Clip.mp4")
        ##
        # Check all the pre-requisites for Media Decompression
        self.media_decomp_setup()

        ##
        # Enable HDR on all the supported panels and perform verification
        # if self.enable_hdr_and_verify() is False:
        #     self.fail()
        ##
        # Enable HDR on all the supported panels and perform basic verification
        if self.toggle_hdr_on_all_supported_panels(enable=True) is False:
            return False

        ##
        # Start a new ETL Capture to verify Media Decompression
        if decomp_verifier.start_etl_capture() is False:
            self.fail("GfxTrace failed to start")

        # Minimize all windows before playback
        winkb_helper.press('WIN+M')

        # Play MTA App
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                logging.info("Invoke Media player with display {}".format(port))
                common_utility.launch_videoplayback(media_file_path, True)

                ##
                # SourcePixelFormat : default pixel format is YUV_420_Planar_8_bpc
                regs = DisplayRegs.get_interface(adapter.platform, gfx_index)

                plane_id = color_etl_utility.get_plane_id(panel.pipe, gfx_index)
                plane_ctl_info = regs.get_plane_ctl_info(plane_id, panel.pipe)
                source_pixel_format = color_constants.source_pixel_format_dict[plane_ctl_info.SourcePixelFormat]

                # Stop ETL Tracer
                playback_etl_file = decomp_verifier.stop_etl_capture(port)

                # Verify Media Decompression Programming
                if decomp_verifier.verify_media_decomp(port, source_pixel_format, playback_etl_file,
                                                       decomp_verifier.get_app_name('MEDIA')):
                    logging.info("Pass: Verification of Media Decompression".center(MAX_LINE_WIDTH, "_"))
                else:
                    logging.error("Fail: Verification of Media Decompression".center(MAX_LINE_WIDTH, "_"))
                    gdhm.report_driver_bug_os(
                        "[{0}] HDR with Media Decompression Verification - Port: {1} Adapter: {2} Source Pixel Format: {3}"
                        .format(adapter.platform, port, gfx_index, source_pixel_format))
                    self.fail("Fail: Verification of Media Decompression")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
