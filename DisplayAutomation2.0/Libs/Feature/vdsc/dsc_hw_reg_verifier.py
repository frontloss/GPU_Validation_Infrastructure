#######################################################################################################################
# @file         dsc_hw_reg_verifier.py
# @brief        Contains PipeDssCtlOneRegister, PipeDssCtlTwoRegister, PipeDssCtlThreeRegister,
#               DSCAdditionalRegVerifier Classes Used For Verifying Pipe DSS CTL Registers and Other Such Registers
#               Which are Programmed as Part of DSC Enabling Sequence.
#
# @author       Praburaj Krishnan
#######################################################################################################################

from __future__ import annotations

import logging
import math

from Libs.Core.logger import gdhm
from Libs.Feature.mipi.mipi_helper import MipiHelper
from registers.mmioregister import MMIORegister


##
# @brief    Holds the Fields that Needs to be Verified as Part of DSC Verification Specific to PIPE_DSS_CTL1_REG
#           This Register is Common for DP, EDP and MIPI DSC Programing.
class PipeDssCtlOneRegister(object):
    # Templates Which Should be Used for logging Success and Failure Case for PipeDssCtlOneRegister.
    success_log_template: str = "PipeDssCtlOneRegister.{}: Expected: {} Actual: {}"
    error_log_template: str = "[Driver Issue] -  PipeDssCtlOneRegister.{} [Mismatch]: Expected: {} Actual: {}"

    ##
    # @brief        Initialize the Member Variables of Class PipeDssCtlOneRegister.
    #               Use Properties to Get the Value of Each Member Variable and Don't Access the Private Members.
    #               Use Member Function to Get Expected/Actual Values and Don't assign the Values Directly.
    def __init__(self):
        # This Fields Must be False as These are for Uncompressed Pipe Joiner Programming.
        self._is_uncompressed_joiner_slave: bool = False
        self._is_uncompressed_joiner_master: bool = False

        # True if it's a Master Pipe False Otherwise
        self._is_master_big_joiner: bool = False

        # True if One DSS Unit is Working with Another DSS Unit in Adjacent Pipe
        self._is_big_joiner_enabled: bool = False

        # True if Two DSC Engines are Working in Parallel. Combines the Output of Two DSC Engines(Left and Right)
        # Exception is Mipi Displays Operating in Dual Link Mode.
        self._is_joiner_enabled: bool = False

        # Splitter is Enabled Whenever Two DSC Engines Are Working in Parallel
        # Exception is Mipi Displays Operating in Dual Link Mode.
        self._is_splitter_enabled: bool = False

        # True if all 4 DSS units is working together
        # This bit will be set to True only for PIPE A, B and C. For PIPE D it won't be set
        self._ultra_joiner_enabled = False

        # True if its the primary ultra joiner (Master). Only PIPE A can be Master.
        self._primary_ultra_joiner_enabled = False

    ##
    # @brief        Private Helper Function Which Populates the PipeDssCtlOneRegister Expected Values In case of MIPI
    #               DSC Displays.
    # @param[in]    mipi_helper: MipiHelper
    #                   Contains Mipi Display Related Information.
    # @return       None
    def fill_expected_pipe_dss_ctl_one_reg_mipi(self, mipi_helper: MipiHelper) -> None:
        vbt_block_56 = mipi_helper.gfx_vbt.block_56.CompressionParamDataStructEntry[mipi_helper.panel1_index]
        dsc_slices_per_line: int = vbt_block_56.DSCSlicesPerLine

        if mipi_helper.dual_link == 0 and dsc_slices_per_line == 1:
            self._is_splitter_enabled = self._is_joiner_enabled = False
        elif mipi_helper.dual_link == 0 and dsc_slices_per_line > 1:
            # Splitter needs to verified only in case of joiner not enabled. HW will by default enable splitter if
            # joiner is enabled.So, driver won't explicitly enable splitter when joiner is already enabled.
            self._is_splitter_enabled = False
            self._is_joiner_enabled = True
        elif mipi_helper.dual_link:
            self._is_splitter_enabled = True
            self._is_joiner_enabled = False

    ##
    # @brief        Private Helper Function Which Populates the PipeDssCtlOneRegister Expected Values In case of EDP,
    #               DP and HDMI DSC Displays. EDP, DP and HDMI DSC Follows Same Logic For Programming this Register.
    # @param[in]    pipe_name: str
    #                   Contains the pipe name for which expected values are being filled. E.g A, B, C, D
    # @param[in]    is_master_pipe: bool
    #                   Helps to Figure out if it's a Master Big Joiner or Not.
    # @param[in]    vdsc_instance: int
    #                   Helps to Figure If Joiner and Big Joiner to Enabled or not.
    # @return       None
    def fill_expected_pipe_dss_ctl_one_reg(self, pipe_name: str, is_master_pipe: bool, vdsc_instance: int) -> None:

        if vdsc_instance in [8, 12]:
            self._is_joiner_enabled = self._is_big_joiner_enabled = True
            self._is_master_big_joiner = is_master_pipe
            if pipe_name in ['A', 'B', 'C']:
                self._ultra_joiner_enabled = True
            if pipe_name == 'A':
                self._primary_ultra_joiner_enabled = True
        elif vdsc_instance == 4:
            self._is_joiner_enabled = self._is_big_joiner_enabled = True
            self._is_master_big_joiner = is_master_pipe
        elif vdsc_instance == 2:
            self._is_joiner_enabled = True

    ##
    # @brief        Member Function to Get the Actual PipeDssCtlOneRegister Based on MMIO Register Values Programmed by
    #               Driver and Input Parameters like Pipe and Transcoder.
    # @param[in]    gfx_index: str
    #                   Represents the Graphics Adapter to Which the Display is Plugged. E.g. 'gfx_0', 'gfx_1'
    # @param[in]    platform: str
    #                   Platform Name in Which the Display is Plugged.
    # @param[in]    pipe: str
    #                   Pipe Name to Which the Display is Connected.
    # @param[in]    transcoder: str
    #                   Transcoder to Which the Display is Connected. Only Used in MIPI and EDP Case.
    # @return       register_name: str
    #                   Returns the Register Name From Which the Values is Read. Helps For Logging Purpose.
    def fill_actual_pipe_dss_ctl_one_reg(self, gfx_index: str, platform: str, pipe: str, transcoder: str) -> str:
        # Transcoder Name is Required to Figure out Whether it's a EDP/MIPI Transcoder or not.
        # Till Gen11 EDP has Separate Transcoder and also Register Name is Different.
        # Also MIPI has Two Separate Transcoders DSI0 and DSI1
        # Hence Transcoder Information is Required to Figure Out the Right Register to Read.
        if transcoder == 'EDP' or (transcoder in ['DSI0', 'DSI1'] and platform in ['ICLLP', 'JSL']):
            register_name: str = 'DSS_CTL1'
            dss_ctl1 = MMIORegister.read("DSS_CTL1_REGISTER", register_name, platform, gfx_index=gfx_index)
        else:
            register_name: str = 'PIPE_DSS_CTL1_P' + pipe
            dss_ctl1 = MMIORegister.read("PIPE_DSS_CTL1_REGISTER", register_name, platform, gfx_index=gfx_index)

            self._is_big_joiner_enabled = bool(dss_ctl1.big_joiner_enable)

            # Uncompressed pipe joiner is supported only from DG2
            if platform not in ['ICLLP', 'LKF1', 'LKFR', 'JSL', 'TGL', 'DG1', 'RKL', 'ADLS']:
                self._is_uncompressed_joiner_slave = bool(dss_ctl1.uncompressed_joiner_slave)
                self._is_uncompressed_joiner_master = bool(dss_ctl1.uncompressed_joiner_master)

            # Ultra-Joiner is supported only from ELG
            if platform not in ['ICLLP', 'LKF1', 'LKFR', 'JSL', 'TGL', 'RKL', 'DG1', 'DG2', 'ADLS', 'ADLP', 'MTL']:
                self._ultra_joiner_enabled = bool(dss_ctl1.ultra_joiner_enable)
                self._primary_ultra_joiner_enabled = bool(dss_ctl1.primary_ultra_joiner_enable)

            self._is_master_big_joiner = bool(dss_ctl1.master_big_joiner_enable)

        self._is_joiner_enabled = bool(dss_ctl1.joiner_enable)
        self._is_splitter_enabled = bool(dss_ctl1.splitter_enable)

        return register_name

    ##
    # @brief        Private Member Function to Log the Expected and Actual Values based on the Log Templates Defined.
    # @param[in]    actual_pipe_dss_ctl_one_register: PipeDssCtlOneRegister
    #                   Object Which Contains the Actual Value Read From the MMIO Registers.
    # @return       is_equal: bool
    #                   True if All Expected and Actual Values are Matching, False Otherwise.
    def _log_eq_(self, actual_pipe_dss_ctl_one_register: PipeDssCtlOneRegister) -> bool:
        is_equal: bool = True

        zip_iterator = zip(self.__dict__.items(), actual_pipe_dss_ctl_one_register.__dict__.items())
        for (e_key, e_value), (a_key, a_value) in zip_iterator:
            if e_value == a_value:
                logging.info(PipeDssCtlOneRegister.success_log_template.format(e_key, e_value, a_value))
            else:
                logging.error(PipeDssCtlOneRegister.error_log_template.format(e_key, e_value, a_value))
                is_equal = False

        return is_equal

    ##
    # @brief        Overriding the Inbuilt Member Function to Add Functionality For Comparing the Objects of Same Type.
    #               This will be Invoked Whenever Checked For Equality(==) of the Objects.
    # @param[in]    actual_pipe_dss_ctl_one_register: PipeDssCtlOneRegister
    #                   Object Which Contains the Actual Value Read From the MMIO Registers.
    # @return       is_equal: bool
    #                   Refer __log_eq__ Function.
    def __eq__(self, actual_pipe_dss_ctl_one_register: PipeDssCtlOneRegister) -> bool:
        is_equal: bool = False

        if isinstance(actual_pipe_dss_ctl_one_register, PipeDssCtlOneRegister) is True:
            is_equal = self._log_eq_(actual_pipe_dss_ctl_one_register)

        return is_equal


##
# @brief    Holds the Fields that Needs to be Verified as Part of DSC Verification Specific to PIPE_DSS_CTL2_REG
class PipeDssCtlTwoRegister(object):
    # Templates Which Should be Used for logging Success and Failure Case for PipeDssCtlTwoRegister.
    success_log_template: str = "PipeDssCtlTwoRegister.{}: Expected: {} Actual: {}"
    error_log_template: str = "[Driver Issue] -  PipeDssCtlTwoRegister.{} [Mismatch]: Expected: {} Actual: {}"

    ##
    # @brief        Initialize the Member Variables of Class PipeDssCtlTwoRegister.
    #               Use Properties to Get the Value of Each Member Variable and Don't access the Private Members.
    #               Use Member Function to Get Expected/Actual Values and Don't assign the Values Directly.
    def __init__(self):
        # True if DSC Engine is Enabled, False Otherwise.
        self._is_left_vdsc_engine_enabled = False
        self._is_right_vdsc_engine_enabled = False
        self._is_second_vdsc_engine_enabled = False

        # True if 3 VDSC Engines output are joined by small joiner, False otherwise.
        self._small_joiner_configuration = False

    ##
    # @brief        Property to Access the Private Member Variable Outside of Class.
    # @return       Returns True is Left vdsc engine is enabled else False
    @property
    def is_left_vdsc_engine_enabled(self) -> bool:
        return self._is_left_vdsc_engine_enabled

    ##
    # @brief        Property to Access the Private Member Variable Outside of Class.
    # @return       Returns True is right vdsc engine is enabled else False
    @property
    def is_right_vdsc_engine_enabled(self) -> bool:
        return self._is_right_vdsc_engine_enabled

    ##
    # @brief        Property to Access the Private Member Variable Outside of Class.
    # @return       Returns True is second vdsc engine is enabled else False
    @property
    def is_second_vdsc_engine_enabled(self) -> bool:
        return self._is_second_vdsc_engine_enabled

    ##
    # @brief        Property to Access the Private Member Variable Outside of Class.
    # @return       Returns True only if three vdsc engines are joined by the small joiner else False
    @property
    def small_joiner_configuration(self) -> bool:
        return self._small_joiner_configuration

    ##
    # @brief        Private Helper Function Which Populates the PipeDssCtlTwoRegister Expected Values In case of MIPI
    #               DSC Displays. Expected Values are Computed by Reading VBT Fields.
    # @param[in]    port: str
    #                   Contains Port Name Which Helps to Decide Which Engine(Right/Left) Should be Enabled.
    # @param[in]    mipi_helper: MipiHelper
    #                   Contains VBT Data Which is Used to Retrieve the Panel Caps.
    # @return       None
    def fill_expected_pipe_dss_ctl_two_reg_mipi(self, port: str, mipi_helper: MipiHelper) -> None:
        # MipiHelper to Get the Slices Per Line Value From the VBT.
        vbt_block_56 = mipi_helper.gfx_vbt.block_56.CompressionParamDataStructEntry[mipi_helper.panel1_index]
        dsc_slices_per_line: int = vbt_block_56.DSCSlicesPerLine

        if mipi_helper.dual_link or dsc_slices_per_line > 1:
            self._is_left_vdsc_engine_enabled = self._is_right_vdsc_engine_enabled = True
        else:
            if port == 'mipi_a':
                self._is_left_vdsc_engine_enabled = True
            elif port == 'mipi_c':
                self._is_right_vdsc_engine_enabled = True

    ##
    # @brief        Private Helper Function Which Populates the PipeDssCtlTwoRegister Expected Values In case of EDP,
    #               DP and HDMI DSC Displays. EDP, DP and HDMI DSC Follows Same Logic For Programming this Register.
    # @param[in]    vdsc_instance: int
    #                   Helps to Decide, If Right Engine Should be Enabled or not.
    # @return       None
    def fill_expected_pipe_dss_ctl_two_reg(self, vdsc_instance: int) -> None:
        self._is_left_vdsc_engine_enabled = True

        if vdsc_instance in [2, 4, 8, 12]:
            self._is_right_vdsc_engine_enabled = True

        if vdsc_instance == 12:
            self._is_second_vdsc_engine_enabled = True
            self._small_joiner_configuration = True

    ##
    # @brief        Member Function to Get the Actual PipeDssCtlTwoRegister Based on MMIO Register Values Programmed by
    #               Driver and Input Parameters like Pipe and Transcoder.
    # @param[in]    gfx_index: str
    #                   Represents the Graphics Adapter to Which the Display is Plugged. E.g. 'gfx_0', 'gfx_1'
    # @param[in]    platform: str
    #                   Platform Name in Which the Display is Plugged.
    # @param[in]    pipe: str
    #                   Pipe Name to Which the Display is Connected. E.g. 'A','B','C','D'
    # @param[in]    transcoder: str
    #                   Transcoder to Which the Display is Connected. Only Used in MIPI and EDP Case.
    # @return       register_name: str
    #                   Returns the Register Name From Which the Values is Read. Helps For Logging Purpose.
    def fill_actual_pipe_dss_ctl_two_reg(self, gfx_index: str, platform: str, pipe: str, transcoder) -> str:
        # Transcoder Name is Required to Figure out Whether it's a EDP Transcoder or not.
        # Till Gen11 EDP has Separate Transcoder and also Register Name is Different.
        # Also MIPI has Two Separate Transcoders DSI0 and DSI1
        # Hence Transcoder Information is Required to Figure Out the Right Register to Read.
        if transcoder == 'EDP' or (transcoder in ['DSI0', 'DSI1'] and platform in ['ICLLP', 'JSL']):
            register_name: str = 'DSS_CTL2'
            dss_ctl2 = MMIORegister.read("DSS_CTL2_REGISTER", register_name, platform, gfx_index=gfx_index)
        else:
            register_name: str = 'PIPE_DSS_CTL2_P' + pipe
            dss_ctl2 = MMIORegister.read("PIPE_DSS_CTL2_REGISTER", register_name, platform, gfx_index=gfx_index)

        self._is_right_vdsc_engine_enabled = bool(dss_ctl2.right_branch_vdsc_enable)
        self._is_left_vdsc_engine_enabled = bool(dss_ctl2.left_branch_vdsc_enable)

        if platform in ["ELG"]:
            self._is_second_vdsc_engine_enabled = bool(dss_ctl2.vdsc2_enable)
            self._small_joiner_configuration = bool(dss_ctl2.small_joiner_configuration)

        return register_name

    ##
    # @brief        Private Member Function to Log the Expected and Actual Values based on the Log Templates Defined.
    # @param[in]    actual_pipe_dss_ctl_two_register: PipeDssCtlTwoRegister
    #                   Object Which Contains the Actual Value Read From the MMIO Registers.
    # @return       is_equal: bool
    #                   True if All Expected and Actual Values are Matching, False Otherwise.
    def _log_eq_(self, actual_pipe_dss_ctl_two_register: PipeDssCtlTwoRegister) -> bool:
        is_equal: bool = True

        zip_iterator = zip(self.__dict__.items(), actual_pipe_dss_ctl_two_register.__dict__.items())
        for (e_key, e_value), (a_key, a_value) in zip_iterator:
            if e_value == a_value:
                logging.info(PipeDssCtlTwoRegister.success_log_template.format(e_key, e_value, e_value))
            else:
                logging.error(PipeDssCtlTwoRegister.error_log_template.format(e_key, e_value, a_value))
                is_equal = False

        return is_equal

    ##
    # @brief        Overriding the Inbuilt Member Function to Add Functionality For Comparing the Objects of Same Type.
    #               This will be Invoked Whenever Checked For Equality(==) of the Objects.
    # @param[in]    actual_pipe_dss_ctl_two_register: PipeDssCtlTwoRegister
    #                   Object Which Contains the Actual Value Read From the MMIO Registers.
    # @return       is_equal: bool
    #                   Refer __log_eq__ Function.
    def __eq__(self, actual_pipe_dss_ctl_two_register: PipeDssCtlTwoRegister) -> bool:
        is_equal: bool = False

        if isinstance(actual_pipe_dss_ctl_two_register, PipeDssCtlTwoRegister) is True:
            is_equal = self._log_eq_(actual_pipe_dss_ctl_two_register)

        return is_equal


##
# @brief    Holds the Fields that Needs to be Verified as Part of DSC Verification Specific to PIPE_DSS_CTL3_REG
class PipeDssCtlThreeRegister:
    # Templates Which Should be Used for logging Success and Failure Case for PipeDssCtlTwoRegister.
    success_log_template: str = "PipeDssCtlThreeRegister.{}: Expected: {} Actual: {}"
    error_log_template: str = "[Driver Issue] -  PipeDssCtlThreeRegister.{} [Mismatch]: Expected: {} Actual: {}"

    ##
    # @brief        Initialize the Member Variables of Class PipeDssCtlThreeRegister.
    #               Use Properties to Get the Value of Each Member Variable and Don't access the Private Members.
    #               Use Member Function to Get Expected/Actual Values and Don't assign the Values Directly.
    def __init__(self):
        self._dsc_pixel_replication = 0

    ##
    # @brief        Property to Access the Private Member Variable Outside of Class.
    # @return       Returns the number of pixels that needs to be replicated, zero indicates no pixel replication
    @property
    def no_of_pixels_replicated(self) -> int:
        return self._dsc_pixel_replication

    ##
    # @brief        Private Helper Function Which Populates the PipeDssCtlThreeRegister Expected Values In case of DP
    #               and HDMI DSC Displays.
    # @param[in]    pipe_name: str
    #                   Pipe Name to Which the Display is Connected. E.g. 'A','B','C','D'
    # @param[in]    pic_width: int
    #                   It's nothing but HActive of the display.
    # @param[in]    slice_count: int
    #                   Slice count is number of slices per display line
    # @return       None
    def fill_expected_pipe_dss_ctl_three_reg(self, pipe_name: str, pic_width: int, slice_count: int) -> None:
        # DSC pixel replication should be programmed only for primary pipe. Pipe A is always the primary pipe in case of
        # ultra-joiner
        if pipe_name == 'A':
            slice_width = int(math.ceil(pic_width / slice_count))
            self._dsc_pixel_replication = (slice_width * slice_count) - pic_width

    ##
    # @brief        Member Function to Get the Actual PipeDssCtlThreeRegister Based on MMIO Register Values Programmed
    #               by Driver
    # @param[in]    gfx_index: str
    #                   Represents the Graphics Adapter to Which the Display is Plugged. E.g. 'gfx_0', 'gfx_1'
    # @param[in]    platform: str
    #                   Platform Name in Which the Display is Plugged.
    # @param[in]    pipe: str
    #                   Pipe Name to Which the Display is Connected. E.g. 'A','B','C','D'
    # @return       register_name: str
    #                   Returns the Register Name From Which the Value is Read. Helps For Logging Purpose.
    def fill_actual_pipe_dss_ctl_three_reg(self, gfx_index: str, platform: str, pipe: str) -> str:
        register_name: str = 'PIPE_DSS_CTL3_P' + pipe

        if platform in ['ELG'] and pipe == 'A':
            dss_ctl3 = MMIORegister.read("PIPE_DSS_CTL3_REGISTER", register_name, platform, gfx_index=gfx_index)
            self._dsc_pixel_replication = dss_ctl3.dsc_pixel_replication

        return register_name

    ##
    # @brief        Private Member Function to Log the Expected and Actual Values based on the Log Templates Defined.
    # @param[in]    actual_pipe_dss_ctl_two_register: PipeDssCtlTwoRegister
    #                   Object Which Contains the Actual Value Read From the MMIO Registers.
    # @return       is_equal: bool
    #                   True if All Expected and Actual Values are Matching, False Otherwise.
    def _log_eq_(self, actual_pipe_dss_ctl_three_register: PipeDssCtlThreeRegister) -> bool:
        is_equal: bool = True

        zip_iterator = zip(self.__dict__.items(), actual_pipe_dss_ctl_three_register.__dict__.items())
        for (e_key, e_value), (a_key, a_value) in zip_iterator:
            if e_value == a_value:
                logging.info(PipeDssCtlThreeRegister.success_log_template.format(e_key, e_value, e_value))
            else:
                logging.error(PipeDssCtlThreeRegister.error_log_template.format(e_key, e_value, a_value))
                is_equal = False

        return is_equal

    ##
    # @brief        Overriding the Inbuilt Member Function to Add Functionality For Comparing the Objects of Same Type.
    #               This will be Invoked Whenever Checked For Equality(==) of the Objects.
    # @param[in]    actual_pipe_dss_ctl_three_register: PipeDssCtlThreeRegister
    #                   Object Which Contains the Actual Value Read From the MMIO Registers.
    # @return       is_equal: bool
    #                   Refer __log_eq__ Function.
    def __eq__(self, actual_pipe_dss_ctl_three_register: PipeDssCtlThreeRegister) -> bool:
        is_equal: bool = False

        if isinstance(actual_pipe_dss_ctl_three_register, PipeDssCtlThreeRegister) is True:
            is_equal = self._log_eq_(actual_pipe_dss_ctl_three_register)

        return is_equal


##
# @brief    Contains All Additional Register Verification Needed for DSC.
class DSCAdditionalRegVerifier:
    # Use this Template For Printing Success and Error Message For Functions Defined in this Class.
    success_log_template: str = "{register}.{field}: Expected: {value}  Actual: {value}"
    error_log_template: str = "[Driver Issue] - {register}.{field} [Mismatch]: Expected: {e_value}  Actual: {a_value}"

    ##
    # @brief        PPS Bit Should be Enabled Prior to Enabling VDSC. PPS DIP Can Only be Enabled For Display Port
    #               S/W Should Enable DSC H/W Only After Enabling PPS.
    # @param[in]    gfx_index: str
    #                   Represents the Graphics Adapter to Which the Display is Plugged. E.g. 'gfx_0', 'gfx_1'
    # @param[in]    platform: str
    #                   Platform Name in Which the Display is Plugged.
    # @param[in]    transcoder: str
    #                   Transcoder to Which the Display is Connected.
    # @return       is_vdip_pps_enabled: bool
    #                   Returns True if Video Data Island Packet PPS is Enabled, False Otherwise.
    @classmethod
    def verify_vdip_pps_status(cls, gfx_index: str, platform: str, transcoder: str) -> bool:
        is_vdip_pps_enabled: bool = True
        register: str = 'VIDEO_DIP_CTL_' + transcoder

        vdip_ctl = MMIORegister.read("VIDEO_DIP_CTL_REGISTER", register, platform, gfx_index=gfx_index)
        if (vdip_ctl.asUint & 0x1000000) == 0x1000000:
            logging.info(cls.success_log_template.format(register=register, field="enable_pps", value="[Enabled]"))
        else:
            logging.error(
                cls.error_log_template.format(register=register, field="enable_pps", e_value="[Enabled]",
                                              a_value="[Disabled]"))
            gdhm.report_bug(
                title="[Interfaces][DP_DSC] PPS Bit is Disabled but it should be enabled before enabling VDSC",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            is_vdip_pps_enabled = False

        return is_vdip_pps_enabled

    ##
    # @brief        This Field is Specific to MIPI Transcoders. Pixel Format Should be Compressed When MIPI DSC is
    #               Enabled.
    # @param[in]    gfx_index: str
    #                   Represents the Graphics Adapter to Which the Display is Plugged. E.g. 'gfx_0', 'gfx_1'
    # @param[in]    platform: str
    #                   Platform Name in Which the Display is Plugged.
    # @param[in]    transcoder: str
    #                   Transcoder to Which the MIPI Display is Connected.
    # @return       is_compressed_pixel_format: bool
    #                   Returns True if Pixel Format is Set Compressed, False Otherwise.
    @classmethod
    def verify_pixel_format_mipi(cls, gfx_index: str, platform: str, transcoder: str) -> bool:
        is_compressed_pixel_format: bool = True
        mipi_helper: MipiHelper = MipiHelper(platform.lower())
        register: str = "TRANS_DSI_FUNC_CONF_" + transcoder

        dsi_reg = MMIORegister.read("TRANS_DSI_FUNC_CONF_REGISTER", register, platform, gfx_index=gfx_index)
        e_pixel_format: str = mipi_helper.decode_pixel_format(dsi_reg.pixel_format)

        if e_pixel_format == "Compressed":
            logging.info(
                cls.success_log_template.format(register=register, field="pixel_format", value="Compressed"))
        else:
            logging.error(
                cls.error_log_template.format(register=register, field="pixel_format", e_value=e_pixel_format,
                                              a_value="Compressed"))
            gdhm.report_bug(
                title="[Interfaces][DP_DSC] Pixel Format is not Compressed though MIPI DSC is Enabled",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            is_compressed_pixel_format = False

        return is_compressed_pixel_format
