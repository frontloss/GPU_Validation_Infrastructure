namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    class SB_Dbuf_Config_Basic : SB_Dbuf_Base
    {
        [Test(Type = TestType.PreCondition, Order = 0)]
        public virtual void TestStep0()
        {
            base.ApplyConfig(base.CurrentConfig);
        }
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            List<PipeDbufInfo> dbufList = base.CheckDbuf(base.CurrentConfig);
            base.checkDbufRedistribution(dbufList);                
        }       
    }
}
