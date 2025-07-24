namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;
    using System.IO;
    using System.Linq;
    using System.Threading;

    class MP_Audio_S3 : MP_Audio_Base
    {
        protected PowerParams powerParams;
        public MP_Audio_S3()
        {
            powerParams = new PowerParams() { Delay = 45, };
            powerParams.PowerStates = PowerStates.S3;            
        }
        [Test(Type = TestType.Method, Order = 1)]
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

        [Test(Type = TestType.Method, Order = 2)]
        public void GetAudioEndpoint()
        {
            //Log.Message(true, "Check Audio endpoint and verify AUD_PIN_ELD_CP_VLD Register");
            base.CheckAudioEndPoint(AccessInterface.GetFeature<AudioDataProvider>(Features.AudioEnumeration, Action.GetAll, Source.AccessAPI));
        }
        [Test(Type = TestType.Method, Order = 3)]
        public void GotopowerState()
        {
            bool SeqCheck = false;
            int Current_Config = base.Get_current_Config();

            SeqCheck = base.IsPDBpresent();

            if (true == SeqCheck)
            {
                base.StartLog();
            }
            Log.Message(true, "Put the system into {0} state & resume", powerParams.PowerStates.ToString());
            base.EventResult(powerParams.PowerStates, base.InvokePowerEvent(powerParams, powerParams.PowerStates));
            Log.Verbose("Verifying audio register and endpoints are correct or not.");
            Thread.Sleep(40000);
            base.CheckAudioEndPoint(AccessInterface.GetFeature<AudioDataProvider>(Features.AudioEnumeration, Action.GetAll, Source.AccessAPI));
            if (true == SeqCheck)
            {
                base.StopLog();
                if (PWR_Status.No_PWR_Change != base.VerifyPWRSequence())
                {
                    if ((PWR_Off != 1) && (PWR_On != 1))
                        Log.Fail("Power send message is incorrect");
                    else
                        Log.Success("Power send message is correct");
                }
                base.VerifyAUDseq_PWREvent(Current_Config);
            }
        }
    }
}
