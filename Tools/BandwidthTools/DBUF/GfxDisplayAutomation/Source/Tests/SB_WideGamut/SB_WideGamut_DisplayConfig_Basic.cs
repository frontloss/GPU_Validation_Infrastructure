using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Threading;

namespace Intel.VPG.Display.Automation
{
    [Test(Type = TestType.HasReboot)]
    [Test(Type = TestType.HasINFModify)]
    [Test(Type = TestType.HasPlugUnPlug)]
    class SB_WideGamut_DisplayConfig_Basic:SB_WideGamut_Base
    {
        [Test(Type = TestType.PreCondition, Order = 0)]
        public virtual void TestStep0()
        {
                     
        }
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            base.WideGamutDriver(7);               
        }
        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            base.PlugDisplays();
        }
        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3()
        {
            //update script as per QC
            base.ApplyConfigOS(base.CurrentConfig);
            Dictionary<WideGamutLevel, string> _customwbLevelEventMap = WBSliderValues();
            base.CurrentConfig.DisplayList.ForEach(curDisp =>
            {
                _customwbLevelEventMap.Keys.ToList().ForEach(curWbLevel =>
                {
                    base.ApplyWideGamutToDisplay(curDisp, curWbLevel);
                    base.VerifyWideGamutValue(curDisp, curWbLevel);
                });
             });
        }
        [Test(Type = TestType.Method, Order = 4)]
        public virtual void TestStep4()
        {
            Log.Message(true, "Test clean up- Unplug all displays");
            base.UnPlugDisplays();
            base.WideGamutDriver(0);
        }
        [Test(Type = TestType.Method, Order = 5)]
        public virtual void TestStep5()
        {
            Log.Message(true, "Test Execution Completed");
        }
    }
}
