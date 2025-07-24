namespace Intel.VPG.Display.Automation
{
    [Test(Type = TestType.HasPlugUnPlug)]
    class SB_HotUnplug_In_S4_pri_sec_swap : SB_HotUnplug_In_S3_pri_sec_swap
    {
        public SB_HotUnplug_In_S4_pri_sec_swap()
        {
            _PowerState = PowerStates.S4;
        }
    }
}
