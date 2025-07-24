namespace Intel.VPG.Display.Automation
{
    using System.Linq;

    [Test(Type = TestType.HasPlugUnPlug)]
    class SB_Hotplug_Unplug_Basic : SB_Hotplug_Base
    {
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            base.CurrentConfig.DisplayList.ForEach(curDisp =>
            {
                if (base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == curDisp).Select(dI => dI.DisplayType).FirstOrDefault() == DisplayType.None)
                {
                    base.HotPlug(curDisp, base._defaultEDIDMap[curDisp]);
                }
            });
            base.ApplyConfigOS(base.CurrentConfig);
        }
        [Test(Type = TestType.Method, Order = 2)]
        public virtual void TestStep2()
        {
            base.CurrentConfig.DisplayList.Intersect(base._defaultEDIDMap.Keys).ToList().ForEach(curDisp =>
            {
                base.HotUnPlug(curDisp);
            });
        }
        [Test(Type = TestType.Method, Order = 3)]
        public virtual void TestStep3()
        {
            base.CurrentConfig.DisplayList.Intersect(base._defaultEDIDMap.Keys).ToList().ForEach(curDisp =>
            {
                base.HotPlug(curDisp, base._defaultEDIDMap[curDisp]);
            });
        }
        [Test(Type = TestType.Method, Order = 4)]
        public virtual void TestStep4()
        {
            base.VerifyConfigOS(base.CurrentConfig);
        }
        [Test(Type = TestType.Method, Order = 5)]
        public virtual void TestStep5()
        {
            Log.Message(true, "Test clean up- Unplug all displays");
            base.CurrentConfig.DisplayList.Intersect(base._defaultEDIDMap.Keys).ToList().ForEach(curDisp =>
            {
                base.HotUnPlug(curDisp);
            });
        }
    }
}
