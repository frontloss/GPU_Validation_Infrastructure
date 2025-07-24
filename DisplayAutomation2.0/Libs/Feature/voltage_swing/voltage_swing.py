##############################################################################################################
# \file         voltage_swing_helper.py
# \addtogroup   PyLibs_Voltage_swing
# \brief        Python Wrapper that exposes the generic method to verify voltage swing
# \remarks      Checks for the platform and calls the correct implementation
# <ul>
# <li> @ref     verify_voltage_swing        	    \n \copybrief verify_voltage_swing \n
# </li>
# </ul>
# \author       Girish Y D
##############################################################################################################
import logging

from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Core.test_env.test_environment import TestEnvironment


##
# VOLTAGE SWING TEST PARAMETERS CLASS
# \brief  - This Object need to used as an input parameter for verify_voltage_swing interface
class VoltageSwingTestParameters(object):
    platform = None
    # display_port = 'HDMI_B'/'DP_B'/'HDMI_C'/'DP_C'/'HDMI_D'/'DP_D'/...
    display_port = None

    # is_active_level_shifter = True or False ( True : active level shifter , False : Passive level shifter)
    is_active_level_shifter = None

    ##
    # Initialize object with Test Parameters
    def __init__(self, display_port, is_active_level_shifter=True):
        self.display_port = display_port
        self.is_active_level_shifter = is_active_level_shifter

    ##
    # @brief     - validates required inputs are initialized for verify_voltage_swing interface based on the platform
    def validate(self):
        result = True

        supported_platforms = ['SKL', 'KBL', 'CFL', 'CNL', 'GLK']
        supported_display_ports = {'SKL': ['HDMI_B', 'HDMI_C', 'HDMI_D'],
                                   'KBL': ['HDMI_B', 'HDMI_C', 'HDMI_D'],
                                   'CFL': ['HDMI_B', 'HDMI_C', 'HDMI_D'],
                                   'CNL': ['HDMI_B', 'HDMI_C', 'HDMI_D', 'HDMI_F'],
                                   'GLK': ['HDMI_B', 'HDMI_C']}

        machine_info = SystemInfo()
        gfx_display_hwinfo = machine_info.get_gfx_display_hardwareinfo()
        # WA : currently test are execute on single platform. so loop break after 1 st iteration.
        # once Enable MultiAdapter remove the break statement.
        for i in range(len(gfx_display_hwinfo)):
            self.platform = ("%s" % gfx_display_hwinfo[i].DisplayAdapterName)
            break

        if self.platform is None:
            logging.error("API get_machine_info Failed to return platform details")
            return False
        else:
            self.platform = self.platform.upper()
            if self.platform not in supported_platforms:
                logging.error("Verify voltage swing for platform %s not implemented" % self.platform)
                return False

        self.display_port = self.display_port.upper()
        display = str(self.display_port).split('_')[0]
        if display != 'HDMI':
            logging.error("verify_voltage_swing is not implemented for %s" % display)
            return False
        elif self.display_port not in supported_display_ports[self.platform]:
            logging.error("%s is not Supported by platform %s" % (self.display_port, self.platform))
            return False

        return result


##
# @brief     - Checks for the platform and calls the correct implementation to verify voltage swing
# @param[in] - vs_test_parameters_obj is of type VoltageSwingTestParameters
# @return    - True if voltage swing programming is correct else False
def verify_voltage_swing(vs_test_parameters_obj):
    if vs_test_parameters_obj.validate() is False:
        return False

    if vs_test_parameters_obj.platform.upper() in ['SKL', 'KBL', 'CFL']:
        from Libs.Feature.voltage_swing import gen9_verify_voltage_swing as verify_voltage_swing
        voltage_swing = verify_voltage_swing.GEN9VerifyVoltageSwing()
        return voltage_swing.verify_voltage_swing(vs_test_parameters_obj)
    elif vs_test_parameters_obj.platform.upper() == 'CNL':
        from Libs.Feature.voltage_swing import cnl_verify_voltage_swing as verify_voltage_swing
        voltage_swing = verify_voltage_swing.CNLVerifyVoltageSwing()
        return voltage_swing.verify_voltage_swing(vs_test_parameters_obj)
    elif vs_test_parameters_obj.platform.upper() == 'GLK':
        from Libs.Feature.voltage_swing import glk_verify_voltage_swing as verify_voltage_swing
        voltage_swing = verify_voltage_swing.GLKVerifyVoltageSwing()
        return voltage_swing.verify_voltage_swing(vs_test_parameters_obj)
    else:
        logging.error("Verify voltage swing for platform %s not implemented" % vs_test_parameters_obj.platform.upper())
        return False


if __name__ == "__main__":
    TestEnvironment.initialize()
    display_port = "HDMI_B"
    vs_test_parameters_obj = VoltageSwingTestParameters(display_port)
    result = verify_voltage_swing(vs_test_parameters_obj)
    if (result is True):
        logging.info("PASS : verify_voltage_swing")
    else:
        logging.error("FAIL : verify_voltage_swing")
