namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.Threading.Tasks;

    [Test(Type = TestType.HasPlugUnPlug)]
    [Test(Type = TestType.ConnectedStandby)]
    class MP_AfterS0ix_Display_HotplugUnplug : MP_S0ixBase
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
        public void SendSystemToS0ix()
        {
            Log.Message(true, "Go to S0i3 & wait for 30 sec and resume");
            base.CSCall();
        }

        [Test(Type = TestType.Method, Order = 3)]
        public void HotplugUnplugExternalDisplay()
        {
            foreach (DisplayType DT in base.CurrentConfig.PluggableDisplayList.Reverse<DisplayType>())
            {
                Log.Message(true, "Hotplug and unplug external display {0}", DT);
                if (base.HotPlug(DT))
                {
                    Log.Success("Successfully hotplug display {0}", DT);
                }
                else
                {
                    Log.Fail("Failed to hotplug display {0}", DT);
                }
                if (base.HotUnPlug(DT))
                {
                    Log.Success("Successfully hotunplug display {0}", DT);
                }
                else
                {
                    Log.Fail("Unable to hotunplug display {0}", DT);
                }
            }
        }

    }
}
