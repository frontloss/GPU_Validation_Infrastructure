namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    using System.Collections.Generic;
    using System.Threading;

    [Test(Type = TestType.HasPlugUnPlug)]
    class MP_ACPI_HK_HotplugUnplug_S3 : MP_ACPI_HK_DisplaySwitch_Default
    {
        private PowerParams powerParams = null;
        internal PowerStates powerState;
        public MP_ACPI_HK_HotplugUnplug_S3()
        {
            powerParams = new PowerParams();
            powerParams.Delay = 40;
            powerState = PowerStates.S3;
        }
        [Test(Type = TestType.PreCondition, Order = 0)]
        public override void TestPreCondition()
        {
            foreach (DisplayType DT in base.CurrentConfig.PluggableDisplayList)
            {
                Log.Message("{0} is not enumerated..Plugging it", DT);
                if (base.HotPlug(DT))
                {
                    Log.Success("Display {0} is plugged successfully", DT);
                }
            }
            if (base.CurrentConfig.EnumeratedDisplays.Count != base.CurrentConfig.DisplayList.Count)
            {
                Log.Abort("Required display is not enumerated");
            }
            base.TestPreCondition();
        }

        [Test(Type = TestType.Method, Order = 5)]
        public void TestStep5()
        {
            Log.Verbose(true, "Put the system to sleep and and unplug the display in {0}", powerState);
            foreach (DisplayType display in DisplayExtensions.pluggedDisplayList.Reverse<DisplayType>())
            {
                DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == display).First();
                if (displayInfo != null)
                {
                    Log.Verbose("Unplug display {0}", displayInfo.DisplayType);
                    if (base.HotUnPlug(displayInfo.DisplayType, true))
                    {
                        Log.Message("{0}  will be HotPlugged in 10 Seconds after system go to {1}", displayInfo.DisplayType, powerState);
                    }
                        
                    Log.Message("Putting the system into {0} state", powerState);
                    base.InvokePowerEvent(powerParams, powerState);
                    Thread.Sleep(1000);
                    displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == display).FirstOrDefault();
                    if (displayInfo == null)
                    {
                        Log.Success("Successfully hot unplug display {0} in low power stare", display);
                    }
                    else
                    {
                        Log.Fail("Failed to hot unplug display {0} in low power state", display);
                    }
                    Log.Message(true, "After {0}, plug back {1}", powerState, display);
                    if (base.HotPlug(display))
                    {
                        Log.Success("Successfully plug display {0} after lowpower state", display);
                    }
                    else
                        Log.Fail("Unable to plug display {0} after lowpower state", display);
                }
                else
                    Log.Message("Cannot plug and unplug {0}", displayInfo.DisplayType);
            }
        }
        [Test(Type = TestType.Method, Order = 6)]
        public void TestStep6()
        {
            Log.Message(true, "Verify Switching sequence after resuming from {0}", powerState);
            base.TestStep1();
            base.TestStep2();
            base.TestStep3();
            base.TestStep4();
        }
    }
}



