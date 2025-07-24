#######################################################################################################################
# @file         hdcp_opm_time_bomb_check.py
# @brief        OPM time bomb check
# @details      Test for verifying HDCP 1.4 & 2.2 with DP MST daisy chain connection
#
# @author       chandrakanth Reddy y
#######################################################################################################################

from Tests.HDCP.hdcp_base import *


##
# @brief        Contains HDCP tests with DP MST topology using North Gate
class HdcpRepeater(HDCPBase):
    ##
    # @brief runTest function of Unit Test FrameWork.
    # @return None
    def runTest(self):
        # get the HDCP displays
        displays = [port for port in self.display_list if display_utility.get_vbt_panel_type(port, 'gfx_0')
                    not in [display_utility.VbtPanelType.LFP_DP, display_utility.VbtPanelType.LFP_MIPI]]
        # Verify HDCP with DP Repeater(MST)
        alert.info("Please connect {0} DP Displays in Daisy Chain mode on {1}".format(self.mst_depth, displays[0]))
        while True:
            if self.verify_mst(displays[0], self.mst_depth):
                break
            else:
                alert.error(f"{self.mst_depth} displays not connected in Daisy chain on {displays[0]}")

        if self.multi_display_single_session() is False:
            self.fail("HDCP Enable failed")
        logging.info("HDCP Enabled successfully")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)


