namespace Intel.VPG.Display.Automation
{
    [Test(Type = TestType.HasPlugUnPlug)]
    class SB_ULT_Hotplug_In_S4 : SB_ULT_Hotplug_In_S3
    {
        public SB_ULT_Hotplug_In_S4()
        {
            _PowerState = PowerStates.S4;
        }
    }
}
