namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.Threading.Tasks;
    [Test(Type = TestType.HasPlugUnPlug)]
    public class SB_Modes_Hotplug_Unplug_S4 : SB_Modes_Hotplug_Unplug_S3
    {
        protected override void InvokePowerEvent()
        {
            Log.Message(true, "Invoking S4");
            this._powerParams = new PowerParams() { Delay = 30 };
            _powerParams.PowerStates = PowerStates.S4;
            _powerParams.Delay = 30;
            base.EventResult(_powerParams.PowerStates, base.InvokePowerEvent(_powerParams, _powerParams.PowerStates));
        }
    }
}
