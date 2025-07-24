namespace Intel.VPG.Display.Automation
{
    class InitEnableCommonRoutine : InitEnvironment
    {
        private TestBase _context = null;
        public InitEnableCommonRoutine(IApplicationManager argManager)
            : base(argManager)
        { }
        public override void DoWork()
        {
            _context = _context.Load(base.Manager.ParamInfo[ArgumentType.TestName] as string);
            if (_context == null)
                return;
            //Enable PIPE Underrun
            AccessInterface.SetFeature<bool>(Features.VerifyUnderrun, Action.SetMethod, true);

            //Any Other common enablement we can do it here.
        }
    }
}
