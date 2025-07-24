namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    using System.Collections.Generic;

    class MP_NativeCollage_Modes : MP_NativeCollage_BAT
    {
        private List<DisplayModeList> _commonDisplayModeList = new List<DisplayModeList>();
        private List<DisplayMode> minMaxInter;
        public MP_NativeCollage_Modes()
        {
            base._performAction = this.PerformAction;
        }
        private void PerformAction()
        {
              Log.Message(true, "Apply all possible Collage Modes");
              _commonDisplayModeList = this.GetAllModes(base.CurrentConfig.CustomDisplayList);
              _commonDisplayModeList.ForEach(dML =>
              {
                  minMaxInter = new List<DisplayMode>();
                  int length = dML.supportedModes.Count;
                  minMaxInter.Add(dML.supportedModes.Last());
                  minMaxInter.Add(dML.supportedModes[length -1]);
                  minMaxInter.Add(dML.supportedModes[length - 2]);
                  minMaxInter.ForEach(dM =>
                  {
                      this.ApplyModeOS(dM, dML.display);
                      this.VerifyModeOS(dM, dML.display);
                  });
              });

        }
        private List<DisplayModeList> GetAllModes(List<DisplayType> argCustomDisplayList)
        {
            List<DisplayModeList> allModeList = AccessInterface.GetFeature<List<DisplayModeList>, List<DisplayType>>(Features.Modes, Action.GetAllMethod, Source.AccessAPI, argCustomDisplayList);
            return allModeList;
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
     
    }
}