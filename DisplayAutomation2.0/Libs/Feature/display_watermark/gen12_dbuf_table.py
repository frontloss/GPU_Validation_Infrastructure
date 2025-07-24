######################################################################################
# @file         gen12_dbuf_table.py
# @addtogroup   PyLibs_DisplayWatermark
# @brief        Gen12 DBuf distribution table
# @author       Suraj Gaikwad, Bhargav Adigarla
######################################################################################


##
# DBuf distribution across different slices for Gen12
# BSpec: https://gfxspecs.intel.com/Predator/Home/Index/49255
#
# There are two display buffers DBUF_S1 and DBUF_S2.
# +----------------+--------------+------------+
# | Display Buffer | Buffer Start | Buffer End |
# +----------------+--------------+------------+
# | DBUF_S1        | 0            | 1023       |
# +----------------+--------------+------------+
# | DBUF_S2        | 1024         | 2047       |
# +----------------+--------------+------------+

DBUF_S1_END = 1023
DBUF_S2_START = 1024
DBUF_FULL_BLOCK_END = 2047

# The table ensures that pipes are using the closest DBUF when there are multiple pipes enabled.
# Pipe and DBUF ordering: PipeD - DBUF_S2 - PipeC - PipeA - DBUF_S1 - PipeB
# When a pipe is allowed to allocate from 2 DBUFs, a plane on that pipe may use allocation that straddles the 2 DBUFs.

# +----------------+-----------+-----------+-----------+-----------+
# | Pipes with     | DBUF for  | DBUF for  | DBUF for  | DBUF for  |
# | Enabled Planes | PipeA     | PipeB     | PipeC     | PipeD     |
# +----------------+-----------+-----------+-----------+-----------+
# | None or VGA    | -         | -         | -         | -         |
# +----------------+-----------+-----------+-----------+-----------+
# | A              | S1 + S2   | -         | -         | -         |
# +----------------+-----------+-----------+-----------+-----------+
# | B              | -         | S1 + S2   | -         | -         |
# +----------------+-----------+-----------+-----------+-----------+
# | A + B          | S2        | S1        | -         | -         |
# +----------------+-----------+-----------+-----------+-----------+
# | C              | -         | -         | S1 + S2   | -         |
# +----------------+-----------+-----------+-----------+-----------+
# | A + C          | S1        | -         | S2        | -         |
# +----------------+-----------+-----------+-----------+-----------+
# | B + C          | -         | S1        | S2        | -         |
# +----------------+-----------+-----------+-----------+-----------+
# | A + B + C      | S1        | S1        | S2        | -         |
# +----------------+-----------+-----------+-----------+-----------+
# | D              | -         | -         | -         | S1 + S2   |
# +----------------+-----------+-----------+-----------+-----------+
# | A + D          | S1        | -         | -         | S2        |
# +----------------+-----------+-----------+-----------+-----------+
# | B + D          | -         | S1        | -         | S2        |
# +----------------+-----------+-----------+-----------+-----------+
# | A + B + D      | S1        | S1        | -         | S2        |
# +----------------+-----------+-----------+-----------+-----------+
# | C + D          | -         | -         | S1        | S2        |
# +----------------+-----------+-----------+-----------+-----------+
# | A + C + D      | S1        | -         | S2        | S2        |
# +----------------+-----------+-----------+-----------+-----------+
# | B + C + D      | -         | S1        | S2        | S2        |
# +----------------+-----------+-----------+-----------+-----------+
# | A + B + C + D  | S1        | S1        | S2        | S2        |
# +----------------+-----------+-----------+-----------+-----------+

# Gen12 DBuf distribution dictionary based on BSpec table
# Key = Bitwise Enabled Pipes, Considering Pipe A, Pipe B , Pipe C and Pipe D as bit 0, 1, 2 and 3 respectively.
# Values = Tuple containing valid start and end of DBUFs for all the Pipes

gen12_dbuf_distribution = {

    ##
    # KEY ==> BIT_PipeD, BIT_PipeC, BIT_PipeB, BIT_PipeA

    # Pipe A
    0b0001: (
        (0, DBUF_FULL_BLOCK_END),  # Pipe A DBuf boundaries
        (0, 0),  # Pipe B DBuf boundaries
        (0, 0),  # Pipe C DBuf boundaries
        (0, 0),  # Pipe D DBuf boundaries
    ),

    # Pipe B
    0b0010: (
        (0, 0),
        (0, DBUF_FULL_BLOCK_END),
        (0, 0),
        (0, 0),
    ),

    # Pipe A + Pipe B
    0b0011: (
        (DBUF_S2_START, DBUF_FULL_BLOCK_END),
        (0, DBUF_S1_END),
        (0, 0),
        (0, 0),
    ),

    # Pipe C
    0b0100: (
        (0, 0),
        (0, 0),
        (0, DBUF_FULL_BLOCK_END),
        (0, 0),
    ),

    # Pipe A + Pipe C
    0b0101: (
        (0, DBUF_S1_END),
        (0, 0),
        (DBUF_S2_START, DBUF_FULL_BLOCK_END),
        (0, 0),
    ),

    # Pipe B + Pipe C
    0b0110: (
        (0, 0),
        (0, DBUF_S1_END),
        (DBUF_S2_START, DBUF_FULL_BLOCK_END),
        (0, 0),
    ),

    # Pipe A + Pipe B + Pipe C
    0b0111: (
        (0, DBUF_S1_END),  # S1 is shared between Pipe A and Pipe B
        (0, DBUF_S1_END),
        (DBUF_S2_START, DBUF_FULL_BLOCK_END),
        (0, 0),
    ),

    # Pipe D
    0b1000: (
        (0, 0),
        (0, 0),
        (0, 0),
        (0, DBUF_FULL_BLOCK_END),
    ),

    # Pipe A + Pipe D
    0b1001: (
        (0, DBUF_S1_END),
        (0, 0),
        (0, 0),
        (DBUF_S2_START, DBUF_FULL_BLOCK_END),
    ),

    # Pipe B + Pipe D
    0b1010: (
        (0, 0),
        (0, DBUF_S1_END),
        (0, 0),
        (DBUF_S2_START, DBUF_FULL_BLOCK_END),
    ),

    # Pipe A + Pipe B + Pipe D
    0b1011: (
        (0, DBUF_S1_END),
        (0, DBUF_S1_END),
        (0, 0),
        (DBUF_S2_START, DBUF_FULL_BLOCK_END),
    ),

    # Pipe C + Pipe D
    0b1100: (
        (0, 0),
        (0, 0),
        (0, DBUF_S1_END),
        (DBUF_S2_START, DBUF_FULL_BLOCK_END),
    ),

    # Pipe A + Pipe C + Pipe D
    0b1101: (
        (0, DBUF_S1_END),
        (0, 0),
        (DBUF_S2_START, DBUF_FULL_BLOCK_END),  # S2 is shared between Pipe C and D
        (DBUF_S2_START, DBUF_FULL_BLOCK_END),
    ),

    # Pipe B + Pipe C + Pipe D
    0b1110: (
        (0, 0),
        (0, DBUF_S1_END),
        (DBUF_S2_START, DBUF_FULL_BLOCK_END),
        (DBUF_S2_START, DBUF_FULL_BLOCK_END),
    ),

    # Pipe A + Pipe B + Pipe C + Pipe D
    0b1111: (
        (0, DBUF_S1_END),
        (0, DBUF_S1_END),
        (DBUF_S2_START, DBUF_FULL_BLOCK_END),
        (DBUF_S2_START, DBUF_FULL_BLOCK_END),
    ),
}
