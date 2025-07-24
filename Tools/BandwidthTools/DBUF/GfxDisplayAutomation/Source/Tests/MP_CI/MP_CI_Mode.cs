namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    using System.Collections.Generic;

    class MP_CI_Mode : TestBase
    {
        protected List<DisplayModeList> allModeList = new List<DisplayModeList>();
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
            allModeList = AccessInterface.GetFeature<List<DisplayModeList>, List<DisplayType>>(Features.Modes, Action.GetAllMethod, Source.AccessAPI, base.CurrentConfig.CustomDisplayList);
        }
        [Test(Type = TestType.Method, Order = 3)]
        public virtual void TestStep3()
        {
            List<DisplayMode> modeList = null;
            allModeList.ForEach(dML =>
            {
                modeList = GetMinMaxInterModes(dML.supportedModes.ToList());
                modeList.ForEach(dM =>
                {
                    this.ApplyNVerifyModeOS(dM, dML.display);
                });
            });
        }
        protected void ApplyNVerifyModeOS(DisplayMode argSelectedMode, DisplayType argDisplayType)
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
        protected List<DisplayMode> GetMinMaxInterModes(List<DisplayMode> modeList)
        {
            List<DisplayMode> minMaxInterMode = new List<DisplayMode>();
            minMaxInterMode.Add(modeList.First());
            minMaxInterMode.Add(modeList[modeList.Count / 2]);
            minMaxInterMode.Add(modeList.Last());
            return minMaxInterMode;
        }
    }
}