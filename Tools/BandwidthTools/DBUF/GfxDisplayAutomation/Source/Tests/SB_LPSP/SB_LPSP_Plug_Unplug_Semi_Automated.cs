namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;

    class SB_LPSP_Plug_Unplug_Semi_Automated : SB_LPSP_Base 
    {
        protected PowerStates _PowerStates;
        protected System.Action _PowerAction;
        protected String _PromptMessage_Plug = "Plug Displays as per Configuration before Going further";
        protected String _PromptMessage_UnPlug = "UnPlug Displays(Except EDP) before Going further";  

        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            foreach (KeyValuePair<System.Action, System.Action> _CurrentModeType in _applyMode)
            {
                //Step - 1
                _CurrentModeType.Key();

                //Step - 2
                Log.Message(true, "Verify LPSP Register");
                _CurrentModeType.Value();

                //Step - 3
                Log.Message(true, "Semi Automated Action");                
                PromptMessage(_PromptMessage_Plug);

                if (null != _PowerAction)
                    _PowerAction();

                //Step - 4
                Log.Message(true, "Displays Enmurated After Hotplug");
                List<DisplayInfo> enumeratedDisplays = AccessInterface.GetFeature<List<DisplayInfo>>(Features.DisplayEnumeration, Action.GetAll);
                List<DisplayType> displays = CurrentConfig.CustomDisplayList.ToList();

                if (enumeratedDisplays.Count < CurrentConfig.ConfigTypeCount)
                    Log.Abort("Plug all displays planned as configuration");

                Log.Message("Checking Displays after Plug");
                enumeratedDisplays.ForEach(dp =>
                    {
                        Log.Message(dp.ToString());
                        displays.Remove(dp.DisplayType);
                    });

                if (displays.Count > 0)
                {
                    Log.Abort("Plug all displays planned as configuration");
                }

                Log.Success("Displays Plugged as per Configuration");

                //Step - 5
                //Adding SD - EDP Config check because After hotplug display config behaviour is not fix
                DisplayConfig hotplugConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);

                Log.Message(true, "Verfiy LPSP Register");
                Log.Message("Configuration After Hotplug : {0}", hotplugConfig.GetCurrentConfigStr());
                if (hotplugConfig.ConfigType == DisplayConfigType.SD && hotplugConfig.PrimaryDisplay == DisplayType.EDP)
                    _CurrentModeType.Value();
                else
                    LPSPRegisterVerify(false);

                //Step - 6
                Log.Message(true, "Semi Automated Action");                
                PromptMessage(_PromptMessage_UnPlug);

                if (null != _PowerAction)
                    _PowerAction();

                //Step - 7
                Log.Message(true, "Checking Displays After HotUnplug");
                enumeratedDisplays = AccessInterface.GetFeature<List<DisplayInfo>>(Features.DisplayEnumeration, Action.GetAll);

                if (enumeratedDisplays.Count != 1 || enumeratedDisplays.ElementAt(0).DisplayType != DisplayType.EDP)
                    Log.Abort("UnPlug all displays except EDP");

                Log.Message("Enumerated Displays after Unplug");
                enumeratedDisplays.ForEach(dp =>
                {
                    Log.Message(dp.ToString());
                });

                Log.Success("Displays Unplugged ");

                //Step - 8
                //Adding SD - EDP Config check because After hotUnplug display config behaviour is not fix
                hotplugConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);

                Log.Message(true, "Verfiy LPSP Register");
                Log.Message("Configuration After HotUnplug : {0}", hotplugConfig.GetCurrentConfigStr());
                if (hotplugConfig.ConfigType == DisplayConfigType.SD && hotplugConfig.PrimaryDisplay == DisplayType.EDP)
                    _CurrentModeType.Value();
                else
                    LPSPRegisterVerify(false);
            }
        }

        protected void PromptMessage(String pMessage)
        {
            if (!AccessInterface.SetFeature<bool, String>(Features.PromptMessage, Action.SetMethod, pMessage))
                Log.Abort("User rejected Semi Automated Request");
        }

        protected void PowerEventAction()
        {
            Log.Message("Putting the system into {0} state", _PowerStates);
            PowerParams powerParams = new PowerParams();
            powerParams.Delay = 30;
            base.InvokePowerEvent(powerParams, _PowerStates);
            Log.Success("Put the system into {0} state & resumed", _PowerStates);
        }
 
    }
}