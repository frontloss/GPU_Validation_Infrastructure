using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    /*
     Check whether Hotplug unplug functionality is working correctly post S4
    */
    [Test(Type = TestType.HasPlugUnPlug)]
    class SB_DP_SST_Hotplug_Unplug_After_S4 : SB_DP_SST_Base
    {
        int delay = 15;
        PowerParams _powerParams = new PowerParams();

        //Put System into Hibernate state
        [Test(Type = TestType.Method, Order = 1)]
        public void putInS4()
        {
            //Delay can be modified as per requirement
            _powerParams.Delay = delay;
            Log.Message("Putting System into S4");
            //Put system into S4 state by invoking power event
            base.InvokePowerEvent(_powerParams, PowerStates.S4);
        }

        //Hotplug DP as secondary display if present in config
        [Test(Type = TestType.Method, Order = 2)]
        public void hotplugSecondary()
        {
            if (base.CurrentConfig.SecondaryDisplay != DisplayType.None)
            {
                DisplayType secondary = base.CurrentConfig.SecondaryDisplay;
                if (DisplayExtensions.GetDisplayType(secondary) == DisplayType.DP)
                {
                    Log.Message("Current config contains DP as secondary display");
                    doHotplug(secondary);
                }
                else
                {
                    Log.Message("Current config doesn't contain DP secondary display");
                }
            }
            else
            {
                Log.Message("Current config doesn't contain secondary display");
            }
        }

        //Unplug DP secondary display which is already plugged
        [Test(Type = TestType.Method, Order = 3)]
        public void hotUnplugSecondary()
        {
            if (base.CurrentConfig.SecondaryDisplay != DisplayType.None)
            {
                DisplayType secondary = base.CurrentConfig.SecondaryDisplay;

                if (DisplayExtensions.GetDisplayType(secondary) == DisplayType.DP)
                {
                    Log.Message("Current config contains DP as secondary display");
                    doHotUnPlug(base.CurrentConfig.SecondaryDisplay);
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

        //Hotplug Tertiary display if present in config
        [Test(Type = TestType.Method, Order = 4)]
        public void testHotplugTertiary()
        {
            if (base.CurrentConfig.TertiaryDisplay != DisplayType.None)
            {
                DisplayType tertiary = base.CurrentConfig.TertiaryDisplay;
                if (DisplayExtensions.GetDisplayType(tertiary) == DisplayType.DP)
                {
                    Log.Message("Tertiary Display is present in config");
                    Log.Message("Hotplug unplug will be tested for tertiary display post S4");
                    putInS4();
                    doHotplug(tertiary);
                }
             }
        }
        // Unplug Tertiary display if already plugged
        [Test(Type = TestType.Method, Order = 5)]
        public void testHotUnplugTertiary()
        {
            if (base.CurrentConfig.TertiaryDisplay != DisplayType.None)
            {
                DisplayType tertiary = base.CurrentConfig.TertiaryDisplay;
                if (DisplayExtensions.GetDisplayType(tertiary) == DisplayType.DP)
                {
                    Log.Message("Hot-unplug of Tertiary Display will be tested ");
                    base.HotUnPlug(tertiary);
                }
            }
        }
    }
}
