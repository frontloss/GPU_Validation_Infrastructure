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

        static void Main(string[] args)
        {
            Console.Write(" Client IP Adddress \r \n");
            Console.Write( GetLocalIP()+"\n \r");
            Console.Write("  \r \n");
            Console.Write(" Enter Server IP Adddress \r \n");
            string Server_IP = Console.ReadLine();
            


            while (true)
            {
                string data_rece;

                SERVER.Class1 server1 = new SERVER.Class1();
                data_rece = server1.Server();
                
                
                string turnoff = "mOFF";
                string two4824bit = "2_Channel_48000Hz_24bits_20s.wav";
                string two4816bit = "2_Channel_48000Hz_24bits_20s.wav";
                string Eight4824bit = "8_Channel_48000Hz_24bits_20s.wav";
                string two19224bit = "2_Channel_192000Hz_24bits_20s.wav";
                string two19216bit = "2_Channel_192000Hz_16bits_20s.wav";
                string Eaght19224bit = "8_Channel_192000Hz_24bits_20s.wav";
                string Eaght19216bit = "8_Channel_192000Hz_16bits_20s.wav";
                string HDCP = "ENABLE_HDCP";
         

                //Audio Compliance 

                if (data_rece == two4824bit || data_rece == two4816bit || data_rece == Eight4824bit || data_rece == two19224bit || data_rece == Eaght19224bit || data_rece == two19216bit || data_rece == Eaght19216bit)
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
                    System.Threading.Thread.Sleep(2000);
                    AutomationElement File_Open = SelectElementNameControlType("File", ControlType.Button);
                    Invoke(File_Open);
                    System.Windows.Forms.SendKeys.SendWait("C:\\HBR Player\\");
                    System.Windows.Forms.SendKeys.SendWait(data_rece);
                  
                    AutomationElement Open = SelectElementNameControlType("Open", ControlType.Button);
                    Invoke(Open);
                    
                    AutomationElement ClickOK = SelectElementNameControlType("Play", ControlType.Button);
                    Invoke(ClickOK);
                    
                    System.Threading.Thread.Sleep(3000);
                    Client.Class1 Client1 = new Client.Class1();
                    Client1.Client(Server_IP, " PASS");



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
                else if (data_rece == "800x600@60MDS8BPC")
                {
                    data_rece = "CLONE_eDP_DP_800_600_60_p_32_MAR_800_600_60_p_32_MDS";
                    SetMode(data_rece);
                    System.Threading.Thread.Sleep(1000);
                    Client.Class1 Client1 = new Client.Class1();
                    Client1.Client(Server_IP, "PASS");
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
                else
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
