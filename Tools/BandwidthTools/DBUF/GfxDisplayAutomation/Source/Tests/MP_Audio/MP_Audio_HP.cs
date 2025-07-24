namespace Intel.VPG.Display.Automation
{
    using System.IO;
    using System.Linq;

    [Test(Type = TestType.HasPlugUnPlug)]
    class MP_Audio_HP : MP_Audio_Base
    {
        [Test(Type = TestType.Method, Order = 1)]
        public void PreCondition()
        {
            if (base.CurrentConfig.DisplayList.Count < 2)
                Log.Abort("Minimum two display required to run the test");
        }

        [Test(Type = TestType.Method, Order = 2)]
        public void HotPlugUnPlugNValidateEndpoint()
        {
            bool SeqCheck = false;
            SeqCheck = base.IsPDBpresent();
            PWR_Status pwr_status = PWR_Status.No_PWR_Change;

            foreach (DisplayType DT in base.CurrentConfig.PluggableDisplayList)
            {
                int ExtDisp = 0;

               ExtDisp= base.Get_current_Config();
                if (SeqCheck)
                    base.StartLog();


                Log.Message("{0} is not enumerated..Plugging it", DT);
                if (base.HotPlug(DT))
                {
                    Log.Message(true,"Hot Plug Display {0} ", DT);
                    Log.Success("Display {0} is plugged successfully", DT);
                   
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

                        ExtDisp= base.Get_current_Config();
                        base.StartLog();

                    }
                   
                    if (base.HotUnPlug(DT))
                    {
                        Log.Message(true, "Hot unplug display {0}", DT);
                        Log.Success("Successfully able to hot unplug display {0}", DT);
                        base.CheckAudioEndPoint(AccessInterface.GetFeature<AudioDataProvider>(Features.AudioEnumeration, Action.GetAll, Source.AccessAPI));

                        if (true == SeqCheck)
                        {
                            base.StopLog();
                            base.VerifyAUDseq_UnPlug();
                            pwr_status = base.VerifyPWRSequence();
                            if ((((ExtDisp == 1) && (pwr_status != PWR_Status.No_PWR_Change))) || (((ExtDisp > 1) && (pwr_status == PWR_Status.No_PWR_Change))))
                                Log.Success("PowerWell Sequence is correct");
                            else
                                Log.Fail("PWR sequence is incorrect ");
                        }
                    }
                    else
                        Log.Fail("Unable to hot unplug display {0}", DT);
                }
                else
                    Log.Fail("Unable to hot plug display {0}", DT);
            }
        }
    }
}
