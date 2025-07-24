##
# @file         detachable_LFP_base.py
# @brief        This acts as base class to detachable_display tests. It contains setUp and HPD function.
#               For any concurrency testing verify_detachable_LFP() method can be used.
# @author       Goutham N
import sys
import time
import unittest
import logging
import enum

from Libs.Core.display_config import display_config
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core import cmd_parser, enum
from Libs.Core.sw_sim.driver_interface import DriverInterface
from Libs.Core.test_env import test_context
from Libs.Core.display_power import DisplayPower
from Libs.Core import display_essential
from Libs.Core import registry_access
from Libs.Core import reboot_helper
from Libs.Core.vbt.vbt import Vbt
from Libs.Core.sw_sim import driver_interface
from Libs.Core.test_env.test_context import TestContext
from Libs.Core.logger import gdhm, etl_tracer
from Libs.Core.test_env.test_environment import TestEnvironment

from Libs.Feature.powercons import registry

from Tests.PowerCons.Modules import common
from Tests.PowerCons.Functional.BLC import blc
from Tests.EDP.PPS import pps_verification


##
# @brief        Base class for detachable_LFP Test cases.
#               Any class containing Detachable_LFP test cases can inherit this class to
#               to get the common setup and setHPD functionality.
#               For any concurrency testing verify_detachable_LFP() method can be used.
class DetachableLFPBase(unittest.TestCase):
    ##
    # @brief        Enum definition for operation.
    class Operation(enum.Enum):
        stress_test = 0
        plug = 1
        unplug = 2

    ##
    # @brief    Entry point for detachable_LFP test cases.
    #           Initializes some of the variable required for detachable_LFP test case execution.
    # @return   None
    @reboot_helper.__(reboot_helper.setup)
    def setUp(self) -> None:
        # Variable initialization
        self.gfx_index = None
        self.displays_in_cmdline = []
        self.port_type = 'NATIVE'
        self.my_custom_tags = ['-detach_LFP', '-power_state', '-repeat', '-plug']
        self.plug = [True, False]
        self.disp_power = DisplayPower()
        self.power_state = None
        self.iterations = 1
        self.reg_key = "LFP2HpdEnable"
        self.is_manual = False
        self.edp_as_companion_display = False
        self.plug_status = False
        # This is a flag variable which will be used to skip teardown in manual scenario.
        self.is_manual_scenario = False
        self.operation = 2
        self.pps_ver = pps_verification.PpsVerification()

        # Parse the cmdline data to get the display details for plugging.
        self.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, self.my_custom_tags)
        for key, value in self.cmd_line_param.items():
            if cmd_parser.display_key_pattern.match(key) is not None:
                if value['connector_port'] is not None:
                    self.displays_in_cmdline.append(value['connector_port'])
                if value['gfx_index'] is None:
                    self.gfx_index = 'gfx_0'
                else:
                    self.gfx_index = value['gfx_index'].lower()

            if key == 'DETACH_LFP':
                self.port_to_detach = value[0].upper()

            if key == 'POWER_STATE':
                self.power_state = value[0].lower()

            if key == 'REPEAT' and value[0].isnumeric():
                self.iterations = int(value[0])

        # With this we enable reg key, do port mapping and make sure companion display is initially unplugged.
        # In MIPI case LFP2 will be disabled when reg_key is enabled
        # whereas in EDP case LFP2 is enabled when reg_key is enabled.
        status = self.__initialize_detachable_LFP(self.port_to_detach,
                                                  port_type=self.port_type, gfx_index=self.gfx_index)
        if status:
            logging.info("Pass: Detachable_LFP initialization is successful.")
        else:
            self.fail("[Test Issue] : Failed to initialize Detachable_LFP.")

    ##
    # @brief        This method plugs/unplugs companion display on given port based on user input.
    # @param[in]    port: str
    #               Mapped port name Eg. DP_A, DP_B.
    # @param[in]    plug: bool
    #               True for plug and False for unplug.
    # @param[in]    port_type: str
    #               connector port type Eg. NATIVE.
    # @param[in]    gfx_index: str
    #               graphics index Eg. gfx_0, gfx_1.
    # @return       bool; Returns True if HPD is success otherwise false
    @staticmethod
    def _setHPD(port: str, plug: bool, port_type: str, gfx_index: str) -> bool:
        ##
        # attach when plug is true and detach when plug is false.
        res = False
        gfx_adapter_info = test_context.TestContext.get_gfx_adapter_details()[gfx_index]
        try:
            res = DriverInterface().trigger_interrupt(gfx_adapter_info, port, plug, port_type)
        except Exception as e:
            logging.info("Error Occurred in trigger_interrupt():- " + str(e))
        return res

    ##
    # @brief        In this method we enable reg_key, do port mapping and
    #               make sure initially companion display is unplugged.
    # @param[in]    port: str
    #               Mapped port name Eg. DP_A, DP_B.
    # @param[in]    plug: bool
    #               True for plug and False for unplug.
    # @param[in]    port_type: str
    #               connector port type Eg. NATIVE.
    # @param[in]    gfx_index: str
    #               graphics index Eg. gfx_0, gfx_1.
    # @return       bool; Returns True if HPD is success otherwise false
    def __initialize_detachable_LFP(self, port, port_type, gfx_index):
        # Enabling Reg Key
        status = self.__enable_reg_key(gfx_index, self.reg_key)
        if not status:
            self.fail('[Test Issue]: Failed to enable reg key - ' + self.reg_key)

        # Check if Port Mapping is already done. If done skip, otherwise map.
        if self.port_to_detach not in ['DP_A', 'DP_B']:
            status = self.__port_mapping(port)
            if not status:
                self.fail(f"[Test Issue]: Failed to map the port."
                          f" Currently this feature is not supported for port -  {port}")

        enumerated_displays = DisplayConfiguration().get_enumerated_display_info()
        status = display_config.is_display_attached(enumerated_displays, self.port_to_detach)
        if status and port != 'DP_A':
            self._setHPD(port, plug=False, port_type=port_type, gfx_index=gfx_index)
            # Delay using polling mechanism until companion display is unplugged
            is_display_detached = self._dynamic_delay(port, plug=False)
            if is_display_detached:
                return True
            else:
                return False
        return True

    ##
    # @brief        This method enables reg key required for detachable_LFP.
    # @param[in]    port: str
    #               port name
    # @param[in]    plug: bool
    # @return       bool; Returns True if reg key is enabled and driver is successfully restarted, otherwise False.
    def __enable_reg_key(self, gfx_index, reg_key):
        ret = registry.write(gfx_index, reg_key, registry_access.RegDataType.DWORD, 0x1)
        if ret is None:
            logging.info(reg_key + ' reg key already enabled.')
        elif ret is True:
            logging.info('Successfully enabled ' + reg_key + ' reg key')
            status, reboot_required = display_essential.restart_gfx_driver()
            if status is True:
                logging.info('Successfully Disabled and Enabled Driver')
            else:
                self.fail('[Driver Issue]: Failed to Disable and Enable Driver')
        else:
            return False
        return True

    ##
    # @brief        This method is for port mapping.
    #               This is done because trigger_hpd() function can not be called directly on EDP_A, EDP_B or MIPI_C.
    #               Internally EDP_A is mapped to DP_A, EDP_B and MIPI_C to DP_B.
    # @param[in]    port_to_detach: str
    #               port to detach
    # @return       bool; Returns True on successful port mapping otherwise False.
    def __port_mapping(self, port_to_detach: str) -> bool:
        # Negative testcase.
        if port_to_detach != 'DP_A' and port_to_detach == 'EDP_A':
            # This is done because eDP panel will be enabled in DP_A port.
            self.port_to_detach = 'DP_A'
            self.mapped_port_to_detach = 'DP_A'

        # Positive testcase
        # Mapping MIPI_C to DP_B. Currently trigger_hpd() works only on DP_B.
        # In future we can directly call HPD for MIPI_C.
        elif port_to_detach != 'DP_B' and port_to_detach == 'MIPI_C':
            self.mapped_port_to_detach = 'DP_B'
        elif port_to_detach != 'DP_B' and port_to_detach == 'EDP_B':
            # This is done because for eDP case, power event S5's expected behavior is different than MIPI.
            # In EDP case LFP2 will be enabled after waking from S5
            # whereas in MIPI case LFP2 will be disabled after waking from S5.
            self.edp_as_companion_display = True
            # This is done because eDP_B panel will be enabled in DP_B port.
            self.port_to_detach = 'DP_B'
            self.mapped_port_to_detach = 'DP_B'
        else:
            return False

        return True

    ##
    # @brief        In this method Delay is added using Polling mechanism for plug and unplug scenario.
    #               Max time limit - 10 sec
    # @param[in]    port: str
    #               port to attach/detach
    # @param[in]    plug: bool
    #               Plug status
    # @return       bool; Returns True if one of the below condition is True, otherwise False
    #               Condition 1 : Display is plugged and it is enumerated within 10 seconds.
    #               Condition 2 : Display is unplugged and it is detached within 10 seconds
    @staticmethod
    def _dynamic_delay(port: str, plug: bool) -> bool:
        maximum_delay = 10
        polling_counter = 0
        status = False
        while polling_counter <= maximum_delay:
            # Retrieving enumerated displays and checking if display is attached on requested port.
            enumerated_displays = DisplayConfiguration().get_enumerated_display_info()
            status = display_config.is_display_attached(enumerated_displays, port)
            if plug:
                # if Expected: plug; Actual: plug, then break, otherwise wait for 1 second and check again.
                if status:
                    break
                time.sleep(1)
                polling_counter += 1
            else:
                # if Expected: unplug; Actual: unplug, then break, otherwise wait for 1 second and check again.
                if not status:
                    break
                time.sleep(1)
                polling_counter += 1

        if (plug and status) or (not plug and not status):
            return True
        # Returns false if time limit of 60 second is exceeded.
        return False

    ##
    # @brief        Helper api for detachable_LFP verifications.
    #               This public method can be used outside this feature for concurrency testing.
    # @param[in]    port: str
    #               port to detach
    # @param[in]    gfx_index: str
    #               gfx_index. Eg. gfx_0, gfx_1
    # @param[in]    iterations: int
    #               Method plugs and unplugs companion display for N No of iterations (user-defined).
    # @param[in]    operation: Operation (Enum)
    #               Operation.stress_test - plugs and unplugs companion display for given number of iterations.
    #               Operation.plug - Only plugs companion display on given port.
    #               Operation.unplug - Only unplugs companion display on given port.
    # @return       None
    def verify_detachable_LFP(self, port: str, gfx_index: str, iterations: int, operation: Operation):
        # detachable_LFP initialization : Enable reg_key, do port mapping and
        # make companion display unplugged initially if it is plugged.
        status = self.__initialize_detachable_LFP(self.mapped_port_to_detach,
                                                  port_type=self.port_type, gfx_index=self.gfx_index)
        if status:
            logging.info("Pass: Detachable_LFP initialization is successful.")
        else:
            self.fail("[Test Issue] : Failed to initialize Detachable_LFP.")

        # if user just wants to plug or unplug; set iterations to 1.
        if operation == self.Operation.plug or operation == self.Operation.unplug:
            iterations = 1

        # Verify plug/unplug for N iterations.
        for i in range(0, iterations):
            # Plug only for operation.plug and operation.stress_test.
            if operation == self.Operation.stress_test or operation == self.Operation.plug:
                plug_status = \
                    self._setHPD(self.mapped_port_to_detach, plug=True, port_type=self.port_type, gfx_index=gfx_index)

                # checking if plug call is successful.
                if not plug_status:
                    self.fail(f"[Test Issue] - Unable to plug companion display on port - {port}")

                # Delay using polling mechanism until companion display is plugged.
                is_display_attached = self._dynamic_delay(port, plug=True)
                self.assertTrue(is_display_attached,
                                f"[Test Issue] - Timeout reached! Display is not enumerated on port {port}")
                logging.info(f"Pass: Successfully plugged companion display on port - {port}")

                # This case is when user only wants to plug companion display.
                if operation == self.Operation.plug:
                    break

            unplug_status = \
                self._setHPD(self.mapped_port_to_detach, plug=False, port_type=self.port_type, gfx_index=gfx_index)

            # checking if unplug call is successful.
            if not unplug_status:
                self.fail(f"[Test Issue] - Unable to unplug companion display on port - {port}")

            # Delay using polling mechanism until companion display is unplugged
            is_display_detached = self._dynamic_delay(port, plug=False)
            self.assertTrue(is_display_detached,
                            f"[Test Issue] - Timeout reached! Display is still enumerated on port {port}")
            logging.info(f"Pass: Successfully unplugged companion display on port - {port}")

        logging.info("Detachable_LFP verification is completed.")

    ##
    # @brief        This function verifies Independent brightness for the Detachable LFP via IGCL API
    #               Added as part of escape action: HSD-16023432259
    # @return       Pass if there is brightness change after changing screen brightness and it matches else False
    @staticmethod
    def verify_blc_after_attach() -> bool:
        status = True
        transition_steps = 200
        logging.info('Verifying BLC for companion display after it is attached:')

        ##
        # 1. Get enumerated display info to fetch detachable LFP's target ID
        enumerated_displays = DisplayConfiguration().get_enumerated_display_info()
        target_id = enumerated_displays.ConnectedDisplays[1].TargetID

        ##
        # 2. Set various brightness level and verify if they work
        for _ in range(3):
            for i in range(10):
                brightness_level = (i * 10)

                ##
                # Change screen brightness value through IGCL api and see if it matches with current brightness
                logging.info(f'Setting and verifying brightness level: {brightness_level}')
                status &= blc.apply_independent_brightness(target_id, brightness_level, transition_steps)
                if status is False:
                    logging.error(f'Independent Brightness verification failed when trying to set brightness level: {brightness_level}!')
                    gdhm.report_driver_bug_di('[DETACHABLE_LFP][IndependentBrightness] Verification Failed!')

        return status

    ##
    # @brief        This function verifies PPS enable and disable sequence for EDP2 from the ETL data during plug-unplug
    #               Added as part of escape action: HSD-16023432259 (After attach-detach of keyboard, EDP2 blanks out)
    # @return       Pass if PPS sequence is correct, otherwise fail
    def verify_pps_basic(self) -> bool:
        ##
        # Verify PPS
        logging.info("Verifying Panel Power Sequence")

        # 1. At this point we would have completed exactly 1 round of unplug and plug of EDP2
        # Hence we will perform below two verifications from the ETL
        # timestamp of bklt off < pwm off < vdd off -> Disable sequence (unplug)
        # timestamp of vdd on > pwm on > bklt on -> Enable sequence (plug)
        self.pps_ver.generate_etl('GfxTrace_pps.etl', skip_power_event=True)

        # 2. Invoke existing API to verify PPS sequence (Detachable_LFP)
        lfp2_status = self.pps_ver.verify_pps_sequence(detachable_lfp=True)

        # 3. GDHM reporting for detachable LFP
        if lfp2_status is False:
            logging.error('PPS verification on LFP2 failed!')
            gdhm.report_driver_bug_di('[DETACHABLE_LFP][PPS] Verification on LFP_2 Failed!')

        return lfp2_status

    ##
    # @brief        This function verifies PPS enable and disable sequence for both the EDPs by triggering sleep event
    # @return       Pass if PPS sequence is correct, otherwise fail
    def verify_pps_with_power_event(self) -> bool:
        ##
        # Verify PPS
        logging.info("Verifying Panel Power Sequence")

        # 1. Stop the default ETL tracer started by Init CTL API
        # This is needed because , there will be multiple VDD, DD_BKLT, DD_PWM
        # timestamps present in the full ETL as it started before plug of 2nd EDP.
        if etl_tracer.stop_etl_tracer() is False:
            self.fail("[Test Issue] Failed to stop default ETL Tracer")

        # 2. Sleep will be triggered as part of below function which will trigger PPS enable and disable sequence
        # These will be captured in a new ETL with the name of "GfxTrace_PPS.etl"
        # From the newly captured ETL, we will make sure below things:
        # timestamp of bklt off < pwm off < vdd off -> Disable sequence
        # timestamp of vdd on > pwm on > bklt on -> Enable sequence
        self.pps_ver.generate_etl('GfxTrace_pps.etl')


        # 3. Invoke existing API to verify PPS sequence (Detachable_LFP)
        # @todo: [HSD-XXXX] -  Currently there is a bug. Driver is only turning off/on BKLT.
        # @todo: VDD and PWM are not turned off and on during CS-Resume for EDP2. It works fine for EDP1 though. Uncomment below lines of code if fixed.
        '''
        lfp2_status = self.pps_ver.verify_pps_sequence(detachable_lfp=True)

        # 4. GDHM reporting for detachable LFP
        if lfp2_status is False:
            logging.error('PPS verification on LFP2 failed!')
            gdhm.report_driver_bug_di('[DETACHABLE_LFP][PPS] Verification on LFP_2 Failed!')
        '''

        # 5. Invoke existing API to verify PPS sequence for LFP_1
        lfp1_status = self.pps_ver.verify_pps_sequence()

        # 6. GDHM reporting for LFP_1
        if lfp1_status is False:
            logging.error('PPS sequence on LFP1 failed!')
            gdhm.report_driver_bug_di('[DETACHABLE_LFP][PPS] Verification on LFP_1 Failed!')

        return lfp1_status


    ##
    # @brief        This method is the exit point for Detachable_LFP tests.
    # @return       None
    @reboot_helper.__(reboot_helper.teardown)
    def tearDown(self):
        logging.info("Test Cleanup...")
        if self.is_manual_scenario == False:
            # make sure companion display(LFP_2) is unplugged at the end.
            # Retrieving enumerated displays and checking if display is attached on requested port.
            enumerated_displays = DisplayConfiguration().get_enumerated_display_info()
            status = display_config.is_display_attached(enumerated_displays, self.mapped_port_to_detach)
            # if companion display is present, then unplugging it.
            if status and self.mapped_port_to_detach == 'DP_B':
                self._setHPD(self.mapped_port_to_detach, plug=False, port_type=self.port_type, gfx_index=self.gfx_index)

            # Disabling Reg Key
            ret = registry.write(self.gfx_index, self.reg_key, registry_access.RegDataType.DWORD, 0x0)
            if ret is None:
                logging.info(self.reg_key + ' reg key already disabled.')
            elif ret is True:
                logging.info('Successfully disabled ' + self.reg_key + ' reg key')

            # Reset VBT to default state so that prepare display can simulate MIPI panel for the next tests.
            # This step is not need in case of EDP.
            # WA: Skip driver restart in case of negative case - test passes but client goes to bad state.
            if self.edp_as_companion_display == False and self.mapped_port_to_detach != 'DP_A':
                logging.info('Resetting VBT to default state')
                if Vbt().reset() is False:
                    self.fail('[Test Issue]: Reset Vbt failed')

                # Disabling Independent brightness reg key
                registry.delete(self.gfx_index, registry.RegKeys.BLC.INDEPENDENT_BRIGHTNESS_CTL)

                # driver disable/enable
                logging.info('Doing a disable-enable of display driver after disabling detachable LFP reg key, '
                             'resetting VBT and removing independent brightness reg key.')
                status, reboot_required = display_essential.restart_gfx_driver()
                if status is False:
                    self.fail('[Driver Issue]: Restarting display driver failed')

        logging.info("Teardown is completed...")
