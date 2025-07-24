namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.Threading.Tasks;

    [Test(Type = TestType.HasPlugUnPlug)]
    class MP_NonCS_Display_HotUnplug : MP_DuringS0ix_DisplayHotplugUnplug
    {
        public MP_NonCS_Display_HotUnplug()
        {
            base.nonCS_PackageC8PlushState = true;
            base.NonCSInputOption = NonCSPowerOption.MonitorOff;
            base.monitorOnOffParam = new MonitorTurnOffParam() { onOffParam = MonitorOnOff.OffOn, waitingTime = 45 };
        }
    }
}
