using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    //This testcases verifies hotplug during S5 states 
    [Test(Type = TestType.HasPlugUnPlug)]
    class SB_DP_SST_Hotplug_Unplug_During_S5 : SB_DP_SST_Base
    {
        [Test(Type = TestType.Method, Order = 1)]
        public void testHotplugSecondary()
        {
            if (base.CurrentConfig.SecondaryDisplay != DisplayType.None)
            {
                DisplayType secondary = base.CurrentConfig.SecondaryDisplay;
                if (DisplayExtensions.GetDisplayType(secondary) == DisplayType.DP)
                {
                    Log.Message("Current config contains secondary display");
                    base.doHotplug(secondary, true, PowerStates.S5);
                }
                else
                {
                    Log.Message("Current config doesn't contain DP as secondary display");
                }
            }
            else
            {
                Log.Message("Current config doesn't contain secondary display");
            }
        }


        [Test(Type = TestType.Method, Order = 2)]
        public void testHotUnplugSecondary()
        {
            if (base.CurrentConfig.SecondaryDisplay != DisplayType.None)
            {
                DisplayType secondary = base.CurrentConfig.SecondaryDisplay;
                if (DisplayExtensions.GetDisplayType(secondary) == DisplayType.DP)
                {
                    Log.Message("Current config contains secondary display");
                    doHotUnPlug(secondary, true, PowerStates.S5);
                }
                else
                {
                    Log.Message("Current config doesn't contain DP as secondary display");
                }
            }
            else
            {
                Log.Message("Current config doesn't contain secondary display");
            }
        }


        [Test(Type = TestType.Method, Order = 3)]
        public void testHotplugTertiary()
        {
            if (base.CurrentConfig.TertiaryDisplay != DisplayType.None)
            {
                DisplayType tertiary = base.CurrentConfig.TertiaryDisplay;
                if (DisplayExtensions.GetDisplayType(tertiary) == DisplayType.DP)
                {
                    Log.Message("DP as Tertiary Display is present in config");
                    Log.Message("DP Hotplug unplug will be tested for tertiary display during S5");
                    doHotplug(tertiary, true, PowerStates.S5);
                }
            }
        }

        [Test(Type = TestType.Method, Order = 4)]
        public void testHotUnplugTertiary()
        {
            if (base.CurrentConfig.TertiaryDisplay != DisplayType.None)
            {
                DisplayType tertiary = base.CurrentConfig.TertiaryDisplay;
                if (DisplayExtensions.GetDisplayType(tertiary) == DisplayType.DP)
                {
                    Log.Message("Hot-unplug of Tertiary Display will be tested ");
                    doHotUnPlug(tertiary, true, PowerStates.S5);
                }
            }
        }
    }
}
