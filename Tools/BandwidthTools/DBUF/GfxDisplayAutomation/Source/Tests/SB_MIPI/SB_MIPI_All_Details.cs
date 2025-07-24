using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    class SB_MIPI_All_Details : SB_MIPI_Native_Resolution
    {
        protected override void VerifyRegisters()
        {
            DisplayType display = DisplayType.MIPI;

            DisplayInfo displayInfo = this.CurrentConfig.EnumeratedDisplays.Find(dispInfo => dispInfo.DisplayType == display);
            availablePorts.ForEach(eachPort =>
             {
                 //if (VerifyRegisters(display + "_ENABLED", PIPE.NONE, PLANE.NONE, eachPort, false))
                 //{

                     Log.Success("MIPI {0} port is enabled", eachPort);

                     //Code for Packet_Sequence_Video_Mode.            
                     GetPacket_Sequence_Video_Mode(eachPort);

                     //Code for Color_Format_Video_Mode.  
                     GetColor_Format_Video_Mode(eachPort);

                     //Code for Number_of_Lanes.     
                     GetNumber_of_Lanes(eachPort);

                     //Code for Dual_Link_Mode.  
                     GetDual_Link_Mode(eachPort);

                     //Code for DPI_Resolution
                     GetDPI_Resolution(eachPort);

                     GetDBI_FIFO_Thrtl(eachPort);
                     GetMIPI_HORIZ_SYNC_PADDING_COUNT(eachPort);
                     GetMIPI_HORIZ_BACK_PORCH_COUNT(eachPort);
                     GetMIPI_HORIZ_FRONT_PORCH_COUNT(eachPort);
                     GetMIPI_HORIZ_ACTIVE_AREA_COUNT(eachPort);
                     GetMIPI_VERT_SYNC_PADDING_COUNT(eachPort);
                     GetMIPI_VERT_BACK_PORCH_COUNT(eachPort);
                     GetMIPI_VERT_FRONT_PORCH_COUNT(eachPort);
                     GetMIPI_HIGH_LOW_SWITCH_COUNT(eachPort);
                     GetMIPI_Data_Width_CMD_Mode(eachPort);
                     GetMIPI_INTR_STAT_REG(eachPort);
                     GetMIPI_GEN_FIFO_STAT_REGISTER(eachPort);
                     GetMIPI_DPHY_PARAM_REG(eachPort);
                     GetMIPI_DEVICE_RESET_TIMER(eachPort);
                     GetMIPI_TURN_AROUND_TIMEOUT_REG(eachPort);
                     GetMIPI_Disable_Video_BTA(eachPort);
                     GetMIPI_HS_TX_TIMEOUT_REG(eachPort);
                     GetMIPI_LP_RX_TIMEOUT_REG(eachPort);
                     GetMIPI_EOT_DISABLE_REGISTER(eachPort);
                 //}
                 //else
                 //{
                 //    Log.Fail("MIPI {0} port is enabled", eachPort);
                 //}
             });
        }

        private void GetMIPI_EOT_DISABLE_REGISTER(PORT port)
        {
            uint regValue_mipi_eot_disable = GetRegisterValue(MIPI_EOT_DISABLE_REGISTER, PIPE.NONE, PLANE.NONE, port);

            if (GetRegisterValue(regValue_mipi_eot_disable, 1, 1) == 1)
                Log.Success("MIPI Clock Stop Feature = Enabled");
            else
                Log.Success("MIPI Clock Stop Feature = Disabled");

            if (GetRegisterValue(regValue_mipi_eot_disable,0, 0) == 1)
                Log.Success("MIPI EoT Packet Transmission = Disabled");
            else
                Log.Success("MIPI EoT Packet Transmission = Enabled");
        }

        private void GetMIPI_LP_RX_TIMEOUT_REG(PORT port)
        {
            uint timeout = GetRegisterValue(MIPI_LP_RX_TIMEOUT_REG, PIPE.NONE, PLANE.NONE, port);
            Log.Success("MIPI_LP_RX_TIMEOUT_REG Value - 0x{0}", timeout.ToString("X"));
        }

        private void GetMIPI_HS_TX_TIMEOUT_REG(PORT port)
        {
            Log.Success("------------  MIPI - HS TX TimeOut Counter --------------");
            uint timeout = GetRegisterValue(MIPI_HS_TX_TIMEOUT_REG, PIPE.NONE, PLANE.NONE, port);
            Log.Success("MIPI_HS_TX_TIMEOUT_REG - 0x{0}", timeout.ToString("X"));
        }

        private void GetMIPI_Disable_Video_BTA(PORT port)
        {
            if (VerifyRegisters(MIPI_TURN_AROUND_TIMEOUT_REG, PIPE.NONE, PLANE.NONE, port,false))
            {
                Log.Success("MIPI Sending Bus Turn Around(BTA) is Disabled.");
            }
            else
                Log.Success("MIPI Sending Bus Turn Around(BTA) is Enabled.");
        }

        private void GetMIPI_TURN_AROUND_TIMEOUT_REG(PORT port)
        {
            // Turn Around Timeout Register
            // Timeout value to be checked after the DSI host makes a turn around in the direction of transfers. If the timer expires the DSI Host enters stop state.
            uint regValue_mipi_turn_around_timeout = GetRegisterValue(MIPI_TURN_AROUND_TIMEOUT_REG, PIPE.NONE, PLANE.NONE, port);
            uint turn_around_timeout = GetRegisterValue(regValue_mipi_turn_around_timeout, 0, 15);
            Log.Success("MIPI -Turn Around Timeout - 0x{0}", turn_around_timeout.ToString("X"));	
        }


        private void GetMIPI_DEVICE_RESET_TIMER(PORT port)
        {
            // Device Reset Timer
            // Timeout value to be checked for device to be reset after issuing reset entry command. If the timer expires the DSI Host enters normal operation
            uint regValue_mipi_device_reset_timer = GetRegisterValue(MIPI_DEVICE_RESET_TIMER, PIPE.NONE, PLANE.NONE, port);
            uint device_reset_timer = GetRegisterValue(regValue_mipi_device_reset_timer, 0, 15);
            Log.Success("MIPI - Device Reset Timer - 0x{0}", device_reset_timer.ToString("X"));
        }

        private void GetMIPI_DPHY_PARAM_REG(PORT port)
        {
            uint regValue_mipi_d_phy_para_ctrl = GetRegisterValue(MIPI_DPHY_PARAM_REG, PIPE.NONE, PLANE.NONE, port);

            // Exit Zero Count
            // THS_0_TIM_UI_CNT and THS_EXIT_TIM_UI_CNT for dphy are programmed as exit zero count by the processor
            uint exit_zero_count = GetRegisterValue(regValue_mipi_d_phy_para_ctrl, 24, 29);

            Log.Success("MIPI - Exit Zero Count - 0x{0}", exit_zero_count.ToString("X"));

            // Trail Count
            // TCLK_POST_TIM_UI_CNT and TCLK_TRAIL_TIM_UI_CNT for dphy are programmed as trail count by the processor
            uint trail_count = GetRegisterValue(regValue_mipi_d_phy_para_ctrl, 16, 20);
            Log.Success("MIPI - Trial Count - 0x{0}", trail_count.ToString("X"));

            // CLK Zero Count
            // TCLK_0_TIM_UI_CNT for dphy is programmed as clk zero count by the processor
            uint clk_zero_count = GetRegisterValue(regValue_mipi_d_phy_para_ctrl, 8, 15);
            Log.Success("MIPI - CLK Zero Count - 0x{0}", clk_zero_count.ToString("X"));

            // Prepare Count
            // TCLK_PREP_TIM_UI_CNT and THS_PREP_TIM_UI_CNT for dphy are programmed as prepare count by the processor
            uint prepare_count = GetRegisterValue(regValue_mipi_d_phy_para_ctrl, 0, 5);
            Log.Success("MIPI - Prepare Count -  0x{0}", prepare_count.ToString("X"));
        }

        private uint GetBitValue(uint val, int index)
        {
            return GetRegisterValue(val, index, index);
        }

        private void GetMIPI_GEN_FIFO_STAT_REGISTER(PORT port)
        {
            uint regValue_mipi_gen_fifo_stat_reg = GetRegisterValue(MIPI_GEN_FIFO_STAT_REGISTER, PIPE.NONE, PLANE.NONE, port);

            if (GetBitValue(regValue_mipi_gen_fifo_stat_reg, 28) == 1)
                Log.Success("MIPI DPI FIFO Empty");
            else
                Log.Success("MIPI DPI FIFO Not Empty");

            if (GetBitValue(regValue_mipi_gen_fifo_stat_reg, 27) == 1)
                Log.Success("MIPI DBI FIFO Empty");
            else
                Log.Success("MIPI DBI FIFO Not Empty");

            if (GetBitValue(regValue_mipi_gen_fifo_stat_reg, 26) == 1)
                Log.Success("MIPI LP Ctrl FIFO Empty");
            else
                Log.Success("MIPI LP Ctrl FIFO Not Empty");

            if (GetBitValue(regValue_mipi_gen_fifo_stat_reg, 25) == 1)
                Log.Success("MIPI LP Ctrl FIFO Half Empty");
            else
                Log.Success("MIPI LP Ctrl FIFO Not Half Empty");

            if (GetBitValue(regValue_mipi_gen_fifo_stat_reg, 24) == 1)
                Log.Success("MIPI LP Ctrl FIFO  Full");
            else
                Log.Success("MIPI LP Ctrl FIFO Not Full ");
        }

        private void GetMIPI_INTR_STAT_REG(PORT port)
        {
            uint regValue_mipi_int_status = GetRegisterValue(MIPI_INTR_STAT_REG, PIPE.NONE, PLANE.NONE, port);

            if(regValue_mipi_int_status == 0)
	            Log.Success("INTR STATUS NOT FOUND.");

            if (GetBitValue(regValue_mipi_int_status, 31) == 1)
                Log.Success("Mipi - Tearing Effect -Trigger Success is Received");

            if (GetBitValue(regValue_mipi_int_status, 30) == 1)
                Log.Success("Mipi - SPL PKT Sent Interrupt - transmission of the DPI event specific commands set in the dpi control and dpi data register");

            if (GetBitValue(regValue_mipi_int_status, 29) == 1)
                Log.Success("Mipi - Gen Read Data Avail - Generic read response data is available in the read FIFO");

            if (GetBitValue(regValue_mipi_int_status, 28) == 1)
                Log.Success("Mipi - LP Generic WR FIFO Full");

            if (GetBitValue(regValue_mipi_int_status, 27) == 1)
                Log.Success("Mipi - HS Generic WR Fifo Full");

            if (GetBitValue(regValue_mipi_int_status, 26) == 1)
                Log.Success("Mipi- RX Prot Violation");

            if (GetBitValue(regValue_mipi_int_status, 25) == 1)
                Log.Success("Mipi - RX Invalid TX Length");

            if (GetBitValue(regValue_mipi_int_status, 24) == 1)
                Log.Success("Mipi - ACK With No Error");

            if (GetBitValue(regValue_mipi_int_status, 23) == 1)
                Log.Success("Mipi - Turn Around Ack Timeout");

            if (GetBitValue(regValue_mipi_int_status, 22) == 1)
                Log.Success("Mipi - LP RX Timeout");

            if (GetBitValue(regValue_mipi_int_status, 21) == 1)
                Log.Success("Mipi - HS TX Timeout");

            if (GetBitValue(regValue_mipi_int_status, 20) == 1)
                Log.Success("Mipi - DPI FIFO Underrun");

            if (GetBitValue(regValue_mipi_int_status, 19) == 1)
                Log.Success("Mipi - Low Contention - LP low fault is registered by at the D-PHY contention detector");

            if (GetBitValue(regValue_mipi_int_status, 18) == 1)
                Log.Success("Mipi - High Contention - LP high fault is registered by at the D-PHY contention detector");

            if (GetBitValue(regValue_mipi_int_status, 17) == 1)
                Log.Success("Mipi - TXDSI Virtual Channel ID Invalid");

            if (GetBitValue(regValue_mipi_int_status, 16) == 1)
                Log.Success("Mipi - Data Type Not Recognised");

            if (GetBitValue(regValue_mipi_int_status, 15) == 1)
                Log.Success("Mipi - TXChecksum Error");

            if (GetBitValue(regValue_mipi_int_status, 14) == 1)
                Log.Success("Mipi - TXECC Multibit Error");

            if (GetBitValue(regValue_mipi_int_status, 13) == 1)
                Log.Success("Mipi - TXECC Single bit Error");

            if (GetBitValue(regValue_mipi_int_status, 12) == 1)
                Log.Success("Mipi - TXFalse Control Error");

            if (GetBitValue(regValue_mipi_int_status, 11) == 1)
                Log.Success("Mipi - RXDSI VC ID Invalid");

            if (GetBitValue(regValue_mipi_int_status, 10) == 1)
                Log.Success("Mipi - RXDSI Data Type Not Recognised	");

            if (GetBitValue(regValue_mipi_int_status, 9) == 1)
                Log.Success("Mipi - RXChecksum Error");

            if (GetBitValue(regValue_mipi_int_status, 8) == 1)
                Log.Success("Mipi - RXECC Multibit Error");

            if (GetBitValue(regValue_mipi_int_status, 7) == 1)
                Log.Success("Mipi - RXECC Single Bit Error");

            if (GetBitValue(regValue_mipi_int_status, 6) == 1)
                Log.Success("Mipi - RXFalse Control Error	");

            if (GetBitValue(regValue_mipi_int_status, 5) == 1)
                Log.Success("Mipi - RXHS Receive Timeout Error");

            if (GetBitValue(regValue_mipi_int_status, 4) == 1)
                Log.Success("Mipi - RX LP TX Sync Error");

            if (GetBitValue(regValue_mipi_int_status, 3) == 1)
                Log.Success("Mipi - Escape Mode Entry Error");

            if (GetBitValue(regValue_mipi_int_status, 2) == 1)
                Log.Success("Mipi - RXEOTSyncError	");

            if (GetBitValue(regValue_mipi_int_status, 1) == 1)
                Log.Success("Mipi - RXSOTError");

            if (GetBitValue(regValue_mipi_int_status, 0) == 1)
                Log.Success("Mipi - RXSOTError");
        }

        private void GetMIPI_HORIZ_SYNC_PADDING_COUNT(PORT port)
        {
            uint count = GetRegisterValue(MIPI_HORIZ_SYNC_PADDING_COUNT, PIPE.NONE, PLANE.NONE, port);

            Log.Success("{0} value is {1}", MIPI_HORIZ_SYNC_PADDING_COUNT, count);
        }

        private void GetMIPI_HORIZ_BACK_PORCH_COUNT(PORT port)
        {
            uint count = GetRegisterValue(MIPI_HORIZ_BACK_PORCH_COUNT, PIPE.NONE, PLANE.NONE, port);
            Log.Success("{0} value is {1}", MIPI_HORIZ_BACK_PORCH_COUNT, count);
        }

        private void GetMIPI_HORIZ_FRONT_PORCH_COUNT(PORT port)
        {
            uint count = GetRegisterValue(MIPI_HORIZ_FRONT_PORCH_COUNT, PIPE.NONE, PLANE.NONE, port);
            Log.Success("{0} value is {1}", MIPI_HORIZ_FRONT_PORCH_COUNT, count);
        }

        private void GetMIPI_HORIZ_ACTIVE_AREA_COUNT(PORT port)
        {
            uint count = GetRegisterValue(MIPI_HORIZ_ACTIVE_AREA_COUNT, PIPE.NONE, PLANE.NONE, port);
            Log.Success("{0} value is {1}", MIPI_HORIZ_ACTIVE_AREA_COUNT, count);
        }

        private void GetMIPI_VERT_SYNC_PADDING_COUNT(PORT port)
        {
            uint count = GetRegisterValue(MIPI_VERT_SYNC_PADDING_COUNT, PIPE.NONE, PLANE.NONE, port);
            Log.Success("{0} value is {1}", MIPI_VERT_SYNC_PADDING_COUNT, count);
        }

        private void GetMIPI_VERT_BACK_PORCH_COUNT(PORT port)
        {
            uint count = GetRegisterValue(MIPI_VERT_BACK_PORCH_COUNT, PIPE.NONE, PLANE.NONE, port);
            Log.Success("{0} value is {1}", MIPI_VERT_BACK_PORCH_COUNT, count);
        }

        private void GetMIPI_VERT_FRONT_PORCH_COUNT(PORT port)
        {
            uint count = GetRegisterValue(MIPI_VERT_FRONT_PORCH_COUNT, PIPE.NONE, PLANE.NONE, port);
            Log.Success("{0} value is {1}", MIPI_VERT_FRONT_PORCH_COUNT, count);
        }

        private void GetMIPI_HIGH_LOW_SWITCH_COUNT(PORT port)
        {
            uint count = GetRegisterValue(MIPI_HIGH_LOW_SWITCH_COUNT, PIPE.NONE, PLANE.NONE, port);
            Log.Success("{0} value is {1}", MIPI_HIGH_LOW_SWITCH_COUNT, count);
        }

        private void GetMIPI_Data_Width_CMD_Mode(PORT port)
        {
            uint regCMD_data_width = GetRegisterValue(MIPI_Data_Width_CMD_Mode, PIPE.NONE, PLANE.NONE, port);
            Log.Success("{0} value is {1}", MIPI_Data_Width_CMD_Mode, regCMD_data_width);

            if (regCMD_data_width == 7)
                Log.Success(" MIPI Command data width - Reserved");

            else if (regCMD_data_width == 6)
                Log.Success(" MIPI Command data width - Reserved");

            else if (regCMD_data_width == 5)
                Log.Success(" MIPI Command data width - Option-2");

            else if (regCMD_data_width == 4)
                Log.Success(" MIPI Command data width - Option-1");

            else if (regCMD_data_width == 3)
                Log.Success(" MIPI Command data width - 8 - Bit");

            else if (regCMD_data_width == 2)
                Log.Success(" MIPI Command data width - 9 - Bit");

            else if (regCMD_data_width == 1)
                Log.Success(" MIPI Command data width - 16 - Bit");

            else if (regCMD_data_width == 0)
                Log.Success(" MIPI Command data width - Reserved");
        }
        
        private void GetDBI_FIFO_Thrtl(PORT port)
        {
            uint throtl = GetRegisterValue(MIPI_DSI_Resolution, PIPE.NONE, PLANE.NONE, port);

            if (throtl == 0)
                Log.Success("MIPI DBI FIFO's watermark = (1/2) DBI fifo empty");
            else if (throtl == 1)
                Log.Success("MIPI DBI FIFO's watermark = (1/4) DBI fifo empty");
            else if (throtl == 2)
                Log.Success("MIPI DBI FIFO's watermark = 7 Locations are Empty");
            else
                Log.Success("MIPI DBI FIFO's watermark = Reserved");
        }

        private void GetDPI_Resolution(PORT port)
        {
            uint hactive = GetRegisterValue(DPI_HACTIVE, PIPE.NONE, PLANE.NONE, port);
            uint vactive = GetRegisterValue(DPI_VACTIVE, PIPE.NONE, PLANE.NONE, port);
            
            Log.Success("HActive:{0}, VActive:{1}", hactive, vactive);
        }

        private void GetDual_Link_Mode(PORT port)
        {
            bool isDualLinkEnabled = VerifyRegisters(MIPI_DUAL_LINK_MODE, PIPE.NONE, PLANE.NONE, port, false);
            if (isDualLinkEnabled)
            {
                Log.Success("Data is driven in Dual Link mode");

                string st = Enum.GetName(typeof(Dual_Link_Mode), Dual_Link_Mode.Dual_Link_Pixel_Alternative_Mode);
                if (VerifyRegisters(st, PIPE.NONE, PLANE.NONE, port, false))
                {
                    Log.Success("Data is driven in pixel alternative mode");
                }
                else
                {
                    Log.Success("Data is driven in Front-Back mode.");
                }
            }
            else
            {
                Log.Success("All 4 MIPI lanes are assigned to pipe A or All 4 MIPI lanes are assigned to pipe B.");
            }
        }

        private void GetNumber_of_Lanes(PORT port)
        {
            uint Lanes_Driver = GetRegisterValue(MIPI_DATA_LANES, PIPE.NONE, PLANE.NONE, port);
            Log.Success("Number of Lanes Data driven for MIPI is {0}", Lanes_Driver);
        }

        private void GetColor_Format_Video_Mode(PORT port)
        {
            uint Color_Format_Val = GetRegisterValue(MIPI_ColorFormat_RGB565, PIPE.NONE, PLANE.NONE, port);
            Color_Format_Val = GetRegisterValue(Color_Format_Val, 7, 10);
            Color_Format_Video_Mode Color_Format = (Color_Format_Video_Mode)Enum.Parse(typeof(Color_Format_Video_Mode), Color_Format_Val.ToString());
            Log.Success("Color_Format_Video_Mode for MIPI is {0}", Enum.GetName(typeof(Color_Format_Video_Mode), Color_Format));
        }
        private void GetPacket_Sequence_Video_Mode(PORT port)
        {
            uint packet_Sequence_Val = GetRegisterValue(BurstMode, PIPE.NONE, PLANE.NONE, port);
            Packet_Sequence_Video_Mode packet_Sequence = (Packet_Sequence_Video_Mode)Enum.Parse(typeof(Packet_Sequence_Video_Mode), packet_Sequence_Val.ToString());
            Log.Success("Packet_Sequence_Video_Mode for MIPI is {0}", Enum.GetName(typeof(Packet_Sequence_Video_Mode), packet_Sequence));
        }
    }
}
