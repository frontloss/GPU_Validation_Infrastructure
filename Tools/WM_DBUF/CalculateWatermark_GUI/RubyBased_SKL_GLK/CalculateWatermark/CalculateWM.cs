using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Runtime.InteropServices;
using CalculateWatermark;

using IgfxExtBridge_DotNet;
using Intel.Display.Automation.Common;
using Intel.Display.Automation.TestsCommon;
using Intel.Display.Automation.Logging;

namespace CalculateWatermark
{
    public partial class CalculateWM : Form
    {
        List<uint> uMem_Latency = new List<uint>();
        IGFX_SYSTEM_CONFIG_DATA_N_VIEWS sysConfigData = new IGFX_SYSTEM_CONFIG_DATA_N_VIEWS();
        
        static RegisterModule reg = new RegisterModule();
        uint[] uPlane_CTL = { 0, 0, 0 };
        uint[] uScalar_CTL = { 0, 0 };
        uint[] uPipe_SRC_SZ = { 0, 0, 0 };                //Calculated for source size of each enabled pipe
        uint[] uPlane_SZ = { 0, 0, 0 };                 //calculated per pipe for plane down scaling coefficient
        uint[] uScalar_Dest_SZ = { 0, 0 };             //Calculated to know the destination window size for pipe/plane down scaling coefficient
        uint[] uWM_LINETIME = { 0, 0, 0 };             //To compare the driver coded values with that of the tool's expected value
        bool bFinalResult = true;                      //assume WM is fine initially, update the bool on even a single error.
        uint[] uPlane_BUF_CFG = { 0, 0, 0 }, uPlane_NV12_BUF_CFG = { 0, 0, 0 };//To calculate plane buffer allocation
        uint[,] uPlane_WM_Base_Offset = { { 0x70240, 0x70340, 0x70440 }, 
                                        { 0x71240, 0x71340, 0x71440 }, 
                                        { 0x72240, 0x72340, 0x72440 } };//Base offset used to get driver programmed WM_enable, line and block values. matrix[pipe,plane]
        uint[,] uPlane_Transition_Watermark_Offset = { { 0x70268, 0x70368, 0x70468, 0x70568},
                                                     { 0x71268, 0x71368, 0x71468, 0x71568},
                                                     { 0x72268, 0x72368, 0x72468, 0x72568}
                                                     };
        uint uDsiPLLStatus, uMIPIA_PortCtrl , uMIPIC_PortCtrl ,uMIPIACtrl , uMIPICCtrl , uMIPI_HSync  , uMIPI_HFrontPorch ,  uMIPI_HBackPorch, uMIPI_HActive , uMIPIA_DSI , uMIPIC_DSI , uMIPIA_VideoMode , uMIPIC_VideoMode , uMIPIA_VTotal , uMIPIC_VTotal = 0 ;
        uint uWM_wa = 0;

        double[,] uPlaneBW = { {0,0,0},{0,0,0},{0,0,0}};
        double[] uPipeBW = { 0, 0, 0 };
        double[,] Latency0Blocks = {{0,0,0},{0,0,0},{0,0,0} };
        double[,] Latency0Lines = { { 0, 0, 0 }, { 0, 0, 0 }, { 0, 0, 0 } };

        double uMemoryFrequency = 0;
        uint uMemoryFreqRegister = 0;
        uint uMemoryChannel0 = 0;
        uint uMemoryChannel1 = 0;
        uint uNoMemoryChannel = 0;
        uint uMemoryRank = 1;
        uint uMemoryRankCh0 = 1;
        uint uMemoryRankCh1 = 1;
        double uRawSystemBW = 0;
        uint uArb_Ctl2 = 0;
        UInt16[] Latency = { 0, 0, 0, 0, 0, 0, 0, 0 };

        String MonitorID1, MonitorID2, MonitorID3;
        UInt32[] MonitorID = {0,0,0 };
        bool Transtion_WM_STatus = false;

        String Platform_Selected;

        int Time=0;

        SimpleLogger logger = new SimpleLogger(null, LogType.LogInXmlFormat, "xyz");

        [DllImport("Utilities.dll")]
        private static extern UInt32 readMMIOReg(UInt32 offset, ref UInt32 value);

        [DllImport("Utilities.dll")]
        private static extern UInt32 writeMMIOReg(UInt32 dwOffset, UInt32 dwValue);

        public CalculateWM()
        {
            InitializeComponent();
           
        }

        private void clbPlatformSelect_SelectedIndexChanged(object sender, EventArgs e)
        {
            if (clbPlatformSelect.CheckedIndices.Count == 0)
            {
                return;
            }
            foreach (string platform in clbPlatformSelect.CheckedItems)
            {
                if (platform == "BDW/HSW")
                {
                    MessageBox.Show("Tool is under design for BDW/HSW. Please select SKL for now! :)");
                    return;
                }
                else if (platform == "BXT")
                {
                    Platform_Selected = "BXT";
                }
                else if (platform == "SKL")
                {
                    Platform_Selected = "SKL";
                }
                else if (platform == "KBL")
                {
                    Platform_Selected = "KBL";
                }
                else if (platform == "GLK")
                {
                    Platform_Selected = "GLK";
                }
                else
                {
                    Platform_Selected = "CNL";
                }
            }

            bCalculateWM.Enabled = true;
            clbPlatformSelect.Enabled = false;
            textBox1.Enabled = true;
            textBox1.Text = "Pipe 1 Disp MonitorID";
            textBox2.Text = "Pipe 2 Disp MonitorID";
            textBox3.Text = "Pipe 3 Disp MonitorID";


        }

        private void bCalculateWM_Click(object sender, EventArgs e)
        {
            CmnDelay.Seconds(Time);
            try
            {
                if (!InitializeWM())
                {
                    rtbInput.AppendText("Cannot retreive current configuration");
                    rtbOutput.AppendText("WM calculation aborted");
                    rtbStatus.ForeColor = Color.Red;
                    rtbStatus.AppendText("FAILED");
                    return;
                }
                WaterMarkCalculate();
                rtbInput.ScrollToCaret();
                rtbOutput.ScrollToCaret();
                if (bFinalResult)
                {
                    rtbStatus.ForeColor = Color.Green;
                    rtbStatus.AppendText("PASS");
                }
                else
                {
                    rtbStatus.ForeColor = Color.Red;
                    rtbStatus.AppendText("FAILED");
                }
            }
            finally
            {
                this.ActiveControl.BringToFront();
                
            }
        }
        private bool InitializeWM()
        {
            rtbInput.Clear();
            rtbOutput.Clear();
            rtbStatus.Clear();
            rtbInput.AppendText("~~~INPUTS~~~");
            rtbOutput.AppendText("===OUTPUTS===");
            
           
            return SDKManager.Instance.GetSystemConfiguration(ref sysConfigData);
        }

        private void WaterMarkCalculate()
        {
            uint uNumberOfEnabledPipes = 0;
            uint uActualPipePixelRate = 0;
           double uAdjustedPipePixelRate = 1, uAdjustedPlanePixelRate = 0;
           double uPipeScalar = 1, uPlaneScalar = 1;
            uint[] WM_LINETIME = { 0, 0, 0 };
            double uMethod1Value = 0, uMethod2Value = 0, uYTileMinimum = 0,uYTileMinimumLines = 0;
            uint uPlaneBytesPerLine = 1;    // Changing the code making uPlaneBytesPerline = 1 for removing the exception
            uint uPlaneBufferAlocation = 0;
            double uResultBlocks = 0, uResultLines = 0;
            uint uWMPlanePipeLatencyLevel = 0;
            uint uWM_Plane_Transition_Value = 0;
            uint Manual_Pixel_Clock = 0;
            double uPlaneBlockperline = 0;
            uint Transtion_Minimum = 14, Transition_Amount = 20, Trans_Result_Block = 0, Trans_Result_Line = 0, Trans_Y_Tile = 0, Trans_Offset_Block = 0 ;
            double Temp1 = 0;
            int i = 0;
            
            //Retrieve memory latency values 
            CalculateMemoryLatency();
            if ((Platform_Selected != "GLK") && (Platform_Selected != "CNL"))
            {
                CalculateArbitratedDisplayBandwidth();
            }

            rtbOutput.AppendText("\n INFO:The tool may not work sometimes if a display config switch is done , in that case apply desired configuration , restart system and run the tool");
           
            //Get number of enabled pipes
            uNumberOfEnabledPipes = sysConfigData.uiNDisplays;
            InitializePipeRegisters();//To get pipe source size, later used in scalar value calculation for pipe
            rtbInput.AppendText("Number of Pipes enabled: " + sysConfigData.uiNDisplays.ToString());
            
            for (int loop = 0; loop < uNumberOfEnabledPipes; loop++)
            {
                i = loop;
                
                //Calculate adjusted pipe pixel rate 
                PixelClock pix = new PixelClock();
                                
                if (loop == 0)
                {
                    if (MonitorID1.Contains("Pipe 1 Disp MonitorID") == false)              //For Display 1 (Pipe1)
                    {
                        MonitorID[i] = Convert.ToUInt32(MonitorID1);
                        uActualPipePixelRate = (uint)pix.GetCurrentMode(MonitorID[i]);
                    }
                    else
                    {
                        if (MonitorID2.Contains("Pipe 2 Disp MonitorID") == false)              //For Display 1 (Pipe1)
                        {
                            i = i + 1;
                            MonitorID[i] = Convert.ToUInt32(MonitorID2);
                            uActualPipePixelRate = (uint)pix.GetCurrentMode(MonitorID[i]);
                        }
                        else
                        {
                            i = i + 2;
                            MonitorID[i] = Convert.ToUInt32(MonitorID3);
                            uActualPipePixelRate = (uint)pix.GetCurrentMode(MonitorID[i]);
                        }
                    }
                }

                if (loop == 1)                                 //For Display 2  (Pipe2)
                {
                    if (MonitorID1.Contains("Pipe 1 Disp MonitorID") == true)              //For Display 1 (Pipe1)
                    {
                        i = i + 1;
                        MonitorID[i] = Convert.ToUInt32(MonitorID3);
                        uActualPipePixelRate = (uint)pix.GetCurrentMode(MonitorID[i]);
                    }
                    else
                    {
                        if (MonitorID2.Contains("Pipe 2 Disp MonitorID") == false)              //For Display 1 (Pipe1)
                        {
                            MonitorID[i] = Convert.ToUInt32(MonitorID2);
                            uActualPipePixelRate = (uint)pix.GetCurrentMode(MonitorID[i]);
                        }
                        else if (MonitorID3.Contains("Pipe 3 Disp MonitorID") == false)
                        {
                            i = i + 1;
                            MonitorID[i] = Convert.ToUInt32(MonitorID3);
                            uActualPipePixelRate = (uint)pix.GetCurrentMode(MonitorID[i]);
                        }
                        else
                        {
                            bFinalResult = false;
                            rtbOutput.AppendText("\n ERROR: You may not have entered monitor IDs for all active displays");
                        }
                    }
                }

                if (loop == 2)                                    //For Display 3 (Pipe3)
                {
                    MonitorID[i] = Convert.ToUInt32(MonitorID3);
                    uActualPipePixelRate = (uint)pix.GetCurrentMode(MonitorID[i]);
                }

                rtbOutput.AppendText("=======================\n\n\n\n\nPIPE: " + (i + 1) + "\n=======================");

                rtbInput.AppendText("Pixel clk from OS "+ uActualPipePixelRate + " for pipe " + (i+1));


                Manual_Pixel_Clock = ((GetHTotal(i) * GetVTotal(i) * Convert.ToUInt32(sysConfigData.DispCfg[loop].Resolution.dwRR.ToString()))/1000); // Keeping the Pixel Clock in Khz
                rtbOutput.AppendText("Manually Calculated Pixel Clock :" + Manual_Pixel_Clock + "  " + GetHTotal(i) + "  " + GetVTotal(i) + " " + Convert.ToUInt32(sysConfigData.DispCfg[loop].Resolution.dwRR.ToString()));
                

                rtbInput.AppendText("~~~~~~~~~~~~~~~~~~~~~~~~\n\n\n\n\nPIPE: " + (i + 1) + "\n~~~~~~~~~~~~~~~~~~~~~~~~");
                rtbInput.AppendText("\nResolution: " + sysConfigData.DispCfg[loop].Resolution.dwHzRes.ToString() + " X " + sysConfigData.DispCfg[loop].Resolution.dwVtRes.ToString() +
                    " X at " + sysConfigData.DispCfg[loop].Resolution.dwRR.ToString() + "Hz and " + sysConfigData.DispCfg[loop].Resolution.dwBPP.ToString() + "bpp");
                rtbOutput.AppendText("\nInfo: Actual pixel rate: " + uActualPipePixelRate.ToString());
               uAdjustedPipePixelRate = uActualPipePixelRate;
               
                if (sysConfigData.DispCfg[loop].Resolution.InterlaceFlag != 0)
                {
                    rtbInput.AppendText("\nInterlaced mode enabled");
                    uAdjustedPipePixelRate = uAdjustedPipePixelRate * 2;
                }
                //If pipe scaling enabled, adjusted pipe pixel rate = adjusted pipe pixel rate * pipe down scale amount 
                InitializeScalarRegisters(i);
                uPipeScalar = GetPipeScalar(i);
                uAdjustedPipePixelRate = (uAdjustedPipePixelRate * uPipeScalar) / 1000000;
               
                rtbOutput.AppendText("\nInfo: Adjusted pipe pixel rate: " + uAdjustedPipePixelRate.ToString());

                if ((uint)uAdjustedPipePixelRate != 0)
                {
                    WM_LINETIME[i] = ((10 * (8 * 1000 * GetHTotal(i))) + (5 * ((uint)uAdjustedPipePixelRate))) / (10 * ((uint)uAdjustedPipePixelRate));

                    if ((Platform_Selected == "BXT") || (Platform_Selected == "GLK"))
                    {
                        WM_LINETIME[i] = WM_LINETIME[i] / 2;
                    }
                }

                if (!Check_WM_LINETIME(i, WM_LINETIME[i]))
                {
                    bFinalResult = false;
                    rtbOutput.AppendText("\nThere is a Watermark linetime mismatch !!! Possible user error !!!  \nIt is possible you entered Monitor ID to the wrong pipe assigned text box(A,B,C) , recheck with monitor ID added in the correct pipe assignment order. Usually , if LFP is present, it is always on Pipe 1 , EFPs can be on Pipe 2 or Pipe 3");
                }

                if(WM_LINETIME[i] == 0)
                {
                    bFinalResult = false;
                    rtbOutput.AppendText("\nWatermark linetime is 0 !!! Possible user error !!!  \nIt is possible you entered Monitor ID to the wrong pipe assigned text box(A,B,C) , recheck with monitor ID added in the correct pipe assignment order. Usually , if LFP is present, it is always on Pipe 1 , EFPs can be on Pipe 2 or Pipe 3");
                }

                InitializePlaneRegisters(i);

                //for calculating 3 planes per pipe
                for (int j = 0; j < 3 && (uPlane_CTL[j] & 0x80000000) == 0x80000000; j++)
                {
                    rtbInput.AppendText("\n\n\nPLANE: " + (j + 1));
                    rtbOutput.AppendText("\n\n\nPLANE: " + (j + 1));
                    if ((uPlane_CTL[j] & 0x80000000) == 0)
                    {
                        rtbOutput.AppendText("\n Plane " + (j + 1) + " in pipe " + (i + 1) + " is not enabled");
                        
                    }
                    else
                    {
                        rtbOutput.AppendText("\n Plane " + (j + 1) + " in pipe " + (i + 1) + " is enabled");
                        uAdjustedPlanePixelRate = uAdjustedPipePixelRate;
                        uPlaneScalar = GetPlaneScalar(i, j);

                        uAdjustedPlanePixelRate =  (uAdjustedPipePixelRate *uPlaneScalar)/1000000;
                    }
                    
                    //for calculations involving each memory latency values per plane
                    for (int k = 0; k < 8; k++)
                    {

 
                        uint BPP = 0;
                        

                       uint A1 = (uPlane_CTL[j] & 0x0F000000)>>24;

                       if (A1 == 1  || A1 == 12)
                           BPP = 1;
                       else if (A1 == 0 || A1 == 14)
                           BPP = 2;
                       else if (A1 == 6)
                           BPP = 8;
                       else
                           BPP = sysConfigData.DispCfg[loop].Resolution.dwBPP / 8;

                       uYTileMinimumLines = 4;

                       if ((uPlane_CTL[j] & 0x00000001) == 1) // 90/270 rotated plane
                       { 
                           if (BPP == 1) uYTileMinimumLines = 16;
                           if (BPP == 2) uYTileMinimumLines = 8;
                       }
                       if (uWM_wa == 1) // WA 1 is to double Y -tile min if arbitrated bw exceeds 20 % of raw system memory bw
                       {
                           uYTileMinimumLines = uYTileMinimumLines * 2;
                       }


                       rtbInput.AppendText("\nLatency:" + uMem_Latency[k] + " AdjustedPlaneRate:" + uAdjustedPlanePixelRate + " Htotal:" + GetHTotal(i) + " BPP:" + BPP);
                        
                        if (((uPlane_CTL[j] & 0x00001000) == 0x00000000) && (uWM_wa != 0)) //add 15us latency if wa enabled for xtiled planes
                        {
                            uMethod1Value = ((uMem_Latency[k]+15) * (uAdjustedPlanePixelRate) * (BPP)) / 512000;  //Considering the Pixel clock in Khz
                        }
                        else if ((Platform_Selected == "GLK") || (Platform_Selected == "CNL"))
                        {
                            uMethod1Value = ((uMem_Latency[k] * (uAdjustedPlanePixelRate) * (BPP)) / 512000) + 1;  //Considering the Pixel clock in Khz
                        }
                        else
                        {
                            uMethod1Value = (uMem_Latency[k] * (uAdjustedPlanePixelRate) * (BPP)) / 512000;
                        }

                        //Method 2:                       
                        uPlaneBytesPerLine = ((uPlane_SZ[j] & 0x00001FFF) + 1)  * (BPP);

                        //Calculate Blocks per line 
                        if ((Platform_Selected == "GLK") || (Platform_Selected == "CNL"))
                        {
                            if ((uPlane_CTL[j] & 0x00001000) == 0x00000000) //Check for X-tiling
                                uPlaneBlockperline = (Math.Ceiling(uPlaneBytesPerLine / 512.0)) + 1;
                            else
                                uPlaneBlockperline = (Math.Ceiling(((uYTileMinimumLines * uPlaneBytesPerLine) / 512.0) + 1)) / uYTileMinimumLines;
                        }
                        else
                        {
                            if ((uPlane_CTL[j] & 0x00001000) == 0x00000000) //Check for X-tiling
                                uPlaneBlockperline = (Math.Ceiling(uPlaneBytesPerLine / 512.0));
                            else
                                uPlaneBlockperline = (Math.Ceiling(((uYTileMinimumLines * uPlaneBytesPerLine) / 512.0))) / uYTileMinimumLines;
                        }
                        rtbInput.AppendText("\n BytesPerLine: " + uPlaneBytesPerLine + " BlocksPerLine: " + uPlaneBlockperline);

                        if (((uPlane_CTL[j] & 0x00001000) == 0x00000000) && (uWM_wa != 0))
                        {
                            Temp1 = Math.Ceiling(((uMem_Latency[k] + 15) * (uAdjustedPlanePixelRate) * 1.0) / (GetHTotal(i) * 1.0 * 1000));
                        }
                        else
                        {
                            Temp1 = Math.Ceiling((uMem_Latency[k] * (uAdjustedPlanePixelRate) * 1.0) / (GetHTotal(i) * 1.0 * 1000));
                        }
                        
                        uMethod2Value = Temp1 * uPlaneBlockperline;
                        rtbInput.AppendText("\n Method1 Value: " + uMethod1Value + " Method2Value:" + uMethod2Value);
                        uPlaneBufferAlocation = CalculatePlaneBufferAllocation(j);
                        if ((uPlane_CTL[j] & 0x00001000) == 0x00000000) //Checking for linear or x-tiled plane
                        {
                            if (k == 0)
                            {
                                rtbInput.AppendText("\nPipe " + (i + 1) + " , plane " + (j + 1) + " is X tiled");
                            }
                            //Code add to remove DividebyZero exception

                            if (uPlaneBytesPerLine == 0)
                                uPlaneBytesPerLine = 1;
                            if ((Platform_Selected == "GLK") || (Platform_Selected == "CNL"))
                            {
                                if ((uPlaneBufferAlocation / uPlaneBlockperline) >= 1)
                                {
                                    uResultBlocks = uMethod2Value;
                                }
                                else if (Latency[k] >= WM_LINETIME[i])
                                {
                                    uResultBlocks = uMethod2Value;
                                }
                                else
                                {
                                    uResultBlocks = uMethod1Value;
                                }
                            }
                            else
                            {
                                if ((uPlaneBufferAlocation / uPlaneBlockperline) >= 1)
                                {
                                    uResultBlocks = Math.Min(uMethod1Value, uMethod2Value);
                                }
                                else if (Latency[k] >= WM_LINETIME[i])
                                {
                                    uResultBlocks = Math.Min(uMethod1Value, uMethod2Value);
                                }
                                else
                                {
                                    uResultBlocks = uMethod1Value;
                                }
                            }
                        }
                        else//y-tiling on the current plane enabled
                        {
                            if (k == 0)
                            {
                                rtbInput.AppendText("\nPipe " + (i + 1) + " , plane " + (j + 1) + " is Y tiled");
                            }
                            if ((uPlane_CTL[j] & 0x00000001) == 1)//90 or 270 rotated plane
                            {
                                if ((uPlane_CTL[j] & 0x0F000000) == 0x01000000)//NV12
                                {
                                    rtbInput.AppendText("\nPipe " + (i + 1) + " , plane " + (j + 1) + " is in NV12 pixel format and rotated");
                                    uYTileMinimum = (uYTileMinimumLines * uPlaneBlockperline);
                                }
                                else if ((uPlane_CTL[j] & 0x0F000000) == 0)//YUV 422
                                {
                                    rtbInput.AppendText("\nPipe " + (i + 1) + " , plane " + (j + 1) + " is in YUV422 pixel format and rotated");
                                    uYTileMinimum = (uYTileMinimumLines * uPlaneBlockperline);
                                }
                                else
                                {
                                    rtbInput.AppendText("\nPipe " + (i + 1) + " , plane " + (j + 1) + " is rotated");
                                    uYTileMinimum = (uYTileMinimumLines * uPlaneBlockperline);
                                }
                            }
                            else
                            {
                                //rtbInput.AppendText("\nPipe " + (i + 1) + " , plane " + (j + 1) + " is not rotated");
                                uYTileMinimum = (Math.Round(uYTileMinimumLines * uPlaneBlockperline));
                            }

                      
                            rtbInput.AppendText("\n YTileMinimum:" + uYTileMinimum);
                            uResultBlocks = Math.Max(uMethod2Value, uYTileMinimum);
                        }

                        uResultLines = (uint)Math.Ceiling(uResultBlocks / uPlaneBlockperline);
                        uResultBlocks = (uint)Math.Ceiling(uResultBlocks) + 1;
                        

                        if ((k > 0 & k < 8) && (Platform_Selected != "GLK"))
                        {
                            
                                if ((uPlane_CTL[j] & 0x00001000) == 0x00000000) //Checking for linear or x-tiled plane
                                    uResultBlocks = uResultBlocks + 1;
                                else
                                {
                                    uResultLines = uResultLines + (uYTileMinimum / uPlaneBlockperline);
                                    uResultBlocks = uResultBlocks + uYTileMinimum;
                                }   

                        }

                        // Check for RC enabled
                        if (((uPlane_CTL[j] & 0x00008000) == 0x00008000) && Platform_Selected == "CNL")
                        {
                            if (k ==0)
                            uResultBlocks = uResultBlocks + uYTileMinimum;
                            else 
                            {
                                if (uResultBlocks < Latency0Blocks[i,j])
                                {
                                    uResultBlocks = Latency0Blocks[i, j];
                                }

                                if (uResultLines < Latency0Lines[i, j])
                                {
                                    uResultLines = Latency0Lines[i, j];
                                }
                            }
                        }

                        if (k==0)
                        {
                            Latency0Blocks[i, j] = uResultBlocks;
                            Latency0Lines[i, j] = uResultLines;
                        }
                            

                        //Calculation for Transition Watermark
                        if (k == 0)
                        {
                            Trans_Offset_Block = Transtion_Minimum + Transition_Amount;
                            Trans_Y_Tile = 2 * (uint)uYTileMinimum * uMem_Latency[0];
                            if ((uPlane_CTL[j] & 0x00001000) == 0x00000000)       //CHeck for X-tiling
                            {
                                Trans_Result_Block = (uint)uResultBlocks + Trans_Offset_Block;
                            }
                            else
                            {
                                Trans_Result_Block = Math.Max((uint)uResultBlocks, Trans_Y_Tile) + Trans_Offset_Block;
                            }

                            Trans_Result_Block = (uint)Math.Ceiling( Trans_Result_Block/1.0) + 1;

                        }

                        //Reading the driver Watermark offset Value
                        reg.ReadRegister((uint)(uPlane_WM_Base_Offset[i, j] + (4 * k)), ref uWMPlanePipeLatencyLevel);
                        if (k==0)
                        reg.ReadRegister((uint)( uPlane_Transition_Watermark_Offset[i,j]), ref uWM_Plane_Transition_Value);
                        //Compare against maximum and check programmed values
                        if ((uResultBlocks >= uPlaneBufferAlocation) || (uResultLines > 31))
                        {
                            if (k == 0)//check if level 0 is exceeding max and still plane enabled.
                            {
                                rtbOutput.AppendText("\nERROR: Plane:" + (j + 1) + " was not supposed to be enabled since max value exceeded for level 0. Terminating test!!! \n Result Blocks:" + (uResultBlocks) + "while Plane Buffer:" + (uPlaneBufferAlocation) + "and Result Lines:" + (uResultLines) + "\n");
                                bFinalResult = false;
                                return;
                            }
                            if ((uWMPlanePipeLatencyLevel & 0x80000000) != 0)
                            {
                                rtbOutput.AppendText("\nERROR: Latency level:" + (k) + " enabled for pipe:" + (i + 1) + " and plane:" + (j + 1) + " even though max value exceeded !!! Result Blocks:" + (uResultBlocks) + "while Plane Buffer:" + (uPlaneBufferAlocation) + "and Result Lines:" + (uResultLines) + "\n");
                                bFinalResult = false;
                            }
                        }
                        else
                        {
                            if ((uWMPlanePipeLatencyLevel & 0x80000000) == 0x80000000)
                            {
                                rtbOutput.AppendText("\nInfo: Latency level:" + (k) + " is enabled for pipe:" + (i + 1) + " and plane:" + (j + 1));
                                if ((uWMPlanePipeLatencyLevel & 0x40000000) == 0)
                                {
                                    if (uResultLines != ((uWMPlanePipeLatencyLevel & 0x0007C000) >> 14))
                                    {
                                        rtbOutput.AppendText("\nERROR: Lines programmed: " + ((uWMPlanePipeLatencyLevel & 0x0007C000) >> 14) + " while expected: " + (uResultLines));
                                        bFinalResult = false;
                                    }
                                    else
                                    {
                                        rtbOutput.AppendText("\nSUCCESS: Lines programmed: " + ((uWMPlanePipeLatencyLevel & 0x0007C000) >> 14) + " while expected: " + (uResultLines));
                                    }
                                }
                                else
                                {
                                    rtbOutput.AppendText("\nInfo: Line watermark value is ignored and Block watermark value is used for pipe:" + (i + 1) + " , plane:" + (j + 1) + " and Latency level:" + (k));
                                }
                                if (uResultBlocks != (uWMPlanePipeLatencyLevel & 0x000003FF))  
                                {
                                    rtbOutput.AppendText("\nERROR: Blocks programmed: " + (uWMPlanePipeLatencyLevel & 0x000003FF) + " while expected: " + (uResultBlocks));
                                    bFinalResult = false;
                                }
                                else if ((Trans_Result_Block != (uWM_Plane_Transition_Value & 0x000003FF)) &&  Transtion_WM_STatus == true && k==0)
                                {
                                    rtbOutput.AppendText("\nERROR: Transition Blocks programmed: " + (uWM_Plane_Transition_Value & 0x000003FF) + " while expected: " + (uResultBlocks));
                                    bFinalResult = false;
                                }
                                else
                                {
                                    rtbOutput.AppendText("\nSUCCESS: Blocks programmed: " + (uWMPlanePipeLatencyLevel & 0x000003FF) + " while expected: " + (uResultBlocks));
                                }
                            }
                        }
                    }
                }

            }

        }

        private uint CalculatePlaneBufferAllocation(int planeCount)
        {
            uint uPlaneBufAllocation = 0;
            if (!((uPlane_CTL[planeCount] & 0x0F000000) == 0x01000000))
            {
                uPlaneBufAllocation = (uint)Math.Abs((int)((uPlane_BUF_CFG[planeCount] & 0x03FF0000) >> 16) - (int)(uPlane_BUF_CFG[planeCount] & 0x000003FF)) + 1;
            }
            else
            {
                uPlaneBufAllocation = (uint)Math.Abs((int)((uPlane_NV12_BUF_CFG[planeCount] & 0x03FF0000) >> 16) - (int)(uPlane_NV12_BUF_CFG[planeCount] & 0x000003FF)) + 1;
            }
            return uPlaneBufAllocation;
        }

        private bool Check_WM_LINETIME(int pipeCount, uint WM_LineTime)
        {
            uint uDriverWMLineTime = 0;
            uDriverWMLineTime = uWM_LINETIME[pipeCount] & 0x000001FF;
            if (WM_LineTime == uDriverWMLineTime)
            {
                rtbOutput.AppendText("\nSUCCESS: WM_LINETIME matches for pipe " + (pipeCount + 1) +
                    ". Driver programmed: " + uDriverWMLineTime + " for expected value: " + WM_LineTime);
                return true;
            }
            else if ((WM_LineTime - 1) == uDriverWMLineTime)
            {
                rtbOutput.AppendText("\nSUCCESS: WM_LINETIME matches for pipe " + (pipeCount + 1) +
                    ". Driver programmed: " + uDriverWMLineTime + " for expected value: " + WM_LineTime);
                return true;
            }
            else if((WM_LineTime + 1) == uDriverWMLineTime)
            {
                rtbOutput.AppendText("\nSUCCESS: WM_LINETIME matches for pipe " + (pipeCount + 1) +
                    ". Driver programmed: " + uDriverWMLineTime + " for expected value: " + WM_LineTime);
                return true;
            }
            else
            {
                rtbOutput.AppendText("\nERROR: WM_LINETIME does not match for pipe " + (pipeCount + 1) +
                    ". Driver programmed: " + uDriverWMLineTime + " for expected value: " + WM_LineTime);
                return false;

            }
        }

        private uint GetHTotal(int pipeCount)
        {
            uint uHtotal = 0;
            uint lane_cnt = 0 , bpp = 0 , A1 = 0;
            uint HActive, HSync, HFPorch, HBPorch , HSyncStart , HSyncEnd = 0;
            bool CalculateHTotal = false;
            if (MonitorID[pipeCount] == 265988)               //eDP or MIPI ID is 4096
            {

                reg.ReadRegister((uint)0x6F000, ref uHtotal);

                if(uHtotal!=0)
                return ((uHtotal & 0x1FFF0000) >> 16) + 1;
            }
       
            // To calculate HTotal for MIPI in BXT MIPI  

                if ((Platform_Selected == "BXT") || (Platform_Selected == "GLK") || (Platform_Selected == "CNL"))
                {
                    reg.ReadRegister((uint)0x46080, ref uDsiPLLStatus);

                    if ((uDsiPLLStatus & 0x80000000) == 0x80000000)
                    {
                        InitializeMIPIRegisters();
                    }

                   
                    if (((uMIPIA_PortCtrl & 0x80000000) == 0x80000000) && (MonitorID[pipeCount] == 266500) )
                    {

                        A1 = (uMIPIA_DSI & 0x00000780) >> 7;

                        if (A1 == 1)
                            bpp = 16;
                        else if (A1 == 3)
                            bpp = 18;
                        else if (A1 == 4)
                            bpp = 24;

                        lane_cnt = uMIPIA_DSI & 0x00000007;

                        

                        CalculateHTotal = true;

                    }
                   
                    if (((uMIPIC_PortCtrl & 0x80000000) == 0x80000000) && (MonitorID[pipeCount] == 266500))
                    {


                        A1 = (uMIPIC_DSI & 0x00000780) >> 7;

                        if (A1 == 1)
                            bpp = 16;
                        else if (A1 == 3)
                            bpp = 18;
                        else if (A1 == 4)
                            bpp = 24;

                        lane_cnt = uMIPIC_DSI & 0x00000007;

                        CalculateHTotal = true;
                    }

                    if (CalculateHTotal)
                    {
                        // To convert bytclk to pixelclk

                        
                        HActive = (uint)Math.Ceiling(((double)uMIPI_HActive * lane_cnt * 8)) / bpp;

                        HSync = (uint)Math.Ceiling(((double)uMIPI_HSync * lane_cnt * 8)) / bpp;

                        HFPorch = (uint)Math.Ceiling(((double)uMIPI_HFrontPorch * lane_cnt * 8)) / bpp;

                        HBPorch = (uint)Math.Ceiling(((double)uMIPI_HBackPorch * lane_cnt * 8)) / bpp;

                        HSyncStart = HFPorch + HActive;

                        HSyncEnd = HSync + HSyncStart - 1;

                        uHtotal = HBPorch + HSyncEnd + 1;

                        rtbInput.AppendText("\nMIPI HTotal calculated:" + (uHtotal));

                        return uHtotal;
                    }
                }

           

            if (pipeCount == 0)
            {
                reg.ReadRegister((uint)0x60000, ref uHtotal);
            }
            else if (pipeCount == 1)
            {
                reg.ReadRegister((uint)0x61000, ref uHtotal);
            }
            else if (pipeCount == 2)
            {
                reg.ReadRegister((uint)0x62000, ref uHtotal);
            }
            return ((uHtotal & 0x1FFF0000) >> 16) + 1;
        }


        private uint GetVTotal(int pipeCount)
        {
            uint uVtotal = 0;
            if (MonitorID[pipeCount] == 265988)               //eDP ID is 4096
            {
                reg.ReadRegister((uint)0x6F00C, ref uVtotal);
                return ((uVtotal & 0x1FFF0000) >> 16) + 1;

            }
            if ((Platform_Selected == "BXT") || (Platform_Selected == "GLK") || (Platform_Selected == "CNL"))
                {
                    reg.ReadRegister((uint)0x46080, ref uDsiPLLStatus);

                    if ((uDsiPLLStatus & 0x80000000) == 0x80000000)
                    {
                        InitializeMIPIRegisters();
                    }
                    
                    if (((uMIPIA_PortCtrl & 0x80000000) == 0x80000000) && (MonitorID[pipeCount] == 266500))
                    {
                        uVtotal = uMIPIA_VTotal;
                    }
                    else if (((uMIPIC_PortCtrl & 0x80000000) == 0x80000000) && (MonitorID[pipeCount] == 266500))
                    {
                        uVtotal = uMIPIC_VTotal;
                    }

                    if (uVtotal != 0)
                        return uVtotal;
                } 
                
               
            

            if (pipeCount == 0)
            {
                reg.ReadRegister((uint)0x6000C, ref uVtotal);
            }
            else if (pipeCount == 1)
            {
                reg.ReadRegister((uint)0x6100C, ref uVtotal);
            }
            else if (pipeCount == 2)
            {
                reg.ReadRegister((uint)0x6200C, ref uVtotal);
            }
            return ((uVtotal & 0x1FFF0000) >> 16) + 1;
        }

        private UInt64 GetPlaneScalar(int pipeCount, int planeCount)
        {
            UInt64 uPlaneDownScale = 1000000;
            UInt64 uHorizontalDownScale = 1, uVerticalDownScale = 1;
            uint uScalar_Dest_SZ_for_Pipe = 0;
            bool iScalar0AttachedToPlane = false;
            if (!((uScalar_CTL[0] != 0) || (uScalar_CTL[1] != 0)))
            {
                return uPlaneDownScale;
            }

            if (((uScalar_CTL[0] & 0x80000000) != 0) && ((planeCount + 1) == ((uScalar_CTL[0] & 0x0E000000) >> 25)))
            {
                rtbInput.AppendText("Scalar 0 is attached to Pipe: " + (pipeCount + 1) + " - plane: " + (planeCount + 1));
                iScalar0AttachedToPlane = true;
            }
            else if (((uScalar_CTL[1] & 0x80000000) != 0) && ((planeCount + 1) == ((uScalar_CTL[1] & 0x0E000000) >> 25)))
            {
                rtbInput.AppendText("Scalar 1 is attached to Pipe: " + (pipeCount + 1) + " - plane: " + (planeCount + 1));
            }
            else
            {
                rtbInput.AppendText("No plane scalar is attached to Pipe: " + (pipeCount + 1) + " - plane: " + (planeCount + 1));
                return uPlaneDownScale;
            }

            if (iScalar0AttachedToPlane)
            {
                uScalar_Dest_SZ_for_Pipe = uScalar_Dest_SZ[0];
            }
            else
            {
                uScalar_Dest_SZ_for_Pipe = uScalar_Dest_SZ[1];
            }

            UInt64 a2= ((uPlane_SZ[planeCount] & 0x00001FFF) + 1) *1000;
            UInt64 b2 = (uScalar_Dest_SZ_for_Pipe & 0x1FFF0000) >> 16;

            if (b2 == 0)
                b2 = 1;
            uHorizontalDownScale = a2 / b2;

            
            if (uHorizontalDownScale <= 1000)
            {
                rtbInput.AppendText("\nPipe " + (pipeCount + 1) + " horizontal down scaling not enabled");
                uHorizontalDownScale = 1000;
            }
            //rtbInput.AppendText("I am Here in Plane Scalar");
            UInt64 a3 = (((uPlane_SZ[planeCount] & 0x1FFF0000) + 1)>>16) * 1000;
            UInt64 b3 = (uScalar_Dest_SZ_for_Pipe & 0x00001FFF);

            if (b3 == 0)
                b3 = 1;
            uVerticalDownScale = a3 / b3;

           

            if (uVerticalDownScale <= 1000)
            {
                rtbInput.AppendText("\nPipe " + (pipeCount + 1) + " vertical down scaling not enabled");
                uVerticalDownScale = 1000;
            }
            uPlaneDownScale = uHorizontalDownScale * uVerticalDownScale;
            
            return uPlaneDownScale;
        }

        private void InitializePipeRegisters()
        {
            reg.ReadRegister((uint)0x6001C, ref uPipe_SRC_SZ[0]);
            reg.ReadRegister((uint)0x6101C, ref uPipe_SRC_SZ[1]);
            reg.ReadRegister((uint)0x6201C, ref uPipe_SRC_SZ[2]);
            reg.ReadRegister((uint)0x45270, ref uWM_LINETIME[0]);
            reg.ReadRegister((uint)0x45274, ref uWM_LINETIME[1]);
            reg.ReadRegister((uint)0x45278, ref uWM_LINETIME[2]);
        }

        private void InitializeScalarRegisters(int pipeCount)
        {
            if (pipeCount == 0)
            {
                reg.ReadRegister((uint)0x68180, ref uScalar_CTL[0]);
                reg.ReadRegister((uint)0x68280, ref uScalar_CTL[1]);
                reg.ReadRegister((uint)0x68174, ref uScalar_Dest_SZ[0]);
                reg.ReadRegister((uint)0x68274, ref uScalar_Dest_SZ[1]);
            }
            if (pipeCount == 1)
            {
                reg.ReadRegister((uint)0x68980, ref uScalar_CTL[0]);
                reg.ReadRegister((uint)0x68A80, ref uScalar_CTL[1]);
                reg.ReadRegister((uint)0x68974, ref uScalar_Dest_SZ[0]);
                reg.ReadRegister((uint)0x68A74, ref uScalar_Dest_SZ[1]);
            }
            if (pipeCount == 2)
            {
                reg.ReadRegister((uint)0x69180, ref uScalar_CTL[0]);
                reg.ReadRegister((uint)0x69174, ref uScalar_Dest_SZ[0]);
                uScalar_CTL[1] = 0;
                uScalar_Dest_SZ[1] = 0;
            }
        }

        private UInt64 GetPipeScalar(int pipeCount)                 
        {
            UInt64 uPipeDownScale = 1000000;
            UInt64 uHorizontalDownScale = 1, uVerticalDownScale = 1;
            InitializePipeRegisters();
            if (!((uScalar_CTL[0] != 0) || (uScalar_CTL[1] != 0)))
            {
                rtbInput.AppendText("\nPipe " + (pipeCount + 1) + " does not have scalar enabled on pipe/plane");
                return uPipeDownScale;
            }

            


            if ((uScalar_CTL[0] & 0x8E000000) == 0x80000000)
            {
                rtbInput.AppendText("\nScalar 0 enabled for pipe:" + (pipeCount + 1));

                uint temp = uPipe_SRC_SZ[0];

                UInt64 a = (((uPipe_SRC_SZ[pipeCount] & 0x1FFF0000) >> 16) + 1)* 1000;
                rtbInput.AppendText("Plane Source Size:" + a);
                UInt64 b = (uScalar_Dest_SZ[0] & 0x1FFF0000) >> 16;
                rtbInput.AppendText("Plane Source Size:" + b);

                if (b == 0)
                    b = 1;

                uHorizontalDownScale = a / b;
                rtbInput.AppendText("Down scaling Amount Horizontal :" + uHorizontalDownScale);

                
                if (uHorizontalDownScale <= 1000)
                {
                    rtbInput.AppendText("\nPipe:" + (pipeCount + 1) + " horizontal down scaling not enabled");
                    uHorizontalDownScale = 1000;
                }

                UInt64 a1 = ((uPipe_SRC_SZ[pipeCount] & 0x00000FFF) + 1)*1000;
                rtbInput.AppendText("Plane Source Size:" + a1);
                UInt64 b1 = (uScalar_Dest_SZ[0] & 0x00000FFF);
                rtbInput.AppendText("Plane destination Size:" + b1);
                if (b1 == 0)
                    b1 = 1;
                uVerticalDownScale = a1 / b1;
                rtbInput.AppendText("Down scaling Amount vertical :" + uVerticalDownScale);

                if (uVerticalDownScale <= 1000)
                {
                    rtbInput.AppendText("\nPipe:" + (pipeCount + 1) + " vertical down scaling not enabled");
                    uVerticalDownScale = 1000;
                }
                uPipeDownScale = uHorizontalDownScale * uVerticalDownScale;
            }
            else if ((uScalar_CTL[1] & 0x8E000000) == 0x80000000)
            {
                rtbInput.AppendText("\nScalar 1 enabled for pipe:" + (pipeCount + 1));

                UInt64 a4 = (((uPipe_SRC_SZ[pipeCount] & 0x1FFF0000) >> 16) + 1) * 1000;
                UInt64 b4 = (uScalar_Dest_SZ[1] & 0x1FFF0000) >> 16;

                if (b4 == 0)
                    b4 = 1;

                uHorizontalDownScale = a4 / b4;

               
                if (uHorizontalDownScale <= 1000)
                {
                    rtbInput.AppendText("\nPipe:" + (pipeCount + 1) + " horizontal down scaling not enabled");
                    uHorizontalDownScale = 1000;
                }


                UInt64 a5 = ((uPipe_SRC_SZ[pipeCount] & 0x00000FFF) + 1)*1000;
                UInt64 b5 = (uScalar_Dest_SZ[1] & 0x00000FFF);

                if (b5 == 0)
                    b5 = 1;
                uVerticalDownScale = a5 / b5; 
              
                if (uVerticalDownScale <= 1000)
                {
                    rtbInput.AppendText("\nPipe:" + (pipeCount + 1) + " vertical down scaling not enabled");
                    uVerticalDownScale = 1000;
                }
                uPipeDownScale = uHorizontalDownScale * uVerticalDownScale;
            }
            else
            {
                rtbInput.AppendText("\nPipe scalar not enabled for pipe:" + (pipeCount + 1));
            }
            return uPipeDownScale;
        }

        private void InitializePlaneRegisters(int pipeCount)
        {
            if (pipeCount == 0)
            {
                reg.ReadRegister((uint)0x70180, ref uPlane_CTL[0]);
                reg.ReadRegister((uint)0x70280, ref uPlane_CTL[1]);
                reg.ReadRegister((uint)0x70380, ref uPlane_CTL[2]);
                reg.ReadRegister((uint)0x70190, ref uPlane_SZ[0]);
                reg.ReadRegister((uint)0x70290, ref uPlane_SZ[1]);
                reg.ReadRegister((uint)0x70390, ref uPlane_SZ[2]);
                reg.ReadRegister((uint)0x7027C, ref uPlane_BUF_CFG[0]);
                reg.ReadRegister((uint)0x7037C, ref uPlane_BUF_CFG[1]);
                reg.ReadRegister((uint)0x7047C, ref uPlane_BUF_CFG[2]);
                reg.ReadRegister((uint)0x70278, ref uPlane_NV12_BUF_CFG[0]);
                reg.ReadRegister((uint)0x70378, ref uPlane_NV12_BUF_CFG[1]);
                reg.ReadRegister((uint)0x70478, ref uPlane_NV12_BUF_CFG[2]);
            }
            if (pipeCount == 1)
            {
                reg.ReadRegister((uint)0x71180, ref uPlane_CTL[0]);
                reg.ReadRegister((uint)0x71280, ref uPlane_CTL[1]);
                reg.ReadRegister((uint)0x71380, ref uPlane_CTL[2]);
                reg.ReadRegister((uint)0x71190, ref uPlane_SZ[0]);
                reg.ReadRegister((uint)0x71290, ref uPlane_SZ[1]);
                reg.ReadRegister((uint)0x71390, ref uPlane_SZ[2]);
                reg.ReadRegister((uint)0x7127C, ref uPlane_BUF_CFG[0]);
                reg.ReadRegister((uint)0x7137C, ref uPlane_BUF_CFG[1]);
                reg.ReadRegister((uint)0x7147C, ref uPlane_BUF_CFG[2]);
                reg.ReadRegister((uint)0x71278, ref uPlane_NV12_BUF_CFG[0]);
                reg.ReadRegister((uint)0x71378, ref uPlane_NV12_BUF_CFG[1]);
                reg.ReadRegister((uint)0x71478, ref uPlane_NV12_BUF_CFG[2]);
            }
            if (pipeCount == 2)
            {
                reg.ReadRegister((uint)0x72180, ref uPlane_CTL[0]);
                reg.ReadRegister((uint)0x72280, ref uPlane_CTL[1]);
                reg.ReadRegister((uint)0x72380, ref uPlane_CTL[2]);
                reg.ReadRegister((uint)0x72190, ref uPlane_SZ[0]);
                reg.ReadRegister((uint)0x72290, ref uPlane_SZ[1]);
                reg.ReadRegister((uint)0x72390, ref uPlane_SZ[2]);
                reg.ReadRegister((uint)0x7227C, ref uPlane_BUF_CFG[0]);
                reg.ReadRegister((uint)0x7237C, ref uPlane_BUF_CFG[1]);
                reg.ReadRegister((uint)0x7247C, ref uPlane_BUF_CFG[2]);
                reg.ReadRegister((uint)0x72278, ref uPlane_NV12_BUF_CFG[0]);
                reg.ReadRegister((uint)0x72378, ref uPlane_NV12_BUF_CFG[1]);
                reg.ReadRegister((uint)0x72478, ref uPlane_NV12_BUF_CFG[2]);
            }
        }

        private void CalculateMemoryLatency()
        {
            reg.ReadRegister((uint)0x45004, ref uArb_Ctl2);


            UInt32 uMailbox_Data0 = 0;
            UInt32 uMailbox_Data1 = 0;
            UInt32 uMailbox_Interface = 0x80000006;     //As per Bspec with Error code =06h and Run/busy=1
            UInt32 uLatency_Data0 = 0;
            UInt32 uLatency_Data1 = 0;
           
            rtbInput.AppendText("Entered to Memory Latency Function ");

            //Write the Mailbox register value

            writeMMIOReg(0x138128, uMailbox_Data0);
            writeMMIOReg(0x13812C, uMailbox_Data1);
            writeMMIOReg(0x138124, uMailbox_Interface);

            readMMIOReg((uint)0x138124, ref uMailbox_Interface);
            readMMIOReg((uint)0x138124, ref uMailbox_Interface);
           
            //Read the Set One Latency Value
            readMMIOReg((uint)0x138128, ref uLatency_Data0);

            uMailbox_Data0 = 1;
            uMailbox_Data1 = 0;
            uMailbox_Interface = 0x80000006;

            //Write the Mailbox register value

            writeMMIOReg(0x138128, uMailbox_Data0);
            writeMMIOReg(0x13812C, uMailbox_Data1);
            writeMMIOReg(0x138124, uMailbox_Interface);

            readMMIOReg((uint)0x138124, ref uMailbox_Interface);
            readMMIOReg((uint)0x138124, ref uMailbox_Interface);
           

            //Read the Set One Latency Value
            readMMIOReg((uint)0x138128, ref uLatency_Data1);

            Latency[0] = (UInt16)(uLatency_Data0 & 0x000000FF);
            Latency[1] = (UInt16)((uLatency_Data0 & 0x0000FF00) >> 8);
            Latency[2] = (UInt16)((uLatency_Data0 & 0x00FF0000) >> 16);
            Latency[3] = (UInt16)((uLatency_Data0 & 0xFF000000) >> 24);
            Latency[4] = (UInt16)(uLatency_Data1 & 0x000000FF);
            Latency[5] = (UInt16)((uLatency_Data1 & 0x0000FF00) >> 8);
            Latency[6] = (UInt16)((uLatency_Data1 & 0x00FF0000) >> 16);
            Latency[7] = (UInt16)((uLatency_Data1 & 0xFF000000) >> 24);

            //Check for BXT whether it is valid or not

            if (Latency[0] == 0)
            {
            Latency[0] = (UInt16)(Latency[0] + 2); 
            Latency[1] = (UInt16)(Latency[1] + 2); 
            Latency[2] = (UInt16)(Latency[2] + 2); 
            Latency[3] = (UInt16)(Latency[3] + 2); 
            Latency[4] = (UInt16)(Latency[4] + 2); 
            Latency[5] = (UInt16)(Latency[5] + 2); 
            Latency[6] = (UInt16)(Latency[6] + 2);
            Latency[7] = (UInt16)(Latency[7] + 2); 
            }

            // If IPC is enabled for KBL , then 4us synthetic latency should be added

            if ((Platform_Selected == "KBL") && ((uArb_Ctl2 & 0x00000008) == 0x00000008))
            {
                Latency[0] = (UInt16)(Latency[0] + 4);
                Latency[1] = (UInt16)(Latency[1] + 4);
                Latency[2] = (UInt16)(Latency[2] + 4);
                Latency[3] = (UInt16)(Latency[3] + 4);
                Latency[4] = (UInt16)(Latency[4] + 4);
                Latency[5] = (UInt16)(Latency[5] + 4);
                Latency[6] = (UInt16)(Latency[6] + 4);
                Latency[7] = (UInt16)(Latency[7] + 4); 
            }

            uMem_Latency.Add(Latency[0]);
            uMem_Latency.Add(Latency[1]);
            uMem_Latency.Add(Latency[2]);
            uMem_Latency.Add(Latency[3]);
            uMem_Latency.Add(Latency[4]);
            uMem_Latency.Add(Latency[5]);
            uMem_Latency.Add(Latency[6]);
            uMem_Latency.Add(Latency[7]);

            rtbInput.AppendText("\n Latency 1:" + Latency[0]);
            rtbInput.AppendText("\n Latency 2:" + Latency[1]);
            rtbInput.AppendText("\n Latency 3:" + Latency[2]);
            rtbInput.AppendText("\n Latency 4:" + Latency[3]);
            rtbInput.AppendText("\n Latency 5:" + Latency[4]);
            rtbInput.AppendText("\n Latency 6:" + Latency[5]);
            rtbInput.AppendText("\n Latency 7:" + Latency[6]);
            rtbInput.AppendText("\n Latency 8:" + Latency[7]);

        }

        private void InitializeMIPIRegisters()
        {

            reg.ReadRegister((uint)0x6B0C0, ref uMIPIA_PortCtrl);
            reg.ReadRegister((uint)0x6B8C0, ref uMIPIC_PortCtrl);
            reg.ReadRegister((uint)0x6B104, ref uMIPIACtrl);
            reg.ReadRegister((uint)0x6B904, ref uMIPICCtrl);
            reg.ReadRegister((uint)0x6B028, ref uMIPI_HSync);
            reg.ReadRegister((uint)0x6B02C, ref uMIPI_HFrontPorch);
            reg.ReadRegister((uint)0x6B030, ref uMIPI_HBackPorch);
            reg.ReadRegister((uint)0x6B034, ref uMIPI_HActive);
            reg.ReadRegister((uint)0x6B00C, ref uMIPIA_DSI);
            reg.ReadRegister((uint)0x6B80C, ref uMIPIC_DSI);
            reg.ReadRegister((uint)0x6B058, ref uMIPIA_VideoMode);
            reg.ReadRegister((uint)0x6B858, ref uMIPIC_VideoMode);
            reg.ReadRegister((uint)0x6B100, ref uMIPIA_VTotal);
            reg.ReadRegister((uint)0x6B900, ref uMIPIC_VTotal);



        }

        private void CalculateArbitratedDisplayBandwidth()
        {
            uint uNumberOfEnabledPipes = 0;
            uint uActualPipePixelRate = 0;
            UInt64 uAdjustedPipePixelRate = 1, uAdjustedPlanePixelRate = 0;
            UInt64 uPipeScalar = 1, uPlaneScalar = 1;
            double uArbitratedBW = 0;
            uint uNoPlanes = 0;
            bool uYtileenabled = false;
            int i = 0;

            uNumberOfEnabledPipes = sysConfigData.uiNDisplays;
            InitializePipeRegisters();//To get pipe source size, later used in scalar value calculation for pipe

            for (int loop = 0; loop < uNumberOfEnabledPipes; loop++)
            {
                i = loop;
                //Calculate adjusted pipe pixel rate 
                PixelClock pix = new PixelClock();

                if (loop == 0)
                {
                    if (MonitorID1.Contains("Pipe 1 Disp MonitorID") == false)              //For Display 1 (Pipe1)
                    {
                        MonitorID[i] = Convert.ToUInt32(MonitorID1);
                        uActualPipePixelRate = (uint)pix.GetCurrentMode(MonitorID[i]);
                    }
                    else
                    {
                        if (MonitorID2.Contains("Pipe 2 Disp MonitorID") == false)              //For Display 1 (Pipe1)
                        {
                            i = i + 1;
                            MonitorID[i] = Convert.ToUInt32(MonitorID2);
                            uActualPipePixelRate = (uint)pix.GetCurrentMode(MonitorID[i]);
                        }
                        else
                        {
                            i = i + 2;
                            MonitorID[i] = Convert.ToUInt32(MonitorID3);
                            uActualPipePixelRate = (uint)pix.GetCurrentMode(MonitorID[i]);
                        }
                    }
                }

                if (loop == 1)                                 //For Display 2  (Pipe2)
                {
                    if (MonitorID1.Contains("Pipe 1 Disp MonitorID") == true)              //For Display 1 (Pipe1)
                    {
                        i = i + 1;
                        MonitorID[i] = Convert.ToUInt32(MonitorID3);
                        uActualPipePixelRate = (uint)pix.GetCurrentMode(MonitorID[i]);
                    }
                    else
                    {
                        if (MonitorID2.Contains("Pipe 2 Disp MonitorID") == false)              //For Display 1 (Pipe1)
                        {
                            MonitorID[i] = Convert.ToUInt32(MonitorID2);
                            uActualPipePixelRate = (uint)pix.GetCurrentMode(MonitorID[i]);
                        }
                        else
                        {
                            i = i + 1;
                            MonitorID[i] = Convert.ToUInt32(MonitorID3);
                            uActualPipePixelRate = (uint)pix.GetCurrentMode(MonitorID[i]);
                        }
                    }
				}

                if (loop == 2)                                    //For Display 3 (Pipe3)
                {
                    MonitorID[i] = Convert.ToUInt32(MonitorID3);
                    uActualPipePixelRate = (uint)pix.GetCurrentMode(MonitorID[i]);
                }



                uAdjustedPipePixelRate = uActualPipePixelRate;
                // uAdjustedPipePixelRate = Manual_Pixel_Clock;    //Considering Pixel value in khz

                //If TRANS_CONF Interlaced Mode == PF-ID, adjusted pipe pixel rate = adjusted pipe pixel rate * 2 
                if (sysConfigData.DispCfg[loop].Resolution.InterlaceFlag != 0)
                {
                    uAdjustedPipePixelRate = uAdjustedPipePixelRate * 2;
                }
                //If pipe scaling enabled, adjusted pipe pixel rate = adjusted pipe pixel rate * pipe down scale amount 
                InitializeScalarRegisters(i);
                uPipeScalar = GetPipeScalar(i);
                uAdjustedPipePixelRate = (uAdjustedPipePixelRate * uPipeScalar) / 1000000;
                
 

                InitializePlaneRegisters(i);
                for (int j = 0; j < 3 && (uPlane_CTL[j] & 0x80000000) == 0x80000000; j++)
                {
                    uNoPlanes++;
                    uAdjustedPlanePixelRate = uAdjustedPipePixelRate;
                    uPlaneScalar = GetPlaneScalar(i, j);

                    uAdjustedPlanePixelRate = (uAdjustedPipePixelRate * uPlaneScalar) / 1000000;
                    double BPP = 0;


                    uint A1 = (uPlane_CTL[j] & 0x0F000000) >> 24;

                    if (A1 == 1)
                        BPP = 1.5;
                    else if (A1 == 0 || A1 == 14)
                        BPP = 2;
                    else if (A1 == 6)
                        BPP = 8;
                    else if (A1 == 12)
                        BPP = 1;
                    else
                        BPP = sysConfigData.DispCfg[loop].Resolution.dwBPP / 8;

                    uPlaneBW[i, j] = uAdjustedPlanePixelRate * BPP;

                    if ((uPlane_CTL[j] & 0x00001000) == 0x00001000)
                    {
                        uYtileenabled = true;
                    }
                }
                uPipeBW[i] = Math.Max(Math.Max(uPlaneBW[i, 0], uPlaneBW[i, 1]), uPlaneBW[i, 2]) * uNoPlanes;
                uNoPlanes = 0;
            }
            uArbitratedBW = Math.Max(Math.Max(uPipeBW[0], uPipeBW[1]), uPipeBW[2]) * uNumberOfEnabledPipes;
            rtbInput.AppendText("\n Arbitrated Bandwidth: " + uArbitratedBW);

            //Checking system memory bandwidth

            if (Platform_Selected == "BXT") 
            {
                readMMIOReg((uint)0x147114, ref uMemoryFreqRegister);
                readMMIOReg((uint)0x147114, ref uMemoryChannel0);
                readMMIOReg((uint)0x147114, ref uMemoryChannel1);

                if ((uMemoryChannel0 & 0x00005000) == 0x00005000)
                {
                    uNoMemoryChannel++;
                }
                if ((uMemoryChannel1 & 0x0000A000) == 0x0000A000)
                {
                    uNoMemoryChannel++;
                }
                uMemoryFrequency = uMemoryFreqRegister & 0x0000003F;
                uMemoryFrequency = uMemoryFrequency * 133.33;
            }
            else
            {
                readMMIOReg((uint)0x145E04, ref uMemoryFreqRegister);
                readMMIOReg((uint)0x14500C, ref uMemoryChannel0);
                readMMIOReg((uint)0x145010, ref uMemoryChannel1);

                if (uMemoryChannel0 > 0)
                {
                    uNoMemoryChannel++;
                }
                if (uMemoryChannel1 > 0)
                {
                    uNoMemoryChannel++;
                }
                uMemoryFrequency = uMemoryFreqRegister & 0x0000000F;
                uMemoryFrequency = uMemoryFrequency * 133.33 * 2;
                
                // if any one slot has dual rank memory , then consider as dual rank
                if (((uMemoryChannel0 & 0x00000400) == 0x00000400) ||  ((uMemoryChannel0 & 0x04000000) == 0x04000000))
                {
                    uMemoryRankCh0 = 2;
                }

                if (((uMemoryChannel1 & 0x00000400) == 0x00000400) || ((uMemoryChannel1 & 0x04000000) == 0x04000000))
                {
                    uMemoryRankCh1 = 2;
                }

                // if both slots have single rank memory then consider as dual rank
                if ((((uMemoryChannel0 & 0x0000003f) > 0) && ((uMemoryChannel0 & 0x04000000) == 0x00000000)) && (((uMemoryChannel0 & 0x0000003f) > 0) && ((uMemoryChannel0 & 0x00000400) == 0x00000000)))
                {
                    uMemoryRankCh0 = 2;
                }

                if ((((uMemoryChannel1 & 0x0000003f) > 0) && ((uMemoryChannel1 & 0x04000000) == 0x00000000)) && (((uMemoryChannel1 & 0x0000003f) > 0) && ((uMemoryChannel1 & 0x00000400) == 0x00000000)))
                {
                    uMemoryRankCh1 = 2;
                }

                uMemoryRank = Math.Min(uMemoryRankCh0, uMemoryRankCh1);
            }

            uRawSystemBW = uMemoryFrequency * 8 * uNoMemoryChannel * 1000; // multiply by 1000 to convert from Mhz to Khz
            rtbInput.AppendText("\n System Bandwidth: " + uRawSystemBW);

            if ((uArbitratedBW > uRawSystemBW * 0.2) && (uYtileenabled == true)) 
            {
                uWM_wa = 1;
                rtbInput.AppendText("\n Ytile 20% WA enabled");
            }
            else if ((uNumberOfEnabledPipes>1) && (uArbitratedBW > 6000000) && (uYtileenabled == true) && ((Platform_Selected == "SKL") || (Platform_Selected == "KBL")))
            {
                uWM_wa = 1;
                rtbInput.AppendText("\n Ytile 20% WA enabled , Arb BW exceeded 6Gbps and pipecount > 1");
            }

            else if (((uNoMemoryChannel == 2) && (uMemoryRank == 1)) && (uArbitratedBW > uRawSystemBW * 0.35))
            {
                uWM_wa = 2;
                rtbInput.AppendText("\n Xtile 35% WA enabled");
            }

            else if (uArbitratedBW > uRawSystemBW * 0.6)
            {
                uWM_wa = 2;
                rtbInput.AppendText("\n Xtile 60% WA enabled");
            }
        }

        private void textBox1_TextChanged(object sender, EventArgs e)
        {
            MonitorID1 = textBox1.Text;
        }

        private void textBox2_TextChanged(object sender, EventArgs e)
        {
            MonitorID2 = textBox2.Text;
        }

        private void textBox3_TextChanged(object sender, EventArgs e)
        {
            MonitorID3 = textBox3.Text;
        }

        private void button1_Click(object sender, EventArgs e)
        {
            Time = 15;
        }
    }
}
