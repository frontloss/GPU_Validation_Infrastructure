using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    [Test(Type = TestType.HasReboot)]
    [Test(Type = TestType.HasINFModify)]
    class SB_WideGamut_Slider_Persistence_Before_After_Display_Switch :SB_WideGamut_Base
    { //edp hdmi dp
        DisplayConfig currentConfig = new DisplayConfig();
         [Test(Type = TestType.PreCondition, Order = 0)]
        public virtual void TestStep0()
        {
            base.WideGamutDriver(7);           
        }
         [Test(Type = TestType.Method, Order = 1)]
         public void TestStep1()
         {
             PerformWideGamutOnSingleDisplay(base.CurrentConfig.PrimaryDisplay, WideGamutLevel.LEVEL4);
             if (base.CurrentConfig.SecondaryDisplay != DisplayType.None)
                 PerformWideGamutOnSingleDisplay(base.CurrentConfig.SecondaryDisplay, WideGamutLevel.LEVEL3);
             if (base.CurrentConfig.TertiaryDisplay != DisplayType.None)
                 PerformWideGamutOnSingleDisplay(base.CurrentConfig.TertiaryDisplay, WideGamutLevel.LEVEL2);
         }
         [Test(Type = TestType.Method, Order = 2)]
         public void TestStep2()
         {
             if (base.CurrentConfig.SecondaryDisplay != DisplayType.None)
             {
                 PerformWideGamuOnDualConfig(DisplayConfigType.DDC, base.CurrentConfig.PrimaryDisplay, base.CurrentConfig.SecondaryDisplay, WideGamutLevel.LEVEL3, WideGamutLevel.LEVEL2);
                 if(base.CurrentConfig.TertiaryDisplay!=DisplayType.None)
                 {
                     PerformWideGamuOnDualConfig(DisplayConfigType.DDC, base.CurrentConfig.PrimaryDisplay, base.CurrentConfig.TertiaryDisplay, WideGamutLevel.LEVEL2, WideGamutLevel.VIVID);
                     PerformWideGamuOnDualConfig(DisplayConfigType.DDC, base.CurrentConfig.TertiaryDisplay, base.CurrentConfig.SecondaryDisplay, WideGamutLevel.VIVID, WideGamutLevel.LEVEL2,false);
                 }
             }
         }
         [Test(Type = TestType.Method, Order = 3)]
         public void TestStep3()
         {
             PerformWideGamutOnSingleDisplay(base.CurrentConfig.PrimaryDisplay, WideGamutLevel.LEVEL4);
         }
         [Test(Type = TestType.Method, Order = 4)]
         public void TestStep4()
         {
             if (base.CurrentConfig.SecondaryDisplay != DisplayType.None)
             {
                 PerformWideGamuOnDualConfig(DisplayConfigType.ED, base.CurrentConfig.PrimaryDisplay, base.CurrentConfig.SecondaryDisplay, WideGamutLevel.LEVEL3, WideGamutLevel.LEVEL2);
                 if (base.CurrentConfig.TertiaryDisplay != DisplayType.None)
                 {
                     PerformWideGamuOnDualConfig(DisplayConfigType.ED, base.CurrentConfig.PrimaryDisplay, base.CurrentConfig.TertiaryDisplay, WideGamutLevel.LEVEL2, WideGamutLevel.VIVID);
                     PerformWideGamuOnDualConfig(DisplayConfigType.ED, base.CurrentConfig.TertiaryDisplay, base.CurrentConfig.SecondaryDisplay, WideGamutLevel.VIVID, WideGamutLevel.LEVEL2, false);
                 }
             }
         }
         [Test(Type = TestType.Method, Order = 5)]
         public void TestStep5()
         {
             if (base.CurrentConfig.TertiaryDisplay != DisplayType.None)
             {
                 PerformWideGamutOnTriConfig(base.CurrentConfig.PrimaryDisplay, base.CurrentConfig.SecondaryDisplay, base.CurrentConfig.TertiaryDisplay, WideGamutLevel.LEVEL3, WideGamutLevel.LEVEL2, WideGamutLevel.LEVEL2);
                 currentConfig = new DisplayConfig() {ConfigType=DisplayConfigType.TED , PrimaryDisplay=base.CurrentConfig.PrimaryDisplay,SecondaryDisplay=base.CurrentConfig.SecondaryDisplay , TertiaryDisplay=base.CurrentConfig.TertiaryDisplay};
                 base.ApplyConfigOS(currentConfig);
                 PerformWideGamutOnTriConfig(base.CurrentConfig.PrimaryDisplay, base.CurrentConfig.SecondaryDisplay, base.CurrentConfig.TertiaryDisplay, WideGamutLevel.LEVEL3, WideGamutLevel.LEVEL2, WideGamutLevel.LEVEL2,false);
             }
         }
         private void PerformWideGamutOnSingleDisplay(DisplayType argDisplayType, WideGamutLevel argWidegamutLevel)
         {
             currentConfig = new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = argDisplayType };
             base.ApplyConfigOS(currentConfig);
             this.VerifyWideGamut(argDisplayType, argWidegamutLevel);
         }
         private void PerformWideGamuOnDualConfig(DisplayConfigType argDispConfigType, DisplayType argPriDisp, DisplayType argSecDisp, WideGamutLevel argDisp1WGLevel, WideGamutLevel argDisp2WGLevel, bool argApplyWideGamut = true)
         {
             currentConfig = new DisplayConfig() { ConfigType = argDispConfigType, PrimaryDisplay = argPriDisp, SecondaryDisplay = argSecDisp };
             base.ApplyConfigOS(currentConfig);
             VerifyWideGamut(argPriDisp, argDisp1WGLevel);
             VerifyWideGamut(argSecDisp, argDisp2WGLevel);

         }
         private void PerformWideGamutOnTriConfig(DisplayType argPriDisp, DisplayType argSecDisp, DisplayType argTriDisp, WideGamutLevel argLevel1, WideGamutLevel argLevel2, WideGamutLevel argLevel3, bool argApplyWideGamut = true)
         {
             currentConfig = new DisplayConfig() {ConfigType=DisplayConfigType.TDC , PrimaryDisplay=argPriDisp , SecondaryDisplay=argSecDisp , TertiaryDisplay=argTriDisp  };
             base.ApplyConfigOS(currentConfig);
             VerifyWideGamut(argPriDisp, argLevel1);
             VerifyWideGamut(argSecDisp, argLevel2);
             VerifyWideGamut(argTriDisp, argLevel3);
         }
         private void VerifyWideGamut(DisplayType argDispType, WideGamutLevel argWIdeGamutLevel, bool argApplyWideGamut=true)
         {
             if(argApplyWideGamut)
             base.ApplyWideGamutToDisplay(argDispType, argWIdeGamutLevel);
             base.VerifyWideGamutValue(argDispType, argWIdeGamutLevel);
         }
    }
}
