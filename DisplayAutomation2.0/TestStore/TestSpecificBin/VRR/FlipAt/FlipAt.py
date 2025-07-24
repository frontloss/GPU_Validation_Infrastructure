########################################################################################################################
# @file         FlipAt.py
# @brief        Script to run FlipAt application with MinRr and MaxRr. Commmand lines FlipAt.py <MinRr> <MaxRr>
# @author       Doriwala Nainesh
########################################################################################################################
import os
import sys
import time
from Libs.Core import registry_access
from Libs.Core import winkb_helper as kb
from Libs.Core.test_env import test_context
from Tests.PowerCons.Modules import workload
from Tests.VRR import vrr

__VRR_BIN_FOLDER = os.path.join(test_context.TEST_SPECIFIC_BIN_FOLDER, "VRR")
minrr = maxrr = 0.0


# command parser to parse command line argument and update into global variable
def command_parser():
    global minrr, maxrr
    minrr = int(sys.argv[1])
    maxrr = int(sys.argv[2])


# command parser to parse command line argument and update into global variable
def launch_flip_at():
    app_config = workload.FlipAtAppConfig()
    app_config.pattern_1 = vrr.get_fps_pattern(maxrr)
    app_config.pattern_2 = vrr.get_fps_pattern(minrr, False)

    path = os.path.join(__VRR_BIN_FOLDER, "FlipAt\\FlipAt.exe")

    reg_args = registry_access.LegacyRegArgs(hkey=registry_access.HKey.CURRENT_USER, reg_path=r"Software\Microsoft")
    if registry_access.write(args=reg_args, reg_name=path, reg_type=registry_access.RegDataType.SZ,
                             reg_value="GpuPreference=0;VRREligibleOverride=1",
                             sub_key=r"DirectX\UserGpuPreferences") is False:
        print(f"\tFailed to update value ='GpuPreference=0;VRREligibleOverride=1' for {path=}")

    # Close any pop up notification before opening the app
    # Pressing WIN+A twice will open and close the notification center, which will close all notification toasts
    kb.press('WIN+A')
    time.sleep(1)
    kb.press('WIN+A')
    time.sleep(1)

    # Open given VRR testing app for each panel
    if workload.open_gaming_app(workload.Apps.FlipAt, False, app_config=app_config) is False:
        print(f"\tFailed to open {workload.Apps.FlipAt} app(Test Issue)")
    else:
        print(f"\tLaunched {workload.Apps.FlipAt} app successfully")
        kb.press('f')


# input value from command line to generate flip with FPS between MinRr and MaxRr
# example FlipAt.py 48 120
# example FlipAt.py 30 240
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("please pass argument in format:FlipAt.py MinRR, MaxRR")
    else:
        print("Input command lines:", end=" ")
        for index in range(len(sys.argv)):
            print(f"{sys.argv[index]}", end=" ")
        print("\n")
        # parse command line arguments
        command_parser()

        launch_flip_at()
