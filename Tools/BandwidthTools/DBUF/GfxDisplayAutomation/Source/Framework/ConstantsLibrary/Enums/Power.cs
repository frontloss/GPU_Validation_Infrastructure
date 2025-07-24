namespace Intel.VPG.Display.Automation
{
    public enum PowerStates
    {
        S3,
        S4,
        S5,
        CS,
        IdleDesktop
    }
    public enum CPU_C_STATE
    {
        C7,
        C8,
        C9,
        C10
    }
    public enum CSVerificationTool
    {
        Undefined,
        BLATool,
        SocWatch
    }
    public enum NonCSPowerOption
    {
        MonitorOff,
        Sleep,
        Idle
    }
    public enum LidSwitchAction
    {
        DoNothing = 0,
        Sleep,
        Hibernate
    }
    public enum MonitorOnOff
    {
        On,
        Off,
        OffOn
    }
}
