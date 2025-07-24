namespace Intel.VPG.Display.Automation
{
    public enum PsrWorkingState
    {
        PsrUninitialized = -1,
        PsrUtilityAppMissing = 0,
        PsrWrongConfig,
        PsrNotEnabledAtSink,
        PsrNotEnabledAtSource,
        PsrEnabledButNotWorking,
        PsrEnabledButLessEntryExitCount,
        PsrEnabledAndWorkingProperly
    }

    public enum PsrEventType
    {
        Default = 0,
        CursorMove,
        CursorChange,
        KeyPress,
        Nothing
    }
}
