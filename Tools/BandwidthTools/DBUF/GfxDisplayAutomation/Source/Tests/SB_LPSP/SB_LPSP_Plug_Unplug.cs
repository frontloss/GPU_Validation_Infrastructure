namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;
    using System.Linq;

    [Test(Type = TestType.HasPlugUnPlug)]
    class SB_LPSP_Plug_Unplug : SB_LPSP_Base 
    {
        protected bool _isLowPowerState = false;
        protected PowerStates _PowerStates; 
        protected System.Action _PowerEventAction = null;

        [Test(Type = TestType.PreCondition, Order = 0)]
        public override void TestStep0()
        {
            if (!(CurrentConfig.DisplayList.Contains(DisplayType.EDP) && base.CurrentConfig.PluggableDisplayList.Count > 0))
                Log.Abort("Test needs atleast 1 pluggable Display");
        }

        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            SetSingleDisplayEDPMode();
        }

        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            foreach (KeyValuePair<System.Action, System.Action> _CurrentModeType in _applyMode)
            {
                // Step - 1
                _CurrentModeType.Key();
                
                // Step - 2
                Log.Message(true, "Verfiy LPSP Register");
                _CurrentModeType.Value();

                // Step - 3
                foreach (DisplayType hotplug in base.CurrentConfig.PluggableDisplayList)
                {
                    Log.Message(true, "Hotplug Action");

                    HotPlug(hotplug);

                    if (base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == hotplug).Select(dI => dI.DisplayType).FirstOrDefault() != DisplayType.None)
                        Log.Success("Enumerated Display List contains {0} after plug", hotplug.ToString());
                    else
                        Log.Fail(false, "Enumerated Display List Does not contain {0} after plug ", hotplug.ToString());
                }

                // Step - 4 
                ApplyConfig(base.CurrentConfig);

                //Adding SD - EDP Config check because After hotplug display config behaviour is not fix
                DisplayConfig hotplugConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);
                
                Log.Message(true, "Verfiy LPSP Register");
                Log.Message("Configuration After Hotplug : {0}", hotplugConfig.GetCurrentConfigStr());
                if (hotplugConfig.ConfigType == DisplayConfigType.SD && hotplugConfig.PrimaryDisplay == DisplayType.EDP)
                    _CurrentModeType.Value();
                else
                    LPSPRegisterVerify(false);

                // Step - 5
                foreach (DisplayType hotplug in base.CurrentConfig.PluggedDisplayList.Reverse<DisplayType>())
                {
                    Log.Message(true,"HotUnplug Action");

                    HotUnPlug(hotplug, _isLowPowerState);

                    if (null != _PowerEventAction)
                    {
                        _PowerEventAction();
                    }

                    if (base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == hotplug).Select(dI => dI.DisplayType).FirstOrDefault() != DisplayType.None)
                        Log.Fail("Enumerated Display List contains {0} after Unplug", hotplug.ToString());
                    else
                        Log.Success("Enumerated Display List Does not contain {0} after Unplug ", hotplug.ToString());
                }

                // Step - 6 
                DisplayConfig currDispConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);
                if (currDispConfig.CustomDisplayList.Intersect(base.CurrentConfig.PluggableDisplayList).ToList().Count!=0)
                    Log.Fail("Hotplugged displays detected after HotUnplug ");

                // Step - 7
                //Adding SD - EDP Config check because After hotUnplug display config behaviour is not fix
                hotplugConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);
                
                Log.Message(true, "Verfiy LPSP Register");
                Log.Message("Display Config after HotUnplug : {0}", hotplugConfig.GetCurrentConfigStr());
                if (hotplugConfig.ConfigType == DisplayConfigType.SD && hotplugConfig.PrimaryDisplay == DisplayType.EDP)
                    _CurrentModeType.Value();
                else
                    LPSPRegisterVerify(false);

                SetSingleDisplayEDPMode();
            }
        }

        protected void PowerEventAction()
        {
            Log.Message(true, "Power Event {0}", _PowerStates);              
            Log.Message("Putting the system into {0} state", _PowerStates);
            PowerParams powerParams = new PowerParams();
            powerParams.Delay = 30;
            base.InvokePowerEvent(powerParams, _PowerStates);
            Log.Success("Put the system into {0} state & resumed", _PowerStates);
        }

        private void SetSingleDisplayEDPMode()
        {
            DisplayConfig dispConfig = new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = DisplayType.EDP };
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, dispConfig))
                Log.Success("Config SET : SD - EDP");
            else
                Log.Fail("Unable to set SD-EDP Mode");
        }
    }
}