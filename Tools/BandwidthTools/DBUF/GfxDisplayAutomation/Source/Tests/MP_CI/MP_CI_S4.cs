namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;

    class MP_CI_S4 : TestBase
    {
        PowerParams _powerParams = null;
        [Test(Type = TestType.Method, Order = 0)]
        public void TestStep0()
        {
            for (int i = 0; i < 5; i++)
            {
                Log.Message(true, "{0} Put the system into {1} state & resume", i,PowerStates.S4);
                this._powerParams = new PowerParams() { Delay = 30, };
                base.InvokePowerEvent(this._powerParams, PowerStates.S4);
                    Log.Success("S4 completed successfully");
            }
        }
    }
}
