namespace Intel.VPG.Display.Automation
{
    internal enum PORT
    {
        NONE = 0x00,
        PORTA,
        PORTB,
        PORTC,
        PORTD,
        PORTE,
        TVPORT,
        PORTX,
        PORTY
    }
    internal enum DTDCategory
    {
        Timing,
        MachineName
    }
    internal enum QDCFlags
    {
        QDC_ALL_PATHS = 0x00000001,
        QDC_ONLY_ACTIVE_PATHS = 0x00000002,
        QDC_DATABASE_CURRENT = 0x00000004
    }
    internal enum DISPLAYCONFIG_TOPOLOGY_ID : uint
    {
        DISPLAYCONFIG_TOPOLOGY_INTERNAL = 0x00000001,
        DISPLAYCONFIG_TOPOLOGY_CLONE = 0x00000002,
        DISPLAYCONFIG_TOPOLOGY_EXTEND = 0x00000004,
        DISPLAYCONFIG_TOPOLOGY_EXTERNAL = 0x00000008,
        DISPLAYCONFIG_TOPOLOGY_NULL = 0x00000000,
        DISPLAYCONFIG_TOPOLOGY_FORCE_UINT32 = 0xFFFFFFFF
    }
    internal enum DisplayType
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
        WIDI
    }
    internal enum DTDBlockInit
    {
        First = 54,
        Second = 72,
        Third = 90,
        Fourth = 108
    }
    public enum DriverEscapeType
    {
        PortName = 0,
        Register = 1,
    }
    internal enum GFX_ESCAPE_CODE
    {
        GFX_ESCAPE_CUICOM_CONTROL = 1,
        GFX_ESCAPE_SOFTBIOS_CONTROL = 8
    }
    internal enum BaseBlockValues
    {
        Manufacturer = 8,
        Product = 10
    }
}
