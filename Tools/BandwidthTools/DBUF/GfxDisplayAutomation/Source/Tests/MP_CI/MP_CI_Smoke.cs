namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    using System;
    using System.Windows.Forms;
    using System.Collections.Generic;

    class MP_CI_Smoke : TestBase
    {
        [Test(Type = TestType.Method, Order = 0)]
        public void TestStep0()
        {
            Log.Message(true, "Disable the driver from Device manager.");
            base.AssertDriverState(Features.DisableDriver, DriverState.Disabled, new[] { 1, 1 });
        }
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            Log.Message(true, "Enable the driver from Device manager.");
            base.AssertDriverState(Features.EnableDriver, DriverState.Running, new[] { 1, 1 });
        }
    }
}