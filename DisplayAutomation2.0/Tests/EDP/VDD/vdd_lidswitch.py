########################################################################################################################
# @file         vdd_lidswitch.py
# @brief        Semi auto test to verify eDP panel is powered off when lid switch is turned off
# Manual TI     https://gta.intel.com/procedures/#/procedures/TI-1061998
# TI name:      VDD_LID_Event
# @author       Akshaya Nair
########################################################################################################################

from Libs.manual.modules import alert
from Tests.EDP.VDD.vdd_base import *


##
# @brief        Contains tests to check if VDD is off when eDP panel is inactive.
class VDDLidSwitch(unittest.TestCase):
    display_pwr = display_power.DisplayPower()
    display_config = display_config.DisplayConfiguration()
    vdd_obj = VDDBase()

    ##
    # @brief This step sets single display config and checks VDD off for eDP
    # @return None
    def test_01_step(self):
        user_msg = "[Expectation]: Boot the system with planned eDP." \
                   "\n[CONFIRM]: Enter Yes if expectations met, else enter No"
        result = alert.confirm(user_msg)
        if not result:
            self.fail("FAIL: Test is not started with planned panel. Rerun the test with planned panel.")
        else:
            logging.info("PASS: Test started with planned eDP")

        user_msg = "Hotplug planned external display" \
                   "\n[CONFIRM]:Enter yes if display is plugged, else enter no"
        result = alert.confirm(user_msg)
        if not result:
            msg = alert.prompt('Please enter your observations', [{'name': 'Message'}])
            logging.error(f"User observations: {msg['Message']}")
            self.fail("FAIL: External panel hotplug")
        else:
            logging.info("PASS: Hot plugged external panel")

        # Applying clone config
        alert.info("Applying Clone config")
        logging.info("Applying Clone config")
        enumerated_display = self.vdd_obj.display_config_.get_enumerated_display_info()
        external_display = 'HDMI_F'
        for index in range(0, enumerated_display.Count):
            external_display = CONNECTOR_PORT_TYPE(enumerated_display.ConnectedDisplays[index].ConnectorNPortType).name
            if external_display != 'DP_A':
                status = self.vdd_obj.display_config_.set_display_configuration_ex(enum.CLONE,
                                                                                    ['DP_A', external_display],
                                                                                    enumerated_display)
                if not status:
                    alert.info(f"Applying Clone config failed")
                    self.fail(f"FAIL: Applying Clone config failed")
                alert.info(f"PASS: Successfully applied Clone Display")

        # verifying vdd off with lid switch off
        alert.info("Turn off Lid")
        logging.info("Setting lid switch off")
        user_msg = "[Expectation]: No display on eDP" \
                   "\n[CONFIRM]: Enter Yes if expectations met, else enter No"
        result = alert.confirm(user_msg)
        if not result:
            self.fail("FAIL: Lid switch off")
        else:
            logging.info("PASS: Lid switch off")
        alert.info("Invoking power event")
        if self.vdd_obj.display_power_.is_power_state_supported(display_power.PowerEvent.CS):
            power_event = display_power.PowerEvent.CS
        else:
            power_event = display_power.PowerEvent.S3
        logging.info(f"Invoking {power_event.name} and verifying vdd status")

        if etl_tracer.start_etl_tracer() is False:
            self.fail("FAIL: Failed to start new ETL tracer (Test Issue)")
        logging.info("PASS: Started new ETL Tracer")

        if self.vdd_obj.display_power_.invoke_power_event(power_event, common.POWER_EVENT_DURATION_DEFAULT) is False:
            self.fail('FAIL: Failed to invoke power event %s' % power_event.name)

        status, etl_file_path = stop_existing_etl("GfxTrace_vdd_status")
        if not status:
            self.fail("FAIL: Failed to stop ETL")

        vdd_status = verify_vdd_status(etl_file_path,port = "PORT_A")
        if not vdd_status:
            alert.info("VDD not turned off for eDP")
            self.fail("FAIL: VDD not turned off for eDP")
        else:
            logging.info("PASS: VDD turned off for eDP")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(
        reboot_helper.get_test_suite('VDDLidSwitch'))
    TestEnvironment.cleanup(outcome)
