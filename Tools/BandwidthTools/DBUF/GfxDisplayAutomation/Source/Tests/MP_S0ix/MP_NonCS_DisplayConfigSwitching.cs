
namespace Intel.VPG.Display.Automation
{
    class MP_NonCS_DisplayConfigSwitching : MP_S0ix_DisplayConfigSwitching
    {
        public MP_NonCS_DisplayConfigSwitching()
        {
            base.nonCS_PackageC8PlushState = true;
            base.NonCSInputOption = NonCSPowerOption.MonitorOff;
            base.monitorOnOffParam = new MonitorTurnOffParam() { onOffParam = MonitorOnOff.OffOn, waitingTime = 45 };
        }
    }
}
