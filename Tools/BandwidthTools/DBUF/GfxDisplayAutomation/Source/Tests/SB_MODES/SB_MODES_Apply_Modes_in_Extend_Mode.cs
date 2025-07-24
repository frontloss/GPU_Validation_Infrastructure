namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    using System.Collections.Generic;
    using System.Threading;
    using System.Windows.Automation;
    using System.Windows;
    using System.IO;

    class SB_MODES_Apply_Modes_in_Extend_Mode : SB_MODES_Base
    {
        private List<DisplayModeList> _commonDisplayModeList = new List<DisplayModeList>();

        [Test(Type = TestType.PreCondition, Order = 0)]
        public void TestStep0()
        {
            DisplayUnifiedConfig unifiedConfig = DisplayExtensions.GetUnifiedConfig(base.CurrentConfig.ConfigType);
            if (!(unifiedConfig == DisplayUnifiedConfig.Extended))
                Log.Abort("Test requires Config Type as Extended");
            if (base.CurrentConfig.DisplayList.Count < 2)
                Log.Abort("DualConfig test requires atleast 2 displays connected!");
        }
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            Log.Message(true, "Set current config via OS call");
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig))
                Log.Success("Config applied successfully");
            else
            {
                base.ListEnumeratedDisplays();
                Log.Abort("Config not applied!");
            }
        }
        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            Log.Message(true, "Get the list of all the modes for the config passed");
            _commonDisplayModeList = base.GetAllModes(base.CurrentConfig.CustomDisplayList);
        }
        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3()
        {
            List<DisplayMode> modeList = null;
            List<List<DisplayMode>> listModeList = new List<List<DisplayMode>>();
            List<List<DisplayMode>> supportedModelist = new List<List<DisplayMode>>();
            _commonDisplayModeList.ForEach(dML =>
            {
                modeList = GetMinMaxInterModes(dML.supportedModes.ToList());
                listModeList.Add(modeList);
                supportedModelist.Add(dML.supportedModes);
            });
            for (int modeCount = 0; modeCount < 3; modeCount++)
            {
                for (int i = 0; i < listModeList.Count; i++)
                {
                    base.ApplyModeOS(listModeList.ElementAt(i).ElementAt(modeCount), listModeList.ElementAt(i).ElementAt(modeCount).display);
                    base.VerifyModeOS(listModeList.ElementAt(i).ElementAt(modeCount), listModeList.ElementAt(i).ElementAt(modeCount).display);
                    ApplydifferentRRforSameMode(listModeList.ElementAt(i).ElementAt(modeCount), supportedModelist.ElementAt(i));
                    ApplyandVerifyScaling(listModeList.ElementAt(i).ElementAt(modeCount).display);
                }
                DisplayConfig currentConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get, Source.AccessAPI);
                SwapDisplaysAndApplyConfig(currentConfig);
            }
        }
        private void ApplydifferentRRforSameMode(DisplayMode mode, List<DisplayMode> modeList)
        {
            List<DisplayMode> RRList = modeList.Where(dI => dI.HzRes == mode.HzRes && dI.VtRes == mode.VtRes && dI.RR != mode.RR).ToList();
            if (RRList.Count != 0)
            {
                RRList.ForEach(RR =>
                {
                    base.ApplyModeOS(RR, RR.display);
                    base.VerifyModeOS(RR, RR.display);
                });
            }
        }
        private void ApplyandVerifyScaling(DisplayType display)
        {
            DisplayMode mode = GetModeCUI(display);
            mode.ScalingOptions.ForEach(scale =>
            {
                ScalingOptions scaleOption = (ScalingOptions)scale;
                DisplayScaling dsScaling = new DisplayScaling(mode.display, scaleOption);
                dsScaling.display = display;
                AccessInterface.SetFeature<bool, DisplayScaling>(Features.Scaling, Action.SetMethod, dsScaling);
                DisplayScaling curr_Scalling_SDK_Manager = AccessInterface.GetFeature<DisplayScaling, DisplayType>(Features.Scaling, Action.GetMethod, Source.AccessAPI, mode.display);
                if (dsScaling.Equals(curr_Scalling_SDK_Manager))
                    Log.Success("Current Scalling : {0}  ------  Expected(Applied) Scalling : {1}", curr_Scalling_SDK_Manager.ToString(), dsScaling);
                else
                    Log.Fail("Scalling Differ - Current Scalling from SDK Manager : {0} Expected(Applied) Scalling : {1}", curr_Scalling_SDK_Manager.ToString(), dsScaling);
            });
        }
        private List<DisplayMode> GetMinMaxInterModes(List<DisplayMode> argModeList)
        {
            List<DisplayMode> minMaxInterMode = new List<DisplayMode>();
            minMaxInterMode.Add(argModeList.First());
            minMaxInterMode.Add(argModeList[argModeList.Count / 2]);
            minMaxInterMode.Add(argModeList.Last());
            return minMaxInterMode;
        }
        private void SwapDisplaysAndApplyConfig(DisplayConfig argDisplayConfig)
        {
            Log.Message(true, "Swapping the displays");
            DisplayType primary = argDisplayConfig.PrimaryDisplay;
            DisplayType secondary = argDisplayConfig.SecondaryDisplay;
            DisplayType tertiary = argDisplayConfig.TertiaryDisplay;
            DisplayConfig config = new DisplayConfig()
            {
                ConfigType = base.CurrentConfig.ConfigType,
                PrimaryDisplay = secondary,
                SecondaryDisplay = primary
            };
            if (base.CurrentConfig.ConfigType == DisplayConfigType.TED)
            {
                config.SecondaryDisplay = tertiary;
                config.TertiaryDisplay = primary;
            }
            ApplyConfigCUI(config);
        }
    }
}
