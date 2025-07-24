#######################################################################################################################
# @file                 color_transforms_sdr_hdr.py
# @addtogroup           Test_Color
# @section              color_transforms_sdr_hdr
# @remarks              @ref color_transforms_sdr_hdr.py \n
#                       The test script enables HDR on the displays supporting HDR,
#                       which is an input parameter from the test command line.
#                       Additionally, for an eDP_HDR display the script invokes the API
#                       to set the OS Brightness Slider level to a value provided in the command line.
#                       If Brightness Slider level has not been given as an input, script sets the slider
#                       to a random value other than the Current Brightness value.
#                       Verification Details:
#                       Gamma with different scale factors will be applied at the beginning of the test.
#                       This should take effect in the programmed values
#                       The test script verifies the DisplayCaps from the ETL for HDR support in the EDID.
#                       Post enabling HDR, the status_code returned from the OS API is decoded and verified.
#                       Pipe_Misc register is also verified for HDR_Mode
#                       Plane and Pipe Verification is performed by iterating through each of the displays
#                       Metadata verification, by comparing the Default and Flip Metadata is performed,
#                       along with register verification
# Sample CommandLines:  python color_transforms_sdr_hdr.py -edp_a SINK_EDP50 -config SINGLE
# Sample CommandLines:  python color_transforms_sdr_hdr.py -edp_a SINK_EDP76 -config SINGLE
# @author       Smitha B
#######################################################################################################################
from Tests.Color.Features.E2E_HDR.hdr_test_base import *


class ColorTransformsSDR_HDR(HDRTestBase):

    @unittest.skipIf(common_utility.get_action_type() != "BASIC",
                     "Skip the  test step as the action type is not basic")
    def runTest(self):
        ##
        # Enable HDR on all the supported panels and perform verification
        if self.enable_hdr_and_verify() is False:
            self.fail()

        ##
        # Applying Gamma with a scalefactor for each of the channels at the beginning of the test after enabling HDR
        gamma_utility.apply_gamma(r_factor=0.76, g_factor=0.87, b_factor=0.99)

        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active:
                    if self.pipe_verification(gfx_index, adapter.platform, port, panel) is False:
                        self.fail()


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
