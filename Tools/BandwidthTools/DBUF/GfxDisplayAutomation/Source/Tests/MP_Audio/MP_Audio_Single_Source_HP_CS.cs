namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;
    using System.Linq;

    [Test(Type = TestType.HasPlugUnPlug)]
    class MP_Audio_Single_Source_HP_CS : MP_Audio_Base
    {
        protected CSParam csPowerParam;
        protected PowerParams powerParams;
        protected bool IsNonCSTest;
        public MP_Audio_Single_Source_HP_CS()
        {
            csPowerParam = new CSParam();
        }
        
        [Test(Type = TestType.Method, Order = 1)]
        public void PreCondition()
        {
            if (base.CurrentConfig.DisplayList.Count < 2)
                Log.Abort("Minimum two display required to run the test");
            else
            {
                Log.Message(true, "Boot the system with one display 1 connected");
                if (!DisplayExtensions.VerifyCSSystem(base.MachineInfo) && IsNonCSTest == false)
                {
                    Log.Abort("Setup is not CS enabled");
                }
            }
        }

        [Test(Type = TestType.Method, Order = 2)]
        public virtual void GotoLPStateNResume()
        {
            bool SeqCheck = false;
            SeqCheck = base.IsPDBpresent();
            if (true == SeqCheck)
                base.StartLog();

            Log.Message(true, "Going CS state and Resume the system from CS after {0} seconds", csPowerParam.Delay);
            AccessInterface.SetFeature<bool, CSParam>(Features.ConnectedStandby, Action.SetMethod, csPowerParam);
            DisplayConfig osConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get, Source.AccessAPI);
            Log.Verbose("Current display config is {0} ", osConfig.GetCurrentConfigStr());
            Log.Success("Successfully resue from CS after {0} sec", csPowerParam.Delay);
            if (true == SeqCheck)
            {
                base.StopLog();
                base.VerifyPWRSequence();
            }

        }

        [Test(Type = TestType.Method, Order = 3)]
        public void HotPlugNValidateEndpoint()
        {
            bool SeqCheck = false;
            int ExtDisp = 0;
            PWR_Status pwr_status = PWR_Status.No_PWR_Change;

            SeqCheck = base.IsPDBpresent();
            int Current_Config = base.Get_current_Config();

            Log.Message( "Hotplug all external displays and verify audio endpoint");
            foreach (DisplayType DT in base.CurrentConfig.PluggableDisplayList)
            {
                ExtDisp = base.Get_current_Config();
                if (SeqCheck)
                    base.StartLog();

                Log.Message(true, "{0} is not enumerated..Plugging it", DT);
                Log.Message("{0} is not enumerated..Plugging it", DT);
                if (base.HotPlug(DT))
                {
                    Log.Success("Display {0} is plugged successfully", DT);

                }
                else
                    Log.Fail("Unable to hotplug display {0}", DT);
            }

            if (base.CurrentConfig.EnumeratedDisplays.Count == base.CurrentConfig.DisplayList.Count)
            {
                SetConfigMethod();
                base.CheckAudioEndPoint(AccessInterface.GetFeature<AudioDataProvider>(Features.AudioEnumeration, Action.GetAll, Source.AccessAPI));
                if (SeqCheck)
                {
                    base.StopLog();
                    base.VerifyAUDseq_Plug();
                    pwr_status = base.VerifyPWRSequence();

                    if ((((ExtDisp == 0) && (pwr_status != PWR_Status.No_PWR_Change))) || (((ExtDisp != 0) && (pwr_status == PWR_Status.No_PWR_Change))))
                        Log.Success("PowerWell Sequence is correct");
                    else
                        Log.Fail("PWR sequence is incorrect ");

                    ExtDisp = base.Get_current_Config();

                }

            }
            else
                Log.Abort("Unable to plug all external display to run the test");
            
        }

        [Test(Type = TestType.Method, Order = 4)]
        public void SelectAudioSource()
        {
            Log.Message(true, "select audio source through CUI audio page");
            base.SetAudioSource();
        }

        [Test(Type = TestType.Method, Order = 5)]
        public void HotUnpluginLowpowerState()
        {
            Log.Message(true, "Hot unplug all external display in low power state");
            foreach (DisplayType unPDT in DisplayExtensions.pluggedDisplayList.Reverse<DisplayType>())
            {
                base.HotUnPlug(unPDT, true);
                GotoLPStateNResume();
                if (base.EnumeratedDisplays.Select(DT => DT.DisplayType == unPDT).FirstOrDefault())
                {
                    Log.Fail("Unable to hot unplug display {0}", base.CurrentConfig.PluggableDisplayList.First());
                }
                else
                {
                    Log.Success("Successfully hot unplug display {0}", base.CurrentConfig.PluggableDisplayList.First());
                }
                base.CheckAudioEndPoint(AccessInterface.GetFeature<AudioDataProvider>(Features.AudioEnumeration, Action.GetAll, Source.AccessAPI));
                Log.Verbose("Default audio endpoint device {0}", base.GetDefaultEndPoint().FriendlyName);
                if (base.HotPlug(unPDT))
                {
                    Log.Success("Successfully hot plug display {0}", unPDT);
                }
                else
                    Log.Fail("Unable to hot plug display {0}", unPDT);
                base.CheckAudioEndPoint(AccessInterface.GetFeature<AudioDataProvider>(Features.AudioEnumeration, Action.GetAll, Source.AccessAPI));
                Log.Verbose("Default audio endpoint device {0}", base.GetDefaultEndPoint().FriendlyName);
            }
        }

        private void SetConfigMethod()
        {
            Log.Message(true, "Set Current config via OS call");
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig))
                Log.Success("Config applied successfully");
            else
            {
                Log.Abort("Config not applied!");
            }
        }

    }
}
