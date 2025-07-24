import sys

from Libs.Core.hw_emu.she_emulator import SheUtility
from Libs.Core.display_config.adapter_info_struct import GfxAdapterInfo


if __name__ == '__main__':
    print('USAGE: she_emulator_ult.py <display_port> <operation (plug/unplug/msa/crc)>\n'
          'E.g: she_emulator_ult.py DP_E plug')
    display = str(sys.argv[1])
    operation = str(sys.argv[2])
    gfx_adapter_info = GfxAdapterInfo()
    gfx_adapter_info.gfxIndex = 'gfx_0'

    she_obj = SheUtility()
    she_obj.initialize()
    #she_obj.com_ports = ['COM6']
    #she_obj.connected_device_type = ["DP", "DP", "DP"]
    if operation.lower() == 'plug':
        ret = she_obj.plug(gfx_adapter_info, display, '', '', '')
        print(f'hotplug returned {ret}')
    elif operation.lower() == 'unplug':
        ret = she_obj.unplug(gfx_adapter_info, display, '')
        print(f'hotunplug returned {ret}')
    elif operation.lower() == 'msa':
        status, MSA_values = she_obj.read_MSA_parameters_from_emulator(she_obj.display_to_emulator_port_map[display][0])
        print(MSA_values)
    elif operation.lower() == 'crc':
        status, RGBValues = she_obj.read_CRC_values_from_emulator(
            she_obj.display_to_emulator_port_map[display][0], 10)
        print(f'status= {status}, RGBValues= {RGBValues}')
    else:
        print("invalid operation passed")
