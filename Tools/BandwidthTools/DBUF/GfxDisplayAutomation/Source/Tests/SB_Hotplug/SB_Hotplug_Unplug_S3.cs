namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    [Test(Type = TestType.HasPlugUnPlug)]
    class SB_Hotplug_Unplug_S3 : SB_Hotplug_Unplug_Basic
    {
        [Test(Type = TestType.Method, Order = 3)]
        public override void TestStep3()
        {
            base.CurrentConfig.DisplayList.Intersect(base._defaultEDIDMap.Keys).ToList().ForEach(curDisp =>
            {
                base.HotPlug(curDisp, base._defaultEDIDMap[curDisp], true);
                InvokePowerEvent(PowerStates.S3);
            });
        }
    }
}
