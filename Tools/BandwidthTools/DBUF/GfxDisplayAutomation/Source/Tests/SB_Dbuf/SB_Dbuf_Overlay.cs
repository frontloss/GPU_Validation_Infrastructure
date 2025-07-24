using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    class SB_Dbuf_Overlay : SB_Dbuf_Config_Basic
    {
        [Test(Type = TestType.Method, Order = 2)]
        public  void TestStep2()
        {
            base.LaunchOverlay(base.CurrentConfig.PrimaryDisplay);
            List<PipeDbufInfo> dbufList = base.CheckDbuf(base.CurrentConfig);
            base.checkDbufRedistribution(dbufList); 
            
        }
        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3()
        {
            base.CloseOverlay(base.CurrentConfig.PrimaryDisplay);
        }
    }
}
