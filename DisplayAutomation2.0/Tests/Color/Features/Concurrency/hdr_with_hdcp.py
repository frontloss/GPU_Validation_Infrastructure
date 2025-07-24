#######################################################################################################################
# @file         hdr_with_hdcp.py
# @brief        HDR Concurrency tests with HDCP authentication flow verification
# @details      Test for verifying HDCP 1.4 & 2.2 authentication flow using ETL for HDMI & DP where HDR Mode is enabled
#
# @author       Smitha B
#######################################################################################################################

from Tests.HDCP.hdcp_base import *
from Tests.Color.Features.E2E_HDR.hdr_test_base import *
from Tests.HDCP.verify_hdcp_flow import verify_hdcp
from Libs.Core.logger import etl_tracer


##
class HdcpBasic(HDCPBase, HDRTestBase):
    ##
    # @brief runTest function of Unit Test FrameWork.
    # @return None
    def runTest(self):
        ##
        # Enable HDR on all the supported panels and perform verification
        if self.enable_hdr_and_verify() is False:
            self.fail()

        # Get the HDCP displays
        displays = [port for port in self.display_list if display_utility.get_vbt_panel_type(port, 'gfx_0')
                    not in [display_utility.VbtPanelType.LFP_DP, display_utility.VbtPanelType.LFP_MIPI]]

        etl_tracer.stop_etl_tracer()
        if etl_tracer.start_etl_tracer() is False:
            self.fail("Failed to start ETL Tracer")

        logging.info("\t STEP : Verify HDCP on {}".format(displays))
        if self.multi_display_single_session() is False:
            logging.error("HDCP verification Failed")
        # minimum wait time to check for any Link Integrity failures
        etl_tracer.stop_etl_tracer()

        etl_file_path = etl_tracer.GFX_TRACE_ETL_FILE
        if os.path.exists(etl_tracer.GFX_TRACE_ETL_FILE):
            file_name = 'GfxTrace_hdcp_' + str(time.time()) + '.etl'
            etl_file_path = os.path.join(test_context.LOG_FOLDER, file_name)
            os.rename(etl_tracer.GFX_TRACE_ETL_FILE, etl_file_path)

        if etl_tracer.start_etl_tracer() is False:
            logging.error("Failed to start ETL Tracer")

        if verify_hdcp(PLATFORM_INFO['gfx_0']['name'], displays, etl_file_path, self.hdcp_type) is False:
            self.fail("HDCP verification Failed")

        logging.info("\tPASS : HDCP verification successful")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)