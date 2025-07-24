using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    class SB_CDClock_S3 : SB_CDClock_Config_Basic
    {
        protected PowerStates _PowerState ;

        public SB_CDClock_S3()
        {
            _PowerState = PowerStates.S3;
        }
        [Test(Type = TestType.Method, Order = 2)]
        public virtual void TestStep2()
        {
            GotoPowerState(_PowerState);
        }

        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3()
        {
            VerifyCDClockRegisters();
        }

        private void GotoPowerState(PowerStates argPowerState)
        {
            Log.Message(true, "Invoking power event {0}", argPowerState);
            PowerParams powerParams = new PowerParams() { Delay = 30 };
            powerParams.PowerStates = argPowerState;
            base.EventResult(powerParams.PowerStates, base.InvokePowerEvent(powerParams, powerParams.PowerStates));
        }
    }
}
