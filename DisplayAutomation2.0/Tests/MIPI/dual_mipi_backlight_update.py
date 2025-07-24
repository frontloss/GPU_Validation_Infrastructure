######################################################################################
# @file         dual_mipi_backlight_update.py
# @brief        This test changes screen brightness & verifies if both the panel PWMs received this update
# @details      Current policy is to update both panel PWMs with single brightness control.
#               This behavior might change in the future, if OS supports dual brightness control.
#               CommandLine: python dual_mipi_backlight_update.py -mipi_a
#               Test will pass only if duty cycle values of both panels' PWMs are updating and matching with each
#               brightness update.
# @author       Sri Sumanth Geesala
######################################################################################
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.MIPI.mipi_base import *
from registers.mmioregister import MMIORegister


##
# @brief        This class contains test to verify if both the panel PWM's receive the brightness change update
class DualMipiBacklightUpdate(MipiBase):
    ##
    # @brief        This function verifies if both the panel PWM's receive the brightness change update after
    #               screen brightness change.
    # @return       None
    def runTest(self):
        if (self.mipi_helper.dual_LFP_MIPI != 1):
            self.fail(
                "Test is applicable only for dual LFP MIPI. Current configuration is Single LFP MIPI. Aborting test.")

        ##
        # 1. Read current PWM duty cycle value of both panels' PWMs
        reg_sblc_pwm_duty_1 = MMIORegister.read("SBLC_PWM_DUTY_REGISTER", "SBLC_PWM_DUTY", self.platform)
        reg_sblc_pwm_duty_2 = MMIORegister.read("SBLC_PWM_DUTY_REGISTER", "SBLC_PWM_DUTY_2", self.platform)
        if (reg_sblc_pwm_duty_1.duty_cycle == reg_sblc_pwm_duty_2.duty_cycle):
            logging.info(
                'PASS: SBLC_PWM_DUTY_REGISTER: Initially, PWM duty_cycle of both panels are same. duty_cycle= %d' % (
                    reg_sblc_pwm_duty_1.duty_cycle))
        else:
            logging.error(
                'FAIL: SBLC_PWM_DUTY_REGISTER: Initially, PWM duty_cycle of both panels are mismatching. '
                'duty_cycle_1= %d, duty_cycle_2= %d' % (
                    reg_sblc_pwm_duty_1.duty_cycle, reg_sblc_pwm_duty_2.duty_cycle))
            self.fail_count += 1

        first_time = True
        prev_pwm_duty_cycle = ""
        for iterate in range(3):
            for i in range(10):
                brightness_level = (i * 10)

                ##
                # 2. Change screen brightness value through OS control
                logging.info('Setting the screen brightness level percent to %d' % (brightness_level))
                ret = self.mipi_helper.set_lfp_brightness(brightness_level)
                self.assertEquals(ret, True, 'Setting screen brightness failed')

                ##
                # 3. Check if both PWM duty cycle values are updated and are the same.
                reg_sblc_pwm_duty_1 = MMIORegister.read("SBLC_PWM_DUTY_REGISTER", "SBLC_PWM_DUTY", self.platform)
                reg_sblc_pwm_duty_2 = MMIORegister.read("SBLC_PWM_DUTY_REGISTER", "SBLC_PWM_DUTY_2", self.platform)

                if brightness_level == 0:
                    if (reg_sblc_pwm_duty_1.duty_cycle == 0 or reg_sblc_pwm_duty_2.duty_cycle == 0):
                        logging.error(
                            'FAIL: PWM duty_cycle cannot be 0 when brightness level percent set to 0. '
                            'duty_cycle_1= %d, duty_cycle_2= %d' % (
                                reg_sblc_pwm_duty_1.duty_cycle, reg_sblc_pwm_duty_2.duty_cycle))
                        self.fail_count += 1
                    else:
                        logging.info('PASS: PWM duty_cycle not 0 when brightness level % set to 0')

                if (first_time is False):
                    if ((reg_sblc_pwm_duty_1.duty_cycle != prev_pwm_duty_cycle) and (
                            reg_sblc_pwm_duty_1.duty_cycle == reg_sblc_pwm_duty_2.duty_cycle)):
                        logging.info(
                            'PASS: SBLC_PWM_DUTY_REGISTER: PWM duty_cycle got updated and value of both panels '
                            'are same. duty_cycle= %d' % (
                                reg_sblc_pwm_duty_1.duty_cycle))
                    else:
                        logging.error(
                            'FAIL: SBLC_PWM_DUTY_REGISTER: PWM duty_cycle did not update or value of both panels are '
                            'mismatching. prev_pwm_duty_cycle= %d, duty_cycle_1= %d, duty_cycle_2= %d' % (
                                prev_pwm_duty_cycle, reg_sblc_pwm_duty_1.duty_cycle, reg_sblc_pwm_duty_2.duty_cycle))
                        self.fail_count += 1
                else:
                    # skipping 1st time since, it is possible the initial brightness before modifying is exactly
                    # equal to this value
                    logging.info('Skipping duty cycle check for 1st iteration')

                prev_pwm_duty_cycle = reg_sblc_pwm_duty_1.duty_cycle
                first_time = False

        ##
        # report test failure if fail_count>0
        if (self.fail_count + self.mipi_helper.verify_fail_count) > 0:
            self.fail(f'Some checks in the test have failed. Check error logs. '
                      f'No. of failures= {(self.fail_count + self.mipi_helper.verify_fail_count)}')

if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
