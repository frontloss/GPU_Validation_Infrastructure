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
    class SB_HDMI_YCBCR_Resolutions : SB_HDMI_YCBCR_Basic
    {
        private List<DisplayModeList> _commonDisplayModeList = new List<DisplayModeList>();

        public SB_HDMI_YCBCR_Resolutions()
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
            var r = new Random();
            _commonDisplayModeList.ForEach(dML =>
            {
                if ((base.CurrentConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Clone) || (dML.display == displayInfo.DisplayType))
                {
                    refreshRateScalingModeList = TestModes(dML.supportedModes.ToList());
                    refreshRateScalingModeList.ForEach(dM =>
                    {
                        this.ApplyNVerifyModeOS(dM, dML.display);
                        DisplayInfo displayInfos = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == dML.display).First();
                        if (((base.CurrentConfig.ConfigType.GetUnifiedConfig() != DisplayUnifiedConfig.Clone) && (displayInfos.ColorInfo.IsXvYcc)) || (base.CurrentConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Clone))
                        {
                            base.RegisterCheck(displayInfo.DisplayType, displayInfo, displayHierarchy, eventCalled);
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

            var r = new Random();
            _commonDisplayModeList.ForEach(dML =>
            {
                if ((base.CurrentConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Clone) || (dML.display == displayInfo.DisplayType))
                {
                    refreshRateScalingModeList = TestModes(dML.supportedModes.ToList());
                    refreshRateScalingModeList.ForEach(dM =>
                    {
                        this.ApplyNVerifyModeOS(dM, dML.display);
                        DisplayInfo displayInfos = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == dML.display).First();
                        if (((base.CurrentConfig.ConfigType.GetUnifiedConfig() != DisplayUnifiedConfig.Clone) && (displayInfos.ColorInfo.IsXvYcc)) || (base.CurrentConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Clone))
                        {
                            Log.Message("Verify registers after Resolution Change");
                            base.RegisterCheck(displayInfo.DisplayType, displayInfo, displayHierarchy, eventCalled);
                            //base.CheckCRC();
                        }
                    });
                }
            });
        }
        private List<DisplayModeList> GetAllModes(List<DisplayType> argCustomDisplayList)
        {
            List<DisplayModeList> listDisplayMode = new List<DisplayModeList>();
            List<DisplayModeList> allModeList = AccessInterface.GetFeature<List<DisplayModeList>, List<DisplayType>>(Features.Modes, Action.GetAllMethod, Source.AccessAPI, argCustomDisplayList);
            List<DisplayMode> commonModes = null;
            if (base.CurrentConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Clone)
            {
                commonModes = allModeList.Where(dML => dML.display == base.CurrentConfig.PrimaryDisplay).Select(dML => dML.supportedModes).FirstOrDefault();
                allModeList.Skip(1).ToList().ForEach(dML => commonModes = commonModes.Intersect(dML.supportedModes, new DisplayMode()).ToList());
                if (commonModes.Count() > 0)
                    listDisplayMode.Add(new DisplayModeList() { display = base.CurrentConfig.PrimaryDisplay, supportedModes = commonModes });
            }
            else
                listDisplayMode = allModeList;
            return listDisplayMode;
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
            List<DisplayMode> modeRefreshRates = new List<DisplayMode>();
            testModes.Add(displayModeList.First());
            testModes.Add(displayModeList[displayModeList.Count / 2]);
            testModes.Add(displayModeList.Last());
            modeRefreshRates = ModesRefreshRates(testModes, displayModeList);
            return modeRefreshRates;
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
