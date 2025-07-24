namespace Intel.VPG.Display.Automation
{
    class SB_LPSP_Plug_Unplug_During_CS_Semi_Automated : SB_LPSP_Plug_Unplug_Semi_Automated  
    {        
        public SB_LPSP_Plug_Unplug_During_CS_Semi_Automated()
        {
            _PowerStates = PowerStates.CS;
            _PowerAction = PowerEventAction;
            _PromptMessage_Plug = "Plug Displays as per Configuration during CS state";
            _PromptMessage_UnPlug = "UnPlug Displays(Except EDP) during CS state"; 
        }       
    }
}