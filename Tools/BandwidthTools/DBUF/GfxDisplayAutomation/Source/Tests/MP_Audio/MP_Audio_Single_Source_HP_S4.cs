namespace Intel.VPG.Display.Automation
{
    [Test(Type = TestType.HasPlugUnPlug)]
    class MP_Audio_Single_Source_HP_S4 : MP_Audio_Single_Source_HP_S3
    {
        public MP_Audio_Single_Source_HP_S4()
        {
            powerParams.PowerStates = PowerStates.S4;
            IsNonCSTest = true;
        }
    }
}
