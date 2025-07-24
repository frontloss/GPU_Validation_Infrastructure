#######################################################################################################################
# @file                 hdr_with_rotation.py
# @addtogroup           Test_Color
# @section              hdr_with_rotation
# @remarks              @ref hdr_with_rotation.py \n
#                       The test script enables HDR on the displays supporting HDR,
#                       which is an input parameter from the test command line.
#                       Test intends to iterate through a list a angles which will be applied through a modeset
#                       Verification Details:
#                       The test script verifies the DisplayCaps from the ETL for HDR support in the EDID.
#                       Post enabling HDR, the status_code returned from the OS API is decoded and verified.
#                       Pipe_Misc register is also verified for HDR_Mode
#                       Plane and Pipe Verification is performed by iterating through each of the displays
#                       Metadata verification, by comparing the Default and Flip Metadata is performed,
#                       along with register verification
# Sample CommandLines:  python hdr_with_rotation.py -edp_a SINK_EDP50 -config SINGLE
# Sample CommandLines:  python hdr_with_rotation.py -edp_a SINK_EDP76 -config SINGLE
# @author       Smitha B
#######################################################################################################################
import random
from Libs.Core.display_config import display_config, display_config_enums
from Libs.Core import registry_access
from Tests.Display_Decompression.Playback import decomp_verifier
from Tests.Color.Features.E2E_HDR.hdr_test_base import *


class HDRWithRotation(HDRTestBase):
    config = display_config.DisplayConfiguration()

    def media_decomp_setup(self):
        ##
        # Check for master registry key - DisableE2ECompression (TGL+)
        if decomp_verifier.PLATFORM_NAME in decomp_verifier.GEN12_PLUS_PLATFORM:
            legacy_reg_args = registry_access.LegacyRegArgs(hkey=registry_access.HKey.LOCAL_MACHINE,
                                                            reg_path=decomp_verifier.INTEL_GMM_PATH)
            registry_value, _ = registry_access.read(legacy_reg_args, "DisableE2ECompression", sub_key="GMM")
            if registry_value == 0:
                logging.error("E2ECompression is enabled; Hence HWRotation cannot be verified (Mutually Exclusive")
                self.fail("E2ECompression is enabled - DisableE2ECompression [{}]".format(registry_value))
            elif registry_value:
                logging.info("E2ECompression is disabled")
            else:
                logging.error(f"E2ECompression Master Registry path/key is not available. Returned value - "
                              f"{registry_value}")
                self.fail(f"E2ECompression Master Registry path/key is not available. Returned value - "
                          f"{registry_value}")

    def runTest(self):
        ##
        # Since HW Rotation and E2E Media Compression are mutually exclusive, verify if the registry key has been
        # disabled
        self.media_decomp_setup()

        rotation_angles = [enum.ROTATE_90, enum.ROTATE_270]
        scaling = [enum.MAR, enum.CAR, enum.CI, enum.FS]

        ##
        # Enable HDR on all the supported panels and perform basic verification
        if self.toggle_hdr_on_all_supported_panels(enable=True) is False:
            return False

        media_list = [('Color\HDR\Video', 'Life_Of_Pi.mp4')]
        media_path = os.path.join(test_context.SHARED_BINARY_FOLDER, media_list[0][0])
        video_file = os.path.join(media_path, media_list[0][1])
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                mode_list = common_utility.get_modelist_subset(panel.display_and_adapterInfo, 1,
                                                               random.choice(scaling))
                if mode_list is None:
                    mode_list = common_utility.get_modelist_subset(panel.display_and_adapterInfo, 1, enum.MDS)
                for mode in mode_list:
                    for rotation_index in range(0, len(rotation_angles)):
                        mode.rotation = rotation_angles[rotation_index]
                        if self.config.set_display_mode([mode]):
                            logging.info("Rotation angle {0} has been applied successfully".format(
                                display_config_enums.Rotation(rotation_angles[rotation_index]).name))
                            if common_utility.launch_videoplayback(video_file, fullscreen=True):
                                if self.pipe_verification(gfx_index, adapter.platform, port, panel) is False:
                                    self.fail()
                            else:
                                self.fail()


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
