namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    using System.Collections.Generic;
    using System;
    

    class MP_NativeCollage_CommonRR : MP_NativeCollage_BAT
    {
        private List<DisplayModeList> _commonDisplayModeList = new List<DisplayModeList>();
        public MP_NativeCollage_CommonRR()
        {
            base._performAction = this.PerformAction;
            _myList = new List<DisplayConfigType>()
            {
                DisplayConfigType.Horizontal,
                DisplayConfigType.Vertical
            };
        }
        private void PerformAction()
        {
            Log.Message(true, "Apply all possible Refresh Rates");
            DisplayInfo currentDisplayInfo = null;
            List<DisplayMode> testModes = null;
            List<DisplayMode> prunedModes = null;       
           _commonDisplayModeList =  AccessInterface.GetFeature<List<DisplayModeList>, List<DisplayType>>(Features.Modes, Action.GetAllMethod, Source.AccessAPI, base.CurrentConfig.CustomDisplayList);
           _commonDisplayModeList.ForEach(dML =>
           {
               List<string> allSupportedResolutions = GetResolutionsFromCUI(dML.display);
               currentDisplayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == dML.display).First();
               prunedModes = this.PrunedCollageModes(dML.supportedModes, allSupportedResolutions);
               testModes = this.TestModes(prunedModes);
               testModes.ForEach(dM =>
                   {
                       this.ApplyModeOS(dM, dML.display);
                       this.VerifyModeOS(dM, dML.display);

                   });
           });
        }
        private void ApplyModeOS(DisplayMode argSelectedMode, DisplayType argDisplayType)
        {
            Log.Message(true, "Set supported mode {0} for {1}", argSelectedMode.GetCurrentModeStr(false), argDisplayType);
            argSelectedMode.display = argDisplayType;
            if (AccessInterface.SetFeature<bool, DisplayMode>(Features.Modes, Action.SetMethod, argSelectedMode))
                Log.Success("Mode applied Successfully");
            else
                Log.Fail("Fail to apply Mode");
        }
        private void VerifyModeOS(DisplayMode argSelectedMode, DisplayType argDisplayType)
        {
            Log.Message(true, "Verify the selected mode got applied for {0}", argDisplayType);
            DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == argDisplayType).First();
            DisplayMode actualMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);
            if (actualMode.GetCurrentModeStr(true).Equals(argSelectedMode.GetCurrentModeStr(true)))
                Log.Success("Mode {0} is verified for {1}", actualMode.GetCurrentModeStr(false), argDisplayType);
            else
                Log.Fail("Mode chosen {0} is not applied for {1}! Actual is {2}", argSelectedMode.GetCurrentModeStr(false), argDisplayType, actualMode.GetCurrentModeStr(false));
        }
        private List<string> GetResolutionsFromCUI(DisplayType display)
        {           
            AccessInterface.SetFeature(Features.SelectDisplay, Action.Set, display);
            List<string> allSupportedResolutions = AccessInterface.GetFeature<List<string>>(Features.Modes, Action.GetAll);
            return allSupportedResolutions;
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
        private List<DisplayMode> PrunedCollageModes(List<DisplayMode> displayModeList, List<string> allSupportedResolutions)
        {
            string[] resolutions;
            List<DisplayMode> prunedMode = new List<DisplayMode>();
            displayModeList.ForEach(dM =>
                {
                    allSupportedResolutions.ForEach(cuiRes =>
                    {
                        resolutions = cuiRes.Split('x');
                        uint hres = Convert.ToUInt32(resolutions[0]);
                        uint vres = Convert.ToUInt32(resolutions[1]);
                    if ((dM.HzRes == hres && dM.VtRes == vres))
                        prunedMode.Add(dM);
                    });                   
                });
            return prunedMode;
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