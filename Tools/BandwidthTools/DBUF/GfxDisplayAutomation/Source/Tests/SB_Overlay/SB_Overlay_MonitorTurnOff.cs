namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;

    public class SB_Overlay_MonitorTurnOff : SB_Overlay_S3
    {
        public SB_Overlay_MonitorTurnOff()
            : base()
        {
            _PowerEvent = this.MonitorTurnoff;
        }

        private void MonitorTurnoff()
        {
            Log.Message(true, "Turn off the monitor for 1 min & resume");
            MonitorTurnOffParam monitorOnOffParam = new MonitorTurnOffParam();
            monitorOnOffParam.onOffParam = MonitorOnOff.OffOn;
            monitorOnOffParam.waitingTime = 30;
            if (AccessInterface.SetFeature<bool, MonitorTurnOffParam>(Features.MonitorTurnOff, Action.SetMethod, monitorOnOffParam))
                Log.Success("Turned off the monitor for 1 min & Resumed");
            else
                Log.Fail("Monitor Turn off Operation Fail");
        }    
    }
}