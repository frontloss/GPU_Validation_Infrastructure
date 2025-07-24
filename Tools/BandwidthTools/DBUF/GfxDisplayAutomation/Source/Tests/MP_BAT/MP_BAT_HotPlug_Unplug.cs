namespace Intel.VPG.Display.Automation
{
    using System.Linq;

    [Test(Type = TestType.HasPlugUnPlug)]
    class MP_BAT_HotPlug_Unplug : TestBase
    {
        [Test(Type = TestType.PreCondition, Order = 0)]
        public void TestPreCondition()
        {
            if (base.CurrentConfig.DisplayList.Count < 2)
                Log.Abort("This test requires atleast 2 displays connected!");
        }
        [Test(Type = TestType.Method, Order = 1)]
        public virtual void TestStep1()
        {
            if (base.CurrentConfig.PluggableDisplayList.Count != 0)
            {
                if (base.HotPlug(base.CurrentConfig.PluggableDisplayList.First()))
                {
                    Log.Success("Successfully hotplug display {0}", base.CurrentConfig.PluggableDisplayList.First());
                }
                else
                    Log.Fail("Failed to hot plug display {0}", base.CurrentConfig.PluggableDisplayList.First());
            }
        }

        [Test(Type = TestType.Method, Order = 2)]
        public virtual void TestStep2()
        {
            if (base.CurrentConfig.PluggableDisplayList.Count > 1)
            {
                if (base.HotPlug(base.CurrentConfig.PluggableDisplayList.Last()))
                {
                    Log.Success("Successfully hotplug display {0}", base.CurrentConfig.PluggableDisplayList.Last());
                }
                else
                    Log.Fail("Failed to hot plug display {0}", base.CurrentConfig.PluggableDisplayList.Last());
            }
        }
        [Test(Type = TestType.Method, Order = 3)]
        public virtual void TestStep3()
        {
            if (DisplayExtensions.pluggedDisplayList.Count != 0)
            {
                if (base.HotUnPlug(DisplayExtensions.pluggedDisplayList.First()))
                {
                    Log.Success("Successfully hot unplug display {0}", DisplayExtensions.pluggedDisplayList.First());
                }
                else
                    Log.Fail("Failed to hot unplug display {0}", DisplayExtensions.pluggedDisplayList.First());
            }
        }
        [Test(Type = TestType.Method, Order = 4)]
        public virtual void TestStep4()
        {
            if (DisplayExtensions.pluggedDisplayList.Count > 1)
            {
                if (base.HotUnPlug(DisplayExtensions.pluggedDisplayList.Last()))
                {
                    Log.Success("Successfully hot unplug display {0}", DisplayExtensions.pluggedDisplayList.Last());
                }
                else
                    Log.Fail("Failed to hot unplug display {0}", DisplayExtensions.pluggedDisplayList.Last());
            }
        }
        [Test(Type = TestType.Method, Order = 5)]
        public void TestStep5()
        {
            Log.Message("Disable and enable the driver from Device manager.");
            base.AssertDriverState(Features.DisableDriver, DriverState.Disabled, new[] { 3, 3 });
            Log.Verbose("\n Driver is Disabled");
            base.AssertDriverState(Features.EnableDriver, DriverState.Running, new[] { 3, 3 });
            Log.Verbose("\n Driver is Enabled");
        }
        protected void InvokePowerEvent(PowerParams PowerParamsObj)
        {
            base.EventResult(PowerParamsObj.PowerStates, base.InvokePowerEvent(PowerParamsObj, PowerParamsObj.PowerStates));
        }
        protected bool CheckEnumeratedDisplayContents(DisplayType DispType)
        {
            if (base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == DispType).Select(dI => dI.DisplayType).FirstOrDefault() != DisplayType.None)
                return true;
            else
                return false;

        }
    }
}