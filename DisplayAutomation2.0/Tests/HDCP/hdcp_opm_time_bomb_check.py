#######################################################################################################################
# @file         hdcp_opm_time_bomb_check.py
# @brief        OPM time bomb check
# @details      Test for verifying HDCP 1.4 & 2.2 with & without OPM time Bomb expire(one month)
#
# @author       chandrakanth Reddy y
#######################################################################################################################

from Tests.HDCP.hdcp_base import *
from datetime import datetime
import win32api


##
# @brief        Contains HDCP tests with OPM tool time expire
class OpmTimeBomb(HDCPBase):
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

        logging.info("\t STEP : Verify HDCP on {}".format(displays))
        if self.multi_display_single_session() is False:
            self.fail("HDCP verification Failed")
        logging.info("\tPASS : HDCP verification successful")

        current_system_time = datetime.now()

        logging.info("Changing system time to one month forward")
        # set new system time
        if set_new_time(current_system_time, month_forward=True) is False:
            self.fail("Failed to change the system time")

        logging.info("\t STEP : Verify HDCP after system time change on {}".format(displays))
        for port in displays:
            if self.enable_hdcp(port_id=self.display_list.index(port)) is False:
                self.fail("HDCP verification Failed")
        logging.info("\tPASS : HDCP is enabled after system time change")

        logging.info("Change back the system time to previous original time")
        # Reset the time to current system time
        if set_new_time(current_system_time) is False:
            self.fail('Failed to reset the system time')


##
# @brief        Method to change the system time
# @param[in]    new_time datetime object
# @param[in]    month_forward True-to change the system time to one month forward else False
# @return       True if the system time updated correctly otherwise False
def set_new_time(new_time, month_forward=False):
    month = new_time.month
    year = new_time.year
    if month_forward:
        # change both month & year if the current month is December
        if new_time.month == 12:
            month = 1
            year += 1
        else:
            month += 1
    time_tuple = (year, month, new_time.day, new_time.hour, new_time.minute, new_time.second,
                  new_time.microsecond // 1000)

    day = datetime(*time_tuple).isocalendar()[2]
    t = time_tuple[:2] + (day,) + time_tuple[2:]
    win32api.SetSystemTime(*t)
    # check the system time changed or not
    system_time = datetime.now()
    if system_time.month == month:
        return True
    return False


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
