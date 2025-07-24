namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    [Test(Type = TestType.HasPlugUnPlug)]
    class SB_HotUnplug_In_S3_pri_sec_swap : SB_Hotplug_Unplug_Basic
    {
        protected PowerStates _PowerState;
        protected System.Action _PowerEvent = null;
        public SB_HotUnplug_In_S3_pri_sec_swap()
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


        [Test(Type = TestType.Method, Order = 3)]
        public override void TestStep3()
        {
            base.CurrentConfig.DisplayList.Intersect(_defaultEDIDMap.Keys).ToList().ForEach(curDisp =>
            {
                base.HotPlug(curDisp, _defaultEDIDMap[curDisp]);
            });

            DisplayConfig currentConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);
            DisplayConfig edConfig = new DisplayConfig() { ConfigType = DisplayConfigType.ED, PrimaryDisplay = currentConfig.SecondaryDisplay, SecondaryDisplay = currentConfig.PrimaryDisplay};
            base.ApplyConfigOS(edConfig);          
        }

             
        [Test(Type = TestType.Method, Order = 4)]
        public override void TestStep4()
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


        public override void TestStep5()
        {
            Log.Success("All external displays unplugged, test passed");
            
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
