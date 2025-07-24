namespace Intel.VPG.Display.Automation
{
    [Test(Type = TestType.HasPlugUnPlug)]
    class SB_HotUnplug_In_MonitorTurnoff : SB_HotUnplug_In_S3
    {
        public SB_HotUnplug_In_MonitorTurnoff()
            : base()
        {
            _PowerEvent = this.MonitorTurnoff;
        }

        private void MonitorTurnoff()
        {
            Log.Message(true, "Turn off the monitor for 1 min & resume");
            MonitorTurnOffParam monitorOnOffParam = new MonitorTurnOffParam();
            monitorOnOffParam.onOffParam = MonitorOnOff.OffOn;
            monitorOnOffParam.waitingTime = 60;
            if (AccessInterface.SetFeature<bool, MonitorTurnOffParam>(Features.MonitorTurnOff, Action.SetMethod, monitorOnOffParam))
                Log.Success("Turned off the monitor for 1 min & Resumed");
            else
                Log.Fail("Monitor Turn off Operation Fail");
        }    
    }
}
