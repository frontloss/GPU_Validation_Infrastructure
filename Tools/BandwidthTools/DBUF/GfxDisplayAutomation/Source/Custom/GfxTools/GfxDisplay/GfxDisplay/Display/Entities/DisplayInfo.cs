namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;

    internal class DisplayInfo
    {
        internal DisplayInfo()
        { }
        internal DisplayInfo(string argDisplayType)
            : this()
        {
            this.DisplayType = argDisplayType;
        }
        internal string DisplayType { get; set; }
        internal uint WindowsMonitorID { get; set; }
        internal string AdapterName { get; set; }
        internal DisplayMode CurrentMode { get; set; }
        internal List<DisplayMode> SupportedModes { get; set; }
        internal bool IsActive { get; set; }

        public override string ToString()
        {
            return string.Format("DisplayType:: {0}{3}WindowsMonitorID:: {1}{3}AdapterName:: {2}{3}", this.DisplayType, this.WindowsMonitorID, this.AdapterName, Environment.NewLine);
        }
    }
}