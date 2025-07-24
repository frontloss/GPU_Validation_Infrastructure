namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;
    using System.Linq;

    [Test(Type = TestType.HasPlugUnPlug)]
    class MP_Audio_LPSP_HP_S4 : MP_Audio_Base
    {
        protected PowerStates powerstate;
        public MP_Audio_LPSP_HP_S4()
        {
            powerstate = PowerStates.S4;
        }

        [Test(Type = TestType.Method, Order = 1)]
        public void PreCondition()
        {
            if (base.CurrentConfig.DisplayList.Count < 2)
                Log.Abort("Minimum two display required to run the test");
        }

        [Test(Type = TestType.Method, Order = 2)]
        public void CheckAudioEndPoint()
        {
            DisplayConfig displayConfig = new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.GetInternalDisplay() };
            Log.Message("Set the initial configuration as SD {0}", displayConfig.PrimaryDisplay);
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, displayConfig))
                Log.Success("Config applied successfully");
            else
                Log.Abort("Unable to set display config");

            base.LPSPRegisterVerify(base.GetLPSPEnableStatus());
            base.CheckAudioEndPoint(AccessInterface.GetFeature<AudioDataProvider>(Features.AudioEnumeration, Action.GetAll, Source.AccessAPI));
        }

        [Test(Type = TestType.Method, Order = 2)]
        public void HotPlugUnPlugNValidateEndpoint()
        {
            foreach (DisplayType DT in base.CurrentConfig.PluggableDisplayList.Reverse<DisplayType>())
            {
                if (base.HotPlug(DT))
                {
                    Log.Success("Successfully able to hotplug display {0}", DT);
                    base.LPSPRegisterVerify(base.GetLPSPEnableStatus());
                    base.CheckAudioEndPoint(AccessInterface.GetFeature<AudioDataProvider>(Features.AudioEnumeration, Action.GetAll, Source.AccessAPI));
                    List<DisplayInfo> enumDisplayBeforeHUP = base.CurrentConfig.EnumeratedDisplays;
                    base.HotUnPlug(DT, true);
                    GotopowerState();
                    List<DisplayInfo> currentEnumDisplay = base.CurrentConfig.EnumeratedDisplays;
                    if (currentEnumDisplay.Select(DTP => DTP.DisplayType == DT).FirstOrDefault() &&
                        (enumDisplayBeforeHUP.Count == currentEnumDisplay.Count))
                        Log.Fail("Unable to hot unplug display {0} in low power state", DT);
                    else
                    {
                        Log.Success("Successfully hot unplug display {0} in low power state", DT);
                    }
                    base.LPSPRegisterVerify(base.GetLPSPEnableStatus());
                    base.CheckAudioEndPoint(AccessInterface.GetFeature<AudioDataProvider>(Features.AudioEnumeration, Action.GetAll, Source.AccessAPI));

                }
                else
                    Log.Fail("Unable to hot plug display {0}", DT);
            }
        }

        private void GotopowerState()
        {
            Log.Message(true, "Put the system into {0} state & resume", powerstate.ToString());
            PowerParams _powerParams = new PowerParams() { Delay = 30, };
            base.InvokePowerEvent(_powerParams, powerstate);
            Log.Verbose("Verifying audio register and endpoints are correct or not.");
        }
    }
}
