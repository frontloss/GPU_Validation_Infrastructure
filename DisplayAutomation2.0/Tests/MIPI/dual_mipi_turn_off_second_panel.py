########################################################################################################################
# @file         dual_mipi_turn_off_second_panel.py
# @brief        This Test applies SD mipi panel1 & then verifies if MIPI port and backlight of
#               second panel are disabled. Repeats same for other panel.
#
# @details      CommandLine: python dual_mipi_turn_off_second_panel.py -mipi_a
#               Test will pass only if MIPI port and backlight of turned off panel are disabled.
# @author       Sri Sumanth Geesala
########################################################################################################################
import importlib

from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.MIPI.mipi_base import *
from registers.mmioregister import MMIORegister


##
# @brief        This class contains test to verify MIPI port and backlight of second panel by turning off the other
class DualMipiTurnOffSecondPanel(MipiBase):

    ##
    # @brief        This function verifies by applying SD mipi panel1 & then verifies if MIPI port and backlight of
    #               second panel are disabled. Repeats same for other panel.
    # @return       None
    def runTest(self):

        if (self.mipi_helper.dual_LFP_MIPI != 1):
            self.fail(
                "Test is applicable only for dual LFP MIPI. Current configuration is Single LFP MIPI. Aborting test.")

        ##
        # 1. Apply SD MIPI panel1
        logging.info('Applying SD %s' % (self.mipi_master_port))
        result = self.config.set_display_configuration_ex(enum.SINGLE, [self.mipi_master_port],
                                                          self.enumerated_displays)
        self.assertNotEquals(result, False,
                             "Aborting the test as applying SD %s display config failed." % (self.mipi_master_port))

        ##
        # 2. Verify whether port and backlight of panel2 are disabled
        self.verify_trans_and_backlight_disable(self.mipi_second_display)

        ##
        # 3. Apply SD MIPI panel2
        logging.info('Applying SD %s' % (self.mipi_second_display))
        result = self.config.set_display_configuration_ex(enum.SINGLE, [self.mipi_second_display],
                                                          self.enumerated_displays)
        self.assertNotEquals(result, False,
                             "Aborting the test as applying SD %s display config failed." % (self.mipi_second_display))

        ##
        # 4. Verify whether port and backlight of panel1 are disabled
        self.verify_trans_and_backlight_disable(self.mipi_master_port)

        ##
        # report test failure if fail_count>0
        if self.fail_count > 0:
            self.fail("Some checks in the test have failed. Check error logs. No. of failures= %d" % self.fail_count)

    ##
    # @brief        This function is used to verify transcoder and backlight disabling
    # @param[in]    mipi_port name of the mipi-port
    # @return       None
    def verify_trans_and_backlight_disable(self, mipi_port):
        reg_suffix = ['', '_2']
        if (mipi_port == 'MIPI_A'):
            index = 0
        else:
            index = 1
        port = self.port_list[index]

        # verify transcoder enable, and transcoder status
        trans_conf = importlib.import_module("registers.%s.TRANS_CONF_REGISTER" % (self.platform))
        reg_trans_conf = MMIORegister.read("TRANS_CONF_REGISTER", "TRANS_CONF" + port, self.platform)
        if ((reg_trans_conf.transcoder_enable == getattr(trans_conf, "transcoder_enable_DISABLE")) and (
                reg_trans_conf.transcoder_state == getattr(trans_conf, "transcoder_state_DISABLED"))):
            logging.info(
                'PASS: TRANS_CONF%s - Expected: transcoder to be disabled \t Actual: transcoder_enable= %d, '
                'transcoder state= %d' % (
                    port, reg_trans_conf.transcoder_enable, reg_trans_conf.transcoder_state))
        else:
            logging.error(
                'FAIL: TRANS_CONF%s - Expected: transcoder to be disabled \t Actual: transcoder_enable= %d, '
                'transcoder state= %d' % (
                    port, reg_trans_conf.transcoder_enable, reg_trans_conf.transcoder_state))
            self.fail_count += 1

        # verify panel power backlight enable, and panel power on status.
        # Expect backlight enable to be set to disable
        pp_control = importlib.import_module("registers.%s.PP_CONTROL_REGISTER" % (self.platform))
        pp_status = importlib.import_module("registers.%s.PP_STATUS_REGISTER" % (self.platform))

        reg_pp_control = MMIORegister.read("PP_CONTROL_REGISTER", "PP_CONTROL" + reg_suffix[index], self.platform)
        reg_pp_status = MMIORegister.read("PP_STATUS_REGISTER", "PP_STATUS" + reg_suffix[index], self.platform)
        self.mipi_helper.verify_and_log_helper(register='PP_CONTROL' + port, field='backlight_enable',
                                          expected=getattr(pp_control, "backlight_enable_DISABLE"),
                                          actual=reg_pp_control.backlight_enable)

        # and panel_power_on_status to be set to disable
        self.mipi_helper.verify_and_log_helper(register='PP_STATUS' + port, field='panel_power_on_status',
                                          expected=getattr(pp_status, "panel_power_on_status_OFF"),
                                          actual=reg_pp_status.panel_power_on_status)

        # verify PWM enable
        sblc_pwm_ctl1 = importlib.import_module("registers.%s.SBLC_PWM_CTL1_REGISTER" % (self.platform))
        reg_sblc_pwm_ctl1 = MMIORegister.read("SBLC_PWM_CTL1_REGISTER", "SBLC_PWM_CTL1" + reg_suffix[index],
                                              self.platform)
        self.mipi_helper.verify_and_log_helper(register='SBLC_PWM_CTL1' + port, field='pwm_pch_enable',
                                          expected=getattr(sblc_pwm_ctl1, "pwm_pch_enable_DISABLE"),
                                          actual=reg_sblc_pwm_ctl1.pwm_pch_enable)

        ##
        # report test failure if fail_count>0
        if (self.fail_count + self.mipi_helper.verify_fail_count) > 0:
            self.fail(f'Some checks in the test have failed. Check error logs. '
                      f'No. of failures= {(self.fail_count + self.mipi_helper.verify_fail_count)}')

if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
