using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    class SB_Dbuf_PopUp : SB_Dbuf_Config_Basic
    {
       
        [Test(Type = TestType.Method, Order = 2)]
        public  void TestStep2()
        {
            base.SemiAutomated("Launch Overlay/NV12");
            base.CheckDbuf(base.CurrentConfig);
        }
    }
}
