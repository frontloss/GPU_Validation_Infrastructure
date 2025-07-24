using System.Collections.Generic;
using System.Threading;
using System.Windows.Forms;
namespace Intel.VPG.Display.Automation
{
    class SB_Dbuf_MPO : SB_Dbuf_Base
    {

        List<PipeDbufInfo> dbufList = new List<PipeDbufInfo>();
        [Test(Type = TestType.PreCondition, Order = 0)]
        public virtual void TestStep0()
        {
            base.ApplyConfig(base.CurrentConfig);
            dbufList = base.CheckDbuf(base.CurrentConfig);
        }
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            base.LaunchMPO();
        }
        [Test(Type = TestType.Method, Order = 2)]
        public virtual void TestStep2()
        {           
            dbufList = RedistributePlane(base.CurrentConfig, dbufList);
            base.checkDbufRedistribution(dbufList);
            Thread.Sleep(5000);
            SendKeys.SendWait("^{Esc}"); //ctrl + esc
        }
    }
}
