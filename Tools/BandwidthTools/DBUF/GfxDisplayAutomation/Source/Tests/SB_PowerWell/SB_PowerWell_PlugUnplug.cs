namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;

    [Test(Type = TestType.HasPlugUnPlug)]
    class SB_PowerWell_PlugUnplug : SB_PowerWell_DisplayConfig
    {
        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3()
        {
            if(base.CurrentConfig.PluggedDisplayList.Count == 0)
            {
                Log.Abort("Pluggable displays are zero. So, Aborting.");
            }

            base.CurrentConfig.PluggedDisplayList.ForEach(curDisp =>
            {
                base.HotUnPlug(curDisp);
            });
        }

        [Test(Type = TestType.Method, Order = 4)]
        public void TestStep4()
        {
            VerifyPowerWell();
        }

        [Test(Type = TestType.Method, Order = 5)]
        public void TestStep5()
        {
            if (base.CurrentConfig.PluggableDisplayList.Count == 0)
            {
                Log.Abort("Pluggable displays are zero. So, Aborting.");
            }

            base.CurrentConfig.PluggableDisplayList.ForEach(curDisp =>
            {
                base.HotPlug(curDisp);
            });
        }

        [Test(Type = TestType.Method, Order = 6)]
        public void TestStep6()
        {
            if (!VerifyConfig(base.CurrentConfig, false))
            {
                ApplyConfig(base.CurrentConfig);
            }

            VerifyPowerWell();
        }
    }
}