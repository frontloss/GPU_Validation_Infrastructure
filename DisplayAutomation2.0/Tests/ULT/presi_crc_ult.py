###############################################################################
# \ref      presi_crc_ult.py
# \brief    presi_crc_ult.py tests presilicon API for CRC verification using hw_register state
# \author   Beeresh Gopal, agolwala
###############################################################################

import logging, os, sys, traceback
import win32api, win32con

from Libs.Core.display_config.display_config import *
from Libs.Core.system_utility import *
from Libs.Feature.presi import presi_crc
from Libs.Core.flip import *
from Libs.Core.test_env import test_context
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.window_helper import *
from Libs.Core.system_utility import *
from Libs.Feature.display_engine.de_base.display_base import *



def capture_crc_ult(target_id, presi_model_obj):
    test_modes = []
    platform = None
    system_utility = SystemUtility()
    machine_info = SystemInfo()
    gfx_display_hwinfo = machine_info.get_gfx_display_hardwareinfo()
    for i in range(len(gfx_display_hwinfo)):
        platform = str(gfx_display_hwinfo[i].DisplayAdapterName).upper()
        break
    port_name = None
    enumerated_displays = disp_config.get_enumerated_display_info()
    for eachDisplay in range(enumerated_displays.Count):
        if enumerated_displays.ConnectedDisplays[eachDisplay].TargetID == target_id:
            port_name = (CONNECTOR_PORT_TYPE(enumerated_displays.ConnectedDisplays[eachDisplay].ConnectorNPortType)).name
            break
    if port_name is None:
        logging.error("Port name is None")
        return None, None

    mode = disp_config.get_current_mode(target_id = target_id)
    if mode is None:
        logging.error("Failed to fetch current mode for %s" % (port_name))
        return None, None

    script_dir = (os.path.dirname(os.path.abspath(__file__)))
    output_file = '%s_display_crc_sw.crc' % (platform)
    output_file_path = os.path.join(script_dir, output_file)
    fd = open(output_file_path, 'w')

    port2pipe_map = get_port_to_pipe()
    pipe = port2pipe_map[port_name]
    presi_crc.control_crc(True, port_name[-1:], pipe[-1:], False, presi_env=presi_model_obj.model_type)

    mode_name = "%dx%d_%dbpp@%dhz_%s" % (mode.HzRes, mode.VtRes,
                                         mode.BPP,
                                         mode.refreshRate,
                                         mode.rotation)

    # mpo_obj = MPO()
    # presi_crc.perform_dft_flip(target_id, mpo_obj)
    result = presi_crc.read_crc(port_name[-1:], presi_model_obj, pipe_plane_suffix=pipe[-1:])
    time.sleep(20)
    line = "mode: %s, port_crc: %s, pipe_crc:%s\n" % (mode_name, result['port_crc'], result['pipe_crc'])
    fd.write(line)
    time.sleep(5)
    fd.close()

    presi_crc.dump_crc_debug_registers()

    presi_crc.control_crc(False, port_name[-1:], pipe[-1:], False, presi_env=presi_model_obj.model_type)
    # presi_crc.stop_dft_flip(mpo_obj)
    return port_name, mode_name


def compare_crc_ult(target_id, mode_name, presi_model_obj):
    platform = None
    system_utility = SystemUtility()
    machine_info = SystemInfo()
    gfx_display_hwinfo = machine_info.get_gfx_display_hardwareinfo()
    for i in range(len(gfx_display_hwinfo)):
        platform = str(gfx_display_hwinfo[i].DisplayAdapterName).upper()
        break
    script_dir = (os.path.dirname(os.path.abspath(__file__)))
    output_file = '%s_display_crc_sw.crc' % (platform)
    output_file_path = os.path.join(script_dir, output_file)
    port_name = None
    enumerated_displays = disp_config.get_enumerated_display_info()
    for eachDisplay in range(enumerated_displays.Count):
        if enumerated_displays.ConnectedDisplays[eachDisplay].TargetID == target_id:
            port_name = (CONNECTOR_PORT_TYPE(enumerated_displays.ConnectedDisplays[eachDisplay].ConnectorNPortType)).name
            break
    if port_name is None:
        return None, None

    port2pipe_map = get_port_to_pipe()
    pipe_name = port2pipe_map[port_name]
    presi_crc.control_crc(True, port_name[-1:], pipe_name[-1:], False, presi_env=presi_model_obj.model_type)

    # mpo_obj = MPO()
    # presi_crc.perform_dft_flip(target_id, mpo_obj)

    crc_value = presi_crc.read_crc(port_name[-1:], presi_model_obj, pipe_name[-1:])
    time.sleep(20)
    fd = open(output_file_path, 'r')
    lines = fd.read()
    fd.close()

    found = False
    line = "%s, %s\n" % (mode_name, crc_value)
    if line in lines:
        found = True

    presi_crc.control_crc(False, port_name[-1:], pipe_name[-1:], False, presi_env=presi_model_obj.model_type)
    # presi_crc.stop_dft_flip(mpo_obj)
    return found


if __name__ == '__main__':
    TestEnvironment.initialize()
    model = presi_crc.PresiModelMeta()
    sys_utility = SystemUtility()
    disp_config = DisplayConfiguration()
    model.model_type = "FULSIM"
    model.ipaddress = "10.223.26.123"
    model.port_no = 4321

    log_folder_path = test_context.LOG_FOLDER
    log_file_name = "presi_crc_ult.log"
    log_file = os.path.join(log_folder_path, log_file_name)

    if not os.path.exists(log_folder_path):
        os.makedirs(log_folder_path)

    FORMAT = '%(asctime)-15s %(levelname)s  [%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s'
    logging.basicConfig(filename=log_file, stream=sys.stderr, level="DEBUG", format=FORMAT, filemode='w')

    try:
        win32api.SetCursorPos((100, 100))
        enumerated_displays = disp_config.get_enumerated_display_info()

        targetid = enumerated_displays.ConnectedDisplays[0].TargetID
        port_name, mode_name = capture_crc_ult(targetid, model)
        result = compare_crc_ult(targetid, mode_name, model)
        logging.info("CRC compare result = %s for port %s and mode=%s" % (result, port_name, mode_name))


    except Exception as e:
        print("Exception in user code: %s" % (e))
        print('-' * 60)
        traceback.print_exc(file=sys.stdout)
        print('-' * 60)
        show_desktop_bg_only(False)
