namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    using System.Collections.Generic;

    class MP_BAT_DisplaySwitch_CUI : MP_DisplaySwitch_OSPage
    {
        public MP_BAT_DisplaySwitch_CUI()
        {
            base._additionalActionHandler = () =>
            {
                base.DisableNVerifyIGDWithDTCM(4);
                base.EnableNVerifyIGDBasic(5);
                List<uint> winMonitorIDList = base.ListEnumeratedDisplays();
                List<uint> enumeratedWinMonIDList = base.CurrentConfig.EnumeratedDisplays.Where(dI => !dI.WindowsMonitorID.Equals(0)).Select(dI => dI.WindowsMonitorID).ToList();
                if (!enumeratedWinMonIDList.Count.Equals(winMonitorIDList.Count))
                {
                    Log.Fail(false, "Some displays are not enumerated!");
                    Log.Verbose("Currently enumerated display list [{0}] mismatch with windows monitor id list [{1}]! A reboot is required.", enumeratedWinMonIDList.Count, winMonitorIDList.Count);
                    base.InvokePowerEvent(new PowerParams() { Delay = 5, PowerStates = PowerStates.S5 }, PowerStates.S5);
                }
            };
        }
    }
}