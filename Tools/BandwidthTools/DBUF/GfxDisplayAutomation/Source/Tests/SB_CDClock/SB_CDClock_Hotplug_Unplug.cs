namespace Intel.VPG.Display.Automation
{
    using System.Linq;

    [Test(Type = TestType.HasPlugUnPlug)]
    class SB_CDClock_Hotplug_Unplug : SB_CDClock_Base
    {
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            base.CurrentConfig.PluggableDisplayList.ForEach(curDisp =>
            {
                    base.HotPlug(curDisp);
            });
            base.ApplyConfig(base.CurrentConfig);

            VerifyCDClockRegisters();
        }
        [Test(Type = TestType.Method, Order = 2)]
        public virtual void TestStep2()
        {
            base.CurrentConfig.PluggableDisplayList.ForEach(curDisp =>
            {
                base.HotUnPlug(curDisp);
            });

            VerifyCDClockRegisters();
        }
    }
}
