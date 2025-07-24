namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;

    public class XvYccYcbXr
    {
        public DisplayType displayType { get; set; }
        public ColorType colorType { get; set; }
        public int isEnabled { get; set; }
        public DisplayConfig currentConfig { get; set; }
    }
}
