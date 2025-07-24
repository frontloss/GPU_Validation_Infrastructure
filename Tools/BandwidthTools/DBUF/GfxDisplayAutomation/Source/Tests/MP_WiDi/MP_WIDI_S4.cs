namespace Intel.VPG.Display.Automation
{
    [Test(Type = TestType.WiDi)]
    class MP_WIDI_S4 : MP_WIDI_S3
    {
        public MP_WIDI_S4()
        {
            _powerStateOption = PowerStates.S4;
        }
    }
}
