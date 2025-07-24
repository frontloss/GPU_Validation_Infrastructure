namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    using System.Collections.Generic;
    using System;

    public class FunctionalBase
    {
        public IApplicationSettings AppSettings { get; set; }
        public IApplicationManager AppManager { get; set; }
        private List<DisplayInfo> _enumeratedDisplays;
        public List<DisplayInfo> EnumeratedDisplays
        {
            get
            {
                if (this.AppManager != null && this.AppManager.ParamInfo.ContainsKey(ArgumentType.Enumeration))
                {
                    _enumeratedDisplays = this.AppManager.ParamInfo[ArgumentType.Enumeration] as List<DisplayInfo>;
                    return _enumeratedDisplays;
                }
                else
                    return null;
            }
            set { _enumeratedDisplays = value; }
        }
        private MachineInfo _machineInfo;
        public MachineInfo MachineInfo
        {
            get
            {
                _machineInfo = this.AppManager.MachineInfo;
                return _machineInfo;
            }
            set { _machineInfo = value; }
        }
        private ParamInfo _paramInfo;
        public ParamInfo ParamInfo
        {
            get
            {
                _paramInfo = this.AppManager.ParamInfo;
                return _paramInfo;
            }
            set { _paramInfo = value; }
        }
        public int CurrentMethodIndex { get; set; }
        public int OverrideMethodIndex { get; set; }
        public DisplayConfig CurrentConfig { get; set; }

        protected uint GetWinMonitorIDByDisplayType(DisplayType argDisplayType)
        {
            DisplayInfo displayInfo = this.EnumeratedDisplays.Where(dI => dI.DisplayType == argDisplayType).FirstOrDefault();
            if (null != displayInfo)
                return displayInfo.WindowsMonitorID;
            return 0;
        }
        protected DisplayType GetDisplayTypeByWinMonitorID(uint argMonitorID)
        {
            DisplayInfo displayInfo = this.EnumeratedDisplays.Where(dI => CommonExtensions.DoesWindowsIdMatched(dI.WindowsMonitorID, argMonitorID)).FirstOrDefault();
            if (null != displayInfo)
                return displayInfo.DisplayType;
            return DisplayType.None;
        }
        protected DisplayMode GetDisplayModeByDisplayType(DisplayType argDisplayType)
        {
            DisplayInfo displayInfo = this.EnumeratedDisplays.Where(dI => dI.DisplayType == argDisplayType).FirstOrDefault();
            if (null != displayInfo)
                return displayInfo.DisplayMode;
            Log.Verbose("DisplayMode is null");
            return default(DisplayMode);
        }
        private void CopyOver(FunctionalBase argContext)
        {
            argContext.AppSettings = this.AppSettings;
            argContext.AppManager = this.AppManager;
            argContext.EnumeratedDisplays = this.EnumeratedDisplays;
            argContext.ParamInfo = this.ParamInfo;
            argContext.MachineInfo = this.MachineInfo;
            argContext.CurrentMethodIndex = this.CurrentMethodIndex;
            argContext.OverrideMethodIndex = this.OverrideMethodIndex;
        }

        public R CreateInstance<R>(R type)
        {
            object obj = Activator.CreateInstance(type.GetType());
            CopyOver(obj as FunctionalBase);
            return (R)obj;
        }
    }
}