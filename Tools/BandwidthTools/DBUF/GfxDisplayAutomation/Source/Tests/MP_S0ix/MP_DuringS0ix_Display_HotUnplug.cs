namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;
    using System.Linq;
    using System.Threading;

    [Test(Type = TestType.HasPlugUnPlug)]
    [Test(Type = TestType.ConnectedStandby)]
    class MP_DuringS0ix_Display_HotUnplug : MP_S0ixBase
    {
        [Test(Type = TestType.Method, Order = 1)]
        public void TestPreCondition()
        {
            //#### if command line contains HDMI/DP and enumerated display dose't contains HDMI/DP, then we will plug Display ####
            foreach (DisplayType DT in base.CurrentConfig.PluggableDisplayList)
            {
                if (DT != base.GetInternalDisplay())
                {
                    Log.Message("Plugging external display {0}", DT);
                    base.HotPlug(DT);
                }
            }
        }

        [Test(Type = TestType.Method, Order = 2)]
        public void SetConfigMethod()
        {
            if (base.EnumeratedDisplays.Count != base.CurrentConfig.DisplayList.Count)
            {
                Log.Abort("Required display is not enumerated");
            }
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

        [Test(Type = TestType.Method, Order = 3)]
        public void SendSystemToS0ix()
        {
            foreach (DisplayType DT in DisplayExtensions.pluggedDisplayList.Reverse<DisplayType>())
            {
                Log.Message(true, "Goto S0i3 state and hotUnplug the external display which was active");
                if (DisplayExtensions.pluggedDisplayList.Count == 1)
                {
                    if (base.EnumeratedDisplays.Where(ADT => ADT.DisplayType == DT).First().isAudioCapable)
                    {
                        //if only one external display is active and audio capable panel we should check for C8+ for HSW/BDW platform.
                        //since we are unplugging any external display while resume from CS, so basically when system is under CS
                        //and external display is audio capable panel we should check c8+ state.
                        Verify_C8_Plus = true;
                    }
                }
                base.HotUnPlug(DT, true);
                base.CSCall();
                DisplayInfo DI = base.EnumeratedDisplays.Find(DTI => DTI.DisplayType.Equals(DT));
                if (DI == null)
                {
                    Log.Success("Successfully hot unplug display {0} in low power state", DT);
                }
                else
                {
                    Log.Fail("Unable to hotunplug display {0} in low power state", DT);
                }
            }
        }
    }
}
