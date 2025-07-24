namespace Intel.VPG.Display.Automation
{
    using System.Text;
    using System.Collections.Generic;
    public class DisplayInfo
    {
        private DisplayColorInfo _colorInfo = null;
        private DisplayVRRInfo _vrrInfo = null;

        public DisplayInfo()
        { dongle = new Dongle(); }
        public DisplayInfo(string argDisplayName, DisplayType argDisplayType, bool argHasCRC, ConnectorType cType)
            : this()
        {
            this.DisplayType = argDisplayType;
            this.DisplayName = argDisplayName;
            this.hasCRC = argHasCRC;
            this.ConnectorType = cType;
        }
        public DisplayType DisplayType { get; set; }
        public uint WindowsMonitorID { get; set; }
        public string DisplayName { get; set; }
        public string CompleteDisplayName { get; set; }
        public DisplayMode DisplayMode { get; set; }
        public uint CUIMonitorID { get; set; }
        public PORT Port { get; set; }
        public string SerialNum { get; set; }
        public bool IsPortraitPanel { get; set; }
        public bool hasCRC { get; set; }
        public ConnectorType ConnectorType { get; set; }
        public Dongle dongle { get; set; }
        public DVMU_PORT DvmuPort { get; set; }
        public bool isAudioCapable { get; set; }
        public DPLL dpll { get; set; }
        public bool ssc { get; set; }
        public List<DisplayMode> DTDResolutions { get; set; }
        public List<DisplayMode> EdidResolutions { get; set; }
        public DisplayExtensionInfo displayExtnInformation { get; set; }
        public DisplayColorInfo ColorInfo
        {
            get { if (null == this._colorInfo) this._colorInfo = new DisplayColorInfo(); return this._colorInfo; }
        }
        public DisplayVRRInfo VRRInfo
        {
            get { if (null == this._vrrInfo) this._vrrInfo = new DisplayVRRInfo(); return this._vrrInfo; }
        }

        public override string ToString()
        {
            StringBuilder displayInfoStr = new StringBuilder();
            displayInfoStr.Append(this.DisplayType.ToString()).Append("/");
            displayInfoStr.Append(this.WindowsMonitorID.ToString()).Append("/");
            displayInfoStr.Append(this.DisplayName.ToString()).Append("/");
            displayInfoStr.Append(this.CompleteDisplayName.ToString()).Append("/");
            displayInfoStr.Append(this.DisplayMode.ToString()).Append("/");
            displayInfoStr.Append(this.CUIMonitorID.ToString()).Append("/");
            displayInfoStr.Append(this.Port.ToString()).Append("/");
            displayInfoStr.Append(this.DvmuPort.ToString()).Append("/");
            displayInfoStr.Append(this.SerialNum).Append("/");
            displayInfoStr.Append(this.ConnectorType.connectorType).Append("/");
            displayInfoStr.Append(this.ConnectorType.deviceType);
            return displayInfoStr.ToString();
        }
    }
}
