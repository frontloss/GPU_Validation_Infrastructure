##
# @file         detachable_LFP_plug_unplug.py
# @brief        This feature supports Plug and Unplug of LFP_2 panels but not LFP_1.
# @details      cmd_line: test_display_python_automation
#               Tests\LFP_Common\Detachable_LFP\detachable_LFP_plug_unplug.py
#               -edp_A SINK_EDP012 VBT_INDEX_0 -MIPI_C SINK_MIP002 VBT_INDEX_1 -detach_lfp mipi_c -repeat 5
# @author       Goutham N
from Tests.LFP_Common.Detachable_LFP.detachable_LFP_base import *


##
# @brief        This class is for stress testing plug and unplug of
#               LFP_2 panel that inherits DetachableLFPBase for setup and _setHPD functionality.
class DetachableLFPPlugUnplug(DetachableLFPBase):
    ##
    # @brief        Test case to test the plug and unplug of LFP_2 panel.
    # @return       None
    def runTest(self) -> None:
        for i in range(0, self.iterations):
            logging.info("Iteration: " + str(i))
            for plug in self.plug:
                enumerated_displays = DisplayConfiguration().get_enumerated_display_info()
                is_display_attached = display_config.is_display_attached(enumerated_displays, self.port_to_detach)

                if plug is not None:
                    ##
                    # if user wants to plug but display is already plugged in that port.
                    if plug:
                        if is_display_attached is True:
                            # EDP 2 will be plugged initially. it gets enabled via regKey.
                            logging.info(
                                f'Unable to perform plug since display is already plugged in {self.port_to_detach}')
                            continue
                    ##
                    # if user wants to unplug but nothing is plugged to perform unplug.
                    else:
                        if is_display_attached is False:
                            logging.info(f'Unable to perform unplug since nothing is plugged in {self.port_to_detach}')
                            continue
                else:
                    self.fail(f'plug is set to NONE, Hence aborting test..')

                #   plug/unplug LFP_2 panel
                plug_status = "plug" if plug is True else "unplug"

                # Restart the ETL.
                # Aim is to have exactly 1 unplug and 1 plug in the ETL
                # Which will be later used for PPS verifications.
                # Note: We have restricted the iteration to 2.
                # In those 2, we will have a lot of unwanted events due to EDP being plugged from the beginning.
                if plug is False:
                    logging.debug("Restarting the ETL Trace before doing first unplug")
                    if etl_tracer.stop_etl_tracer() is False:
                        self.fail("[Test Issue] Failed to stop default ETL Tracer")
                    if etl_tracer.start_etl_tracer() is False:
                        self.fail("Failed to start ETL Tracer")

                logging.info("Hot " + plug_status + "ging LFP...")
                set_hpd = self._setHPD(self.mapped_port_to_detach, plug, self.port_type, self.gfx_index)

                # Delay
                status = self._dynamic_delay(self.port_to_detach, plug)
                if plug == True and status == False and self.mapped_port_to_detach != 'DP_A':
                    self.assertTrue(status,
                                    f"[Test Issue] - Timeout reached! Display is not enumerated on port "
                                    f"{self.port_to_detach}")
                elif plug == False and status == False and self.mapped_port_to_detach != 'DP_A':
                    # Delay
                    status = self._dynamic_delay(self.port_to_detach, plug=False)
                    self.assertTrue(status,
                                    f"[Test Issue] - Timeout reached! Display is still enumerated on port "
                                    f"{self.port_to_detach}")

                # Retrieving enumerated displays
                enumerated_displays = DisplayConfiguration().get_enumerated_display_info()
                # printing enumerated displays info
                logging.debug('Enumerated display information: {}'.format(enumerated_displays.to_string()))
                # Checking if display is attached/detached
                is_display_attached = display_config.is_display_attached(enumerated_displays, self.port_to_detach)

                # checking if panel(s) are enumerated as per expectation after _setHPD().
                if set_hpd:
                    # plug case
                    if plug:
                        # LFP_1 case - Negative Scenario
                        if (
                                self.port_to_detach == 'EDP_A' or self.port_to_detach == 'DP_A') and is_display_attached is False:
                            logging.info('PASS: Since this feature is intended to ' + plug_status +
                                         ' LFP_2 panel not LFP_1, '
                                         'hence LFP_1 is not enumerated after HPD-plug call on port={}'.format(
                                             self.port_to_detach))

                        elif (
                                self.port_to_detach == 'EDP_A' or self.port_to_detach == 'DP_A') and is_display_attached is True:
                            self.fail(
                                'FAIL: HPD-' + plug_status +
                                ' called on port={} and LFP_1 is enumerated ideally it shouldn\'t, '
                                'since this feature is intended to plug LFP_2 panel not LFP_1'.format(
                                    self.port_to_detach))
                        # LFP_2 case - Positive Scenario
                        else:
                            if is_display_attached is False:
                                gdhm.report_test_bug_di(
                                    '[DETACHABLE_LFP] LFP_2 is not attached after issuing SetHPD as True')
                                self.fail(
                                    f"FAIL: plug issued but display didn't enumerate on port: {self.port_to_detach}")

                            logging.info(f"PASS: plug issued and display got enumerated on port: {self.port_to_detach}")

                            # blc verifications and pps verification are restricted to detachable_EDP only.
                            # TODO: Need to analyze and add for MIPI later if needed.
                            if self.edp_as_companion_display:
                                status &= self.verify_blc_after_attach()
                                self.assertTrue(status, f" BLC Verifications after attach of LFP_2 has failed!")
                                logging.info('BLC verification is completed for detachable LFP.')

                                status &= self.verify_pps_basic()
                                self.assertTrue(status, f" PPS verifications after attach of LFP_2 has failed!")
                                logging.info('PPS verification is completed for detachable LFP')

                    # unplug case
                    else:
                        # LFP_1 case - Negative Scenario
                        if (
                                self.port_to_detach == 'EDP_A' or self.port_to_detach == 'DP_A') and is_display_attached is True:
                            logging.info(
                                'PASS: Since this feature is intended to ' + plug_status +
                                ' LFP_2 panel not LFP_1, '
                                'hence LFP_1 is enumerated even after HPD-unplug call on port={}'.format(
                                    self.port_to_detach))
                        elif (
                                self.port_to_detach == 'EDP_A' or self.port_to_detach == 'DP_A') and is_display_attached is False:
                            self.fail('FAIL: HPD-' + plug_status + ' called on port={} and EDP is unplugged'.format(
                                self.port_to_detach))
                        # LFP_2 case - Positive Scenario
                        else:
                            if is_display_attached:
                                gdhm.report_driver_bug_di(
                                    '[DETACHABLE_LFP] Unable to detach LFP_2 after issuing SetHPD as False')
                                self.assertFalse(is_display_attached,
                                                 f"FAIL: Unplug issued but display got enumerated on port {self.port_to_detach}")
                            logging.info(
                                f"PASS: Unplug issued and display didn't enumerate on port {self.port_to_detach}")

                # _setHPD() fail case
                else:
                    # LFP_1 Case
                    if self.port_to_detach == 'EDP_A' or self.port_to_detach == 'DP_A':
                        logging.info("HPD-" + plug_status + " failed for {}".format(self.port_to_detach))
                        logging.info(
                            "PASS: Since this feature is intended to unplug LFP_2, hence HPD " + plug_status +
                            " failed for {}".format(self.port_to_detach))
                    # LFP_2 Case
                    else:
                        self.fail("HPD-" + plug_status + " failed for {}".format(self.port_to_detach))


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('DetachableLFPPlugUnplug'))
    TestEnvironment.cleanup(outcome)
