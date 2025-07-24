namespace AudioEndpointVerification
{
    using System.Text;
    public class DisplayInfo
    {
        public DisplayType DisplayType { get; set; }
        public Hierarchy DisplayHierarchy { get; set; }
        public DisplayConfigType ConfigType { get; set; }
        public uint WindowsMonitorID { get; set; }
        public string DisplayName { get; set; }
        public string CompleteDisplayName { get; set; }
        public uint CUIMonitorID { get; set; }
        public PORT Port { get; set; }
        public string SerialNum { get; set; }
        public bool isAudioCapable { get; set; }

        public DisplayInfo(string argDisplayName, DisplayType argDisplayType)
        {
            this.DisplayType = argDisplayType;
            this.DisplayName = argDisplayName;
        }
        public DisplayInfo()
        {
        }
    }
    public class EnumeratedDisplayDetails
    {
        public DisplayType DisplayType { get; set; }
        public string DisplayName { get; set; }
        public string CompleteDisplayName { get; set; }
        public string SerialNum { get; set; }
        public DisplayConfigType configType { get; set; }
        public Hierarchy DisplayHierarchy { get; set; }
    }
}
