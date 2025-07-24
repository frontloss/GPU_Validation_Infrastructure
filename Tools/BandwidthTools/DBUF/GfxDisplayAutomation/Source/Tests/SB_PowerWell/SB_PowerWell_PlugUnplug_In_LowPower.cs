namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;

    class SB_PowerWell_PlugUnplug_In_LowPower : SB_PowerWell_DisplayConfig
    {
        int displaysCountBeforeUnplug = 0;
        int pluggableDisplays = 0;

        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3()
        {
            displaysCountBeforeUnplug = base.EnumeratedDisplays.Count;
            pluggableDisplays = base.CurrentConfig.PluggedDisplayList.Count;

            if (base.CurrentConfig.PluggedDisplayList.Count == 0)
            {
                Log.Abort("Pluggable displays are zero. So, Aborting.");
            }

            base.CurrentConfig.PluggedDisplayList.ForEach(curDisp =>
            {
                base.HotUnPlug(curDisp, true);
            });

            PowerEvent(PowerStates.S3);

            if((displaysCountBeforeUnplug - pluggableDisplays) == base.CurrentConfig.EnumeratedDisplays.Count)
            {
                Log.Success("Displays unplugged as expected.");
            }
            else
            {
                Log.Fail("Displays are not unplugged as expected.");
            }
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
                base.HotPlug(curDisp, true);
            });

            PowerEvent(PowerStates.S4);

            if (displaysCountBeforeUnplug == base.CurrentConfig.EnumeratedDisplays.Count)
            {
                Log.Success("Displays Plugged as expected.");
            }
            else
            {
                Log.Fail("Displays are not Plugged as expected.");
            }
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