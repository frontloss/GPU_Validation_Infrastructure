namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.Threading.Tasks;

    [Test(Type = TestType.HasPlugUnPlug)]
    class MP_Stress_HotplugUnplug : MP_Stress_Base
    {
        [Test(Type = TestType.Method, Order = 1)]
        public void StressTestingOfHPD()
        {
            if (base.CurrentConfig.PluggableDisplayList.Count == 0)
            {
                Log.Abort("No Pluggable display found to run the test");
            }

            Log.Message("Running {0} test for {1} cycle.", base.TestName, base.StressCycle);
            for (int count = 1; count <= base.StressCycle; count++)
            {
                Log.Message(true, "Executing Test Cycle {0} of {1}.", count, base.TestName);
                HotplugUnplugExternalDisplay();
            }
        }

        private void HotplugUnplugExternalDisplay()
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
