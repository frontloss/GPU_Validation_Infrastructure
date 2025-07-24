using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    //Test hot unplug
    [Test(Type = TestType.HasPlugUnPlug)]
    class SB_DP_SST_HotUnplug : SB_DP_SST_Base
    {
        DisplayConfig configBefore, configAfter;

        // Constants to store Bitmap and golden value
        uint uiDPCDOffset = (uint)DPCDRegisters.DPCD_SINK_CONTROL;
        private const uint DP_HOTPLUG_BITMAP = 1;
        private const uint DP_HOTPLUG_GOLDENVALUE = 1;
        private const uint DP_HOTUNPLUG_GOLDENVALUE = 0;
        
        [Test(Type = TestType.Method, Order = 1)]
        public void BringUpSystem()
        {
            //First hotplug DP Display
            if (base.CurrentConfig.SecondaryDisplay == DisplayType.DP || base.CurrentConfig.SecondaryDisplay == DisplayType.DP_2 || base.CurrentConfig.SecondaryDisplay == DisplayType.DP_3)
            {
                Log.Message("DP is present as secondary display ");
                base.HotPlug(base.CurrentConfig.SecondaryDisplay, _defaultEDIDMap[base.CurrentConfig.SecondaryDisplay]);
            }
            // Apply/Set SD on secondary Display
            DisplayConfig sec = new DisplayConfig { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay };
            ApplyConfigOS(sec);

            // Retrieve Display of the external Display1
            if (base.CurrentConfig.SecondaryDisplay == DisplayType.DP || base.CurrentConfig.SecondaryDisplay == DisplayType.DP_2 || base.CurrentConfig.SecondaryDisplay == DisplayType.DP_3)
            {
                DisplayType displayType = base.CurrentConfig.SecondaryDisplay;

                // Call VerifyDPCDRegisterValue function to read DPCD register value and compare against golden/expected values
                base.VerifyDPCDRegisterValue(displayType, uiDPCDOffset, DP_HOTPLUG_BITMAP, DP_HOTPLUG_GOLDENVALUE);
            }
            //Call only after bringing up system
            configBefore = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);
        }

        [Test(Type = TestType.Method, Order = 2)]
        public void UnplugDisplay()
        {
            if (base.CurrentConfig.SecondaryDisplay == DisplayType.DP || base.CurrentConfig.SecondaryDisplay == DisplayType.DP_2 || base.CurrentConfig.SecondaryDisplay == DisplayType.DP_3)
            {
                base.HotUnPlug(base.CurrentConfig.SecondaryDisplay);
            }
            configAfter = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);
        }

        [Test(Type = TestType.Method, Order = 3)]
        public void VerifyInOS()
        { // Verify whether OS page enumerates only connected displays 
            Log.Message(true, "Verify the selected display got unplugged  through OS");

            base.VerifyInOS(configBefore, configAfter, DisplayAction.HOTUNPLUG);
        }      
    }
}
