namespace Intel.VPG.Display.Automation
{
    public enum DeepColorOptions
    {
        None,
        Enable,
        Disable,
        Move,
        Close,
    }

    public enum DeepColorAppType
    {
        None = -1,
        FP16,
        DPApplet,
        N10BitScanOut

    }

    public enum WideGamutLevel
    {
        Unsupported = 0,
        NATURAL = 1,
        LEVEL2 = 2,
        LEVEL3 = 3,
        LEVEL4 = 4,
        VIVID = 5
    }
    public enum NarrowGamutOption
    {
        EnableNarrowGamut,
        DisbaleNarrowGamut,
        EnableINF,
        ResetINF,
        VerifyINF
    }
    public enum WideGamutOption
    {
        SetWideGamut,
        ChangeINF,
        VerifyINF
    }
}
