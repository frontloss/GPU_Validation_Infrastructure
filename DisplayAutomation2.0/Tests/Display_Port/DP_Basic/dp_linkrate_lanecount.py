#######################################################################################################################
# @file         dp_linkrate_lanecount.py
# @brief        This tests verifies display engine for a given DP(clocks, pipe, plane, transcoders) for various configurations (link rates,lane count etc ).
# @details      Test Scenario:
#               1. Plug DP panel
#               2. Set display config to SD DP
#               3. Verify Display engine
#
# @author       Ap Kamal, Golwala Ami
#######################################################################################################################
import os
import time
from ctypes.wintypes import RGB

from Libs import env_settings
from Libs.Core import enum
from Libs.Core.logger import gdhm
from Libs.Core.test_env.test_context import TestContext
from Libs.Feature.display_engine.de_master_control import DisplayEngine
from Libs.Feature.presi import presi_crc, presi_crc_env_settings
from Tests.Display_Port.DP_Basic.dp_base import *


##
# @brief        This class contains a test function which implements the mentioned test scenario / test steps.
class dpConfigurationsTest(DpBase):

    ##
    # @brief        This test enables SSC if passed in command line
    # @return       None
    def test_plug_display(self):
        logging.info("**************DP LINKRATE/LANECOUNT TEST START**************")

        if len(self.plugged_dp_list) > 0:
            for key, value in self.plugged_dp_list:
                self.dp_plug_unplug("PLUG", value['connector_port'], value['edid_name'], value['dpcd_name'])

            enumerated_displays = self.config.get_enumerated_display_info()
            logging.info(enumerated_displays.to_string())

            if "-SSC" in sys.argv:
                status, reboot_required = self.set_ssc(enable=True)
                if status:
                    logging.info("Enable SSC in VBT passed and successfully restarted driver.")
                elif status is False and reboot_required is True:
                    if reboot_helper.reboot(self, 'test_run') is False:
                        self.fail("Failed to reboot the system")
                else:
                    self.fail("Failed to restart display driver")
        else:
            logging.error("Pluged_dp list is empty")
            self.fail()

    ##
    # @brief        This test method plugs the required display, applies modeset and verifies Display Engine.
    # @return       None
    def test_run(self):

        fail_count = 0
        if len(self.plugged_dp_list) > 0:
            for key, value in self.plugged_dp_list:
                # Test whether clock, plane, pipe, transcoder, DDI are programmed correctly
                ports = [value['connector_port']]
                silicon_type = env_settings.get('GENERAL', 'silicon_type')
                crc_presi_operation = env_settings.get('CRC', 'crc_presi')
                is_presi_crc = False
                if (silicon_type is not None and silicon_type in ['SIMULATOR', 'EMULATOR']
                        and crc_presi_operation is not None and crc_presi_operation in ['CAPTURE', 'COMPARE']):
                    color = RGB(20, 99, 177)  # Dark Blue
                    presi_crc_env_settings.set_desktop_color(color)
                    is_presi_crc = True
                    time.sleep(30)

                result = self.config.set_display_configuration_ex(enum.SINGLE, [value['connector_port']])
                if result == False:
                    self.fail("Failed to set display config")

                if is_presi_crc is True:
                    time.sleep(120)
                else:
                    time.sleep(5)
                display = DisplayEngine()
                test_fail = display.verify_display_engine(ports)
                test_fail &= self.verify_crc(value['connector_port'], value['edid_name'], value['dpcd_name'])
                if test_fail is False:
                    fail_count += 1

            for key, value in self.plugged_dp_list:
                if value['connector_port'] is not None:
                    self.dp_plug_unplug(action="UNPLUG", port=value['connector_port'])

            if fail_count != 0:
                self.fail("FAIL : dpConfigurationsTest")
                # Gdhm bug reporting handled in verify_display_engine and verify_or_capture_presi_crc
        else:
            logging.error("Pluged_dp list is empty")
            self.fail()

    ##
    # @brief        This test method disables SSC in VBT
    # @return       None
    def test_disable_ssc(self):

        if "-SSC" in sys.argv:
            status, reboot_required = self.set_ssc(enable=False)
            if status:
                logging.info("Disable SSC in VBT passed and successfully restarted driver.")
            elif status is False and reboot_required is True:
                if reboot_helper.reboot(self, 'test_end') is False:
                    self.fail("Failed to reboot the system")
            else:
                self.fail("Failed to restart display driver")

    ##
    # @brief        This test method ends the test.
    # @return       None
    def test_end(self):
        logging.info("**************DP LINKRATE/LANECOUNT TEST END**************")

    ##
    # @brief        This test method verifies the CRC for given port with mentioned EDID and DPCD.
    # @param[in]    connector_port: str
    #                   Port name for which display is to be plugged
    # @param[in]    edid_name: str
    #                   EDID to be plugged
    # @param[in]    dpcd_name: str
    #                   DPCD to be plugged
    # @return       crc_status : Boolean
    def verify_crc(self, connector_port, edid_name, dpcd_name):
        crc_status = True
        platform = None

        gfx_display_hwinfo = self.machine_info.get_gfx_display_hardwareinfo()
        # WA : currently test are execute on single platform. so loop break after 1 st iteration.
        # once Enable MultiAdapter remove the break statement.
        for i in range(len(gfx_display_hwinfo)):
            platform = ("%s" % gfx_display_hwinfo[i].DisplayAdapterName)
            break

        if platform.upper() in ['LKF1', 'TGL']:
            silicon_type = env_settings.get('GENERAL', 'silicon_type')
            crc_presi_operation = env_settings.get('CRC', 'crc_presi')
            if (silicon_type is not None and silicon_type in ['SIMULATOR', 'EMULATOR']
                    and crc_presi_operation is not None and crc_presi_operation in ['CAPTURE', 'COMPARE']):
                display_port = connector_port
                crc_file_name = "%s_dp_modes.crc" % platform.lower()
                crc_file_path = os.path.join(TestContext.root_folder(),
                                             "Tests\\Display_Port\\DP_Basic\crc\\%s" % crc_file_name)
                # mode_name , Example : "EDIDName_DPCDName"
                mode_name = edid_name.split(".")[0] + "_" + dpcd_name.split(".")[0]
                logging.info(" CAPTURE or VERIFY CRC For MODE %s" % mode_name)
                crc_status &= presi_crc.verify_or_capture_presi_crc(display_port, crc_file_path, mode_name)
        return crc_status


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('dpConfigurationsTest'))
    TestEnvironment.cleanup(outcome)
