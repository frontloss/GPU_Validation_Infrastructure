namespace Intel.VPG.Display.Automation
{
    using System.ComponentModel;

    public enum DisplayUnifiedConfig
    {
        None = 0,
        Single,
        Clone,
        Extended,
        Collage
    }
    public enum DisplayConfigType
    {
        None = 0,
        SD,
        DDC,
        ED,
        TDC,
        TED,
        Horizontal,
        Vertical
    }
    public enum CollageOptions
    {
        Disable = 1,
        Enable
    }
    public enum ScalingOptions
    {
        //please dont change the sequence
        None,
        Center_Image = 1,
        Scale_Full_Screen = 2,
        Maintain_Aspect_Ratio = 4,
        Customize_Aspect_Ratio = 8,
        Maintain_Display_Scaling = 64,
    }

    public enum PanelFit
    {
        CenterImage = 1,
        ScaleFullScreen = 2,
        MaintainAspectRatio = 4,
        CustomAspectRatio = 8,
        MaintainDisplayScaling = 64,
        Unsupported
    }

    public enum BPP
    {
        BPP_8_BIT = 8,
        BPP_16_BIT = 16,
        BPP_32_BIT = 32,
    }

    public enum DisplayType
    {
        None = 0,
        EDP,
        CRT,
        DP,
        DP_2,
        DP_3,
        HDMI,
        HDMI_2,
        HDMI_3,
        MIPI,
        WIDI,
        DVI,
        WIGIG_DP,
        WIGIG_DP2
    }
    public enum DisplayExtensionInfo
    {
        Internal,
        External
    }
    public enum DFTPluggableDisplay
    {
        None = 0,
        DP,
        DP_2,
        DP_3,
        HDMI,
        HDMI_2,
        HDMI_3
    }
    public enum DVMUPluggableDisplay
    {
        None = 0,
        HDMI,
        HDMI_2
    }
    public enum DongleType
    {
        None = 0,
        Active,
        Passive,
        Real
    }
    public enum DisplayHierarchy
    {
        Display_1,
        Display_2,
        Display_3,
        Display_4,
        Display_5,
        Unsupported,
    }
    public enum DisplayFlag
    {
        Progressive = 0,
        Interlaced = 2,
    }
    public enum PORT
    {
        NONE = 0x00,
        PORTA,
        PORTB,
        PORTC,
        PORTD,
        PORTE,
        PORTF,
        TVPORT,
        PORTX,
        PORTY
    }
    public enum PLANE
    {
        NONE = 0x00,
        PLANE_A,
        PLANE_B,
        PLANE_C
    }
    public enum GENERIC_PLANE
    {
        NONE = -1,
        PLANE_1,
        PLANE_2,
        PLANE_3,
        PLANE_4
    }

    public enum SCALAR_MAP
    {
        NONE=-1,
        PIPE = 0,
        PLANE_1 = 0x2000000,
        PLANE_2 = 0x4000000,
        PLANE_3 = 0x6000000,
        PLANE_4 = 0x8000000
    }
    public enum SCALAR
    {
        NONE = -1,
        Plane_Scalar_1 = 0,
        Plane_Scalar_2
    }
    public enum PIPE
    {
        NONE = 0x00,
        PIPE_A,
        PIPE_B,
        PIPE_C,
        PIPE_EDP,
    }
	public enum ColorDepthOptions
    { 
        _16_Bit = 16,
        _32_Bit = 32
    }
    public enum ColorType
    {
        HueSATURATION,
        XvYCC,
        YCbCr,
        WideGamut,
        RGBQuantization
    }
    public enum ColorFormat
    {
        RGB,
        YUV
    }
    public enum PanelType
    {
        RGB,
        XVYCC_YCBCR
    }
    public enum DPLL
    {
        DPLL0 = 0x00,
        DPLL1,
        DPLL2,
        DPLL3,
        Invalid
    }
    public enum RGB_QUANTIZATION_RANGE
    {
        Unsupported = -1,
        DEFAULT,
        LIMITED,
        FULL,
        RESERVED
    }
    public enum InfChanges
    {
        ModifyInf,
        RevertInf,
        DeleteInf,
        ReadInf
    }
    public enum TileFormat
    {
        Linear_Memory = 0x00,
        Tile_X_Memory,
        Tile_Y_Legacy_Memory,
        Tile_Y_F_Memory,
        Invalid
    }
    public enum PlanePixelFormat
    {
        YUV_4_2_2 = 0,
        NV12_4_2_0 = 1,
        RGB_2_10_10_10 = 2,
        P010_YUV_4_2_0 = 3,
        RGB_8_8_8_8 =4,
        P012_YUV_4_2_0 = 5,
        RGB_16_16_16_16_float = 6,
        P016_YUV_4_2_0 = 7,
        YUV_4_4_4 =8,
        RGB_16_16_16_16_uint = 9,
        RGB_XR_BIAS_10_10_10 =10,
        Indexed_8_bit =12,
        RGB_5_6_5 =14,
    }
    public enum RotationAngle
    {
        ROTATION_0 = 0,
        ROTATION_90 = 1,
        ROTATION_180 = 2,
        ROTATION_270 = 3,
    }
    public enum CollageOption
    {
        None = 0,
        Enable,
        Disable,
        SetConfig,
        GetConfig,
        IsCollageSupported
    }
    public enum SDKType
    {
        Default,
        Old,
        New
    }

    public enum SDKServices
    {
        None,
        DisplayType,
        EDID,
        Config,
        Mode,
        IndependentRotation,
        Scaling,
        Collage,
        DpcdRegister,
        Audio,
        XvYcc,
        YCbCr,
        NarrowGamut,
        WideGamut,
        QuantizationRange
    }
    public enum DPCDRegisters
    {
        DPCD_SINK_CONTROL = 0x600
    }
    public enum DisplayAction
    {
        HOTPLUG = 0,
        HOTUNPLUG,
        MONITORTURNOFF,
        DISPLAYCONFIGSWITCH
    }
}
