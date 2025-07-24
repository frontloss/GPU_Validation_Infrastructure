#######################################################################################################################
# @file         hdcp_basic.py
# @brief        HDCP authentication flow verification tests
# @details      Test for verifying HDCP 1.4 & 2.2 authentication flow using ETL for HDMI & DP
#
# @author       chandrakanth Reddy y
#######################################################################################################################

from Tests.HDCP.hdcp_base import *
from Tests.HDCP.verify_hdcp_flow import verify_hdcp
from Libs.Core.logger import etl_tracer


##
# @brief        Contains HDCP tests with ETL based verification
class HdcpBasic(HDCPBase):
    ##
    # @brief runTest function of Unit Test FrameWork.
    # @return None
    def runTest(self):
        # Apply the configuration passed in cmdline
        topology = eval("enum.%s" % (self.cmd_line_param['CONFIG']))
        if self.display_config.set_display_configuration_ex(topology, self.display_list,
                                                            self.enumerated_displays) is False:
            self.fail("FAIL: Failed to apply display configuration {} on displays {}".
                      format(self.cmd_line_param['CONFIG'], self.display_list))
        time.sleep(OPM_LITE_RE_INTIALIZE_DURATION)
        # get the HDCP displays
        displays = [port for port in self.display_list if display_utility.get_vbt_panel_type(port, 'gfx_0')
                    not in [display_utility.VbtPanelType.LFP_DP, display_utility.VbtPanelType.LFP_MIPI]]

        etl_tracer.stop_etl_tracer()
        if etl_tracer.start_etl_tracer() is False:
            self.fail("Failed to start ETL Tracer")

        logging.info("\t STEP : Verify HDCP on {}".format(displays))
        if len(self.display_list) == 1:
            status = self.single_display_single_session()
        elif len(self.display_list) > 1:
            status = self.multi_display_single_session()

        if status is False:
            logging.error("HDCP verification Failed")

        # minimum wait time to check for any Link Integrity failures
        time.sleep(5)
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