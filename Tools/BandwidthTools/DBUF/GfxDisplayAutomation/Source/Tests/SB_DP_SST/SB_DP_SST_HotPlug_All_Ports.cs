using System;
using System.Collections.Generic;
using System.Collections;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    /*
     * This testcase hotplugs DP display to all supported ports.
     * For test to run sucessfully LSPCON should not be enabled on port
     */ 
    [Test(Type = TestType.HasPlugUnPlug)]
    class SB_DP_SST_HotPlug_All_Ports : SB_DP_SST_Base
    {
        DisplayConfig configBefore, configAfter;

        // Constants to store Bitmap and golden value
        uint uiDPCDOffset = (uint)DPCDRegisters.DPCD_SINK_CONTROL;
        private const uint DP_HOTPLUG_BITMAP = 1;
        private const uint DP_HOTPLUG_GOLDENVALUE = 1;
       
        Hashtable displayIdPortId = new Hashtable();

        /*
         *method name: getValidPorts_HotPlugOnAllPorts
         *argument: none
         *return type: none
         *description: get list of ports on which DP is supported and do hot plug on each port.
         *             Ensure hot plug is succesful.
         */
        [Test(Type = TestType.Method, Order = 1)]
        public void getValidPortsNHotPlugOnAllPorts()
        {
            Log.Message("DFT doesn't support hotplug on LSPCON enabled ports. So ensure LSPCON is disabled on all ports for running this test");
            displayIdPortId = base.getSupportedPorts(DisplayType.DP);
            ICollection keys = displayIdPortId.Keys;
            //to ensure we are doing hotplug unplug for windows id of first instance of port
            int count_DPB = 0, count_DPC = 0, count_DPD = 0;
            foreach (UInt32 displayId in keys)
            {
                String str = displayIdPortId[displayId].ToString();
                if ((str.Contains("DPB") == true && count_DPB == 0 )|| (str.Contains("DPC") == true && count_DPC == 0) || (str.Contains("DPD") == true && count_DPD == 0))
                {
                    configBefore = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);
                    Log.Message("Doing Hotplug on  Port:-" + str + "For Display ID" + displayId);
                    base.HotPlug(DisplayType.DP, true, displayId, _defaultEDIDMap[DisplayType.DP], false);
                    configAfter = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);
                    base.VerifyInOS(configBefore, configAfter, DisplayAction.HOTPLUG);
                    base.VerifyDPCDRegisterValue(DisplayType.DP, uiDPCDOffset, DP_HOTPLUG_BITMAP, DP_HOTPLUG_GOLDENVALUE);
                    base.HotUnPlug(DisplayType.DP);

                    if (str.Contains("DPB") == true)
                        count_DPB++;

                    if (str.Contains("DPC") == true)
                        count_DPC++;

                    if (str.Contains("DPD") == true)
                        count_DPD++;
                }
            }
        }
    }
}
