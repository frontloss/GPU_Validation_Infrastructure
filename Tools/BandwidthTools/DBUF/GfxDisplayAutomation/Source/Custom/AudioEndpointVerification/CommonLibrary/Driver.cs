namespace AudioEndpointVerification
{
    public enum DriverState
    {
        Disabled,
        Running,
        UnKnown,
    }

    public enum ConfigManagerErrorCode
    {
        Unknown = -1,
        Running = 0,
        Disabled = 22,
        Restart_Required = 14
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

    public enum ErrorCode
    {
        Information,
        Warning,
        Error
    }
}