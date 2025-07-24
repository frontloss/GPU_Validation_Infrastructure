namespace Intel.VPG.Display.Automation
{
    public enum HDCPOptions
    {
        None = -1,
        ActivateHDCP,
        DeactivateHDCP,
        Move,
        Close,
        QueryGlobalProtectionLevel,
        QueryLocalProtectionLevel,
        SetSRM,
        GetSRMVersion,
        ActivateACP,
        ActivateCGMSA
    }

    public enum HDCPApplication
    {
        None = -1,
        OPMTester,
        COPPTester
    }

    public enum HDCPPlayerInstance
    {
        Player_1,
        Player_2,
        Player_3
    }
}
