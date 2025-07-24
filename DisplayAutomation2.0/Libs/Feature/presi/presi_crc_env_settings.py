#####################################################################################################################################
# @file         presi_crc_env_settings.py
# @brief        Interface for setting CRC value enviornment in pre-silicon environment
# @author       ** ADD DETAILS HERE **
########################################################################################################################
import ctypes
import logging
import os
import winreg
from ctypes.wintypes import RGB

from Libs.Core import enum, registry_access
from Libs.Core.test_env import test_context
from Libs.Core.test_env.test_environment import TestEnvironment


##
# @brief        sets desktop background
# @param[in]    desktop_img_path - Image File to be set
# @return       status - bool
def set_desktop_bg(desktop_img_path=None):
    status = False
    dll = ctypes.WinDLL('user32')
    SPI_GETDESKWALLPAPER = 0x0073
    SPI_SETDESKWALLPAPER = 0x0014
    SPIF_SENDCHANGE = 0x0003

    ubuf = ctypes.create_unicode_buffer(200)
    if dll.SystemParametersInfoW(SPI_GETDESKWALLPAPER, 200, ubuf, 0):
        logging.debug("Current Desktop Wallpaper Path : %s" % ubuf.value)

    if desktop_img_path is None:
        desktop_img_path = os.path.join(test_context.TestContext.root_folder(), "TestStore\\CRC\\img0.jpg")

    logging.debug("Setting Desktop Wallpaper Path : %s" % desktop_img_path)
    if dll.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, ctypes.create_unicode_buffer(desktop_img_path),
                                 SPIF_SENDCHANGE):
        ubuf = ctypes.create_unicode_buffer(200)
        if dll.SystemParametersInfoW(SPI_GETDESKWALLPAPER, 200, ubuf, 0):
            if ubuf.value == desktop_img_path:
                logging.info("Desktop background is set with image %s" % desktop_img_path)
                status = True
    if status is False:
        logging.error("FAIL : Seeting Desktop background with image : %s" % desktop_img_path)
    return status


##
# @brief        sets desktop background color
# @param[in]    color  "RGB Value to be set"
#                      - if color value is not provided then api will set color to dark blue
# @return       status - bool
def set_desktop_color(color=None):
    status = False
    dll = ctypes.WinDLL('user32')
    SPI_GETDESKWALLPAPER = 0x0073
    SPI_SETDESKWALLPAPER = 0x0014
    SPIF_SENDCHANGE = 0x0003
    if dll.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, "", SPIF_SENDCHANGE):
        COLOR_BACKGROUND = 1  # from winuser.h
        SetSysColors = ctypes.windll.user32.SetSysColors
        if color is None:
            color = RGB(0, 99, 177)  # Dark Blue
        status = SetSysColors(1, ctypes.byref(ctypes.c_int(COLOR_BACKGROUND)), ctypes.byref(ctypes.c_int(color)))
    return status


##
# @brief        Set HDWM properties and set show configurations Message as ON
# @param[in]    action - The signing action
# @return       None
def set_hdwm_properties_show_cfg_msg_on(action=False):
    hdwm_properties = os.path.join("C:\\hdwm.properties")
    hdwm_properties_fd = open(hdwm_properties, 'r')
    hdwm_properties_lines = hdwm_properties_fd.readlines()
    hdwm_properties_fd.close()
    hdwm_properties_fd = open(hdwm_properties, 'w')
    for hdwm_properties_line in hdwm_properties_lines:
        if "hdwm_properties_show_cfg_msg_on" in hdwm_properties_line:
            if action is False:
                hdwm_properties_line = "hdwm_properties_show_cfg_msg_on=Off\n"
            else:
                hdwm_properties_line = "hdwm_properties_show_cfg_msg_on=On\n"
            hdwm_properties_fd.write(hdwm_properties_line)
        else:
            hdwm_properties_fd.write(hdwm_properties_line)
    hdwm_properties_fd.close()


##
# @brief        Hide Desktop Icons
# @param[in]    action - The signing action
# @return       None
def hide_desktop_icons1(action=True):
    reg_args = registry_access.LegacyRegArgs(hkey=registry_access.HKey.CURRENT_USER,
                                             reg_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced")
    registry_access.write(args=reg_args, reg_name="HideIcons", reg_type=registry_access.RegDataType.DWORD,
                          reg_value=0x1 if action is True else 0x0)


##
# @brief        Disable Multiple Display taskbar
# @return       None
def disable_multiple_display_taskbar():
    # Disable Multiple Display TaskBar
    reg_args = registry_access.LegacyRegArgs(hkey=registry_access.HKey.CURRENT_USER,
                                             reg_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced")
    registry_access.write(args=reg_args, reg_name="MMTaskbarEnabled", reg_type=registry_access.RegDataType.DWORD,
                          reg_value=0)


##
# @brief        Disable Windows Notifications
# @return       None
def disable_windows_notifications():
    # Disable BallonTips
    reg_args1 = registry_access.LegacyRegArgs(hkey=registry_access.HKey.CURRENT_USER,
                                              reg_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced")
    registry_access.write(args=reg_args1, reg_name="EnableBalloonTips", reg_type=registry_access.RegDataType.DWORD,
                          reg_value=0)

    # Disable Push Notifications
    reg_args2 = registry_access.LegacyRegArgs(hkey=registry_access.HKey.CURRENT_USER,
                                              reg_path=r"Software\Microsoft\Windows\CurrentVersion\PushNotifications")
    registry_access.write(args=reg_args2, reg_name="ToastEnabled", reg_type=registry_access.RegDataType.DWORD,
                          reg_value=0)

    # Disable Firewall notification pop up
    registry_handle = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
    registry_path = r"Software\Microsoft\Windows\CurrentVersion\Notifications\Settings"
    key_handle = winreg.OpenKey(registry_handle, registry_path, 0, winreg.KEY_WRITE)
    sub_key = "Windows.SystemToast.SecurityAndMaintenance"
    new_key_handle = winreg.CreateKey(key_handle, sub_key)
    winreg.FlushKey(new_key_handle)
    winreg.CloseKey(new_key_handle)
    winreg.FlushKey(key_handle)
    winreg.CloseKey(key_handle)
    winreg.CloseKey(registry_handle)
    reg_args2 = registry_access.LegacyRegArgs(hkey=registry_access.HKey.CURRENT_USER,
                                              reg_path=r"Software\Microsoft\Windows\CurrentVersion\Notifications\Settings\Windows.SystemToast.SecurityAndMaintenance")
    registry_access.write(args=reg_args2, reg_name="Enabled", reg_type=registry_access.RegDataType.DWORD, reg_value=0)

    # Disable Notification Center
    registry_handle = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
    registry_path = "Software\Policies\Microsoft\Windows"
    key_handle = winreg.OpenKey(registry_handle, registry_path, 0, winreg.KEY_WRITE)
    sub_key = "Explorer"
    new_key_handle = winreg.CreateKey(key_handle, sub_key)
    winreg.FlushKey(new_key_handle)
    winreg.CloseKey(new_key_handle)
    winreg.FlushKey(key_handle)
    winreg.CloseKey(key_handle)
    winreg.CloseKey(registry_handle)
    reg_args2 = registry_access.LegacyRegArgs(hkey=registry_access.HKey.CURRENT_USER,
                                              reg_path=r"Software\Policies\Microsoft\Windows\Explorer")
    registry_access.write(args=reg_args2, reg_name="DisableNotificationCenter",
                          reg_type=registry_access.RegDataType.DWORD, reg_value=1)


##
# @brief        Set Test signing as ON
# @param[in]    action - The signing action
# @return       None
def set_test_signing_on(action=False):
    cmd_line = "bcdedit -set TESTSIGNING OFF"
    if action is True:
        cmd_line = "bcdedit -set TESTSIGNING ON"
    os.system(cmd_line)


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("****SET PRE-SI CRC ENV Settings *****")
    logging.info(" SET DESKTOP Background ")
    set_desktop_bg()
    logging.info(" set_hdwm_properties_show_cfg_msg_on")
    set_hdwm_properties_show_cfg_msg_on()
    logging.info("hide_desktop_icons")
    hide_desktop_icons1()
    logging.info("disable_windows_notifications")
    disable_windows_notifications()
    logging.info("disable_multiple_display_taskbar")
    disable_multiple_display_taskbar()
    logging.info("set_test_signing_on")
    set_test_signing_on()
    ##
    # Need to do Restart of Machine after this settings
