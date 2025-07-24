namespace Intel.VPG.Display.Automation
{
    public class Dongle
    {
        DongleType type;
        public DongleType Type
        {
            get { return type; }
            set { type = value; }
        }
        DisplayType downStreamType;
        public DisplayType DownStreamType
        {
            get { return downStreamType; }
            set { downStreamType = value; }
        }        

        //private DisplayType GetDisplayType(List<DisplayInfo> enumeratedDisplays, uint sdkMonId)
        //{
        //    switch (enumeratedDisplays.Where(DT => DT.CUIMonitorID == sdkMonId).First().DisplayType)
        //    {
        //        case DisplayType.EDP:
        //            return DisplayType.EDP;
        //        case DisplayType.MIPI:
        //            return DisplayType.MIPI;
        //        case DisplayType.CRT:
        //            return DisplayType.CRT;
        //        case DisplayType.HDMI:
        //        case DisplayType.HDMI_2:
        //        case DisplayType.HDMI_3:
        //            return DisplayType.HDMI;
        //        case DisplayType.DP:
        //        case DisplayType.DP_2:
        //        case DisplayType.DP_3:
        //            return DisplayType.DP;
        //        case DisplayType.WIDI:
        //            return DisplayType.WIDI;
        //        default:
        //            return DisplayType.None;
        //    }
        //}
    }
}
