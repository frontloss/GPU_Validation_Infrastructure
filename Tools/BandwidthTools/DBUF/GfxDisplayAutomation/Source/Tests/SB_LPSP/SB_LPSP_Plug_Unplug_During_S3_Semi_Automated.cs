namespace Intel.VPG.Display.Automation
{
    class SB_LPSP_Plug_Unplug_During_S3_Semi_Automated : SB_LPSP_Plug_Unplug_Semi_Automated  
    {                
        public SB_LPSP_Plug_Unplug_During_S3_Semi_Automated()
        {
            _PowerStates = PowerStates.S3;
            _PowerAction = PowerEventAction;
            _PromptMessage_Plug = "Plug Displays as per Configuration during S3 state";
            _PromptMessage_UnPlug = "UnPlug Displays(Except EDP) during S3 state"; 
        }
    }
}