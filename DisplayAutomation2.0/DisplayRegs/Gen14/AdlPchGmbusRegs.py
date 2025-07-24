# ===========================================================================
#
#    Copyright (c) Intel Corporation (2000 - 2020)
#
#    INTEL MAKES NO WARRANTY OF ANY KIND REGARDING THE CODE.  THIS CODE IS LICENSED
#    ON AN "AS IS" BASIS AND INTEL WILL NOT PROVIDE ANY SUPPORT, ASSISTANCE,
#    INSTALLATION, TRAINING OR OTHER SERVICES.  INTEL DOES NOT PROVIDE ANY UPDATES,
#    ENHANCEMENTS OR EXTENSIONS.  INTEL SPECIFICALLY DISCLAIMS ANY WARRANTY OF
#    MERCHANTABILITY, NONINFRINGEMENT, FITNESS FOR ANY PARTICULAR PURPOSE, OR ANY
#    OTHER WARRANTY.  Intel disclaims all liability, including liability for
#    infringement of any proprietary rights, relating to use of the code. No license,
#    express or implied, by estoppel or otherwise, to any intellectual property
#    rights is granted herein.
#
# --------------------------------------------------------------------------
#
# @file AdlPchGmbusRegs.py
# @brief contains AdlPchGmbusRegs.py related register definitions

import ctypes
from enum import Enum


class ENUM_PIN_PAIR_SELECT(Enum):
    PIN_PAIR_SELECT_NONE_DISABLED = 0x0
    PIN_PAIR_SELECT_PIN_PAIR_1 = 0x1
    PIN_PAIR_SELECT_PIN_PAIR_2 = 0x2
    PIN_PAIR_SELECT_PIN_PAIR_3 = 0x3
    PIN_PAIR_SELECT_PIN_PAIR_4 = 0x4
    PIN_PAIR_SELECT_PIN_PAIR_5 = 0x5
    PIN_PAIR_SELECT_PIN_PAIR_6 = 0x6
    PIN_PAIR_SELECT_PIN_PAIR_7 = 0x7
    PIN_PAIR_SELECT_PIN_PAIR_8 = 0x8
    PIN_PAIR_SELECT_PIN_PAIR_9 = 0x9
    PIN_PAIR_SELECT_PIN_PAIR_10 = 0xA
    PIN_PAIR_SELECT_PIN_PAIR_11 = 0xB
    PIN_PAIR_SELECT_PIN_PAIR_12 = 0xC
    PIN_PAIR_SELECT_PIN_PAIR_13 = 0xD
    PIN_PAIR_SELECT_PIN_PAIR_14 = 0xE
    PIN_PAIR_SELECT_PIN_PAIR_15 = 0xF
    PIN_PAIR_SELECT_PIN_PAIR_16 = 0x10


class ENUM_BYTE_COUNT_OVERRIDE(Enum):
    BYTE_COUNT_OVERRIDE_DISABLE = 0x0
    BYTE_COUNT_OVERRIDE_ENABLE = 0x1


class ENUM_GMBUS_RATE_SELECT(Enum):
    GMBUS_RATE_SELECT_100_KHZ = 0x0
    GMBUS_RATE_SELECT_50_KHZ = 0x1
    GMBUS_RATE_SELECT_TEST = 0x3


class ENUM_AKSV_SELECT(Enum):
    AKSV_SELECT_USE_GMBUS = 0x0  # Use the GMBUS data buffer (GMBUS3) for data transmission
    AKSV_SELECT_USE_HDCP = 0x1  # Use HDCP internal Aksv for data transmission


class OFFSET_GMBUS0:
    GMBUS0 = 0xC5100


class _GMBUS0(ctypes.LittleEndianStructure):
    _fields_ = [
        ('PinPairSelect', ctypes.c_uint32, 5),
        ('Reserved5', ctypes.c_uint32, 1),
        ('ByteCountOverride', ctypes.c_uint32, 1),
        ('Reserved7', ctypes.c_uint32, 1),
        ('GmbusRateSelect', ctypes.c_uint32, 2),
        ('Reserved10', ctypes.c_uint32, 1),
        ('AksvSelect', ctypes.c_uint32, 1),
        ('Reserved12', ctypes.c_uint32, 2),
        ('ClockStopDisable', ctypes.c_uint32, 1),
        ('HoldtimeSelect', ctypes.c_uint32, 1),
        ('Reserved16', ctypes.c_uint32, 16),
    ]


class REG_GMBUS0(ctypes.Union):
    value = 0
    offset = 0

    PinPairSelect = 0  # bit 0 to 5
    Reserved5 = 0  # bit 5 to 6
    ByteCountOverride = 0  # bit 6 to 7
    Reserved7 = 0  # bit 7 to 8
    GmbusRateSelect = 0  # bit 8 to 10
    Reserved10 = 0  # bit 10 to 11
    AksvSelect = 0  # bit 11 to 12
    Reserved12 = 0  # bit 12 to 14
    ClockStopDisable = 0  # bit 14 to 15
    HoldtimeSelect = 0  # bit 15 to 16
    Reserved16 = 0  # bit 16 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _GMBUS0),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_GMBUS0, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_SLAVE_ADDRESS_AND_DIRECTION(Enum):
    SLAVE_ADDRESS_AND_DIRECTION_GENERAL_CALL_ADDRESS = 0x1
    SLAVE_ADDRESS_AND_DIRECTION_START_BYTE = 0x0
    SLAVE_ADDRESS_AND_DIRECTION_CBUS_ADDRESS = 0x0
    SLAVE_ADDRESS_AND_DIRECTION_10BIT_ADDRESSING = 0x0


class ENUM_BUS_CYCLE_SELECT(Enum):
    BUS_CYCLE_SELECT_NO_CYCLE = 0x0  # No GMBUS cycle is generated
    BUS_CYCLE_SELECT_NO_INDEX_NO_STOP_WAIT = 0x1  # GMBUS cycle is generated without an INDEX, with no STOP, and ends w
                                                  # ith a WAIT
    BUS_CYCLE_SELECT_INDEX_NO_STOP_WAIT = 0x3  # GMBUS cycle is generated with an INDEX, with no STOP, and ends with a 
                                               # WAIT
    BUS_CYCLE_SELECT_GEN_STOP = 0x4  # Generates a STOP if currently in a WAIT or after the completion of the current b
                                     # yte if active
    BUS_CYCLE_SELECT_NO_INDEX_STOP = 0x5  # GMBUS cycle is generated without an INDEX and with a STOP
    BUS_CYCLE_SELECT_INDEX_STOP = 0x7  # GMBUS cycle is generated with an INDEX and with a STOP


class ENUM_ENABLE_TIMEOUT(Enum):
    ENABLE_TIMEOUT_DISABLE = 0x0
    ENABLE_TIMEOUT_ENABLE = 0x1


class ENUM_SOFTWARE_READY(Enum):
    SOFTWARE_READY_DEASSERT = 0x0  # De-asserted via the assertion event for HW_RDY bit
    SOFTWARE_READY_SW_ASSERT = 0x1  # When asserted by software, results in de-assertion of HW_RDY bit


class ENUM_SOFTWARE_CLEAR_INTERRUPT(Enum):
    SOFTWARE_CLEAR_INTERRUPT_CLEAR_HW_RDY = 0x0  # If this bit is written as a zero when its current state is a one, wi
                                                 # ll clear the HW_RDY bit and allows register writes to be accepted to
                                                 # the GMBUS registers (Write Protect Off). This bit is cleared to zero
                                                 # when an event causes the HW_RDY bit transition to occur.
    SOFTWARE_CLEAR_INTERRUPT_ASSERT_HW_RDY = 0x1  # Asserted by software after servicing the GMBUS interrupt. Setting t
                                                  # his bit causes the INT status bit to be cleared. Setting (1) this
                                                  # bit also asserts the HW_RDY bit (until this bit is written with a
                                                  # 0). When this bit is set, no writes to GMBUS registers will cause
                                                  # the contents to change with the exception of this bit which can be
                                                  # written.


class OFFSET_GMBUS1:
    GMBUS1 = 0xC5104


class _GMBUS1(ctypes.LittleEndianStructure):
    _fields_ = [
        ('SlaveAddressAndDirection', ctypes.c_uint32, 8),
        ('_8BitSlaveRegisterIndex', ctypes.c_uint32, 8),
        ('TotalByteCount', ctypes.c_uint32, 9),
        ('BusCycleSelect', ctypes.c_uint32, 3),
        ('Reserved28', ctypes.c_uint32, 1),
        ('EnableTimeout', ctypes.c_uint32, 1),
        ('SoftwareReady', ctypes.c_uint32, 1),
        ('SoftwareClearInterrupt', ctypes.c_uint32, 1),
    ]


class REG_GMBUS1(ctypes.Union):
    value = 0
    offset = 0

    SlaveAddressAndDirection = 0  # bit 0 to 8
    _8BitSlaveRegisterIndex = 0  # bit 8 to 16
    TotalByteCount = 0  # bit 16 to 25
    BusCycleSelect = 0  # bit 25 to 28
    Reserved28 = 0  # bit 28 to 29
    EnableTimeout = 0  # bit 29 to 30
    SoftwareReady = 0  # bit 30 to 31
    SoftwareClearInterrupt = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _GMBUS1),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_GMBUS1, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_GMBUS_ACTIVE(Enum):
    GMBUS_ACTIVE_IDLE = 0x0
    GMBUS_ACTIVE_ACTIVE = 0x1


class ENUM_NAK_INDICATOR(Enum):
    NAK_INDICATOR_NO_BUS_ERROR = 0x0
    NAK_INDICATOR_NAK_OCCURRED = 0x1


class ENUM_HARDWARE_READY(Enum):
    HARDWARE_READY_0 = 0x0  # Condition required for assertion has not occurred or when this bit is a one and:- SW_RDY 
                            # bit has been asserted- During a GMBUS read transaction, after the each read of the data
                            # register- During a GMBUS write transaction, after each write of the data register-
                            # SW_CLR_INT bit has been cleared
    HARDWARE_READY_1 = 0x1  # This bit is asserted under the following conditions: - After a reset or when the transact
                            # ion is aborted by the setting of the SW_CLR_INT bit - When an active GMBUS cycle has
                            # terminated with a STOP - When during a GMBUS write transaction, the data register needs
                            # and can accept another four bytes of data - During a GMBUS read transaction, this bit is
                            # asserted when the data register has four bytes of new data or the read transaction DATA
                            # phase is complete and the data register contains the last few bytes of the read data


class ENUM_SLAVE_STALL_TIMEOUT_ERROR(Enum):
    SLAVE_STALL_TIMEOUT_ERROR_NO_SLAVE_TIMEOUT = 0x0
    SLAVE_STALL_TIMEOUT_ERROR_SLAVE_TIMEOUT = 0x1


class ENUM_HARDWARE_WAIT_PHASE(Enum):
    HARDWARE_WAIT_PHASE_NOT_IN_A_WAIT_PHASE = 0x0
    HARDWARE_WAIT_PHASE_IN_WAIT_PHASE = 0x1


class ENUM_INUSE(Enum):
    INUSE_GMBUS_IS_ACQUIRED = 0x0  # Read operation that contains a zero in this bit position indicates that the GMBUS 
                                   # engine is now acquired and the subsequent reads of this register will now have
                                   # this bit set. Writing a 0 to this bit has no effect.
    INUSE_GMBUS_IN_USE = 0x1  # Read operation that contains a one for this bit indicates that the GMBUS is currently a
                              # llocated to someone else and "In use". Once set, a write of a 1 to this bit indicates
                              # that the software has relinquished the GMBUS resource and will reset the value of this
                              # bit to a 0.


class OFFSET_GMBUS2:
    GMBUS2 = 0xC5108


class _GMBUS2(ctypes.LittleEndianStructure):
    _fields_ = [
        ('CurrentByteCount', ctypes.c_uint32, 9),
        ('GmbusActive', ctypes.c_uint32, 1),
        ('NakIndicator', ctypes.c_uint32, 1),
        ('HardwareReady', ctypes.c_uint32, 1),
        ('Reserved12', ctypes.c_uint32, 1),
        ('SlaveStallTimeoutError', ctypes.c_uint32, 1),
        ('HardwareWaitPhase', ctypes.c_uint32, 1),
        ('Inuse', ctypes.c_uint32, 1),
        ('Reserved16', ctypes.c_uint32, 16),
    ]


class REG_GMBUS2(ctypes.Union):
    value = 0
    offset = 0

    CurrentByteCount = 0  # bit 0 to 9
    GmbusActive = 0  # bit 9 to 10
    NakIndicator = 0  # bit 10 to 11
    HardwareReady = 0  # bit 11 to 12
    Reserved12 = 0  # bit 12 to 13
    SlaveStallTimeoutError = 0  # bit 13 to 14
    HardwareWaitPhase = 0  # bit 14 to 15
    Inuse = 0  # bit 15 to 16
    Reserved16 = 0  # bit 16 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _GMBUS2),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_GMBUS2, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_GMBUS3:
    GMBUS3 = 0xC510C


class _GMBUS3(ctypes.LittleEndianStructure):
    _fields_ = [
        ('DataByte0', ctypes.c_uint32, 8),
        ('DataByte1', ctypes.c_uint32, 8),
        ('DataByte2', ctypes.c_uint32, 8),
        ('DataByte3', ctypes.c_uint32, 8),
    ]


class REG_GMBUS3(ctypes.Union):
    value = 0
    offset = 0

    DataByte0 = 0  # bit 0 to 8
    DataByte1 = 0  # bit 8 to 16
    DataByte2 = 0  # bit 16 to 24
    DataByte3 = 0  # bit 24 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _GMBUS3),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_GMBUS3, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_INTERRUPT_MASK(Enum):
    INTERRUPT_MASK_SLAVE_STALL_TIMEOUT_INTERRUPT_DISABLE = 0x0
    INTERRUPT_MASK_SLAVE_STALL_TIMEOUT_INTERRUPT_ENABLE = 0x0
    INTERRUPT_MASK_NAK_INTERRUPT_DISABLE = 0x0
    INTERRUPT_MASK_NAK_INTERRUPT_ENABLE = 0x0
    INTERRUPT_MASK_IDLE_INTERRUPT_DISABLE = 0x0
    INTERRUPT_MASK_IDLE_INTERRUPT_ENABLE = 0x0
    INTERRUPT_MASK_HW_WAIT_INTERRUPT_CYCLE_WITHOUT_A_STOP_HAS_COMPLETED_DISABLE = 0x0
    INTERRUPT_MASK_W_WAIT_INTERRUPT_CYCLE_WITHOUT_A_STOP_HAS_COMPLETED_ENABLE = 0x0
    INTERRUPT_MASK_HW_READY_DATA_TRANSFERRED_INTERRUPT_DISABLE = 0x0
    INTERRUPT_MASK_HW_READY_DATA_TRANSFERRED_INTERRUPT_ENABLE = 0x0


class OFFSET_GMBUS4:
    GMBUS4 = 0xC5110


class _GMBUS4(ctypes.LittleEndianStructure):
    _fields_ = [
        ('InterruptMask', ctypes.c_uint32, 5),
        ('Reserved5', ctypes.c_uint32, 27),
    ]


class REG_GMBUS4(ctypes.Union):
    value = 0
    offset = 0

    InterruptMask = 0  # bit 0 to 5
    Reserved5 = 0  # bit 5 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _GMBUS4),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_GMBUS4, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_GMBUS5:
    GMBUS5 = 0xC5120


class _GMBUS5(ctypes.LittleEndianStructure):
    _fields_ = [
        ('_2ByteSlaveIndex', ctypes.c_uint32, 16),
        ('Reserved16', ctypes.c_uint32, 15),
        ('_2ByteIndexEnable', ctypes.c_uint32, 1),
    ]


class REG_GMBUS5(ctypes.Union):
    value = 0
    offset = 0

    _2ByteSlaveIndex = 0  # bit 0 to 16
    Reserved16 = 0  # bit 16 to 31
    _2ByteIndexEnable = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _GMBUS5),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_GMBUS5, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_GPIO_CLOCK_DIRECTION_MASK(Enum):
    GPIO_CLOCK_DIRECTION_MASK_DOT_NOT_WRITE = 0x0
    GPIO_CLOCK_DIRECTION_MASK_WRITE = 0x1


class ENUM_GPIO_CLOCK_DIRECTION_VALUE(Enum):
    GPIO_CLOCK_DIRECTION_VALUE_INPUT = 0x0
    GPIO_CLOCK_DIRECTION_VALUE_OUTPUT = 0x1


class ENUM_GPIO_CLOCK_DATA_MASK(Enum):
    GPIO_CLOCK_DATA_MASK_DOT_NOT_WRITE = 0x0
    GPIO_CLOCK_DATA_MASK_WRITE = 0x1


class ENUM_GPIO_CLOCK_DATA_IN(Enum):
    GPIO_CLOCK_DATA_IN_UNDEFINED_READ_ONLY_DEPENDS_ON_I_O_PIN = 0x0


class ENUM_GPIO_DATA_DIRECTION_MASK(Enum):
    GPIO_DATA_DIRECTION_MASK_DOT_NOT_WRITE = 0x0
    GPIO_DATA_DIRECTION_MASK_WRITE = 0x1


class ENUM_GPIO_DATA_DIRECTION_VALUE(Enum):
    GPIO_DATA_DIRECTION_VALUE_INPUT = 0x0
    GPIO_DATA_DIRECTION_VALUE_OUTPUT = 0x1


class ENUM_GPIO_DATA_MASK(Enum):
    GPIO_DATA_MASK_DOT_NOT_WRITE = 0x0
    GPIO_DATA_MASK_WRITE = 0x1


class ENUM_GPIO_DATA_IN(Enum):
    GPIO_DATA_IN_UNDEFINED_READ_ONLY_DEPENDS_ON_I_O_PIN = 0x0


class OFFSET_GPIO_CTL:
    GPIO_CTL_1 = 0xC5014
    GPIO_CTL_2 = 0xC5018
    GPIO_CTL_3 = 0xC501C
    GPIO_CTL_9 = 0xC5034
    GPIO_CTL_10 = 0xC5038
    GPIO_CTL_11 = 0xC503C
    GPIO_CTL_12 = 0xC5040
    GPIO_CTL_13 = 0xC5044
    GPIO_CTL_14 = 0xC5048


class _GPIO_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('GpioClockDirectionMask', ctypes.c_uint32, 1),
        ('GpioClockDirectionValue', ctypes.c_uint32, 1),
        ('GpioClockDataMask', ctypes.c_uint32, 1),
        ('GpioClockDataValue', ctypes.c_uint32, 1),
        ('GpioClockDataIn', ctypes.c_uint32, 1),
        ('Reserved5', ctypes.c_uint32, 3),
        ('GpioDataDirectionMask', ctypes.c_uint32, 1),
        ('GpioDataDirectionValue', ctypes.c_uint32, 1),
        ('GpioDataMask', ctypes.c_uint32, 1),
        ('GpioDataValue', ctypes.c_uint32, 1),
        ('GpioDataIn', ctypes.c_uint32, 1),
        ('Reserved13', ctypes.c_uint32, 19),
    ]


class REG_GPIO_CTL(ctypes.Union):
    value = 0
    offset = 0

    GpioClockDirectionMask = 0  # bit 0 to 1
    GpioClockDirectionValue = 0  # bit 1 to 2
    GpioClockDataMask = 0  # bit 2 to 3
    GpioClockDataValue = 0  # bit 3 to 4
    GpioClockDataIn = 0  # bit 4 to 5
    Reserved5 = 0  # bit 5 to 8
    GpioDataDirectionMask = 0  # bit 8 to 9
    GpioDataDirectionValue = 0  # bit 9 to 10
    GpioDataMask = 0  # bit 10 to 11
    GpioDataValue = 0  # bit 11 to 12
    GpioDataIn = 0  # bit 12 to 13
    Reserved13 = 0  # bit 13 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _GPIO_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_GPIO_CTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value

