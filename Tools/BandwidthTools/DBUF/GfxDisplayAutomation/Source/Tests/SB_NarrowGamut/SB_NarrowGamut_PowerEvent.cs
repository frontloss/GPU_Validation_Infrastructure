using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Microsoft.Win32;
namespace Intel.VPG.Display.Automation
{
     [Test(Type = TestType.HasINFModify)]
     [Test(Type = TestType.HasReboot)]
    class SB_NarrowGamut_PowerEvent:SB_NarrowGamut_Base
    {
        [Test(Type = TestType.PreCondition, Order = 0)]
        public virtual void TestStep0()
        {
            ////Log.Message(true, "Disabling Driver Signature Enforcement");
            ////SetBCDEditOptions("-set loadoptions DDISABLE_INTEGRITY_CHECKS", "-set TESTSIGNING ON");
        }
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            //Log.Message("Verify Disabling Driver Signature Enforcement");
            //CheckBCDEditOptions("loadoptions DDISABLE_INTEGRITY_CHECKS", "testSigning Yes");
        }

        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            base.NarrowGamutDriver(NarrowGamutOption.EnableINF);
        }
          [Test(Type = TestType.Method, Order = 3)]
          public void TestStep3()
          {
              base.VerifyInfChanges(NarrowGamutOption.VerifyINF);
              base.ApplyConfig(base.CurrentConfig);
              base.NarrowGamutSupportedDisplays.Intersect(base.CurrentConfig.DisplayList).ToList().ForEach(curDisp =>
              {
                  base.SetNarrowGamutStatus(curDisp, NarrowGamutOption.EnableNarrowGamut);
              });
              base.CheckNarrowGamutRegister(DisplayType.EDP, NarrowGamutOption.EnableNarrowGamut);
          }
         [Test(Type = TestType.Method, Order = 4)]
          public void TestStep4()
          {
              base.PowerEvent(PowerStates.S3);             
          }
         [Test(Type = TestType.Method, Order = 5)]
         public void TestStep5()
         {
             base.NarrowGamutSupportedDisplays.Intersect(base.CurrentConfig.DisplayList).ToList().ForEach(curDisp =>
             {
                 base.CheckNarrowGamutRegister(curDisp, NarrowGamutOption.EnableNarrowGamut);
             });
             base.PowerEvent(PowerStates.S4);
            
         }
         [Test(Type = TestType.Method, Order = 6)]
         public void TestStep6()
         {
             base.NarrowGamutSupportedDisplays.Intersect(base.CurrentConfig.DisplayList).ToList().ForEach(curDisp =>
             {
                 base.CheckNarrowGamutRegister(curDisp, NarrowGamutOption.EnableNarrowGamut);
             });
             base.PowerEvent(PowerStates.S5);

         }
         [Test(Type = TestType.Method, Order = 7)]
         public void TestStep7()
         {
             if (base.MachineInfo.PlatformDetails.Platform != Platform.CHV)
             { // csc is always enabled in chv , hence disbale state is not being checked.
                 base.NarrowGamutSupportedDisplays.Intersect(base.CurrentConfig.DisplayList).ToList().ForEach(curDisp =>
                 {
                     base.CheckNarrowGamutRegister(curDisp, NarrowGamutOption.EnableNarrowGamut);
                 });
             }
         }       
         [Test(Type = TestType.Method, Order = 8)]
         public void TestStep8()
         {
            base.RevertNarrowGamutChanges();
         }
         [Test(Type = TestType.Method, Order = 9)]
         public void TestStep9()
         {
             //base.VerifyNarrowGamutChangesOnRevert();
         }
    } 
}
