using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    [Test(Type = TestType.HasPlugUnPlug)]
    class SB_PLL_Hotplug_Unplug_S3:SB_PLL_Hotplug_Unplug_Basic
    {
        [Test(Type = TestType.Method, Order = 2)]
        public override void TestStep2()
        {
            int displaysCountBeforePlug = base.EnumeratedDisplays.Count;

            base.CurrentConfig.PluggableDisplayList.ForEach(curDisp =>
            {
                base.HotUnPlug(curDisp);
            });
            base.CurrentConfig.PluggableDisplayList.ForEach(curDisp =>
            {
                base.HotPlug(curDisp, true);
                base.PowerEvent(PowerStates.S3);
            });

            if (displaysCountBeforePlug != base.EnumeratedDisplays.Count)
            {
                Log.Fail("Mismatch in no. of displays. Expected: {0} Observed: {1}",
                    displaysCountBeforePlug, base.EnumeratedDisplays.Count);
                Log.Abort("Aborting test");
            }
        }
    }

    //[Test(Type = TestType.HasPlugUnPlug)]
    //class SB_PLL_Hotplug_Unplug_S3 : SB_PLL_Hotplug_Unplug_Basic
    //{
    //    [Test(Type = TestType.Method, Order = 2)]
    //    public override void TestStep2()
    //    {
    //        base._pluggableDisplay.Keys.ToList().Intersect(base.CurrentConfig.DisplayList).ToList().ForEach(curDisp =>
    //        {
    //            base.Hotplug(FunctionName.UNPLUG, curDisp, _pluggableDisplay[curDisp]);
    //        });
    //        base._pluggableDisplay.Keys.ToList().Intersect(base.CurrentConfig.DisplayList).ToList().ForEach(curDisp =>
    //        {
    //            HotPlugUnplug obj = new HotPlugUnplug(FunctionName.PLUG, _pluggableDisplay[curDisp], "HDMI_DELL.EDID", 15);
    //            bool status = AccessInterface.SetFeature<bool, HotPlugUnplug>(Features.DvmuHotPlugStatus, Action.SetMethod, obj);
    //            base.PowerEvent(PowerStates.S3);
    //            obj.FunctionName = FunctionName.PlugEnumerate;
    //            status = AccessInterface.SetFeature<bool, HotPlugUnplug>(Features.DvmuHotPlugStatus, Action.SetMethod, obj);
    //        });
    //    }
    //}
}
