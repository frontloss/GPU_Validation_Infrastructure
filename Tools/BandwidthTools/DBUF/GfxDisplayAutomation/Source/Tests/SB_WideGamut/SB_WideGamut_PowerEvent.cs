using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    [Test(Type = TestType.HasReboot)]
    [Test(Type = TestType.HasINFModify)]
    class SB_WideGamut_PowerEvent : SB_WideGamut_Base
    {
        WideGamutLevel _wgLevel = WideGamutLevel.LEVEL3;
        [Test(Type = TestType.PreCondition, Order = 0)]
        public virtual void TestStep0()
        {
            //if ((base.CurrentConfig.ConfigType != DisplayConfigType.DDC || base.CurrentConfig.ConfigType != DisplayConfigType.TED))
            //    Log.Abort("Test needs DDC/TED");

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
            base.ApplyConfigOS(base.CurrentConfig);
            base.CurrentConfig.DisplayList.ForEach(curDisp =>
                {
                    base.ApplyWideGamutToDisplay(curDisp, _wgLevel);
                    base.VerifyWideGamutValue(curDisp, _wgLevel);
                });
            base.InvokePowerEvent(PowerStates.S3);
        }
        [Test(Type = TestType.Method, Order = 4)]
        public void TestStep4()
        {
            VerifyPersistanceAfterPowerEvent(PowerStates.S3, _wgLevel);
            base.InvokePowerEvent(PowerStates.S4);
        }
        [Test(Type = TestType.Method, Order = 5)]
        public void TestStep5()
        {
            VerifyPersistanceAfterPowerEvent(PowerStates.S4, _wgLevel);
            base.InvokePowerEvent(PowerStates.S5);
        }
        [Test(Type = TestType.Method, Order = 6)]
        public void TestStep6()
        {
            VerifyPersistanceAfterPowerEvent(PowerStates.S5, _wgLevel);
            base.WideGamutDriver(0);
        }
        private void VerifyPersistanceAfterPowerEvent(PowerStates argPowerState, WideGamutLevel argWGLevel)
        {
            DisplayConfig currentConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);
            if (currentConfig.GetCurrentConfigStr().Equals(base.CurrentConfig.GetCurrentConfigStr()))
            {
                Log.Success("Config {0} retained after {1}", base.CurrentConfig.GetCurrentConfigStr(), argPowerState);
                base.CurrentConfig.DisplayList.ForEach(curDisp =>
                {
                    base.VerifyWideGamutValue(curDisp, argWGLevel);
                });
            }
            else
                Log.Fail("Expected Config after {0} {1} , current config {2}",argPowerState, base.CurrentConfig.GetCurrentConfigStr(), currentConfig.GetCurrentConfigStr());
        }
    }
}
