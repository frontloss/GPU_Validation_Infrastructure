#####################################################################################################################################
# @file     display_dip_control.py
# @brief    Python wrapper exposes interfaces for DisplayDIPControl verification
# @details  display_dip_control.py provides interface's to Verify video_dip_ctl and AVI Infoframe data for HDMI port
#           User-Input : DisplayDIPControl() object - display_port, BPC value
# @note     Supported display interfaces are HDMI\n
# @author   Aafiya Kaleem
####################################################################################################################################
import importlib
import logging
import os

from Libs.Core import registry_access
from Libs.Core.sw_sim import driver_interface
from Libs.Core.wrapper.driver_escape_args import AviEncodingMode
from Libs.Core.logger import gdhm
from Libs.Core.machine_info.machine_info import PRE_GEN_14_PLATFORMS
from Libs.Feature.display_engine.de_base import display_base
from Libs.Feature.hdmi.hf_vsdb_block import HdmiForumVendorSpecificDataBlock
from Libs.Feature.vdsc.dsc_helper import DSCHelper

from Tests.Color import color_common_utility


from registers.mmioregister import MMIORegister

# Mapping of CEA VICs to HDMI_VICs
hdmi_cea_to_4k2k_dict = {95: 1, 94: 2, 93: 3, 98: 4}

##
# @brief DisplayDIPControl class
class DisplayDIPControl(display_base.DisplayBase):

    ##
    # @brief Initializes DisplayDIPControl object
    # @param[in] display_port display to verify
    # @param[in] BPC bits per component
    # @param[in] gfx_index graphics adapter
    # @param[in] color_format - RGB or YUV
    # @param[in] vic_id - Video Format Identification code
    def __init__(self, display_port, BPC=None, gfx_index='gfx_0', color_format=None, vic_id=None):
        self.display_port = display_port
        self.BPC = BPC  # 6,8,10,12
        self.color_format = color_format
        self.vic_id = vic_id
        display_base.DisplayBase.__init__(self, display_port, gfx_index=gfx_index)


##
# @brief Verify video_dip_gcp(gcp_color_indication bit[2]) programming for HDMI port
# @param[in] dipCtrlObj DisplayDIPControl() object instance to specify port_name, BPC
# @param[in] gfx_index graphics adapter
# @return Return true if MMIO programming is correct, else return false
def verify_video_dip_gcp(dipCtrlObj, gfx_index='gfx_0'):
    reg = MMIORegister.read("VIDEO_DIP_GCP_REGISTER", "VIDEO_DIP_GCP_%s" % (dipCtrlObj.pipe_suffix),
                            dipCtrlObj.platform, gfx_index=gfx_index)
    logging.debug("VIDEO_DIP_GCP_%s" % (dipCtrlObj.pipe_suffix) + " --> Offset : "
                  + format(reg.offset, '08X') + " Value :" + format(reg.asUint, '08X'))

    is_compression_enabled = DSCHelper.is_vdsc_enabled_in_driver(gfx_index, dipCtrlObj.display_port)

    # If DSC is enabled, GCP packets will not be sent
    if is_compression_enabled:
        gcp_color_indication = 0
    else:
        gcp_color_indication = 0 if (dipCtrlObj.BPC in [6, 8]) else 1

    if (gcp_color_indication == reg.gcp_color_indication):
        logging.info(
            "PASS : gcp_color_indication Expected : %s Actual : %s" % (gcp_color_indication, reg.gcp_color_indication))
        return True
    else:
        gdhm.report_bug(
            title="[Interfaces][Display_Engine][DIP_Control]: Mismatch in gcp_color_indication  Expected: {0} Actual: "
                  "{1}".format(gcp_color_indication, reg.gcp_color_indication),
            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
            component=gdhm.Component.Driver.DISPLAY_INTERFACES,
            priority=gdhm.Priority.P2,
            exposure=gdhm.Exposure.E2
        )
        logging.error(
            "FAIL : gcp_color_indication Expected : %s Actual : %s" % (gcp_color_indication, reg.gcp_color_indication))
    return False

##
# @brief Verify video_dip_ctl(vdip_enable_gcp bit[16],vdip_enable_avi bit[12]) programming for HDMI port
# @param[in] dipCtrlObj DisplayDIPControl() object instance to specify port_name, BPC
# @param[in] gfx_index graphics adapter
# @return bool Return true if MMIO programming is correct, else return false
def verify_video_dip_ctl(dipCtrlObj, gfx_index='gfx_0'):
    status = False
    reg = MMIORegister.read("VIDEO_DIP_CTL_REGISTER", "VIDEO_DIP_CTL_%s" % (dipCtrlObj.pipe_suffix),
                            dipCtrlObj.platform, gfx_index=gfx_index)
    logging.debug("VIDEO_DIP_CTL_%s" % (dipCtrlObj.pipe_suffix) + " --> Offset : "
                  + format(reg.offset, '08X') + " Value :" + format(reg.asUint, '08X'))

    is_compression_enabled = DSCHelper.is_vdsc_enabled_in_driver(gfx_index, dipCtrlObj.display_port)

    # If DSC is enabled, GCP packets will not be sent
    if is_compression_enabled:
        vdip_enable_gcp = 0
    else:
        # GCP will be sent always irrespective of BPC
        # HSD: 14021291774
        vdip_enable_gcp = 1

    if vdip_enable_gcp == reg.vdip_enable_gcp:
        logging.info("PASS : vdip_enable_gcp Expected : %s Actual : %s" % (vdip_enable_gcp, reg.vdip_enable_gcp))
        status = True
        if reg.vdip_enable_gcp:
            status = verify_video_dip_gcp(dipCtrlObj, gfx_index)
    else:
        gdhm.report_bug(
            title="[Interfaces][Display_Engine][DIP_Control]: Mismatch in vdip_enable_gcp  Expected: {0} Actual: "
                  "{1}".format(vdip_enable_gcp, reg.vdip_enable_gcp),
            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
            component=gdhm.Component.Driver.DISPLAY_INTERFACES,
            priority=gdhm.Priority.P2,
            exposure=gdhm.Exposure.E2
        )
        logging.error("FAIL : vdip_enable_gcp Expected : %s Actual : %s" % (vdip_enable_gcp, reg.vdip_enable_gcp))

    # vdip_enable_avi should be enabled for hdmi
    if (reg.vdip_enable_avi):
        logging.info("PASS : vdip_enable_avi Expected : 1 (Enable) Actual : %s" % (reg.vdip_enable_avi))
        return (status and True)
    else:
        gdhm.report_bug(
            title="[Interfaces][Display_Engine][DIP_Control]: vdip_enable_avi not enabled  Expected: 1 (Enable) Actual:"
                  "{}".format(reg.vdip_enable_avi),
            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
            component=gdhm.Component.Driver.DISPLAY_INTERFACES,
            priority=gdhm.Priority.P2,
            exposure=gdhm.Exposure.E2
        )
        logging.error("FAIL : vdip_enable_avi Expected : 1 (Enable) Actual : %s" % (reg.vdip_enable_avi))

    return False

##
# @brief Verify video_dip_avi_infoframe programming for HDMI port
# @param[in] dipCtrlObj DisplayDIPControl() object instance to specify port_name
# @param[in] gfx_index graphics adapter
# @return  bool Return true if MMIO programming is correct, else return false
def verify_video_dip_avi_infoframe(dipCtrlObj, gfx_index='gfx_0'):
    status = True
    # TODO : AVI Infoframe byte 0-7 verification to be added. Only header info added for now
    reg = MMIORegister.read("VIDEO_DIP_AVI_HEADER_BYTE_REGISTER", "VIDEO_DIP_AVI_DATA_%s_0" % (dipCtrlObj.pipe_suffix),
                            dipCtrlObj.platform, gfx_index=gfx_index)
    logging.debug("VIDEO_DIP_AVI_DATA_%s_0" % (dipCtrlObj.pipe_suffix) + "--> Offset : " + format(reg.offset, '08X')
                  + " Value :" + format(reg.asUint, '08X'))
    if ((reg.header_byte_0 == 0x82) and ((reg.header_byte_1 == 0x02) or (reg.header_byte_1 == 0x03)) and (reg.header_byte_2 == 0x0D)):
        logging.info("INFO : AVI Infoframe Header Byte is as per spec")
    else:
        gdhm.report_bug(
            title="[Interfaces][Display_Engine][DIP_Control]: AVI Infoframe Header Byte is not as per spec",
            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
            component=gdhm.Component.Driver.DISPLAY_INTERFACES,
            priority=gdhm.Priority.P2,
            exposure=gdhm.Exposure.E2
        )
        logging.error("AVI Infoframe Header Byte is not as per spec")
        status = False

    # Reading Header of AVI Info frame
    avi_base = MMIORegister.get_instance("VIDEO_DIP_AVI_HEADER_BYTE_REGISTER",
                                     "VIDEO_DIP_AVI_DATA_%s_0" % dipCtrlObj.pipe_suffix, dipCtrlObj.platform)

    # Verify Color Format being sent in AVI Info frame
    if dipCtrlObj.color_format is not None:
        status = verify_color_format_in_avi(dipCtrlObj, avi_base)

    # For now disabling VIC ID verification due to issues found during ULT. Will enable VIC ID verification back once
    # both the issues are fixed. HSD: 16021211152, 16021269743
    # Remove below line to enable VIC verification
    # dipCtrlObj.vic_id = None

    # Verify VIC ID in AVI info frame or HDMI_VIC in H14bVSIF
    if dipCtrlObj.vic_id is not None:

        # Parse HF-VSDB block
        hf_vsdb_parser = HdmiForumVendorSpecificDataBlock()
        hf_vsdb_parser.parse_hdmi_forum_vendor_specific_data_block('gfx_0', dipCtrlObj.display_port)
        uhd_vic = hf_vsdb_parser.is_uhd_vic_set
        allm_support = hf_vsdb_parser.is_allm_supported

        # Get VIC ID programmed in AVI Info frame
        vic_in_avi = get_vic_id_in_avi(avi_base)

        # If 4k2k mode is found and features from Table 10-1 from HDMI2.1 spec are not supported, then verify H14bVSIF
        if not uhd_vic and dipCtrlObj.vic_id in hdmi_cea_to_4k2k_dict.keys() and not allm_support:

            # Read Header of H14bVSIF
            vsif_base = MMIORegister.get_instance("VIDEO_DIP_VS_HEADER_BYTE_REGISTER", "VIDEO_DIP_VS_DATA_%s_0" % dipCtrlObj.pipe_suffix,
                                                  dipCtrlObj.platform)

            # Verify VIC in AVI Info frame for 4k2k mode
            status = verify_vic_in_avi_for_4k2k_mode(vic_in_avi)

            # Verify IEEE Version in H14bVSIF
            status = verify_ieee_in_h14bvsif(vsif_base)

            # Verify HDMI_VIC in H14bVSIF
            status = verify_hdmi_vic_in_h14bvsif(dipCtrlObj, vsif_base)

        # If not 4k2k mode, Verify CEA VIC in AVI info frame
        else:
            status = verify_cea_vic_in_avi(dipCtrlObj, vic_in_avi)
    return status


##
# @brief Verify video_dip_ctl programming for HDMI port
# @param[in] dipCtrlList list of DisplayDIPControl() object instances to specify port_name
# @param[in] gfx_index graphics adapter
# @return bool Return true if MMIO programming is correct, else return false
def VerifyDisplayDIPAVIdata(dipCtrlList, gfx_index='gfx_0'):
    status = True
    registry_name = "HdmiNoNullPacketAndAudio"
    for dipCtrlObj in dipCtrlList:
        if dipCtrlObj.pipe is None:
            gdhm.report_bug(
                title="[Interfaces][Display_Engine][DIP_Control]:{} port is not connected to any Pipe during DIPAVIdata"
                      "verification".format(dipCtrlObj.display_port),
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.error(
                "ERROR : " + dipCtrlObj.display_port + " is not connected to any Pipe. Check if it is connected")
            status = False
            continue

        if not dipCtrlObj.display_port.startswith("HDMI_"):
            logging.debug("VerifyDisplayDIPControl is supported only for HDMI port. Current display port is {0}".format(
                dipCtrlObj.display_port))
            continue
            # TRANS_DDI_FUNC_CTL
        trans_ddi_func_ctl_reg_module = importlib.import_module(
            "registers.%s.TRANS_DDI_FUNC_CTL_REGISTER" % (dipCtrlObj.platform.lower()))
        trans_ddi_func_ctl_reg_offset_name = 'TRANS_DDI_FUNC_CTL' + '_' + dipCtrlObj.pipe_suffix
        trans_ddi_func_ctl_reg = MMIORegister.read("TRANS_DDI_FUNC_CTL_REGISTER",
                                                       trans_ddi_func_ctl_reg_offset_name,
                                                       dipCtrlObj.platform, gfx_index=gfx_index)

        # Assigning HDMI mode of operation to mode_select_verify variable
        mode_select_verify = getattr(trans_ddi_func_ctl_reg_module,'trans_ddi_mode_select_HDMI')

        diss_reg_args = registry_access.StateSeparationRegArgs(gfx_index='gfx_0')
        read_val, read_type = registry_access.read(args=diss_reg_args, reg_name=registry_name)

        # If "HdmiNoNullPacketAndAudio" is set, assign DVI mode to mode_select_verify. Else, HDMI mode of operation
        # remains unchanged
        if read_val == 1:
            mode_select_verify = getattr(trans_ddi_func_ctl_reg_module,'trans_ddi_mode_select_DVI')

        if trans_ddi_func_ctl_reg.trans_ddi_mode_select == mode_select_verify:
            status = status and verify_video_dip_avi_infoframe(dipCtrlObj, gfx_index)

    return status
##
# @brief Verify video_dip_ctl programming for HDMI port
# @param[in] dipCtrlList list of DisplayDIPControl() object instances to specify port_name, BPC
# @param[in] gfx_index graphics adapter
# @return bool Return true if MMIO programming is correct, else return false
def VerifyDisplayDIPControl(dipCtrlList, gfx_index='gfx_0'):
    registry_name = "HdmiNoNullPacketAndAudio"
    status = True
    for dipCtrlObj in dipCtrlList:
        if (dipCtrlObj.pipe is None):
            gdhm.report_bug(
                title="[Interfaces][Display_Engine][DIP_Control]:{} port is not connected to any Pipe during video "
                      "DIPControl verification".format(dipCtrlObj.display_port),
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.error(
                "ERROR : " + dipCtrlObj.display_port + " is not connected to any Pipe. Check if it is connected")
            status = False
            continue

        if not (dipCtrlObj.display_port.startswith("HDMI_")):
            logging.debug("VerifyDisplayDIPControl is supported only for HDMI port. Current display port is {0}".format(
                dipCtrlObj.display_port))
            continue

        if dipCtrlObj.BPC is None:
            logging.debug("INFO : BPC is not passed as user-input, assigning BPC to MMIO programmed value")
            bpp, bpc = display_base.GetTranscoderBPCValue(dipCtrlObj, gfx_index)
            dipCtrlObj.BPC = bpc

        if dipCtrlObj.BPC not in [6, 8, 10, 12]:
            gdhm.report_bug(
                title="[Interfaces][Display_Engine][DIP_Control]:Incorrect BPC value found in DIP Control object:"
                      " {}".format(dipCtrlObj.BPC),
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.error("ERROR : Incorrect BPC value. Valid BPC values - 6,8,10,12.")
            status = False
            continue

        # TRANS_DDI_FUNC_CTL
        trans_ddi_func_ctl_reg_module = importlib.import_module(
            "registers.%s.TRANS_DDI_FUNC_CTL_REGISTER" % (dipCtrlObj.platform.lower()))
        trans_ddi_func_ctl_reg_offset_name = 'TRANS_DDI_FUNC_CTL' + '_' + dipCtrlObj.pipe_suffix
        trans_ddi_func_ctl_reg = MMIORegister.read("TRANS_DDI_FUNC_CTL_REGISTER", trans_ddi_func_ctl_reg_offset_name,
                                                   dipCtrlObj.platform, gfx_index= gfx_index)

        # Assigning HDMI mode of operation to mode_select_verify variable
        mode_select_verify = getattr(trans_ddi_func_ctl_reg_module, 'trans_ddi_mode_select_HDMI')

        diss_reg_args = registry_access.StateSeparationRegArgs(gfx_index='gfx_0')
        read_val, read_type = registry_access.read(args=diss_reg_args, reg_name=registry_name)

        # If "HdmiNoNullPacketAndAudio" is set, assign DVI mode to mode_select_verify. Else, HDMI mode of operation
        # remains unchanged
        if read_val == 1:
            mode_select_verify = getattr(trans_ddi_func_ctl_reg_module, 'trans_ddi_mode_select_DVI')

        if trans_ddi_func_ctl_reg.trans_ddi_mode_select == mode_select_verify:
            status = status and verify_video_dip_ctl(dipCtrlObj, gfx_index)

    return status


##
# @brief Verify Color Format programming in AVI Info frame for HDMI
# @param[in] dipCtrlObj DisplayDIPControl() object instance to specify port_name
# @param[in] avi_base Base of AVI Info frame structure
# @return bool Return true if Color Format programming in AVI Info frame is correct, else return false
def verify_color_format_in_avi(dipCtrlObj, avi_base):
    avi_offset = avi_base.offset + 4
    reg_value = driver_interface.DriverInterface().mmio_read(avi_offset, 'gfx_0')

    # As per AVI Info frame structure: Y0, Y1 indicates color format.
    color_format_in_avi = color_common_utility.get_bit_value(reg_value, 13, 15)
    color_format_in_avi = AviEncodingMode(color_format_in_avi).name

    if dipCtrlObj.color_format == color_format_in_avi:
        logging.info(f"PASS : Color Format in AVI Info frame  Expected: {dipCtrlObj.color_format}   Actual: {color_format_in_avi}")
    else:
        gdhm.report_driver_bug_di("Color Format programming in AVI Info frame failed")
        logging.error(f"FAIL : Color Format in AVI Info frame  Expected: {dipCtrlObj.color_format}   Actual: {color_format_in_avi}")
        return False
    return True


##
# @brief Get VIC ID value programmed in AVI Info frame
# @param[in] avi_base Base of AVI Info frame structure
# @return int Value of VIC ID programmed in AVI Info frame
def get_vic_id_in_avi(avi_base):
    # Read offset to get VIC ID in AVI Info frame
    avi_offset = avi_base.offset + 8
    reg_value = driver_interface.DriverInterface().mmio_read(avi_offset, 'gfx_0')

    # As per AVI Info frame structure: VIC0...VIC6 indicates VIC ID.
    vic_in_avi = color_common_utility.get_bit_value(reg_value, 0, 7)
    return vic_in_avi


##
# @brief Verify VIC in AVI info frame for 4k2k modes
# @param[in] vic_in_avi VIC ID programmed in AVI info frame
# @return bool Return true if vic_in-avi is zero, else return false
def verify_vic_in_avi_for_4k2k_mode(vic_in_avi):

    # VIC in AVI Info frame should be equal to zero for 4k2k modes
    if vic_in_avi == 0:
        logging.info(f"PASS : VIC ID in AVI Info frame is programmed to zero for 4k2k mode ")
    else:
        gdhm.report_driver_bug_di("VIC ID in AVI Info frame is not programmed to zero for 4k2k mode")
        logging.info(f"FAIL : VIC ID in AVI Info frame is not programmed to zero for 4k2k mode  Expected: 0  Actual: {vic_in_avi}")
        return False
    return True


##
# @brief Verify IEEE version in H14bVSIF
# @param[in] vsif_base Base for HDMI 1.4 vendor specific info frame (H14bVSIF)
# @return bool Return true if IEEE value is programmed correctly, else return false
def verify_ieee_in_h14bvsif(vsif_base):
    h14bvsif_ieee = 3075  # 0x000C03 in hex as per HDMI1.4 spec

    # To get IEEE Registration Identifier in H14VSIF
    vs_offset = vsif_base.offset + 4
    reg_value = driver_interface.DriverInterface().mmio_read(vs_offset, 'gfx_0')
    ieee_in_vsif = color_common_utility.get_bit_value(reg_value, 8, 31)

    # Verify IEEE Version in H14bVSIF
    if ieee_in_vsif == h14bvsif_ieee:
        logging.info(f"PASS: IEEE Verification in H14bVSIF  Expected: {h14bvsif_ieee}  Actual: {ieee_in_vsif}")
    else:
        gdhm.report_driver_bug_di("IEEE Verification in H14bVSIF failed")
        logging.error(f"FAIL: IEEE Verification in H14bVSIF  Expected: {h14bvsif_ieee}  Actual: {ieee_in_vsif}")
        return False
    return True


##
# @brief Verify HDMI_VIC programming in H14bVSIF
# @param[in] dipCtrlObj DisplayDIPControl() object instance to specify port_name
# @param[in] vsif_base Base for HDMI 1.4 vendor specific info frame (H14bVSIF)
# @return bool Return true if HDMI_VIC is programmed correctly, else return false
def verify_hdmi_vic_in_h14bvsif(dipCtrlObj, vsif_base):

    # To get HDMI_VIC in H14bVSIF
    vs_offset = vsif_base.offset + 8
    reg_value = driver_interface.DriverInterface().mmio_read(vs_offset, 'gfx_0')

    hdmi_vic_in_vsif = color_common_utility.get_bit_value(reg_value, 8, 15)

    # Verify if correct HDMI_VIC is sent for 4k2k mode
    if hdmi_cea_to_4k2k_dict[dipCtrlObj.vic_id] == hdmi_vic_in_vsif:
        logging.info(f"PASS: HDMI VIC Verification in H14bVSIF Expected: {hdmi_cea_to_4k2k_dict[dipCtrlObj.vic_id]}   Actual: {hdmi_vic_in_vsif}")
    else:
        gdhm.report_driver_bug_di("HDMI VIC ID programming in H14b vendor specific Info frame failed")
        logging.error(f"FAIL: HDMI VIC Verification in H14bVSIF Expected: {hdmi_cea_to_4k2k_dict[dipCtrlObj.vic_id]}   Actual: {hdmi_vic_in_vsif}")
        return False
    return True


##
# @brief Verify CEA VIC programming in AVI Info frame
# @param[in] dipCtrlObj DisplayDIPControl() object instance to specify port_name
# @param[in] vic_in_avi VIC ID programmed in AVI info frame
# @return bool Return true if CEA VIC is programmed correctly, else return false
def verify_cea_vic_in_avi(dipCtrlObj, vic_in_avi):

    # For non CEA modes, VIC ID in AVI info frame should be programmed to zero
    if dipCtrlObj.vic_id == 255 and vic_in_avi == 0:
        logging.info(f"PASS : VIC ID in AVI Info frame is programmed to zero for non CEA timing")
    elif dipCtrlObj.vic_id == 255 and vic_in_avi != 0:
        gdhm.report_driver_bug_di("VIC ID in AVI Info frame is not programmed to zero for non CEA timing")
        logging.error(f"FAIL : VIC ID in AVI Info frame is not programmed to zero for non CEA timing")
        return False

    # For CEA modes, VIC ID in AVI info frame should be programmed to CEA VIC Value
    elif dipCtrlObj.vic_id == vic_in_avi:
        logging.info(f"PASS : VIC ID in AVI Info frame  Expected: {dipCtrlObj.vic_id}   Actual: {vic_in_avi}")
    else:
        gdhm.report_driver_bug_di("VIC ID programming in AVI Info frame failed")
        logging.error(
            f"FAIL : VIC ID in AVI Info frame  Expected: {dipCtrlObj.vic_id}   Actual: {vic_in_avi}")
        return False
    return True


if __name__ == "__main__":
    scriptName = os.path.basename(__file__).replace(".py", "")
    FORMAT = '%(asctime)-15s %(levelname)s  [%(filename)s:%(lineno)s - %(funcName)s() ] %(message)s'
    logging.basicConfig(level=logging.DEBUG,
                        format=FORMAT,
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename=scriptName + '.log',
                        filemode='w')

    dipList = []
    dipList.append(DisplayDIPControl("HDMI_C", 8))
    VerifyDisplayDIPControl(dipList, 'gfx_0')

