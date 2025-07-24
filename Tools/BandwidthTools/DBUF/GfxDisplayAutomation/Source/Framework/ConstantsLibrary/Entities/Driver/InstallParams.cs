namespace Intel.VPG.Display.Automation
{
    public class InstallUnInstallParams
    {
        private int _overrideMethodIdx = -1;
        public int OverrideMethodIndex
        {
            get { return this._overrideMethodIdx; }
            set { this._overrideMethodIdx = value; }
        }
        public string ProdPath { get; set; }
        public DriverAdapterType AdapterType { get; set; }
        public string SecondaryPath { get; set; }
    }
}