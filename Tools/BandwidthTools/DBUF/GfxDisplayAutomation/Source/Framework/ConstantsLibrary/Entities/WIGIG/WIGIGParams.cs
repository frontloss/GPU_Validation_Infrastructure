namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;

    public class WiGigParams : Dictionary<DisplayType, string>
    {
        public DisplayType wigigDisplay { get; set; }
        public WIGIG_SYNC wigigSyncInput { get; set; }
    }
}

