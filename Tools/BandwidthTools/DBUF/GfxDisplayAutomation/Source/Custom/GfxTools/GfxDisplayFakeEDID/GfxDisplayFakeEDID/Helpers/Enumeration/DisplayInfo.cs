namespace Intel.VPG.Display.Automation
{
    using System.Text;

    class DisplayInfo
    {
        public DisplayInfo()
        { }
        public DisplayInfo(string argDisplayName, DisplayType argDisplayType)
            : this()
        {
            this.DisplayType = argDisplayType;
            this.DisplayName = argDisplayName;
        }
        public DisplayType DisplayType { get; set; }
        public string CompleteDisplayName { get; set; }
        public string DisplayName { get; set; }
        public uint WindowsMonitorID { get; set; }
        public uint CUIMonitorID { get; set; }
        public PORT Port { get; set; }
        public int PortValue { get; set; }
        public string ManufacturerName { get; set; }
        public byte[] ManufacturerInfo { get; set; }
        public string ProductCode { get; set; }
        public byte[] ProductInfo { get; set; }
        public bool IsActive { get; set; }
        public string ActiveStatus
        {
            get { return this.IsActive ? "Active" : "InActive"; }
        }
        public byte[] BaseEDIDBlock { get; set; }
        public byte[] CEAExtnBlock { get; set; }

        public override string ToString()
        {
            StringBuilder displayInfoStr = new StringBuilder();
            displayInfoStr.Append(this.DisplayType.ToString()).Append("/");
            displayInfoStr.Append(this.CompleteDisplayName.ToString()).Append("/");
            displayInfoStr.Append(this.Port.ToString()).Append("/");
            return displayInfoStr.ToString();
        }
    }
}
