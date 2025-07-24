namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;
    using System.Linq;
    using System.Threading;

    [Test(Type = TestType.HasPlugUnPlug)]
    class MP_ConnectedStandbyHotUnplugSingleDisplay : MP_ConnectedStandbyBase
    {
        HotPlugUnplug plugUnplugHandle;

        [Test(Type = TestType.Method, Order = 1)]
        public void TestPreCondition()
        {
            powerParam.Delay = 60;
            plugUnplugHandle = new HotPlugUnplug(FunctionName.OPEN, DVMU_PORT.PORTA, "HDMI_DELL.EDID", 4);
            if (!AccessInterface.SetFeature<bool, HotPlugUnplug>(Features.DvmuHotPlugStatus, Action.SetMethod, plugUnplugHandle))
            {
                base.CleanUP();
                Log.Abort("DVMU open command failed");
            }
            //#### if command line contains HDMI and enumerated display dosent contains HDMI, then we will plug HDMI ####
            if (base.CurrentConfig.CustomDisplayList.Exists(DT => DT.Equals(DisplayType.HDMI)) &&
                !base.CurrentConfig.EnumeratedDisplays.Exists(DT => DT.DisplayType.Equals(DisplayType.HDMI)))
            {
                Log.Message(true, "Plugging HDMI display to run the test");
                plugUnplugHandle.FunctionName = FunctionName.PLUG;
                if (!AccessInterface.SetFeature<bool, HotPlugUnplug>(Features.DvmuHotPlugStatus, Action.SetMethod, plugUnplugHandle))
                {
                    base.CleanUP();
                    Log.Abort("Unable to plug HDMI to run the test");
                }
            }
        }

        [Test(Type = TestType.Method, Order = 2)]
        public void SetConfigMethod()
        {
            Log.Message(true, "Set display Config using Windows API");
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig))
            {
                Log.Success("Config applied successfully");
                Log.Message("Set the maximum display mode on all the active displays");
                if (!base.CurrentConfig.EnumeratedDisplays.Exists(DT => DT.DisplayType.Equals(DisplayType.HDMI)))
                {
                    Log.Verbose("Currently HDMI is not enumerated, plug HDMI to run the test normally");
                    plugUnplugHandle.FunctionName = FunctionName.PLUG;
                    if (!AccessInterface.SetFeature<bool, HotPlugUnplug>(Features.DvmuHotPlugStatus, Action.SetMethod, plugUnplugHandle))
                    {
                        base.CleanUP();
                        Log.Abort("Unable to plug HDMI");
                    }
                }
            }
            else
            {
                this.CleanUP();
                Log.Abort("Config not applied!");
            }
        }

        [Test(Type = TestType.Method, Order = 3)]
        public void HotUnplug()
        {
            Thread.Sleep(6000);
            List<DisplayInfo> currentEnumeratedDisplay = base.CurrentConfig.EnumeratedDisplays;
            Log.Message(true, "Doing hotunplug while system in CS state.");
            Log.Verbose("befor Hotunplug enumeratedDisplay listed below");
            base.PrintEnumeratedDisplay(base.CurrentConfig.EnumeratedDisplays);
            Log.Verbose("Send DVMU unplug command after 12 sec");
            plugUnplugHandle.FunctionName = FunctionName.UNPLUG;
            plugUnplugHandle.Delay = 12;
            if (AccessInterface.SetFeature<bool, HotPlugUnplug>(Features.DvmuHotPlugStatus, Action.SetMethod, plugUnplugHandle))
            {
                this.S0ixCall();
                if (base.CurrentConfig.EnumeratedDisplays.Count() < currentEnumeratedDisplay.Count())
                {
                    DisplayInfo unplugDisplay = currentEnumeratedDisplay.Except(base.CurrentConfig.EnumeratedDisplays).First();
                    Log.Success("Display {0} is not enumerated after hot-unplug", unplugDisplay.DisplayType);
                    base.PrintEnumeratedDisplay(base.CurrentConfig.EnumeratedDisplays);
                }
                else
                {
                    List<DisplayInfo> enmDisplay = AccessInterface.GetFeature<List<DisplayInfo>>(Features.DisplayEnumeration, Action.GetAll);
                    if (base.CurrentConfig.EnumeratedDisplays.Count() < enmDisplay.Count())
                    {
                        DisplayInfo unplugDisplay = currentEnumeratedDisplay.Except(base.CurrentConfig.EnumeratedDisplays).First();
                        Log.Success("Display {0} is not enumerated after hot-unplug", unplugDisplay.DisplayType);
                        base.PrintEnumeratedDisplay(base.CurrentConfig.EnumeratedDisplays);
                    }
                    else
                    {
                        Log.Fail("Display is enumerated after hotunplug");
                        base.PrintEnumeratedDisplay(base.CurrentConfig.EnumeratedDisplays);
                    }
                }
            }
            else
                Log.Fail("DVMU unplug command failed");
        }
    }
}
