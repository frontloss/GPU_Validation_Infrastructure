namespace Intel.VPG.Display.Automation
{
    public enum DriverState
    {
        Disabled,
        Running,
        UnKnown,
    }

    public enum ConfigManagerErrorCode
    {
        Running = 0,
        Disabled = 22,
        Restart_Required = 14
    }

    public enum DriverEscapeType
    {
        PortName = 0,
        Register = 1,
        GTARegisterRead=2,
        GTARegisterWrite=3,
        VBTByteRead=4,
        SBRegisterRead=5,
        DIVARegisterEscape=6,
        DIVAMMIORead = 7,
        DIVAMMIOWrite = 8,
    }

    public enum InstallUninstallMethod
    {
        HaveDisk,
        Setup  
    }
    public enum DriverAdapterType
    {
        Intel = 0,
        ATI,
        Audio
    }

    public enum POWERWELL
    {
        POWERWELL_PG1,
        POWERWELL_PG2,
        POWERWELL_PG3,
        POWERWELL_PG4,
    }   
}