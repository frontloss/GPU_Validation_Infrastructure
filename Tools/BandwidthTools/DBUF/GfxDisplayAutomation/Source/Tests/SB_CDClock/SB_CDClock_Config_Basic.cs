using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    class SB_CDClock_Config_Basic:SB_CDClock_Base
    {
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            base.ApplyConfig(base.CurrentConfig);
            base.VerifyCDClockRegisters();
        }
    }
}
