namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;

    public class VerifyCRCArgs
    {
        public DisplayType display { get; set; }
        public DisplayConfig currentConfig { get; set; }
        public bool ComputePipeCRC { get; set; }
    }
}
