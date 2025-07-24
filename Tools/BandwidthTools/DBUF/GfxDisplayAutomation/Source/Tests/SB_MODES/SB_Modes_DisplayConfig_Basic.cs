namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.Threading.Tasks;
    public class SB_Modes_DisplayConfig_Basic : SB_MODES_Base
    {
        protected List<DisplayConfig> _displayConfigSwitchOrder = null;
        protected DisplayConfig _currentConfig;
        protected Dictionary<DisplayUnifiedConfig, System.Action> _veriftConfigSwitch = null;
        public SB_Modes_DisplayConfig_Basic()
        {
            _veriftConfigSwitch = new Dictionary<DisplayUnifiedConfig, System.Action>();
            _veriftConfigSwitch.Add(DisplayUnifiedConfig.Clone, VerifyOptimalResolution);
            _veriftConfigSwitch.Add(DisplayUnifiedConfig.Extended, ApplyVerifyNativeResolution);
            _veriftConfigSwitch.Add(DisplayUnifiedConfig.Single, ApplyVerifyNativeResolution);
        }
        [Test(Type = TestType.PreCondition, Order = 0)]
        public virtual void TestStep0()
        {
            if (base.CurrentConfig.DisplayList.Count() < base.MachineInfo.PlatformDetails.Platform.GetDisplaysCount())
                Log.Abort("{0} requires atleast {1} Displays to be enumerated, current Display count: {2}", base.CurrentConfig.ConfigType, base.MachineInfo.PlatformDetails.Platform.GetDisplaysCount(), base.CurrentConfig.DisplayList.Count());

            DisplayConfig ddcConfig = new DisplayConfig() { ConfigType = DisplayConfigType.DDC, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay };
            DisplayConfig edConfig = new DisplayConfig() { ConfigType = DisplayConfigType.ED, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay };
            DisplayConfig sdConfig = new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay };
            if (base.MachineInfo.PlatformDetails.Platform.GetDisplaysCount() == 3)
            {
                DisplayConfig tdcConfig = new DisplayConfig() { ConfigType = DisplayConfigType.TDC, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay, TertiaryDisplay = base.CurrentConfig.TertiaryDisplay };
                DisplayConfig tedConfig = new DisplayConfig() { ConfigType = DisplayConfigType.TED, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay, TertiaryDisplay = base.CurrentConfig.TertiaryDisplay };
                this._displayConfigSwitchOrder = new List<DisplayConfig>() { ddcConfig, edConfig, tdcConfig, tedConfig, sdConfig };
            }
            else
            {
                this._displayConfigSwitchOrder = new List<DisplayConfig>() { ddcConfig, edConfig, sdConfig };
            }
        }
        [Test(Type = TestType.Method, Order = 1)]
        public virtual void TestStep1()
        {
            DisplayConfig curConfig = new DisplayConfig();
            curConfig.ConfigType = DisplayConfigType.SD;
            curConfig.PrimaryDisplay = base.CurrentConfig.PrimaryDisplay;
            ApplyConfigCUI(curConfig);

            List<DisplayModeList> _modeList = new List<DisplayModeList>();
            _modeList = base.GetMaxModeForConfig(new List<DisplayType>() { base.CurrentConfig.PrimaryDisplay }, base.CurrentConfig.ConfigType.GetUnifiedConfig());
            ApplyMode(_modeList, curConfig);
        }
        [Test(Type = TestType.Method, Order = 2)]
        public virtual void TestStep2()
        {
            _displayConfigSwitchOrder.ForEach(curConfig =>
            {
                _currentConfig = curConfig;
                ApplyConfigCUI(curConfig);
                _veriftConfigSwitch[_currentConfig.ConfigType.GetUnifiedConfig()]();
            });
        }
        protected void VerifyOptimalResolution()
        {
            Log.Message(true, "Verify Resolution on switching to {0}", _currentConfig.GetCurrentConfigStr());
            List<DisplayMode> curDispModeList = new List<DisplayMode>();
            _currentConfig.DisplayList.ForEach(curDisp =>
            {
                DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == curDisp).First();
                DisplayMode actualMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);
                curDispModeList.Add(actualMode);
            });
            List<DisplayModeList> allModeList = AccessInterface.GetFeature<List<DisplayModeList>, List<DisplayType>>(Features.Modes, Action.GetAllMethod, Source.AccessAPI, _currentConfig.DisplayList);
            allModeList.ForEach(curDisp =>
            {
                if (curDisp.supportedModes.Last().HzRes == curDispModeList.Where(dI => dI.display == curDisp.display).Select(dI => dI.HzRes).FirstOrDefault() &&
                  curDisp.supportedModes.Last().VtRes == curDispModeList.Where(dI => dI.display == curDisp.display).Select(dI => dI.VtRes).FirstOrDefault())
                {
                    Log.Success("{0} Resolution is switched to optiomal {1} ", curDisp.display, curDisp.supportedModes.Last().GetCurrentModeStr(false));
                }
                else
                {
                    Log.Fail("{0} is not switched to optimal :{1} current mode:{2}", curDisp.display, curDisp.supportedModes.Last().GetCurrentModeStr(false), curDispModeList.Where(dI => dI.display == curDisp.display).FirstOrDefault().GetCurrentModeStr(false));
                }
            });
        }
        protected void ApplyVerifyNativeResolution()
        {
            Log.Message(true, "Verify Resolution on switching to {0}", _currentConfig.GetCurrentConfigStr());
            List<DisplayMode> curDispModeList = new List<DisplayMode>();
            _currentConfig.DisplayList.ForEach(curDisp =>
            {
                DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == curDisp).First();
                DisplayMode actualMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);
                curDispModeList.Add(actualMode);
            });
            List<DisplayModeList> allModeList = AccessInterface.GetFeature<List<DisplayModeList>, List<DisplayType>>(Features.Modes, Action.GetAllMethod, Source.AccessAPI, _currentConfig.DisplayList);
            allModeList.ForEach(curDisp =>
            {
                uint nativeHZres = curDisp.supportedModes.Last().HzRes;
                uint nativeVTres = curDisp.supportedModes.Last().VtRes;
                DisplayMode curMode = curDispModeList.Where(dI => dI.display == curDisp.display).Last();
                if (curMode.HzRes == nativeHZres && curMode.VtRes == nativeVTres)
                {
                    Log.Success("{0} has switched to native resolution {1}", curDisp.display, curMode.GetCurrentModeStr(false));
                }
                else
                {
                    string res = nativeHZres + " x " + nativeVTres;
                    Log.Message("Applying native resolution {0} to {1}", res, curDisp.display);
                    ApplyModeOS(curMode, curDisp.display);

                    CheckWatermark(curMode.display);//watermark

                    //verify Mode
                    DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == curDisp.display).First();
                    DisplayMode actualMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);
                    if (actualMode.HzRes == nativeHZres && actualMode.VtRes == nativeVTres)
                        Log.Success("Native resolution {0} is applied to {1}", res, curDisp.display);
                    else
                        Log.Fail("Failed to apply Native Resolution {0} to {1}, Current Resolution {2} x{3}", curDisp.display, res, actualMode.HzRes, actualMode.VtRes);
                }
            });
        }
        protected virtual void ApplyMode(List<DisplayModeList> argDispModeList, DisplayConfig argDispConfig)
        {
            argDispModeList.ForEach(curDisp =>
            {
                curDisp.supportedModes.ForEach(curMode =>
                {
                    base.ApplyModeOS(curMode, curMode.display);
                    //CheckWatermark(curMode.display, argDispConfig);//watermark
                });
            });
        }
    }
}
