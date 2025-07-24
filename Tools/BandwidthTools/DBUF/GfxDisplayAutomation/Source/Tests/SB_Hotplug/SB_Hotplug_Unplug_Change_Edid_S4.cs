namespace Intel.VPG.Display.Automation
{
    [Test(Type = TestType.HasPlugUnPlug)]
    class SB_Hotplug_Unplug_Change_Edid_S4 : SB_Hotplug_Unplug_Change_Edid_S3
    {
        public SB_Hotplug_Unplug_Change_Edid_S4()
        {
            _PowerState = PowerStates.S4;
        }
    }
}
