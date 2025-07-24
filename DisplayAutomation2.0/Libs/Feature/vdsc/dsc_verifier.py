#######################################################################################################################
# @file         dsc_verifier.py
# @brief        Contains Different DSC Verifiers based on the Display Technology like DP, EDP and MIPI.
#               DisplayStreamCompressionVerifier - Base Class For All DSC Verifiers.
#               DisplayPortDSCVerifier, EdpDSCVerifier, MipiDSCVerifier are All the Currently Available DSC Verifiers
#
# @author       Praburaj Krishnan
#######################################################################################################################

from __future__ import annotations

import logging
from abc import abstractmethod, ABC
from typing import List, Dict, Optional, Any

from Libs.Core.logger import gdhm
from Libs.Core.machine_info import machine_info
from Libs.Core.sw_sim.dp_mst import DisplayPort
from Libs.Core.display_config.display_config_struct import DisplayTimings
from Libs.Feature.display_mode_enum.mode_enum_xml_parser import ColorFormat
from Libs.Feature.display_port import dpcd_helper
from Libs.Feature.display_port.dp_enum_constants import VirtualDisplayportPeerDevice
from Libs.Feature.mipi.mipi_helper import MipiHelper
from Libs.Feature.vdsc.dsc_definitions import DSCDisplay, DSCPictureParameterSet, DSCRequiredPictureParameterSet
from Libs.Feature.vdsc.dsc_definitions import PictureParameterSDP
from Libs.Feature.vdsc.dsc_enum_constants import DPCDOffsets
from Libs.Feature.vdsc.dsc_enum_constants import DisplayType, DSCEngine, TestDataKey, EDP_FEC_UNSUPPORTED_PLATFORMS
from Libs.Feature.vdsc.dsc_enum_constants import COMMON_SDP_TL_SUPPORTED_PLATFORMS
from Libs.Feature.vdsc.dsc_helper import DSCHelper
from Libs.Feature.vdsc.dsc_hw_reg_verifier import DSCAdditionalRegVerifier, PipeDssCtlOneRegister
from Libs.Feature.vdsc.dsc_hw_reg_verifier import PipeDssCtlTwoRegister, PipeDssCtlThreeRegister
from Libs.Feature.vdsc.pps_calculator import PictureParameterSetCalculator
from Libs.Feature.vdsc.pps_calculator_dp import DpPictureParameterSetCalculator
from Libs.Feature.vdsc.pps_calculator_edp import EdpPictureParameterSetCalculator
from Libs.Feature.vdsc.pps_calculator_hdmi import HDMIPictureParameterSetCalculator
from Libs.Feature.vdsc.pps_calculator_mipi import MipiPictureParameterSetCalculator
from Libs.Feature.display_engine.de_base.display_base import DisplayBase
from registers.mmioregister import MMIORegister


##
# @brief        DisplayStreamCompressionVerifier is Defines Multiple Functions Required for DSC Verification.
#               Any DSC Verifier that Inherits DisplayStreamCompressionVerifier Should Implement the Abstract Methods
#               Defined here. Multiple Functions Which are Common Across DP, EDP and MIPI are Implemented here.
#               If any Verifier Needs Additional Functionality than Defined here, then that Particular Verifier Needs to
#               Override the Function and Implement Changes. Functions Defined here Shouldn't be Modified Unless the
#               Changes are Applicable to All DSC Verifiers.
class DisplayStreamCompressionVerifier(ABC):

    ##
    # @brief        Initialize the Display Stream Compression Verifier Using the DSC Display Information.
    # @param[in]    display_info: DSCDisplay
    #                   Contains all Basic Information Related to the DSC Display.
    # @param[in]    test_data: Dict[TestDataKey, Any]
    #                   Contains any data that is needed for verification from the test scripts can be passed using this
    #                   dictionary. Key has to be of type TestDataKey. Value can be anything.
    def __init__(self, display_info: DSCDisplay, test_data: Dict[TestDataKey, Any]):
        # Contains the Display Information like Transcoder, Pipe which are Required for PipeDssCtlRegisters
        self._dsc_display_info: DSCDisplay = display_info

        # Contains information/expected data that needs to be verified with the driver programmed values.
        self.test_data: Dict[TestDataKey, Any] = test_data

        self._pps_calculator: Optional[PictureParameterSetCalculator] = None
        self._pipe_dss_ctl_1_dict: Dict[str, PipeDssCtlOneRegister] = {}
        self._pipe_dss_ctl_2_dict: Dict[str, PipeDssCtlTwoRegister] = {}
        self._pipe_dss_ctl_3_dict: Dict[str, PipeDssCtlThreeRegister] = {}

    ##
    # @brief        Property to Access the Private Member Variable Outside of Class.
    # @return       Returns graphics index in which the display is plugged in small letters. E.g. gfx_0, gfx_1
    @property
    def gfx_index(self) -> str:
        return self._dsc_display_info.gfx_index

    ##
    # @brief        Property to Access the Private Member Variable Outside of Class.
    # @return       Returns the Port Name on Which the Display is Plugged From Display Object.
    @property
    def port_name(self) -> str:
        return self._dsc_display_info.port_name

    ##
    # @brief        Property to Access the Private Member Variable Outside of Class.
    # @return       Returns the type of Virtual DP Peer Device enumerated.
    @property
    def virtual_dp_peer_device(self) -> VirtualDisplayportPeerDevice:
        return self._dsc_display_info.virtual_dp_peer_device

    ##
    # @brief        Property to Access the Private Member Variable Outside of Class.
    # @return       Returns True if big joiner is enabled else False
    @property
    def is_big_joiner_enabled(self) -> bool:
        return self._pps_calculator.is_big_joiner_enabled

    ##
    # @brief        Property to Access the Private Member Variable Outside of Class.
    # @return       Returns the Expected Picture Parameter Set Values for the DP DSC Display Which is Initialized.
    @property
    def calculated_pic_parameter_set(self) -> DSCRequiredPictureParameterSet:

        if self._pps_calculator is None:
            assert False, 'PictureParameterSetCalculator is Not Initialized.'

        return self._pps_calculator.calculated_pic_parameter_set

    ##
    # @brief        Property to Get the Number of Pipes That are Used to Drive the Display Based on Slice Count.
    # @return       no_of_pipes: int
    #                   Returns the no of pipes occupied by the display based on no. of vdsc instances.
    @property
    def no_of_pipes_required(self) -> int:
        if self.vdsc_instances >= 8:
            no_of_pipes = 4
        elif self.vdsc_instances >= 4:
            no_of_pipes = 2
        else:
            no_of_pipes = 1

        return no_of_pipes

    ##
    # @brief        Property to get the number of vdsc instances enabled.
    # @return       Returns no.of vdsc instances enabled for the display.
    @property
    def vdsc_instances(self) -> int:
        return self.calculated_pic_parameter_set.vdsc_instances

    ##
    # @brief        Property to get the picture width from pps
    # @return       Returns picture width of the display
    @property
    def pic_width(self) -> int:
        return self.calculated_pic_parameter_set.pic_width

    ##
    # @brief        Property to get the slice count from pps
    # @return       Returns the slice count from pps
    @property
    def slice_count(self) -> int:
        return self.calculated_pic_parameter_set.slice_count

    ##
    # @brief        Private Member Function Which Acts as Wrapper to Verify Pipe DSS CTL Registers(One/Two) by
    #               Comparing the Expected Value Against Register Programmed Value.
    #               Big Joiner Case is also Handled Where Pipe DSS CTL Registers(One/Two) Happens For the Slave Pipe.
    # @return       is_success: bool
    #                   Returns True If Both Pipe DSS CTL One Pipe DSS CTL Two Registers are Matching With the
    #                   Expected Values, False Otherwise.
    def _verify_pipe_dss_ctl_registers(self) -> bool:
        is_success: bool = True
        gfx_index, platform = self._dsc_display_info.gfx_index, self._dsc_display_info.platform

        for pipe, expected_pipe_dss_ctl_1_reg in self._pipe_dss_ctl_1_dict.items():
            transcoder = self._dsc_display_info.transcoder_list[0]

            actual_pipe_dss_ctl_1_reg = PipeDssCtlOneRegister()
            reg_name = actual_pipe_dss_ctl_1_reg.fill_actual_pipe_dss_ctl_one_reg(gfx_index, platform, pipe, transcoder)

            logging.info("Verifying {} Register".format(reg_name))
            is_success &= (expected_pipe_dss_ctl_1_reg == actual_pipe_dss_ctl_1_reg)

        for pipe, expected_pipe_dss_ctl_2_reg in self._pipe_dss_ctl_2_dict.items():
            transcoder = self._dsc_display_info.transcoder_list[0]

            actual_pipe_dss_ctl_2_reg = PipeDssCtlTwoRegister()
            reg_name = actual_pipe_dss_ctl_2_reg.fill_actual_pipe_dss_ctl_two_reg(gfx_index, platform, pipe, transcoder)

            logging.info("Verifying {} Register".format(reg_name))
            is_success &= (expected_pipe_dss_ctl_2_reg == actual_pipe_dss_ctl_2_reg)

        # Pipe DSS CTL3 register is present only in ELG
        if platform in ['ELG']:
            for pipe, expected_pipe_dss_ctl_3_reg in self._pipe_dss_ctl_3_dict.items():
                actual_pipe_dss_ctl_3_reg = PipeDssCtlThreeRegister()
                reg_name = actual_pipe_dss_ctl_3_reg.fill_actual_pipe_dss_ctl_three_reg(gfx_index, platform, pipe)

                logging.info("Verifying {} Register".format(reg_name))
                is_success &= (expected_pipe_dss_ctl_3_reg == actual_pipe_dss_ctl_3_reg)

        return is_success

    ##
    # @brief        Private Member Function Which Verifies DSC Picture Parameter Set by Comparing Register Values
    #               Against the Expected DSC Picture Parameter Set. Need to Invoked From _verify_dsc_engine()
    # @param[in]    pipe_name: str
    #                   Pipe Name For Which DSC Parameters has to be Verified.
    # @param[in]    expected_pps: DSCPictureParameterSet
    #                   Calculated DSC Parameters Which Needs to Checked Against the Programmed Values by Driver.
    # @return       is_success: bool
    #                   Returns True if DSC Parameters Programmed Matches with the Expected Parameters, False Otherwise
    def _verify_dsc_parameters(self, pipe_name: str, expected_pps: DSCPictureParameterSet) -> bool:
        is_success: bool = True
        gfx_index, platform_name = self._dsc_display_info.gfx_index, self._dsc_display_info.platform

        engines_to_verify: List[DSCEngine] = []

        if self._pipe_dss_ctl_2_dict[pipe_name].is_left_vdsc_engine_enabled:
            engines_to_verify.append(DSCEngine.LEFT)

        if self._pipe_dss_ctl_2_dict[pipe_name].is_right_vdsc_engine_enabled:
            engines_to_verify.append(DSCEngine.RIGHT)

        if self._pipe_dss_ctl_2_dict[pipe_name].is_second_vdsc_engine_enabled:
            engines_to_verify.append(DSCEngine.MIDDLE)

        for dsc_engine in engines_to_verify:
            actual_engine_pps = DSCPictureParameterSet()
            actual_engine_pps.fill_actual_pps(gfx_index, platform_name, pipe_name, dsc_engine)

            logging.info("Verifying DSC Picture Parameter Set for DSC {} Engine".format(dsc_engine.name))
            if actual_engine_pps == expected_pps:
                logging.info(f"Expected and Actual Picture Parameter Set for {dsc_engine.name} Engine are Matching")
            else:
                gdhm.report_driver_bug_di(f'[Display_Interfaces][DSC] Expected and Actual PPS values are mismatching for {dsc_engine.name} Engine')
                logging.error(f"Expected and Actual Picture Parameter Set for {dsc_engine.name} Engine are Mismatching")
                is_success = False

        return is_success

    ##
    # @brief        Private Member Function Which Acts as a Wrapper to Verify DSC PPS Parameters Using the Computed
    #               PPS Parameter. Big Joiner Case is also Handled Here Where Slave Pipe's PPS Parameters also Verified.
    # @return       is_success: bool
    #                   Returns True Register Programmed PPS Matches with Expected/Computed PPS
    def _verify_dsc_engine(self) -> bool:
        expected_pic_parameter_set = DSCPictureParameterSet.from_calculated_pps(self.calculated_pic_parameter_set)
        is_success: bool = True

        for pipe_name in self._dsc_display_info.pipe_list:
            logging.info("Verifying PIPE_{} DSC Picture Parameter Set".format(pipe_name))
            is_success &= self._verify_dsc_parameters(pipe_name, expected_pic_parameter_set)

        return is_success

    ##
    # @brief        Private Member Function Helps to Set the Expected Pipe DSS CTL Registers Values For Each Pipe and
    #               Store the Values in Dictionary Format with Key as Pipe Name.
    #               This Function can be overridden by the Inherited class if the Implementation is not Suited for a
    #               Particular Display Type. This Implementation is Applicable for EDP, DP and HDMI DSC Displays.
    # @return       Returns bool. Refer derived class for details
    def _set_expected_pipe_dss_ctl_dict(self) -> None:
        is_master = True
        picture_width = self._pps_calculator.timing_info.hActive

        for pipe_name in self._dsc_display_info.pipe_list:
            pipe_dss_ctl1_reg = PipeDssCtlOneRegister()
            pipe_dss_ctl1_reg.fill_expected_pipe_dss_ctl_one_reg(pipe_name, is_master, self.vdsc_instances)

            pipe_dss_ctl2_reg = PipeDssCtlTwoRegister()
            pipe_dss_ctl2_reg.fill_expected_pipe_dss_ctl_two_reg(self.vdsc_instances)

            self._pipe_dss_ctl_1_dict[pipe_name] = pipe_dss_ctl1_reg
            self._pipe_dss_ctl_2_dict[pipe_name] = pipe_dss_ctl2_reg

            # Pipe DSS CTL3 register is present only in ELG
            if self._dsc_display_info.platform in ['ELG']:
                pipe_dss_ctl3_reg = PipeDssCtlThreeRegister()
                pipe_dss_ctl3_reg.fill_expected_pipe_dss_ctl_three_reg(pipe_name, picture_width, self.slice_count)
                self._pipe_dss_ctl_3_dict[pipe_name] = pipe_dss_ctl3_reg

            # First pipe will always be a master pipe in case of big joiner
            # Alternate pipe will be a master pipe in case of ultra joiner i.e. A and C will be big joiner which is the
            # only possibility
            is_master = not is_master

    ##
    # @brief        Private Member Function that verifies PPS Header information are sent in the correct order.
    # @return       is_success: bool
    #                   Returns True if the Header information read from Video Data Island Packet Picture Parameter Set
    #               registers matches with the PPS values that is calculated.
    def _verify_video_dip_pps_data(self):
        is_success = True
        gfx_index, platform_name = self._dsc_display_info.gfx_index, self._dsc_display_info.platform
        expected_pps_sdp = PictureParameterSDP.from_calculated_pps_sdp(self.calculated_pic_parameter_set)

        for transcoder in self._dsc_display_info.transcoder_list:
            logging.info("Verifying Video_DIP_PPS_DATA_{} DSC Picture Parameter Set".format(transcoder))

            video_dip_pps_data_byte_array = DSCHelper.get_video_dip_pps_byte_array(gfx_index, platform_name, transcoder)
            actual_pps_sdp = PictureParameterSDP.from_byte_array(video_dip_pps_data_byte_array)

            is_success &= (actual_pps_sdp == expected_pps_sdp)

        return is_success

    ##
    # @brief        Private Member Function which is invoked from test script To verify Common SDP TL Programming
    # @return       is_success: bool
    #                   Returns True If Enabled, else False
    def _verify_common_sdp_enable(self) -> bool:
        is_success = True
        gfx_index, platform_name = self._dsc_display_info.gfx_index, self._dsc_display_info.platform

        if platform_name in COMMON_SDP_TL_SUPPORTED_PLATFORMS:
            gfx_index, port = self._dsc_display_info.gfx_index, self._dsc_display_info.port_name
            display_base = DisplayBase(port, gfx_index=gfx_index)

            pipe, _, transcoder = display_base.GetPipeDDIAttachedToPort(port, True, gfx_index)
            pipe = pipe[-1].upper()
            register_name: str = 'CMN_SDP_TL_' + pipe
            cmn_sdp_tl = MMIORegister.read("CMN_SDP_TL_REGISTER", register_name, platform_name, gfx_index=gfx_index)

            if bool(cmn_sdp_tl.enable) is True:
                logging.info("COMMON_SDP_TRANSMISSION_LINE.Enable: Expected: [Enabled]  Actual: [Enabled]")
            else:
                logging.error("COMMON_SDP_TRANSMISSION_LINE.Enable: Expected: [Enabled]  Actual: [Disabled]")
                is_success = False

            display_and_adapter_info = DSCHelper.display_config.get_display_and_adapter_info_ex(port, gfx_index)
            if type(display_and_adapter_info) is list:
                display_and_adapter_info = display_and_adapter_info[0]

            timing_info: DisplayTimings = DSCHelper.get_display_timing_from_qdc(display_and_adapter_info)

            ## v_min = timing_info.vTotal  TimingInfo gives Vtotal as 0. Below is the WA to get vtotal
            if platform_name in machine_info.PRE_GEN_16_PLATFORMS:
                register_name2: str = 'TRANS_VTOTAL_' + pipe
                v_total = MMIORegister.read('TRANS_VTOTAL_REGISTER', register_name2, platform_name, gfx_index=gfx_index)
                v_min = v_total.vertical_total + 1
            else:
                register_name2: str = 'TRANS_VRR_VMAX_' + pipe
                vrr_vmax = MMIORegister.read('TRANS_VRR_VMAX_REGISTER', register_name2, platform_name,
                                            gfx_index=gfx_index)
                v_min = vrr_vmax.vrr_vmax + 1

            # Get Vactive
            v_active = timing_info.vActive

            if cmn_sdp_tl.base_transmission_line < (v_min - v_active):
                logging.info("SDP Base TL {0} is less than Vmin {1} - VActive {2}".format(cmn_sdp_tl.base_transmission_line, v_min, v_active))
            else:
                logging.error("SDP Base TL {0} is not less than Vmin {1} - VActive {2}".format(cmn_sdp_tl.base_transmission_line, v_min, v_active))
                is_success = False

        return is_success

    ##
    # @brief        Abstract Method, Needs to be Implemented in the Derived Class as per the Requirement of Display
    #               Technology. This Serves as a Wrapper for All the Verification that are part of DSC Verification.
    #               Need to be Invoked From the Test Script Using Verifier Object.
    # @return       Returns bool. Refer derived class for details
    @abstractmethod
    def verify_dsc_programming(self) -> bool:
        pass

    ##
    # @brief        Class Method to Get the Appropriate DSC Verifier based on the Display Technology.
    # @param[in]    display_info: DSCDisplay
    #                   Contains Display Type Which Helps to Create Appropriate DSC Verifier.
    # @param[in]    test_data: Dict[TestDataKey, Any]
    #                   Contains any data that is needed for verification from the test scripts can be passed using this
    #                   dictionary. Key has to be of type TestDataKey. Value can be anything.
    # @return       dsc_verifier: DisplayStreamCompressionVerifier
    #                   Returns Verifier Based on the Display Type.
    @classmethod
    def get_dsc_verifier(cls, display_info: DSCDisplay, test_data: Dict[TestDataKey, Any]
                         ) -> DisplayStreamCompressionVerifier:

        if display_info.display_type == DisplayType.DISPLAY_PORT:
            dsc_verifier = DisplayPortDSCVerifier(display_info, test_data)
        elif display_info.display_type == DisplayType.EMBEDDED_DISPLAY_PORT:
            dsc_verifier = EdpDSCVerifier(display_info, test_data)
        elif display_info.display_type == DisplayType.MIPI_DISPLAY:
            dsc_verifier = MipiDSCVerifier(display_info, test_data)
        elif display_info.display_type == DisplayType.HDMI_DISPLAY:
            dsc_verifier = HdmiDSCVerifier(display_info, test_data)
        else:
            dsc_verifier = None
            gdhm.report_bug(
                title="[Interfaces][DP_DSC] Invalid/Unknown DisplayType passed in dsc verifier",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            assert True, "Unknown Display Type in Get DSC Verifier."

        return dsc_verifier


##
# @brief        EdpDSCVerifier is Inherited From DisplayStreamCompressionVerifier And Verifies DSC Programming For EDP.
class EdpDSCVerifier(DisplayStreamCompressionVerifier):

    # @brief        Initialize the Display Stream Compression Verifier Using the EDP DSC Display Information.
    # @param[in]    edp_dsc_display: DSCDisplay
    #                   Contains all Basic Information Related to the EDP DSC Display.
    # @param[in]    test_data: Dict[TestDataKey, Any]
    #                   Contains any data that is needed for verification from the test scripts can be passed using this
    #                   dictionary. Key has to be of type TestDataKey. Value can be anything.
    def __init__(self, edp_dsc_display: DSCDisplay, test_data: Dict[TestDataKey, Any]) -> None:
        super().__init__(edp_dsc_display, test_data)

    # @brief        Private Member Function Helps to Initialize the Environment/Variables that are Required for DSC
    #               Programming Verification.
    # @return       None
    def _initialize_expected_parameters(self) -> None:
        self.set_pps_calculator()
        self._pps_calculator.set_dsc_picture_parameter_set()

        self._dsc_display_info.update_pipe_list(self.no_of_pipes_required)
        self._set_expected_pipe_dss_ctl_dict()

    ##
    # @brief        Sets the PPS Calculator to EDP PPS Calculator.
    # @return       None
    def set_pps_calculator(self) -> None:
        self._pps_calculator = EdpPictureParameterSetCalculator(self._dsc_display_info, self.test_data)

    ##
    # @brief        Private Member Function Which Acts as a Wrapper to Verify FEC Enable Bit For Each of the
    #               Transcoder Connected to the Display.
    # @return       is_success: bool
    #                   Returns True if FEC Enable Bit is Set in All the Transcoder/DDI Connected to the Display, False
    #                   Otherwise.
    def _verify_fec_enable_bit(self) -> bool:
        is_success: bool = True
        gfx_index, platform = self._dsc_display_info.gfx_index, self._dsc_display_info.platform

        gfx_index, port = self._dsc_display_info.gfx_index, self._dsc_display_info.port_name
        display_and_adapter_info = DSCHelper.display_config.get_display_and_adapter_info_ex(port, gfx_index)
        if type(display_and_adapter_info) is list:
            display_and_adapter_info = display_and_adapter_info[0]

        is_fec_supported = DSCHelper.is_fec_supported(display_and_adapter_info)
        if (self._dsc_display_info.display_type == DisplayType.DISPLAY_PORT) and is_fec_supported is False:
            logging.error("[Panel Issue] - FEC is not supported by DP DSC Display")
            gdhm.report_bug(
                title=f"[Interfaces][DP_DSC] FEC is not supported by DP DSC Display",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            return False

        link_rate: float = dpcd_helper.DPCD_getLinkRate(self._dsc_display_info.target_id)
        logging.debug('Link Rate Trained by Driver: {}'.format(link_rate))

        # FEC Enable bit in DP_TP_CTL Register won't be set by driver for DP 2.1 displays as FEC is inherent to the
        # protocol and FEC will be enabled by the HW. Note: HW won't set this bit.
        if link_rate >= 10:
            logging.info("Skipping FEC Enable Bit (DP_TP_CTL register) Verification for DP2.1 Displays")
            return is_success

        for transcoder, ddi in zip(self._dsc_display_info.transcoder_list, self._dsc_display_info.ddi_list):
            status = True

            # Forward Error Correction (FEC) coding for Display Ports (DP).
            # For pre Gen11.5 platforms DP_TP_CTL is based on DDI and post that it's mapped to transcoder.
            transcoder_ddi = ddi[-1] if platform in ['GLK', 'ICLLP', 'EHL', 'JSL'] else transcoder
            is_fec_enabled = DSCHelper.get_fec_status(gfx_index, platform, transcoder_ddi)

            if is_fec_supported is True and is_fec_enabled is True:
                logging.info("FEC bit is Enabled in transcoder_ddi: {}".format(transcoder_ddi))
            elif is_fec_supported is True and is_fec_enabled is False:
                logging.error("[Driver Issue] - FEC bit is Disabled in transcoder_ddi: {}".format(transcoder_ddi))
                gdhm.report_bug(
                    title=f"[Interfaces][DP_DSC] FEC bit is Disabled in transcoder_ddi: {transcoder_ddi}",
                    problem_classification=gdhm.ProblemClassification.OTHER,
                    component=gdhm.Component.Test.DISPLAY_INTERFACES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                status = False

            # Below two cases will occur only for EDP DSC displays as FEC is not mandatory for EDP DSC displays but
            # mandatory for DP DSC displays
            elif is_fec_supported is False and is_fec_enabled is True:
                logging.error(f"[Driver Issue] - FEC bit is Enabled in transcoder_ddi: {transcoder_ddi} for Non-FEC"
                              f"EDP DSC Display")
                gdhm.report_bug(
                    title=f"[Interfaces][DP_DSC] FEC bit is Enabled in transcoder_ddi: {transcoder_ddi} for Non-FEC"
                          f"EDP DSC Display",
                    problem_classification=gdhm.ProblemClassification.OTHER,
                    component=gdhm.Component.Test.DISPLAY_INTERFACES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                status = False
            elif is_fec_supported is False and is_fec_enabled is False:
                logging.info("Skipping FEC Enable Status Verification as FEC is not Supported by the EDP DSC Display")

            is_success &= status

        return is_success

    ##
    # @brief        Private Member Function Which Acts as a Wrapper to Verify FEC_READY bit is set in the
    #               FEC_CONFIGURATION DPCD Register.
    # @return       is_fec_read_bit_set: bool
    #                   Returns True if FEC Configuration is Enabled, False Otherwise.
    def _verify_fec_ready_bit(self):
        is_success = True

        gfx_index, port = self._dsc_display_info.gfx_index, self._dsc_display_info.port_name
        display_and_adapter_info = DSCHelper.display_config.get_display_and_adapter_info_ex(port, gfx_index)
        if type(display_and_adapter_info) is list:
            display_and_adapter_info = display_and_adapter_info[0]

        is_fec_supported = DSCHelper.is_fec_supported(display_and_adapter_info)
        if (self._dsc_display_info.display_type == DisplayType.DISPLAY_PORT) and is_fec_supported is False:
            logging.error("[Panel Issue] - FEC is not supported by DP DSC Displays")
            gdhm.report_bug(
                title="[Interfaces][DP_DSC]  FEC is not supported by DP DSC Displays",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            return False

        link_rate: float = dpcd_helper.DPCD_getLinkRate(self._dsc_display_info.target_id)
        logging.debug('Link Rate Trained by Driver: {}'.format(link_rate))

        # FEC Ready bit in FEC Configuration DPCD Register is don't care for DP2.0 Displays
        if link_rate >= 10:
            logging.info("Skipping FEC Ready Bit Verification for DP2.0 Displays")
            return is_success

        is_fec_ready_bit_set = DSCHelper.get_fec_ready_status(display_and_adapter_info)

        if is_fec_supported is True and is_fec_ready_bit_set is True:
            logging.info("FEC Ready Bit is Set in FEC CONFIGURATION DPCD Register")
        elif is_fec_supported is True and is_fec_ready_bit_set is False:
            logging.error("[Driver Issue] - FEC Ready Bit is not Set in FEC CONFIGURATION DPCD REGISTER")
            gdhm.report_bug(
                title="[Interfaces][DP_DSC]  FEC Ready Bit is not Set in FEC CONFIGURATION DPCD REGISTER",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            is_success = False

        # Below two cases will occur only for EDP DSC displays as FEC is not mandatory for EDP DSC displays but
        # mandatory for DP DSC displays
        elif is_fec_supported is False and is_fec_ready_bit_set is True:
            logging.error("[Driver Issue] - FEC Ready Bit is Set in FEC CONFIGURATION DPCD Register for Non-FEC EDP DSC"
                          " Display")
            gdhm.report_bug(
                title="[Interfaces][EDP_DSC] - FEC Ready Bit is Set in FEC CONFIGURATION DPCD Register for Non-FEC EDP "
                      "DSC Display",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            is_success = False
        elif is_fec_supported is False and is_fec_ready_bit_set is False:
            logging.info("Skipping FEC Ready Bit Verification for EDP DSC Display as FEC is not supported in panel")

        return is_success

    ##
    # @brief        Public Member Function Which is Invoked From Test Script to Invoke All EDP DSC Related Verifications
    # @return       is_success: bool
    #                   Returns True If All DSC Related Verification is Success, False Otherwise.
    def verify_dsc_programming(self) -> bool:
        is_success = True
        is_fec_verification_required = False
        display_type, platform = self._dsc_display_info.display_type, self._dsc_display_info.platform

        self._initialize_expected_parameters()

        if (display_type == DisplayType.EMBEDDED_DISPLAY_PORT) and (platform not in EDP_FEC_UNSUPPORTED_PLATFORMS):
            gfx_index, port_name = self._dsc_display_info.gfx_index, self._dsc_display_info.port_name
            edp_dpcd_rev = DSCHelper.read_dpcd(gfx_index, port_name, DPCDOffsets.EDP_DPCD_REV)[0]
            if edp_dpcd_rev >= 0x5:
                is_fec_verification_required = True
        elif display_type == DisplayType.DISPLAY_PORT:
            is_fec_verification_required = True

        if is_fec_verification_required is True:
            is_success &= self._verify_fec_enable_bit()
            is_success &= self._verify_fec_ready_bit()

        is_success &= self._verify_pipe_dss_ctl_registers()
        is_success &= self._verify_dsc_engine()

        # Adding Video DIP PPS register verification only gen12+ platforms as I don't see any ROI for pre-gen12
        if platform not in machine_info.PRE_GEN_12_PLATFORMS:
            is_success &= self._verify_video_dip_pps_data()
            is_success &= self._verify_common_sdp_enable()

        return is_success

##
# @brief        DisplayPortDSCVerifier is Inherited From EdpDSCVerifier as Most of the Verification Logic For DP is
#               is Similar to Displayport
class DisplayPortDSCVerifier(EdpDSCVerifier):

    ##
    # @brief        Initialize the Display Stream Compression Verifier Using the DP DSC Display Information.
    # @param[in]    dp_dsc_display: DSCDisplay
    #                   Contains all Basic Information Related to the DP DSC Display.
    # @param[in]    test_data: Dict[TestDataKey, Any]
    #                   Contains any data that is needed for verification from the test scripts can be passed using this
    #                   dictionary. Key has to be of type TestDataKey. Value can be anything.
    def __init__(self, dp_dsc_display: DSCDisplay, test_data: Dict[TestDataKey, Any]) -> None:
        super().__init__(dp_dsc_display, test_data)

    ##
    # @brief        Sets the PPS Calculator to DP PPS Calculator.
    # @return       None
    def set_pps_calculator(self) -> None:
        self._pps_calculator = DpPictureParameterSetCalculator(self._dsc_display_info, self.test_data)

    ##
    # @brief        Property to if Big Joiner is Enabled Based on the Number of Pipes Required to Drive the Display.
    # @return       is_big_joiner_enabled: bool
    #                   Returns True if big joiner is enabled else False
    @property
    def is_big_joiner_enabled(self) -> bool:
        return self._pps_calculator.is_big_joiner_enabled

    ##
    # @brief        Private Member Function to Which Acts as a Wrapper to Verify PPS Enable Bit in Video Data Island
    #               Packet Register For Each of the Transcoder Connected to the Display.
    # @return       is_success: bool
    #                   Returns True if PPS Enable Bit is Set in All the Transcoder Connected to the Display, False
    #                   Otherwise.
    def _verify_vdip_pps_enable_bit(self) -> bool:
        is_success: bool = True
        gfx_index, platform = self._dsc_display_info.gfx_index, self._dsc_display_info.platform

        for transcoder in self._dsc_display_info.transcoder_list:
            is_success &= DSCAdditionalRegVerifier.verify_vdip_pps_status(gfx_index, platform, transcoder)

        return is_success

    ##
    # @breif        Private Member Function to
    def _verify_decompression_enable_bit(self) -> bool:
        is_success = is_dsc_enabled = False

        if self.virtual_dp_peer_device == VirtualDisplayportPeerDevice.VIRTUAL_DP_SINK_PEER_DEVICE:
            ret_status, dsc_enable = DisplayPort().read_dpcd(self.port_name, False, 1, DPCDOffsets.DSC_ENABLE,
                                                             self._dsc_display_info.display_rad_info.NodeRAD)
            assert ret_status, f"DPCD Read failed for address: {DPCDOffsets.DSC_ENABLE}"
            decompression_enable = DSCHelper.extract_bits(dsc_enable[0], 1, 0)
            is_dsc_enabled = True if decompression_enable == 1 else False

        elif self.virtual_dp_peer_device == VirtualDisplayportPeerDevice.VIRTUAL_DP_PEER_DEVICE_NOT_SUPPORTED:
            is_dsc_enabled = DSCHelper.is_vdsc_enabled_in_panel(self.gfx_index, self.port_name)

        if is_dsc_enabled is True:
            logging.info("DSC Decompression bit is set in the device as expected")
            is_success = True
        else:
            gdhm.report_driver_bug_di(f"[Display_Interfaces][VDSC] DSC Decompression bit is not set in {DPCDOffsets.DSC_ENABLE} DPCD")
            logging.error(f"[Driver Issue] - DSC Decompression bit is not set in {DPCDOffsets.DSC_ENABLE} DPCD")

        return is_success

    ##
    # @brief        Public Member Function Which is Invoked From Test Script to Invoke All DP DSC Related Verifications.
    # @return       is_success: bool
    #                   Returns True If All DSC Related Verification is Success, False Otherwise.
    def verify_dsc_programming(self) -> bool:
        is_success: bool = self._verify_vdip_pps_enable_bit()
        is_success &= self._verify_decompression_enable_bit()
        is_success &= super().verify_dsc_programming()

        return is_success


##
# @brief        MipiDSCVerifier is Inherited From DisplayStreamCompressionVerifier And Verifies DSC Programming For
#               Mipi Display.
class MipiDSCVerifier(DisplayStreamCompressionVerifier):

    ##
    # @brief        Initialize the Display Stream Compression Verifier Using the MIPI DSC Display Information.
    # @param[in]    mipi_dsc_display: DSCDisplay
    #                   Contains all Basic Information Related to the MIPI DSC Display.
    # @param[in]    test_data: Dict[TestDataKey, Any]
    #                   Contains any data that is needed for verification from the test scripts can be passed using this
    #                   dictionary. Key has to be of type TestDataKey. Value can be anything.
    def __init__(self, mipi_dsc_display: DSCDisplay, test_data: Dict[TestDataKey, Any]) -> None:
        super().__init__(mipi_dsc_display, test_data)
        self.mipi_helper: MipiHelper = MipiHelper(self._dsc_display_info.platform.lower())

    ##
    # @brief        Private Member Function Helps to Initialize the Environment/Variables that are Required for DSC
    #               Programming Verification.
    # @return       None
    def _initialize_expected_parameters(self) -> None:
        self.set_pps_calculator()
        self._pps_calculator.set_dsc_picture_parameter_set()

        if self.mipi_helper.dual_link == 1:
            self._dsc_display_info.update_transcoder_list('DSI1')

        self._set_expected_pipe_dss_ctl_dict()

    ##
    # @brief        Sets the PPS Calculator to MIPI PPS Calculator.
    # @return       None
    def set_pps_calculator(self) -> None:
        self._pps_calculator = MipiPictureParameterSetCalculator(self._dsc_display_info, self.test_data)

    ##
    # @brief        Property to Access the Private Member Variable Outside of Class.
    # @return       Returns the Expected Picture Parameter Set Values for the MIPI DSC Display Which is Initialized.
    @property
    def expected_pic_parameter_set(self) -> DSCRequiredPictureParameterSet:
        return self._pps_calculator.calculated_pic_parameter_set

    ##
    # @brief        Private Member Function Acts as a Wrapper to Get Expected the Pipe DSS CTL Register Values For Each
    #               Pipe and Store the Values in Dictionary Format with Key as Pipe Name.
    # @return       None
    def _set_expected_pipe_dss_ctl_dict(self) -> None:
        port, pipe = self._dsc_display_info.port_name, self._dsc_display_info.pipe_list[0]

        pipe_dss_ctl1_reg = PipeDssCtlOneRegister()
        pipe_dss_ctl1_reg.fill_expected_pipe_dss_ctl_one_reg_mipi(self.mipi_helper)

        pipe_dss_ctl2_reg = PipeDssCtlTwoRegister()
        pipe_dss_ctl2_reg.fill_expected_pipe_dss_ctl_two_reg_mipi(port, self.mipi_helper)

        self._pipe_dss_ctl_1_dict[pipe] = pipe_dss_ctl1_reg
        self._pipe_dss_ctl_2_dict[pipe] = pipe_dss_ctl2_reg

    ##
    # @brief        Private Member Function Which Acts as a Wrapper And Verifies Pixel Format Programmed in Transcoder.
    #               In case of Dual Link MIPI Checks Both the Transcoder.
    # @return       is_success: bool
    #                   Returns True If Pixel Format is Compressed, False Otherwise.
    def _verify_pixel_format(self) -> bool:
        is_success: bool = True

        gfx_index, platform = self._dsc_display_info.gfx_index, self._dsc_display_info.platform
        for transcoder in self._dsc_display_info.transcoder_list:
            is_success &= DSCAdditionalRegVerifier.verify_pixel_format_mipi(gfx_index, platform, transcoder)

        return is_success

    ##
    # @brief        Public Member Function Which is Invoked From Test Script to Invoke All MIPI DSC Related
    #               Verifications
    # @return       is_success: bool
    #                   Returns True If All DSC Related Verification is Success, False Otherwise.
    def verify_dsc_programming(self) -> bool:
        self._initialize_expected_parameters()

        is_success: bool = self._verify_pixel_format()

        self._pps_calculator.set_dsc_picture_parameter_set()

        is_success &= self._verify_pipe_dss_ctl_registers()
        is_success &= self._verify_dsc_engine()

        return is_success


##
# @brief        HdmiDSCVerifier is Inherited From DisplayStreamCompressionVerifier And Verifies DSC Programming For HDMI
class HdmiDSCVerifier(DisplayStreamCompressionVerifier):

    ##
    # @brief        Initialize the Display Stream Compression Verifier Using the HDMI DSC Display Information.
    # @param[in]    hdmi_dsc_display: DSCDisplay
    #                   Contains all Basic Information Related to the HDMI DSC Display.
    # @param[in]    test_data: Dict[TestDataKey, Any]
    #                   Contains any data that is needed for verification from the test scripts can be passed using this
    #                   dictionary. Key has to be of type TestDataKey. Value can be anything.
    def __init__(self, hdmi_dsc_display: DSCDisplay, test_data: Dict[TestDataKey, Any]) -> None:
        super().__init__(hdmi_dsc_display, test_data)

    ##
    # @brief        Sets the PPS Calculator to MIPI PPS Calculator.
    # @return       None
    def set_pps_calculator(self) -> None:
        self._pps_calculator = HDMIPictureParameterSetCalculator(self._dsc_display_info, self.test_data)

    ##
    # @brief        Property to get the number of vdsc instances enabled.
    # @return       Returns no.of vdsc instances enabled for the display.
    @property
    def vdsc_instances(self) -> int:
        return self.calculated_pic_parameter_set.vdsc_instances

    ##
    # @brief        Property to Get the Number of Pipes That are Used to Drive the Display Based on Slice Count.
    # @return       no_of_pipes: int
    #                   Returns the no of pipes occupied by the display based on no. of vdsc instances.
    @property
    def no_of_pipes_required(self) -> int:
        no_of_pipes = 2 if self.vdsc_instances > 2 else 1
        return no_of_pipes

    # @brief        Private Member Function Helps to Initialize the Environment/Variables that are Required for DSC
    #               Programming Verification.
    # @return       None
    def _initialize_expected_parameters(self) -> None:
        self.set_pps_calculator()
        self._pps_calculator.set_dsc_picture_parameter_set()
        self._dsc_display_info.update_pipe_list(self.no_of_pipes_required)
        self._set_expected_pipe_dss_ctl_dict()

    def verify_dsc_programming(self) -> bool:
        self._initialize_expected_parameters()

        is_success: bool = self._verify_pipe_dss_ctl_registers()
        is_success &= self._verify_dsc_engine()
        is_success &= self._verify_video_dip_pps_data()

        return is_success


##
# @brief        Exposed API to Verify All DSC Related Programming.
# @param[in]    gfx_index: str
#                   Represents the Graphics Adapter in Which the Display is Plugged. E.g. 'gfx_0', 'gfx_1'
# @param[in]    port: str
#                   Port Name in Which the DSC Display is Plugged.
# @param[in]    test_data: Optional[Dict[TestDataKey, Any]]
#                   Contains any data that is needed for verification from the test scripts can be passed using this
#               dictionary. Key has to be of type TestDataKey. Value can be anything.
# @param[in]    slave_port: Optional[str]
#                   Contains slave port name in case of SST Tiled DSC displays.
# @return       is_success: bool
#                   Returns True if All the Verification Related to DSC is Success, False Otherwise.
def verify_dsc_programming(gfx_index: str, port: str, test_data: Optional[Dict[TestDataKey, Any]] = None,
                           slave_port: Optional[str] = '') -> bool:
    if bool(test_data) is False:
        test_data = {}

    is_dsc_verification_required = is_success = True
    dsc_display = DSCDisplay(gfx_index, port, slave_port)
    dsc_display.initialize_display()

    is_dsc_supported_by_immediate_device  = DSCHelper.is_vdsc_supported_in_panel(gfx_index, port)
    is_dsc_pass_through_supported_by_immediate_device = DSCHelper.is_vdsc_pass_through_supported(gfx_index, port)

    if is_dsc_supported_by_immediate_device is False and is_dsc_pass_through_supported_by_immediate_device is False:
        logging.info("Skipping DSC verification as immediate branch/sink device doesn't support DSC or pass-through")
        return is_success

    is_dsc_required = DSCHelper.is_vdsc_required(gfx_index, port,
                                                 test_data.setdefault(TestDataKey.COLOR_FORMAT, ColorFormat.RGB))
    is_vdsc_enabled = DSCHelper.is_vdsc_enabled_in_driver(gfx_index, port)

    dsc_verifier = DisplayStreamCompressionVerifier.get_dsc_verifier(dsc_display, test_data)

    is_dp_2_1 = (DSCHelper.read_dpcd(gfx_index, port, DPCDOffsets.MAIN_LINK_CHANNEL_ENCODING_CAP)[0] == 3 or
                 DSCHelper.read_dpcd(gfx_index, port, DPCDOffsets.EXT_MAIN_LINK_CHANNEL_ENCODING_CAP)[0] == 3)

    # DSC is always enabled for eDP(Legacy), MIPI, Tiled, MST and DP 2.1(LNL+) Displays
    dsc_required_check = not (dsc_display.is_mst_display or
                              dsc_display.is_tiled_display or
                              dsc_display.display_type == DisplayType.EMBEDDED_DISPLAY_PORT or
                              dsc_display.display_type == DisplayType.MIPI_DISPLAY or
                              (is_dp_2_1 and dsc_display.platform in ['LNL', 'PTL', 'NVL']))

    if dsc_required_check is True:
        if is_dsc_required is True and is_vdsc_enabled is True:
            is_dsc_verification_required = True
        elif is_dsc_required is True and is_vdsc_enabled is False:
            is_dsc_verification_required = is_success = False
            logging.error(f"[Driver Issue] - DSC Should be Enabled for Display Plugged at: {port} on {gfx_index}")
            gdhm.report_bug(
                title=f"[Interfaces][DP_DSC] - DSC Should be Enabled for Display Plugged at: {port} on {gfx_index}",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
        elif is_dsc_required is False and is_vdsc_enabled is False:
            is_dsc_verification_required = False
            logging.info("Skipping DSC Verification as DSC is not Required to Drive the Current Mode")
        elif is_dsc_required is False and is_vdsc_enabled is True:
            is_dsc_verification_required = is_success = False
            logging.error(f"[Driver Issue] - DSC Should Not be Enabled for Display Plugged at: {port} on {gfx_index}")
            gdhm.report_bug(
                title=f"[Interfaces][DP_DSC] - DSC Should Not be Enabled for Display Plugged at: {port} on {gfx_index}",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )

    if is_dsc_verification_required is True:
        is_success = dsc_verifier.verify_dsc_programming()

    if is_success is False:
        gdhm.report_bug(
            title=f"[Interfaces][DP_DSC] DSC programming verification failed for DisplayType: "
                  f"{dsc_display.display_type}",
            problem_classification=gdhm.ProblemClassification.OTHER,
            component=gdhm.Component.Test.DISPLAY_INTERFACES,
            priority=gdhm.Priority.P2,
            exposure=gdhm.Exposure.E2
        )

    return is_success
