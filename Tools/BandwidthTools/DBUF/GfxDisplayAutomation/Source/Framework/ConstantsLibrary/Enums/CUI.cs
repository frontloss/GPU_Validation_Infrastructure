namespace Intel.VPG.Display.Automation
{
    public enum AppBarOptions
    {
        RestoreDefault,
        Apply,
        Cancel
    }
    public enum CUIWindowOptions
    {
        Close = 0,
        Maximize = 3,
        Restore = 9,
        Minimize = 11
    }
    public enum DTCMAccess
    {
        Desktop,
        Tray
    }
    public enum CUISysInfo
    {
        DriverVersion
    }
    public enum ColorOptions
    {
        All,
        Red,
        Green,
        Blue
    }
    public enum ColorEnhancement
    {
        Brightness,
        Contrast,
        Gamma,
        Hue,
        Saturation
    }
}