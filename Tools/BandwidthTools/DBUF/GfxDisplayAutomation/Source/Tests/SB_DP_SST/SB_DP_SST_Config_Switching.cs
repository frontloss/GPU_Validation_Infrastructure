namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;
    using System.Linq;

    public class SB_DP_SST_Config_Switching : SB_DP_SST_Base
    {
        protected List<DisplayConfig> _dispSwitchOrder = null;
        public uint uiDPCDOffset = (uint)DPCDRegisters.DPCD_SINK_CONTROL;

        [Test(Type = TestType.Method, Order = 1)]
        public virtual void ConfigCheck()
        {
            if (base.CurrentConfig.DisplayList.Count() <= 1)
            {
                Log.Abort("This test should be run with atleast two external displays");
            }             
        }

        [Test(Type = TestType.Method, Order = 2)]
        //Function to set SD Configuration
        public void ConfigSwitchingSingle()
        {
            DisplayConfig sdConfig = new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay };

            ApplyConfigOS(sdConfig);
            VerifyConfigOS(sdConfig);
        }


        [Test(Type = TestType.Method, Order = 3)]
        //Function to set DDC,ED Configuration on External Display
        public void ConfigSwitchingDual()
        {
            DisplayConfig edConfig = new DisplayConfig() { ConfigType = DisplayConfigType.ED, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay };
            DisplayConfig ddcConfig = new DisplayConfig() { ConfigType = DisplayConfigType.DDC, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay };
            DisplayType display = base.CurrentConfig.SecondaryDisplay;

            _dispSwitchOrder = new List<DisplayConfig>() { ddcConfig, edConfig };

            _dispSwitchOrder.ForEach(curConfig =>
            {
                ApplyConfigOS(curConfig);

                // Verify DPCD register only if Display type is DP
                if (DisplayExtensions.GetDisplayType(display) == DisplayType.DP)
                {
                    // Call VerifyDPCDRegisterValue function to read DPCD register value and compare against golden/expected values
                    base.VerifyDPCDRegisterValue(display, uiDPCDOffset, DP_HOTPLUG_BITMAP, DP_HOTPLUG_GOLDENVALUE);
                }

                VerifyConfigOS(curConfig);

                //Now we swap the displays and again verify the config switching works
                SwapDisplaysAndApplyConfig(curConfig);
            });
        }

        [Test(Type = TestType.Method, Order = 4)]
        //Function to set TDC,TED Configuration on External Display
        public void ConfigSwitchingTri()
        {
            DisplayConfig tedConfig = new DisplayConfig() { ConfigType = DisplayConfigType.TED, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay, TertiaryDisplay = base.CurrentConfig.TertiaryDisplay };
            DisplayConfig tdcConfig = new DisplayConfig() { ConfigType = DisplayConfigType.TDC, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay, TertiaryDisplay = base.CurrentConfig.TertiaryDisplay };

            // If tertiary display planned then then repeat test for Tri Clone and Extended combinations
            if (base.CurrentConfig.TertiaryDisplay != DisplayType.None)
            {
                DisplayType display = base.CurrentConfig.TertiaryDisplay;
                _dispSwitchOrder = new List<DisplayConfig>() { tedConfig, tdcConfig };

                _dispSwitchOrder.ForEach(curConfig =>
                {
                    ApplyConfigOS(curConfig);

                    // Verify DPCD register only if Display type is DP
                    if (DisplayExtensions.GetDisplayType(display) == DisplayType.DP)
                    {
                        // Call VerifyDPCDRegisterValue function to read DPCD register value and compare against golden/expected values
                        base.VerifyDPCDRegisterValue(display, uiDPCDOffset, DP_HOTPLUG_BITMAP, DP_HOTPLUG_GOLDENVALUE);
                    }

                    VerifyConfigOS(curConfig);

                    //Now we swap the displays and again verify the config switching works
                    SwapDisplaysAndApplyConfig(curConfig);
                });
            }
        }
    }
}
