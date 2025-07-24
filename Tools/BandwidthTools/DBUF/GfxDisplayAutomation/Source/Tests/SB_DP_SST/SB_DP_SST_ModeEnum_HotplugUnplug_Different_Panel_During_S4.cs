using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    // This test verifies the HotPlug and Unplug functionalities of the external DFP (DP/HDMI) display(s)
    // where one DFP is replaced with another different DFP. As part of verification:
    // 1) Checks whether CUI/OS page enumerates hotplugged displays properly or not and 
    // 2) DPCD register values of DP displays are read and evaluated for correctness 

    [Test(Type = TestType.HasPlugUnPlug)]
    class SB_DP_SST_ModeEnum_HotplugUnplug_Different_Panel_During_S4 : SB_DP_SST_Base
    {
        // Constants to store Bitmap and golden value
        private const uint DP_HOTPLUG_BITMAP = 0x00000001;
        private const uint DP_HOTPLUG_GOLDENVALUE = 0x00000001;

        DisplayConfig CurrentConfig = new DisplayConfig();

        public uint uiDPCDOffset = (uint)DPCDRegisters.DPCD_SINK_CONTROL;  // Variable to store DPCD offset

        private List<DisplayModeList> _commonDisplayModeList = new List<DisplayModeList>();

        // Handle 2 Displays in this Step
        [Test(Type = TestType.Method, Order = 1)]
        public void ModeEnum_HotplugUnplug_DifferentPanels_S4_TwoDisplays()
        {
            DisplayType Secondary = base.CurrentConfig.SecondaryDisplay;

            // Hotplug external display (DP/HDMI) and verify DPCD register value for the DP display
            base.doHotplug(Secondary, true, PowerStates.S4, _defaultEDIDMap[Secondary]);

            // Verify DPCD register only if Display type is DP
            if (DisplayExtensions.GetDisplayType(base.CurrentConfig.SecondaryDisplay) == DisplayType.DP)
            {
                // Call VerifyDPCDRegisterValue function to read DPCD register value and compare against golden/expected values
                base.VerifyDPCDRegisterValue(Secondary, uiDPCDOffset, DP_HOTPLUG_BITMAP, DP_HOTPLUG_GOLDENVALUE);
            }

            // Verify LFP (eDP) + DFP (DP/HDMI) in Dual-Clone mode works as expected                
            CurrentConfig.PrimaryDisplay = base.CurrentConfig.PrimaryDisplay;
            CurrentConfig.SecondaryDisplay = base.CurrentConfig.SecondaryDisplay;

            // Apply dual display Clone/ED config, Swap displays and verifies max resolutions retrieved from OS/CUI
            ApplyConfig_Swap_CheckMaxRes_TwoDisplays(CurrentConfig);

            // Unplug DFT display1 and plug display2 when System is in S4   
            doHotUnPlugPlug(Secondary, _changeEdid[Secondary], true, PowerStates.S4);

            // Verify DPCD register only if Display type is DP
            if (DisplayExtensions.GetDisplayType(base.CurrentConfig.SecondaryDisplay) == DisplayType.DP)
            {
                // Call VerifyDPCDRegisterValue function to read DPCD register value and compare against golden/expected values
                base.VerifyDPCDRegisterValue(Secondary, uiDPCDOffset, DP_HOTPLUG_BITMAP, DP_HOTPLUG_GOLDENVALUE);
            }

            // Verify LFP (eDP) + DFP (DP/HDMI) in Dual-Clone mode works as expected                
            CurrentConfig.PrimaryDisplay = base.CurrentConfig.PrimaryDisplay;
            CurrentConfig.SecondaryDisplay = base.CurrentConfig.SecondaryDisplay;

            // Apply dual display Clone/ED config, Swap displays and verifies max resolutions retrieved from OS/CUI
            ApplyConfig_Swap_CheckMaxRes_TwoDisplays(CurrentConfig);
        }

        // Handle 3 Displays in this Step. This step is applicable only if 3rd Display is planned
        [Test(Type = TestType.Method, Order = 2)]
        public virtual void ModeEnum_HotplugUnplug_DifferentPanels_S4_ThreeDisplays()
        {
            // If tertiary display planned then then repeat test for Tri Clone and Extended combinations
            if (base.CurrentConfig.TertiaryDisplay != DisplayType.None)
            {
                DisplayType TertiaryDisplay = base.CurrentConfig.TertiaryDisplay;

                // Hotplug external display (DP/HDMI) and verify DPCD register value for the DP display
                base.doHotplug(TertiaryDisplay, true, PowerStates.S4, _defaultEDIDMap[TertiaryDisplay]);

                // Verify DPCD register only if Display type is DP
                if (DisplayExtensions.GetDisplayType(base.CurrentConfig.TertiaryDisplay) == DisplayType.DP)
                {
                    // Call VerifyDPCDRegisterValue function to read DPCD register value and compare against golden/expected values
                    base.VerifyDPCDRegisterValue(TertiaryDisplay, uiDPCDOffset, DP_HOTPLUG_BITMAP, DP_HOTPLUG_GOLDENVALUE);
                }

                // Verify LFP (eDP) + DFP (DP/HDMI) in Tri-Clone mode works as expected
                CurrentConfig.PrimaryDisplay = base.CurrentConfig.PrimaryDisplay;
                CurrentConfig.SecondaryDisplay = base.CurrentConfig.SecondaryDisplay;
                CurrentConfig.TertiaryDisplay = base.CurrentConfig.TertiaryDisplay;

                // Apply dual display Clone/ED config, Swap displays and verifies max resolutions retrieved from OS/CUI
                ApplyConfig_Swap_CheckMaxRes_ThreeDisplays(CurrentConfig);

                // Unplug DFT display1 and plug display2 when System is in S4   
                doHotUnPlugPlug(TertiaryDisplay, _changeEdid[TertiaryDisplay], true, PowerStates.S4);

                // Verify DPCD register only if Display type is DP
                if (DisplayExtensions.GetDisplayType(base.CurrentConfig.TertiaryDisplay) == DisplayType.DP)
                {
                    // Call VerifyDPCDRegisterValue function to read DPCD register value and compare against golden/expected values
                    base.VerifyDPCDRegisterValue(TertiaryDisplay, uiDPCDOffset, DP_HOTPLUG_BITMAP, DP_HOTPLUG_GOLDENVALUE);
                }

                // Verify LFP (eDP) + DFP (DP/HDMI) in Tri-Clone mode works as expected
                CurrentConfig.PrimaryDisplay = base.CurrentConfig.PrimaryDisplay;
                CurrentConfig.SecondaryDisplay = base.CurrentConfig.SecondaryDisplay;
                CurrentConfig.TertiaryDisplay = base.CurrentConfig.TertiaryDisplay;

                // Apply dual display Clone/ED config, Swap displays and verifies max resolutions retrieved from OS/CUI
                ApplyConfig_Swap_CheckMaxRes_ThreeDisplays(CurrentConfig);
            }
        }
    }
}
