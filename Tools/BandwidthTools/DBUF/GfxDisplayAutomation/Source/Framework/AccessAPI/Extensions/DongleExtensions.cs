namespace Intel.VPG.Display.Automation
{
    internal class DongleExtensions : FunctionalBase
    {
        const uint IGFX_I2C_AUX_READ = 9;
        const uint IGFX_I2C_AUX_WRITE = 8;
        const uint IGFX_INVALID_AUX_DEVICE = 0x0043;
        const uint IGFX_INVALID_AUX_ADDRESS = 0x0044;
        const uint IGFX_INVALID_AUX_DATA_SIZE = 0x0045;
        const uint IGFX_AUX_DEFER = 0x0046;
        const uint IGFX_AUX_TIMEOUT = 0x0047;

        const uint DPCD_BUFFER_SIZE = 0x0008;
        const uint REG_ADDR_DONGLE = 0x00007;
        const uint REG_ADDR_DOWN_STR_TYPE = 0x00080;
        const uint VGA_DONGLE_REG_VALUE = 0x09;
        const uint DPCD_DONGLE_REG_VALUE = 129;
        const uint HDMI_ACTIVE_DONGLE_REG_VALUE = 0x0B;
        const uint VGA_ACTIVE_DONGLE_REG_VALUE = 0x09;

        internal void GetDongleData(DisplayInfo displayInfo)
        {
            DongleType dongleType = DongleType.None;
            if (GetDPCDData(displayInfo, REG_ADDR_DONGLE, out dongleType) == DPCD_DONGLE_REG_VALUE)
            {
                DisplayType downStreamType = GetDownStreamPort(displayInfo);
                displayInfo.dongle.Type = dongleType;
                displayInfo.dongle.DownStreamType = downStreamType;
            }
        }

        private uint GetDPCDData(DisplayInfo Displays, uint address, out DongleType argDongleType)
        {
            DpcdRegister dpcdRead = base.CreateInstance<DpcdRegister>(new DpcdRegister());
            DpcdInfo dpcd = new DpcdInfo();
            dpcd.Offset = address; //DPCD_EDP_REV_ADDR
            dpcd.DispInfo = Displays;
            argDongleType = DongleType.None;

            dpcdRead.GetMethod(dpcd);
            if (dpcd.Value != 0)
            {
                argDongleType = DongleType.Active;
                return dpcd.Value;
            }
            return 0;
        }
        private DisplayType GetDownStreamPort(DisplayInfo Displays)
        {
            DongleType dongleType = DongleType.None;
            uint value = GetDPCDData(Displays, REG_ADDR_DONGLE, out dongleType);
            switch (value)
            {
                case HDMI_ACTIVE_DONGLE_REG_VALUE:
                    Log.Verbose("Dongle Down Stream type is HDMI.");
                    return DisplayType.HDMI;
                case VGA_ACTIVE_DONGLE_REG_VALUE:
                    Log.Verbose("Dongle Down Stream type is CRT.");
                    return DisplayType.CRT;
                default:
                    return DisplayType.None;
            }
        }
    }
}
