using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Threading;

namespace Intel.VPG.Display.Automation
{
    [Test(Type = TestType.HasReboot)]
    [Test(Type = TestType.HasPlugUnPlug)]
    [Test(Type = TestType.HasINFModify)]
    class SB_WideGamut_Plug_Unplug_S5 : SB_WideGamut_MonitorTurnOff
    {
        public SB_WideGamut_Plug_Unplug_S5()
        {
            base._wideGamutLevel = WideGamutLevel.LEVEL2;
        }
        [Test(Type = TestType.Method, Order = 4)]
        public override void TestStep4()
        {
            _pluggableDisplaySim.ForEach(curDisp =>
            {
                base.HotUnPlug(curDisp, true);
            });
            InvokePowerEvent(PowerStates.S5);             
        }
        [Test(Type = TestType.Method, Order = 5)]
        public override void TestStep5()
        {
            base.InitializeHotplugFramework();          
            base.PlugDisplays();
            base.ApplyConfigOS(base.CurrentConfig);
            base.CurrentConfig.DisplayList.ForEach(curDisp =>
            {
                VerifyWideGamutValue(curDisp, base._wideGamutLevel);
            });
        }
        [Test(Type = TestType.Method, Order = 6)]
        public override void TestStep6()
        {
            Log.Message(true, "Test clean up- Unplug all displays");
            base.UnPlugDisplays();

            base.WideGamutDriver(0);
        }       
    }
}
