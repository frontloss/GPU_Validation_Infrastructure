namespace Intel.VPG.Display.Automation
{
    internal abstract class InitEnvironment
    {
        private IApplicationManager _manager = null;

        public InitEnvironment()
        { }
        public InitEnvironment(IApplicationManager argManager)
            : this()
        {
            this._manager = argManager;
        }

        public abstract void DoWork();

        protected IApplicationManager Manager
        {
            get { return this._manager; }
        }
        protected IAccessInterface AccessInterface
        {
            get { return this._manager.AccessInterface; }
        }
        protected MachineInfo MachineInfo
        {
            get { return this._manager.MachineInfo; }
        }
    }
}