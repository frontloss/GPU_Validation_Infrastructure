using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    [Test(Type = TestType.HasPlugUnPlug)]
    class SB_MBO_Hotplug_Unplug : SB_MBO_Base
    {
        [Test(Type = TestType.PreCondition, Order = 0)]
        public void TestStep0()
        {
            if (!base.CurrentConfig.CustomDisplayList.Contains(DisplayType.EDP))
                Log.Abort("Test has to be run with eDP");
            if (base.CurrentConfig.ConfigTypeCount < 2)
                Log.Abort("Need atleast 2 displays to be planned");
        }
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            base.MBO_RegEdit(1);
            base.ApplySDEDP();
            base.SwitchToDCMode();
            base.PlayVideo();
            base.VerifyMBOEnable();           
        }
        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            base.PlugDisplays();
            base.ApplyConfigOS(base.CurrentConfig);
            base.VerifyMBODisable();
        }
        [Test(Type = TestType.Method, Order = 3)]
        public virtual void TestStep3()
        {
            base.UnPlugDisplays();
            base.VerifyMBOEnable();
            base.StopVideo();
        }
    }
}
