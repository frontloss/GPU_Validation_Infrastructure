namespace Intel.VPG.Display.Automation
{
    class SB_LPSP_AC_DC_During_S4_Semi_Automated : SB_LPSP_AC_DC_During_S3_Semi_Automated
    {
        public SB_LPSP_AC_DC_During_S4_Semi_Automated()
        {
            _PowerState = PowerStates.S4;
        }
    }
}