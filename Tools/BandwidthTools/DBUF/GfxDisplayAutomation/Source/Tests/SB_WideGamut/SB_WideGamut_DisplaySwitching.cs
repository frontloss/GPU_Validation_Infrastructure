using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    [Test(Type = TestType.HasReboot)]
    [Test(Type = TestType.HasINFModify)]
    [Test(Type = TestType.HasPlugUnPlug)]
    class SB_WideGamut_DisplaySwitching : SB_WideGamut_Base
    {
        [Test(Type = TestType.PreCondition, Order = 0)]
        public virtual void TestStep0()
        {
            if (base.CurrentConfig.DisplayList.Count !=3)
                Log.Abort("Test needs 3 displays");
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
            PerformSDConfig();
        }     
        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3()
        {
            PerformDualConfig();           
        }
        [Test(Type = TestType.Method, Order = 4)]
        public void TestStep4()
        {
            PerformTriConfig();
        }
        [Test(Type = TestType.Method, Order = 5)]
        public void TestStep5()
        {
            Log.Message(true, "Test clean up- Unplug all displays");
            base.UnPlugDisplays();
        }
        [Test(Type = TestType.Method, Order = 6)]
        public void TestStep6()
        {
            base.WideGamutDriver(0);
        }
        [Test(Type = TestType.Method, Order = 7)]
        public void TestStep7()
        {
            Log.Message(true, "Test Execution completed");
        }
        private void PerformSDConfig()
        {
            base.CurrentConfig.DisplayList.ForEach(curDisp =>
                {
                    DisplayConfig curConfig = new DisplayConfig() { ConfigType=DisplayConfigType.SD , PrimaryDisplay=curDisp };
                    base.ApplyConfigOS(curConfig);
                    base.ApplyWideGamutToDisplay(curDisp, WideGamutLevel.NATURAL);
                    VerifyWideGamutValue(curDisp, WideGamutLevel.NATURAL);
                });
        }
        private void PerformDualConfig()
        {
            DisplayConfig ddc = new DisplayConfig() {ConfigType=DisplayConfigType.DDC, PrimaryDisplay=base.CurrentConfig.TertiaryDisplay , SecondaryDisplay=base.CurrentConfig.SecondaryDisplay };
            base.ApplyConfigOS(ddc);
            ddc.CustomDisplayList.ForEach(curDisp =>
                {
                    ApplyWideGamutToDisplay(curDisp, WideGamutLevel.LEVEL3);
                    VerifyWideGamutValue(curDisp, WideGamutLevel.LEVEL3);
                });

            DisplayConfig ed = new DisplayConfig() {ConfigType=DisplayConfigType.ED , PrimaryDisplay=base.CurrentConfig.SecondaryDisplay , SecondaryDisplay=base.CurrentConfig.PrimaryDisplay };
            base.ApplyConfigOS(ed);
            ed.CustomDisplayList.ForEach(curDisp =>
                {
                    ApplyWideGamutToDisplay(curDisp, WideGamutLevel.LEVEL2);
                    VerifyWideGamutValue(curDisp, WideGamutLevel.LEVEL2);
                });
        }
        private void PerformTriConfig()
        {
            DisplayConfig tdc = new DisplayConfig() {ConfigType=DisplayConfigType.TDC , PrimaryDisplay=base.CurrentConfig.TertiaryDisplay , SecondaryDisplay=base.CurrentConfig.PrimaryDisplay , TertiaryDisplay=base.CurrentConfig.SecondaryDisplay };
            base.ApplyConfigOS(tdc);
            tdc.CustomDisplayList.ForEach(curDisp =>
                {
                    ApplyWideGamutToDisplay(curDisp, WideGamutLevel.LEVEL4);
                    VerifyWideGamutValue(curDisp, WideGamutLevel.LEVEL4);
                });
            DisplayConfig ted = new DisplayConfig() {ConfigType=DisplayConfigType.TED,PrimaryDisplay=base.CurrentConfig.PrimaryDisplay , SecondaryDisplay=base.CurrentConfig.TertiaryDisplay , TertiaryDisplay=base.CurrentConfig.SecondaryDisplay };
            base.ApplyConfigOS(ted);
            ted.CustomDisplayList.ForEach(curDisp =>
                {
                    ApplyWideGamutToDisplay(curDisp, WideGamutLevel.NATURAL);
                    VerifyWideGamutValue(curDisp, WideGamutLevel.NATURAL);
                });
        }
    }
}
