using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Threading;
namespace Intel.VPG.Display.Automation
{
    class SB_WideGamut_Via_SDK_App_Persistance_with_Power_Events:SB_WideGamut_Base
    {
        [Test(Type = TestType.PreCondition, Order = 0)]
        public virtual void TestStep0()
        {
            Log.Message(true, "Disabling Driver Signature Enforcement");
            SetBCDEditOptions("-set loadoptions DDISABLE_INTEGRITY_CHECKS", "-set TESTSIGNING ON");
        }
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            Log.Message("Verify Disabling Driver Signature Enforcement");
            CheckBCDEditOptions("loadoptions DDISABLE_INTEGRITY_CHECKS", "testSigning Yes");
        }
        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            base.WideGamutDriver(7);
        }
        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3()
        {
            //update script as per QC
            base.ApplyConfigOS(base.CurrentConfig);
            base.CurrentConfig.DisplayList.ForEach(curDisp =>
            {
                base.ApplyWideGamutToDisplay(curDisp, base._wideGamutLevel);
                base.VerifyWideGamutValue(curDisp, base._wideGamutLevel);
            });
        }
        [Test(Type = TestType.Method, Order = 4)]
        public void TestStep4()
        {
            base.InvokePowerEvent(PowerStates.S3);
        }
        [Test(Type = TestType.Method, Order = 5)]
        public void TestStep5()
        {
            VerifyConfig();
            base.CurrentConfig.DisplayList.ForEach(curDisp =>
            {
                VerifyWideGamutValue(curDisp, base._wideGamutLevel);
            });
            base.InvokePowerEvent(PowerStates.S4);
        }
        [Test(Type = TestType.Method, Order = 6)]
        public void TestStep6()
        {
            VerifyConfig();
            base.CurrentConfig.DisplayList.ForEach(curDisp =>
            {
                VerifyWideGamutValue(curDisp, base._wideGamutLevel);
            });
            base.InvokePowerEvent(PowerStates.S5);
        }
        [Test(Type = TestType.Method, Order = 7)]
        public void TestStep7()
        {
            VerifyConfig();
            base.CurrentConfig.DisplayList.ForEach(curDisp =>
            {
                VerifyWideGamutValue(curDisp, base._wideGamutLevel);
            });
            base.WideGamutDriver(0);
        }
        private void VerifyConfig()
        {
            DisplayConfig currentConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);
            if (currentConfig.GetCurrentConfigStr().Equals(base.CurrentConfig.GetCurrentConfigStr()))
                Log.Success("{0} retained", base.CurrentConfig.GetCurrentConfigStr());
            else
                Log.Fail("Expcted:{0} , current: {1}", base.CurrentConfig.GetCurrentConfigStr(), currentConfig.GetCurrentConfigStr());
        }
    }
}
