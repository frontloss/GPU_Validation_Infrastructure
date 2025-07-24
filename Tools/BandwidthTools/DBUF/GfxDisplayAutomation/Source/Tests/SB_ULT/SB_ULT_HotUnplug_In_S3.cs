namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    [Test(Type = TestType.HasPlugUnPlug)]
    class SB_ULT_HotUnplug_In_S3 : SB_ULT_Hotplug_Unplug_Basic
    {
        protected PowerStates _PowerState;
        protected System.Action _PowerEvent = null;
        public SB_ULT_HotUnplug_In_S3()
            : base()
        {
            _PowerState = PowerStates.S3;
            _PowerEvent = PowerEvent;
        }

        [Test(Type = TestType.Method, Order = 2)]
        public override void TestStep2()
        {
            int displaysCountBeforePlug = base.EnumeratedDisplays.Count;
            base.CurrentConfig.DisplayList.Intersect(base._defaultEDIDMap.Keys).ToList().ForEach(curDisp =>
            {
                base.HotUnPlug(curDisp, true);
                _PowerEvent();

                if (displaysCountBeforePlug-1 == base.EnumeratedDisplays.Count)
                {
                    Log.Success("{0} UnPlug Successful.", curDisp);
                    displaysCountBeforePlug--;
                }
                else
                {
                    Log.Fail("Unable to UnPlug {0}.", curDisp);
                }
            });
        }

        protected void PowerEvent()
        {
            Log.Verbose("Putting the system into {0} state & resume ", _PowerState);
            PowerParams powerParams = new PowerParams();
            powerParams.Delay = 30;
            base.InvokePowerEvent(powerParams, _PowerState);
            Log.Success("Put the system into {0} state & resumed ", _PowerState);
        }
    }
}
