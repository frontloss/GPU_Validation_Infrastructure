namespace Intel.VPG.Display.Automation
{
    using System;
    using System.IO;

    public class SB_DP_SST_Monitor_TurnOff_Basic : SB_DP_SST_Base
    {
        public uint uiDPCDOffset = (uint)DPCDRegisters.DPCD_SINK_CONTROL;
        protected DisplayConfig configAfter, configBefore;

        [Test(Type = TestType.Method, Order = 0)]
        //To perform sleep/resume operation by Monitor TurnOff using display timer
        public void MonitorTurnOffOn()
        {
            Log.Message(true, "Checking for the Connected Displays");
            configBefore = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);
            Log.Message(true, "Turning Off Monitor for 1 min and resuming back");
            MonitorTurnOffParam monitorOnOffParam = new MonitorTurnOffParam();
            monitorOnOffParam.onOffParam = MonitorOnOff.OffOn;         
            // Read monitor turnoff time from the Configuration file. 
            string HandletoFile = Path.Combine(Directory.GetCurrentDirectory(), "SB_DP_SST_MonitorTurnOff_WaitingTime.txt"); 
            string countStr = File.ReadAllText(HandletoFile); 
            int waitingTime = Convert.ToUInt16(countStr.Trim());

            if (AccessInterface.SetFeature<bool, MonitorTurnOffParam>(Features.MonitorTurnOff, Action.SetMethod, monitorOnOffParam))
            {
                Log.Success("Successfully Turn off monitor and resume back after {0} sec", waitingTime);
            }
            else
            {
                Log.Fail("Error in Turning off the monitor.");
            }
            foreach(DisplayType display in base.CurrentConfig.PluggableDisplayList)
            {
                Log.Message("{0} is not enumerated. Plugging now ...", display);
                // Read DPCD register values only if DisplayType is DP 
                if (DisplayExtensions.GetDisplayType(display) == DisplayType.DP)
                {
                    // Call VerifyDPCDRegisterValue function to read DPCD register value and compare against golden/expected values 
                    VerifyDPCDRegisterValue(display, uiDPCDOffset, DP_HOTPLUG_BITMAP, DP_HOTPLUG_GOLDENVALUE);
                }
            }
            configAfter = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);
            VerifyInOS(configBefore, configAfter, DisplayAction.MONITORTURNOFF);
        }
    }
}