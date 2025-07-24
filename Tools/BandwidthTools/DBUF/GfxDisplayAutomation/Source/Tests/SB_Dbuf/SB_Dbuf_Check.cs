using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    class SB_Dbuf_Check: SB_Dbuf_Base
    {
             
            [Test(Type = TestType.Method, Order = 1)]
            public void TestStep1()
            {
                List<PipeDbufInfo> dbufList = base.CheckDbuf(base.CurrentConfig);
                base.checkDbufRedistribution(dbufList);
            }
        
    }
}
