using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Threading;

namespace Intel.VPG.Display.Automation
{
    [Test(Type = TestType.HasReboot)]
    [Test(Type = TestType.HasPlugUnPlug)]
    [Test(Type = TestType.HasINFModify)]
    class SB_WideGamut_Plug_Unplug_S4 : SB_WideGamut_Plug_Unplug_S3
    {
        public SB_WideGamut_Plug_Unplug_S4()
        {
            base._wideGamutLevel = WideGamutLevel.LEVEL2;
            base._powerState = PowerStates.S4;
        }        
    }
}
