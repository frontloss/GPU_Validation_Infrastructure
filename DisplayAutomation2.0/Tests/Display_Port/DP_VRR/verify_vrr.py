#######################################################################################################################
# @file         verify_vrr.py
# @brief        This file contains vrr verification script to be used in VRR manual tests
# @details      This script verifies whether required HW registers are programmed according to Bspec, to enable
#               VRR (Variable refresh rate) for given mode (resolution and Refresh rate).
#               This script also verifies whether VRR live status bit is enabled or disabled based on user input.
#               If state requested is 'enabled', it will check for enable status on ports passed and
#               disable status on remaining active ports. If state requested is 'disabled', it will check for
#               disable status on all ports.
#
# @author       Sri Sumanth Geesala
#######################################################################################################################


import logging
import math
import sys
import time
import unittest

from Libs.Core import cmd_parser, driver_escape
from Libs.Core import display_essential
from Libs.Core import display_utility
from Libs.Core import winkb_helper
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE, Scaling
from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Feature.display_engine.de_base.display_base import DisplayBase
from registers.cnl import TRANS_VRR_CTL_REGISTER
from registers.mmioregister import MMIORegister

##
# @brief    Display Range limits class contains Mix and Max RR
class DisplayRangeLimits():
    ##
    # @brief    Initialize
    def __init__(self):
        self.ContFreqSup = 0
        self.RR_min = 0
        self.RR_max = 0


##
# callcounted Class used to register logging.error, for maintaining call count. This count will decide test pass/fail
class callcounted(object):
    """Decorator to determine number of calls for a method"""

    ##
    # @brief        Initialize
    # @param[in]    method
    def __init__(self, method):
        self.method = method
        self.counter = 0

    ##
    # @brief    Call method
    # @param[in]    args
    # @param[in]    kwargs
    # @return       call to init method
    def __call__(self, *args, **kwargs):
        self.counter += 1
        return self.method(*args, **kwargs)

##
# @brief    VerifyVRR Test Class
class VerifyVrr(unittest.TestCase):

    ##
    # @brief        This method performs setup for Verify VRR test script.
    # @return       None
    def setUp(self):
        logging.info("Starting Test Setup")
        self.config = DisplayConfiguration()
        self.machine_info = SystemInfo()
        logging.error = callcounted(logging.error)
        self.vrr_sup_platforms = ['glk', 'cnl', 'icllp', 'iclhp', 'lkf1']
        self.platform = None

        # check platform
        gfx_display_hwinfo = self.machine_info.get_gfx_display_hardwareinfo()
        # WA : currently test are execute on single platform. so loop break after 1 st iteration.
        # once Enable MultiAdapter remove the break statement.
        for i in range(len(gfx_display_hwinfo)):
            self.platform = ("%s" % gfx_display_hwinfo[i].DisplayAdapterName).lower()
            break

        if self.platform not in self.vrr_sup_platforms:
            self.fail('[Test Issue]: VRR is supported only on %s, current platform is %s' % (
                self.vrr_sup_platforms, self.platform))
        elif self.platform != 'cnl':  # for other platforms, use CNL register set
            self.platform = 'cnl'

        ##
        # parse command line and plug the displays.
        self.custom_cmd_tags = ['-state']
        self.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, self.custom_cmd_tags)
        self.plugged_display, self.enumerated_displays = display_utility.plug_displays(self, self.cmd_line_param)

        # print current configuration
        ret = self.config.get_current_display_configuration_ex(self.enumerated_displays)
        logging.info('Current display configuration is %s %s' % (ret[0], ret[1]))

        ##
        # get the active VRR displays list
        active_ports = self.get_active_ports()
        self.vrr_displays = self.get_vrr_capable_displays(
            active_ports)  # self.vrr_displays now contains the port: transcoder information. This can be consumed from tests.

        # get ports passed from command line. We should verify enable VRR state on these ports only.
        self.cmd_line_ports = []
        for key, value in self.cmd_line_param.items():
            if cmd_parser.display_key_pattern.match(key) is not None:
                connector_port_name = value['connector_port']
                self.cmd_line_ports.append(connector_port_name)

        if len(self.vrr_displays) == 0:
            self.fail(
                "[Test Issue]: This test requires VRR capable displays. None of the active displays are VRR capable")
        else:
            logging.info("VRR displays active are %s" % (self.vrr_displays))

    ##
    # @brief        This method performs teardown for Verify VRR test script.
    # @return       None
    def tearDown(self):
        logging.info("Starting Test Cleanup")
        ##
        # Unplug the displays and restore the configuration to the initial configuration.
        for display in self.plugged_display:
            logging.info("Trying to unplug %s" % (display))
            flag = display_utility.unplug(display)
            self.assertEquals(flag, True, 'Unplug of %s failed' % (display))

        ##
        # Check TDR.
        result = display_essential.detect_system_tdr(gfx_index='gfx_0')
        self.assertNotEquals(result, True, "[Driver Issue]: Aborting the test as TDR happened while executing the test")

        # report test failure if fail_count>0
        if (logging.error.counter > 0):
            self.fail(
                "Some checks in the test have failed. Check error logs. No. of failures= %d" % (logging.error.counter))

    ##
    # @brief        This method performs run test for Verify VRR test script.
    # @return       None
    def runTest(self):

        # get the expected state from command line params
        valid_states = ['DISABLED', 'ENABLED']
        if 'STATE' not in self.cmd_line_param.keys():
            self.fail('[Test Issue]: -state param is not provided in command line')
        if self.cmd_line_param['STATE'][0] not in valid_states:
            self.fail('[Test Issue]: wrong value passed to -state param in command line')
        expected_state = self.cmd_line_param['STATE'][0]

        if expected_state == 'ENABLED':
            # input("\n\n-------Test paused. Launch game application, Minimize game(Alt + Tab) and press enter here...")
            logging.info(
                '\n\n--------Put the game application to fullscreen immediately. Test will resume in 10 sec--------')
            time.sleep(10)
            logging.info('Test resumed.')

        # for each VRR display connected, check VRR register programming, and VRR status
        for disp in self.vrr_displays.items():
            # For extended mode where only 1 display will have async flip app running, VRR can enable on that display only.
            # This is controlled from command line by passing only those ports where we expect VRR enable.
            expected_state = self.cmd_line_param['STATE'][0]
            if expected_state == 'ENABLED':
                if disp[0] not in self.cmd_line_ports:
                    expected_state = 'DISABLED'

            logging.info('----Verifying VRR for %s------' % (disp[0]))
            target_id = self.config.get_target_id(disp[0], self.enumerated_displays)
            cur_mode = self.config.get_current_mode(target_id)
            logging.info(
                'Current mode on %s = %d x %d @%d Hz' % (disp[0], cur_mode.HzRes, cur_mode.VtRes, cur_mode.refreshRate))

            if expected_state == 'ENABLED':
                self.verify_vrr_registers(disp)
            cur_state = self.is_vrr_enabled(disp)
            cur_state = valid_states[cur_state]
            if cur_state == expected_state:
                logging.info(
                    'PASS: On %s, VRR live status, Expected= "%s", Actual= "%s"' % (disp[0], expected_state, cur_state))
            else:
                logging.error(
                    '[Driver Issue]: FAIL, On %s, VRR live status, Expected= "%s", Actual= "%s"' % (
                        disp[0], expected_state, cur_state))

        # show desktop to indicate end of test
        winkb_helper.press('WIN+D')

    ##
    # @brief        gets the list of active ports from the enumerated displays
    # @return       list of active ports' names
    def get_active_ports(self):
        active_ports = []
        for display_index in range(self.enumerated_displays.Count):
            if self.enumerated_displays.ConnectedDisplays[display_index].IsActive is True:
                active_ports.append(CONNECTOR_PORT_TYPE(
                    self.enumerated_displays.ConnectedDisplays[display_index].ConnectorNPortType).name)

        return active_ports

    ##
    # @brief        for the target display, reads the edid and extracts range limits
    # @param[in]    target_id
    # @return       object of type DisplayRangeLimits, containing range limits data
    def get_display_range_limits(self, target_id):

        range_limits = DisplayRangeLimits()
        edid_flag, edid_data, _ = driver_escape.get_edid_data(target_id)
        if not edid_flag:
            logging.error(f"Failed to get EDID data for target_id : {target_id}")
            self.fail()

        range_limits.ContFreqSup = edid_data[24] & 0x1
        if (range_limits.ContFreqSup):
            index = 54  # start of 1st 18 byte descriptor
            while index < 126:
                if (edid_data[index + 3] == 0xFD):  # 0xFD is display range limits block
                    range_limits.RR_min = edid_data[index + 5]
                    range_limits.RR_max = edid_data[index + 6]
                    break
                index += 18

        # WA: As eDP VRR panels are not coming with required EDID fields set, need this WA.
        # if RR_min or RR_max are 0, get values from DTD modelist. Consider only DTD modes (these will have MDS scaling)
        if range_limits.RR_min == 0 or range_limits.RR_max == 0:
            min_val = 1000
            max_val = 0
            supported_modes = self.config.get_all_supported_modes([target_id])
            for key, values in supported_modes.items():
                for mode in values:
                    if Scaling(mode.scaling).name == 'MDS':
                        logging.debug("For display with target_id %d, DTD mode found. %d x %d @%d Hz" % (
                            target_id, mode.HzRes, mode.VtRes, mode.refreshRate))
                        min_val = min([min_val, mode.refreshRate])
                        max_val = max([max_val, mode.refreshRate])
            range_limits.RR_min = min_val
            range_limits.RR_max = max_val

        return range_limits

    ##
    # @brief       out of the list of ports passed, finds the ports that supports VRR
    # @param[in]   port_list
    # @return      dict containing (port: transcoder) tuples that support VRR
    def get_vrr_capable_displays(self, port_list):

        vrr_disps = {}
        for port in port_list:
            if 'DP' not in port:
                continue

            # get target id from port
            target_id = self.config.get_target_id(port, self.enumerated_displays)

            # get respective transcoder based on port
            if port == 'DP_A':
                trans = 'EDP'
            else:
                display_base_obj = DisplayBase(port)
                trans, pipe = display_base_obj.get_transcoder_and_pipe(port)
                trans = chr(int(trans) + 64)

            # from edid, get display range limits
            range_limits = self.get_display_range_limits(target_id)

            # get MSA_timing_par_ignored from DPCD (offset 00007h: bit 6)
            dpcd_flag, dpcd_value = driver_escape.read_dpcd(target_id, 0x00007)
            if dpcd_flag is False:
                logging.error(f"Failed to read DPCD for target_id ({target_id}) at offset ({0x00007})")
            msa_timing_par_ignored = (dpcd_value[0] & 0x40) >> 6

            # If satisfies required conditions, add (port: transcoder) to vrr_disps dictionary
            if trans != 'EDP':
                if (msa_timing_par_ignored and range_limits.ContFreqSup and (range_limits.RR_min != 0) and (
                        range_limits.RR_max != 0)):
                    vrr_disps[port] = trans
            # WA: As eDP VRR panels are not coming with required EDID fields set, need this WA.
            # For eDP, even if ContFreqSup is not set, consider it as VRR panel. msa_timing_par_ignored set to 1 is enough.
            else:
                if (msa_timing_par_ignored and (range_limits.RR_min != 0) and (range_limits.RR_max != 0)):
                    vrr_disps[port] = trans
        # end of for

        return vrr_disps

    ##
    # @brief        Verifies all VRR register programming for the display supplied
    # @param[in]    disp is a tuple of (port: transcoder)
    # @return       None
    def verify_vrr_registers(self, disp):

        port = disp[0]
        trans = disp[1]
        target_id = self.config.get_target_id(port, self.enumerated_displays)

        ##
        # calculate Vmin and Vmax
        cur_mode = self.config.get_current_mode(target_id)
        range_limits = self.get_display_range_limits(target_id)
        logging.info("For %s, RR_min= %d, RR_max= %d" % (port, range_limits.RR_min, range_limits.RR_max))
        trans_htotal = MMIORegister.read("TRANS_HTOTAL_REGISTER", "TRANS_HTOTAL_" + trans, 'glk')
        trans_vtotal = MMIORegister.read("TRANS_VTOTAL_REGISTER", "TRANS_VTOTAL_" + trans, 'glk')
        Vmin = trans_vtotal.vertical_total - 1
        Vmax = (cur_mode.pixelClock_Hz / ((trans_htotal.horizontal_total + 1) * range_limits.RR_min * 1.0)) - 1
        Vmax = int(math.floor(Vmax))

        ##
        # verify vrr registers - VRR_CTL, VRR_MAX, VRR_MIN, VRR master flip bit
        trans_vrr_ctl = MMIORegister.read("TRANS_VRR_CTL_REGISTER", "TRANS_VRR_CTL_" + trans, self.platform)
        if (trans_vrr_ctl.vrr_enable == TRANS_VRR_CTL_REGISTER.vrr_enable_ENABLE):
            logging.info('PASS: TRANS_VRR_CTL_%s: VRR enable bit, Expected= "set", Actual= "set"' % (trans))
        else:
            logging.error(
                '[Driver Issue]: FAIL, TRANS_VRR_CTL_%s: VRR enable bit, Expected= "set", Actual= "not set"' % (trans))

        trans_vrr_vmin = MMIORegister.read("TRANS_VRR_VMIN_REGISTER", "TRANS_VRR_VMIN_" + trans, self.platform)
        if (trans_vrr_vmin.vrr_vmin == Vmin):
            logging.info('PASS: TRANS_VRR_VMIN_%s: Vmin is programmed correct. Expected= %d, Actual= %d' % (
                trans, Vmin, trans_vrr_vmin.vrr_vmin))
        else:
            logging.error(
                '[Driver Issue]: FAIL, TRANS_VRR_VMIN_%s: Vmin is programmed wrong. Expected= %d, Actual= %d' % (
                    trans, Vmin, trans_vrr_vmin.vrr_vmin))

        trans_vrr_vmax = MMIORegister.read("TRANS_VRR_VMAX_REGISTER", "TRANS_VRR_VMAX_" + trans, self.platform)
        if (trans_vrr_vmax.vrr_vmax == Vmax):
            logging.info('PASS: TRANS_VRR_VMAX_%s: Vmax is programmed correct. Expected= %d, Actual= %d' % (
                trans, Vmax, trans_vrr_vmax.vrr_vmax))
        else:
            logging.error(
                '[Driver Issue]: FAIL, TRANS_VRR_VMAX_%s: Vmax is programmed wrong. Expected= %d, Actual= %d' % (
                    trans, Vmax, trans_vrr_vmax.vrr_vmax))

        display_base_obj = DisplayBase(port)
        trans_temp, pipe = display_base_obj.get_transcoder_and_pipe(port)
        pipe = chr(int(pipe) + 65)
        plane_surf_1 = MMIORegister.read("PLANE_SURF_REGISTER", "PLANE_SURF_1_" + pipe, self.platform)
        logging.info('PLANE_SURF_1_%s: VRR master flip= %d' % (pipe, plane_surf_1.vrr_master_flip))

    ##
    # @brief     Gets the VRR state from VRR live status bit, for the supplied display
    # @param[in] disp is a tuple of (port: transcoder)
    # @return    bool. True if VRR is enabled on disp, False otherwise
    def is_vrr_enabled(self, disp):

        # read VRR status and return True/False
        trans = disp[1]
        trans_vrr_status = MMIORegister.read("TRANS_VRR_STATUS_REGISTER", "TRANS_VRR_STATUS_" + trans, self.platform)
        if (trans_vrr_status.vrr_enable_live == TRANS_VRR_CTL_REGISTER.vrr_enable_live_ENABLED):
            return True
        else:
            return False


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
