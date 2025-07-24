namespace Intel.VPG.Display.Automation
{
    [Test(Type = TestType.HasPlugUnPlug)]
    class SB_HotUnplug_In_S4 : SB_HotUnplug_In_S3
    {
        public SB_HotUnplug_In_S4()
        {
            _PowerState = PowerStates.S4;
        }
    }
}
