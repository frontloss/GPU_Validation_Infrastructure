namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    using System.Collections.Generic;

    class MP_NativeCollage_MonitorTurnOff : MP_NativeCollage_BAT
    {
        public MP_NativeCollage_MonitorTurnOff()
        {
            base._performAction = this.PerformAction;
            _myList = new List<DisplayConfigType>()
            {
                DisplayConfigType.Horizontal
            };
        }
        private void PerformAction()
        {
            Log.Message(true, "Turn off the monitor for 1 min & resume");
            MonitorTurnOffParam monitorOnOffParam = new MonitorTurnOffParam();
            monitorOnOffParam.onOffParam = MonitorOnOff.OffOn;
            monitorOnOffParam.waitingTime = 60;
            if (AccessInterface.SetFeature<bool, MonitorTurnOffParam>(Features.MonitorTurnOff, Action.SetMethod, monitorOnOffParam))
            {
                Log.Success("Successfully Turn off monitor and resume back after {0} sec", monitorOnOffParam.waitingTime);
            }
            else
                Log.Fail("Error in Turning off the monitor.");
        }
    }
}