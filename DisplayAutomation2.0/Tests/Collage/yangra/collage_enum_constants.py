#######################################################################################################################
# @file         collage_enum_constants.py
# @brief        This file contains all the enums and constants required for collage test cases.
#
# @author       Praburaj Krishnan
#######################################################################################################################

from enum import Enum

DELAY_5_SECONDS = 5.0

MAX_PIPE_INFO = {
    3: ['icl', 'icllp', 'rkl', 'lnl'],
    4: ['lkf1', 'tgl', 'ryf', 'dg1', 'dg2', 'adls', 'adlp', 'mtl', 'elg']
}


##
# @brief    Plug/Unplug Actions enum
class Action(Enum):
    UNPLUG = 0
    HOT_PLUG = 1
    HOT_PLUG_ALL = 2
    UNPLUG_ALL = 3
