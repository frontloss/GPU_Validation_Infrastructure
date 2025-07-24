namespace Intel.VPG.Display.Automation
{
    public enum TestType
    {
        PreCondition,
        Method,
        PostCondition,
        HasReboot,
        HasPlugUnPlug,
        WiDi,
        HasINFModify,
        HasUpgrade,
        ConnectedStandby,
    }
    public enum ArgumentType
    {
        TestName = 0,
        Config = 1,
        Display = 2,
        Help = 4,
        Enumeration = 3
    }
    public enum ComponentType
    {
        ApplicationManager,
        CurrentMethodIndex
    }
    public enum Source
    {
        Default,
        AccessAPI,
        Environment,
        CoreLibrary,
        CrcGenerator,
        AccessUI,
        WindowsAutomationUI
    }
    public enum DumpCategory
    {
        WatchDogdump,
        Minidump,
        Memorydump
    }
    public enum FunctionKeys
    {
        None,
        F1,
        F2,
        F3,
        F4,
        F5,
        F8,
        F9,
        F10,
        F11
    }
    public enum DecisionActions
    {
        Yes,
        No
    }

    //This should be maintained in the same order the platforms are released.
    public enum Platform
    {
        IVBM,
        HSW,
        VLV,
        BDW,
        CHV,
        SKL,
        BXT,
        KBL,
        CNL,
        GLK,
        ICL,
        ALL,
    }

    public enum FormFactor
    {
        Unknown,
        APL
    }

    public enum OSType
    {
        Default,
        WIN7,
        WIN8,
        WINBLUE,
        WINTHRESHOLD
    }

    public enum DRV_COPY_ARG
    {
        SOURCE_MISMATCH,
        DEST_MISMATCH,
        MATCH
    }
    public enum TestCleanUpType
    {
        Unknown,
        SimulatedBattery,
        LANConnection,
        SimulatedDisplay,
        Players,
        Underrun,
        WiGig,
        ValidatePowerScheme
    }
}
