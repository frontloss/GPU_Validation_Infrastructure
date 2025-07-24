namespace Intel.VPG.Display.Automation
{
    using Microsoft.Win32;

    public class RegistryParams
    {
        private int _overrideMethodIdx = -1;
        public int OverrideMethodIndex
        {
            get { return this._overrideMethodIdx; }
            set { this._overrideMethodIdx = value; }
        }
        public RegistryKey registryKey { get; set; }
        public string keyName { get; set; }
        public int value { get; set; }
        public InfChanges infChanges { get; set; }
        public string path { get; set; }
    }
}