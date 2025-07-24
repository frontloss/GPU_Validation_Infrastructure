#######################################################################################################################
# @file                 hdr_with_async_flips.py
# @addtogroup           Test_Color
# @section              hdr_with_async_flips
# @remarks              @ref hdr_with_async_flips.py \n
#                       The test script enables HDR on all HDR supported displays,
#                       input from the test command line.
#                       Verification Details:
#                       The test script verifies the DisplayCaps from the ETL for HDR support in the EDID.
#                       Post enabling HDR, the status_code returned from the OS API is decoded and verified.
#                       Pipe_Misc register is also verified for HDR_Mode
#                       Plane and Pipe Verification is performed by iterating through each of the displays
#                       Metadata verification, by comparing the Default and Flip Metadata is performed,
#                       along with register verification; DPCD verification is performed.
#                       In case of Aux based panel, DPCD verification is performed.
# Sample CommandLines:  python hdr_with_async_flips.py -edp_a SINK_EDP50 -config SINGLE
# Sample CommandLines:  python hdr_with_async_flips.py -edp_a SINK_EDP76 -config SINGLE
# @author       Smitha B
#######################################################################################################################
from Tests.Color.Features.E2E_HDR.hdr_test_base import *


class HDRWithAsyncFlips(HDRTestBase):
    flip_stream_artifactory = os.getcwd()[:2] + "\SHAREDBINARY\926864574"

    def setUp(self):
        self.custom_tags["-STREAM"] = None
        ##
        # Invoking Common BaseClass's setUp() to perform all the basic functionalities
        super().setUp()
        self.stream = self.context_args.test.cmd_params.test_custom_tags["-STREAM"]

    def runTest(self):
        ##
        # Enable HDR on all the supported panels and perform verification
        logging.info("*** Step 1 : Enable HDR on all supported panels and verify ***")
        ##
        # Enable HDR on all the supported panels and perform basic verification
        if self.toggle_hdr_on_all_supported_panels(enable=True) is False:
            self.fail()

        ##
        # Parse the async_stream.xml to get the command line for the input stream
        logging.info("*** Step 2 : AsyncFlips and verify ***")
        xml_tree = ET.parse("%s\AsyncFlips\\async_streams.xml" % self.flip_stream_artifactory)
        if not xml_tree:
            logging.error("FAIL : The streams file is not found. Exiting the test")
            self.fail()
        stream_info = xml_tree.getroot()
        stream = stream_info.find("./Stream[@name='%s']" % self.stream)

        command_line = stream.find("./Command").text

        os.system("%s\AsyncFlips\GfxBench\\x64\GfxPlayer.exe %s %s\AsyncFlips\%s\capture.lcs2"
                  % (self.flip_stream_artifactory, command_line, self.flip_stream_artifactory, self.stream))


        logging.info("*** Step 3 : Perform HDR Verification after enabling AsyncFlips ***")
        ##
        # Perform Plane and Pipe Verification after Enabling HDR
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if self.plane_verification(gfx_index, adapter.platform, panel, 1) is False:
                    return False
                if self.pipe_verification(gfx_index, adapter.platform, port, panel) is False:
                    return False


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
