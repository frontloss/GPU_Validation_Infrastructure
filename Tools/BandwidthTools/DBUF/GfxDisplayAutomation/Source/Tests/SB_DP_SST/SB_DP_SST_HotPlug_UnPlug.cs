using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    // This test verifies the HotPlug/Unplug functionality of the external DP display(s). As part of verification -  
    // 1) Checks whether CUI/OS page enumerates hotplugged displays properly or not and 
    // 2) DPCD register values of DP displays are read and evaluated for correctness 

    [Test(Type = TestType.HasPlugUnPlug)]
    class SB_DP_SST_HotPlug_UnPlug : SB_DP_SST_Base
    {
        // Constants to store Bitmap and golden value
        private const uint DP_HOTPLUG_BITMAP = 0x00000001;
        private const uint DP_HOTPLUG_GOLDENVALUE = 0x00000001;

        // Variables to store Config details before and after plug/unplug of displays
        DisplayConfig ConfigBeforeHotplug, ConfigAfterHotplug, ConfigBeforeHotunplug, ConfigAfterHotunplug;

        public uint uiDPCDOffset; // Variable to store DPCD offset

        [Test(Type = TestType.Method, Order = 1)]
        public void HotPlugUnPlugExternalDisplays()
        {
            // Save the Display details which are active/connected
            ConfigBeforeHotplug = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);
            Log.Message(true, "Hotplug all the External displays");
            DisplayList displayList = this.ApplicationManager.ParamInfo.Get<DisplayList>(ArgumentType.Display);

            if (!displayList.Contains(DisplayType.DP))
            {
                Log.Abort("This test requires atleast one DP Display");
            }
            // Hotplug external displays and verify DPCD registers values for each DP display
            foreach (DisplayType Display in base.CurrentConfig.PluggableDisplayList)
            {
                Log.Message("{0} is not enumerated. Plugging now ...", Display);
                if (true == base.HotPlug(Display, _defaultEDIDMap[Display], false))
                {
                    Log.Success("Display {0} is plugged successfully", Display);

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
            if (EnumeratedDisplays.Count == 2)
            {
                DisplayConfig ddcConfig = new DisplayConfig() { ConfigType = DisplayConfigType.DDC, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay };
                ApplyConfigOS(ddcConfig);
                Log.Success("Successfully applied DDC Configuration");
            }
            else if (EnumeratedDisplays.Count == 3)
            {
                DisplayConfig tdcConfig = new DisplayConfig() { ConfigType = DisplayConfigType.TDC, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay, TertiaryDisplay = base.CurrentConfig.TertiaryDisplay };
                ApplyConfigOS(tdcConfig);
                Log.Success("Successfully applied TDC Configuration");
            }

            // Save the config after Hotplugging of external displays
            ConfigAfterHotplug = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);

            // Verify newly Plugged Displays are enumerated by the OS
            VerifyInOS(ConfigBeforeHotplug, ConfigAfterHotplug, DisplayAction.HOTPLUG);

            ConfigBeforeHotunplug = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);

            Log.Message(true, "HotUnplug all the External displays");
            // Hotunplug external displays and verify DPCD registers values for each DP display
            base.CurrentConfig.DisplayList.Intersect(base._defaultEDIDMap.Keys).ToList().ForEach(curDisp =>
            {
                if (true == base.HotUnPlug(curDisp, false))
                {
                    Log.Success("Display {0} is Unplugged successfully", curDisp);

                    // Save the config after Hotplugging of external displays
                    ConfigAfterHotunplug = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);

                    // Verify whether OS page enumerates only connected displays 
                    Log.Message(true, "Verify the selected display got Unplugged through OS");
                    VerifyInOS(ConfigBeforeHotunplug, ConfigAfterHotunplug, DisplayAction.HOTUNPLUG);
                }
                else
                {
                    Log.Fail("Unable to HotUnplug display {0}", curDisp);
                }
            });
        }
    }
}