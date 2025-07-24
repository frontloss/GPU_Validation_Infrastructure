namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.Threading.Tasks;

    [Test(Type = TestType.HasPlugUnPlug)]
    class SB_Hotplug_Unplug_Change_Edid_CS:SB_Hotplug_Unplug_Change_Edid
    {
        [Test(Type = TestType.Method, Order = 3)]
        public override void TestStep3()
        {
            base.CurrentConfig.DisplayList.Intersect(base._defaultEDIDMap.Keys).ToList().ForEach(curDisp =>
            {
                base.HotPlug(curDisp, base._changeEdid[curDisp], true);
                base.InvokePowerEvent(PowerStates.CS);
            });
        }
    }
}
