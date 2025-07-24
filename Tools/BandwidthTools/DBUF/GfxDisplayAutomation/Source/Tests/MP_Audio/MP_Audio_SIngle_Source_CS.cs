namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;
    using System.IO;
    using System.Linq;
    class MP_Audio_Single_Source_CS : MP_Audio_Base
    {
        protected CSParam powerParam = new CSParam();
        [Test(Type = TestType.Method, Order = 1)]
        public void PreCondition()
        {
            if (base.CurrentConfig.DisplayList.Count < 2)
                Log.Abort("Minimum two display required to run the test");
            else
            {
                Log.Message(true, "Boot the system with one display 1 connected");
                if (!DisplayExtensions.VerifyCSSystem(base.MachineInfo))
                {
                    Log.Abort("Setup is not CS enabled");
                }
            }
        }

        [Test(Type = TestType.Method, Order = 2)]
        public void SetConfigMethod()
        {
            Log.Message(true, "Set Current config via OS call");
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig))
                Log.Success("Config applied successfully");
            else
            {
                Log.Abort("Config not applied!");
            }
        }

        [Test(Type = TestType.Method, Order = 3)]
        public void SetAudioSourceNVerify()
        {
            base.SetAudioSource();
        }

        [Test(Type = TestType.Method, Order = 4)]
        public void GetAudioEndpoint()
        {
            //Log.Message(true, "Check Audio endpoint and verify AUD_PIN_ELD_CP_VLD Register");
            base.CheckAudioEndPoint(AccessInterface.GetFeature<AudioDataProvider>(Features.AudioEnumeration, Action.GetAll, Source.AccessAPI));
        }

        [Test(Type = TestType.Method, Order = 5)]
        public void GotopowerState()
        {
            
            bool SeqCheck = false;
            int Current_Config = base.Get_current_Config();
            SeqCheck = base.IsPDBpresent();
            if (true == SeqCheck)
                base.StartLog();

            Log.Message(true, "Goto CS and resume");
            Log.Message("Going CS state and Resume the system from CS after {0} seconds", powerParam.Delay);
            AccessInterface.SetFeature<bool, CSParam>(Features.ConnectedStandby, Action.SetMethod, powerParam);
            DisplayConfig osConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get, Source.AccessAPI);
            Log.Verbose("Current display config is {0} ", osConfig.GetCurrentConfigStr());
            Log.Success("Successfully resume from CS after {0} sec", powerParam.Delay);
            GetAudioEndpoint();

            if (true == SeqCheck)
            {
                base.StopLog();
                if (PWR_Status.No_PWR_Change == base.VerifyPWRSequence())
                    Log.Fail("No PWR sequence followed");
                else
                {
                    if ((PWR_Off != 1) && (PWR_On != 1))
                        Log.Fail("PWR Sequence wrongly happened");

                    Log.Success("PWR Sequence happened correctly");
                }
                base.VerifyAUDseq_PWREvent(Current_Config);
            }
        }
    }
}
