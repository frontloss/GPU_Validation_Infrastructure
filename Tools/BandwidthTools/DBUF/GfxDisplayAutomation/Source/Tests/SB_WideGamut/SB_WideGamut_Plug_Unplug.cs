using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
     [Test(Type = TestType.HasReboot)]
    [Test(Type = TestType.HasPlugUnPlug)]
    [Test(Type = TestType.HasINFModify)]
    class SB_WideGamut_Plug_Unplug : SB_WideGamut_MonitorTurnOff
    {
        public SB_WideGamut_Plug_Unplug()
        {
            base._wideGamutLevel = WideGamutLevel.LEVEL3;
        }
        [Test(Type = TestType.Method, Order = 3)]
        public override void TestStep3()
        {
            base.InitializeHotplugFramework();
            base.CurrentConfig.PluggableDisplayList.ForEach(curDisp=>
            {
                base.HotPlug(curDisp);
            });
            base.TestStep3();
        }
        [Test(Type = TestType.Method, Order = 4)]
        public override void TestStep4()
        {
            base.CurrentConfig.PluggableDisplayList.ForEach(curDisp =>
            {
                base.HotUnPlug(curDisp);
            });
            base.CurrentConfig.PluggableDisplayList.ForEach(curDisp =>
            {
                base.HotPlug(curDisp);
            });
        }
    }
}
