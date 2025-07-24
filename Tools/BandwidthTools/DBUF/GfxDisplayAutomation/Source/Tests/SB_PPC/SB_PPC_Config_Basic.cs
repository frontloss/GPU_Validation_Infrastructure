namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    class SB_PPC_Config_Basic : SB_PPC_Base
    {
        [Test(Type = TestType.PreCondition, Order = 0)]
        public void TestStep0()
        {
            Log.Message(true, "Checking Preconditions for test");
            if (base.CurrentConfig.ConfigTypeCount != base.CurrentConfig.DisplayList.Count())
                Log.Abort("This test requires atleast {0} displays , current display count: {1}", base.CurrentConfig.ConfigTypeCount, base.CurrentConfig.DisplayList.Count());
        }

        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            base.ApplyConfig(base.CurrentConfig);
            base.VerifyPPC();
        }
    }
}
