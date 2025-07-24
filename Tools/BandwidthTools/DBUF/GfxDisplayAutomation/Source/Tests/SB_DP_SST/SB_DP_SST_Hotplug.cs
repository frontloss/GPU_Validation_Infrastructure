using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    // This test verifies the HotPlug functionality of the external DP display(s). As part of verification -  
    // 1) Checks whether CUI/OS page enumerates hotplugged displays properly or not and 
    // 2) DPCD register values of DP displays are read and evaluated for correctness 

    [Test(Type = TestType.HasPlugUnPlug)]
    class SB_DP_SST_Hotplug : SB_DP_SST_Base
    {
        // Constants to store Bitmap and golden value
        private const uint DP_HOTPLUG_BITMAP       = 0x00000001;
        private const uint DP_HOTPLUG_GOLDENVALUE  = 0x00000001;

        // Variables to store Config details before and after plug/unplug of displays
        DisplayConfig ConfigBeforeHotplug, ConfigAfterHotplug;

        public uint uiDPCDOffset; // Variable to store DPCD offset

        [Test(Type = TestType.Method, Order = 1)]
        public void HotPlugExternalDisplays()
        {
            // Save the Display details which are active/connected
            ConfigBeforeHotplug = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);

            Log.Message(true, "Hotplug all the external displays");

            // Hotplug external displays and verify DPCD registers values for each DP display
            foreach(DisplayType Display in base.CurrentConfig.PluggableDisplayList)
            {
                Log.Message("{0} is not enumerated. Plugging now ...", Display);

                if (true == base.HotPlug(Display, _defaultEDIDMap[Display], false))
                {
                    Log.Success("Display {0} is plugged successfully", Display);

                    // Apply/Set SD on plugged DP display
                    DisplayConfig SDConfig = new DisplayConfig { ConfigType = DisplayConfigType.SD, PrimaryDisplay = Display };
                    ApplyConfigOS(SDConfig);

                    // Read DPCD register values only if DisplayType is DP

                    if (DisplayExtensions.GetDisplayType(Display) == DisplayType.DP)
                    {
                        // Copy DPCD register address to uiDPCDOffset                        
                        uiDPCDOffset = (uint)DPCDRegisters.DPCD_SINK_CONTROL;

                        // Call VerifyDPCDRegisterValue function to read DPCD register value and compare against golden/expected values
                        base.VerifyDPCDRegisterValue(Display, uiDPCDOffset, DP_HOTPLUG_BITMAP, DP_HOTPLUG_GOLDENVALUE);
                    }
                }
                else
                {
                    Log.Fail("Unable to Hotplug display {0}", Display);
                }
            }

            // Save the config after Hotplugging of external displays
            ConfigAfterHotplug = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);

            // Verify newly Plugged Displays are enumerated by the OS
            VerifyInOS(ConfigBeforeHotplug, ConfigAfterHotplug, DisplayAction.HOTPLUG);
        }       
    }
}