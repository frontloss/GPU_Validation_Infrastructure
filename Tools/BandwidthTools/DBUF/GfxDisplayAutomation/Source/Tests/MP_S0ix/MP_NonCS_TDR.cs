namespace Intel.VPG.Display.Automation
{
    class MP_NonCS_TDR : MP_S0ix_TDR
    {
        public MP_NonCS_TDR()
        {
            nonCS_PackageC8PlushState = true;
            NonCSInputOption = NonCSPowerOption.MonitorOff;
            base.monitorOnOffParam = new MonitorTurnOffParam() { onOffParam = MonitorOnOff.OffOn, waitingTime = 45 };
        }
    }
}
