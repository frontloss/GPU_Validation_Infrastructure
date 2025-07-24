namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;

    public class InfoFrame
    {
        public InfoFrameType infoFrameType { get; set; }
        public FunctionInfoFrame functionInfoFrame { get; set; }
        public DVMU_PORT port { get; set; }
        public List<string> infoFrameData { get; set; }
    }
}