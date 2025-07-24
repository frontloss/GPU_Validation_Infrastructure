namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;

    public class HotPlugUnPlugContext
    {
        public List<HotPlugUnplug> HotPlugUnPlugInfo { get; set; }
        public Dictionary<DisplayType, string> EDID_Files { get; set; }
        public bool PlugUnplugInLowPower { get; set; }
        public HotPlugUnPlugContext()
        {
            this.EDID_Files = new Dictionary<DisplayType, string>();
            this.EDID_Files.Add(DisplayType.EDP, DisplayExtensions.GetEdidFile(DisplayType.EDP));
            this.EDID_Files.Add(DisplayType.DP, DisplayExtensions.GetEdidFile(DisplayType.DP));
            this.EDID_Files.Add(DisplayType.DP_2, DisplayExtensions.GetEdidFile(DisplayType.DP_2));
            this.EDID_Files.Add(DisplayType.HDMI, DisplayExtensions.GetEdidFile(DisplayType.HDMI));
            this.EDID_Files.Add(DisplayType.HDMI_2, DisplayExtensions.GetEdidFile(DisplayType.HDMI_2));
            this.HotPlugUnPlugInfo = new List<HotPlugUnplug>();
            this.PlugUnplugInLowPower = false;
        }
    }
}
