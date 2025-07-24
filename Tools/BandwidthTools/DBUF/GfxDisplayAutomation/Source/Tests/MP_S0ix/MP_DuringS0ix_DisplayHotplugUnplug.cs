namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.Threading.Tasks;

    [Test(Type = TestType.HasPlugUnPlug)]
    [Test(Type = TestType.ConnectedStandby)]
    class MP_DuringS0ix_DisplayHotplugUnplug : MP_S0ixBase
    {
        [Test(Type = TestType.Method, Order = 1)]
        public void TestPreCondition()
        {
            //#### if command line contains HDMI/DP and enumerated display dosent contains HDMI/DP, then we will plug Display ####
            foreach (DisplayType DT in base.CurrentConfig.PluggableDisplayList)
            {
                Log.Message("Plugging external display {0}", DT);
                base.HotPlug(DT);
            }
        }

        [Test(Type = TestType.Method, Order = 2)]
        public void SetConfigMethod()
        {
            if (base.CurrentConfig.EnumeratedDisplays.Count == base.CurrentConfig.DisplayList.Count)
            {
                Log.Message(true, "Set display Config using Windows API");
                if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig))
                {
                    Log.Success("Config applied successfully");
                    Log.Message("Set the maximum display mode on all the active displays");
                }
                else
                {
                    Log.Abort("Config not applied!");
                }
            }
            else
                Log.Abort("Required display is not enumerated");
        }

        [Test(Type = TestType.Method, Order = 3)]
        public void SendSystemToS0ix()
        {
            Log.Message(true, "Go to S0i3 & wait for 30 sec and resume");
            base.CSCall();
        }

        [Test(Type = TestType.Method, Order = 4)]
        public void HotUnPlugInLPState()
        {
            Log.Message(true, "Go to S0i3 & wait for 30 sec and hotunplug");
            if (DisplayExtensions.pluggedDisplayList.Count != 0)
            {
                DisplayType unPDT = DisplayExtensions.pluggedDisplayList.First();
                base.HotUnPlug(DisplayExtensions.pluggedDisplayList.First(), true);
                base.CSCall();
                DisplayInfo DI = base.EnumeratedDisplays.Find(DT => DT.DisplayType.Equals(unPDT));
                if (DI == null)
                {
                    Log.Success("Successfully hotUnplug display {0} in low power state", unPDT);
                }
                else
                {
                    Log.Fail("Unable to Hot Unplug Display {0} in low power state", unPDT);
                }
            }
        }

        [Test(Type = TestType.Method, Order = 5)]
        public void HotUnPlugPlugInLPState()
        {
            if (base.CurrentConfig.displaySequence.PluggableDisplayList.Count > 1)
            {
                Log.Message(true, "Go to S0i3 & wait for 30 sec and hotplug Display2 & unplug Display3");
                DisplayType PT = base.CurrentConfig.displaySequence.PluggableDisplayList.First();
                DisplayType UT = base.CurrentConfig.displaySequence.PluggableDisplayList.Last();

                base.HotPlug(PT, true);
                base.HotUnPlug(UT, true);
                base.CSCall();

                DisplayInfo PI = base.EnumeratedDisplays.Find(DT => DT.DisplayType.Equals(PT));
                if (PI.DisplayType == PT)
                {
                    Log.Success("Successfully plug display {0} in low power state", PT);
                }
                else
                {
                    Log.Fail("Unable to plug display {0} in low power state", PT);
                }

                DisplayInfo UI = base.EnumeratedDisplays.Find(DT => DT.DisplayType.Equals(UT));
                if (UI == null)
                {
                    Log.Success("Successfully hot unplug display {0} in low power state", UT);
                }
                else
                {
                    Log.Fail("Unable to hot unplug display {0} in low power state", UT);
                }
            }
        }
    }
}
