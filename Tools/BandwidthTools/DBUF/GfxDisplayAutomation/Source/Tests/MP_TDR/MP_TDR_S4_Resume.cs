namespace Intel.VPG.Display.Automation
{
    [Test(Type = TestType.HasReboot)]
    class MP_TDR_S4_Resume : MP_TDR_S3_Resume
    {
        public MP_TDR_S4_Resume()
            : base(PowerStates.S4)
        { }
    }
}