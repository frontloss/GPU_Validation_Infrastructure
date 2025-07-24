#######################################################################################################################
# @file         emp_block.py
# @brief        This file contains Extended Metadata packets(EMP) parser and properties to get the required payload
#               details which driver program
# @details      For more information related to the block refer HDMI2.1 Spec EMP section
#
# @author       Doriwala Nainesh
#######################################################################################################################

import logging

from Libs.Feature.hdmi import emp_data_structures as emp_struct


##
# @brief        This class holds all the SCDS data and exposes properties to get all the required capabilities from the
#               HDMI Forum Vendor Specific Data Block
class HdmiEmpDataBlock:

    ##
    # @brief        Initializes all the data and stores the HDMI file name to be parsed.
    def __init__(self) -> None:
        self._payload_byte_zero: emp_struct.PayloadByteZero = emp_struct.PayloadByteZero(Value=0x0)
        self._payload_byte_one: emp_struct.PayloadByteOne = emp_struct.PayloadByteOne(Value=0x0)
        self._payload_byte_two: emp_struct.PayloadByteTwo = emp_struct.PayloadByteTwo(Value=0x0)
        self._payload_byte_three: emp_struct.PayloadByteThree = emp_struct.PayloadByteThree(Value=0x0)
        self._payload_byte_four: emp_struct.PayloadByteFour = emp_struct.PayloadByteFour(Value=0x0)
        self._payload_byte_five: emp_struct.PayloadByteFive = emp_struct.PayloadByteFive(Value=0x0)
        self._payload_byte_six: emp_struct.PayloadByteSix = emp_struct.PayloadByteSix(Value=0x0)
        self._payload_byte_seven: emp_struct.PayloadByteSeven = emp_struct.PayloadByteSeven(Value=0x0)
        self._payload_byte_eight: emp_struct.PayloadByteEight = emp_struct.PayloadByteEight(Value=0x0)
        self._payload_byte_nine: emp_struct.PayloadByteNine = emp_struct.PayloadByteNine(Value=0x0)
        self._payload_byte_ten: emp_struct.PayloadByteTen = emp_struct.PayloadByteTen(Value=0x0)

    ##
    # @brief        Property to get payload zero
    # @return       Return an int value of pb0
    @property
    def get_pb0(self) -> int:
        return self._payload_byte_zero.Value

    ##
    # @brief        Property to get payload one
    # @return       Return an int value of pb1
    @property
    def get_pb1(self) -> int:
        return self._payload_byte_one.Value

    ##
    # @brief        Property to get payload two
    # @return       Return an int value of pb2
    @property
    def get_pb2(self) -> int:
        return self._payload_byte_two.Value

    ##
    # @brief        Property to get payload three
    # @return       Return an int value of pb3
    @property
    def get_pb3(self) -> int:
        return self._payload_byte_three.Value

    ##
    # @brief        Property to get payload four
    # @return       Return an int value of pb4
    @property
    def get_pb4(self) -> int:
        return self._payload_byte_four.Value

    ##
    # @brief        Property to get payload five
    # @return       Return an int value of pb5
    @property
    def get_pb5(self) -> int:
        return self._payload_byte_five.Value

    ##
    # @brief        Property to get payload six
    # @return       Return a int value of pb6
    @property
    def get_pb6(self) -> int:
        return self._payload_byte_six.Value

    ##
    # @brief        Property to get the VRR en for the panel
    # @return       Return a bool True for enable else False from PB7
    @property
    def vrr_en(self) -> bool:
        # vrr enable bit in payload seven from bit 0
        return self._payload_byte_seven.vrr_en

    ##
    # @brief        Property to get the M_const for the panel
    # @return       Return an int value of m_const of panel from PB7
    @property
    def m_const(self) -> int:
        # m_const in payload seven from bit 1
        return (self._payload_byte_seven.m_const & 0x02) >> 1

    ##
    # @brief        Property to get the fva_factor for the panel
    # @return       Return an int value of fva_factor of panel from PB7
    @property
    def fva_factor_m1(self) -> int:
        # m_const in payload seven from bit 4 to bit 7
        return (self._payload_byte_seven.fva_factor_m1 & 0xF0) >> 4

    ##
    # @brief        Property to get the base vfront for the panel
    # @return       Return an int value of base vfront of panel from PB8
    @property
    def base_vfront(self) -> int:
        # base vfront in payload eight from pb8
        return self._payload_byte_eight.Value

    ##
    # @brief        Property to get the base refresh rate for the panel
    # @return       Return an int value of base refresh rate of panel from PB10 and pb9
    @property
    def base_refresh_rate(self) -> int:
        # base RR value 2MSB bit comes from nine payload bit nine and eight and 7 LSB from payload ten
        return (self._payload_byte_nine.base_refresh_rate_biteightnine << 8 | self._payload_byte_ten.
                base_refresh_rate_bitzeroseven) & 0x3FF

    ##
    # @brief        This Member Function Helps to Parse the HF-VSDB Block and Fills the Respective Payload Bytes.
    # @param[in]    gfx_index: str
    #                   Represents the Graphics Adapter to Which the Display is Plugged. E.g. 'gfx_0', 'gfx_1'
    # @param[in]    port_name: str
    #                   Port Name in Which the Display is Plugged. E.g. 'HDMI_B', 'HDMI_C'
    # @return       None
    def parse_hdmi_emp_data_block(self, emp_data) -> None:
        self._payload_byte_zero.Value = emp_data[0] & 0x000000FF
        self._payload_byte_one.Value = (emp_data[0] >> 8) & 0x000000FF
        self._payload_byte_two.Value = (emp_data[0] >> 16) & 0x000000FF
        self._payload_byte_three.Value = (emp_data[0] >> 24) & 0x000000FF
        self._payload_byte_four.Value = emp_data[1] & 0x000000FF
        self._payload_byte_five.Value = (emp_data[1] >> 8) & 0x000000FF
        self._payload_byte_six.Value = (emp_data[1] >> 16) & 0x000000FF
        self._payload_byte_seven.Value = (emp_data[1] >> 24) & 0x000000FF
        self._payload_byte_eight.Value = emp_data[2] & 0x000000FF
        self._payload_byte_nine.Value = (emp_data[2] >> 8) & 0x000000FF
        self._payload_byte_ten.Value = (emp_data[2] >> 16) & 0x000000FF

        logging.info("\t\tEMP data Block Parsed Successfully and Data is Filled")
