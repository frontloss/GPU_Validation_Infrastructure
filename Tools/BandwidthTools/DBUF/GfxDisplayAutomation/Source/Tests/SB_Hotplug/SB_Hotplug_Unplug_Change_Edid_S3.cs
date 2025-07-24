namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    [Test(Type = TestType.HasPlugUnPlug)]
    class SB_Hotplug_Unplug_Change_Edid_S3 : SB_Hotplug_Unplug_Change_Edid
    {
        protected PowerStates _PowerState;
        public SB_Hotplug_Unplug_Change_Edid_S3()
        {
            _PowerState = PowerStates.S3;
        }

        [Test(Type = TestType.Method, Order = 3)]
        public override void TestStep3()
        {
            base.CurrentConfig.DisplayList.Intersect(base._defaultEDIDMap.Keys).ToList().ForEach(curDisp =>
            {
                base.HotPlug(curDisp, base._changeEdid[curDisp], true);
                base.InvokePowerEvent(_PowerState);
            });
        }
    }
}
