using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Intel.VPG.Display.Automation
{
    [Test(Type = TestType.HasReboot)]
    [Test(Type = TestType.HasINFModify)]
    [Test(Type = TestType.HasPlugUnPlug)]
    class SB_WideGamut_Enable_Disable_INF : SB_WideGamut_DisplayConfig_Basic
    {
        public SB_WideGamut_Enable_Disable_INF()
        {
            base._wideGamutLevel = WideGamutLevel.LEVEL3;
        }
        [Test(Type = TestType.Method, Order = 4)]
        public override void TestStep4()
        {
            SendKeys.SendWait("{ESC}");
            
            base.CurrentConfig.DisplayList.ForEach(curDisp =>
            {
                DisplayConfig curConfig = new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = curDisp };
                ApplyConfigOS(curConfig);
                
                base.ApplyWideGamutToDisplay(curDisp, base._wideGamutLevel);
                base.VerifyWideGamutValue(curDisp, _wideGamutLevel);
            });            
        }
        [Test(Type = TestType.Method, Order = 5)]
        public override void TestStep5()
        {
            Log.Message(true, "Test clean up- Unplug all displays");

            _pluggableDisplaySim.ForEach(curDisp =>
            {
                base.HotUnPlug(curDisp);
            });
            _pluggableDisplaySim.Clear();
            base.WideGamutDriver(0);
        }
        [Test(Type = TestType.Method, Order = 6)]
        public void TestStep6()
        {
            base.WideGamutDriver(7);
            base.PlugDisplays();
            base.ApplyConfigOS(base.CurrentConfig);
        }
        [Test(Type = TestType.Method, Order = 7)]
        public void TestStep7()
        {
            //update script as per QC
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
        [Test(Type = TestType.Method, Order = 8)]
        public void TestStep8()
        {
            Log.Message(true, "Test clean up- Unplug all displays");
            base.UnPlugDisplays();
            base.WideGamutDriver(0);
        }
        [Test(Type = TestType.Method, Order = 9)]
        public void TestStep9()
        {
            Log.Message(true, "Test Execution Completed");
        }
    }
}
