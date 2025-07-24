using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
     [Test(Type = TestType.HasPlugUnPlug)]
    class SB_Hotplug_Unplug_CS : SB_Hotplug_Unplug_Basic
    {
        [Test(Type = TestType.Method, Order = 3)]
        public override void TestStep3()
        {
            base.CurrentConfig.DisplayList.Intersect(base._defaultEDIDMap.Keys).ToList().ForEach(curDisp =>
            {
                base.HotPlug(curDisp, base._defaultEDIDMap[curDisp], true);
                InvokePowerEvent(PowerStates.CS);
            });
        }
    }
}
