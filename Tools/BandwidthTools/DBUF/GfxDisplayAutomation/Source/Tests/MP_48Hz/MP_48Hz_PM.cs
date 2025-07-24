namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Linq;
    using System.Windows.Forms;
    using System.Threading;
    using System.IO;
    using System.Diagnostics;

    class MP_48Hz_PM : MP_48Hz_Basic
    {
        private PowerStates _powerStateOption;

        [Test(Type = TestType.Method, Order = 7)]
        public void TestStep7()
        {
            Log.Message(true, "Go to S3 and resume");
            _powerStateOption = PowerStates.S3;
            PowerParams powerParam = new PowerParams() { Delay = 30, PowerStates = _powerStateOption };
            if (AccessInterface.SetFeature<bool, PowerParams>(Features.PowerEvent, Action.SetMethod, powerParam))
                Log.Success("{0} completed successfully", powerParam.PowerStates);
            else
                Log.Fail("{0} power state event failed !! ", powerParam.PowerStates);
            base.TestStep5();
            base.TestStep6();
        }
        [Test(Type = TestType.Method, Order = 8)]
        public void TestStep8()
        {
            Log.Message(true, "Go to S4 and resume");
            _powerStateOption = PowerStates.S4;
            PowerParams powerParam = new PowerParams() { Delay = 30, PowerStates = _powerStateOption };
            if (AccessInterface.SetFeature<bool, PowerParams>(Features.PowerEvent, Action.SetMethod, powerParam))
                Log.Success("{0} completed successfully", powerParam.PowerStates);
            else
                Log.Fail("{0} power state event failed !! ", powerParam.PowerStates);
            base.TestStep5();
            base.TestStep6();
        }
    }
}
