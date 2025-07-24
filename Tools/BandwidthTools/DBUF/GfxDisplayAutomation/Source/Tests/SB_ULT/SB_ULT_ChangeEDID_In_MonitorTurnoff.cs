namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    [Test(Type = TestType.HasPlugUnPlug)]
    class SB_ULT_ChangeEDID_In_MonitorTurnoff : SB_ULT_ChangeEDID_In_S3
    {
        [Test(Type = TestType.Method, Order = 3)]
        public override void TestStep3()
        {
            Log.Message(true, "Turn off the monitor for 1 min & resume");
            MonitorTurnOffParam monitorOnOffParam = new MonitorTurnOffParam();
            monitorOnOffParam.onOffParam = MonitorOnOff.OffOn;
            monitorOnOffParam.waitingTime = 60;
            if (AccessInterface.SetFeature<bool, MonitorTurnOffParam>(Features.MonitorTurnOff, Action.SetMethod, monitorOnOffParam))
                Log.Success("Turned off the monitor for 1 min & Resumed");
            else
                Log.Fail("Monitor Turn off Operation Fail");
        }
    }
}
