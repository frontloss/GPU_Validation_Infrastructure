########################################################################################################################
# @file          virtual_display_crt.py
# @brief         Virtual Display verification with "VirtualCRTSupport" Registry is covered in below scenarios:
#                * Virtual Display verification in headless mode
#                * Virtual Display verification post hot-plug/unplug of external display
#                * Virtual Display verification post driver disable-enable with registry
# @author        Prateek Joshi
########################################################################################################################
import ctypes
import logging
import sys
import unittest

from Libs.Core import display_essential
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.wrapper import control_api_wrapper, control_api_args
from Tests.VirtualDisplay.Yangra import virtual_display_yangra_base as yangra_base


##
# @brief  It contains methods to enable virtual display with registry key VirtualCRTSupport
class VirtualCRTSupport(yangra_base.VirtualDisplayYangraBase):

    ##
    # @brief        Unittest runTest function
    # @param[in]    self; Object of virtual display yangra base class
    # @return       void
    def runTest(self):
        # Debug purpose
        self.log_enumerated_status()

        # Enable CRTSupport
        logging.info('Step_1: Enable VirtualCRTSupport registry'.center(yangra_base.LINE_WIDTH, '-'))
        self.assertEqual(self.enable_disable_virtualcrtsupport(True), True, 'Failed to enable CRTSupport')
        logging.info('Enabled CRTSupport')

        logging.info('Step_2: Unplug External Display'.center(yangra_base.LINE_WIDTH, '-'))
        for display in self.connected_list:
            if yangra_base.display_utility.unplug(display) is False:
                self.fail("Failed to unplug display {}".format(display))
            self.plugged_display.remove(display)
            logging.info('Successfully unplugged the display {}'.format(display))

        self.log_enumerated_status()

        # Verify virtual display
        logging.info('Step_3: Verify Headless System'.center(yangra_base.LINE_WIDTH, '-'))
        self.assertEqual(self.verify_headless_virtual_display(), True, 'Failed to verify virtual display')
        logging.info('Successfully verified virtual display is enumerated')

        # ToDo: Need to fix the issue here with CLIB
        ''' 
        # Control Library Display Properties Verification
        targetid = self.display_config.get_target_id(self.connected_list[0], self.enumerated_displays)
        displayEncoderProperties = control_api_args.ctl_adapter_display_encoder_properties_t()
        displayEncoderProperties.Size = ctypes.sizeof(displayEncoderProperties)

        logging.info("Step_4: IGCL Display Type Verification")
        if control_api_wrapper.get_display_encoder_properties(displayEncoderProperties, targetid):
            if targetid == displayEncoderProperties.Os_display_encoder_handle.WindowsDisplayEncoderID:
                logging.info("Display Target_ID {} verified"
                             .format(displayEncoderProperties.Os_display_encoder_handle.WindowsDisplayEncoderID))
                logging.info("Encoder_Config_Flags {}".format(displayEncoderProperties.EncoderConfigFlags))
                if control_api_args.ctl_encoder_config_flags_v.VIRTUAL_DISPLAY.value and \
                        displayEncoderProperties.EncoderConfigFlags:
                    logging.info("Virtual Display Enabled {}".format(
                        control_api_args.ctl_encoder_config_flags_v.VIRTUAL_DISPLAY.value and
                        displayEncoderProperties.EncoderConfigFlags))
                    logging.info("Pass: IGCL Virtual Display Type Verified")
                else:
                    logging.error("Virtual Display Config Flag is not reported from IGCL {}".format(
                        control_api_args.ctl_encoder_config_flags_v.VIRTUAL_DISPLAY.value and
                        displayEncoderProperties.EncoderConfigFlags))
        '''

        logging.info('Step_5: Verify Virtual Display'.center(yangra_base.LINE_WIDTH, '-'))
        self.assertEqual(self.verify_virtual_display(), True, 'Failed to verify virtual display')
        logging.info('Successfully verified virtual display is enumerated')

        # Restart display driver to make the registry changes
        logging.info('Step_6: Restart Display Driver'.center(yangra_base.LINE_WIDTH, '-'))
        status, reboot_required = display_essential.restart_gfx_driver()
        if status is False:
            self.fail('Failed to restart driver after writing into registry')
        logging.debug('Display driver restarted successfully')

        # Verify virtual display
        logging.info('Step_7: Verify Headless System post Driver Restart'.center(yangra_base.LINE_WIDTH, '-'))
        self.assertEqual(self.verify_headless_virtual_display(), True, 'Failed to verify virtual display')
        logging.info('Successfully verified virtual display is enumerated')

        logging.info('Step_8: Plug External Display'.center(yangra_base.LINE_WIDTH, '-'))
        for display in self.connected_list:
            if yangra_base.display_utility.plug(display) is False:
                self.fail("Failed to plug display {}".format(display))
            self.plugged_display.append(display)
            logging.info('Successfully plugged the display {}'.format(display))

        self.log_enumerated_status()

        # Verify virtual display
        logging.info('Step_9: Verify Virtual Display'.center(yangra_base.LINE_WIDTH, '-'))
        self.assertEqual(self.verify_virtual_display(), True, 'Failed to verify virtual display')
        logging.info('Successfully verified virtual display is enumerated')


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
