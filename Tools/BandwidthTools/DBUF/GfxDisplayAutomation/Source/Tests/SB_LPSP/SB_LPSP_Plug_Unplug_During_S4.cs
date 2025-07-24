namespace Intel.VPG.Display.Automation
{
    [Test(Type = TestType.HasPlugUnPlug)]
    class SB_LPSP_Plug_Unplug_During_S4 : SB_LPSP_Plug_Unplug_During_S3 
    {
        public SB_LPSP_Plug_Unplug_During_S4()
        {
            _isLowPowerState = true;
            _PowerEventAction = this.PowerEventAction;
            _PowerStates = PowerStates.S4;
        }
    }
}