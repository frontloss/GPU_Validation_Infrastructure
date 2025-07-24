using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    class SB_PLL_S4:SB_PLL_S3
    {
        [Test(Type = TestType.Method, Order = 2)]
        public override void TestStep2()
        {
            base.PowerEvent(PowerStates.S4);
        }
    }
}
