namespace Intel.VPG.Display.Automation
{
    [Test(Type = TestType.HasPlugUnPlug)]
    class MP_Audio_Multi_Source_HP_S3 : MP_Audio_Single_Source_HP_CS
    {
        public MP_Audio_Multi_Source_HP_S3()
        {
            _audioInputSource = AudioInputSource.Multiple;
            powerParams = new PowerParams() { Delay = 45, };
            powerParams.PowerStates =  PowerStates.S3;
            IsNonCSTest = true;
        }
        [Test(Type = TestType.Method, Order = 2)]
        public override void GotoLPStateNResume()
        {

            Log.Message(true, "Going {0} state and Resume the system from {1} after {2} seconds", powerParams.PowerStates, powerParams.PowerStates, powerParams.Delay);
            base.EventResult(powerParams.PowerStates, base.InvokePowerEvent(powerParams, powerParams.PowerStates));
        }
    }
}
