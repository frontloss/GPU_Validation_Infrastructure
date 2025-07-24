namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Linq;
    using System.ComponentModel;
    using System.Collections.Generic;
    using System.IO;
    using System.Diagnostics;
    using System.Xml;

    public static class DisplayExtensions
    {
        private static Dictionary<DisplayConfigType, DisplayUnifiedConfig> _configsMapping = null;
        private static Dictionary<DisplayConfigType, int> _displaysCount = null;
        private static Dictionary<Platform, int> _dispCountByPlatform = null;
        private static IAccessInterface _accessInterface = null;
        public static List<PipePlaneParams> pipePlaneInfo = new List<PipePlaneParams>();
        public static bool AudioWTVideoEnable = false;
        public static bool EnableMonitorTurnOff = false;
        public static List<DisplayType> pluggedDisplayList = null;
        public static int OverridePowerParamDelay = 0;
        
        static DisplayExtensions()
        {
            if (null == _configsMapping)
            {
                _configsMapping = new Dictionary<DisplayConfigType, DisplayUnifiedConfig>();
                _configsMapping.Add(DisplayConfigType.SD, DisplayUnifiedConfig.Single);
                _configsMapping.Add(DisplayConfigType.DDC, DisplayUnifiedConfig.Clone);
                _configsMapping.Add(DisplayConfigType.ED, DisplayUnifiedConfig.Extended);
                _configsMapping.Add(DisplayConfigType.TDC, DisplayUnifiedConfig.Clone);
                _configsMapping.Add(DisplayConfigType.TED, DisplayUnifiedConfig.Extended);
                _configsMapping.Add(DisplayConfigType.Horizontal, DisplayUnifiedConfig.Collage);
                _configsMapping.Add(DisplayConfigType.Vertical, DisplayUnifiedConfig.Collage);
            }
            if (null == _displaysCount)
            {
                _displaysCount = new Dictionary<DisplayConfigType, int>();
                _displaysCount.Add(DisplayConfigType.SD, 1);
                _displaysCount.Add(DisplayConfigType.DDC, 2);
                _displaysCount.Add(DisplayConfigType.ED, 2);
                _displaysCount.Add(DisplayConfigType.TDC, 3);
                _displaysCount.Add(DisplayConfigType.TED, 3);
            }
            if (null == _dispCountByPlatform)
            {
                _dispCountByPlatform = new Dictionary<Platform, int>();
                _dispCountByPlatform.Add(Platform.VLV, 2);
            }
            pluggedDisplayList = new List<DisplayType>();
        }

        public static void InitAccessInterface(IAccessInterface argAccessInterface)
        {
            _accessInterface = argAccessInterface;
        }
        public static DisplayType GetEnumMember(this DisplayType argContext, string argReference)
        {
            DisplayType displayType;
            if (!Enum.TryParse<DisplayType>(argReference, out displayType))
            {
                foreach (var field in argContext.GetType().GetFields())
                {
                    if (field.IsDefined(typeof(DescriptionAttribute), false))
                    {
                        var alias = field.GetCustomAttributes(false).FirstOrDefault();
                        if (null != alias && ((DescriptionAttribute)alias).Description.Equals(argReference))
                        {
                            Enum.TryParse<DisplayType>(field.Name, out displayType);
                            break;
                        }
                    }
                }
            }
            return displayType;
        }
        public static DisplayUnifiedConfig GetUnifiedConfig(this DisplayConfigType argConfigType)
        {
            return _configsMapping[argConfigType];
        }
        public static DisplayConfigType GetConfigTypeByCount(int argDisplaysCount)
        {
            return _displaysCount.Where(kV => kV.Value.Equals(argDisplaysCount)).Select(kV => kV.Key).LastOrDefault();
        }
        public static int GetDisplaysCount(this DisplayConfigType argConfigType)
        {
            return _displaysCount[argConfigType];
        }
        public static int GetDisplaysCount(this Platform argPlatform)
        {
            if (_dispCountByPlatform.ContainsKey(argPlatform))
                return _dispCountByPlatform[argPlatform];
            return 3;   //3-pipe
        }
        public static DisplayConfigType GetConfigType(this DisplayUnifiedConfig argUnifiedConfigType, int argDisplaysCount)
        {
            List<DisplayConfigType> configTypeList = _configsMapping.Where(kV => kV.Value == argUnifiedConfigType).Select(kV => kV.Key).ToList();
            foreach (DisplayConfigType dCType in configTypeList)
                if (dCType == _displaysCount.Where(kV => (kV.Key == dCType && kV.Value.Equals(argDisplaysCount))).Select(kV => kV.Key).FirstOrDefault())
                    return dCType;
            return default(DisplayConfigType);
        }
        public static DisplayType GetDisplay(this List<DisplayType> argDisplayList, DisplayHierarchy argHierarchy)
        {
            DisplayType displayType = DisplayType.None;
            if (null != argDisplayList && !argDisplayList.Count.Equals(0))
            {
                switch (argHierarchy)
                {
                    case DisplayHierarchy.Display_1:
                        displayType = argDisplayList.First();
                        break;
                    case DisplayHierarchy.Display_2:
                        if (argDisplayList.Count > 1)
                            displayType = argDisplayList.Skip(1).First();
                        break;
                    case DisplayHierarchy.Display_3:
                        if (argDisplayList.Count > 2)
                            displayType = argDisplayList.Skip(2).First();
                        break;
                }
            }
            return displayType;
        }
        public static DisplayHierarchy GetDispHierarchy(this DisplayConfig currentConfig, DisplayType disp)
        {
            if (disp == currentConfig.PrimaryDisplay)
                return DisplayHierarchy.Display_1;
            else if (disp == currentConfig.SecondaryDisplay)
                return DisplayHierarchy.Display_2;
            else if (disp == currentConfig.TertiaryDisplay)
                return DisplayHierarchy.Display_3;

            Log.Alert("Display Hierarchy not found for {0}", disp);
            return DisplayHierarchy.Unsupported;
        }
        public static string GetCurrentConfigStr(this DisplayConfig argConfig)
        {
            if (null == argConfig.DisplayList || argConfig.DisplayList.Count.Equals(0))
                argConfig.DisplayList = argConfig.CustomDisplayList;
            return string.Concat(argConfig.ConfigType, " ", argConfig.DisplayList.GetDisplayListStr());
        }
        public static string GetCurrentAudioEndpointDevice(this AudioDataProvider argEndpontData)
        {
            if (argEndpontData.ListAudioEndpointDevice.Count == 0)
                return "NULL";
            return string.Join(",", argEndpontData.ListAudioEndpointDevice);
        }
        public static string GetCurrentModeStr(this DisplayMode argMode, bool argResOnly)
        {
            string modeStr = string.Concat(argMode.HzRes, "x", argMode.VtRes);
            if (argResOnly)
                return modeStr;
            modeStr = string.Concat(modeStr, ", ", argMode.RR, argMode.InterlacedFlag.Equals(0) ? "p Hz" : "i Hz", ", ", argMode.Bpp, " Bit", ", ", argMode.Angle, " Deg,", " PixelClock ", argMode.pixelClock);
            if (null != argMode.ScalingOptions && !argMode.ScalingOptions.Count.Equals(0))
                modeStr = string.Concat(modeStr, ", ", (PanelFit)argMode.ScalingOptions.First());
            return modeStr;
        }
        public static string GetDriverInfoStr(this DriverInfo argDriverInfo)
        {
            return string.Concat(argDriverInfo.Name, " ", argDriverInfo.Version, " ", argDriverInfo.Status);
        }
        public static string GetDisplayListStr(this List<DisplayType> argDisplayList)
        {
            return string.Join("+", argDisplayList.Select(d => d.ToString()));
        }
        public static bool CanFlip(this DisplayMode argContext)
        {
            return (argContext.Angle == 90 || argContext.Angle == 270);
        }
        public static void VerifyOrientation(this DisplayMode curMode)
        {
            switch (curMode.Angle)
            {
                case 0:
                case 180:
                    if (curMode.HzRes > curMode.VtRes)
                        Log.Success("Lanscape orientation is maintained at an angle{0}", curMode.Angle);
                    else
                        Log.Fail("Lanscape orientation is not  maintained at an angle{0}", curMode.Angle);
                    break;
                case 90:
                case 270:
                    if (curMode.HzRes < curMode.VtRes)
                        Log.Success("Portrait orientation is maintained at an angle{0}", curMode.Angle);
                    else
                        Log.Fail("Portrait orientation is not maintained at an angle{0}", curMode.Angle);
                    break;

            }

        }
        public static string GetDriverVesion(string DriverPath)
        {
            string[] data = File.ReadLines(DriverPath).ToArray();
            foreach (string line in data)
            {
                if (line.ToLower().Contains("driverver"))
                {
                    return line.Split('=').Last();
                }
            }
            return string.Empty;
        }
        public static DisplayType GetDisplayType(DisplayType display)
        {
            DisplayType displayType = DisplayType.None;
            switch (display)
            {
                case DisplayType.CRT:
                    displayType = DisplayType.CRT;
                    break;
                case DisplayType.DP:
                case DisplayType.DP_2:
                case DisplayType.DP_3:
                    displayType = DisplayType.DP;
                    break;
                case DisplayType.EDP:
                    displayType = DisplayType.EDP;
                    break;
                case DisplayType.MIPI:
                    displayType = DisplayType.MIPI;
                    break;
                case DisplayType.HDMI:
                case DisplayType.HDMI_2:
                case DisplayType.HDMI_3:
                    displayType = DisplayType.HDMI;
                    break;
                case DisplayType.WIGIG_DP:
                case DisplayType.WIGIG_DP2:
                    displayType = DisplayType.WIGIG_DP;
                    break;
                default:
                    break;
            }
            return displayType;
        }
        public static void SwapValue<T>(ref T value1, ref T value2)
        {
            T temp = value1;
            value1 = value2;
            value2 = temp;
        }

        public static bool VerifyCSSystem(MachineInfo argMachineInfo)
        {
            Log.Message("Checking CS test pre condition");
            Log.Verbose("checking connected standby system using powercfg.exe /a");
            Process pwrCfgProcess = new Process();
            pwrCfgProcess = CommonExtensions.StartProcess("powercfg.exe", " /a");
            bool CSFlag = false;
            string standbyStringName = string.Empty;
            if (argMachineInfo.OS.Type == OSType.WINTHRESHOLD)
            {
                standbyStringName = "standby (s0 low power idle)";
            }
            else
                standbyStringName = "standby (connected)";
            while (!pwrCfgProcess.StandardOutput.EndOfStream)
            {
                string line = pwrCfgProcess.StandardOutput.ReadLine();
                if (line == "The following sleep states are not available on this system:")
                    break;
                if (line.Trim().ToLower().Contains(standbyStringName.Trim()))
                {
                    Log.Verbose("Connected Standby Setup Ready for execution");
                    CSFlag = true;
                }
            }
            pwrCfgProcess.Close();
            return CSFlag;
        }

        public static string GetEdidFile(DisplayType display)
        {
            string path = Directory.GetCurrentDirectory() + @"\EDIDFiles";
            bool defaultEdidSelection = false;
            string edidFile = string.Empty;

            XmlDocument edidDetails = new XmlDocument();
            edidDetails.Load(@"Mapper\EDIDData.map");
            XmlNode eventBenchmarkRoot = edidDetails.SelectSingleNode("/EDIDData/Default_EDID");
            if (null == eventBenchmarkRoot.Attributes["selection_mode"].Value)
                Log.Abort("Selection Mode Attribute is missing from EDIDData.map");

            Boolean.TryParse(eventBenchmarkRoot.Attributes["selection_mode"].Value.Trim(), out defaultEdidSelection);

            /*****************************************************************************************
             * If default edid selection mode is true in EDIDData.map, then it will select specifyed 
             * edid in display field. else it will select any random edid file which is present in 
             * EDIDFiles location.
             *****************************************************************************************/

            if (defaultEdidSelection)
            {
                foreach (XmlNode childNode in eventBenchmarkRoot.ChildNodes)
                {
                    if (childNode.Attributes["type"].Value.Trim().ToUpper().Equals(display.ToString()))
                    {
                        edidFile = childNode.Attributes["edid"].Value.Trim();
                        break;
                    }
                }
            }
            else
            {
                string[] edidFileList = Directory.GetFiles(path, "*.EDID")
                .Where(Name => Name.ToUpper().Contains(display.ToString().ToUpper().Split('_').FirstOrDefault())).ToArray();
                if (edidFileList.Length > 0)
                {
                    edidFile = Path.GetFileName(edidFileList[new Random().Next(0, edidFileList.Length)]);
                }
            }
            return edidFile;
        }

        public static void ValidatePowerScheme()
        {
            string high_Performance_GUID = "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c";
            string balanced_GUID = "381b4222-f694-41f0-9685-ff5bb260df2e";
            bool isBalancedPowerScheme = false;
            Process sysPowerScheme = CommonExtensions.StartProcess("powercfg", "/getactivescheme", 5);
            while (!sysPowerScheme.StandardOutput.EndOfStream)
            {
                string line = sysPowerScheme.StandardOutput.ReadLine();
                if (line.ToLower().Contains(balanced_GUID))
                {
                    Log.Verbose("Current power scheme is balenced");
                    isBalancedPowerScheme = true;
                    break;
                }
            }
            if (isBalancedPowerScheme)
            {
                Log.Message("Change power scheme to High Performance");
                sysPowerScheme = CommonExtensions.StartProcess("powercfg", "/s " + high_Performance_GUID, 0);
                sysPowerScheme.WaitForExit();
                if (sysPowerScheme.ExitCode == 0)
                    Log.Verbose("Successfully change current power scheme to high performance");
                else
                    Log.Fail("Failed to change current power scheme to high performance");
            }
        }
    }
}