######################################################################################
# @file         common.py
# @addtogroup   PyLibs_DisplayPower
# @brief        Contains common structure definitions for powerwell modules
#
# @author       Rohit Kumar
######################################################################################

import ctypes


##
# @brief        DisplayPowerWellMask is the common structure used to indicate the overall powerwell status.
# @description  This structure is used as part of the powerwell union defined in each gen module. Each gen module can
#               decide what power wells to be enabled and can assign power well values accordingly.
class DisplayPowerWellMask(ctypes.LittleEndianStructure):
    _fields_ = [
        ("PowerwellPG1", ctypes.c_uint64, 1),
        ("PowerwellPG2", ctypes.c_uint64, 1),
        ("PowerwellPG3", ctypes.c_uint64, 1),
        ("PowerwellPG4", ctypes.c_uint64, 1),
        ("PowerwellPG5", ctypes.c_uint64, 1),
        ("PowerwellAuxAIo", ctypes.c_uint64, 1),
        ("PowerwellAuxBIo", ctypes.c_uint64, 1),
        ("PowerwellAuxCIo", ctypes.c_uint64, 1),
        ("PowerwellAuxDIo", ctypes.c_uint64, 1),
        ("PowerwellAuxEIo", ctypes.c_uint64, 1),
        ("PowerwellAuxFIo", ctypes.c_uint64, 1),
        ("PowerwellAuxGIo", ctypes.c_uint64, 1),
        ("PowerwellAuxHIo", ctypes.c_uint64, 1),
        ("PowerwellAuxIIo", ctypes.c_uint64, 1),
        ("PowerwellAuxTBT1Io", ctypes.c_uint64, 1),
        ("PowerwellAuxTBT2Io", ctypes.c_uint64, 1),
        ("PowerwellAuxTBT3Io", ctypes.c_uint64, 1),
        ("PowerwellAuxTBT4Io", ctypes.c_uint64, 1),
        ("PowerwellAuxTBT5Io", ctypes.c_uint64, 1),
        ("PowerwellAuxTBT6Io", ctypes.c_uint64, 1),
        ("PowerwellDdiAIo", ctypes.c_uint64, 1),
        ("PowerwellDdiBIo", ctypes.c_uint64, 1),
        ("PowerwellDdiCIo", ctypes.c_uint64, 1),
        ("PowerwellDdiDIo", ctypes.c_uint64, 1),
        ("PowerwellDdiEIo", ctypes.c_uint64, 1),
        ("PowerwellDdiFIo", ctypes.c_uint64, 1),
        ("PowerwellDdiGIo", ctypes.c_uint64, 1),
        ("PowerwellDdiHIo", ctypes.c_uint64, 1),
        ("PowerwellDdiIIo", ctypes.c_uint64, 1),
        ("PowerwellPGA", ctypes.c_uint64, 1),
        ("PowerwellPGB", ctypes.c_uint64, 1),
        ("PowerwellPGC", ctypes.c_uint64, 1),
        ("PowerwellPGD", ctypes.c_uint64, 1),
        ("Reserved_1", ctypes.c_uint64, 31)
    ]
