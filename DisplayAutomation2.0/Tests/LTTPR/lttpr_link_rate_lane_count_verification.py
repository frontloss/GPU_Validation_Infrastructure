#####################################################################################
# @file
# @brief This test fetches the EDID, DPCD and get the no. of active non-transparent mode LTTPRs between DPTX and DPRX.
# @details This test verifies the presence of non-transparent mode LTTPRs between DPTX and DPRX by getting the link training data between DPTX and LTTPR,
# and check the DP1.4/DP2.1 Link Training flow.
# Command line : python Tests\LTTPR\lttpr_link_rate_lane_count_verification.py -[hdmi_*/dp_*]
# @author  Neha Kumari
######################################################################################

import logging
import sys
import unittest

from Tests.LTTPR.lttpr_base import LttprBase
from Libs.Core.logger import gdhm
from Libs.Core import display_utility, enum, driver_escape
from Libs.Core.test_env.test_environment import TestEnvironment

LTTPR_MAX_LINK_RATE = 0xF0001
MAX_LINK_RATE_8b_10b = 0x00001
MAX_LINK_RATE_128b_132b = 0x02200
MAIN_LINK_CHANEL_CODING_CAP = 0X00006
LINK_BW_SET = 0x100
LINK_RATES = {6: 1.62, 10: 2.7, 20: 5.4, 30: 8.1, 1: 10, 2: 20, 4: 13.5}
LANE_COUNT = {1: "1 Lane", 2: "2 Lanes", 4: "4 Lanes"}
PHY_REPEATER_CNT = {"0x1": 8, "0x2": 7, "0x4": 6, "0x8": 5, "0x10": 4, "0x20": 3, "0x40": 2, "0x80": 1, "0xff": 9}

##
# @brief This class has the test implementation to verify whether link is trained properly with required link rates and lane counts
# based on link rate and lane count required by LTTPR and sink. LTTPR is there in between DPTX and DPRX, so 
# link has to got trained with min. link rate and lane count of the path.
# @return None
class LttprLinkRateLaneCountVerification(LttprBase):
    ##
    # @brief Unit-test runTest function. Plug the required display and start the LTTPR verification.
    # @return None
    def runTest(self):
        for display_port, edid_dpcd in self.display_edid_dpcd.items():
            # Plug the display
            if not display_utility.plug(port=display_port, edid=edid_dpcd[1], dpcd=edid_dpcd[2], gfx_index=edid_dpcd[0]):
                self.fail(f"FAIL: Plug of display {display_port} Failed")
            # set display config
            self.display_and_adapter_info = self.display_config.get_display_and_adapter_info_ex(display_port, gfx_index=edid_dpcd[0])
            if self.display_config.set_display_configuration_ex(enum.SINGLE, [self.display_and_adapter_info]) is False:
                self.fail("FAIL: SetDisplayConfigurationEX returned false")
            else:       
                logging.info("************** LTTPR Verification Started **************")
                self.verify_lttpr_programming(self.display_and_adapter_info, gfx_index=edid_dpcd[0])


    ##
    # @brief Create a list of DP1.4 link rate and lane count DPCD offset values.
    # @param[in] display_and_adapter_info display_and_adapter_info passed.
    # @return panel_details list
    def panel_link_rate_lane_count_8b10b(self, display_and_adapter_info):
        panel_details = []
        flag, panel_caps = driver_escape.read_dpcd(display_and_adapter_info, MAX_LINK_RATE_8b_10b)
        if not flag:
            self.fail("DPCD read Failed.")
        panel_max_link_rate, panel_max_lane_count = panel_caps[0], panel_caps[1]
        panel_max_link_rate = LINK_RATES[panel_max_link_rate]
        # Bitwise ANDing value at panel_max_lane_count with 0xF to get the first 4 bits that will specify the lane count.
        panel_max_lane_count = panel_max_lane_count & 0xF
        panel_details.append(panel_max_link_rate) 
        panel_details.append(panel_max_lane_count)
        logging.debug(f"panel max. link rate: {panel_max_link_rate}, panel max. lane count: {panel_max_lane_count}")
        return panel_details

    ##
    # @brief Create a list of LTTPR link rate and lane count DPCD offset values.
    # @param[in] display_and_adapter_info display_and_adapter_info passed.
    # @return lttpr_details list
    def lttpr_link_rate_lane_count_8b10b(self, display_and_adapter_info):
        lttpr_details = []
        flag, lttpr_caps = driver_escape.read_dpcd(display_and_adapter_info, LTTPR_MAX_LINK_RATE)
        if not flag:
            self.fail("DPCD read Failed.")
        lttpr_max_link_rate, lttpr_max_lane_count = lttpr_caps[0], lttpr_caps[3]
        lttpr_max_link_rate = LINK_RATES[lttpr_max_link_rate]
        # Bitwise ANDing value at lttpr_max_lane_count with 0xF to get the first 4 bits that will specify the lane count.
        lttpr_max_lane_count = lttpr_max_lane_count & 0xF
        lttpr_details.append(lttpr_max_link_rate)
        lttpr_details.append(lttpr_max_lane_count)
        logging.debug(f"LTTPR max. link rate: {lttpr_max_link_rate}, LTTPR max. lane count: {lttpr_max_lane_count}")
        return lttpr_details
  
    ##
    # @brief Create a list of DP2.1 link rate and lane count DPCD offset values.
    # @param[in] display_and_adapter_info display_and_adapter_info passed.
    # @return panel_details list
    def panel_link_rate_lane_count_128b132b(self, display_and_adapter_info):
        panel_details = []
        flag, panel_caps = driver_escape.read_dpcd(display_and_adapter_info, MAX_LINK_RATE_128b_132b)
        if not flag:
            self.fail("DPCD read Failed.")
        panel_max_link_rate, panel_max_lane_count = panel_caps[15], panel_caps[2]
        panel_max_link_rate = LINK_RATES[panel_max_link_rate]
        # Bitwise ANDing value at panel_max_lane_count with 0xF to get the first 4 bits that will specify the lane count.
        panel_max_lane_count = panel_max_lane_count & 0xF
        panel_details.append(panel_max_link_rate) 
        panel_details.append(panel_max_lane_count)
        logging.debug(f"panel max. link rate: {panel_max_link_rate}, panel max. lane count: {panel_max_lane_count}")
        return panel_details

    ##
    # @brief Create a list of LTTPR link rate and lane count DPCD offset values.
    # @param[in] display_and_adapter_info display_and_adapter_info passed.
    # @return lttpr_details list
    def lttpr_link_rate_lane_count_128b132b(self, display_and_adapter_info):
        lttpr_details = []
        flag, lttpr_caps = driver_escape.read_dpcd(display_and_adapter_info, LTTPR_MAX_LINK_RATE)
        if not flag:
            self.fail("DPCD read Failed.")
        lttpr_max_link_rate, lttpr_max_lane_count = lttpr_caps[6], lttpr_caps[3]
        lttpr_max_link_rate = LINK_RATES[lttpr_max_link_rate]
        # Bitwise ANDing value at lttpr_max_lane_count with 0xF to get the first 4 bits that will specify the lane count.
        lttpr_max_lane_count = lttpr_max_lane_count & 0xF
        lttpr_details.append(lttpr_max_link_rate)
        lttpr_details.append(lttpr_max_lane_count)
        logging.debug(f"LTTPR max. link rate: {lttpr_max_link_rate}, LTTPR max. lane count: {lttpr_max_lane_count}")
        return lttpr_details

    ##
    # @brief Create a list of DP and LTTPR DPCD offset values.
    # Compare those offset values with link rate and lane count on which link got trained.
    # The link must got trained with min.(link rate,lane count) of LTTPR and sink.
    # @param[in] display_and_adapter_info display_and_adapter_info passed.
    # @param[in]    gfx_index: str
    # @return None
    def verify_lttpr_programming(self, display_and_adapter_info, gfx_index = None):

        # Reading DPCD offset values.
        # Reading the LTTPR link rate and lane count DPCD.
        flag, lttpr_caps = driver_escape.read_dpcd(display_and_adapter_info, LTTPR_MAX_LINK_RATE)
        if not flag:
            self.fail("DPCD read Failed.")
        lttpr_operating_mode = lttpr_caps[2]
        phy_repeater_cnt = PHY_REPEATER_CNT[hex(lttpr_caps[1])]

        # Reading the channel encoding DPCD.
        dpcd_read_flag, dpcd_value = driver_escape.read_dpcd(display_and_adapter_info, MAIN_LINK_CHANEL_CODING_CAP)
        if dpcd_read_flag == True:
            if dpcd_value[0] == 3:
                logging.info(f"Display connected on port supports 128b/132b channel encoding")
                panel_details = self.panel_link_rate_lane_count_128b132b(display_and_adapter_info)
                lttpr_details = self.lttpr_link_rate_lane_count_128b132b(display_and_adapter_info)
            else:
                logging.info(f"Display connected on port supports 8b/10b channel encoding")
                panel_details = self.panel_link_rate_lane_count_8b10b(display_and_adapter_info)
                lttpr_details = self.lttpr_link_rate_lane_count_8b10b(display_and_adapter_info)
        else:
            self.fail("DPCD read Failed.")

        # Checking the actual link rate and lane count of the link trained with.
        flag, programmed_lt_values = driver_escape.read_dpcd(display_and_adapter_info, LINK_BW_SET)
        if not flag:
            self.fail("DPCD read Failed.")
        actual_link_rate, actual_lane_count = programmed_lt_values[0], programmed_lt_values[1]
        actual_link_rate = LINK_RATES[actual_link_rate]
        # Bitwise ANDing value at panel_max_lane_count with 0xF to get the first 4 bits that will specify the lane count.
        actual_lane_count = actual_lane_count & 0xF

        # Getting min. link rate and lane count or expected link rate and lane count
        # on which link is expected to be trained with.
        expected_link_rate = min(panel_details[0], lttpr_details[0])
        expected_lane_count = min(panel_details[1], lttpr_details[1])

        logging.info(f"No. of LTTPRs in between DPTX and DPRX is : {phy_repeater_cnt}")

        if not (expected_link_rate == actual_link_rate and expected_lane_count == actual_lane_count) :
            if (phy_repeater_cnt < 9):
                gdhm.report_driver_bug_di(f'[Interfaces][LTTPR] Failure is seen in link training. Link got trained with incorrect link rate and lane count. in {gfx_index}')
                self.fail(f"[Link Rate, Lane Count] -  Actual: {actual_link_rate,  LANE_COUNT[actual_lane_count]}, Expected: {expected_link_rate, LANE_COUNT[expected_lane_count] }, Expected link rate and actual LT values are NOT matching.")
            else:
                # In case of no. of LTTPR greater than 8, which is not possible according to spec, the link will get trained with panel capabilities.
                # LTTPR will not be there at the path between DPTX and DPRX.
                # In that case actual link rate and lane count will be the one defined for panel's DPCD.
                # But, expected we are calculating min. link rate/lane count of (LTTPR and panel),
                # so, actual and expected link rate and lane count will not match.
                logging.info("No. of LTTPR is more than 8.")
                logging.info(f'[Link Rate, Lane Count] -  Actual: {actual_link_rate,  LANE_COUNT[actual_lane_count]}, Expected: {expected_link_rate, LANE_COUNT[expected_lane_count] }')
                logging.info("Expected Behavior: expected link rate and actual LT values are NOT matching")
                if hex(lttpr_operating_mode) != "0xAA":
                    logging.info("LTTPR is operating in transparent mode.")
                else:
                    gdhm.report_driver_bug_di('[Interfaces][LTTPR] LTTPR is operating in non-transparent mode.')
                    self.fail("LTTPR is operating in non-transparent mode.")
        else:
            logging.info("Expected link rate and actual LT values are matching")
            logging.info(f'[Link Rate, Lane Count] -  Actual: {actual_link_rate,  LANE_COUNT[actual_lane_count]}, Expected: {expected_link_rate, LANE_COUNT[expected_lane_count] }')
            
        logging.info("************** LTTPR Verification Completed **************")

if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)  
    
