namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.Threading.Tasks;

    class SB_PND_Max_Fifo_Basic : SB_PND_Base
    {
        private const string PND_Max_FIFO_ENABLE = "PND_Max_FIFO_ENABLE";

        [Test(Type = TestType.PreCondition, Order = 0)]
        public virtual void TestStep0()
        {
            if (base.CurrentConfig.ConfigTypeCount > base.CurrentConfig.DisplayList.Count())
                Log.Abort("{0} requires atleast {1} Displays to be enumerated, current Display count: {2}", base.CurrentConfig.ConfigType, base.CurrentConfig.ConfigTypeCount, base.CurrentConfig.DisplayList.Count());
        }

        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            ApplyConfigOS(base.CurrentConfig);
            VerifyConfigOS(base.CurrentConfig);

            TestMaxFifo(base.CurrentConfig);
        }

       
    }
}
