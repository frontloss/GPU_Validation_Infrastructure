using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
     [Test(Type = TestType.HasReboot)]
     [Test(Type = TestType.HasINFModify)]
     [Test(Type = TestType.HasPlugUnPlug)]
    class SB_WideGamut_S3:SB_WideGamut_MonitorTurnOff
    {
        public SB_WideGamut_S3()
        {
            base._wideGamutLevel = WideGamutLevel.LEVEL4;
        }
        [Test(Type = TestType.Method, Order = 4)]
        public override void TestStep4()
        {
            base.InvokePowerEvent(PowerStates.S3);

        }
    }
}
