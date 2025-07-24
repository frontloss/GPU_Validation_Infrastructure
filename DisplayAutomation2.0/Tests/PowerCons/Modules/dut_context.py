#######################################################################################################################
# @file         dut_context.py
# @brief        Contains object definitions used in dut.py module
#
# @author       Rohit Kumar
#######################################################################################################################
from enum import IntEnum
from typing import Dict

import DisplayRegs
from DisplayRegs import DisplayRegsService
from DisplayRegs.DisplayArgs import PipeType, TranscoderType

GEN_09_PLATFORMS = ['SKL', 'KBL', 'CFL']
GEN_10_PLATFORMS = ['GLK', 'CNL', 'APL']
GEN_11_PLATFORMS = ['ICLLP', 'EHL', 'JSL']
GEN_11p5_PLATFORMS = ['LKF1']
GEN_12_PLATFORMS = ['TGL', 'RKL', 'DG1', 'ADLS']
GEN_13_PLATFORMS = ['DG2', 'ADLP']
GEN_14_PLATFORMS = ['DG3', 'MTL', 'ELG']
GEN_15_PLATFORMS = ['LNL']
GEN_16_PLATFORMS = ['PTL']
GEN_17_PLATFORMS = ['CLS', 'NVL']
PRE_GEN_12_PLATFORMS = GEN_09_PLATFORMS + GEN_10_PLATFORMS + GEN_11_PLATFORMS + GEN_11p5_PLATFORMS
PRE_GEN_13_PLATFORMS = PRE_GEN_12_PLATFORMS + GEN_12_PLATFORMS
PRE_GEN_14_PLATFORMS = PRE_GEN_13_PLATFORMS + GEN_13_PLATFORMS
PRE_GEN_15_PLATFORMS = PRE_GEN_14_PLATFORMS + GEN_14_PLATFORMS
PRE_GEN_16_PLATFORMS = PRE_GEN_15_PLATFORMS + GEN_15_PLATFORMS
PRE_GEN_17_PLATFORMS = PRE_GEN_16_PLATFORMS + GEN_16_PLATFORMS


##
# @brief        Exposed enum object for Windows OS version
class WinOsVersion(IntEnum):
    WIN_UNKNOWN = 0
    WIN_TH1 = 1
    WIN_TH2 = 2
    WIN_RS1 = 3
    WIN_RS2 = 4
    WIN_RS3 = 5
    WIN_RS4 = 6
    WIN_RS5 = 7
    WIN_19H1 = 8
    WIN_VIBRANIUM = 9
    WIN_20H1 = 10
    WIN_20H2 = 11
    WIN_21H1 = 12
    WIN_21H2 = 13
    WIN_COBALT = 14
    WIN_NICKEL = 15
    WIN_MAX = 21


##
# @brief        Exposed class for RR switching methods
class RrSwitchingMethod:
    CLOCK = 'CLOCK'
    VTOTAL_SW = 'VTOTAL_SW'
    VTOTAL_HW = 'VTOTAL_HW'
    UNSUPPORTED = 'UNSUPPORTED'


##
# @brief        Exposed object class for EDP capabilities
class EdpCaps:
    ##
    # @brief       Initializer for EdpCaps instances
    def __init__(self):
        self.edp_revision = 0  # Default eDP 1.1
        self.is_set_power_capable = False
        self.is_assr_supported = False
        self.mso_segments = 0

    ##
    # @brief       Function to get the string format of EdpCaps object
    # @return      string representation of the EdpCaps object
    def __repr__(self):
        return f"EdpCaps(EdpRevision={self.edp_revision}, SetPowerCapable={self.is_set_power_capable}, " \
               f"AssrSupported={self.is_assr_supported}, " \
               f"MsoSupport={'False' if self.mso_segments == 0 else 'True(%s)' % self.mso_segments})"


##
# @brief        Exposed object class for DRRS capabilities
class RrSwitchingCaps:
    ##
    # @brief       Initializer for RrSwitchingCaps instances
    def __init__(self):
        self.is_drrs_supported = False
        self.is_dmrrs_supported = False
        self.max_pixel_clock = None
        self.min_pixel_clock = None
        self.min_rr = None  # Min RR returned by the OS in mode info
        self.max_rr = None  # Max RR returned by the OS in mode info
        self.actual_min_rr = None   # Min RR calculated based on the max pixel clock value in DTD
        self.actual_max_rr = None   # Max RR calculated based on the max pixel clock value in DTD

    ##
    # @brief       Function to get the string format of RrSwitchingCaps object
    # @return      string representation of the RrSwitchingCaps object
    def __repr__(self):
        return "RrSwitchingCaps(DrrsSupported={0}, DmrrsSupported={1}, OS RR(Min={2}, Max={3}), " \
               "DTD RR(Min={4}, Max={5}), MinPixelClock={6}, MaxPixelClock={7})".format(
            self.is_drrs_supported, self.is_dmrrs_supported, self.min_rr, self.max_rr,
            self.actual_min_rr, self.actual_max_rr, self.min_pixel_clock, self.max_pixel_clock)


##
# @brief        Exposed object class for HDR capabilities
class HdrCaps:
    ##
    # @brief       Initializer for HdrCaps instances
    def __init__(self):
        self.is_hdr_supported = False
        self.is_aux_only_brightness = False
        self.colorimetry_with_sdp_supported = False
        self.colorimetry_support = False
        self.enable_sdp_override_aux = False
        self.brightness_optimization_supported = False
        self.brightness_ctrl_in_nits_level_using_Aux_supported = False

    ##
    # @brief       Function to get the string format of HdrCaps object
    # @return      string representation of the HdrCaps object
    def __repr__(self):
        return f"HdrCaps(HdrSupported={self.is_hdr_supported}, AuxOnlyBrightness={self.is_aux_only_brightness}, " \
               f"ColorimetryWithSdpSupported= {self.colorimetry_with_sdp_supported}, " \
               f"ColorimetrySupported={self.colorimetry_support}, SdpOverrideAux={self.enable_sdp_override_aux}, " \
               f"BrightnessOptimizationSupported={self.brightness_optimization_supported}, " \
               f"BrightnessNitsRangeSupport={self.brightness_ctrl_in_nits_level_using_Aux_supported})"


##
# @brief        Exposed object class for LRR capabilities
class LrrCaps:
    ##
    # @brief       Initializer for LrrCaps instances
    def __init__(self):
        self.is_lrr_supported = False
        self.is_lrr_1_0_supported = False
        self.is_lrr_2_0_supported = False
        self.is_lrr_2_5_supported = False  # Idle -> PSR2 SU, Media PB -> PSR disable - VTotal RR change - PSR enable
        self.rr_switching_method = RrSwitchingMethod.UNSUPPORTED

    ##
    # @brief       Function to get the string format of LrrCaps object
    # @return      string representation of the LrrCaps object
    def __repr__(self):
        return f"LrrCaps(LRR1={self.is_lrr_1_0_supported}, LRR2={self.is_lrr_2_0_supported}, " \
               f"LRR2.5={self.is_lrr_2_5_supported}, RrSwitchingMethod={self.rr_switching_method})"


##
# @brief        Exposed object class for LRR capabilities
class BfrCaps:
    ##
    # @brief       Initializer for LrrCaps instances
    def __init__(self):
        self.is_bfr_supported = False

    ##
    # @brief       Function to get the string format of LrrCaps object
    # @return      string representation of the LrrCaps object
    def __repr__(self):
        return f"BfrCaps(BfrSupported={self.is_bfr_supported})"


##
# @brief        Exposed object class for MSO capabilities
class MsoCaps:
    ##
    # @brief       Initializer for MsoCaps instances
    def __init__(self):
        self.is_mso_supported = False
        self.no_of_segments = None

    ##
    # @brief       Function to get the string format of MsoCaps object
    # @return      string representation of the MsoCaps object
    def __repr__(self):
        return "MsoCaps(MsoSupported={0}, segments={1})".format(self.is_mso_supported, self.no_of_segments)


##
# @brief        Exposed object class for PSR capabilities
class PsrCaps:
    ##
    # @brief       Initializer for PsrCaps instances
    def __init__(self):
        self.is_psr_supported = False
        self.is_psr2_supported = False
        self.is_enabled_in_vbt = False
        self.psr_version = 0
        self.setup_time = 0
        self.alpm_caps = 0  # ALPM CAPS DPCD data
        self.y_coordinate_required = False
        self.su_granularity_supported = False
        self.su_y_granularity = 0  # Su Y-granularity value supported by Panel DPCD
        self.early_transport_supported = False

    ##
    # @brief       Function to get the string format of PsrCaps object
    # @return      string representation of the PsrCaps object
    def __repr__(self):
        return "PsrCaps(Psr1Supported={0}, Psr2Supported={1} , psr_version={2} , SetupTime={3}, ALPMSupport={4}, " \
               "Y_Coordinate supported={5}, SuGranularitySupport={6}, Y_GranularityVal={7} , EarlyTransport={8}, " \
               "EnabledInVbt={9})" \
            .format(self.is_psr_supported, self.is_psr2_supported, self.psr_version, self.setup_time, self.alpm_caps,
                    self.y_coordinate_required, self.su_granularity_supported, self.su_y_granularity,
                    self.early_transport_supported, self.is_enabled_in_vbt)


##
# @brief        Exposed object class for VDSC capabilities
class VdscCaps:
    ##
    # @brief       Initializer for VdscCaps instances
    def __init__(self):
        self.is_vdsc_supported = False

    ##
    # @brief       Function to get the string format of VdscCaps object
    # @return      string representation of the VdscCaps object
    def __repr__(self):
        return "VdscCaps(VdscSupported={0})".format(self.is_vdsc_supported)


##
# @brief        Exposed object class for Pipe joiner or Tiled capabilities
class PipeJoinerTiledCaps:
    ##
    # @brief       Initializer for PipeJoinerCaps instances
    def __init__(self):
        self.is_pipe_joiner_require = False
        self.is_tiled_panel = False
        self.master_pipe = None
        self.slave_pipe = None

    ##
    # @brief       Function to get the string format of PipeJoinerTiledCaps object
    # @return      string representation of the PipeJoinerTiledCaps object
    def __repr__(self):
        return "PipeJoinerTiledCaps(IsPipeJoinerRequire={0}, IsTiled Panel={1}, master_pipe= {2}, slave_pipe= {3})"\
            .format(self.is_pipe_joiner_require, self.is_tiled_panel, self.master_pipe, self.slave_pipe)


##
# @brief        Exposed object class for HDMI 2.1 capabilities
class Hdmi2p1Caps:
    ##
    # @brief       Initializer for Hdmi2p1Caps instances
    def __init__(self):
        self.is_hdmi_2_1_pcon = False
        self.is_hdmi_2_1_native = False
        self.is_hdmi_2_1_tmds = False

    ##
    # @brief       Function to get the string format of Hdmi2p1Caps object
    # @return      string representation of the Hdmi2p1Caps object
    def __repr__(self):
        return (f"Hdmi21Caps(IsHdmi2p1Pcon={self.is_hdmi_2_1_pcon}, IsHdmi2p1Native={self.is_hdmi_2_1_native},"
                f"IsHdmi2p1tmds={self.is_hdmi_2_1_tmds})")


##
# @brief        Exposed object class for VRR capabilities
class VrrCaps:
    ##
    # @brief       Initializer for VrrCaps instances
    def __init__(self):
        self.is_vrr_supported = False
        self.is_vrr_enabled_in_vbt = True
        self.min_rr = 0  # MRL min
        self.max_rr = 0  # MRL max
        self.is_vrr_sdp_supported = False
        self.is_dc_balancing_enabled = False
        self.is_always_vrr_mode = False
        self.is_always_vrr_mode_on_non_vrr_panel = False
        self.vrr_min_rr = 0
        self.vrr_max_rr = 0
        self.vrr_profile_min_rr = 0
        self.vrr_profile_max_rr = 0
        self.vrr_profile_sfdit = 0
        self.vrr_profile_sfddt = 0

    ##
    # @brief       Function to get the string format of VrrCaps object
    # @return      string representation of the VrrCaps object
    def __repr__(self):
        return "VrrCaps(VrrSupported={0}, EnabledInVbt={1} MRLMinRR={2}, MRLMaxRR={3}, VRRMinRR={4}, VRRMaxRR={5}," \
               "VrrProfileVmin={6}, VrrProfileVmax={7}, VrrProfileSFDIT={8}, VrrProfileSFDDT={9}, " \
               "VrrSdpSupported={10}, VrrDCBalanceSupported={11}, IsAlwaysVRRMode={12}," \
               "IsAlwaysVRROnNonVRRPanel={13})" .format(self.is_vrr_supported, self.is_vrr_enabled_in_vbt,
                                                        self.min_rr, self.max_rr, self.vrr_min_rr, self.vrr_max_rr,
                                                        self.vrr_profile_min_rr, self.vrr_profile_max_rr,
                                                        self.vrr_profile_sfdit, self.vrr_profile_sfddt,
                                                        self.is_vrr_sdp_supported,
                                                        self.is_dc_balancing_enabled, self.is_always_vrr_mode,
                                                        self.is_always_vrr_mode_on_non_vrr_panel)


##
# @brief        Exposed object class for MIPI Caps
class MipiCaps:
    ##
    # @brief       Initializer for MipiCaps instances
    def __init__(self):
        self.is_video_mode_supported = False
        self.is_dual_link = False
        self.is_feature_swapped = False

    ##
    # @brief       Function to get the string format of MipiCaps object
    # @return      string representation of the MipiCaps object
    def __repr__(self):
        return "MipiCaps(VideoModeSupported={0}, DualLink={1})".format(
            self.is_video_mode_supported, self.is_dual_link)


##
# @brief        Exposed object class for IDT capabilities
class IdtCaps:
    ##
    # @brief       Initializer for IdtCaps instances
    def __init__(self):
        self.is_ubzrr_supported = False
        self.is_ublrr_supported = False
        self.is_alrr_supported = False
        self.is_pixoptix_supported = False

    ##
    # @brief       Function to get the string format of IdtCaps object
    # @return      string representation of the IdtCaps object
    def __repr__(self):
        return f"IdtCaps(UbZrrSupported={self.is_ubzrr_supported}, UbLrrSupported={self.is_ublrr_supported}, " \
               f"AlrrSupported={self.is_alrr_supported}, PixOptixSupported={self.is_pixoptix_supported})"


##
# @brief        Exposed object class for PanelReplay capabilities
class PrCaps:
    ##
    # @brief       Initializer for PrCaps instances
    def __init__(self):
        self.is_pr_supported = False
        self.pr_su_granularity_needed = False
        self.su_y_granularity = 0  # Su Y-granularity value supported by Panel DPCD
        self.early_transport_supported = False
        self.aux_less_alpm = False

    ##
    # @brief       Function to get the string format of PrCaps object
    # @return      string representation of the PrCaps object
    def __repr__(self):
        return f"PrCaps(PrSupported={self.is_pr_supported}, PrGranularityRequired= {self.pr_su_granularity_needed}, " \
               f"Y_GranularityValue={self.su_y_granularity} EarlyTransportSupported={self.early_transport_supported}, " \
               f"AuxLessALPM supported={self.aux_less_alpm})"


##
# @brief        Exposed object class for Vesa Blc capabilities
class VesaCaps:
    ##
    # @brief       Initializer for VesaCaps instances
    def __init__(self):
        self.is_nits_brightness_supported = False
        self.is_variable_brightness_supported = False
        self.is_smooth_brightness_supported = False

    ##
    # @brief       Function to get the string format of VesaCaps object
    # @return      string representation of the VesaCaps object
    def __repr__(self):
        return (f"VesaCaps(NitsSupported={self.is_nits_brightness_supported}, BrightnessOptimization= "
                f"{self.is_variable_brightness_supported}, SmoothBrightness={self.is_smooth_brightness_supported}")


##
# @brief        Exposed object class for edid Luminance data
class LuminanceCaps:
    ##
    # @brief       Initializer for LuminanceCaps instances
    def __init__(self):
        self.max_fall_did_2p1 = 0
        self.max_cll_did_2p1 = 0
        self.min_cll_did_2p1 = 0
        self.max_fall_display_param = 0
        self.max_cll_display_param = 0
        self.min_cll_display_param = 0

    ##
    # @brief       Function to get the string format of LuminanceCaps object
    # @return      string representation of the LuminanceCaps object
    def __repr__(self):
        return ("LuminanceCaps(DID2.1[MaxFall={0}, MaxCll={1}, MinCll={2}], DisplayParam[MaxFall={3},MaxCll={4},"
                " MinCll={5}]),").format(self.max_fall_did_2p1, self.max_cll_did_2p1, self.min_cll_did_2p1,
                    self.max_fall_display_param, self.max_cll_display_param, self.min_cll_display_param)


##
# @brief        Exposed object class for gfx adapter
class Adapter:
    ##
    # @brief       Initializer for Adapter instances
    # @param[in]   gfx_index GFX Adapter Index Value
    # @param[in]   adapter_info object containing info like deviceID, gfx_index, ...
    def __init__(self, gfx_index, adapter_info):
        self.gfx_index: str = gfx_index
        self.index: int = int(gfx_index[-1])
        self.name: str = adapter_info.get_platform_info().PlatformName
        self.adapter_info = adapter_info
        self.panels: Dict[str, Panel] = dict()
        self.lfp_count: int = 0
        self.is_yangra: bool = False if (self.name in GEN_09_PLATFORMS + GEN_10_PLATFORMS) else True
        # VRR is only supported from ICL+
        self.is_vrr_supported: bool = self.is_yangra
        # HRR is only enabled for ICL+
        self.is_hrr_supported: bool = self.is_yangra
        self.regs: DisplayRegsService = DisplayRegs.get_interface(self.name, self.gfx_index)
        self.cpu_stepping: int = 0

    ##
    # @brief       Function to get the string format of Adapter object
    # @return      string representation of the Adapter object
    def __repr__(self):
        return "Adapter(gfx_index={0}, name={1})".format(self.gfx_index, self.name)

    ##
    # @brief       Function to compare two Adapter objects
    # @param[in]   other Adapter object to compare with self
    # @return      0 if both are same, 1 otherwise
    def __cmp__(self, other):
        if not isinstance(other, Adapter):
            return 1

        if self.gfx_index == other.gfx_index and self.name == other.name:
            return 0
        return 1


##
# @brief        Exposed object class for Panel
class Panel:
    ##
    # @brief       Initializer for Panel instances
    # @param[in]   args command line arguments used to fill the instance members
    # @param[in]   kwargs keyword arguments used to fill the instance members
    def __init__(self, *args, **kwargs):
        # caps from command line
        self.gfx_index = None
        self.port = None
        self.port_type = None
        self.is_lfp = None
        self.panel_index = None
        self.edid_path = None
        self.dpcd_path = None
        self.description = None

        # caps after plug-in
        self.target_id = None
        self.source_id = None
        self.panel_type = None
        self.pipe = None
        self.pipe_type: PipeType = PipeType.PIPE_NULL
        self.transcoder = None
        self.transcoder_type: TranscoderType = TranscoderType.TRANSCODER_NULL
        self.bpc = None
        self.pnp_id = None
        self.is_active = False

        self.rr_list = None
        self.max_rr = None      # Max RR returned by the OS in mode info
        self.min_rr = None      # Min RR returned by the OS in mode info
        self.actual_max_rr = None  # Max RR calculated based on the max pixel clock value in DTD
        self.actual_min_rr = None  # Min RR calculated based on the min pixel clock value in DTD
        self.current_mode = None

        # luminous data can be available irrespective of HDR support
        self.max_fall = 0
        self.max_cll = 0
        self.min_cll = 0

        self.dpcd_version = 0x10  # Default DPCD 1.0
        self.max_lane_count = 0
        self.pixel_clocks = None
        self.native_mode = None
        self.link_rate = None
        self.monitor_id = None

        self.timing_caps = None
        self.edp_caps = EdpCaps()
        self.drrs_caps = RrSwitchingCaps()
        self.hdr_caps = HdrCaps()
        self.lrr_caps = LrrCaps()
        self.mso_caps = MsoCaps()
        self.psr_caps = PsrCaps()
        self.vdsc_caps = VdscCaps()
        self.vrr_caps = VrrCaps()
        self.mipi_caps = MipiCaps()
        self.pipe_joiner_tiled_caps = PipeJoinerTiledCaps()
        self.hdmi_2_1_caps = Hdmi2p1Caps()
        self.bfr_caps = BfrCaps()
        self.idt_caps = IdtCaps()
        self.pr_caps = PrCaps()
        self.vesa_caps= VesaCaps()
        self.luminance_caps = LuminanceCaps()

        self.display_info = None

        for attribute in dir(self):
            if attribute in kwargs.keys():
                setattr(self, attribute, kwargs[attribute])

    ##
    # @brief       Function to get the string format of Panel object
    # @return      string representation of the Panel object
    def __repr__(self):
        return f"Panel(Port={self.port}, Pipe={self.pipe}, SourceId={self.source_id}, Transcoder={self.transcoder}, " \
               f"LinkRate={self.link_rate}, MaxLaneCount={self.max_lane_count}, IsActive={self.is_active}, " \
               f"BPC={self.bpc}, PixelClocks={self.pixel_clocks}, NativeMode={self.native_mode})\n" \
               f"Feature Support(PSR={self.psr_caps.is_psr_supported or self.psr_caps.is_psr2_supported}, " \
               f"VDSC={self.vdsc_caps.is_vdsc_supported}, HDR={self.hdr_caps.is_hdr_supported}, " \
               f"DRRS={self.drrs_caps.is_drrs_supported}, LRR={self.lrr_caps.is_lrr_supported}, " \
               f"VRR={self.vrr_caps.is_vrr_supported}, BFR={self.bfr_caps.is_bfr_supported}, " \
               f"UBRR={self.idt_caps.is_ubzrr_supported or self.idt_caps.is_ublrr_supported}, " \
               f"ALRR={self.idt_caps.is_alrr_supported}, MIPI_VideoMode={self.mipi_caps.is_video_mode_supported}, " \
               f"PR={self.pr_caps.is_pr_supported}, Vesa(Aux={self.vesa_caps.is_nits_brightness_supported}, " \
               f"CABC={self.vesa_caps.is_variable_brightness_supported}, " \
               f"SmoothBrightness={self.vesa_caps.is_smooth_brightness_supported})"

    ##
    # @brief       Function to compare two Panel objects
    # @param[in]   other Panel object to compare with self
    # @return      0 if both are same, 1 otherwise
    def __cmp__(self, other):
        if not isinstance(other, Panel):
            return 1

        if self.gfx_index == other.gfx_index and self.port == other.port and self.port_type == other.port_type:
            return 0
        return 1
