using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    [Test(Type = TestType.HasPlugUnPlug)]
    class SB_MBO_Entry_SD_EDP : SB_MBO_Hotplug_Unplug
    {
        [Test(Type = TestType.Method, Order = 3)]
        public override void TestStep3()
        {
            base.PlayVideo();
            base.ApplySDEDP();
            base.VerifyMBOEnable();
            base.StopVideo();
            base.UnPlugDisplays();
        }
    }
}
