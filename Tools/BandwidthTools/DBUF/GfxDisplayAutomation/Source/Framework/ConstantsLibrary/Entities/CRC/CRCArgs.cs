namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;

    public class CRCArgs
    {
        public DisplayType displayType { get; set; }
        public PORT port { get; set; }
        public DisplayConfig currentConfig { get; set; }
        public uint CRCValue { get; set; }
        public bool ComputePipeCRC { get; set; }
    }
}
