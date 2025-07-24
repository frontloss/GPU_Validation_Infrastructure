namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;

        class MP_ACPI_HK_PanelFit_S4:MP_ACPI_HK_PanelFit
    {
        [Test(Type = TestType.Method, Order = 3)]
        public override void TestStep3()
        {
            base.PerformTriDisplay = false;
            List<ScalingOptions> scalingOptionList = ApplyNonNativeResolutionToEDP();

            ScalingOptions currentScaling = base.GetCurrentScaling();
            base.PerformPowerEvent(PowerStates.S4, 45);
            if (base.GetCurrentScaling() != currentScaling)
            {
                Log.Fail(false,"Expected Scaling after resuming from S4  was {0}", currentScaling.ToString());
            }
            else
            {
                Log.Success("Scaling {0} retained after resuming from S4", currentScaling.ToString());
            }
            //PerformACPIf8(scalingOptionList, true);
            PerformACPIF11();
        }
        [Test(Type = TestType.Method, Order = 4)]
        public override void TestStep4()
        {
            PerformACPIToggleSequence();
        }
    }
}
