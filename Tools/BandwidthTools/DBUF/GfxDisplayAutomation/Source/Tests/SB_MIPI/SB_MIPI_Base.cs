namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    using System.Collections.Generic;
    
    using System;
    using System.IO;
    using System.Threading;
    using System.Diagnostics;

    class SB_MIPI_Base : TestBase
    {
        const int vbtHeaderSize = 48;
        const int VBT_BIOS_DATA_HEADER_size = 22;
        const UInt32 Block_52 = 52;
        const UInt32 Block_40 = 40;
        List<UInt32> vbtData = new List<uint>();
        Process procNaakuthanthi;

        protected const string DPI_HACTIVE = "DPI_HACTIVE";
        protected const string DPI_VACTIVE = "DPI_VACTIVE";
        protected const string MIPI_DUAL_LINK_MODE = "MIPI_DUAL_LINK_MODE";
        protected const string MIPI_DITHERING_STATUS = "MIPI_DITHERING_STATUS";
        protected const string MIPI_DATA_LANES = "MIPI_DATA_LANES";
        protected const string MIPI_PIXEL_OVERLAP_COUNT = "MIPI_PIXEL_OVERLAP_COUNT";
        protected const string BurstMode = "BurstMode";
        protected const string MIPI_ColorFormat_RGB565 = "MIPI_ColorFormat_RGB565";

        protected const string MIPI_DSI_Resolution = "MIPI_DSI_Resolution";
        protected const string MIPI_HORIZ_SYNC_PADDING_COUNT = "MIPI_HORIZ_SYNC_PADDING_COUNT";
        protected const string MIPI_HORIZ_BACK_PORCH_COUNT = "MIPI_HORIZ_BACK_PORCH_COUNT";
        protected const string MIPI_HORIZ_FRONT_PORCH_COUNT = "MIPI_HORIZ_FRONT_PORCH_COUNT";
        protected const string MIPI_HORIZ_ACTIVE_AREA_COUNT = "MIPI_HORIZ_ACTIVE_AREA_COUNT";
        protected const string MIPI_VERT_SYNC_PADDING_COUNT = "MIPI_VERT_SYNC_PADDING_COUNT";
        protected const string MIPI_VERT_BACK_PORCH_COUNT = "MIPI_VERT_BACK_PORCH_COUNT";
        protected const string MIPI_VERT_FRONT_PORCH_COUNT = "MIPI_VERT_FRONT_PORCH_COUNT";
        protected const string MIPI_HIGH_LOW_SWITCH_COUNT = "MIPI_HIGH_LOW_SWITCH_COUNT";
        protected const string MIPI_Data_Width_CMD_Mode = "MIPI_Data_Width_CMD_Mode";
        protected const string MIPI_INTR_STAT_REG = "MIPI_INTR_STAT_REG";
        protected const string MIPI_GEN_FIFO_STAT_REGISTER = "MIPI_GEN_FIFO_STAT_REGISTER";



        protected const string MIPI_DPHY_PARAM_REG = "MIPI_DPHY_PARAM_REG";
        protected const string MIPI_DEVICE_RESET_TIMER = "MIPI_DEVICE_RESET_TIMER";
        protected const string MIPI_TURN_AROUND_TIMEOUT_REG = "MIPI_TURN_AROUND_TIMEOUT_REG";
        protected const string MIPI_Disable_Video_BTA = "MIPI_Disable_Video_BTA";
        protected const string MIPI_HS_TX_TIMEOUT_REG = "MIPI_HS_TX_TIMEOUT_REG";
        protected const string MIPI_LP_RX_TIMEOUT_REG = "MIPI_LP_RX_TIMEOUT_REG";
        protected const string MIPI_EOT_DISABLE_REGISTER = "MIPI_EOT_DISABLE_REGISTER";

        public enum Packet_Sequence_Video_Mode
        {
            Packet_Sequence_None,
            NonBurst_Sync_Pulse = 1,
            NonBurst_Sync_Events = 2,
            BurstMode = 3
        }
        public enum Color_Format_Video_Mode
        {
            MIPI_ColorFormat_Not_Supported,
            MIPI_ColorFormat_RGB565=1,
            MIPI_ColorFormat_RGB666=2,
            MIPI_ColorFormat_RGB666_Loosely_Packed=3,
            MIPI_ColorFormat_RGB888=4
        }

        public enum Dual_Link_Mode
        {
            Dual_Link_not_supported=0,
            Dual_Link_Front_Back_Mode=1,
            Dual_Link_Pixel_Alternative_Mode=2,
            Reserved
        }

        protected List<DisplayMode> GetModesForTest(DisplayType pDisplayType)
        {
            List<DisplayType> displays = new List<DisplayType>();
            displays.Add(pDisplayType);
            List<DisplayModeList> displayModeList_OSPage = AccessInterface.GetFeature<List<DisplayModeList>, List<DisplayType>>(Features.Modes, Action.GetAllMethod, Source.AccessAPI, displays);
            List<DisplayMode> dispModes = displayModeList_OSPage.Where(dML => dML.display == pDisplayType).Select(dML => dML.supportedModes).FirstOrDefault();
            return dispModes;
        }
        protected void ApplyNativeMode(DisplayType display)
        {
            Log.Message(true, "Applying Native Mode");

            // Finding Native Mode
            List<DisplayMode> displayModes = GetModesForTest(display);

            if (AccessInterface.SetFeature<bool, DisplayMode>(Features.Modes, Action.SetMethod, displayModes.Last()))
                Log.Success("Native Mode Applied");
            else
                Log.Fail("Failed to apply Native Mode");
        }

        protected void ApplyNonNativeMode(DisplayType display)
        {
            Log.Message(true, "Applying Non-Native Mode");

            // Finding Native Mode
            List<DisplayMode> displayModes = GetModesForTest(display);

            if (AccessInterface.SetFeature<bool, DisplayMode>(Features.Modes, Action.SetMethod, displayModes.First()))
                Log.Success("Non - Native Mode Applied");
            else
                Log.Fail("Failed to apply Non - Native Mode");
        }

        private List<UInt32> GetVBTData()
        {
            string vbtFilepath = string.Concat(base.ApplicationManager.ApplicationSettings.ULTDumpFiles, "\\vbt_mipi.bin");
            Log.Message(vbtFilepath);
            vbtData = File.ReadAllBytes(vbtFilepath).Select((b) => (UInt32)b).ToList();
           
            //if (vbtData.Count == 0)
            //{
            //    DriverEscapeData<List<uint>, List<uint>> driverData = new DriverEscapeData<List<uint>, List<uint>>();
            //    driverData.input = new List<uint>();
            //    driverData.output = new List<uint>();

            //    DriverEscapeParams driverParams = new DriverEscapeParams(DriverEscapeType.VBTByteRead, driverData);
            //    if (!AccessInterface.SetFeature<bool, DriverEscapeParams>(Features.DriverEscape, Action.SetMethod, driverParams))
            //        Log.Abort("Failed to read Register with offset as {0}", driverData.input);
            //    else
            //    {
            //        vbtData = driverData.output;
            //    }
            //}
            return vbtData;
        }
        protected Packet_Sequence_Video_Mode GetPacketSequence()
        {
            uint GeneralMipiParams = GetMIPIConfigByteData();
            Packet_Sequence_Video_Mode packetSequence = Packet_Sequence_Video_Mode.Packet_Sequence_None;

            uint packetSequenceValue = GetRegisterValue(GeneralMipiParams, 6, 7);

            packetSequence = (Packet_Sequence_Video_Mode)Enum.Parse(typeof(Packet_Sequence_Video_Mode), packetSequenceValue.ToString());

            return packetSequence;
        }

        protected Color_Format_Video_Mode GetMIPIColorFormat()
        {
            uint GeneralMipiParams = GetMIPIConfigByteData();
            Color_Format_Video_Mode packetSequence = Color_Format_Video_Mode.MIPI_ColorFormat_Not_Supported;

            uint colorFormatValue = GetRegisterValue(GeneralMipiParams, 10, 13);

            packetSequence = (Color_Format_Video_Mode)Enum.Parse(typeof(Color_Format_Video_Mode), colorFormatValue.ToString());

            return packetSequence;
        }

        protected uint GetMIPIDualLinkPixelOverlap()
        {
            uint PortDescData = GetMIPIPortDesc();

            uint pixelOverlap = GetRegisterValue(PortDescData, 4, 6);

            return pixelOverlap;
        }

        protected uint GetNoOfLanes()
        {
            uint PortDescData = GetMIPIPortDesc();

            uint lanes = GetRegisterValue(PortDescData, 2, 3) + 1;

            return lanes;
        }

        protected Dual_Link_Mode GetMIPIDualLinkMode()
        {
            Dual_Link_Mode dualLinkMode = Dual_Link_Mode.Reserved;

             uint PortDescData = GetMIPIPortDesc();

            uint dualLinkModeData = GetRegisterValue(PortDescData, 0, 1);

            dualLinkMode = (Dual_Link_Mode)Enum.Parse(typeof(Dual_Link_Mode), dualLinkModeData.ToString());
            
            Log.Message("Current Link Mode from VBT is: {0}.", dualLinkMode);

            return dualLinkMode;
        }

        private uint GetMIPIConfigByteData()
        {
            List<UInt32> VBTData = GetVBTData();
            int currentByte = vbtHeaderSize + VBT_BIOS_DATA_HEADER_size;

            while (Block_40 != VBTData[currentByte])
            {
                uint hdd = VBTData[currentByte + 1] | VBTData[currentByte + 2] << 8;
                currentByte = currentByte + (int)hdd + 3;

                uint bbb = VBTData[currentByte];
            }

            int panelType =(int) VBTData[currentByte + 3];

            while (Block_52 != VBTData[currentByte])
            {
                uint hdd = VBTData[currentByte + 1] | VBTData[currentByte + 2] << 8;
                currentByte = currentByte + (int)hdd + 3;

                uint bbb = VBTData[currentByte];
            }

            int mipiConfig = currentByte + 3;

            int panelIdentifier = mipiConfig + panelType * 122 ;
            int ColorFormatByte = mipiConfig + 2;

            uint GeneralMipiParams = VBTData[ColorFormatByte] | VBTData[ColorFormatByte + 1] << 8;

            return GeneralMipiParams;
        }

        private uint GetMIPIPortDesc()
        {
            List<UInt32> VBTData = GetVBTData();
            int currentByte = vbtHeaderSize + VBT_BIOS_DATA_HEADER_size;
            
            while (Block_40 != VBTData[currentByte])
            {
                uint hdd = VBTData[currentByte + 1] | VBTData[currentByte + 2] << 8;
                currentByte = currentByte + (int)hdd + 3;

                uint bbb = VBTData[currentByte];
            }

            int panelType = (int)VBTData[currentByte + 3];

            while (Block_52 != VBTData[currentByte])
            {
                uint hdd = VBTData[currentByte + 1] | VBTData[currentByte + 2] << 8;
                currentByte = currentByte + (int)hdd + 3;

                uint bbb = VBTData[currentByte];
            }

            int portDescIndex = currentByte + 3 + panelType * 122 + 2 + 4;

            uint PortDescParams = VBTData[portDescIndex] | VBTData[portDescIndex + 1] << 8;

            return PortDescParams;
        }
        public uint GetRegisterValue(uint RegisterValue, int start, int end)
        {
            uint value = RegisterValue << (31 - end);
            value >>= (31 - end + start);
            return value;
        }

        public bool IsMipiVideoModePanel(PORT port)
        {
            bool IsVideoMode = VerifyRegisters("MIPI_VIDEO_MODE", PIPE.NONE, PLANE.NONE, port, false);
            
            return IsVideoMode;
        }

        public bool IsMipiDualLinkPanel(DisplayType display)
        {
            DisplayInfo displayInfo = this.CurrentConfig.EnumeratedDisplays.Find(dispInfo => dispInfo.DisplayType == display);
            return VerifyRegisters(MIPI_DUAL_LINK_MODE, PIPE.NONE, PLANE.NONE, displayInfo.Port, false);
        }

        public void StartMouseMovement()
        {
            string PSR_UTILITY_APP = "Naakuthanthi.exe";
            string args = "c:draw e:pixelpath w:300 h:300";

            procNaakuthanthi = new Process();
            procNaakuthanthi.StartInfo.UseShellExecute = false;
            procNaakuthanthi.StartInfo.CreateNoWindow = false;
            procNaakuthanthi.StartInfo.FileName = PSR_UTILITY_APP;
            procNaakuthanthi.StartInfo.Arguments = args;

            procNaakuthanthi.Start();
            Thread.Sleep(2000);
        }

        public void StopMouseMovement()
        {
            if (!procNaakuthanthi.HasExited)
                procNaakuthanthi.Kill();
        }
    }
}