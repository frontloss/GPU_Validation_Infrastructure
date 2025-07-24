namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;
    using System.Linq;
    using System.Threading;
    using System.Runtime.InteropServices;
    using System;
using System.Diagnostics;
    class MP_ACPI_HK_PanelFit : MP_ACPI_Base
    {
        protected bool PerformTriDisplay = true;
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
            base.SetConfig(base.CurrentConfig);
        }
        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            DisplayConfig currentConfig = new DisplayConfig();
            currentConfig.ConfigType = DisplayConfigType.SD;
            currentConfig.PrimaryDisplay = base.GetInternalDisplay();
            currentConfig.DisplayList = new List<DisplayType>() { base.GetInternalDisplay() };
            base.SetConfig(currentConfig);
        }
        [Test(Type = TestType.Method, Order = 3)]
        public virtual void TestStep3()
        {
            List<ScalingOptions> scalingOptionList = ApplyNonNativeResolutionToEDP();
            PerformACPIF11();
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
                base.SetConfig(base.CurrentConfig);
                List<ScalingOptions> scalingOptionList = ApplyNonNativeResolutionToEDP();
                PerformACPIF11();
            }
        }

        protected ScalingOptions GetCurrentScaling()
        {
            DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == DisplayType.EDP).First();
            DisplayMode actualMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);
            return (ScalingOptions)actualMode.ScalingOptions.First();
        }

        protected void PerformACPIF11()
        {
            if (AccessInterface.SetFeature<bool, string>(Features.ACPIFunctions, Action.SetMethod, "F11"))
            {
                Log.Success("ACPI Switched successfull for dislay config {0} " ,base.CurrentConfig.ToString());
            }
            else
            {
                Log.Fail("ACPI Switching Failed for the display config {0}",base.CurrentConfig.ToString());
            }
        }
        protected List<ScalingOptions> ApplyNonNativeResolutionToEDP()
        {
            List<ScalingOptions> allscalingOptionList = new List<ScalingOptions>();
            List<ScalingOptions> scalingOptionList;
            List<DisplayType> paramDispList = base.EnumeratedDisplays.Select(dI => dI.DisplayType).ToList(); 
            foreach (DisplayType disptype in paramDispList)
            {
                List<DisplayModeList> allMode = AccessInterface.GetFeature<List<DisplayModeList>, List<DisplayType>>(Features.Modes, Action.GetAllMethod, Source.AccessAPI, paramDispList);
                List<DisplayMode> edpSupportedModes = allMode.Where(dI => dI.display == disptype).Select(dI => dI.supportedModes).FirstOrDefault();
                if (edpSupportedModes != null)
                {
                    edpSupportedModes.Reverse();
                    if (AccessInterface.SetFeature<bool, DisplayMode>(Features.Modes, Action.SetMethod, edpSupportedModes.Last()))
                        Log.Success("Mode applied Successfully");
                    else
                        Log.Fail(false, "Fail to apply Mode");

                    scalingOptionList = new List<ScalingOptions>();
                    scalingOptionList = edpSupportedModes.Last().ScalingOptions.Select(dI => (ScalingOptions)dI).ToList();
                    foreach (ScalingOptions scoption in scalingOptionList)
                    {
                        if (!allscalingOptionList.Contains(scoption))
                        {
                            allscalingOptionList.Add(scoption);
                        }
                    }
                }
            }
          
            return allscalingOptionList;
        }
        protected void PerformACPIToggleSequence()
        {
            base.ReadACPIDataFromFile();
            if (base._acpiToggle.Count() > 0)
            {
                string key = "F1";
                List<DisplayConfig> acpiToggleList = new List<DisplayConfig>();
                if (!base._acpiToggle.ContainsKey(key))
                {
                    Log.Alert("F1 sequence eliminated,hence performing Toggle sequence for {0}", base._acpiToggle.First().Key.ToString());
                    key = base._acpiToggle.First().Key.ToString();
                }
                acpiToggleList = base._acpiToggle.First().Value;
                DisplayConfig initialConfig = acpiToggleList.First();
                if ((base.MachineInfo.OS.Type == OSType.WINTHRESHOLD) &&
                    (DisplayExtensions.GetUnifiedConfig(initialConfig.ConfigType).Equals(DisplayUnifiedConfig.Clone)))
                {
                    Log.Message("Initial config is {0} so returning from key {1}", initialConfig.ConfigType, base._acpiToggle.First().Key.ToString());
                    return;
                }
                base.SetConfig(initialConfig);

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
                            PerformACPIF11();
                        }

                        if ((base.MachineInfo.OS.Type == OSType.WINTHRESHOLD) &&
                        (DisplayExtensions.GetUnifiedConfig(osConfig.ConfigType).Equals(DisplayUnifiedConfig.Clone)))
                        {
                            DisplayConfig dConfig = new DisplayConfig()
                            {
                                ConfigType = DisplayConfigType.SD,
                                PrimaryDisplay = base.CurrentConfig.PrimaryDisplay
                            };
                            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, dConfig))
                                Log.Message("Config (SD {0}) applied successfully", dConfig.PrimaryDisplay);
                            else
                                Log.Fail("Config (SD {0}) not applied!", dConfig.PrimaryDisplay);
                            break;
                        }
                    }
                }
            }
        }
        protected void PerformPowerEvent(PowerStates argPowerState, int argDelay)
        {
            Log.Message(true, "Performing power event {0}", argPowerState.ToString());
            PowerParams powerParamObj = new PowerParams();
            powerParamObj.PowerStates = argPowerState;
            powerParamObj.Delay = argDelay;
            base.EventResult(powerParamObj.PowerStates, base.InvokePowerEvent(powerParamObj, powerParamObj.PowerStates));
        }
    }
}


