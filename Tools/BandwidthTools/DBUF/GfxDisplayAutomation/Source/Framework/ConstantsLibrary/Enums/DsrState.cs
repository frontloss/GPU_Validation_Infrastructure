namespace Intel.VPG.Display.Automation
{
    public enum DsrWorkingState
    {
        DsrUninitialized = -1,
        DsrUtilityAppMissing = 0,
        DsrWrongConfig,
        DsrSupportabilityFailed,
        DsrEnabledButNotWorking,
        DsrEnabledButLessEntryExitCount,
        DsrEnabledAndWorkingProperly
    }
}
