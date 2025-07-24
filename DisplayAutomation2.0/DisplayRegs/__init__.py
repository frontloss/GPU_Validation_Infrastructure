########################################################################################################################
# @file         __init__.py
# @brief        Contains API to expose DisplayRegs interface
#
# @author       Rohit Kumar
########################################################################################################################

from DisplayRegs.DisplayRegsInterface import DisplayRegsService
from DisplayRegs.Gen11 import Gen11DisplayRegsInterface
from DisplayRegs.Gen11p5 import Gen11p5DisplayRegsInterface
from DisplayRegs.Gen12 import Gen12DisplayRegsInterface
from DisplayRegs.Gen13 import Gen13DisplayRegsInterface
from DisplayRegs.Gen14 import Gen14DisplayRegsInterface
from DisplayRegs.Gen15 import Gen15DisplayRegsInterface


def get_interface(platform: str, gfx_index: str) -> DisplayRegsService:
    assert platform
    assert gfx_index

    if platform in ['ICLLP', 'JSL', 'EHL']:
        return Gen11DisplayRegsInterface.Gen11DisplayRegsService(platform, gfx_index)

    if platform in ['LKF1']:
        return Gen11p5DisplayRegsInterface.Gen11p5DisplayRegsService(platform, gfx_index)

    if platform in ['TGL', 'DG1', 'RKL', 'ADLS']:
        return Gen12DisplayRegsInterface.Gen12DisplayRegsService(platform, gfx_index)

    if platform in ['DG2', 'ADLP']:
        return Gen13DisplayRegsInterface.Gen13DisplayRegsService(platform, gfx_index)

    if platform in ['DG3', 'MTL', 'ELG']:
        return Gen14DisplayRegsInterface.Gen14DisplayRegsService(platform, gfx_index)

    if platform in ['LNL', 'PTL', 'CLS', 'NVL', 'CLS']:
        return Gen15DisplayRegsInterface.Gen15DisplayRegsService(platform, gfx_index)

    return Gen11DisplayRegsInterface.Gen11DisplayRegsService(platform, gfx_index)
