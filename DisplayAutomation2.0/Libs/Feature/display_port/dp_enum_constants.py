######################################################################################################################
# @file         dp_enum_constants.py
# @brief        Contains All the Constants and Enum that will be used across different test cases and verification
#
# @author       Praburaj Krishnan
#######################################################################################################################

from enum import Enum

# For DP SST considering 8/10b encoding overhead the bandwidth efficiency is 80%
DP_DATA_BW_EFFICIENCY_SST_PER_100 = 80.00

# For DP SST considering 8/10 encoding Overhead + FEC overhead of 2.4% the efficiency comes to 78.08%
DP_DATA_BW_EFFICIENCY_SST_FEC_PER_100 = 78.08

# For DP SST considering 8/10 encoding Overhead + FEC overhead of 2.4% and in DSC case we should consider EOC overhead.
# Hence, the efficiency comes to 77.78%
DP_DATA_BW_EFFICIENCY_SST_DSC_PER_100 = 77.78

# For DP MST considering 8/10b encoding overhead + MST overhead of 1.562% the efficiency comes to 78.75%
DP_DATA_BW_EFFICIENCY_MST_PER_100 = 78.75

# For DP MST considering 8/10b encoding overhead + MST overhead of 1.562% + FEC overhead of 2.4% the efficiency comes
# to 76.86%
DP_DATA_BW_EFFICIENCY_MST_FEC_PER_100 = 76.86

# For DP MST considering 8/10b encoding overhead + MST overhead of 1.562% + FEC overhead of 2.4% + in DSC case we should
# consider EOC overhead the efficiency comes to 76.56%
DP_DATA_BW_EFFICIENCY_MST_DSC_PER_100 = 76.56

# DP 2.0 uses 128/132b encoding. Hence, the efficiency is 96.71%
DP_DATA_BW_EFFICIENCY_128B_132B_PER_100 = 96.71

# Available MTP time slot for 8b/10b encoding
AVAILABLE_MTP_TIMESLOTS_8B_10B = 63

# Available MTP time slot for 128b/132b encoding
AVAILABLE_MTP_TIMESLOTS_128B_132B = 64


##
# @brief        Enum type that holds different types of virtual dp peer device that can be enumerated
class VirtualDisplayportPeerDevice(Enum):
    VIRTUAL_DP_PEER_DEVICE_NOT_SUPPORTED = 0
    VIRTUAL_DP_SINK_PEER_DEVICE = 1
    VIRTUAL_DP2DP_PEER_DEVICE = 2
    VIRTUAL_DP2PROTOCOL_CONVERTER_PEER_DEVICE = 3
