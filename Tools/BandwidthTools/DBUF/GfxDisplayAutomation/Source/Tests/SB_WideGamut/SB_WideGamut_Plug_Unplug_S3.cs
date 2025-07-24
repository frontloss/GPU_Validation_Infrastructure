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
    class SB_WideGamut_Plug_Unplug_S3 : SB_WideGamut_MonitorTurnOff
    {
        protected PowerStates _powerState;
        public SB_WideGamut_Plug_Unplug_S3()
        {
            base._wideGamutLevel = WideGamutLevel.LEVEL2;
            _powerState = PowerStates.S3;
        }
        [Test(Type = TestType.Method, Order = 4)]
        public override void TestStep4()
        {
            _pluggableDisplaySim.ForEach(curDisp =>
            {
                DisplayInfo displayInfo = base.EnumeratedDisplays.Where(item => item.DisplayType == curDisp).FirstOrDefault();
                base.HotUnPlug(curDisp, true);
                InvokePowerEvent(_powerState);               
                base.HotPlug(curDisp, base._defaultEDIDMap[curDisp]);
                
                DisplayConfig currentConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);
                if (currentConfig.GetCurrentConfigStr().Equals(base.CurrentConfig.GetCurrentConfigStr()))
                    Log.Success("{0} retained", base.CurrentConfig.GetCurrentConfigStr());
                else
                    Log.Fail("Expected:{0} , current: {1}", base.CurrentConfig.GetCurrentConfigStr(), currentConfig.GetCurrentConfigStr());

                if (!VerifyConfig(base.CurrentConfig))
                    ApplyConfigOS(base.CurrentConfig);

                base.CurrentConfig.DisplayList.ForEach(curdisp =>
                {
                    VerifyWideGamutValue(curdisp, base._wideGamutLevel);
                });
            });            
        }
        [Test(Type = TestType.Method, Order = 5)]
        public override void TestStep5()
        {
            Log.Message(true, "Test clean up- Unplug all displays");
            base.UnPlugDisplays();
        }
    }
}
