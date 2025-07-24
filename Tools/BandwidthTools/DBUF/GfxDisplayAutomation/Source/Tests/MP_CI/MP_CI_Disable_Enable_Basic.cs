namespace Intel.VPG.Display.Automation
{
    using System;

    class MP_CI_Disable_Enable_Basic : TestBase
    {
        DriverInfo drivInfo;
        [Test(Type = TestType.PreCondition, Order = 0)]
        public void TestPreCondition()
        {
            Log.Message(true, "Set current config via OS call");
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig))
                Log.Success("Config applied successfully");
            else
            {
                base.ListEnumeratedDisplays();
                Log.Fail("Config not applied!");
            }
        }
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            Log.Message(true, "Disable the driver from Device manager.");
            base.AssertDriverState(Features.DisableDriver, DriverState.Disabled, new[] { 1, 1 });

            drivInfo = AccessInterface.GetFeature<DriverInfo, DriverAdapterType>(Features.DriverFunction, Action.GetMethod, Source.AccessAPI, DriverAdapterType.Intel);
            if (drivInfo.Status.ToLower().Equals("disabled"))
                Log.Success("IGD Disabled.");
            else
                Log.Fail("IGD not Disabled.");
        }
        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            Log.Message(true, "Enable the driver from Device manager.");
            base.AssertDriverState(Features.EnableDriver, DriverState.Running, new[] { 1, 1 });

            drivInfo = AccessInterface.GetFeature<DriverInfo, DriverAdapterType>(Features.DriverFunction, Action.GetMethod, Source.AccessAPI, DriverAdapterType.Intel);
            if (drivInfo.Status.ToLower().Equals("running"))
            {
                Log.Success("IGD Enabled.");
                AccessInterface.SetFeature(Features.CUIHeaderOptions, Action.Set, CUIWindowOptions.Close);
            }
            else
                Log.Fail("IGD not Enabled.");
        }
    }
}
