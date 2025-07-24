namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;
    using System.Linq;
    using System.Threading;

    [Test(Type = TestType.HasPlugUnPlug)]
    [Test(Type = TestType.ConnectedStandby)]
    class MP_DuringS0ix_Display_Hotplug : MP_S0ixBase
    {
        [Test(Type = TestType.Method, Order = 1)]
        public void TestPreCondition()
        {
            if (base.EnumeratedDisplays.Count > 1)
            {
                Log.Alert("System should boot with only internal display connected");
            }
        }

        [Test(Type = TestType.Method, Order = 2)]
        public void HotPluginLPState()
        {
            foreach (DisplayType DT in base.CurrentConfig.PluggableDisplayList)
            {
                Log.Message(true, "Goto S0i3 state and hotplug external display {0}", DT);
                base.HotPlug(DT, true);
                this.CSCall();
                DisplayInfo plugginDisplay = base.EnumeratedDisplays.Find(DTP => DTP.DisplayType == DT);
                if (plugginDisplay.DisplayType == DT)
                {
                    Log.Success("Successfully Hotplug Display {0} in low power state", DT);
                }
                else
                {
                    Log.Fail("Unable to Hotplug Display {0} in low power state", DT);
                }
            }
        }

    }
}
