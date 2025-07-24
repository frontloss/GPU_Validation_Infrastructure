namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;
    using System.Linq;
    using System;

    class SB_DisplayCStates_Mode : SB_DisplayCStates_BasicFeature
    {


        [Test(Type = TestType.Method, Order = 3)]
        public void ModeSwitch()
        {
            DisplayConfig currentConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);
            List<DisplayModeList> allModeList = AccessInterface.GetFeature<List<DisplayModeList>, List<DisplayType>>(Features.Modes, Action.GetAllMethod, Source.AccessAPI, currentConfig.DisplayList);
            allModeList.ForEach(curDisp =>
            {
                curDisp.supportedModes.ForEach(curMode =>
                {
                        ApplyModeOS(curMode, curMode.display);
                        VerifyModeOS(curMode, curMode.display);
                        base.Method();
                });
            });

        }
        protected void ApplyModeOS(DisplayMode argSelectedMode, DisplayType argDisplayType)
        {
            Log.Message(true, "Set supported mode {0} for {1}", argSelectedMode.GetCurrentModeStr(false), argDisplayType);
            argSelectedMode.display = argDisplayType;
            if (AccessInterface.SetFeature<bool, DisplayMode>(Features.Modes, Action.SetMethod, argSelectedMode))
            {
                Log.Success("Mode applied Successfully");
            }
            else
                Log.Fail("Fail to apply Mode");
        }
        protected void VerifyModeOS(DisplayMode argSelectedMode, DisplayType argDisplayType)
        {
            Log.Message(true, "Verify the  mode  for {0} through OS", argDisplayType);
            DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == argDisplayType).First();
            DisplayMode actualMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);
            if (actualMode.GetCurrentModeStr(true).Equals(argSelectedMode.GetCurrentModeStr(true)))
            {
                Log.Success("Mode {0} is verified for {1}", actualMode.GetCurrentModeStr(false), argDisplayType);
            }
            else
                Log.Fail("Mode chosen {0} is not applied for {1}! Actual is {2}", argSelectedMode.GetCurrentModeStr(false), argDisplayType, actualMode.GetCurrentModeStr(false));
        }
    } 
}