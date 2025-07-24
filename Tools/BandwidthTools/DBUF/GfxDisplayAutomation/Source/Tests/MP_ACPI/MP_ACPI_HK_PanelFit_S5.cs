namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;
   
    class MP_ACPI_HK_PanelFit_S5 : MP_ACPI_HK_PanelFit
    {
        [Test(Type = TestType.Method, Order = 3)]
        public override void TestStep3()
        {
            base.PerformTriDisplay = false;
            List<ScalingOptions> scalingOptionList = ApplyNonNativeResolutionToEDP();                  
            ScalingOptions currentScaling = base.GetCurrentScaling();
            base.PerformPowerEvent(PowerStates.S5, 5);            
        }
        [Test(Type = TestType.Method, Order = 4)]
        public override void TestStep4()
        {
            Log.Message("Resume from S5");
            List<ScalingOptions> scalingOptionList = ApplyNonNativeResolutionToEDP(); 
            //PerformACPIf8(scalingOptionList,true);
            PerformACPIF11();
            PerformACPIToggleSequence();
        }
    }
}
