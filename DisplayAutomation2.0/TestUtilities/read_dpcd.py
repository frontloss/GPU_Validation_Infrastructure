###############################################################################
# Script Name         : read_dpcd
# Script Owner        : Vinod D S, Reeju Srivastava, Praneeth Kumar Bhadriraju
# Description         : Helper functions to read DPCD registers for eDP & DP
###############################################################################

import sys

from Libs.Core import driver_escape
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE
from Libs.Core.test_env import test_environment
from Libs.Core.wrapper import dll_logger

_BIT_OFFSET_NAME = ['B7', 'B6', 'B5', 'B4', 'B3', 'B2', 'B1', 'B0']
_VALID_DISPLAYS = ['EDP', 'DP']
_EDP_PORT_NAME = "DP_A"


def read_dpcd_value(dpcd_offset: int, disp_target_id: int, display_name: str) -> None:
    try:
        flag, reg_value = driver_escape.read_dpcd(disp_target_id, dpcd_offset)
        if flag is True:
            output = [i for i in format(reg_value[0], "08b")]

            print("\nDPCD Value for Display: {0} with Offset: {1} = 0x{2}({3})".format(
                display_name, hex(dpcd_offset), format(reg_value[0], '02x').upper(), reg_value[0]))
            print(" : ".join(map(lambda x: '{}'.format(x), _BIT_OFFSET_NAME)))
            print("  : ".join(map(lambda x: '{}'.format(x), output)))
        else:
            print("Unable to read DPCD Data")
    except Exception as ex:
        print("Exception: {}".format(ex))


def get_port_targetid_map(gfx_index: str = 'gfx_0') -> dict:
    enumerated_displays = DisplayConfiguration().get_enumerated_display_info()
    print(f"Requested gfx index - {gfx_index}\nEnumerated displays - \n{enumerated_displays.to_string()}")
    target_id_mapping = dict()

    for display_index in range(enumerated_displays.Count):
        display = enumerated_displays.ConnectedDisplays[display_index]
        if gfx_index == display.DisplayAndAdapterInfo.adapterInfo.gfxIndex:
            target_id_mapping[CONNECTOR_PORT_TYPE(display.ConnectorNPortType).name] = int(display.TargetID)

    return target_id_mapping


if __name__ == '__main__':
    test_environment.TestEnvironment.load_dll_module()
    if len(sys.argv) == 3:
        dll_logger.initialize(True)
        display = sys.argv[1].upper()
        offset = 0

        if display not in _VALID_DISPLAYS:
            print("Invalid Display Name")
        try:
            offset = int(sys.argv[2], 16)
        except ValueError:
            print("Invalid Offset value")

        port_targetid_dict = get_port_targetid_map()

        if display == "EDP":
            if _EDP_PORT_NAME not in port_targetid_dict.keys():
                print("Display is not enumerated")
            target_id = port_targetid_dict[_EDP_PORT_NAME]
            read_dpcd_value(offset, target_id, display)
        else:
            for port, target_id in port_targetid_dict.items():
                if (port is not _EDP_PORT_NAME) and ("DP" in port):
                    read_dpcd_value(offset, target_id, port)
        dll_logger.cleanup()
    else:
        print("Invalid arguments. Refer below for using the functionality")
        print("Usage: read_dpcd.py <Display_name> <offset_value>")
