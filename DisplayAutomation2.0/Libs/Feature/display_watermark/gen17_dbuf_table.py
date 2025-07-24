######################################################################################
# @file         gen17_dbuf_table.py
# @addtogroup   PyLibs_DisplayWatermark
# @brief        Gen17 DBuf distribution table
# @author       Prateek Joshi
######################################################################################

from Libs.Feature.display_watermark.watermark_utils import DBUF_SLICE_END, DBUF_FULL_BLOCK_END, DBUF_SLICE_END_CLS, \
    DBUF_FULL_BLOCK_END_CLS


##
# DBuf distribution across different slices for Gen17
# NVL BSpec: https://gfxspecs.intel.com/Predator/Home/Index/68907

# Gen17 DBuf distribution dictionary
# Key = Bitwise Enabled Pipes, Considering Pipe A, Pipe B , Pipe C and Pipe D as bit 0, 1, 2 and 3 respectively.
# Values = Allocation start and end, DBuf slices enabled, MBus joined mode


##
# NVL DBuf distribution dictionary
gen17_nvl_dbuf_distribution = {

    ##
    # KEY ==> BIT_PipeD, BIT_PipeC, BIT_PipeB, BIT_PipeA

    # Pipe A
    0b0001: {
        'allocation': (                                 # DBuf allocation boundaries across different pipes
            (0, DBUF_FULL_BLOCK_END),                   # Pipe A DBuf boundaries
            (0, 0),                                     # Pipe B DBuf boundaries
            (0, 0),                                     # Pipe C DBuf boundaries
            (0, 0),                                     # Pipe D DBuf boundaries
        ),
        'slices_enabled': ['S0', 'S1', 'S2', 'S3'],     # DBuf slices enabled
        'mbus_joined': True                             # MBus joined mose status
    },

    # Pipe B
    0b0010: {
        'allocation': (
            (0, 0),
            (0, DBUF_FULL_BLOCK_END),
            (0, 0),
            (0, 0),
        ),
        'slices_enabled': ['S0', 'S1', 'S2', 'S3'],
        'mbus_joined': True
    },

    # Pipe A + Pipe B
    0b0011: {
        'allocation': (
            (0, DBUF_SLICE_END),
            (0, DBUF_SLICE_END),
            (0, 0),
            (0, 0),
        ),
        'slices_enabled': ['S0', 'S1', 'S2', 'S3'],
        'mbus_joined': False
    },

    # Pipe C
    0b0100: {
        'allocation': (
            (0, 0),
            (0, 0),
            (0, DBUF_SLICE_END),
            (0, 0),
        ),
        'slices_enabled': ['S2', 'S3'],
        'mbus_joined': False
    },

    # Pipe A + Pipe C
    0b0101: {
        'allocation': (
            (0, DBUF_SLICE_END),
            (0, 0),
            (0, DBUF_SLICE_END),
            (0, 0),
        ),
        'slices_enabled': ['S0', 'S1', 'S2', 'S3'],
        'mbus_joined': False
    },

    # Pipe B + Pipe C
    0b0110: {
        'allocation': (
            (0, 0),
            (0, DBUF_SLICE_END),
            (0, DBUF_SLICE_END),
            (0, 0),
        ),
        'slices_enabled': ['S2', 'S3'],
        'mbus_joined': False
    },

    # Pipe A + Pipe B + Pipe C
    0b0111: {
        'allocation': (
            (0, DBUF_SLICE_END),
            (0, DBUF_SLICE_END),
            (0, DBUF_SLICE_END),
            (0, 0),
        ),
        'slices_enabled': ['S0', 'S1', 'S2', 'S3'],
        'mbus_joined': False
    },

    # Pipe D
    0b1000: {
        'allocation': (
            (0, 0),
            (0, 0),
            (0, 0),
            (0, DBUF_SLICE_END),
        ),
        'slices_enabled': ['S0', 'S1'],
        'mbus_joined': False
    },

    # Pipe A + Pipe D
    0b1001: {
        'allocation': (
            (0, DBUF_SLICE_END),
            (0, 0),
            (0, 0),
            (0, DBUF_SLICE_END),
        ),
        'slices_enabled': ['S0', 'S1'],
        'mbus_joined': False
    },

    # Pipe B + Pipe D
    0b1010: {
        'allocation': (
            (0, 0),
            (0, DBUF_SLICE_END),
            (0, 0),
            (0, DBUF_SLICE_END),
        ),
        'slices_enabled': ['S0', 'S1', 'S2', 'S3'],
        'mbus_joined': False
    },

    # Pipe A + Pipe B + Pipe D
    0b1011: {
        'allocation': (
            (0, DBUF_SLICE_END),
            (0, DBUF_SLICE_END),
            (0, 0),
            (0, DBUF_SLICE_END),
        ),
        'slices_enabled': ['S0', 'S1', 'S2', 'S3'],
        'mbus_joined': False
    },

    # Pipe C + Pipe D
    0b1100: {
        'allocation': (
            (0, 0),
            (0, 0),
            (0, DBUF_SLICE_END),
            (0, DBUF_SLICE_END),
        ),
        'slices_enabled': ['S0', 'S1', 'S2', 'S3'],
        'mbus_joined': False
    },

    # Pipe A + Pipe C + Pipe D
    0b1101: {
        'allocation': (
            (0, DBUF_SLICE_END),
            (0, 0),
            (0, DBUF_SLICE_END),
            (0, DBUF_SLICE_END),
        ),
        'slices_enabled': ['S0', 'S1', 'S2', 'S3'],
        'mbus_joined': False
    },

    # Pipe B + Pipe C + Pipe D
    0b1110: {
        'allocation': (
            (0, 0),
            (0, DBUF_SLICE_END),
            (0, DBUF_SLICE_END),
            (0, DBUF_SLICE_END),
        ),
        'slices_enabled': ['S0', 'S1', 'S2', 'S3'],
        'mbus_joined': False
    },

    # Pipe A + Pipe B + Pipe C + Pipe D
    0b1111: {
        'allocation': (
            (0, DBUF_SLICE_END),
            (0, DBUF_SLICE_END),
            (0, DBUF_SLICE_END),
            (0, DBUF_SLICE_END),
        ),
        'slices_enabled': ['S0', 'S1', 'S2', 'S3'],
        'mbus_joined': False
    },
}

##
# CLS DBuf distribution dictionary
gen17_cls_dbuf_distribution = {

    ##
    # KEY ==> BIT_PipeD, BIT_PipeC, BIT_PipeB, BIT_PipeA

    # Pipe A
    0b0001: {
        'allocation': (                                 # DBuf allocation boundaries across different pipes
            (0, DBUF_FULL_BLOCK_END_CLS),                   # Pipe A DBuf boundaries
            (0, 0),                                     # Pipe B DBuf boundaries
            (0, 0),                                     # Pipe C DBuf boundaries
            (0, 0),                                     # Pipe D DBuf boundaries
        ),
        'slices_enabled': ['S0', 'S1', 'S2', 'S3'],     # DBuf slices enabled
        'mbus_joined': True                             # MBus joined mose status
    },

    # Pipe B
    0b0010: {
        'allocation': (
            (0, 0),
            (0, DBUF_FULL_BLOCK_END_CLS),
            (0, 0),
            (0, 0),
        ),
        'slices_enabled': ['S0', 'S1', 'S2', 'S3'],
        'mbus_joined': True
    },

    # Pipe A + Pipe B
    0b0011: {
        'allocation': (
            (0, DBUF_SLICE_END_CLS),
            (0, DBUF_SLICE_END_CLS),
            (0, 0),
            (0, 0),
        ),
        'slices_enabled': ['S0', 'S1', 'S2', 'S3'],
        'mbus_joined': False
    },

    # Pipe C
    0b0100: {
        'allocation': (
            (0, 0),
            (0, 0),
            (0, DBUF_SLICE_END_CLS),
            (0, 0),
        ),
        'slices_enabled': ['S2', 'S3'],
        'mbus_joined': False
    },

    # Pipe A + Pipe C
    0b0101: {
        'allocation': (
            (0, DBUF_SLICE_END_CLS),
            (0, 0),
            (0, DBUF_SLICE_END_CLS),
            (0, 0),
        ),
        'slices_enabled': ['S0', 'S1', 'S2', 'S3'],
        'mbus_joined': False
    },

    # Pipe B + Pipe C
    0b0110: {
        'allocation': (
            (0, 0),
            (0, DBUF_SLICE_END_CLS),
            (0, DBUF_SLICE_END_CLS),
            (0, 0),
        ),
        'slices_enabled': ['S2', 'S3'],
        'mbus_joined': False
    },

    # Pipe A + Pipe B + Pipe C
    0b0111: {
        'allocation': (
            (0, DBUF_SLICE_END_CLS),
            (0, DBUF_SLICE_END_CLS),
            (0, DBUF_SLICE_END_CLS),
            (0, 0),
        ),
        'slices_enabled': ['S0', 'S1', 'S2', 'S3'],
        'mbus_joined': False
    },

    # Pipe D
    0b1000: {
        'allocation': (
            (0, 0),
            (0, 0),
            (0, 0),
            (0, DBUF_SLICE_END_CLS),
        ),
        'slices_enabled': ['S0', 'S1'],
        'mbus_joined': False
    },

    # Pipe A + Pipe D
    0b1001: {
        'allocation': (
            (0, DBUF_SLICE_END_CLS),
            (0, 0),
            (0, 0),
            (0, DBUF_SLICE_END_CLS),
        ),
        'slices_enabled': ['S0', 'S1'],
        'mbus_joined': False
    },

    # Pipe B + Pipe D
    0b1010: {
        'allocation': (
            (0, 0),
            (0, DBUF_SLICE_END_CLS),
            (0, 0),
            (0, DBUF_SLICE_END_CLS),
        ),
        'slices_enabled': ['S0', 'S1', 'S2', 'S3'],
        'mbus_joined': False
    },

    # Pipe A + Pipe B + Pipe D
    0b1011: {
        'allocation': (
            (0, DBUF_SLICE_END_CLS),
            (0, DBUF_SLICE_END_CLS),
            (0, 0),
            (0, DBUF_SLICE_END_CLS),
        ),
        'slices_enabled': ['S0', 'S1', 'S2', 'S3'],
        'mbus_joined': False
    },

    # Pipe C + Pipe D
    0b1100: {
        'allocation': (
            (0, 0),
            (0, 0),
            (0, DBUF_SLICE_END_CLS),
            (0, DBUF_SLICE_END_CLS),
        ),
        'slices_enabled': ['S0', 'S1', 'S2', 'S3'],
        'mbus_joined': False
    },

    # Pipe A + Pipe C + Pipe D
    0b1101: {
        'allocation': (
            (0, DBUF_SLICE_END_CLS),
            (0, 0),
            (0, DBUF_SLICE_END_CLS),
            (0, DBUF_SLICE_END_CLS),
        ),
        'slices_enabled': ['S0', 'S1', 'S2', 'S3'],
        'mbus_joined': False
    },

    # Pipe B + Pipe C + Pipe D
    0b1110: {
        'allocation': (
            (0, 0),
            (0, DBUF_SLICE_END_CLS),
            (0, DBUF_SLICE_END_CLS),
            (0, DBUF_SLICE_END_CLS),
        ),
        'slices_enabled': ['S0', 'S1', 'S2', 'S3'],
        'mbus_joined': False
    },

    # Pipe A + Pipe B + Pipe C + Pipe D
    0b1111: {
        'allocation': (
            (0, DBUF_SLICE_END_CLS),
            (0, DBUF_SLICE_END_CLS),
            (0, DBUF_SLICE_END_CLS),
            (0, DBUF_SLICE_END_CLS),
        ),
        'slices_enabled': ['S0', 'S1', 'S2', 'S3'],
        'mbus_joined': False
    },
}