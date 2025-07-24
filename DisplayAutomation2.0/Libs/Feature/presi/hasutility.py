###################################################################################################################
# @file         hasutility.py
# @brief        Utility to do plane-processing, hotplug(HDMI/DP/TBT/TypeC) .
#               This communicate with HAS for required functionality required it
# @author       Ap, Kamal
##########################################################################################################################
import ctypes
import socket
from enum import IntEnum


##
# @brief        Contains HAS HDR Requirement
class HAS_HDR(ctypes.Structure):
    _fields_ = [("msg_type", ctypes.c_uint),
                ("trans_id", ctypes.c_uint),
                ("size", ctypes.c_uint)]


##
# @brief        Contains HAS Inner Var Requirement
class HAS_INNER_VAR_REQ(ctypes.Structure):
    _fields_ = [("has_hdr", HAS_HDR),
                ("write", ctypes.c_uint32, 1),
                ("non_dword", ctypes.c_uint32, 16),
                ("reserved", ctypes.c_uint32, 15),
                ("id", ctypes.c_uint32),
                ("data", ctypes.c_uint32)]


##
# @brief        Contains HAS diplay port
class HasDisplayPort(IntEnum):
    DDI_A = 0
    DDI_B = 1
    DDI_C = 2
    DDI_D = 3
    DDI_E = 4
    DDI_F = 5


##
# @brief        Contains has-hotplug types
class HasHotplugType(IntEnum):
    HDMI_DP_SHORT_PULSE = 4
    HDMI_DP_LONG_PULSE = 5
    TBT_SHORT_PULSE = 6
    TBT_LONG_PULSE = 7
    TC_SHORT_PULSE = 8
    TC_LONG_PULSE = 9


##
# @brief        HAS UTILITY Class
class HAS_UTILITY():

    ##
    # @brief        constructor
    # @param[in]    ip
    # @param[in]    port
    def __init__(self, ip, port):
        self.HAS_INNER_VAR_REQ_TYPE = 18
        self.ip = ip
        self.port = port

    ##
    # @brief    Issue HAS-Plane Processing command
    # @return   None
    def has_do_plane_processing(self):
        self.inner_var_set(3, 1)

    ##
    # @brief        has-command
    # @param[in]    id
    # @param[in]    data
    # @return       None
    def inner_var_set(self, id, data):
        inner_var_req = HAS_INNER_VAR_REQ((self.HAS_INNER_VAR_REQ_TYPE, 0,
                                           ctypes.sizeof(HAS_INNER_VAR_REQ) - ctypes.sizeof(HAS_HDR)),
                                          1, 0, 0, id, data)
        self.skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.skt.connect((self.ip, self.port))
        self.skt.sendall(inner_var_req)
        self.skt.close()

    ##
    # @brief     Issue Hotplug interrupt on specified port
    # @param[in] port : type HasDisplayPort
    # @param[in] hotplug_type : type HasHotplugType
    # @return    None
    def has_do_hot_plug(self, port, hotplug_type):
        self.inner_var_set(port, hotplug_type)


if __name__ == '__main__':
    h = HAS_UTILITY("127.0.0.1", 5325)
    h.has_do_plane_processing()
    h.has_do_hot_plug(HasDisplayPort.DDI_B, HasHotplugType.HDMI_DP_SHORT_PULSE)
