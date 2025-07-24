namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;
    using System.Linq;
    using IgfxExtBridge_DotNet;
    using System.Xml.Linq;
    using System.IO;
    using System.Text;
    using System;
    using System.Threading;

    [Test(Type = TestType.HasPlugUnPlug)]
    class SB_HDMI_YCBCR_Overlay_Resolutions : SB_HDMI_YCBCR_Overlay_Basic
    {
        private List<DisplayModeList> _commonDisplayModeList = new List<DisplayModeList>();

        public SB_HDMI_YCBCR_Overlay_Resolutions()
            : base()
        {
            base._actionAfterEnable = this.ActionAfterEnable;
            base._actionAfterDisable = this.ActionAfterDisable;
        }
        private void ActionAfterEnable()
        {
            Log.Message(true, "Apply Min, Max and Intermediate Resolution with Refresh Rate and Scaling");
            _commonDisplayModeList = GetAllModes(base.CurrentConfig.CustomDisplayList);
            List<DisplayMode> refreshRateScalingModeList = null;
            
            _commonDisplayModeList.ForEach(dML =>
            {
                if (dML.display == displayInfo.DisplayType)
                {
                    refreshRateScalingModeList = TestModes(dML.supportedModes.ToList());
                    refreshRateScalingModeList.ForEach(dM =>
                    {
                        this.ApplyNVerifyModeOS(dM, dML.display);
                        DisplayInfo displayInfos = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == dML.display).First();
                        if (((base.CurrentConfig.ConfigType.GetUnifiedConfig() != DisplayUnifiedConfig.Clone) && (displayInfos.ColorInfo.IsXvYcc)) || (base.CurrentConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Clone))
                        {
                            base.MoveCursorToPrimary(base.CurrentConfig);
                            base.StopVideo(dh, base.CurrentConfig);
                            base.PlayAndMoveVideo(dh, base.CurrentConfig);
                            base.RegisterCheck(displayInfo.DisplayType, displayInfo, displayHierarchy, eventCalled);
                            base.StopVideo(dh, base.CurrentConfig);
                            //base.CheckCRC();
                        }
                    });
                }
            });
        }
        private void ActionAfterDisable()
        {
            Log.Message(true, "Apply Min, Max and Intermediate Resolution with Refresh Rate and Scaling");
            _commonDisplayModeList = GetAllModes(base.CurrentConfig.CustomDisplayList);
            List<DisplayMode> refreshRateScalingModeList = null;

            _commonDisplayModeList.ForEach(dML =>
            {
                if (dML.display == displayInfo.DisplayType)
                {
                    refreshRateScalingModeList = TestModes(dML.supportedModes.ToList());
                    refreshRateScalingModeList.ForEach(dM =>
                    {
                        this.ApplyNVerifyModeOS(dM, dML.display);
                        DisplayInfo displayInfos = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == dML.display).First();
                        if (((base.CurrentConfig.ConfigType.GetUnifiedConfig() != DisplayUnifiedConfig.Clone) && (displayInfos.ColorInfo.IsXvYcc)) || (base.CurrentConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Clone))
                        {
                            base.MoveCursorToPrimary(base.CurrentConfig);
                            base.StopVideo(dh, base.CurrentConfig);
                            base.PlayAndMoveVideo(dh, base.CurrentConfig);
                            base.RegisterCheck(displayInfo.DisplayType, displayInfo, displayHierarchy, eventCalled);
                            base.StopVideo(dh, base.CurrentConfig);
                            //base.CheckCRC();
                        }
                    });
                }
            });
        }
        private List<DisplayModeList> GetAllModes(List<DisplayType> argCustomDisplayList)
        {
            List<DisplayModeList> allModeList = AccessInterface.GetFeature<List<DisplayModeList>, List<DisplayType>>(Features.Modes, Action.GetAllMethod, Source.AccessAPI, argCustomDisplayList);

            return allModeList;
        }
        private void ApplyNVerifyModeOS(DisplayMode argSelectedMode, DisplayType argDisplayType)
        {
            Log.Message(true, "Set supported mode {0} for {1}", argSelectedMode.GetCurrentModeStr(false), argDisplayType);
            argSelectedMode.display = argDisplayType;
            if (AccessInterface.SetFeature<bool, DisplayMode>(Features.Modes, Action.SetMethod, argSelectedMode))
                Log.Success("Mode applied Successfully");
            else
                Log.Fail("Fail to apply Mode");
            Log.Message("Verify the selected mode got applied for {0}", argDisplayType);
            DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == argDisplayType).First();
            DisplayMode actualMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);
            if (actualMode.GetCurrentModeStr(true).Equals(argSelectedMode.GetCurrentModeStr(true)))
                Log.Success("Mode {0} is applied for {1}", actualMode.GetCurrentModeStr(false), argDisplayType);
            else
                Log.Fail("Mode chosen {0} is not applied for {1}! Actual is {2}", argSelectedMode.GetCurrentModeStr(false), argDisplayType, actualMode.GetCurrentModeStr(false));
        }
        private List<DisplayMode> TestModes(List<DisplayMode> displayModeList)
        {
            List<DisplayMode> testModes = new List<DisplayMode>();
            IEnumerable<DisplayMode> modeRefreshRates = new List<DisplayMode>();

            modeRefreshRates = displayModeList.Except(displayModeList.Where(item => item.InterlacedFlag == 1).ToList());

            testModes.Add(modeRefreshRates.First());
            testModes.Add(modeRefreshRates.ElementAt(modeRefreshRates.Count() / 2));
            testModes.Add(modeRefreshRates.Last());
            //modeRefreshRates = ModesRefreshRates(testModes, displayModeList);
            return testModes;
        }
        private List<DisplayMode> ModesRefreshRates(List<DisplayMode> testMode, List<DisplayMode> entireModeList)
        {
            List<DisplayMode> modeRefreshRate = new List<DisplayMode>();
            for (int i = 0; i < testMode.Count; i++)
            {
                for (int j = 0; j < entireModeList.Count; j++)
                {
                    if ((testMode[i].HzRes == entireModeList[j].HzRes) && (testMode[i].VtRes == entireModeList[j].VtRes))
                        modeRefreshRate.Add(entireModeList[j]);
                }
            }
            return modeRefreshRate;
        }
    }
}
