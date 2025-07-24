######################################################################################
# @file     dpcd_model_data_struct.py
# @brief    Exposes Structures related to DPCD Model Data
# @author   Sri Sumanth Geesala
######################################################################################

import ctypes
from ctypes import c_uint, c_ulong, c_ubyte

DPCD_MAX_DPCD_VALUES = 8
DPCD_MAX_DPCD_SETS = 2
DPCD_MAX_TRANSACTIONS = 15


##
# @brief        DPCD Value List class
class DPCDValueList(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('ulStartingOffset', c_ulong),
        ('ucLength', c_ubyte),
        ('ucValues', c_ubyte * DPCD_MAX_DPCD_VALUES),
    ]


##
# @brief        DPCD Transaction class
class DPCDTransaction(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('ucNumInputDpcdSets', c_ubyte),
        ('stInputDpcdSets', DPCDValueList * DPCD_MAX_DPCD_SETS),
        ('ucNumResponseDpcdSets', c_ubyte),
        ('stResponseDpcdSets', DPCDValueList * DPCD_MAX_DPCD_SETS)
    ]


##
# @brief        DPCD Model Data class
class DPCDModelData(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('ucTransactionCount', c_ubyte),
        ('stDPCDTransactions', DPCDTransaction * DPCD_MAX_TRANSACTIONS),
        ('ulTriggerOffset', c_ulong),
        ('stDefaultResponseDpcdSet', DPCDValueList)
    ]


##
# @brief        DPDPCD Model Data class
class DPDPCDModelData(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('uiPortNum', c_uint),
        ('eTopologyType', c_uint),
        ('stDPCDModelData', DPCDModelData)
    ]
