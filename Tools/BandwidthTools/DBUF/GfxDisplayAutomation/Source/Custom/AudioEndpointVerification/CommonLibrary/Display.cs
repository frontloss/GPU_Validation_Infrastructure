namespace AudioEndpointVerification
{
    using System.ComponentModel;
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
        WIDI
    }
    public enum Hierarchy
    {
        None = 0,
        PrimaryDisplay,
        SecondaryDisplay,
        TertiaryDisplay
    }
    public enum PORT
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
    public enum PLANE
    {
        NONE = 0x00,
        PLANE_A,
        PLANE_B,
        PLANE_C
    }
    public enum PIPE
    {
        NONE = 0x00,
        PIPE_A,
        PIPE_B,
        PIPE_C,
        PIPE_EDP,
    }
    public enum DriverEscapeType
    {
        PortName = 0,
        Register = 1,
        GTARegisterRead = 2,
        GTARegisterWrite = 3,
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
}
