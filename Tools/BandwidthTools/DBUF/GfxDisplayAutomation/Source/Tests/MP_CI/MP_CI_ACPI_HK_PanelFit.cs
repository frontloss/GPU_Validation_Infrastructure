namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;
    using System.Linq;
    using System.Threading;
    using System.Xml.Linq;
    using System;
    using System.IO;

    class MP_CI_ACPI_HK_PanelFit : TestBase
    {
        protected bool PerformTriDisplay = true;
        private Dictionary<string, List<DisplayConfig>> _acpiToggle = null;
        private Dictionary<PORT, List<DisplayType>> _portDisplayMapping = null;
        [Test(Type = TestType.PreCondition, Order = 0)]
        public void TestPreCondition()
        {
            if (!base.CurrentConfig.DisplayList.Contains(DisplayType.EDP))
            {
                Log.Abort("Display list must contain EDP");
            }
            if (base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == DisplayType.EDP).Select(dI => dI.DisplayType).FirstOrDefault() == DisplayType.None)
            {
                Log.Abort("EDP must be enumerated");
            }
        }
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            this.SetConfig(base.CurrentConfig);
        }
        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            DisplayConfig currentConfig = new DisplayConfig();
            currentConfig.ConfigType = DisplayConfigType.SD;
            currentConfig.PrimaryDisplay = base.GetInternalDisplay();
            currentConfig.DisplayList = new List<DisplayType>() { base.GetInternalDisplay() };
            this.SetConfig(currentConfig);
        }
        [Test(Type = TestType.Method, Order = 3)]
        public virtual void TestStep3()
        {
            List<ScalingOptions> scalingOptionList = ApplyNonNativeResolutionToEDP();
            PerformACPIf8(scalingOptionList, true);
        }
        [Test(Type = TestType.Method, Order = 4)]
        public virtual void TestStep4()
        {
            PerformACPIToggleSequence();
        }
        [Test(Type = TestType.Method, Order = 5)]
        public void TestStep5()
        {
            if (PerformTriDisplay && (base.CurrentConfig.ConfigType == DisplayConfigType.TDC || base.CurrentConfig.ConfigType == DisplayConfigType.TED))
            {
                this.SetConfig(base.CurrentConfig);
                List<ScalingOptions> scalingOptionList = ApplyNonNativeResolutionToEDP();
                PerformACPIf8(scalingOptionList, true);
            }
        }
        private ScalingOptions GetCurrentScaling()
        {
            DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == DisplayType.EDP).First();
            DisplayMode actualMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);
            return (ScalingOptions)actualMode.ScalingOptions.First();
        }
        private void PerformACPIf8(List<ScalingOptions> argScalingOptionList,bool argRetryFlag)
        {

            Log.Message(true, "Performing ACPI Hotkey F8");
            ScalingOptions originalScaling = GetCurrentScaling();
            ScalingOptions scaleResult; int count = 0; ScalingOptions previousScaling = originalScaling;
            do
            {
                bool f8Result = AccessInterface.SetFeature<bool, FunctionKeys>(Features.ACPIFunctions, Action.SetMethod, FunctionKeys.F8);
                scaleResult = GetCurrentScaling();
                if (f8Result && !previousScaling.Equals(scaleResult) && argScalingOptionList.Contains(scaleResult))
                    Log.Success("Scaling option changed to {0}", scaleResult.ToString());
                else
                {
                    Log.Sporadic(false, "ACPI hotkey switch failed,{0} retained after switching", scaleResult.ToString());
                    if (argRetryFlag)
                    {
                        Log.Message("Performing a retry");
                        Thread.Sleep(5000);
                        PerformACPIf8(argScalingOptionList, false);						
                    }
                    break;
                }
                count++;
                previousScaling = scaleResult;
            } while (scaleResult != originalScaling);

        }
        private List<ScalingOptions> ApplyNonNativeResolutionToEDP()
        {
            List<DisplayType> paramDispList=new List<DisplayType>(){DisplayType.EDP};
            List<DisplayModeList> allMode = AccessInterface.GetFeature<List<DisplayModeList>, List<DisplayType>>(Features.Modes, Action.GetAllMethod, Source.AccessAPI,paramDispList);
            List<DisplayMode> edpSupportedModes = allMode.Where(dI => dI.display == DisplayType.EDP).Select(dI => dI.supportedModes).FirstOrDefault();
            DisplayMode currentMode = new DisplayMode();
            edpSupportedModes.Reverse();

            int maxScalingCount = 1;
            foreach (DisplayMode dispMode in edpSupportedModes)
            {
                if (dispMode.ScalingOptions.Count() > maxScalingCount)
                {
                    currentMode = dispMode;
                    maxScalingCount = dispMode.ScalingOptions.Count();
                }
            }
            if (AccessInterface.SetFeature<bool, DisplayMode>(Features.Modes, Action.SetMethod, currentMode))
                Log.Success("Mode applied Successfully");
            else
                Log.Fail(false, "Fail to apply Mode");

            List<ScalingOptions> scalingOptionList = new List<ScalingOptions>();
            scalingOptionList = currentMode.ScalingOptions.Select(dI => (ScalingOptions)dI).ToList();
            return scalingOptionList;
        }
        private void PerformACPIToggleSequence()
        {
            this.ReadACPIDataFromFile();
            if (this._acpiToggle.Count() > 0)
            {
                string key = "F1";
                List<DisplayConfig> acpiToggleList = new List<DisplayConfig>();
                if (!this._acpiToggle.ContainsKey(key))
                {
                    Log.Alert("F1 sequence eliminated,hence performing Toggle sequence for {0}", this._acpiToggle.First().Key.ToString());
                    key = this._acpiToggle.First().Key.ToString();
                }
                acpiToggleList = this._acpiToggle.First().Value;
                DisplayConfig initialConfig = acpiToggleList.First();
                this.SetConfig(initialConfig);

                acpiToggleList.RemoveAt(0);
                foreach (DisplayConfig currentDispConfig in acpiToggleList)
                {
                    Log.Message(true, "Performing acpi default switch for key {0} ", key);
                    AccessInterface.SetFeature<bool, string>(Features.ACPIFunctions, Action.SetMethod, key);
                    DisplayConfig osConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get, Source.AccessAPI);
                    Log.Verbose(osConfig.GetCurrentConfigStr());
                    if (osConfig.ConfigType != currentDispConfig.ConfigType ||
                        osConfig.CustomDisplayList.Except(currentDispConfig.DisplayList).Count() != 0)
                    {
                        Log.Fail(false, "Mismatch in config in key {0} Expected Configuration:{1} Current Configuration:{2}", key, currentDispConfig.GetCurrentConfigStr(), osConfig.GetCurrentConfigStr());
                        break;
                    }
                    else
                    {
                        Log.Success("ACPI switch configutaion {0} match the expected sequence for Key: {1}", osConfig.GetCurrentConfigStr(), key);
                        if (osConfig.CustomDisplayList.Contains(DisplayType.EDP))
                        {
                            List<ScalingOptions> scalingOptionList = ApplyNonNativeResolutionToEDP();
                            PerformACPIf8(scalingOptionList, true);
                        }
                    }
                }
            }
        }
        private void ReadACPIDataFromFile()
        {
            _acpiToggle = new Dictionary<string, List<DisplayConfig>>();
            _portDisplayMapping = new Dictionary<PORT, List<DisplayType>>();
            _portDisplayMapping.Add(PORT.PORTB, new List<DisplayType> { DisplayType.DP });
            _portDisplayMapping.Add(PORT.PORTC, new List<DisplayType> { DisplayType.HDMI });
            _portDisplayMapping.Add(PORT.PORTX, new List<DisplayType> { DisplayType.EDP, DisplayType.MIPI });
            _portDisplayMapping.Add(PORT.PORTY, new List<DisplayType> { DisplayType.CRT });

            string fileName = string.Concat(Directory.GetCurrentDirectory(), "\\Mapper\\ACPIConfig.map");
            if (!File.Exists(fileName))
                Log.Abort("File {0} not found", fileName);
            XDocument doc = XDocument.Load(fileName);
            var platform = from plt in doc.Descendants("Platform")
                           where plt.Attribute("id").Value.ToString().Contains(base.MachineInfo.PlatformDetails.Platform.ToString())
                           select new
                           {
                               platformId = plt.Attribute("id").Value,
                               key = plt.Descendants("Key")
                           };
            foreach (var currentKey in platform.First().key)
            {
                List<DisplayConfig> DispConfigList = new List<DisplayConfig>();
                var toggleSequence = currentKey.Descendants("ToggleSequence");

                var toggleList = from toggle in toggleSequence.Descendants("Toggle")
                                 select new
                                 {
                                     config = toggle.Attribute("config").Value,
                                     portList = toggle.Descendants("Port")
                                 };
                foreach (var currentToggle in toggleList)
                {
                    DisplayConfig currentDispConfig = new DisplayConfig();
                    currentDispConfig.DisplayList = new List<DisplayType>();

                    bool validDisplays = true;
                    DisplayConfigType dispconfigType;
                    Enum.TryParse<DisplayConfigType>(currentToggle.config.ToString(), true, out dispconfigType);
                    currentDispConfig.ConfigType = dispconfigType;
                    foreach (var currentPort in currentToggle.portList)
                    {
                        PORT port; DisplayType currentDispType;
                        Enum.TryParse<PORT>(currentPort.Value.ToString(), true, out port);
                        List<DisplayType> dispList = _portDisplayMapping[port];
                        if (dispList.Count() == 1)
                        {
                            currentDispType = dispList.First();
                        }
                        else
                        {
                            currentDispType = base.CurrentConfig.EnumeratedDisplays.Where(dI => dispList.Contains(dI.DisplayType)).Select(dI => dI.DisplayType).FirstOrDefault();
                        }
                        if (currentDispType != DisplayType.None)
                            currentDispType = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == currentDispType).Select(dI => dI.DisplayType).FirstOrDefault();
                        if (currentDispType != DisplayType.None)
                            currentDispConfig.DisplayList.Add(currentDispType);
                        else
                        {
                            validDisplays = false;
                            break;
                        }
                    }
                    if (validDisplays)
                        DispConfigList.Add(currentDispConfig);
                }
                if (DispConfigList.Count > 0)
                {
                    DispConfigList.Add(DispConfigList.First());//append the first entry
                    _acpiToggle.Add(currentKey.Attribute("id").Value.ToString(), DispConfigList);
                }
            }
        }
        private void SetConfig(DisplayConfig argDisplayConfig)
        {
            argDisplayConfig.PrimaryDisplay = argDisplayConfig.DisplayList.GetDisplay(DisplayHierarchy.Display_1);
            argDisplayConfig.SecondaryDisplay = argDisplayConfig.DisplayList.GetDisplay(DisplayHierarchy.Display_2);
            argDisplayConfig.TertiaryDisplay = argDisplayConfig.DisplayList.GetDisplay(DisplayHierarchy.Display_3);

            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, argDisplayConfig))
                Log.Success("Config applied successfully");
            else
                Log.Fail(false, "Failed to apply config");
        }
    }
}


