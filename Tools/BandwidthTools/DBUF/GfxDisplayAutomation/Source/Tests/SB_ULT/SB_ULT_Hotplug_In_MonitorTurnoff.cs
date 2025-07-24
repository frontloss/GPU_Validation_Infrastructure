namespace Intel.VPG.Display.Automation
{
    [Test(Type = TestType.HasPlugUnPlug)]
    class SB_ULT_Hotplug_In_MonitorTurnoff : SB_ULT_Hotplug_In_S3
    {
        public SB_ULT_Hotplug_In_MonitorTurnoff()
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
