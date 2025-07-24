########################################################################################################################
# @file         vdd_display_config.py
# @brief        Test to verify eDP panel is powered off when inactive
#
# @author       Akshaya Nair
########################################################################################################################

from Tests.EDP.VDD.vdd_base import *


##
# @brief        Contains tests to check VDD off when eDP panel if inactive.
class VDDDisplayConfig(VDDBase):
    ##
    # @brief This step sets single display config and checks VDD off for eDP + external panel scenario
    # @return None
    # @cond
    @common.configure_test(selective=["DISPLAY_CONFIG"])
    # @endcond
    def t_01_lfp_efp(self):
        if self.__class__.display_config_.set_display_configuration_ex(enum.SINGLE, [self.external_panels[0]]) is False:
            self.fail(f"FAIL: Failed to apply display config")
        logging.info(f"PASS: Successfully applied Single Display on port {self.external_panels[0]}")

        if self.display_power_.is_power_state_supported(display_power.PowerEvent.CS):
            power_event = display_power.PowerEvent.CS
        else:
            power_event = display_power.PowerEvent.S3

        # Start new ETL
        if etl_tracer.start_etl_tracer() is False:
            self.fail("FAIL: Failed to start new ETL tracer (Test Issue)")
        logging.info("PASS: Started new ETL Tracer")

        if self.display_power_.invoke_power_event(power_event, common.POWER_EVENT_DURATION_DEFAULT) is False:
            self.fail('Fail: Failed to invoke power event %s' % power_event.name)
        status, etl_file_path = stop_existing_etl("GfxTrace_after_powerevent")
        if not status:
            self.fail("FAIL: Failed to stop ETL tracer")

        vdd_status = verify_vdd_status(etl_file_path,port = "PORT_A")

        if not vdd_status:
            gdhm.report_driver_bug_di(f"{GDHM_VDD} VDD not turned for LFP")
            self.fail("FAIL: VDD not turned off for eDP")
        logging.info("PASS: VDD turned off for eDP")

    ##
    # @brief This step sets single display config and checks VDD off for LFP2 in dual LFP scenario
    # @return None
    # @cond
    @common.configure_test(selective=["DUAL_LFP"])
    # @endcond
    def t_02_dual_lfp(self):
        if reboot_helper.is_reboot_scenario() is True:
            logging.info("System rebooted successfully")
            # Verfying VDD off on LFP2 after rebooting with single display config set on LFP1
            status, new_boot_etl_file = stop_existing_etl("GfxBootTrace_dual_lfp")

            if verify_vdd_status(new_boot_etl_file, port = "PORT_B") is False:
                gdhm.report_driver_bug_di(f"{GDHM_VDD} VDD not turned for LFP2 after reboot ")
                self.fail("FAIL: Failed to verify VDD Status after reboot")

            logging.info("PASS: Successfully verified VDD Status after reboot")
        else:
            logging.info("Setting Single Display on LFP1")
            enumerated_display = self.__class__.display_config_.get_enumerated_display_info()
            for index in range(0, enumerated_display.Count):
                disp = CONNECTOR_PORT_TYPE(enumerated_display.ConnectedDisplays[index].ConnectorNPortType).name
                if disp != 'DP_B':
                    status = self.__class__.display_config_.set_display_configuration_ex(enum.SINGLE, [disp])
                    if not status:
                        self.fail(f"FAIL: Failed to apply display config")
                    logging.info(f"PASS: Successfully applied Single Display on port {disp}")

            if self.display_power_.is_power_state_supported(display_power.PowerEvent.CS):
                power_event = display_power.PowerEvent.CS
            else:
                power_event = display_power.PowerEvent.S3

            if etl_tracer.start_etl_tracer() is False:
                self.fail("FAIL: Failed to start new ETL tracer (Test Issue)")
            logging.info("PASS: Started new ETL Tracer")

            if self.display_power_.invoke_power_event(power_event, common.POWER_EVENT_DURATION_DEFAULT) is False:
                logging.error('Failed to invoke power event %s' % power_event.name)
            status, etl_file_path = stop_existing_etl("GfxTrace_after_powerevent_dual_lfp")
            if not status:
                self.fail("FAIL: Failed to stop ETL tracer")

            vdd_status = verify_vdd_status(etl_file_path, port = "PORT_B")
            if not vdd_status:
                gdhm.report_driver_bug_di(f"{GDHM_VDD} VDD not turned for LFP2 ")
                self.fail("FAIL: VDD not turned off for LFP2")
            logging.info("PASS: VDD turned off for LFP2")

            # Verfying VDD off on LFP2 after rebooting with single display config set on LFP1
            if etl_tracer.start_etl_tracer() is False:
                self.fail("FAIL: Failed to start ETL Tracer")
            logging.info("Rebooting the system")
            if reboot_helper.reboot(self, 't_02_dual_lfp') is False:
                self.fail("FAIL: Failed to reboot the system")


if __name__ == '__main__':
    TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(VDDDisplayConfig))
    TestEnvironment.cleanup(test_result)
