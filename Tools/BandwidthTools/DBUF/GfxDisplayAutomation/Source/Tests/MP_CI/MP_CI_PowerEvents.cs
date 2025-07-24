namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.Threading.Tasks;

    public class MP_CI_PowerEvents : TestBase
    {
        PowerParams _powerParams = null;
        [Test(Type = TestType.Method, Order = 0)]
        public void TestStep0()
        {
            for (int i = 0; i < 3; i++)
            {
                Log.Message(true, "{0} Put the system into {1} state & resume", i, PowerStates.S3);
                this._powerParams = new PowerParams() { Delay = 30, };
                if (base.InvokePowerEvent(this._powerParams, PowerStates.S3))
                    Log.Success("S3 completed successfully");
                else
                    Log.Fail("Failed to resume from S3");

                Log.Message(true, "{0} Put the system into {1} state & resume", i, PowerStates.S4);
                this._powerParams = new PowerParams() { Delay = 45, };
                if (base.InvokePowerEvent(this._powerParams, PowerStates.S4))
                    Log.Success("S4 completed successfully");
                else
                    Log.Fail("Failed to resume from S4");
            }
        }

        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            Log.Message(true, "Restart Machine");
            this._powerParams = new PowerParams();
            this._powerParams.Delay = 5;
            base.InvokePowerEvent(this._powerParams, PowerStates.S5);
        }

        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            TestStep0();
        }
    }
}
