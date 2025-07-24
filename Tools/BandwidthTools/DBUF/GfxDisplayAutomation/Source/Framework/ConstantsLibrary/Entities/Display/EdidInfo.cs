using System.Collections.Generic;
namespace Intel.VPG.Display.Automation
{
    public class EdidInfo
    {

        public DisplayType DisplayType { get; set; }
        public byte[] RawEdid { get; set; }
        public List<DisplayMode> EsatablishedTiming1 { get; set; }
        public List<DisplayMode> EsatablishedTiming2 { get; set; }
        public List<DisplayMode> StandardTiming { get; set; }
    }
}