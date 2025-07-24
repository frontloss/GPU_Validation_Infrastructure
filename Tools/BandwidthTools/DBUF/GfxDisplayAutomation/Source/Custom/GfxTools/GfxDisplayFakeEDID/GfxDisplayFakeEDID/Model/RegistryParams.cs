namespace Intel.VPG.Display.Automation
{
    using System;

    class RegistryParams
    {
        public string FakeEDIDFile { get; set; }
        public string FakeEDIDBlock { get; set; }
        public EDIDBlockType EDIDBlockType
        {
            get
            {
                EDIDBlockType edidBlockType = EDIDBlockType.None;
                Enum.TryParse(this.FakeEDIDBlock.Replace(" ", "_"), true, out edidBlockType);
                return edidBlockType;
            }
        }
        public DisplayInfo DisplayInfo { get; set; }
        public string RegistryOption { get; set; }
        public int PortValue { get; set; }
    }
}
