namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;

    class SB_PowerWell_PowerEvents : SB_PowerWell_DisplayConfig
    {
        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3()
        {
            PowerEvent(PowerStates.S3);
        }

        [Test(Type = TestType.Method, Order = 4)]
        public void TestStep4()
        {
            VerifyConfig(base.CurrentConfig);
            VerifyPowerWell();
        }

        [Test(Type = TestType.Method, Order = 5)]
        public void TestStep5()
        {
            PowerEvent(PowerStates.S4);
        }

        [Test(Type = TestType.Method, Order = 6)]
        public void TestStep6()
        {
            VerifyConfig(base.CurrentConfig);
            VerifyPowerWell();
        }

        [Test(Type = TestType.Method, Order = 7)]
        public void TestStep7()
        {
            PowerEvent(PowerStates.S5);
        }

        [Test(Type = TestType.Method, Order = 8)]
        public void TestStep8()
        {
            VerifyConfig(base.CurrentConfig);
            VerifyPowerWell();
        }
    }
}