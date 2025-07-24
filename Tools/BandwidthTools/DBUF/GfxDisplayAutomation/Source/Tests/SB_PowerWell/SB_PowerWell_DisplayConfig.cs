namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;

    class SB_PowerWell_DisplayConfig : SB_PowerWell_Base
    {
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            ApplyConfig(base.CurrentConfig);   
        }

        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            VerifyPowerWell();    
        }
    }
}