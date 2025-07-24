##############################################################################################################
# @file       voltage_swing_helper.py
# @brief      Python Wrapper that exposes the generic helper methods
# @author     Girish Y D
##############################################################################################################
import logging
from enum import IntEnum

from Libs.Core import display_essential
from Libs.Core.vbt.vbt import Vbt

iboost_magnitude_array = [0x1, 0x3, 0x7]


##
# VBT DeviceClass Enum
class VBTDeviceClass(IntEnum):
    NO_DEVICE = 0X0000
    INTEGRATED_DP_ONLY = 0X68C6
    INTEGRATED_EDP = 0X78C6
    INTEGRATED_DP_WITH_HDMI_OR_DVI = 0X60D6
    INTEGRATED_DP_WITH_DVI = 0X68D6
    INTEGRATED_HDMI_OR_DVI = 0X60D2
    INTEGRATED_DVI_ONLY = 0X68D2
    INTEGRATED_MIPI = 0X7CC2


##
# @brief         Does the platform check and returns port number as per VBT for the display_port if supported
# @param[in]     platform
# @param[in]     display_port
# @return        VBT port number if display_port is supported else None
def get_vbt_port_number(platform, display_port):
    display_port = display_port.upper()
    display = str(display_port).split('_')[0]
    if display not in ['HDMI', 'DP']:
        logging.error("get_vbt_port_number is not implemented for %s" % display)
        return None

    vbt_display_port_map = None
    if platform.upper() == "CNL":
        vbt_display_port_map = dict([
            ('HDMI_B', 0x01),
            ('HDMI_C', 0x02),
            ('HDMI_D', 0x03),
            ('HDMI_F', 0x0E),
            ('DP_B', 0x07),
            ('DP_C', 0x08),
            ('DP_D', 0x09),
            ('DP_E', 0x0B),
            ('DP_F', 0x0D)
        ])
    elif platform.upper() == "GLK":
        vbt_display_port_map = dict([
            ('HDMI_B', 0x01),
            ('HDMI_C', 0x02),
            ('DP_A', 0x0A),
            ('DP_B', 0x07),
            ('DP_C', 0x08)
        ])
    elif platform.upper() in ["SKL", "KBL", "CFL"]:
        vbt_display_port_map = dict([
            ('HDMI_B', 0x01),
            ('HDMI_C', 0x02),
            ('HDMI_D', 0x03),
            ('DP_B', 0x07),
            ('DP_C', 0x08),
            ('DP_D', 0x09),
            ('DP_E', 0x0B)
        ])
    else:
        logging.error("get_vbt_supported_ports not implemented for %s" % platform)
        return None
    return vbt_display_port_map.get(display_port)


##
# @brief         Does the platform check and returns max level/index of hdmi level shifter supported
# @param[in]     platform
# @return        max level/index of hdmi level shifter configuration or -1 if not implemented for platform
def get_hdmi_max_level_shifter_configuration_level(platform):
    max_level_shifter_configuration_level = -1
    if platform.upper() == "CNL":
        max_level_shifter_configuration_level = 15
    elif platform.upper() == "GLK":
        max_level_shifter_configuration_level = 9
    elif platform.upper() in ["SKL", "KBL", "CFL"]:
        max_level_shifter_configuration_level = 10
    else:
        logging.error("get_hdmi_max_level_shifter_configuation_level not implemented for %s" % platform)
    return max_level_shifter_configuration_level


##
# @brief        If VBT is configured  with given display_port (HDMI_B/HDMI_C/HDMI_D/HDMI_E/HDMI_F
#               then returns vbt block2 and device_index (1, 2, 3, 4)
# @param[in]    platform
# @param[in]    display_port
# @return       True, stBlock2 , device_index If success; False, None, None If Fail
#               where stBlock2 is data block2 of VBT of TYPE Block2 which is defined in vbt_access.py
#                    device_index is index of DisplayDeviceDataStructureEntry array in Block2 where display_port is configured
def get_vbt_block2_if_display_port_configured(platform, display_port):
    result = True
    device_index = None

    display = str(display_port).split('_')[0]
    port = str(display_port).split('_')[1]
    if display != 'HDMI':
        logging.error("get_vbt_block2_if_display_port_configured is not implemented for %s" % display)
        return False, None, device_index

    vbt_hdmi_port_number = get_vbt_port_number(platform, display_port)
    if vbt_hdmi_port_number is None:
        return False, None, device_index
    vbt_dp_port_number = get_vbt_port_number(platform, 'DP_' + port)

    gfx_vbt = Vbt()
    ##
    # Getting VBT block
    is_vbt_configured_with_display_port = False
    for index in range(1, 4):
        st_name = VBTDeviceClass.INTEGRATED_DP_WITH_DVI.name
        stblock2_device_class = gfx_vbt.block_2.DisplayDeviceDataStructureEntry[index].DeviceClass
        stblock2_dvo_port = gfx_vbt.block_2.DisplayDeviceDataStructureEntry[index].DVOPort
        if ((
                stblock2_device_class == VBTDeviceClass.INTEGRATED_HDMI_OR_DVI and stblock2_dvo_port == vbt_hdmi_port_number)
                or (
                        stblock2_device_class == VBTDeviceClass.INTEGRATED_DP_WITH_HDMI_OR_DVI and stblock2_dvo_port == vbt_dp_port_number)):
            is_vbt_configured_with_display_port = True
            device_index = index
            break
    if is_vbt_configured_with_display_port is False:
        logging.debug("ERROR : VBT is not configured with %s" % display_port)
        result = False
        device_index = None
    return result, gfx_vbt, device_index


##
# @brief         If VBT is configured with given display_port (HDMI_B/HDMI_C/HDMI_D/HDMI_E/HDMI_F
#                then returns hdmi level shifter configuration level/index set in VBT
# @param[in]     platform
# @param[in]     display_port
# @return        True, Level/Index If success; False, None If Fail
#              Level/Index = level/index value of voltage swing selected/set in VBT
def get_vbt_hdmi_level_shifter_configuration(platform, display_port):
    result = True
    level_shifter_configuration_level = None
    is_vbt_configured_with_display_port, gfx_vbt, device_index = get_vbt_block2_if_display_port_configured(platform,
                                                                                                           display_port)
    if is_vbt_configured_with_display_port is True:
        level_shifter_configuration_level = gfx_vbt.block_2.DisplayDeviceDataStructureEntry[
            device_index].HDMILevelShifter
    else:
        result = False
    return result, level_shifter_configuration_level


##
# @brief         For the given display_port (HDMI_B/HDMI_C/HDMI_D/HDMI_E/HDMI_F
#                If VBT is configured then sets hdmi level shifter configuration level/index in VBT
#                and does restart of driver
# @param[in]     platform
# @param[in]     display_port
# @param[in]     level_shifter_configuration_level should be level/index value of voltage swing selected/set in VBT
# @param[in]     restart_driver
# @return        True If success; False, If Fail
def set_vbt_hdmi_level_shifter_configuration(platform, display_port, level_shifter_configuration_level,
                                             restart_driver=False):
    result = True
    is_vbt_modified = False

    is_vbt_configured_with_display_port, gfx_vbt, device_index = get_vbt_block2_if_display_port_configured(platform,
                                                                                                           display_port)
    if is_vbt_configured_with_display_port is True:
        max_level = get_hdmi_max_level_shifter_configuration_level(platform)
        if max_level is -1:
            return False

        if (0 <= level_shifter_configuration_level <= max_level) is False:
            logging.error("level_shifter_configuration_level: %s is not Supported" % level_shifter_configuration_level)
            return False

        gfx_vbt.block_2.DisplayDeviceDataStructureEntry[
            device_index].HDMILevelShifter = level_shifter_configuration_level
        if gfx_vbt.apply_changes() is False:
            logging.error('Setting VBT block 2 failed')
            result = False
        else:
            is_vbt_modified = True
    else:
        result = False

    if is_vbt_modified is True and restart_driver is True:
        status, reboot_required = display_essential.restart_gfx_driver()
        if status is False:
            logging.error('restarting display driver failed')
            result = False
    return result


##
# @brief         If VBT is configured with given display_port (HDMI_B/HDMI_C/HDMI_D/HDMI_E/HDMI_F
#                then returns Iboost is enabled or disabled and iboost magnitude set in VBT
# @param[in]     platform
# @param[in]     display_port
# @return        True, iboost_enabled, iboost_magnitude If success; False, None, None If Failure
#                where iboost_enabled (1 or 0)  1 -ENABLE ; 0-DISABLE
#                iboost_magnitude will be 0x1 or  0x3 or 0x7
def get_iboost_details(platform, display_port):
    result = True
    iboost_enabled = None
    iboost_magnitude = None

    if platform.upper() not in ["SKL", "KBL", "CFL"]:
        logging.error("IBoost Feature is not supported for Platform :%s" % platform)
        return False, iboost_enabled, iboost_magnitude

    display = str(display_port).split('_')[0]
    if display != 'HDMI':
        logging.error("get_iboost_details is not implemented for %s" % display)
        return False, iboost_enabled, iboost_magnitude

    is_vbt_configured_with_display_port, gfx_vbt, device_index = get_vbt_block2_if_display_port_configured(platform,
                                                                                                           display_port)
    if is_vbt_configured_with_display_port is True:
        iboost_enabled = (gfx_vbt.block_2.DisplayDeviceDataStructureEntry[
                              device_index].Flags1 >> 3) & 0b00000001
        vbt_iboost_magnitude_index_for_hdmi = (gfx_vbt.block_2.DisplayDeviceDataStructureEntry[
                                                   device_index].BoostLevel >> 4) & 0b00001111
        iboost_magnitude = iboost_magnitude_array[vbt_iboost_magnitude_index_for_hdmi]
    else:
        result = False
    logging.debug("device_index = %s, Flags1 =%s, boost_level =%s" % (
    device_index, gfx_vbt.block_2.DisplayDeviceDataStructureEntry[device_index].Flags1,
    gfx_vbt.block_2.DisplayDeviceDataStructureEntry[device_index].BoostLevel))
    logging.debug("iboost_enabled = %s, iboost_magnitude =%s" % (
        iboost_enabled, iboost_magnitude))
    return result, iboost_enabled, iboost_magnitude


##
# @brief         For the given display_port (HDMI_B/HDMI_C/HDMI_D/HDMI_E/HDMI_F
#                If VBT is configured then sets iboost_enabled and iboost_magnitude in VBT
#                and does restart of driver
# @param[in]     platform
# @param[in]     display_port
# @param[in]     iboost_enabled  should be (1 or 0)  1 -ENABLE ; 0-DISABLE
# @param[in]     iboost_magnitude should be (0x1 or 0x3 or 0x7)
# @param[in]     restart_driver
# @return        True, If success; False, If Failure
def set_iboost_details(platform, display_port, level_shifter_configuration_level, iboost_enabled, iboost_magnitude,
                       restart_driver=False):
    result = True
    is_vbt_modified = False

    if platform.upper() not in ["SKL", "KBL", "CFL"]:
        logging.error("IBoost Feature is not supported for Platform :%s" % platform)
        return False

    display = str(display_port).split('_')[0]
    if display != 'HDMI':
        logging.error("set_iboost_details is not implemented for %s" % display)
        return False

    is_vbt_configured_with_display_port, gfx_vbt, device_index = get_vbt_block2_if_display_port_configured(platform,
                                                                                                           display_port)
    if is_vbt_configured_with_display_port is True:
        # Iboost Enable/Disable
        if iboost_enabled == 1:
            gfx_vbt.block_2.DisplayDeviceDataStructureEntry[device_index].Flags1 |= 0b00001000
        else:
            gfx_vbt.block_2.DisplayDeviceDataStructureEntry[device_index].Flags1 &= 0b11110111

        # Iboost_magnitude
        if iboost_magnitude == 0x1:
            gfx_vbt.block_2.DisplayDeviceDataStructureEntry[device_index].BoostLevel &= 0b00001111
            gfx_vbt.block_2.DisplayDeviceDataStructureEntry[device_index].BoostLevel |= 0b00000000
        elif iboost_magnitude == 0x3:
            gfx_vbt.block_2.DisplayDeviceDataStructureEntry[device_index].BoostLevel &= 0b00001111
            gfx_vbt.block_2.DisplayDeviceDataStructureEntry[device_index].BoostLevel |= 0b00010000
        elif iboost_magnitude == 0x7:
            gfx_vbt.block_2.DisplayDeviceDataStructureEntry[device_index].BoostLevel &= 0b00001111
            gfx_vbt.block_2.DisplayDeviceDataStructureEntry[device_index].BoostLevel |= 0b00100000

        # voltage swing level
        gfx_vbt.block_2.DisplayDeviceDataStructureEntry[
            device_index].HDMILevelShifter = level_shifter_configuration_level

        logging.info("device_index = %s, Flags1 =%s, boost_level =%s" % (
            device_index, gfx_vbt.block_2.DisplayDeviceDataStructureEntry[device_index].Flags1,
            gfx_vbt.block_2.DisplayDeviceDataStructureEntry[device_index].BoostLevel))

        if gfx_vbt.apply_changes() is False:
            logging.error('Setting VBT block 2 failed')
            result = False
        else:
            is_vbt_modified = True
    else:
        result = False

    if is_vbt_modified is True and restart_driver is True:
        status, reboot_required = display_essential.restart_gfx_driver()
        if status is False:
            logging.error('restarting display driver failed')
            result = False
    return result


##
# @brief Reset the VBT and restart the driver. After this call, Driver uses default VBT.
# @return    - True If success; False, If Fail
def reset_vbt_and_restart_driver():
    result = True
    if Vbt().reset() is False:
        logging.error('VBT RESET Failed')
        result = False
    else:
        status, reboot_required = display_essential.restart_gfx_driver()
        if status is False:
            logging.error('restarting display driver failed')
            result = False
    return result


##
# @brief        function validate feature and log it generically
# @param[in]    current_value
# @param[in]    expected_value
# @param[in]    feature
# @return       True If Sucess; False if Fail
def validate_feature(current_value, expected_value, feature):
    if (current_value == expected_value):
        logging.info("PASS: {0}- Expected : {1} Actual : {2}".format(feature, str(expected_value), str(current_value)))
        return True
    else:
        logging.error("FAIL: {0}- Expected : {1} Actual : {2}".format(feature, str(expected_value), str(current_value)))
        return False


##
# @brief        function verifies register bit field value
# @param[in]    reg_offset_name
# @param[in]    reg_offset
# @param[in]    bit_field_name
# @param[in]    bit_field_expected_value
# @return       True, If success; False, If Fail
def verify_register_bit_fields(reg_offset_name, reg_offset, bit_field_name, bit_field_expected_value):
    result = True
    bit_field_actual_value = reg_offset.__getattribute__(bit_field_name)
    feature_name = reg_offset_name + '_' + bit_field_name
    result &= validate_feature(bit_field_actual_value, bit_field_expected_value, feature_name)
    return result
