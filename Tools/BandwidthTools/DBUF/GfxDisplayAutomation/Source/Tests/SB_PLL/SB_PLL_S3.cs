using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    class SB_PLL_S3 : SB_PLL_Base_Chv
    {
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            base.ApplyConfig(base.CurrentConfig);
            base.VerifyPLLRegister(base.CurrentConfig);
        }
        [Test(Type = TestType.Method, Order = 2)]
        public virtual void TestStep2()
        {
            base.PowerEvent(PowerStates.S3);
        }
        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3()
        {
            base.VerifyConfig(base.CurrentConfig);
            base.VerifyPLLRegister(base.CurrentConfig);
        }
    }
}
