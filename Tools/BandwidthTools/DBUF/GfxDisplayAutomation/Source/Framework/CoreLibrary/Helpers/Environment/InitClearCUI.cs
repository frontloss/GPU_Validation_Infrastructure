namespace Intel.VPG.Display.Automation
{
    class InitClearCUI : InitEnvironment
    {
        public InitClearCUI(IApplicationManager argManager)
            : base(argManager)
        { }
        public override void DoWork()
        {
            AccessInterface.SetFeature(Features.CUIHeaderOptions, Action.Set, CUIWindowOptions.Close);
        }
    }
}