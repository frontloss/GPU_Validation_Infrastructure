namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;

    class SB_PowerWell_Disable_Enable_Driver : SB_PowerWell_DisplayConfig
    {
        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3()
        {
            base.AssertDriverState(Features.DisableDriver, DriverState.Disabled, new[] { 1, 1 });

            base.AssertDriverState(Features.EnableDriver, DriverState.Running, new[] { 1, 1 });

            System.Threading.Thread.Sleep(3000);
        }

        [Test(Type = TestType.Method, Order = 4)]
        public void TestStep4()
        {
            VerifyConfig(base.CurrentConfig);
            VerifyPowerWell();
        }
    }
}