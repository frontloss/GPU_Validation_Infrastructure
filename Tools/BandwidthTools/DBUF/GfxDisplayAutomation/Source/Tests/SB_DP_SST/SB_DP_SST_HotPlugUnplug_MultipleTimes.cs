using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.IO;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    // This test verifies the Hotplug and Unplug functionality of the external DP display(s) for fixed number of cycles. 
    // Where number of cycles can be any valid number as mentioned in the configuration file SB_DP_SST_HotPlugUnplug_CyclesCount.txt. 
    // As part of verification -  
    // 1) Checks whether CUI/OS page enumerates hot plugged/unplugged displays properly or not and 
    // 2) DPCD register values of DP displays are read and evaluated for correctness for each Hot plug and Unplug

    [Test(Type = TestType.HasPlugUnPlug)]
    class SB_DP_SST_HotPlugUnplug_MultipleTimes : SB_DP_SST_Base
    {
        // Constants to store register Bitmap and expected Golden value
        private const uint DP_HOTPLUG_UNPLUG_BITMAP = 0x00000001;
        private const uint DP_HOTPLUG_GOLDENVALUE   = 0x00000001;
        private const uint DP_HOTUNPLUG_GOLDENVALUE = 0x00000000;

        public uint uiDPCDOffset; // Variable to store DPCD offset

        [Test(Type = TestType.Method, Order = 1)]
        public void HotPlugUnPlugExternalDisplays_MultipleTimes()
        {
            Log.Message(true, "Hotplug and Unplug of the external displays multiple times");

            // Read number of cycles to be repeated for Hotplug and Unplug from the Configuration file.
            string HandletoFile = Path.Combine(Directory.GetCurrentDirectory(), "SB_DP_SST_HotPlugUnplug_CyclesCount.txt");
            string countStr = File.ReadAllText(HandletoFile);
            int Num_Of_Cycles = Convert.ToUInt16(countStr.Trim());

            // Repeat Hotplug and Unplug for fixed number of cycles as defined by Tester in the Configuration file
            for (int index = 1; index <= Num_Of_Cycles; index++)
            {
                // Hotplug external displays and verify DPCD registers values for each DP display
                foreach (DisplayType Display in base.CurrentConfig.PluggableDisplayList)
                {
                    // Copy DPCD register address to uiDPCDOffset                        
                    uiDPCDOffset = (uint)DPCDRegisters.DPCD_SINK_CONTROL;

                    Log.Message("Cycle {0}: Performing HotPlug and UnplugPlug unplug of DP display", index);

                    // Hotplug the external DP display
                    if (true == base.HotPlug(Display, _defaultEDIDMap[Display]))
                    {
                        Log.Success("Cycle {0}: Display {0} is plugged successfully", index, Display);

                        if (DisplayExtensions.GetDisplayType(Display) == DisplayType.DP)
                        {
                            // Call VerifyDPCDRegisterValue function to read DPCD register value and compare against golden/expected values
                            base.VerifyDPCDRegisterValue(Display, uiDPCDOffset, DP_HOTPLUG_UNPLUG_BITMAP, DP_HOTPLUG_GOLDENVALUE);
                        }
                    }
                    else
                    {
                        Log.Fail("Cycle {0}: Unable to Hotplug display {0}", index, Display);
                    }

                    // HotUnplug the external DP display
                    if (true == base.HotUnPlug(Display))
                    {
                        Log.Success("Cycle {0}: Display {0} is Unplugged successfully", index, Display);
                    }
                    else
                    {
                        Log.Fail("Cycle {0}: Unable to Unplug display {0}", index, Display);
                    }
                }
            }
        }
    }
}