using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
     [Test(Type = TestType.HasReboot)]
     [Test(Type = TestType.HasINFModify)]
    class SB_WideGamut_S5:SB_WideGamut_MonitorTurnOff
    {
        public SB_WideGamut_S5()
        {
            base._wideGamutLevel = WideGamutLevel.LEVEL2;
        }
        [Test(Type = TestType.Method, Order = 4)]
        public override void TestStep4()
        {
            base.InvokePowerEvent(PowerStates.S5);
        }
    }
}
