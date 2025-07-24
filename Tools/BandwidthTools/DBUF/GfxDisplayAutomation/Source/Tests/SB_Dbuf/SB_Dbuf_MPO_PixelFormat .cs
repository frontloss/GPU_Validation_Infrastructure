using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Threading;
namespace Intel.VPG.Display.Automation
{
    class SB_Dbuf_MPO_PixelFormat : SB_Dbuf_MPO
    {
        [Test(Type = TestType.Method, Order = 1)]
        public  void TestStep1()
        {
            base.TestStep1();
            for (int i = 0; i < 2; i++)
            {
                Log.Message("Key press event(f) to change the mode");
                Thread.Sleep(1000);
                SendKeys.SendWait("F"); //ctrl + esc
            }
        }
    }
}
