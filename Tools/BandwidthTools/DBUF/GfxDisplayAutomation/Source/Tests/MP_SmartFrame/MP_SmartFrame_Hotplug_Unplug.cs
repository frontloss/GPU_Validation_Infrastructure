namespace Intel.VPG.Display.Automation
{
    using System;
    using System.IO;
    using System.Linq;
    using System.Threading;
    using System.Collections.Generic;

    [Test(Type = TestType.HasReboot)]
    [Test(Type = TestType.HasPlugUnPlug)]
    class MP_SmartFrame_Hotplug_Unplug : MP_SmartFrame_Base
    {
        [Test(Type = TestType.PreCondition, Order = 0)]
        public void TestPreCondition()
        {
            foreach (DisplayType DT in base.CurrentConfig.PluggableDisplayList)
            {
                Log.Message(true, "Verify {0} is not connected", DT);
                if ((base.CurrentConfig.EnumeratedDisplays.Any(dI => dI.DisplayType.Equals(DT))))
                    Log.Abort("{0} is already connected...Aborting the test", DT);
            }

            Log.Message(true, "Set config SD {0} via OS", base.GetInternalDisplay());
            DisplayConfig config = new DisplayConfig();
            config.ConfigType = DisplayConfigType.SD;
            config.PrimaryDisplay = base.GetInternalDisplay();
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, config))
                Log.Success("Config applied successfully");
            else
            {
                base.ListEnumeratedDisplays();
                Log.Abort("Config not applied!");
            }
        }

        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            Log.Message(true, "Enable Smart Frame");
            base.EnableRegistryForSF();
        }
        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            base.EnableSF();
            base.VerifySmartFrameStatus(true, SmartFrameRegistryEvent);
        }
        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3()
        {
            foreach(DisplayType DT in base.CurrentConfig.PluggableDisplayList)
            {
                Log.Message(true, "{0} is not enumerated..Plugging {1}", DT, DT);
                if (base.HotPlug(DT))
                {
                    Log.Success("Successfully hotplug display {0}", DT);
                }
                else
                {
                    Log.Fail("Unable to hotplug display {0}", DT);
                }
            }
        }

        [Test(Type = TestType.Method, Order = 4)]
        public void TestStep4()
        {
            Log.Message(true, "Disable Smart Frame");
            base.DisableSF();
            base.DisableRegistryForSF();
        }
        [Test(Type = TestType.Method, Order = 5)]
        public void TestStep5()
        {
            base.VerifySmartFrameStatus(false, SmartFrameRegistryEvent);
            Log.Message(true, "Unplug external display and plug it back");
            foreach (DisplayType DT in DisplayExtensions.pluggedDisplayList.Reverse<DisplayType>())
            {
                if (base.HotUnPlug(DT))
                {
                    Log.Success("Successfully hot unplug display {0}", DT);
                }
                else
                    Log.Fail("Unable to hotunplug display {0}", DT);
            }

            foreach (DisplayType DT in base.CurrentConfig.PluggableDisplayList)
            {
                if (base.HotPlug(DT))
                {
                    Log.Success("Successfully hotplug display {0}", DT);
                }
                else
                    Log.Fail("Unable to hotunplug display {0}", DT);
            }
        }

        [Test(Type = TestType.Method, Order = 6)]
        public void TestStep6()
        {
            Log.Message(true, "Swtich to SF mode.");
            base.EnableRegistryForSF();
        }

        [Test(Type = TestType.Method, Order = 7)]
        public void TestStep7()
        {
            base.EnableSF();
            base.VerifySmartFrameStatus(true, SmartFrameRegistryEvent);
        }
    }
}