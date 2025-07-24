using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Intel.VPG.Display.Automation
{
    [Test(Type = TestType.HasPlugUnPlug)]
    class SB_MBO_AC_DC : SB_MBO_Base
    {
        [Test(Type = TestType.PreCondition, Order = 0)]
        public void TestStep0()
        {
            if (!base.CurrentConfig.CustomDisplayList.Contains(DisplayType.EDP))
                Log.Abort("Test has to be run with eDP");
        }
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            base.MBO_RegEdit(1);
            base.SwitchToACMode();
            base.ApplySDEDP();
            base.PlayVideo();
            base.VerifyMBODisable();
        }
        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            base.SwitchToDCMode();
            base.VerifyMBOEnable();
        }
        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3()
        {
            base.SwitchToACMode();
            base.VerifyMBODisable();
            base.StopVideo();
            base.CleanUpHotplugFramework();
        }
    }
}

