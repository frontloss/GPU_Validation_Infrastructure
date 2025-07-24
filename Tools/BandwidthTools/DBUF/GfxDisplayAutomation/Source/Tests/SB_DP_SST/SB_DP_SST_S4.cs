using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    /*
    This testcase check whether Displays attached to system remain connected after S4
    */
    [Test(Type = TestType.HasPlugUnPlug)]
    class SB_DP_SST_S4 : SB_DP_SST_Base
    {
        int delay;
        DisplayConfig configBefore, configAfter;

        // Constants to store Bitmap and golden value
        uint uiDPCDOffset = (uint)DPCDRegisters.DPCD_SINK_CONTROL;
        private const uint DP_HOTPLUG_BITMAP = 1;
        private const uint DP_HOTPLUG_GOLDENVALUE = 1;
        private const uint DP_HOTUNPLUG_GOLDENVALUE = 0;

        
        // Attach displays mentioned in command 
        [Test(Type = TestType.Method, Order = 1)]
        public void doHotPlug()
        {
            if (base.CurrentConfig.SecondaryDisplay != DisplayType.None)
            {
                DisplayType secondary = base.CurrentConfig.SecondaryDisplay;
                if (DisplayExtensions.GetDisplayType(secondary) == DisplayType.DP)
                {
                    Log.Message("Current config contains secondary display");
                    base.doHotplug(secondary);
                }
                else
                {
                    Log.Fail("Current config doesn't contain DP as secondary display");
                }
            }
            else
            {
                Log.Fail("Current config doesn't contain secondary display");
            }

            if (base.CurrentConfig.TertiaryDisplay != DisplayType.None)
            {
                DisplayType tertiary = base.CurrentConfig.TertiaryDisplay;
                if (DisplayExtensions.GetDisplayType(tertiary) == DisplayType.DP)
                {
                    Log.Message("Current config contains tertiary display");
                    base.doHotplug(tertiary);
                }
                else
                {
                    Log.Message("Current config doesn't contain DP as tertiary display");
                }
            }
        }

        // Put system into S4 state
        [Test(Type = TestType.Method, Order = 2)]
        public void putInS4()
        {
            configBefore = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);
            base.InvokePowerEvent(PowerStates.S4);
        }
        

        [Test(Type = TestType.Method, Order = 3)]
        public void verifyDPCD()
        {
            if (base.CurrentConfig.SecondaryDisplay != DisplayType.None)
            {
                DisplayType secondary = base.CurrentConfig.SecondaryDisplay;
                if (DisplayExtensions.GetDisplayType(secondary) == DisplayType.DP)
                {
                    VerifyDPCDRegisterValue(secondary, uiDPCDOffset, DP_HOTPLUG_BITMAP, DP_HOTPLUG_GOLDENVALUE);
                }
                else
                {
                    Log.Message("DP as Secondary Display not connected post S3");
                }
            }
            else
            {
                Log.Message("Secondary Display not present");
            }

            if (base.CurrentConfig.TertiaryDisplay != DisplayType.None)
            {
                DisplayType tertiary = base.CurrentConfig.TertiaryDisplay;
                if (DisplayExtensions.GetDisplayType(tertiary) == DisplayType.DP)
                {
                    VerifyDPCDRegisterValue(tertiary, uiDPCDOffset, DP_HOTPLUG_BITMAP, DP_HOTPLUG_GOLDENVALUE);
                }
                else
                {
                    Log.Alert("DP as Tertiary Display not connected post S4");
                }
            }
        }

        //Check in OS page whether all displays are listed post CS
        [Test(Type = TestType.Method, Order = 4)]
        public void verifyInOSPage()
        {
            configAfter = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);
            if (configAfter.ToString().Equals(configBefore.ToString()))
            {
                Log.Message("All Displays are connected post S4");
            }
            else
            {
                Log.Fail("all displays before S4 are not same as all displays after S4");
            }
        }
    }
}
