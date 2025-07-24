using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Windows.Forms;
using SERVER;
using Client;
using System.IO;
using System.Windows.Automation;
using System.Reflection;
using System.Diagnostics;
using System.Net;
using System.Net.Sockets;
using Microsoft.Win32;
using IgfxExtBridge_DotNet;
using System.Threading;



namespace DP_Compliance_Client_Console
{
    class Program
    {
//Get Local Ip address
       static private string GetLocalIP()
        {

            IPHostEntry host;
            host = Dns.GetHostEntry(Dns.GetHostName());
            foreach (IPAddress ip in host.AddressList)
            {
                if (ip.AddressFamily == AddressFamily.InterNetwork)
                {

                    return ip.ToString();
                }

            }
            return "127.0.0.1";
        }

//Convert Scaling function
       static public GENERIC ConvertScaling(string panelFit)
       {
           switch (panelFit)
           {
               case "MDS":
                   return GENERIC.IGFX_MAINTAIN_DISPLAY_SCALING;
               case "CAR":
                   return GENERIC.IGFX_SCALING_CUSTOM;
               case "MAR":
                   return GENERIC.IGFX_ASPECT_SCALING;
               case "CI":
                   return GENERIC.IGFX_CENTERING;               
               case "FS":
                   return GENERIC.IGFX_PANEL_FITTING;
               default:
                   return GENERIC.IGFX_MAINTAIN_DISPLAY_SCALING;
           }

       }

       static public void FillDevideIDs(ref IGFX_SYSTEM_CONFIG_DATA_N_VIEWS systemCfgData, string display1, string display2)
       {
           if (display1 == "eDP" || display2 == "eDP")
           {
               switch (display1)
               {
                   case "eDP":
                       systemCfgData.DispCfg[0].dwDisplayUID = 4096;
                       break;
                   case "DP":
                   case "HDMI":
                       systemCfgData.DispCfg[0].dwDisplayUID = 256;
                       break;
               }
               switch (display2)
               {
                   case "eDP":
                       systemCfgData.DispCfg[1].dwDisplayUID = 4096;
                       break;
                   case "DP":
                   case "HDMI":
                       systemCfgData.DispCfg[1].dwDisplayUID = 256;
                       break;
               }
           }

           if (display1 == "DP" &&  display2 == "HDMI" || display1 == "HDMI" &&  display2 == "DP")
           {
               switch (display1)
               {
                   case "DP":
                       systemCfgData.DispCfg[0].dwDisplayUID = 265;
                       break;                   
                   case "HDMI":
                       systemCfgData.DispCfg[0].dwDisplayUID = 512;
                       break;
               }
               switch (display2)
               {
                   case "DP":
                       systemCfgData.DispCfg[1].dwDisplayUID = 265;
                       break;
                   case "HDMI":
                       systemCfgData.DispCfg[1].dwDisplayUID = 512;
                       break;
               }
           }

       }

       static public void FillModeDetails(ref IGFX_SYSTEM_CONFIG_DATA_N_VIEWS systemCfgData, string dataReceived)        
       {
          
           string[] data = dataReceived.Split('_');

           switch (data[0])
           {
               case "ED":
                   systemCfgData.dwOpMode = (uint)DISPLAY_DEVICE_CONFIG_FLAG.IGFX_DISPLAY_DEVICE_CONFIG_FLAG_DDEXTD;            
                   break;
               case "CLONE":
                   systemCfgData.dwOpMode = (uint)DISPLAY_DEVICE_CONFIG_FLAG.IGFX_DISPLAY_DEVICE_CONFIG_FLAG_DDCLONE;     
                   break;
            
           }

           systemCfgData.uiNDisplays = 2;
           systemCfgData.uiSize = 152;

           FillDevideIDs(ref systemCfgData, data[1], data[2]);

           //Fill resolution and scaling details for primary Display
           systemCfgData.DispCfg[0].Resolution.dwHzRes = Convert.ToUInt32(data[3]);
           systemCfgData.DispCfg[0].Resolution.dwVtRes = Convert.ToUInt32(data[4]);
           systemCfgData.DispCfg[0].Resolution.dwRR = Convert.ToUInt32(data[5]);
           systemCfgData.DispCfg[0].Resolution.InterlaceFlag = (ushort)((data[6] == "p") ? 0 : 1);
           systemCfgData.DispCfg[0].Resolution.dwBPP = Convert.ToUInt32(data[7]);
           systemCfgData.DispCfg[0].dwScaling = (uint)ConvertScaling(data[8]);

           //Fill resolution and scaling details for secondary Display
           systemCfgData.DispCfg[1].Resolution.dwHzRes = Convert.ToUInt32(data[9]);
           systemCfgData.DispCfg[1].Resolution.dwVtRes = Convert.ToUInt32(data[10]);
           systemCfgData.DispCfg[1].Resolution.dwRR = Convert.ToUInt32(data[11]);
           systemCfgData.DispCfg[1].Resolution.InterlaceFlag = (ushort)((data[12] == "p") ? 0 : 1);
           systemCfgData.DispCfg[1].Resolution.dwBPP = Convert.ToUInt32(data[13]);
           systemCfgData.DispCfg[1].dwScaling = (uint)ConvertScaling(data[14]);
       }

//A function to set resolution
       static bool SetMode(string dataReceived)
       {
           bool result = false;
           DisplayUtil displayUtil = new DisplayUtil();        

           IGFX_ERROR_CODES igfxErrorCode = IGFX_ERROR_CODES.IGFX_SUCCESS;
           string errorDesc = "";
           IGFX_SYSTEM_CONFIG_DATA_N_VIEWS systemCfgData = new IGFX_SYSTEM_CONFIG_DATA_N_VIEWS();
           systemCfgData.DispCfg = new IGFX_DISPLAY_CONFIG_DATA_EX[6];

           FillModeDetails(ref systemCfgData, dataReceived);
           displayUtil.SetSystemConfigDataNViews(ref systemCfgData, out igfxErrorCode, out errorDesc);
           Thread.Sleep(5000);
           if (igfxErrorCode == IGFX_ERROR_CODES.IGFX_SUCCESS)
           {
               Console.Write("SUCCESS to Set Configuration -> ErrorCode: {0}", igfxErrorCode);
               result = true;
           }
           else
           {
               Console.Write("Failed to SetConfiguration -> ErrorCode: {0}", igfxErrorCode);
               result = false;
           }
           return result;
       }

        //Function to enable xvYCC
       static bool Enable_Xvycc(uint hdmi_deviceID)
       {
           bool result = false;
           DisplayUtil displayUtil = new DisplayUtil();

           IGFX_ERROR_CODES igfxErrorCode = IGFX_ERROR_CODES.IGFX_SUCCESS;
           string errorDesc = "";
           IGFX_XVYCC_INFO setxvycc;
           setxvycc = new IGFX_XVYCC_INFO();
           setxvycc.dwDeviceID = hdmi_deviceID;
           setxvycc.bEnableXvYCC = 1;
           displayUtil.SetXvYcc(ref setxvycc, out igfxErrorCode, out errorDesc);           
           if (igfxErrorCode == IGFX_ERROR_CODES.IGFX_SUCCESS)
           {
               Console.Write("SUCCESS to ENABLE XVYCC for HDMI device ID : {0}", hdmi_deviceID);
               result = true;
           }
           else
           {
               Console.Write("Failed to ENABLE XVYCC For HDMI Device ID : {0}  -> ErrorCode: {1}", hdmi_deviceID, igfxErrorCode);
               result = false;
           }
           return result;
       }

        //Disable xvYCC
       static bool Disable_Xvycc(uint hdmi_deviceID)
       {
           bool result = false;
           DisplayUtil displayUtil = new DisplayUtil();

           IGFX_ERROR_CODES igfxErrorCode = IGFX_ERROR_CODES.IGFX_SUCCESS;
           string errorDesc = "";
           IGFX_XVYCC_INFO setxvycc;
           setxvycc = new IGFX_XVYCC_INFO();
           setxvycc.dwDeviceID = hdmi_deviceID;
           setxvycc.bEnableXvYCC = 0;
           displayUtil.SetXvYcc(ref setxvycc, out igfxErrorCode, out errorDesc);
           if (igfxErrorCode == IGFX_ERROR_CODES.IGFX_SUCCESS)
           {
               Console.Write("SUCCESS to DISABLE XVYCC for HDMI device ID : {0}", hdmi_deviceID);
               result = true;
           }
           else
           {
               Console.Write("Failed to DISABLE XVYCC For HDMI Device ID : {0}  -> ErrorCode: {1}", hdmi_deviceID, igfxErrorCode);
               result = false;
           }
           return result;
       }

        //Enable ycbcr
       static bool Enable_Ycbcr(uint hdmi_deviceID)
       {
           bool result = false;
           DisplayUtil displayUtil = new DisplayUtil();

           IGFX_ERROR_CODES igfxErrorCode = IGFX_ERROR_CODES.IGFX_SUCCESS;
           string errorDesc = "";
           IGFX_YCBCR_INFO setYcbcr;
           setYcbcr = new IGFX_YCBCR_INFO();
           setYcbcr.dwDeviceID = hdmi_deviceID;
           setYcbcr.bEnableYCbCr = 1;
           displayUtil.SetYcBcr(ref setYcbcr, out igfxErrorCode, out errorDesc);
           if (igfxErrorCode == IGFX_ERROR_CODES.IGFX_SUCCESS)
           {
               Console.Write("SUCCESS to ENABLE YCBCR for HDMI device ID : {0}", hdmi_deviceID);
               result = true;
           }
           else
           {
               Console.Write("Failed to ENABLE YCBCR For HDMI Device ID : {0}  -> ErrorCode: {1}", hdmi_deviceID, igfxErrorCode);
               result = false;
           }
           return result;
       }

        //Disable ycbcr
       static bool Disable_Ycbcr(uint hdmi_deviceID)
       {
           bool result = false;
           DisplayUtil displayUtil = new DisplayUtil();

           IGFX_ERROR_CODES igfxErrorCode = IGFX_ERROR_CODES.IGFX_SUCCESS;
           string errorDesc = "";
           IGFX_YCBCR_INFO setYcbcr;
           setYcbcr = new IGFX_YCBCR_INFO();
           setYcbcr.dwDeviceID = hdmi_deviceID;
           setYcbcr.bEnableYCbCr = 0;
           displayUtil.SetYcBcr(ref setYcbcr, out igfxErrorCode, out errorDesc);
           if (igfxErrorCode == IGFX_ERROR_CODES.IGFX_SUCCESS)
           {
               Console.Write("SUCCESS to DISABLE YCBCR for HDMI device ID : {0}", hdmi_deviceID);
               result = true;
           }
           else
           {
               Console.Write("Failed to DISABLE YCBCR For HDMI Device ID : {0}  -> ErrorCode: {1}", hdmi_deviceID, igfxErrorCode);
               result = false;
           }
           return result;
       }



        static void Main(string[] args)
        {
            uint HDMI_Display_ID = 0;//HDMI Device ID 

            Console.Write(" Client IP Adddress \r \n");
            Console.Write( GetLocalIP()+"\n \r");
            Console.Write("  \r \n");
            Console.Write(" Enter Server IP Adddress \r \n");
            string Server_IP = Console.ReadLine();

            string Val = "0";

            Console.Write(" Please Enter the DUT Configuration \r \n ");
            Console.Write(" Press 1 for eDP + HDMI \r \n  Press 2 for DP + HDMI \r \n  Press 3 for eDP + DP \r \n");

            //Read Continuosly until valid configuration is entered
            while (true)
            {
                Val = Console.ReadLine();
                //read continuously until valid configuration is pressed otherwise display a warning message and continue reading until valid number is pressed
                if (Val == "1" || Val == "2" || Val == "3")
                {
                    break;
                }
                else 
                {
                    Console.WriteLine(" Please Enter the Valid Configuration \r" );
                }

            }

            // eDP+HDMI Device ID 256
            if (Val == "1")
            {
              HDMI_Display_ID = 256;
            }

            //DP+HDMI Device ID 512
            else if (Val == "2")
            {
                HDMI_Display_ID = 512;
            }

            while (true)
            {

                string data_rece;

                SERVER.Class1 server1 = new SERVER.Class1();
                data_rece = server1.Server();
                
                
                string turnoff = "mOFF";
                string two4824bit = "2_Channel_48000Hz_24bits_20s.wav";
                string Eight4824bit = "8_Channel_48000Hz_24bits_20s.wav";
                string two19224bit = "2_Channel_192000Hz_24bits_20s.wav";
                string two19216bit = "2_Channel_192000Hz_16bits_20s.wav";
                string Eaght19224bit = "8_Channel_192000Hz_24bits_20s.wav";
              //  string Eaght19216bit = "8_Channel_192000Hz_16bits_20s.wav";
                string Eaght19216bit = "Sine_SevenPointOneSurround_192000Hz_16bits_20s.wav";
                string HDCP = "ENABLE_HDCP";
              //  string dts_hd = "Tone_71_BDMA.dtshd";

                string xvYCC_var_enable = "Enable_xvYcc";
                string xvYCC_var_disable = "Disable_xvYcc";
                string YCbCr_var_enable = "Enable_YCbCr";
                string YCbCr_var_disable = "Disable_YCbCr";

                //Audio Compliance 
                //Play 2 channel or 8 channel Audio
                if (data_rece == two4824bit || data_rece == Eight4824bit || data_rece == two19224bit || data_rece == Eaght19224bit || data_rece == two19216bit || data_rece == Eaght19216bit)
                {

                    foreach (var process in Process.GetProcessesByName("HBRPlayerGUI"))
                    {
                        process.Kill();
                    }

                    System.Threading.Thread.Sleep(8000);
                    Process myProcess = new Process();
                    myProcess.StartInfo.WorkingDirectory = @"C:\HBR Player\";
                    myProcess.StartInfo.FileName = "HBRPlayerGUI.exe";
                    myProcess.StartInfo.Verb = "runas";
                    System.Threading.Thread.Sleep(4000);
                    myProcess.Start();
                    System.Threading.Thread.Sleep(4000);

                    AutomationElement pcm_button = SelectElementNameControlType("PCM", ControlType.RadioButton);
                    SelectionItem(pcm_button);
                    System.Threading.Thread.Sleep(2000);

                    AutomationElement File_Open = SelectElementNameControlType("File", ControlType.Button);
                    Invoke(File_Open);
                    System.Threading.Thread.Sleep(4000);
                    System.Windows.Forms.SendKeys.SendWait("C:\\HBR Player\\");
                    System.Windows.Forms.SendKeys.SendWait(data_rece);
                    System.Threading.Thread.Sleep(2000);
                  
                    AutomationElement Open = SelectElementNameControlType("Open", ControlType.Button);
                    Invoke(Open);
                    System.Threading.Thread.Sleep(2000);

                    AutomationElement ClickOK = SelectElementNameControlType("Play", ControlType.Button);
                    Invoke(ClickOK);     
                    System.Threading.Thread.Sleep(2000);

                    send_pass_function(Server_IP);// Send an acknowledgement that audio is played
                    
                }
                    
                  //Play dts_hd audio
                else if (data_rece == "Tone_71_BDMA.dtshd")
                {
                    foreach (var process in Process.GetProcessesByName("HBRPlayerGUI"))
                    {
                        process.Kill();
                    }

                    System.Threading.Thread.Sleep(8000);
                    Process myProcess = new Process();
                    myProcess.StartInfo.WorkingDirectory = @"C:\HBR Player\";
                    myProcess.StartInfo.FileName = "HBRPlayerGUI.exe";
                    myProcess.StartInfo.Verb = "runas";
                    System.Threading.Thread.Sleep(4000);
                    myProcess.Start();
                    System.Threading.Thread.Sleep(4000);

                    AutomationElement dts_button = SelectElementNameControlType("DTS HD", ControlType.RadioButton);
                    SelectionItem(dts_button);
                    System.Threading.Thread.Sleep(2000);

                    AutomationElement File_Open = SelectElementNameControlType("File", ControlType.Button);
                    Invoke(File_Open);
                    System.Threading.Thread.Sleep(4000);
                    System.Windows.Forms.SendKeys.SendWait("C:\\HBR Player\\");
                    System.Windows.Forms.SendKeys.SendWait(data_rece);
                    System.Threading.Thread.Sleep(2000);

                    AutomationElement Open = SelectElementNameControlType("Open", ControlType.Button);
                    Invoke(Open);
                    System.Threading.Thread.Sleep(2000);

                    AutomationElement ClickOK = SelectElementNameControlType("Play", ControlType.Button);
                    Invoke(ClickOK);

                    System.Threading.Thread.Sleep(2000);
                    send_pass_function(Server_IP);//Send an Acknowledgement that required audio is played 

                }

                    //close hbr app
                else if (data_rece == "CloseHBR")
                {
                    foreach (var process in Process.GetProcessesByName("HBRPlayerGUI"))
                    {
                        process.Kill();
                    }

                    send_pass_function(Server_IP);//Send an acknowledgement that the required task is completed

                }

                    //close all apps
                else if (data_rece == "CloseAllApps")
                {
                    foreach (var process in Process.GetProcessesByName("HBRPlayerGUI"))
                    {
                        process.Kill();
                    }

                    System.Threading.Thread.Sleep(3000);

                    foreach (var process in Process.GetProcessesByName("DP_Compliance_Client_Console"))
                    {
                        process.Kill();
                    }
                }

                    //Enable xvycc in the client
                else if (data_rece == xvYCC_var_enable)
                {
                    Enable_Xvycc(HDMI_Display_ID);
                    System.Threading.Thread.Sleep(1000);
                    send_pass_function(Server_IP);//Send an acknowledgement that the required task is completed
                }

                    //Disable xvycc in client
                else if (data_rece == xvYCC_var_disable)
                {
                    Disable_Xvycc(HDMI_Display_ID);
                    System.Threading.Thread.Sleep(1000);
                    send_pass_function(Server_IP);//Send an acknowledgement that the required task is completed
                }

                    //Enable ycbcr in client
                else if (data_rece == YCbCr_var_enable)
                {
                    Enable_Ycbcr(HDMI_Display_ID);
                    System.Threading.Thread.Sleep(2000);
                    send_pass_function(Server_IP);//Send an acknowledgement that the required task is completed
                }

                    //Disable ycbcr in client
                else if (data_rece == YCbCr_var_disable)
                {
                    Disable_Ycbcr(HDMI_Display_ID);
                    System.Threading.Thread.Sleep(1000);
                    send_pass_function(Server_IP);//Send an acknowledgement that the required task is completed
                }

                else if (data_rece == HDCP)
                {

                    foreach (var process in Process.GetProcessesByName("OPMTester"))
                    {
                        process.Kill();
                    }
                    Process myProcess = new Process();
                    myProcess.StartInfo.WorkingDirectory = @"C:\OPM Tester\";
                    myProcess.StartInfo.FileName = "OPMTester.exe";
                    myProcess.StartInfo.Verb = "runas";
                    myProcess.Start();

                    System.Threading.Thread.Sleep(3000);
                    AutomationElement ClickYes = SelectElementNameControlType("Yes", ControlType.Button);
                    Invoke(ClickYes);
                    System.Threading.Thread.Sleep(2000);

                    AutomationElement MenuElement_File = SelectElementNameControlType("File", ControlType.MenuItem);
                    ExpandCollapse(MenuElement_File);

                    System.Threading.Thread.Sleep(2000);
                    AutomationElement MenuElement_OpenClip = SelectElementNameControlType("Open Clip", ControlType.MenuItem);
                    Invoke(MenuElement_OpenClip);

                    System.Threading.Thread.Sleep(4000);
                    System.Windows.Forms.SendKeys.SendWait("C:\\OPM Tester\\baseball.mpeg");
                    System.Windows.Forms.SendKeys.SendWait("{ENTER}");

                    System.Threading.Thread.Sleep(2000);
                    AutomationElement MenuElement_OPM = SelectElementNameControlType("OPM", ControlType.MenuItem);
                    ExpandCollapse(MenuElement_OPM);

                    System.Windows.Forms.SendKeys.SendWait("{RIGHT 1}");
                    System.Threading.Thread.Sleep(1000);
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 2}");
                    System.Threading.Thread.Sleep(1000);
                    System.Windows.Forms.SendKeys.SendWait("{RIGHT 1}");
                    System.Threading.Thread.Sleep(1000);
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 1}");
                    System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                    System.Threading.Thread.Sleep(1000);
                    Client.Class1 Client1 = new Client.Class1();
                    Client1.Client(Server_IP, " PASS");

                }

                else if(data_rece == "1024x768@60MDSCLONE")
                {
                    data_rece = "CLONE_eDP_HDMI_1024_768_60_p_32_MAR_1024_768_60_p_32_MDS";
                    SetMode(data_rece);
                    System.Threading.Thread.Sleep(1000);
                    send_pass_function(Server_IP);//Send an acknowledgement that the required task is completed
                }

                else if (data_rece == "800x600@60MDS8BPC")
                {
                    data_rece = "CLONE_eDP_DP_800_600_60_p_32_MAR_800_600_60_p_32_MDS";
                    SetMode(data_rece);
                    System.Threading.Thread.Sleep(1000);
                    Client.Class1 Client1 = new Client.Class1();
                    Client1.Client(Server_IP, "PASS");
                }

                    //Apply ED mode with required resolution
                else if (data_rece == "720x480@60MDS8BPC")
                {
                    data_rece = "ED_eDP_HDMI_1024_768_60_p_32_MAR_720_480_60_p_32_MDS";
                    SetMode(data_rece);
                    System.Threading.Thread.Sleep(1000);
                    send_pass_function(Server_IP);//Send an acknowledgement that the required task is completed
                }

                    //Apply ED mode with required resolution
                else if (data_rece == "720x480@59MDS8BPC")
                {
                    data_rece = "ED_eDP_HDMI_1024_768_60_p_32_MAR_720_480_59_p_32_MDS";
                    SetMode(data_rece);
                    System.Threading.Thread.Sleep(1000);
                    send_pass_function(Server_IP);//Send an acknowledgement that the required task is completed
                }

                //Apply ED mode with required resolution
                else if (data_rece == "640x480@60MDS8BPC")
                {
                    data_rece = "ED_eDP_HDMI_1024_768_60_p_32_MAR_640_480_60_p_32_MDS";
                    SetMode(data_rece);
                    System.Threading.Thread.Sleep(1000);
                    send_pass_function(Server_IP);//Send an acknowledgement that the required task is completed
                }

                //Apply ED mode with required resolution
                else if (data_rece == "640x480@59MDS8BPC")
                {
                    data_rece = "ED_eDP_HDMI_1024_768_60_p_32_MAR_640_480_59_p_32_MDS";
                    SetMode(data_rece);
                    System.Threading.Thread.Sleep(1000);
                    send_pass_function(Server_IP);//Send an acknowledgement that the required task is completed
                }

                //Apply ED mode with required resolution
                else if (data_rece == "1280x720@60MDS8BPC")
                {
                    data_rece = "ED_eDP_HDMI_1024_768_60_p_32_MAR_1280_720_60_p_32_MDS";
                    SetMode(data_rece);
                    System.Threading.Thread.Sleep(1000);
                    send_pass_function(Server_IP);//Send an acknowledgement that the required task is completed
                }

                //Apply ED mode with required resolution
                else if (data_rece == "1280x720@59MDS8BPC")
                {
                    data_rece = "ED_eDP_HDMI_1024_768_60_p_32_MAR_1280_720_59_p_32_MDS";
                    SetMode(data_rece);
                    System.Threading.Thread.Sleep(1000);
                    send_pass_function(Server_IP);//Send an acknowledgement that the required task is completed
                }

                //Apply ED mode with required resolution
                else if (data_rece == "1280x720@50MDS8BPC")
                {
                    data_rece = "ED_eDP_HDMI_1024_768_60_p_32_MAR_1280_720_50_p_32_MDS";
                    SetMode(data_rece);
                    System.Threading.Thread.Sleep(1000);
                    send_pass_function(Server_IP);//Send an acknowledgement that the required task is completed
                }

                //Apply ED mode with required resolution
                else if (data_rece == "1280x720@49MDS8BPC")
                {
                    data_rece = "ED_eDP_HDMI_1024_768_60_p_32_MAR_1280_720_49_p_32_MDS";
                    SetMode(data_rece);
                    System.Threading.Thread.Sleep(1000);
                    send_pass_function(Server_IP);//Send an acknowledgement that the required task is completed
                }

                    //Apply ED mode with required resolution
                else if (data_rece == "1920x1080@60MDS8BPC")
                {
                    data_rece = "ED_eDP_HDMI_1024_768_60_p_32_MAR_1920_1080_60_p_32_MDS";
                    SetMode(data_rece);
                    System.Threading.Thread.Sleep(1000);
                    send_pass_function(Server_IP);//Send an acknowledgement that the required task is completed
                }

                //Apply ED mode with required resolution
                else if (data_rece == "1920x1080@59MDS8BPC")
                {
                    data_rece = "ED_eDP_HDMI_1024_768_60_p_32_MAR_1920_1080_59_p_32_MDS";
                    SetMode(data_rece);
                    System.Threading.Thread.Sleep(1000);
                    send_pass_function(Server_IP);//Send an acknowledgement that the required task is completed
                }

                    //Apply ED mode with required resolution
                else if (data_rece == "1920x1080@50MDS8BPC")
                {
                    data_rece = "ED_eDP_HDMI_1024_768_60_p_32_MAR_1920_1080_50_p_32_MDS";
                    SetMode(data_rece);
                    System.Threading.Thread.Sleep(1000);
                    send_pass_function(Server_IP);//Send an acknowledgement that the required task is completed
                }

                    //Apply ED mode with required resolution
                else if (data_rece == "1920x1080@49MDS8BPC")
                {
                    data_rece = "ED_eDP_HDMI_1024_768_60_p_32_MAR_1920_1080_49_p_32_MDS";
                    SetMode(data_rece);
                    System.Threading.Thread.Sleep(1000);
                    send_pass_function(Server_IP);//Send an acknowledgement that the required task is completed
                }

                    //Apply ED mode with required resolution
                else if (data_rece == "2880x480@60MDS8BPC")
                {
                    data_rece = "ED_eDP_HDMI_1024_768_60_p_32_MAR_2880_480_60_p_32_MDS";
                    SetMode(data_rece);
                    System.Threading.Thread.Sleep(1000);
                    send_pass_function(Server_IP);//Send an acknowledgement that the required task is completed
                }

                                        //Apply ED mode with required resolution
                else if (data_rece == "3840x2160@30MDS8BPC")
                {
                    data_rece = "ED_eDP_HDMI_1024_768_60_p_32_MAR_3840_2160_30_p_32_MDS";
                    SetMode(data_rece);
                    System.Threading.Thread.Sleep(1000);
                    send_pass_function(Server_IP);//Send an acknowledgement that the required task is completed
                }

                //Apply ED mode with required resolution
                else if (data_rece == "3840x2160@25MDS8BPC")
                {
                    data_rece = "ED_eDP_HDMI_1024_768_60_p_32_MAR_3840_2160_25_p_32_MDS";
                    SetMode(data_rece);
                    System.Threading.Thread.Sleep(1000);
                    send_pass_function(Server_IP);//Send an acknowledgement that the required task is completed
                }

                //Apply ED mode with required resolution
                else if (data_rece == "3840x2160@30MDS8BPC")
                {
                    data_rece = "ED_eDP_HDMI_1024_768_60_p_32_MAR_3840_2160_24_p_32_MDS";
                    SetMode(data_rece);
                    System.Threading.Thread.Sleep(1000);
                    send_pass_function(Server_IP);//Send an acknowledgement that the required task is completed
                }

                    //Apply ED mode with required resolution
                else if (data_rece == "720x576@50MDS8BPC")
                {
                    data_rece = "ED_eDP_HDMI_1024_768_60_p_32_MAR_720_576_50_p_32_MDS";
                    SetMode(data_rece);
                    System.Threading.Thread.Sleep(1000);
                    send_pass_function(Server_IP);//Send an acknowledgement that the required task is completed
                }

                    //Apply ED mode with required resolution
                else if (data_rece == "720x576@49MDS8BPC")
                {
                    data_rece = "ED_eDP_HDMI_1024_768_60_p_32_MAR_720_576_49_p_32_MDS";
                    SetMode(data_rece);
                    System.Threading.Thread.Sleep(1000);
                    send_pass_function(Server_IP);//Send an acknowledgement that the required task is completed
                }

                    //Apply ED mode with required resolution
                else if (data_rece == "720x576@i50MDS8BPC")
                {
                    data_rece = "ED_eDP_HDMI_1024_768_60_i_32_MAR_720_576_50_i_32_MDS";
                    SetMode(data_rece);
                    System.Threading.Thread.Sleep(1000);
                    send_pass_function(Server_IP);//Send an acknowledgement that the required task is completed
                }

                    //Apply ED mode with required resolution
                else if (data_rece == "720x576@i49MDS8BPC")
                {
                    data_rece = "ED_eDP_HDMI_1024_768_60_i_32_MAR_720_576_49_i_32_MDS";
                    SetMode(data_rece);
                    System.Threading.Thread.Sleep(1000);
                    send_pass_function(Server_IP);//Send an acknowledgement that the required task is completed
                }

                    //Apply ED mode with required resolution
                else if (data_rece == "1920x1080@i50MDS8BPC")
                {
                    data_rece = "ED_eDP_HDMI_1024_768_60_i_32_MAR_1920_1080_50_i_32_MDS";
                    SetMode(data_rece);
                    System.Threading.Thread.Sleep(1000);
                    send_pass_function(Server_IP);//Send an acknowledgement that the required task is completed
                }

                    //Apply ED mode with required resolution
                else if (data_rece == "1920x1080@i49MDS8BPC")
                {
                    data_rece = "ED_eDP_HDMI_1024_768_60_i_32_MAR_1920_1080_49_i_32_MDS";
                    SetMode(data_rece);
                    System.Threading.Thread.Sleep(1000);
                    send_pass_function(Server_IP);//Send an acknowledgement that the required task is completed
                }

                    //Apply ED mode with required resolution
                else if (data_rece == "1920x1080@i60MDS8BPC")
                {
                    data_rece = "ED_eDP_HDMI_1024_768_60_i_32_MAR_1920_1080_60_i_32_MDS";
                    SetMode(data_rece);
                    System.Threading.Thread.Sleep(1000);
                    send_pass_function(Server_IP);//Send an acknowledgement that the required task is completed
                }

                    //Apply ED mode with required resolution
                else if (data_rece == "1920x1080@i59MDS8BPC")
                {
                    data_rece = "ED_eDP_HDMI_1024_768_60_i_32_MAR_1920_1080_59_i_32_MDS";
                    SetMode(data_rece);
                    System.Threading.Thread.Sleep(1000);
                    send_pass_function(Server_IP);//Send an acknowledgement that the required task is completed
                }

                    //Apply ED mode with required resolution
                else if (data_rece == "720x480@i60MDS8BPC")
                {
                    data_rece = "ED_eDP_HDMI_1024_768_60_i_32_MAR_720_480_60_i_32_MDS";
                    SetMode(data_rece);
                    System.Threading.Thread.Sleep(1000);
                    send_pass_function(Server_IP);//Send an acknowledgement that the required task is completed
                }

                    //Apply ED mode with required resolution
                else if (data_rece == "720x480@i59MDS8BPC")
                {
                    data_rece = "ED_eDP_HDMI_1024_768_60_i_32_MAR_720_480_59_i_32_MDS";
                    SetMode(data_rece);
                    System.Threading.Thread.Sleep(1000);
                    send_pass_function(Server_IP);//Send an acknowledgement that the required task is completed
                }

                //Apply ED mode with required resolution
                else if (data_rece == "3840x2160@50MDS8BPC")
                {
                    data_rece = "ED_eDP_HDMI_1024_768_60_p_32_MAR_3840_2160_50_p_32_MDS";
                    SetMode(data_rece);
                    System.Threading.Thread.Sleep(1000);
                    send_pass_function(Server_IP);//Send an acknowledgement that the required task is completed
                }

                //Apply ED mode with required resolution
                else if (data_rece == "3840x2160@60MDS8BPC")
                {
                    data_rece = "ED_eDP_HDMI_1024_768_60_p_32_MAR_3840_2160_60_p_32_MDS";
                    SetMode(data_rece);
                    System.Threading.Thread.Sleep(1000);
                    send_pass_function(Server_IP);//Send an acknowledgement that the required task is completed
                }

                //Apply ED mode with required resolution
                else if (data_rece == "4096x2160@60MDS8BPC")
                {
                    data_rece = "ED_eDP_HDMI_1024_768_60_p_32_MAR_4096_2160_60_p_32_MDS";
                    SetMode(data_rece);
                    System.Threading.Thread.Sleep(1000);
                    send_pass_function(Server_IP);//Send an acknowledgement that the required task is completed
                }

                //Apply ED mode with required resolution
                else if (data_rece == "4096x2160@50MDS8BPC")
                {
                    data_rece = "ED_eDP_HDMI_1024_768_60_p_32_MAR_4096_2160_50_p_32_MDS";
                    SetMode(data_rece);
                    System.Threading.Thread.Sleep(1000);
                    send_pass_function(Server_IP);//Send an acknowledgement that the required task is completed
                }


                //Apply ED mode with required resolution
                else if (data_rece == "DeepColor")
                {
                    Microsoft.Win32.RegistryKey key;
                    key = Registry.LocalMachine.CreateSubKey("SYSTEM\\ControlSet001\\Control\\Class\\{4d36e968-e325-11ce-bfc1-08002be10318}\\0000");
                    if (key != null)
                    {
                        key.SetValue("SelectMaxDisplayBPC", new Byte[] { 1, 0, 0, 0 }, RegistryValueKind.Binary);
                        key.Close();
                    }

                    System.Threading.Thread.Sleep(2000);
                    send_pass_function(Server_IP);//Send an acknowledgement that the required task is completed
                }


                //Apply ED mode with required resolution
                else if (data_rece == "DeepColorDisable")
                {
                    Microsoft.Win32.RegistryKey key;
                    key = Registry.LocalMachine.CreateSubKey("SYSTEM\\ControlSet001\\Control\\Class\\{4d36e968-e325-11ce-bfc1-08002be10318}\\0000");
                    if (key != null)
                    {
                        key.SetValue("SelectMaxDisplayBPC", new Byte[] { 0, 0, 0, 0 }, RegistryValueKind.Binary);
                        key.Close();
                    }

                    System.Threading.Thread.Sleep(2000);
                    send_pass_function(Server_IP);//Send an acknowledgement that the required task is completed
                }

                else if (data_rece == "-mOFF")
                {

                    PowerParams argPowerParams = new PowerParams();

                    argPowerParams.Delay = 30;
                    string sleepArg = string.Format("/sleep /s:{0} /c:1 /p:{1}", argPowerParams.PowerStates.ToString().ToLower().Split('s').Last(), argPowerParams.Delay);
                    CommonExtensions.StartProcess("pwrtest.exe", sleepArg).WaitForExit();
              
                    System.Threading.Thread.Sleep(3000);

                    System.Windows.Forms.SendKeys.SendWait("{ENTER}");

                }
            /*    else
                {


                    Process ApletProcess = new Process();
                    System.Threading.Thread.Sleep(8000);
                    ApletProcess.StartInfo.WorkingDirectory = @"C:\commandlineApplet\";
                    ApletProcess.StartInfo.FileName = "DisplayPortApp.exe";
                    ApletProcess.StartInfo.Arguments = data_rece;
                    ApletProcess.StartInfo.Verb = "runas";
                    ApletProcess.Start();
                    System.Threading.Thread.Sleep(8000);

                    if (data_rece != turnoff)
                    {
                        Client.Class1 Client1 = new Client.Class1();
                        Client1.Client(Server_IP, " PASS");

                    }
                }*/
            }

        }

//Send Pass after applying the required DUT configuration
        private static void send_pass_function(string Server_IP)
        {
            int count = 0;
        exc1: try
            {
                count++;//Initial value of count is zero
                Client.Class1 Client1 = new Client.Class1();
                Client1.Client(Server_IP, "PASS");
            }

            catch
            {
                if (count <= 4)//Wait until count is greater than 3 times so that manual pop up will appear.
                {
                    System.Threading.Thread.Sleep(1000);//Wait for 1 sec
                    goto exc1;//execute try block once again automatically
                }

                else
                {
                    //If the client fails 3 times, ask manually
                    DialogResult result1 = MessageBox.Show("Do you want to retry or cancel?", "Important Note", MessageBoxButtons.RetryCancel);
                   
                    //If Retry button is pressed, again execute try block 3 times
                    if (result1 == DialogResult.Retry)
                    {
                        count = 0;
                        goto exc1;
                    }
                        //If cancel is pressed, abort the process.
                    else if (result1 == DialogResult.Cancel)
                    {
                        foreach (var process in Process.GetProcessesByName("DP_Compliance_Client_Console"))
                        {
                            process.Kill();
                        }
                    }
                }
            }
        }

        public static void ExpandCollapse(AutomationElement element)
        {
            if (element != null)
            {
                ExpandCollapsePattern pattern = element.GetCurrentPattern(ExpandCollapsePattern.Pattern) as ExpandCollapsePattern;
                if (pattern.Current.ExpandCollapseState == ExpandCollapseState.Collapsed)
                    pattern.Expand();
            }
        }

        public static void SelectionItem(AutomationElement element)
        {
            if (element != null)
            {
                SelectionItemPattern pattern = element.GetCurrentPattern(SelectionItemPattern.Pattern) as SelectionItemPattern;
                pattern.Select();
            }
        }


        public static void Invoke(AutomationElement element)
        {
            if (element != null)
            {
                InvokePattern pattern = element.GetCurrentPattern(InvokePattern.Pattern) as InvokePattern;
                pattern.Invoke();
            }
        }

        public static AutomationElement SelectElementNameControlType(string name, ControlType ct)
        {
            return SelectElementNameControlType(AutomationElement.RootElement, name, ct);
        }

        public static AutomationElement SelectElementNameControlType(AutomationElement parentelement, string name, ControlType ct)
        {
            condition = new AndCondition(
                       new PropertyCondition(AutomationElement.NameProperty, name, PropertyConditionFlags.IgnoreCase),
                       new PropertyCondition(AutomationElement.ControlTypeProperty, ct)
                       );
            return parentelement.FindFirst(TreeScope.Descendants, condition);
        }

        public static AutomationElement SelectElementName(AutomationElement parentelement, string name)
        {
            PropertyCondition condition = new PropertyCondition(AutomationElement.NameProperty, name, PropertyConditionFlags.IgnoreCase);
            return parentelement.FindFirst(TreeScope.Descendants, condition);
        }

        public static AndCondition condition { get; set; }




        }
    }
