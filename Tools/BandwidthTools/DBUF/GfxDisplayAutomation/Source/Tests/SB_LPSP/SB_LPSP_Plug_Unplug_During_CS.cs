namespace Intel.VPG.Display.Automation
{    
    [Test(Type = TestType.HasPlugUnPlug)]
    class SB_LPSP_Plug_Unplug_During_CS : SB_LPSP_Plug_Unplug  
    {
        public SB_LPSP_Plug_Unplug_During_CS()
        {
            _isLowPowerState = true;
            _PowerEventAction = this.PowerEventAction;
            _PowerStates = PowerStates.CS;
        }
   }
}