using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using NetworksApi.TCP.SERVER;
using System.IO;
using System.Windows.Automation;
using System.Reflection;
using System.Diagnostics;
using SERVER;
using Client;
using System.Net;
using System.Net.Sockets;
using System.Net.NetworkInformation;



namespace DP_Compliance

{
    public delegate void UpdateTextBox(string txt);

    public partial class Form1 : Form
    {
        
       
        public Form1()
        {
            InitializeComponent();




        }

       
        private void Form1_Load(object sender, EventArgs e)
        {
            textBox2.Text = GetLocalIP();

            START.Enabled = false;

          
        }

        private string GetLocalIP()
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
            return " 127.0.0.1";



        }
        

     
        private void START_Click(object sender, EventArgs e)
        {
            
            
           

            DPR100_APP_Close();
            DPR120_APP_Close();

           
            if (DPR120_LINK.Checked == true || DPR120_Applet.Checked == true)
            {
                DPR120_APP_Close();
                DPR120_APP_Open();
            
            }

            if (DPR100_LINK.Checked == true || DPR100_HDCP.Checked == true || DPR100_AUDIO.Checked == true || DPR100_Applet.Checked == true)
            {
                DPR100_APP_Close();
                DPR100_APP_Open();
            
            }



            if (DPR100_LINK.Checked == true)
            {

                DPR100_TestRun1_4_2_1_1();
                DPR100_Test_2_27();
                DPR100_Test_2();
                DPR100_Test_3();
                DPR100_Test_4();
                DPR100_Test_5();
                DPR100_Test_6();
                DPR100_Test_7();
                DPR100_Test_8();
                DPR100_Test_9();
                DPR100_Test_10();
                DPR100_Test_11();
                DPR100_Test_12();
                DPR100_Test_13();
                DPR100_Test_14();
                DPR100_Test_15();
                DPR100_Test_16();
                DPR100_Test_17();
                DPR100_Test_18();
                DPR100_Test_19();
                DPR100_Test_20();
                DPR100_Test_21();
                DPR100_Test_22();
                DPR100_Test_23();
                DPR100_Test_24();
                DPR100_Test_25();
                DPR100_Test_26();
                DPR100_Test_27();
                DPR100_Applet_4_3_3_1();
                DPR100_Applet_4_4_1_1();
                DPR100_Applet_4_4_1_2();
                DPR100_Applet_4_4_1_3();
                DPR100_Applet_4_4_3();
                DPR100_7_1_1_1();
                DPR100_7_1_1_2();

            }

            if (DPR100_AUDIO.Checked == true && BDW.Checked == true)
            {
                
                DPR100_Audio_Test_4_4_4_3();
                DPR100_Audio_Test_4_4_4_4();
                DPR100_Audio_Test_4_4_4_5();
                DPR100_Audio_Test_4_4_4_6();


            }

            if (DPR100_AUDIO.Checked == true && SKL.Checked == true)
            {

                SKL_DPR100_Audio_Test_4_4_4_3();
                DPR100_Audio_Test_4_4_4_4();
                SKL_DPR100_Audio_Test_4_4_4_5();
                SKL_DPR100_Audio_Test_4_4_4_6();


            } 
            
            if (DPR100_HDCP.Checked == true)

            {


                DPR100_HDCP_1A_01();
                DPR100_HDCP_1A_02();
                DPR100_HDCP_1A_03();
                DPR100_HDCP_1A_04();
                DPR100_HDCP_1A_05();
                DPR100_HDCP_1A_06();
                DPR100_HDCP_1A_07();
                DPR100_HDCP_1B_01();
                DPR100_HDCP_1B_02();
                DPR100_HDCP_1B_03();
                DPR100_HDCP_1B_04();
                DPR100_HDCP_1B_05();
                DPR100_HDCP_1B_06();
                DPR100_HDCP_1B_07();
            
            
            }

            if (DPR100_Applet.Checked == true)

            {
                DPR120_APP_Close();
                DPR100_Applet_4_3_3_1();
                DPR100_Applet_4_4_1_1();
                DPR100_Applet_4_4_1_2();
                DPR100_Applet_4_4_1_3();
                DPR100_Applet_4_4_3();
            
            }

            if (DPR120_LINK.Checked == true )
            {
                //DPR120_Test_1_to_33();
                DPR120_Test_1();
                
                DPR120_Test_2();
               
                DPR120_Test_3();
                
                DPR120_Test_4();
                
                DPR120_Test_5();
                
                DPR120_Test_6();
                
                DPR120_Test_7();
               
                DPR120_Test_8();
                
                DPR120_Test_9();
                
                DPR120_Test_10();
                
                DPR120_Test_11();
                
                DPR120_Test_12();
                
                DPR120_Test_13();
               
                DPR120_Test_14();
               
                DPR120_Test_15();
                
                DPR120_Test_16();
                
                DPR120_Test_17();
                
                DPR120_Test_18();
               
                DPR120_Test_20();
                
                DPR120_Test_21();
                
                DPR120_Test_22();
                
                DPR120_Test_23();
                
                DPR120_Test_24();
                
                DPR120_Test_25();     
                DPR120_Test_26();
                DPR120_Test_27();
                DPR120_Test_28();
                DPR120_Test_29();
                DPR120_Test_30();
                DPR120_Test_31();
                DPR120_Test_32();
                DPR120_Test_33();
                // DPR120_Test_34();
                // DPR120_Test_35();
                // DPR120_Test_36();
                // DPR120_Test_37();
                // DPR120_Test_38();
                // DPR120_Test_39();
                // DPR120_Test_40();
                // DPR120_Test_41();
                // DPR120_Test_42();
                DPR120_Test_Video_Time_Stam_Generation_400_3_3_1();
                DPR120_Test_Applete_test_4_4_1_1();
                DPR120_Test_Applete_test_4_4_1_2();
                DPR120_Test_Applete_test_4_4_1_3();
                DPR120_Test_Power_Management_test_4_4_3();
               

            }

            if (DPR120_Applet.Checked == true)

            {

                DPR120_Test_Video_Time_Stam_Generation_400_3_3_1();
                DPR120_Test_Applete_test_4_4_1_1();
                DPR120_Test_Applete_test_4_4_1_2();
                DPR120_Test_Applete_test_4_4_1_3();
                DPR120_Test_Power_Management_test_4_4_3();
            }



            if (DPR120_LINK.Checked == true || DPR120_Applet.Checked == true)
            {
                DPR120_Save_Log();
                DPR120_APP_Close();

            }


            if (DPR100_LINK.Checked == true || DPR100_HDCP.Checked == true || DPR100_AUDIO.Checked == true || DPR100_Applet.Checked == true)
            {

                DPR100_LogSave();
                DPR100_APP_Close();
               

            }




   
        }




 // DPR 120 Application Close 


        private void DPR120_APP_Close()
        {

         

            Process myProcess = new Process();
            foreach (var process in Process.GetProcessesByName("980mgr"))
            {
                process.Kill();

            }

        }

//  DPR120 Application Open 

        private void DPR120_APP_Open()
        {


            Process myProcess = new Process();
            myProcess.StartInfo.WorkingDirectory = @"C:\Program Files (x86)\Unigraf\DPR-120\";
            myProcess.StartInfo.FileName = "DP_DTC.exe";
            myProcess.StartInfo.Verb = "runas";
            myProcess.Start();
            System.Threading.Thread.Sleep(8000);
            AutomationElement tab_firstElems1 = SelectElementNameControlType("Proceed", ControlType.Button);
            Invoke(tab_firstElems1);


            AutomationElement Tabitem_Source_DUT = SelectElementNameControlType("Source DUT Testing", ControlType.TabItem);
            SelectionItem(Tabitem_Source_DUT);
            System.Windows.Forms.SendKeys.SendWait("{ENTER}");

            AutomationElement MenuElement_FILE = SelectElementNameControlType("File", ControlType.MenuItem);
            ExpandCollapse(MenuElement_FILE);

            AutomationElement Open_CTS_Settings = SelectElementNameControlType("Open CTS Settings ...", ControlType.MenuItem);
            Invoke(Open_CTS_Settings);
            System.Threading.Thread.Sleep(4000);
            if (BDW.Checked)
            {
                System.Windows.Forms.SendKeys.SendWait("C:\\DPR120Settings.CFG");
            }
            else if(SKL.Checked)
            {
                System.Windows.Forms.SendKeys.SendWait("C:\\SDPR120Settings.CFG");
            }
            System.Threading.Thread.Sleep(2000);
            System.Windows.Forms.SendKeys.SendWait("{ENTER}");
            //AutomationElement File_Open = SelectElementNameControlType("Open", ControlType.Button);
            //Invoke(File_Open);


        
        }


 // DPR120 Test 1 to 33
        private void DPR120_Test_1_to_33()
        {

         
            int count = Int32.Parse(textBox2_Iteration.Text);

            for (int Test = 0; Test < 32; Test++)// All tests repeat loop
            {


                for (int i = 0; i < count; i++)
                {

                    Network_Check(); // Network Check before sending data 

                            // Data send to server

                            string client_data = "800x600@60MDS8BPC";
                            Client.Class1 Client1 = new Client.Class1();
                            Client1.Client(textBox1.Text, client_data);
                         


                    //// Data reciveve 

                    string data_rece;
                    SERVER.Class1 server1 = new SERVER.Class1();
                    data_rece = server1.Server();
                    





                    System.Threading.Thread.Sleep(3000);
                    AutomationElement Tabitem_RUN_Tests = SelectElementNameControlType("RUN Tests", ControlType.TabItem);
                    SelectionItem(Tabitem_RUN_Tests);
                    System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                    System.Windows.Forms.SendKeys.SendWait("{TAB}");

                    if (i == 0)
                    {
                        System.Windows.Forms.SendKeys.SendWait("{DOWN 1}");
                    }

                    if (Test == 18)
                    {
                        System.Windows.Forms.SendKeys.SendWait("{DOWN 1}");
                    }



                    System.Windows.Forms.SendKeys.SendWait("{TAB}");
                    System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                    while (true)
                    {
                        

                        AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                        if (Testcommpleted != null)
                        {
                            Invoke(Testcommpleted);
                            break;
                        }

                    }

                }
            }
        
        
        }

        private void DPR120_Test_1()
        {


            int count = Int32.Parse(textBox2_Iteration.Text);

                for (int i = 0; i < count; i++)
                {
                    
                    Network_Check(); // Network Check before sending data 

                    // Data send to server

                    string client_data = "800x600@60MDS8BPC";
                    Client.Class1 Client1 = new Client.Class1();
                    Client1.Client(textBox1.Text, client_data);



                    //// Data reciveve 

                    string data_rece;
                    SERVER.Class1 server1 = new SERVER.Class1();
                    data_rece = server1.Server();






                    System.Threading.Thread.Sleep(10000);
                    AutomationElement Tabitem_RUN_Tests = SelectElementNameControlType("RUN Tests", ControlType.TabItem);
                    SelectionItem(Tabitem_RUN_Tests);
                    System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                    System.Windows.Forms.SendKeys.SendWait("{TAB}");

                    if (i == 0)
                    {
                        System.Windows.Forms.SendKeys.SendWait("{UP 35}");
                        System.Windows.Forms.SendKeys.SendWait("{DOWN 1}");
                    }

                    System.Windows.Forms.SendKeys.SendWait("{TAB}");
                    System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                    while (true)
                    {
                        

                        AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                        if (Testcommpleted != null)
                        {
                            Invoke(Testcommpleted);
                            break;
                        }

                    }

                }
            


        }

        private void DPR120_Test_2()
        {


            int count = Int32.Parse(textBox2_Iteration.Text);

            for (int i = 0; i < count; i++)
            {
                

                Network_Check(); // Network Check before sending data 

                // Data send to server

                string client_data = "800x600@60MDS8BPC";
                Client.Class1 Client1 = new Client.Class1();
                Client1.Client(textBox1.Text, client_data);



                //// Data reciveve 

                string data_rece;
                SERVER.Class1 server1 = new SERVER.Class1();
                data_rece = server1.Server();






                System.Threading.Thread.Sleep(10000);
                AutomationElement Tabitem_RUN_Tests = SelectElementNameControlType("RUN Tests", ControlType.TabItem);
                SelectionItem(Tabitem_RUN_Tests);
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                System.Windows.Forms.SendKeys.SendWait("{TAB}");

                if (i == 0)
                {
                    System.Windows.Forms.SendKeys.SendWait("{UP 35}");
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 1}");
                }

                System.Windows.Forms.SendKeys.SendWait("{TAB}");
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                while (true)
                {
                    

                    AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                    if (Testcommpleted != null)
                    {
                        Invoke(Testcommpleted);
                        break;
                    }

                }

            }
        }

        private void DPR120_Test_3()
        {


            int count = Int32.Parse(textBox2_Iteration.Text);

            for (int i = 0; i < count; i++)
            {
                
                Network_Check(); // Network Check before sending data 

                // Data send to server

                string client_data = "800x600@60MDS8BPC";
                Client.Class1 Client1 = new Client.Class1();
                Client1.Client(textBox1.Text, client_data);



                //// Data reciveve 

                string data_rece;
                SERVER.Class1 server1 = new SERVER.Class1();
                data_rece = server1.Server();






                System.Threading.Thread.Sleep(10000);
                AutomationElement Tabitem_RUN_Tests = SelectElementNameControlType("RUN Tests", ControlType.TabItem);
                SelectionItem(Tabitem_RUN_Tests);
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                System.Windows.Forms.SendKeys.SendWait("{TAB}");

                if (i == 0)
                {
                    System.Windows.Forms.SendKeys.SendWait("{UP 35}");
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 2}");
                }

                System.Windows.Forms.SendKeys.SendWait("{TAB}");
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                while (true)
                {
                    

                    AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                    if (Testcommpleted != null)
                    {
                        Invoke(Testcommpleted);
                        break;
                    }

                }

            }



        }

        private void DPR120_Test_4()
        {

            
            int count = Int32.Parse(textBox2_Iteration.Text);

            for (int i = 0; i < count; i++)
            {
                System.Threading.Thread.Sleep(15000);
                Network_Check(); // Network Check before sending data 

                // Data send to server

                string client_data = "800x600@60MDS8BPC";
                Client.Class1 Client1 = new Client.Class1();
                Client1.Client(textBox1.Text, client_data);



                //// Data reciveve 

                string data_rece;
                SERVER.Class1 server1 = new SERVER.Class1();
                data_rece = server1.Server();






                System.Threading.Thread.Sleep(10000);
                AutomationElement Tabitem_RUN_Tests = SelectElementNameControlType("RUN Tests", ControlType.TabItem);
                SelectionItem(Tabitem_RUN_Tests);
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                System.Windows.Forms.SendKeys.SendWait("{TAB}");

                if (i == 0)
                {
                    System.Windows.Forms.SendKeys.SendWait("{UP 35}");
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 3}");
                }

                System.Windows.Forms.SendKeys.SendWait("{TAB}");
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                while (true)
                {
                    

                    AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                    if (Testcommpleted != null)
                    {
                        Invoke(Testcommpleted);
                        break;
                    }

                }

            }



        }

        private void DPR120_Test_5()
        {

            
            int count = Int32.Parse(textBox2_Iteration.Text);

            for (int i = 0; i < count; i++)
            {
                
                Network_Check(); // Network Check before sending data 

                // Data send to server

                string client_data = "800x600@60MDS8BPC";
                Client.Class1 Client1 = new Client.Class1();
                Client1.Client(textBox1.Text, client_data);



                //// Data reciveve 

                string data_rece;
                SERVER.Class1 server1 = new SERVER.Class1();
                data_rece = server1.Server();
                





                System.Threading.Thread.Sleep(10000);
                AutomationElement Tabitem_RUN_Tests = SelectElementNameControlType("RUN Tests", ControlType.TabItem);
                SelectionItem(Tabitem_RUN_Tests);
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                System.Windows.Forms.SendKeys.SendWait("{TAB}");

                if (i == 0)
                {
                    System.Windows.Forms.SendKeys.SendWait("{UP 35}");
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 4}");
                }

                System.Windows.Forms.SendKeys.SendWait("{TAB}");
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                while (true)
                {
                    

                    AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                    if (Testcommpleted != null)
                    {
                        Invoke(Testcommpleted);
                        break;
                    }

                }

            }



        }

        private void DPR120_Test_6()
        {

            
            int count = Int32.Parse(textBox2_Iteration.Text);

            for (int i = 0; i < count; i++)
            {
                
                Network_Check(); // Network Check before sending data 

                // Data send to server

                string client_data = "800x600@60MDS8BPC";
                Client.Class1 Client1 = new Client.Class1();
                Client1.Client(textBox1.Text, client_data);



                //// Data reciveve 

                string data_rece;
                SERVER.Class1 server1 = new SERVER.Class1();
                data_rece = server1.Server();






                System.Threading.Thread.Sleep(10000);
                AutomationElement Tabitem_RUN_Tests = SelectElementNameControlType("RUN Tests", ControlType.TabItem);
                SelectionItem(Tabitem_RUN_Tests);
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                System.Windows.Forms.SendKeys.SendWait("{TAB}");

                if (i == 0)
                {
                    System.Windows.Forms.SendKeys.SendWait("{UP 35}");
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 5}");
                }

                System.Windows.Forms.SendKeys.SendWait("{TAB}");
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                while (true)
                {
                    

                    AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                    if (Testcommpleted != null)
                    {
                        Invoke(Testcommpleted);
                        break;
                    }

                }

            }



        }

        private void DPR120_Test_7()
        {

            
            int count = Int32.Parse(textBox2_Iteration.Text);

            for (int i = 0; i < count; i++)
            {
                
                Network_Check(); // Network Check before sending data 

                // Data send to server

                string client_data = "800x600@60MDS8BPC";
                Client.Class1 Client1 = new Client.Class1();
                Client1.Client(textBox1.Text, client_data);



                //// Data reciveve 

                string data_rece;
                SERVER.Class1 server1 = new SERVER.Class1();
                data_rece = server1.Server();






                System.Threading.Thread.Sleep(10000);
                AutomationElement Tabitem_RUN_Tests = SelectElementNameControlType("RUN Tests", ControlType.TabItem);
                SelectionItem(Tabitem_RUN_Tests);
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                System.Windows.Forms.SendKeys.SendWait("{TAB}");

                if (i == 0)
                {
                    System.Windows.Forms.SendKeys.SendWait("{UP 35}");
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 6}");
                }

                System.Windows.Forms.SendKeys.SendWait("{TAB}");
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                while (true)
                {
                    

                    AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                    if (Testcommpleted != null)
                    {
                        Invoke(Testcommpleted);
                        break;
                    }

                }

            }



        }

        private void DPR120_Test_8()
        {

           
            int count = Int32.Parse(textBox2_Iteration.Text);

            for (int i = 0; i < count; i++)
            {
                
                Network_Check(); // Network Check before sending data 

                // Data send to server

                string client_data = "800x600@60MDS8BPC";
                Client.Class1 Client1 = new Client.Class1();
                Client1.Client(textBox1.Text, client_data);



                //// Data reciveve 

                string data_rece;
                SERVER.Class1 server1 = new SERVER.Class1();
                data_rece = server1.Server();






                System.Threading.Thread.Sleep(10000);
                AutomationElement Tabitem_RUN_Tests = SelectElementNameControlType("RUN Tests", ControlType.TabItem);
                SelectionItem(Tabitem_RUN_Tests);
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                System.Windows.Forms.SendKeys.SendWait("{TAB}");

                if (i == 0)
                {
                    System.Windows.Forms.SendKeys.SendWait("{UP 35}");
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 7}");
                }

                System.Windows.Forms.SendKeys.SendWait("{TAB}");
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                while (true)
                {
                   

                    AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                    if (Testcommpleted != null)
                    {
                        Invoke(Testcommpleted);
                        break;
                    }

                }

            }



        }

        private void DPR120_Test_9()
        {

            
            int count = Int32.Parse(textBox2_Iteration.Text);

            for (int i = 0; i < count; i++)
            {
                
                Network_Check(); // Network Check before sending data 

                // Data send to server

                string client_data = "800x600@60MDS8BPC";
                Client.Class1 Client1 = new Client.Class1();
                Client1.Client(textBox1.Text, client_data);



                //// Data reciveve 

                string data_rece;
                SERVER.Class1 server1 = new SERVER.Class1();
                data_rece = server1.Server();






                System.Threading.Thread.Sleep(10000);
                AutomationElement Tabitem_RUN_Tests = SelectElementNameControlType("RUN Tests", ControlType.TabItem);
                SelectionItem(Tabitem_RUN_Tests);
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                System.Windows.Forms.SendKeys.SendWait("{TAB}");

                if (i == 0)
                {
                    System.Windows.Forms.SendKeys.SendWait("{UP 35}");
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 8}");
                }

                System.Windows.Forms.SendKeys.SendWait("{TAB}");
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                while (true)
                {
                    

                    AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                    if (Testcommpleted != null)
                    {
                        Invoke(Testcommpleted);
                        break;
                    }

                }

            }



        }

        private void DPR120_Test_10()
        {

            
            int count = Int32.Parse(textBox2_Iteration.Text);

            for (int i = 0; i < count; i++)
            {
                
                Network_Check(); // Network Check before sending data 

                // Data send to server

                string client_data = "800x600@60MDS8BPC";
                Client.Class1 Client1 = new Client.Class1();
                Client1.Client(textBox1.Text, client_data);



                //// Data reciveve 

                string data_rece;
                SERVER.Class1 server1 = new SERVER.Class1();
                data_rece = server1.Server();






                System.Threading.Thread.Sleep(10000);
                AutomationElement Tabitem_RUN_Tests = SelectElementNameControlType("RUN Tests", ControlType.TabItem);
                SelectionItem(Tabitem_RUN_Tests);
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                System.Windows.Forms.SendKeys.SendWait("{TAB}");

                if (i == 0)
                {
                    System.Windows.Forms.SendKeys.SendWait("{UP 35}");
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 9}");
                }

                System.Windows.Forms.SendKeys.SendWait("{TAB}");
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                while (true)
                {
                    

                    AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                    if (Testcommpleted != null)
                    {
                        Invoke(Testcommpleted);
                        break;
                    }

                }

            }

        }


             private void DPR120_Test_11()
        {

            
            int count = Int32.Parse(textBox2_Iteration.Text);

                for (int i = 0; i < count; i++)
                {
                    
                    Network_Check(); // Network Check before sending data 

                    // Data send to server

                    string client_data = "800x600@60MDS8BPC";
                    Client.Class1 Client1 = new Client.Class1();
                    Client1.Client(textBox1.Text, client_data);



                    //// Data reciveve 

                    string data_rece;
                    SERVER.Class1 server1 = new SERVER.Class1();
                    data_rece = server1.Server();






                    System.Threading.Thread.Sleep(10000);
                    AutomationElement Tabitem_RUN_Tests = SelectElementNameControlType("RUN Tests", ControlType.TabItem);
                    SelectionItem(Tabitem_RUN_Tests);
                    System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                    System.Windows.Forms.SendKeys.SendWait("{TAB}");

                    if (i == 0)
                    {
                        System.Windows.Forms.SendKeys.SendWait("{UP 35}");
                        System.Windows.Forms.SendKeys.SendWait("{DOWN 10}");
                    }

                    System.Windows.Forms.SendKeys.SendWait("{TAB}");
                    System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                    while (true)
                    {
                        

                        AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                        if (Testcommpleted != null)
                        {
                            Invoke(Testcommpleted);
                            break;
                        }

                    }

                }
            


        }

         private void DPR120_Test_12()
        {


            int count = Int32.Parse(textBox2_Iteration.Text);

                for (int i = 0; i < count; i++)
                {
                    
                    Network_Check(); // Network Check before sending data 

                    // Data send to server

                    string client_data = "800x600@60MDS8BPC";
                    Client.Class1 Client1 = new Client.Class1();
                    Client1.Client(textBox1.Text, client_data);



                    //// Data reciveve 

                    string data_rece;
                    SERVER.Class1 server1 = new SERVER.Class1();
                    data_rece = server1.Server();






                    System.Threading.Thread.Sleep(10000);
                    AutomationElement Tabitem_RUN_Tests = SelectElementNameControlType("RUN Tests", ControlType.TabItem);
                    SelectionItem(Tabitem_RUN_Tests);
                    System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                    System.Windows.Forms.SendKeys.SendWait("{TAB}");

                    if (i == 0)
                    {
                        System.Windows.Forms.SendKeys.SendWait("{UP 35}");
                        System.Windows.Forms.SendKeys.SendWait("{DOWN 11}");
                    }

                    System.Windows.Forms.SendKeys.SendWait("{TAB}");
                    System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                    while (true)
                    {
                        

                        AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                        if (Testcommpleted != null)
                        {
                            Invoke(Testcommpleted);
                            break;
                        }

                    }

                }
            


        }

         private void DPR120_Test_13()
        {


            int count = Int32.Parse(textBox2_Iteration.Text);

                for (int i = 0; i < count; i++)
                {
                   
                    Network_Check(); // Network Check before sending data 

                    // Data send to server

                    string client_data = "800x600@60MDS8BPC";
                    Client.Class1 Client1 = new Client.Class1();
                    Client1.Client(textBox1.Text, client_data);



                    //// Data reciveve 

                    string data_rece;
                    SERVER.Class1 server1 = new SERVER.Class1();
                    data_rece = server1.Server();
                    





                    System.Threading.Thread.Sleep(10000);
                    AutomationElement Tabitem_RUN_Tests = SelectElementNameControlType("RUN Tests", ControlType.TabItem);
                    SelectionItem(Tabitem_RUN_Tests);
                    System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                    System.Windows.Forms.SendKeys.SendWait("{TAB}");

                    if (i == 0)
                    {
                        System.Windows.Forms.SendKeys.SendWait("{UP 35}");
                        System.Windows.Forms.SendKeys.SendWait("{DOWN 12}");
                    }

                    System.Windows.Forms.SendKeys.SendWait("{TAB}");
                    System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                    while (true)
                    {
                        

                        AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                        if (Testcommpleted != null)
                        {
                            Invoke(Testcommpleted);
                            break;
                        }

                    }

                }
            


        }

         private void DPR120_Test_14()
        {


            int count = Int32.Parse(textBox2_Iteration.Text);

                for (int i = 0; i < count; i++)
                {

                    Network_Check(); // Network Check before sending data 

                    // Data send to server

                    string client_data = "800x600@60MDS8BPC";
                    Client.Class1 Client1 = new Client.Class1();
                    Client1.Client(textBox1.Text, client_data);



                    //// Data reciveve 

                    string data_rece;
                    SERVER.Class1 server1 = new SERVER.Class1();
                    data_rece = server1.Server();






                    System.Threading.Thread.Sleep(10000);
                    AutomationElement Tabitem_RUN_Tests = SelectElementNameControlType("RUN Tests", ControlType.TabItem);
                    SelectionItem(Tabitem_RUN_Tests);
                    System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                    System.Windows.Forms.SendKeys.SendWait("{TAB}");

                    if (i == 0)
                    {
                        System.Windows.Forms.SendKeys.SendWait("{UP 35}");
                        System.Windows.Forms.SendKeys.SendWait("{DOWN 13}");
                    }

                    System.Windows.Forms.SendKeys.SendWait("{TAB}");
                    System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                    while (true)
                    {
                        

                        AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                        if (Testcommpleted != null)
                        {
                            Invoke(Testcommpleted);
                            break;
                        }

                    }

                }
            


        }

         private void DPR120_Test_15()
        {


            int count = Int32.Parse(textBox2_Iteration.Text);

                for (int i = 0; i < count; i++)
                {

                    Network_Check(); // Network Check before sending data 

                    // Data send to server

                    string client_data = "800x600@60MDS8BPC";
                    Client.Class1 Client1 = new Client.Class1();
                    Client1.Client(textBox1.Text, client_data);



                    //// Data reciveve 

                    string data_rece;
                    SERVER.Class1 server1 = new SERVER.Class1();
                    data_rece = server1.Server();






                    System.Threading.Thread.Sleep(10000);
                    AutomationElement Tabitem_RUN_Tests = SelectElementNameControlType("RUN Tests", ControlType.TabItem);
                    SelectionItem(Tabitem_RUN_Tests);
                    System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                    System.Windows.Forms.SendKeys.SendWait("{TAB}");

                    if (i == 0)
                    {
                        System.Windows.Forms.SendKeys.SendWait("{UP 35}");
                        System.Windows.Forms.SendKeys.SendWait("{DOWN 14}");
                    }

                    System.Windows.Forms.SendKeys.SendWait("{TAB}");
                    System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                    while (true)
                    {
                        

                        AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                        if (Testcommpleted != null)
                        {
                            Invoke(Testcommpleted);
                            break;
                        }

                    }

                }
            


        }

         private void DPR120_Test_16()
        {


            int count = Int32.Parse(textBox2_Iteration.Text);

                for (int i = 0; i < count; i++)
                {

                    Network_Check(); // Network Check before sending data 

                    // Data send to server

                    string client_data = "800x600@60MDS8BPC";
                    Client.Class1 Client1 = new Client.Class1();
                    Client1.Client(textBox1.Text, client_data);



                    //// Data reciveve 

                    string data_rece;
                    SERVER.Class1 server1 = new SERVER.Class1();
                    data_rece = server1.Server();






                    System.Threading.Thread.Sleep(10000);
                    AutomationElement Tabitem_RUN_Tests = SelectElementNameControlType("RUN Tests", ControlType.TabItem);
                    SelectionItem(Tabitem_RUN_Tests);
                    System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                    System.Windows.Forms.SendKeys.SendWait("{TAB}");

                    if (i == 0)
                    {
                        System.Windows.Forms.SendKeys.SendWait("{UP 35}");
                        System.Windows.Forms.SendKeys.SendWait("{DOWN 15}");
                    }

                    System.Windows.Forms.SendKeys.SendWait("{TAB}");
                    System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                    while (true)
                    {
                        

                        AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                        if (Testcommpleted != null)
                        {
                            Invoke(Testcommpleted);
                            break;
                        }

                    }

                }
            


        }

         private void DPR120_Test_17()
        {


            int count = Int32.Parse(textBox2_Iteration.Text);

                for (int i = 0; i < count; i++)
                {

                    Network_Check(); // Network Check before sending data 

                    // Data send to server

                    string client_data = "800x600@60MDS8BPC";
                    Client.Class1 Client1 = new Client.Class1();
                    Client1.Client(textBox1.Text, client_data);



                    //// Data reciveve 

                    string data_rece;
                    SERVER.Class1 server1 = new SERVER.Class1();
                    data_rece = server1.Server();






                    System.Threading.Thread.Sleep(10000);
                    AutomationElement Tabitem_RUN_Tests = SelectElementNameControlType("RUN Tests", ControlType.TabItem);
                    SelectionItem(Tabitem_RUN_Tests);
                    System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                    System.Windows.Forms.SendKeys.SendWait("{TAB}");

                    if (i == 0)
                    {
                        System.Windows.Forms.SendKeys.SendWait("{UP 35}");
                        System.Windows.Forms.SendKeys.SendWait("{DOWN 16}");
                    }

                    System.Windows.Forms.SendKeys.SendWait("{TAB}");
                    System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                    while (true)
                    {
                        

                        AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                        if (Testcommpleted != null)
                        {
                            Invoke(Testcommpleted);
                            break;
                        }

                    }

                }
            


        }

         private void DPR120_Test_18()
        {


            int count = Int32.Parse(textBox2_Iteration.Text);

                for (int i = 0; i < count; i++)
                {

                    Network_Check(); // Network Check before sending data 

                    // Data send to server

                    string client_data = "800x600@60MDS8BPC";
                    Client.Class1 Client1 = new Client.Class1();
                    Client1.Client(textBox1.Text, client_data);



                    //// Data reciveve 

                    string data_rece;
                    SERVER.Class1 server1 = new SERVER.Class1();
                    data_rece = server1.Server();






                    System.Threading.Thread.Sleep(10000);
                    AutomationElement Tabitem_RUN_Tests = SelectElementNameControlType("RUN Tests", ControlType.TabItem);
                    SelectionItem(Tabitem_RUN_Tests);
                    System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                    System.Windows.Forms.SendKeys.SendWait("{TAB}");

                    if (i == 0)
                    {
                        System.Windows.Forms.SendKeys.SendWait("{UP 35}");
                        System.Windows.Forms.SendKeys.SendWait("{DOWN 17}");
                    }

                    System.Windows.Forms.SendKeys.SendWait("{TAB}");
                    System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                    while (true)
                    {
                        

                        AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                        if (Testcommpleted != null)
                        {
                            Invoke(Testcommpleted);
                            break;
                        }

                    }

                }
            


        }

    
         private void DPR120_Test_20()
        {


            int count = Int32.Parse(textBox2_Iteration.Text);

                for (int i = 0; i < count; i++)
                {

                    Network_Check(); // Network Check before sending data 

                    // Data send to server

                    string client_data = "800x600@60MDS8BPC";
                    Client.Class1 Client1 = new Client.Class1();
                    Client1.Client(textBox1.Text, client_data);



                    //// Data reciveve 

                    string data_rece;
                    SERVER.Class1 server1 = new SERVER.Class1();
                    data_rece = server1.Server();






                    System.Threading.Thread.Sleep(10000);
                    AutomationElement Tabitem_RUN_Tests = SelectElementNameControlType("RUN Tests", ControlType.TabItem);
                    SelectionItem(Tabitem_RUN_Tests);
                    System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                    System.Windows.Forms.SendKeys.SendWait("{TAB}");

                    if (i == 0)
                    {
                        System.Windows.Forms.SendKeys.SendWait("{UP 35}");
                        System.Windows.Forms.SendKeys.SendWait("{DOWN 19}");
                    }

                    System.Windows.Forms.SendKeys.SendWait("{TAB}");
                    System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                    while (true)
                    {
                        

                        AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                        if (Testcommpleted != null)
                        {
                            Invoke(Testcommpleted);
                            break;
                        }

                    }

                }
            


        }
         private void DPR120_Test_21()
        {


            int count = Int32.Parse(textBox2_Iteration.Text);

                for (int i = 0; i < count; i++)
                {

                    Network_Check(); // Network Check before sending data 

                    // Data send to server

                    string client_data = "800x600@60MDS8BPC";
                    Client.Class1 Client1 = new Client.Class1();
                    Client1.Client(textBox1.Text, client_data);



                    //// Data reciveve 

                    string data_rece;
                    SERVER.Class1 server1 = new SERVER.Class1();
                    data_rece = server1.Server();






                    System.Threading.Thread.Sleep(10000);
                    AutomationElement Tabitem_RUN_Tests = SelectElementNameControlType("RUN Tests", ControlType.TabItem);
                    SelectionItem(Tabitem_RUN_Tests);
                    System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                    System.Windows.Forms.SendKeys.SendWait("{TAB}");

                    if (i == 0)
                    {
                        System.Windows.Forms.SendKeys.SendWait("{UP 35}");
                        System.Windows.Forms.SendKeys.SendWait("{DOWN 20}");
                    }

                    System.Windows.Forms.SendKeys.SendWait("{TAB}");
                    System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                    while (true)
                    {
                        

                        AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                        if (Testcommpleted != null)
                        {
                            Invoke(Testcommpleted);
                            break;
                        }

                    }

                }
            


        }

         private void DPR120_Test_22()
        {


            int count = Int32.Parse(textBox2_Iteration.Text);

                for (int i = 0; i < count; i++)
                {

                    Network_Check(); // Network Check before sending data 

                    // Data send to server

                    string client_data = "800x600@60MDS8BPC";
                    Client.Class1 Client1 = new Client.Class1();
                    Client1.Client(textBox1.Text, client_data);



                    //// Data reciveve 

                    string data_rece;
                    SERVER.Class1 server1 = new SERVER.Class1();
                    data_rece = server1.Server();






                    System.Threading.Thread.Sleep(10000);
                    AutomationElement Tabitem_RUN_Tests = SelectElementNameControlType("RUN Tests", ControlType.TabItem);
                    SelectionItem(Tabitem_RUN_Tests);
                    System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                    System.Windows.Forms.SendKeys.SendWait("{TAB}");

                    if (i == 0)
                    {
                        System.Windows.Forms.SendKeys.SendWait("{UP 35}");
                        System.Windows.Forms.SendKeys.SendWait("{DOWN 21}");
                    }

                    System.Windows.Forms.SendKeys.SendWait("{TAB}");
                    System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                    while (true)
                    {
                        

                        AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                        if (Testcommpleted != null)
                        {
                            Invoke(Testcommpleted);
                            break;
                        }

                    }

                }
            


        }

         private void DPR120_Test_23()
        {


            int count = Int32.Parse(textBox2_Iteration.Text);

                for (int i = 0; i < count; i++)
                {

                    Network_Check(); // Network Check before sending data 

                    // Data send to server

                    string client_data = "800x600@60MDS8BPC";
                    Client.Class1 Client1 = new Client.Class1();
                    Client1.Client(textBox1.Text, client_data);



                    //// Data reciveve 

                    string data_rece;
                    SERVER.Class1 server1 = new SERVER.Class1();
                    data_rece = server1.Server();






                    System.Threading.Thread.Sleep(10000);
                    AutomationElement Tabitem_RUN_Tests = SelectElementNameControlType("RUN Tests", ControlType.TabItem);
                    SelectionItem(Tabitem_RUN_Tests);
                    System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                    System.Windows.Forms.SendKeys.SendWait("{TAB}");

                    if (i == 0)
                    {
                        System.Windows.Forms.SendKeys.SendWait("{UP 35}");
                        System.Windows.Forms.SendKeys.SendWait("{DOWN 22}");
                    }

                    System.Windows.Forms.SendKeys.SendWait("{TAB}");
                    System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                    while (true)
                    {
                        

                        AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                        if (Testcommpleted != null)
                        {
                            Invoke(Testcommpleted);
                            break;
                        }

                    }

                }
            


        }

         private void DPR120_Test_24()
        {


            int count = Int32.Parse(textBox2_Iteration.Text);

                for (int i = 0; i < count; i++)
                {

                    Network_Check(); // Network Check before sending data 

                    // Data send to server

                    string client_data = "800x600@60MDS8BPC";
                    Client.Class1 Client1 = new Client.Class1();
                    Client1.Client(textBox1.Text, client_data);



                    //// Data reciveve 

                    string data_rece;
                    SERVER.Class1 server1 = new SERVER.Class1();
                    data_rece = server1.Server();






                    System.Threading.Thread.Sleep(10000);
                    AutomationElement Tabitem_RUN_Tests = SelectElementNameControlType("RUN Tests", ControlType.TabItem);
                    SelectionItem(Tabitem_RUN_Tests);
                    System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                    System.Windows.Forms.SendKeys.SendWait("{TAB}");

                    if (i == 0)
                    {
                        System.Windows.Forms.SendKeys.SendWait("{UP 35}");
                        System.Windows.Forms.SendKeys.SendWait("{DOWN 23}");
                    }

                    System.Windows.Forms.SendKeys.SendWait("{TAB}");
                    System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                    while (true)
                    {
                        

                        AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                        if (Testcommpleted != null)
                        {
                            Invoke(Testcommpleted);
                            break;
                        }

                    }

                }
            


        }

         private void DPR120_Test_25()
        {


            int count = Int32.Parse(textBox2_Iteration.Text);

                for (int i = 0; i < count; i++)
                {

                    Network_Check(); // Network Check before sending data 

                    // Data send to server

                    string client_data = "800x600@60MDS8BPC";
                    Client.Class1 Client1 = new Client.Class1();
                    Client1.Client(textBox1.Text, client_data);



                    //// Data reciveve 

                    string data_rece;
                    SERVER.Class1 server1 = new SERVER.Class1();
                    data_rece = server1.Server();






                    System.Threading.Thread.Sleep(10000);
                    AutomationElement Tabitem_RUN_Tests = SelectElementNameControlType("RUN Tests", ControlType.TabItem);
                    SelectionItem(Tabitem_RUN_Tests);
                    System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                    System.Windows.Forms.SendKeys.SendWait("{TAB}");

                    if (i == 0)
                    {
                        System.Windows.Forms.SendKeys.SendWait("{UP 35}");
                        System.Windows.Forms.SendKeys.SendWait("{DOWN 24}");
                    }

                    System.Windows.Forms.SendKeys.SendWait("{TAB}");
                    System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                    while (true)
                    {
                        

                        AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                        if (Testcommpleted != null)
                        {
                            Invoke(Testcommpleted);
                            break;
                        }

                    }

                }
            


        }

         private void DPR120_Test_26()
        {


            int count = Int32.Parse(textBox2_Iteration.Text);

                for (int i = 0; i < count; i++)
                {

                    Network_Check(); // Network Check before sending data 

                    // Data send to server

                    string client_data = "800x600@60MDS8BPC";
                    Client.Class1 Client1 = new Client.Class1();
                    Client1.Client(textBox1.Text, client_data);



                    //// Data reciveve 

                    string data_rece;
                    SERVER.Class1 server1 = new SERVER.Class1();
                    data_rece = server1.Server();






                    System.Threading.Thread.Sleep(10000);
                    AutomationElement Tabitem_RUN_Tests = SelectElementNameControlType("RUN Tests", ControlType.TabItem);
                    SelectionItem(Tabitem_RUN_Tests);
                    System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                    System.Windows.Forms.SendKeys.SendWait("{TAB}");

                    if (i == 0)
                    {
                        System.Windows.Forms.SendKeys.SendWait("{UP 35}");
                        System.Windows.Forms.SendKeys.SendWait("{DOWN 25}");
                    }

                    System.Windows.Forms.SendKeys.SendWait("{TAB}");
                    System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                    while (true)
                    {
                        

                        AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                        if (Testcommpleted != null)
                        {
                            Invoke(Testcommpleted);
                            break;
                        }

                    }

                }
            


        }

         private void DPR120_Test_27()
        {


            int count = Int32.Parse(textBox2_Iteration.Text);

                for (int i = 0; i < count; i++)
                {

                    Network_Check(); // Network Check before sending data 

                    // Data send to server

                    string client_data = "800x600@60MDS8BPC";
                    Client.Class1 Client1 = new Client.Class1();
                    Client1.Client(textBox1.Text, client_data);



                    //// Data reciveve 

                    string data_rece;
                    SERVER.Class1 server1 = new SERVER.Class1();
                    data_rece = server1.Server();






                    System.Threading.Thread.Sleep(10000);
                    AutomationElement Tabitem_RUN_Tests = SelectElementNameControlType("RUN Tests", ControlType.TabItem);
                    SelectionItem(Tabitem_RUN_Tests);
                    System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                    System.Windows.Forms.SendKeys.SendWait("{TAB}");

                    if (i == 0)
                    {
                        System.Windows.Forms.SendKeys.SendWait("{UP 35}");
                        System.Windows.Forms.SendKeys.SendWait("{DOWN 26}");
                    }

                    System.Windows.Forms.SendKeys.SendWait("{TAB}");
                    System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                    while (true)
                    {
                        

                        AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                        if (Testcommpleted != null)
                        {
                            Invoke(Testcommpleted);
                            break;
                        }

                    }

                }
            


        }

         private void DPR120_Test_28()
        {


            int count = Int32.Parse(textBox2_Iteration.Text);

                for (int i = 0; i < count; i++)
                {

                    Network_Check(); // Network Check before sending data 

                    // Data send to server

                    string client_data = "800x600@60MDS8BPC";
                    Client.Class1 Client1 = new Client.Class1();
                    Client1.Client(textBox1.Text, client_data);



                    //// Data reciveve 

                    string data_rece;
                    SERVER.Class1 server1 = new SERVER.Class1();
                    data_rece = server1.Server();






                    System.Threading.Thread.Sleep(10000);
                    AutomationElement Tabitem_RUN_Tests = SelectElementNameControlType("RUN Tests", ControlType.TabItem);
                    SelectionItem(Tabitem_RUN_Tests);
                    System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                    System.Windows.Forms.SendKeys.SendWait("{TAB}");

                    if (i == 0)
                    {
                        System.Windows.Forms.SendKeys.SendWait("{UP 35}");
                        System.Windows.Forms.SendKeys.SendWait("{DOWN 27}");
                    }

                    System.Windows.Forms.SendKeys.SendWait("{TAB}");
                    System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                    while (true)
                    {
                        

                        AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                        if (Testcommpleted != null)
                        {
                            Invoke(Testcommpleted);
                            break;
                        }

                    }

                }
            


        }

         private void DPR120_Test_29()
        {


            int count = Int32.Parse(textBox2_Iteration.Text);

                for (int i = 0; i < count; i++)
                {

                    Network_Check(); // Network Check before sending data 

                    // Data send to server

                    string client_data = "800x600@60MDS8BPC";
                    Client.Class1 Client1 = new Client.Class1();
                    Client1.Client(textBox1.Text, client_data);



                    //// Data reciveve 

                    string data_rece;
                    SERVER.Class1 server1 = new SERVER.Class1();
                    data_rece = server1.Server();






                    System.Threading.Thread.Sleep(10000);
                    AutomationElement Tabitem_RUN_Tests = SelectElementNameControlType("RUN Tests", ControlType.TabItem);
                    SelectionItem(Tabitem_RUN_Tests);
                    System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                    System.Windows.Forms.SendKeys.SendWait("{TAB}");

                    if (i == 0)
                    {
                        System.Windows.Forms.SendKeys.SendWait("{UP 35}");
                        System.Windows.Forms.SendKeys.SendWait("{DOWN 28}");
                    }

                    System.Windows.Forms.SendKeys.SendWait("{TAB}");
                    System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                    while (true)
                    {
                        

                        AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                        if (Testcommpleted != null)
                        {
                            Invoke(Testcommpleted);
                            break;
                        }

                    }

                }
            


        }

         private void DPR120_Test_30()
        {


            int count = Int32.Parse(textBox2_Iteration.Text);

                for (int i = 0; i < count; i++)
                {

                    Network_Check(); // Network Check before sending data 

                    // Data send to server

                    string client_data = "800x600@60MDS8BPC";
                    Client.Class1 Client1 = new Client.Class1();
                    Client1.Client(textBox1.Text, client_data);



                    //// Data reciveve 

                    string data_rece;
                    SERVER.Class1 server1 = new SERVER.Class1();
                    data_rece = server1.Server();






                    System.Threading.Thread.Sleep(10000);
                    AutomationElement Tabitem_RUN_Tests = SelectElementNameControlType("RUN Tests", ControlType.TabItem);
                    SelectionItem(Tabitem_RUN_Tests);
                    System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                    System.Windows.Forms.SendKeys.SendWait("{TAB}");

                    if (i == 0)
                    {
                        System.Windows.Forms.SendKeys.SendWait("{UP 35}");
                        System.Windows.Forms.SendKeys.SendWait("{DOWN 29}");
                    }

                    System.Windows.Forms.SendKeys.SendWait("{TAB}");
                    System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                    while (true)
                    {
                        

                        AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                        if (Testcommpleted != null)
                        {
                            Invoke(Testcommpleted);
                            break;
                        }

                    }

                }
            


        }

         private void DPR120_Test_31()
        {


            int count = Int32.Parse(textBox2_Iteration.Text);

                for (int i = 0; i < count; i++)
                {

                    Network_Check(); // Network Check before sending data 

                    // Data send to server

                    string client_data = "800x600@60MDS8BPC";
                    Client.Class1 Client1 = new Client.Class1();
                    Client1.Client(textBox1.Text, client_data);



                    //// Data reciveve 

                    string data_rece;
                    SERVER.Class1 server1 = new SERVER.Class1();
                    data_rece = server1.Server();






                    System.Threading.Thread.Sleep(10000);
                    AutomationElement Tabitem_RUN_Tests = SelectElementNameControlType("RUN Tests", ControlType.TabItem);
                    SelectionItem(Tabitem_RUN_Tests);
                    System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                    System.Windows.Forms.SendKeys.SendWait("{TAB}");

                    if (i == 0)
                    {
                        System.Windows.Forms.SendKeys.SendWait("{UP 35}");
                        System.Windows.Forms.SendKeys.SendWait("{DOWN 30}");
                    }

                    System.Windows.Forms.SendKeys.SendWait("{TAB}");
                    System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                    while (true)
                    {
                        
                        AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                        if (Testcommpleted != null)
                        {
                            Invoke(Testcommpleted);
                            break;
                        }

                    }

                }
            


        }

         private void DPR120_Test_32()
        {


            int count = Int32.Parse(textBox2_Iteration.Text);

                for (int i = 0; i < count; i++)
                {

                    Network_Check(); // Network Check before sending data 

                    // Data send to server

                    string client_data = "800x600@60MDS8BPC";
                    Client.Class1 Client1 = new Client.Class1();
                    Client1.Client(textBox1.Text, client_data);



                    //// Data reciveve 

                    string data_rece;
                    SERVER.Class1 server1 = new SERVER.Class1();
                    data_rece = server1.Server();






                    System.Threading.Thread.Sleep(10000);
                    AutomationElement Tabitem_RUN_Tests = SelectElementNameControlType("RUN Tests", ControlType.TabItem);
                    SelectionItem(Tabitem_RUN_Tests);
                    System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                    System.Windows.Forms.SendKeys.SendWait("{TAB}");

                    if (i == 0)
                    {
                        System.Windows.Forms.SendKeys.SendWait("{UP 35}");
                        System.Windows.Forms.SendKeys.SendWait("{DOWN 31}");
                    }

                    System.Windows.Forms.SendKeys.SendWait("{TAB}");
                    System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                    while (true)
                    {
                        

                        AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                        if (Testcommpleted != null)
                        {
                            Invoke(Testcommpleted);
                            break;
                        }

                    }

                }
            


        }

         private void DPR120_Test_33()
        {


            int count = Int32.Parse(textBox2_Iteration.Text);

                for (int i = 0; i < count; i++)
                {

                    Network_Check(); // Network Check before sending data 

                    // Data send to server

                    string client_data = "800x600@60MDS8BPC";
                    Client.Class1 Client1 = new Client.Class1();
                    Client1.Client(textBox1.Text, client_data);



                    //// Data reciveve 

                    string data_rece;
                    SERVER.Class1 server1 = new SERVER.Class1();
                    data_rece = server1.Server();






                    System.Threading.Thread.Sleep(10000);
                    AutomationElement Tabitem_RUN_Tests = SelectElementNameControlType("RUN Tests", ControlType.TabItem);
                    SelectionItem(Tabitem_RUN_Tests);
                    System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                    System.Windows.Forms.SendKeys.SendWait("{TAB}");

                    if (i == 0)
                    {
                        System.Windows.Forms.SendKeys.SendWait("{UP 35}");
                        System.Windows.Forms.SendKeys.SendWait("{DOWN 32}");
                    }

                    System.Windows.Forms.SendKeys.SendWait("{TAB}");
                    System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                    while (true)
                    {
                        

                        AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                        if (Testcommpleted != null)
                        {
                            Invoke(Testcommpleted);
                            break;
                        }

                    }

                }
            


        }
         private void DPR120_Test_34()
         {


             int count = Int32.Parse(textBox2_Iteration.Text);

             for (int i = 0; i < count; i++)
             {

                 Network_Check(); // Network Check before sending data 

                 // Data send to server

                 string client_data = "800x600@60MDS8BPC";
                 Client.Class1 Client1 = new Client.Class1();
                 Client1.Client(textBox1.Text, client_data);



                 //// Data reciveve 

                 string data_rece;
                 SERVER.Class1 server1 = new SERVER.Class1();
                 data_rece = server1.Server();






                 System.Threading.Thread.Sleep(10000);
                 AutomationElement Tabitem_RUN_Tests = SelectElementNameControlType("RUN Tests", ControlType.TabItem);
                 SelectionItem(Tabitem_RUN_Tests);
                 System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                 System.Windows.Forms.SendKeys.SendWait("{TAB}");

                 if (i == 0)
                 {
                     System.Windows.Forms.SendKeys.SendWait("{UP 50}");
                     System.Windows.Forms.SendKeys.SendWait("{DOWN 38}");
                 }

                 System.Windows.Forms.SendKeys.SendWait("{TAB}");
                 System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                 while (true)
                 {


                     AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                     if (Testcommpleted != null)
                     {
                         Invoke(Testcommpleted);
                         break;
                     }

                 }

             }



         }
         private void DPR120_Test_35()
         {


             int count = Int32.Parse(textBox2_Iteration.Text);

             for (int i = 0; i < count; i++)
             {

                 Network_Check(); // Network Check before sending data 

                 // Data send to server

                 string client_data = "800x600@60MDS8BPC";
                 Client.Class1 Client1 = new Client.Class1();
                 Client1.Client(textBox1.Text, client_data);



                 //// Data reciveve 

                 string data_rece;
                 SERVER.Class1 server1 = new SERVER.Class1();
                 data_rece = server1.Server();






                 System.Threading.Thread.Sleep(10000);
                 AutomationElement Tabitem_RUN_Tests = SelectElementNameControlType("RUN Tests", ControlType.TabItem);
                 SelectionItem(Tabitem_RUN_Tests);
                 System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                 System.Windows.Forms.SendKeys.SendWait("{TAB}");

                 if (i == 0)
                 {
                     System.Windows.Forms.SendKeys.SendWait("{UP 50}");
                     System.Windows.Forms.SendKeys.SendWait("{DOWN 39}");
                 }

                 System.Windows.Forms.SendKeys.SendWait("{TAB}");
                 System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                 while (true)
                 {


                     AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                     if (Testcommpleted != null)
                     {
                         Invoke(Testcommpleted);
                         break;
                     }

                 }

             }



         }
         private void DPR120_Test_36()
         {


             int count = Int32.Parse(textBox2_Iteration.Text);

             for (int i = 0; i < count; i++)
             {

                 Network_Check(); // Network Check before sending data 

                 // Data send to server

                 string client_data = "800x600@60MDS8BPC";
                 Client.Class1 Client1 = new Client.Class1();
                 Client1.Client(textBox1.Text, client_data);



                 //// Data reciveve 

                 string data_rece;
                 SERVER.Class1 server1 = new SERVER.Class1();
                 data_rece = server1.Server();






                 System.Threading.Thread.Sleep(10000);
                 AutomationElement Tabitem_RUN_Tests = SelectElementNameControlType("RUN Tests", ControlType.TabItem);
                 SelectionItem(Tabitem_RUN_Tests);
                 System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                 System.Windows.Forms.SendKeys.SendWait("{TAB}");

                 if (i == 0)
                 {
                     System.Windows.Forms.SendKeys.SendWait("{UP 50}");
                     System.Windows.Forms.SendKeys.SendWait("{DOWN 40}");
                 }

                 System.Windows.Forms.SendKeys.SendWait("{TAB}");
                 System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                 while (true)
                 {


                     AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                     if (Testcommpleted != null)
                     {
                         Invoke(Testcommpleted);
                         break;
                     }

                 }

             }



         }
         private void DPR120_Test_37()
         {


             int count = Int32.Parse(textBox2_Iteration.Text);

             for (int i = 0; i < count; i++)
             {

                 Network_Check(); // Network Check before sending data 

                 // Data send to server

                 string client_data = "800x600@60MDS8BPC";
                 Client.Class1 Client1 = new Client.Class1();
                 Client1.Client(textBox1.Text, client_data);



                 //// Data reciveve 

                 string data_rece;
                 SERVER.Class1 server1 = new SERVER.Class1();
                 data_rece = server1.Server();






                 System.Threading.Thread.Sleep(10000);
                 AutomationElement Tabitem_RUN_Tests = SelectElementNameControlType("RUN Tests", ControlType.TabItem);
                 SelectionItem(Tabitem_RUN_Tests);
                 System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                 System.Windows.Forms.SendKeys.SendWait("{TAB}");

                 if (i == 0)
                 {
                     System.Windows.Forms.SendKeys.SendWait("{UP 50}");
                     System.Windows.Forms.SendKeys.SendWait("{DOWN 41}");
                 }

                 System.Windows.Forms.SendKeys.SendWait("{TAB}");
                 System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                 while (true)
                 {


                     AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                     if (Testcommpleted != null)
                     {
                         Invoke(Testcommpleted);
                         break;
                     }

                 }

             }



         }
         private void DPR120_Test_38()
         {


             int count = Int32.Parse(textBox2_Iteration.Text);

             for (int i = 0; i < count; i++)
             {

                 Network_Check(); // Network Check before sending data 

                 // Data send to server

                 string client_data = "800x600@60MDS8BPC";
                 Client.Class1 Client1 = new Client.Class1();
                 Client1.Client(textBox1.Text, client_data);



                 //// Data reciveve 

                 string data_rece;
                 SERVER.Class1 server1 = new SERVER.Class1();
                 data_rece = server1.Server();






                 System.Threading.Thread.Sleep(10000);
                 AutomationElement Tabitem_RUN_Tests = SelectElementNameControlType("RUN Tests", ControlType.TabItem);
                 SelectionItem(Tabitem_RUN_Tests);
                 System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                 System.Windows.Forms.SendKeys.SendWait("{TAB}");

                 if (i == 0)
                 {
                     System.Windows.Forms.SendKeys.SendWait("{UP 50}");
                     System.Windows.Forms.SendKeys.SendWait("{DOWN 42}");
                 }

                 System.Windows.Forms.SendKeys.SendWait("{TAB}");
                 System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                 while (true)
                 {


                     AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                     if (Testcommpleted != null)
                     {
                         Invoke(Testcommpleted);
                         break;
                     }

                 }

             }



         }
         private void DPR120_Test_39()
         {


             int count = Int32.Parse(textBox2_Iteration.Text);

             for (int i = 0; i < count; i++)
             {

                 Network_Check(); // Network Check before sending data 

                 // Data send to server

                 string client_data = "800x600@60MDS8BPC";
                 Client.Class1 Client1 = new Client.Class1();
                 Client1.Client(textBox1.Text, client_data);



                 //// Data reciveve 

                 string data_rece;
                 SERVER.Class1 server1 = new SERVER.Class1();
                 data_rece = server1.Server();






                 System.Threading.Thread.Sleep(10000);
                 AutomationElement Tabitem_RUN_Tests = SelectElementNameControlType("RUN Tests", ControlType.TabItem);
                 SelectionItem(Tabitem_RUN_Tests);
                 System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                 System.Windows.Forms.SendKeys.SendWait("{TAB}");

                 if (i == 0)
                 {
                     System.Windows.Forms.SendKeys.SendWait("{UP 50}");
                     System.Windows.Forms.SendKeys.SendWait("{DOWN 43}");
                 }

                 System.Windows.Forms.SendKeys.SendWait("{TAB}");
                 System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                 while (true)
                 {


                     AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                     if (Testcommpleted != null)
                     {
                         Invoke(Testcommpleted);
                         break;
                     }

                 }

             }



         }
         private void DPR120_Test_40()
         {


             int count = Int32.Parse(textBox2_Iteration.Text);

             for (int i = 0; i < count; i++)
             {

                 Network_Check(); // Network Check before sending data 

                 // Data send to server

                 string client_data = "800x600@60MDS8BPC";
                 Client.Class1 Client1 = new Client.Class1();
                 Client1.Client(textBox1.Text, client_data);



                 //// Data reciveve 

                 string data_rece;
                 SERVER.Class1 server1 = new SERVER.Class1();
                 data_rece = server1.Server();






                 System.Threading.Thread.Sleep(10000);
                 AutomationElement Tabitem_RUN_Tests = SelectElementNameControlType("RUN Tests", ControlType.TabItem);
                 SelectionItem(Tabitem_RUN_Tests);
                 System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                 System.Windows.Forms.SendKeys.SendWait("{TAB}");

                 if (i == 0)
                 {
                     System.Windows.Forms.SendKeys.SendWait("{UP 50}");
                     System.Windows.Forms.SendKeys.SendWait("{DOWN 44}");
                 }

                 System.Windows.Forms.SendKeys.SendWait("{TAB}");
                 System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                 while (true)
                 {


                     AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                     if (Testcommpleted != null)
                     {
                         Invoke(Testcommpleted);
                         break;
                     }

                 }

             }



         }
         private void DPR120_Test_41()
         {


             int count = Int32.Parse(textBox2_Iteration.Text);

             for (int i = 0; i < count; i++)
             {

                 Network_Check(); // Network Check before sending data 

                 // Data send to server

                 string client_data = "800x600@60MDS8BPC";
                 Client.Class1 Client1 = new Client.Class1();
                 Client1.Client(textBox1.Text, client_data);



                 //// Data reciveve 

                 string data_rece;
                 SERVER.Class1 server1 = new SERVER.Class1();
                 data_rece = server1.Server();






                 System.Threading.Thread.Sleep(10000);
                 AutomationElement Tabitem_RUN_Tests = SelectElementNameControlType("RUN Tests", ControlType.TabItem);
                 SelectionItem(Tabitem_RUN_Tests);
                 System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                 System.Windows.Forms.SendKeys.SendWait("{TAB}");

                 if (i == 0)
                 {
                     System.Windows.Forms.SendKeys.SendWait("{UP 50}");
                     System.Windows.Forms.SendKeys.SendWait("{DOWN 45}");
                 }

                 System.Windows.Forms.SendKeys.SendWait("{TAB}");
                 System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                 while (true)
                 {


                     AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                     if (Testcommpleted != null)
                     {
                         Invoke(Testcommpleted);
                         break;
                     }

                 }

             }



         }
         private void DPR120_Test_42()
         {


             int count = Int32.Parse(textBox2_Iteration.Text);

             for (int i = 0; i < count; i++)
             {

                 Network_Check(); // Network Check before sending data 

                 // Data send to server

                 string client_data = "800x600@60MDS8BPC";
                 Client.Class1 Client1 = new Client.Class1();
                 Client1.Client(textBox1.Text, client_data);



                 //// Data reciveve 

                 string data_rece;
                 SERVER.Class1 server1 = new SERVER.Class1();
                 data_rece = server1.Server();






                 System.Threading.Thread.Sleep(10000);
                 AutomationElement Tabitem_RUN_Tests = SelectElementNameControlType("RUN Tests", ControlType.TabItem);
                 SelectionItem(Tabitem_RUN_Tests);
                 System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                 System.Windows.Forms.SendKeys.SendWait("{TAB}");

                 if (i == 0)
                 {
                     System.Windows.Forms.SendKeys.SendWait("{UP 50}");
                     System.Windows.Forms.SendKeys.SendWait("{DOWN 46}");
                 }

                 System.Windows.Forms.SendKeys.SendWait("{TAB}");
                 System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                 while (true)
                 {


                     AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                     if (Testcommpleted != null)
                     {
                         Invoke(Testcommpleted);
                         break;
                     }

                 }

             }



         }



















  

// DPR120 Test Video Time Stamp Generation 400.3.3.1

        private void DPR120_Test_Video_Time_Stam_Generation_400_3_3_1()
        {

            int count = Int32.Parse(textBox2_Iteration.Text);
            

            for (int i = 0; i < count; i++)
            {


                
               

                System.Threading.Thread.Sleep(3000);
                AutomationElement Tabitem_RUN_Tests = SelectElementNameControlType("RUN Tests", ControlType.TabItem);
                SelectionItem(Tabitem_RUN_Tests);
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                System.Windows.Forms.SendKeys.SendWait("{TAB}");

                if (i == 0)
                {
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 1}");
                    System.Windows.Forms.SendKeys.SendWait("{UP 50}");
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 18}");
                }

                System.Windows.Forms.SendKeys.SendWait("{TAB}");
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                int Patter_no = 0;
                string client_data;

                while (true)
                {
                    System.Threading.Thread.Sleep(2000);

                    AutomationElement PatternApply_Proceed = SelectElementNameControlType("Proceed", ControlType.Button);

                    if (PatternApply_Proceed != null)
                    {


                        if (Patter_no == 0 || Patter_no == 5)
                        {
                            // Data send to server
                            Network_Check(); // Network Check before sending data 

                            if (DP_PORT_B.Checked == true)
                            {
                                client_data = "-dDPB -n1920x1080@8";
                            }

                            else if(DP_PORT_C.Checked == true)
                            {
                                client_data = "-dDPC -n1920x1080@8";
                            }
                            else
                            {
                                client_data = "-dDPD -n1920x1080@8";

                            }
                            Client.Class1 Client1 = new Client.Class1();
                            Client1.Client(textBox1.Text, client_data);


                            //// Data reciveve 

                            string data_rece;
                            SERVER.Class1 server1 = new SERVER.Class1();
                            data_rece = server1.Server();
                            
                            Invoke(PatternApply_Proceed);


                            Patter_no++;


                        } 
                        if (Patter_no == 1 || Patter_no == 3 || Patter_no == 4)
                        {
                            // Data send to server
                            Network_Check(); // Network Check before sending data 


                            if(DP_PORT_B.Checked == true)
                            {
                                client_data = "-dDPB -n640x480@6";
                            }

                            else if(DP_PORT_C.Checked == true)
                            {
                                client_data = "-dDPC -n640x480@6";
                            }

                            else
                            {
                                client_data = "-dDPD -n640x480@6";
                            }
                            
                            Client.Class1 Client1 = new Client.Class1();
                            Client1.Client(textBox1.Text, client_data);

                            //// Data reciveve 

                            string data_rece;
                            SERVER.Class1 server1 = new SERVER.Class1();
                            data_rece = server1.Server();
                            
                            Invoke(PatternApply_Proceed);

                            Patter_no++;

                        } 

                        if (Patter_no == 2)
                         {
                             Network_Check(); // Network Check before sending data 

                             if (DP_PORT_B.Checked == true)
                             {
                                 client_data = "-dDPB -n1920x1440@8";
                             }

                             else if (DP_PORT_C.Checked == true)
                             {
                                 client_data = "-dDPC -n1920x1440@8";
                             }

                             else
                             {
                                 client_data = "-dDPD -n1920x1440@8";
                             }

                             Client.Class1 Client1 = new Client.Class1();
                             Client1.Client(textBox1.Text, client_data);

                             //// Data reciveve 

                             string data_rece;
                             SERVER.Class1 server1 = new SERVER.Class1();
                             data_rece = server1.Server();
                             
                             Invoke(PatternApply_Proceed);


                             Patter_no++;
                        
                        
                        }

                       




                  

                       


                    }
                    AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                    if (Testcommpleted != null)
                    {
                        Invoke(Testcommpleted);
                        break;
                    }



                }




            }
        }

 // DPR120 Applet Test DPR120_Test_Applete_test 4.4.1.1

        private void DPR120_Test_Applete_test_4_4_1_1()
        {


            int count = Int32.Parse(textBox2_Iteration.Text);

            for (int i = 0; i < count; i++)
            {


                


                System.Threading.Thread.Sleep(3000);
                AutomationElement Tabitem_RUN_Tests = SelectElementNameControlType("RUN Tests", ControlType.TabItem);
                SelectionItem(Tabitem_RUN_Tests);
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                System.Windows.Forms.SendKeys.SendWait("{TAB}");

                if (i == 0)
                {
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 1}");
                    System.Windows.Forms.SendKeys.SendWait("{UP 50}");
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 33}");
                }

                System.Windows.Forms.SendKeys.SendWait("{TAB}");
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                int Patter_no = 0;
                string client_data;

                while (true)
                {
                    System.Threading.Thread.Sleep(2000);

                    AutomationElement PatternApply_Proceed = SelectElementNameControlType("Proceed", ControlType.Button);

                    if (PatternApply_Proceed != null)
                    {


                        if (Patter_no == 0 || Patter_no == 2 || Patter_no == 4 || Patter_no == 6)
                        {

                            Network_Check(); // Network Check before sending data 
                            
                            // Data send to server

                            if (DP_PORT_B.Checked == true)
                            {
                                client_data = "-dDPB -n640x480@6";
                            }

                            else if (DP_PORT_C.Checked == true)
                            {
                                client_data = "-dDPC -n640x480@6";
                            }

                            else
                            {
                                client_data = "-dDPD -n640x480@6";
                            }
                            
                            Client.Class1 Client1 = new Client.Class1();
                            Client1.Client(textBox1.Text, client_data);
                            string str = Convert.ToString(Patter_no);
                            

                            ////// Data reciveve 

                            string data_rece;
                            SERVER.Class1 server1 = new SERVER.Class1();
                            data_rece = server1.Server();
                            
                            Invoke(PatternApply_Proceed);
                            System.Threading.Thread.Sleep(10000);

                            Patter_no++;

                        }

                        if (Patter_no == 1 || Patter_no == 3 || Patter_no == 5 || Patter_no == 7)
                        {

                            Network_Check(); // Network Check before sending data 
                            // Data send to server

                            if (DP_PORT_B.Checked == true)
                            {
                                client_data = "-dDPB -n640x480@8";
                            }

                            else if (DP_PORT_C.Checked == true)
                            {
                                client_data = "-dDPC -n640x480@8";
                            }

                            else
                            {
                                client_data = "-dDPD -n640x480@8";
                            }
                            
                            Client.Class1 Client1 = new Client.Class1();
                            Client1.Client(textBox1.Text, client_data);
                            string str = Convert.ToString(Patter_no);
                            

                            ////// Data reciveve 

                            string data_rece;
                            SERVER.Class1 server1 = new SERVER.Class1();
                            data_rece = server1.Server();
                           
                            Invoke(PatternApply_Proceed);
                            System.Threading.Thread.Sleep(10000);
                            Patter_no++;

                        }



                        

                       


                    }
                    AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                    if (Testcommpleted != null)
                    {
                        Invoke(Testcommpleted);
                        break;
                    }



                }




            }
        }


//DPR120 Applet Test DPR120_Test_Applete_test_4_4_1_2;


        private void DPR120_Test_Applete_test_4_4_1_2()
    {


        int count = Int32.Parse(textBox2_Iteration.Text);

        for (int i = 0; i < count; i++)
        {


            


            System.Threading.Thread.Sleep(3000);
            AutomationElement Tabitem_RUN_Tests = SelectElementNameControlType("RUN Tests", ControlType.TabItem);
            SelectionItem(Tabitem_RUN_Tests);
            System.Windows.Forms.SendKeys.SendWait("{ENTER}");
            System.Windows.Forms.SendKeys.SendWait("{TAB}");

            if (i == 0)
            {
                System.Windows.Forms.SendKeys.SendWait("{DOWN 1}");
                System.Windows.Forms.SendKeys.SendWait("{UP 50}");
                System.Windows.Forms.SendKeys.SendWait("{DOWN 34}");
            }

            System.Windows.Forms.SendKeys.SendWait("{TAB}");
            System.Windows.Forms.SendKeys.SendWait("{ENTER}");
            int Patter_no = 0;
            string client_data;

            while (true)
            {
                System.Threading.Thread.Sleep(2000);

                AutomationElement PatternApply_Proceed = SelectElementNameControlType("Proceed", ControlType.Button);

                if (PatternApply_Proceed != null)
                {


                    if (Patter_no == 0 )
                    {


                        Network_Check(); // Network Check before sending data 
                        // Data send to server



                        if (DP_PORT_B.Checked == true)
                        {
                            client_data = "-dDPB -n640x480@6";
                        }

                        else if (DP_PORT_C.Checked == true)
                        {
                            client_data = "-dDPC -n640x480@6";
                        }

                        else
                        {
                            client_data = "-dDPD -n640x480@6";
                        }

                        Client.Class1 Client1 = new Client.Class1();
                        Client1.Client(textBox1.Text, client_data);

                        //// Data reciveve 

                        string data_rece;
                        SERVER.Class1 server1 = new SERVER.Class1();
                        data_rece = server1.Server();
                        
                        Invoke(PatternApply_Proceed);


                        Patter_no++;


                    } 





                  



                }
                AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                if (Testcommpleted != null)
                {
                    Invoke(Testcommpleted);
                    break;
                }


            }




        }
    
    
    
    }


//DPR120 Applet Test DPR120_Test_Applete_test_4_4_1_3;



        private void DPR120_Test_Applete_test_4_4_1_3()
        {

            int count = Int32.Parse(textBox2_Iteration.Text);

            for (int i = 0; i < count; i++)
            {


                


                System.Threading.Thread.Sleep(3000);
                AutomationElement Tabitem_RUN_Tests = SelectElementNameControlType("RUN Tests", ControlType.TabItem);
                SelectionItem(Tabitem_RUN_Tests);
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                System.Windows.Forms.SendKeys.SendWait("{TAB}");

                if (i == 0)
                {
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 1}");
                    System.Windows.Forms.SendKeys.SendWait("{UP 50}");
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 35}");
                }

                System.Windows.Forms.SendKeys.SendWait("{TAB}");
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                int Patter_no = 0;
                string client_data;

                while (true)
                {
                    System.Threading.Thread.Sleep(2000);

                    AutomationElement PatternApply_Proceed = SelectElementNameControlType("Proceed", ControlType.Button);

                    if (PatternApply_Proceed != null)
                    {


                        if (PatternApply_Proceed != null)
                        {


                            if (Patter_no == 0)
                            {

                                Network_Check(); // Network Check before sending data 

                                // Data send to server
                                if (DP_PORT_B.Checked == true)
                                {
                                    client_data = "-dDPB -n1024x768@6";
                                }

                                else if(DP_PORT_C.Checked == true)
                                {
                                    client_data = "-dDPC -n1024x768@6";
                                }
                                else
                                {
                                    client_data = "-dDPD -n1024x768@6";
                                }
                                Client.Class1 Client1 = new Client.Class1();
                                Client1.Client(textBox1.Text, client_data);
                                string str = Convert.ToString(Patter_no);

                                ////// Data reciveve 

                                string data_rece;
                                SERVER.Class1 server1 = new SERVER.Class1();
                                data_rece = server1.Server();
                                
                                Invoke(PatternApply_Proceed);
                                System.Threading.Thread.Sleep(10000);

                                Patter_no++;

                            }

                            if (Patter_no == 1)
                            {

                                Network_Check(); // Network Check before sending data 
                                // Data send to server


                                if (DP_PORT_B.Checked == true)
                                {
                                    client_data = "-l2 -s0 -dDPB -n1280x1024@8";
                                }

                                else if(DP_PORT_C.Checked == true)
                                {
                                    client_data = "-l2 -s0 -dDPC -n1280x1024@8";
                                }

                                else
                                {
                                    client_data = "-l2 -s0 -dDPD -n1280x1024@8";
                                }

                                Client.Class1 Client1 = new Client.Class1();
                                Client1.Client(textBox1.Text, client_data);
                                string str = Convert.ToString(Patter_no);


                                ////// Data reciveve 

                                string data_rece;
                                SERVER.Class1 server1 = new SERVER.Class1();
                                data_rece = server1.Server();
                                Invoke(PatternApply_Proceed);
                                System.Threading.Thread.Sleep(10000);
                                Patter_no++;

                            } if (Patter_no == 2)
                            {

                                Network_Check(); // Network Check before sending data 
                                // Data send to server


                                if (DP_PORT_B.Checked == true)
                                {
                                    client_data = "-dDPB -n1792x1344@8";
                                }

                                else if(DP_PORT_C.Checked == true)
                                {
                                    client_data = "-dDPC -n1792x1344@8";
                                }

                                else
                                {
                                    client_data = "-dDPD -n1792x1344@8";
                                }
                                Client.Class1 Client1 = new Client.Class1();
                                Client1.Client(textBox1.Text, client_data);
                                string str = Convert.ToString(Patter_no);


                                ////// Data reciveve 

                                string data_rece;
                                SERVER.Class1 server1 = new SERVER.Class1();
                                data_rece = server1.Server();
                                Invoke(PatternApply_Proceed);
                                System.Threading.Thread.Sleep(10000);
                                Patter_no++;

                            }


               

                           


                        }


                    }
                    AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                    if (Testcommpleted != null)
                    {
                        Invoke(Testcommpleted);
                        break;
                    }





                }



            }
        }


// DPR120 Power managment tests 4.4.3

        private void DPR120_Test_Power_Management_test_4_4_3 ()
        {

            int count = Int32.Parse(textBox2_Iteration.Text);

            for (int i = 0; i < count; i++)
            {


                
              

                System.Threading.Thread.Sleep(3000);
                AutomationElement Tabitem_RUN_Tests = SelectElementNameControlType("RUN Tests", ControlType.TabItem);
                SelectionItem(Tabitem_RUN_Tests);
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                System.Windows.Forms.SendKeys.SendWait("{TAB}");

                if (i == 0)
                {
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 1}");
                    System.Windows.Forms.SendKeys.SendWait("{UP 50}");
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 37}");
                }
                System.Threading.Thread.Sleep(10000);
                System.Windows.Forms.SendKeys.SendWait("{TAB}");
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                
                



                while (true)
                {
                    System.Threading.Thread.Sleep(2000);

                    AutomationElement PatternApply_Proceed = SelectElementNameControlType("Proceed", ControlType.Button);

                    if (PatternApply_Proceed != null)
                    {

                        Network_Check(); // Network Check before sending data 
                        
                            // Data send to server

                            string client_data = "-mOFF";
                            Client.Class1 Client1 = new Client.Class1();
                            Client1.Client(textBox1.Text, client_data);
                            

                            

                           System.Threading.Thread.Sleep(10000);
                           Invoke(PatternApply_Proceed);

                           Network_Check();
                           Invoke(PatternApply_Proceed);

                          

                    }
                    AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                    if (Testcommpleted != null)
                    {
                        Invoke(Testcommpleted);
                        break;
                    }
                    




                }




            }


        }


//DPR 120 App Save Log

        private void DPR120_Save_Log()
        {



            AutomationElement MenuElement_FILE = SelectElementNameControlType("File", ControlType.MenuItem);
            ExpandCollapse(MenuElement_FILE);

            AutomationElement Save_CTS_Test_Report = SelectElementNameControlType("Save CTS Test Report...", ControlType.MenuItem);
            Invoke(Save_CTS_Test_Report);
            System.Windows.Forms.SendKeys.SendWait("{ENTER}");
            System.Threading.Thread.Sleep(1000);
            
            

            System.Windows.Forms.SendKeys.SendWait("C:\\120logs\\" + Platform.Text+"_" + Driver_Version.Text +"_"+ DateTime.Now.ToString("dd.MM.yyyy.hh.mm.ss") + ".html");
            System.Threading.Thread.Sleep(5000);

            AutomationElement Save = SelectElementNameControlType("Save", ControlType.Button);
            Invoke(Save);
           
            
            System.Threading.Thread.Sleep(3000);
            AutomationElement Save1 = SelectElementNameControlType("Save", ControlType.Button);
            Invoke(Save1);
            System.Threading.Thread.Sleep(5000);

        
        }







// DPR100 Application Open 

        private void DPR100_APP_Open()
        {

            Process myProcess = new Process();
            myProcess.StartInfo.WorkingDirectory = @"C:\Program Files (x86)\Unigraf\RefSinkCTS";
            myProcess.StartInfo.FileName = "DP_RefSink_CTS.exe";
            myProcess.StartInfo.Verb = "runas";
            myProcess.Start();
            System.Threading.Thread.Sleep(5000);

            AutomationElement MenuElement_FILE = SelectElementNameControlType("File", ControlType.MenuItem);
            ExpandCollapse(MenuElement_FILE);
            
            AutomationElement Load_Settings = SelectElementNameControlType("Load Settings ...", ControlType.MenuItem);
            Invoke(Load_Settings);
            System.Threading.Thread.Sleep(4000); 
            if(BDW.Checked)
            {
                System.Windows.Forms.SendKeys.SendWait("C:\\DPR100Settings.CFG");
            }
            else if(SKL.Checked)
            {
                System.Windows.Forms.SendKeys.SendWait("C:\\SDPR100Settings.CFG");
            }
            System.Threading.Thread.Sleep(2000);
            System.Windows.Forms.SendKeys.SendWait("{ENTER}");
            
        
        
        }

//DPR100 Test 1 ( 4.2.1.1 Source DUT Retry on No- Replay Durining Aux Read)

        private void DPR100_TestRun1_4_2_1_1()
    {

        int count = Int32.Parse(textBox2_Iteration.Text);
        for (int i = 0; i < count; i++)
        {

            Network_Check(); // Network Check before sending data 
            // Data send to server



            string client_data = "800x600@60MDS8BPC";
            Client.Class1 Client1 = new Client.Class1();
            Client1.Client(textBox1.Text, client_data);

            //// Data reciveve 

            string data_rece;
            SERVER.Class1 server1 = new SERVER.Class1();
            data_rece = server1.Server();
            
            System.Threading.Thread.Sleep(3000);




            AutomationElement Link_layer = SelectElementNameControlType("Link Layer Tests", ControlType.TabItem);
            SelectionItem(Link_layer);
            System.Windows.Forms.SendKeys.SendWait("{ENTER}");
            System.Windows.Forms.SendKeys.SendWait("{TAB}");

            if (i == 0)
            {
                System.Windows.Forms.SendKeys.SendWait("{DOWN 1}");
            }


            System.Windows.Forms.SendKeys.SendWait("{TAB}");
            System.Windows.Forms.SendKeys.SendWait("{ENTER}");
            while (true)
            {
                System.Threading.Thread.Sleep(1000);

                AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                if (Testcommpleted != null)
                {
                    Invoke(Testcommpleted);
                    break;
                }

            }

        }
    
    
    }


//DPR100 Test 2 to 27 

        private void DPR100_Test_2_27()
        {

            for (int Test = 1; Test < 27; Test++)// All tests repeat loop
            {

                int count = Int32.Parse(textBox2_Iteration.Text);
                for (int i = 0; i < count; i++)
                {

                    Network_Check(); // Network Check before sending data 

                    // Data send to server

                    string client_data = "800x600@60MDS8BPC";
                    Client.Class1 Client1 = new Client.Class1();
                    Client1.Client(textBox1.Text, client_data);

            //// Data reciveve 

                    string data_rece;
                    SERVER.Class1 server1 = new SERVER.Class1();
                    data_rece = server1.Server();
                    




                    System.Threading.Thread.Sleep(5000);
                    AutomationElement Link_layer = SelectElementNameControlType("Link Layer Tests", ControlType.TabItem);
                    SelectionItem(Link_layer);
                    System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                    System.Windows.Forms.SendKeys.SendWait("{TAB}");

                    if (i == 0)
                    {
                        System.Windows.Forms.SendKeys.SendWait("{DOWN 1}");
                    }


                    System.Windows.Forms.SendKeys.SendWait("{TAB}");
                    System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                    while (true)
                    {
                        

                        AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                        if (Testcommpleted != null)
                        {
                            Invoke(Testcommpleted);
                            break;
                        }

                    }

                }
            }


        
        }

        private void DPR100_Test_2()
        {

           
                int count = Int32.Parse(textBox2_Iteration.Text);
                for (int i = 0; i < count; i++)
                {

                    Network_Check(); // Network Check before sending data 

                    // Data send to server

                    string client_data = "800x600@60MDS8BPC";
                    Client.Class1 Client1 = new Client.Class1();
                    Client1.Client(textBox1.Text, client_data);

                    //// Data reciveve 

                    string data_rece;
                    SERVER.Class1 server1 = new SERVER.Class1();
                    data_rece = server1.Server();





                    System.Threading.Thread.Sleep(5000);
                    AutomationElement Link_layer = SelectElementNameControlType("Link Layer Tests", ControlType.TabItem);
                    SelectionItem(Link_layer);
                    System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                    System.Windows.Forms.SendKeys.SendWait("{TAB}");

                    if (i == 0)
                    {
                        System.Windows.Forms.SendKeys.SendWait("{UP 35}");
                        System.Windows.Forms.SendKeys.SendWait("{DOWN 1}");
                    }


                    System.Windows.Forms.SendKeys.SendWait("{TAB}");
                    System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                    while (true)
                    {
                        

                        AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                        if (Testcommpleted != null)
                        {
                            Invoke(Testcommpleted);
                            break;
                        }

                    }

                }
            



        }

        private void DPR100_Test_3()
        {


            int count = Int32.Parse(textBox2_Iteration.Text);
            for (int i = 0; i < count; i++)
            {

                Network_Check(); // Network Check before sending data 

                // Data send to server

                string client_data = "800x600@60MDS8BPC";
                Client.Class1 Client1 = new Client.Class1();
                Client1.Client(textBox1.Text, client_data);

                //// Data reciveve 

                string data_rece;
                SERVER.Class1 server1 = new SERVER.Class1();
                data_rece = server1.Server();





                System.Threading.Thread.Sleep(5000);
                AutomationElement Link_layer = SelectElementNameControlType("Link Layer Tests", ControlType.TabItem);
                SelectionItem(Link_layer);
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                System.Windows.Forms.SendKeys.SendWait("{TAB}");

                if (i == 0)
                {
                    System.Windows.Forms.SendKeys.SendWait("{UP 35}");
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 2}");
                }


                System.Windows.Forms.SendKeys.SendWait("{TAB}");
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                while (true)
                {
                    

                    AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                    if (Testcommpleted != null)
                    {
                        Invoke(Testcommpleted);
                        break;
                    }

                }

            }




        }

        private void DPR100_Test_4()
        {


            int count = Int32.Parse(textBox2_Iteration.Text);
            for (int i = 0; i < count; i++)
            {

                Network_Check(); // Network Check before sending data 

                // Data send to server

                string client_data = "800x600@60MDS8BPC";
                Client.Class1 Client1 = new Client.Class1();
                Client1.Client(textBox1.Text, client_data);

                //// Data reciveve 

                string data_rece;
                SERVER.Class1 server1 = new SERVER.Class1();
                data_rece = server1.Server();





                System.Threading.Thread.Sleep(5000);
                AutomationElement Link_layer = SelectElementNameControlType("Link Layer Tests", ControlType.TabItem);
                SelectionItem(Link_layer);
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                System.Windows.Forms.SendKeys.SendWait("{TAB}");

                if (i == 0)
                {
                    System.Windows.Forms.SendKeys.SendWait("{UP 35}");
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 3}");
                }


                System.Windows.Forms.SendKeys.SendWait("{TAB}");
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                while (true)
                {
                    

                    AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                    if (Testcommpleted != null)
                    {
                        Invoke(Testcommpleted);
                        break;
                    }

                }

            }




        }

        private void DPR100_Test_5()
        {


            int count = Int32.Parse(textBox2_Iteration.Text);
            for (int i = 0; i < count; i++)
            {

                Network_Check(); // Network Check before sending data 

                // Data send to server

                string client_data = "800x600@60MDS8BPC";
                Client.Class1 Client1 = new Client.Class1();
                Client1.Client(textBox1.Text, client_data);

                //// Data reciveve 

                string data_rece;
                SERVER.Class1 server1 = new SERVER.Class1();
                data_rece = server1.Server();





                System.Threading.Thread.Sleep(5000);
                AutomationElement Link_layer = SelectElementNameControlType("Link Layer Tests", ControlType.TabItem);
                SelectionItem(Link_layer);
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                System.Windows.Forms.SendKeys.SendWait("{TAB}");

                if (i == 0)
                {
                    System.Windows.Forms.SendKeys.SendWait("{UP 35}");
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 4}");
                }


                System.Windows.Forms.SendKeys.SendWait("{TAB}");
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                while (true)
                {
                    

                    AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                    if (Testcommpleted != null)
                    {
                        Invoke(Testcommpleted);
                        break;
                    }

                }

            }




        }

        private void DPR100_Test_6()
        {


            int count = Int32.Parse(textBox2_Iteration.Text);
            for (int i = 0; i < count; i++)
            {

                Network_Check(); // Network Check before sending data 

                // Data send to server

                string client_data = "800x600@60MDS8BPC";
                Client.Class1 Client1 = new Client.Class1();
                Client1.Client(textBox1.Text, client_data);

                //// Data reciveve 

                string data_rece;
                SERVER.Class1 server1 = new SERVER.Class1();
                data_rece = server1.Server();





                System.Threading.Thread.Sleep(5000);
                AutomationElement Link_layer = SelectElementNameControlType("Link Layer Tests", ControlType.TabItem);
                SelectionItem(Link_layer);
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                System.Windows.Forms.SendKeys.SendWait("{TAB}");

                if (i == 0)
                {
                    System.Windows.Forms.SendKeys.SendWait("{UP 35}");
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 5}");
                }


                System.Windows.Forms.SendKeys.SendWait("{TAB}");
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                while (true)
                {
                    

                    AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                    if (Testcommpleted != null)
                    {
                        Invoke(Testcommpleted);
                        break;
                    }

                }

            }




        }

        private void DPR100_Test_7()
        {


            int count = Int32.Parse(textBox2_Iteration.Text);
            for (int i = 0; i < count; i++)
            {

                Network_Check(); // Network Check before sending data 

                // Data send to server

                string client_data = "800x600@60MDS8BPC";
                Client.Class1 Client1 = new Client.Class1();
                Client1.Client(textBox1.Text, client_data);

                //// Data reciveve 

                string data_rece;
                SERVER.Class1 server1 = new SERVER.Class1();
                data_rece = server1.Server();





                System.Threading.Thread.Sleep(5000);
                AutomationElement Link_layer = SelectElementNameControlType("Link Layer Tests", ControlType.TabItem);
                SelectionItem(Link_layer);
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                System.Windows.Forms.SendKeys.SendWait("{TAB}");

                if (i == 0)
                {
                    System.Windows.Forms.SendKeys.SendWait("{UP 35}");
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 6}");
                }


                System.Windows.Forms.SendKeys.SendWait("{TAB}");
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                while (true)
                {
                    

                    AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                    if (Testcommpleted != null)
                    {
                        Invoke(Testcommpleted);
                        break;
                    }

                }

            }




        }

        private void DPR100_Test_8()
        {


            int count = Int32.Parse(textBox2_Iteration.Text);
            for (int i = 0; i < count; i++)
            {

                Network_Check(); // Network Check before sending data 

                // Data send to server

                string client_data = "800x600@60MDS8BPC";
                Client.Class1 Client1 = new Client.Class1();
                Client1.Client(textBox1.Text, client_data);

                //// Data reciveve 

                string data_rece;
                SERVER.Class1 server1 = new SERVER.Class1();
                data_rece = server1.Server();





                System.Threading.Thread.Sleep(5000);
                AutomationElement Link_layer = SelectElementNameControlType("Link Layer Tests", ControlType.TabItem);
                SelectionItem(Link_layer);
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                System.Windows.Forms.SendKeys.SendWait("{TAB}");

                if (i == 0)
                {
                    System.Windows.Forms.SendKeys.SendWait("{UP 35}");
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 7}");
                }


                System.Windows.Forms.SendKeys.SendWait("{TAB}");
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                while (true)
                {
                   

                    AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                    if (Testcommpleted != null)
                    {
                        Invoke(Testcommpleted);
                        break;
                    }

                }

            }




        }

        private void DPR100_Test_9()
        {


            int count = Int32.Parse(textBox2_Iteration.Text);
            for (int i = 0; i < count; i++)
            {

                Network_Check(); // Network Check before sending data 

                // Data send to server

                string client_data = "800x600@60MDS8BPC";
                Client.Class1 Client1 = new Client.Class1();
                Client1.Client(textBox1.Text, client_data);

                //// Data reciveve 

                string data_rece;
                SERVER.Class1 server1 = new SERVER.Class1();
                data_rece = server1.Server();





                System.Threading.Thread.Sleep(5000);
                AutomationElement Link_layer = SelectElementNameControlType("Link Layer Tests", ControlType.TabItem);
                SelectionItem(Link_layer);
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                System.Windows.Forms.SendKeys.SendWait("{TAB}");

                if (i == 0)
                {
                    System.Windows.Forms.SendKeys.SendWait("{UP 35}");
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 8}");
                }


                System.Windows.Forms.SendKeys.SendWait("{TAB}");
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                while (true)
                {
                    

                    AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                    if (Testcommpleted != null)
                    {
                        Invoke(Testcommpleted);
                        break;
                    }

                }

            }




        }

        private void DPR100_Test_10()
        {


            int count = Int32.Parse(textBox2_Iteration.Text);
            for (int i = 0; i < count; i++)
            {

                Network_Check(); // Network Check before sending data 

                // Data send to server

                string client_data = "800x600@60MDS8BPC";
                Client.Class1 Client1 = new Client.Class1();
                Client1.Client(textBox1.Text, client_data);

                //// Data reciveve 

                string data_rece;
                SERVER.Class1 server1 = new SERVER.Class1();
                data_rece = server1.Server();





                System.Threading.Thread.Sleep(5000);
                AutomationElement Link_layer = SelectElementNameControlType("Link Layer Tests", ControlType.TabItem);
                SelectionItem(Link_layer);
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                System.Windows.Forms.SendKeys.SendWait("{TAB}");

                if (i == 0)
                {
                    System.Windows.Forms.SendKeys.SendWait("{UP 35}");
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 9}");
                }


                System.Windows.Forms.SendKeys.SendWait("{TAB}");
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                while (true)
                {
                    

                    AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                    if (Testcommpleted != null)
                    {
                        Invoke(Testcommpleted);
                        break;
                    }

                }

            }




        }

        private void DPR100_Test_11()
        {


            int count = Int32.Parse(textBox2_Iteration.Text);
            for (int i = 0; i < count; i++)
            {

                Network_Check(); // Network Check before sending data 

                // Data send to server

                string client_data = "800x600@60MDS8BPC";
                Client.Class1 Client1 = new Client.Class1();
                Client1.Client(textBox1.Text, client_data);

                //// Data reciveve 

                string data_rece;
                SERVER.Class1 server1 = new SERVER.Class1();
                data_rece = server1.Server();





                System.Threading.Thread.Sleep(5000);
                AutomationElement Link_layer = SelectElementNameControlType("Link Layer Tests", ControlType.TabItem);
                SelectionItem(Link_layer);
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                System.Windows.Forms.SendKeys.SendWait("{TAB}");

                if (i == 0)
                {
                    System.Windows.Forms.SendKeys.SendWait("{UP 35}");
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 10}");
                }


                System.Windows.Forms.SendKeys.SendWait("{TAB}");
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                while (true)
                {
                    

                    AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                    if (Testcommpleted != null)
                    {
                        Invoke(Testcommpleted);
                        break;
                    }

                }

            }




        }

        private void DPR100_Test_12()
        {


            int count = Int32.Parse(textBox2_Iteration.Text);
            for (int i = 0; i < count; i++)
            {

                Network_Check(); // Network Check before sending data 

                // Data send to server

                string client_data = "800x600@60MDS8BPC";
                Client.Class1 Client1 = new Client.Class1();
                Client1.Client(textBox1.Text, client_data);

                //// Data reciveve 

                string data_rece;
                SERVER.Class1 server1 = new SERVER.Class1();
                data_rece = server1.Server();





                System.Threading.Thread.Sleep(5000);
                AutomationElement Link_layer = SelectElementNameControlType("Link Layer Tests", ControlType.TabItem);
                SelectionItem(Link_layer);
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                System.Windows.Forms.SendKeys.SendWait("{TAB}");

                if (i == 0)
                {
                    System.Windows.Forms.SendKeys.SendWait("{UP 35}");
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 11}");
                }


                System.Windows.Forms.SendKeys.SendWait("{TAB}");
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                while (true)
                {
                    

                    AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                    if (Testcommpleted != null)
                    {
                        Invoke(Testcommpleted);
                        break;
                    }

                }

            }




        }

        private void DPR100_Test_13()
        {


            int count = Int32.Parse(textBox2_Iteration.Text);
            for (int i = 0; i < count; i++)
            {

                Network_Check(); // Network Check before sending data 

                // Data send to server

                string client_data = "800x600@60MDS8BPC";
                Client.Class1 Client1 = new Client.Class1();
                Client1.Client(textBox1.Text, client_data);

                //// Data reciveve 

                string data_rece;
                SERVER.Class1 server1 = new SERVER.Class1();
                data_rece = server1.Server();





                System.Threading.Thread.Sleep(5000);
                AutomationElement Link_layer = SelectElementNameControlType("Link Layer Tests", ControlType.TabItem);
                SelectionItem(Link_layer);
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                System.Windows.Forms.SendKeys.SendWait("{TAB}");

                if (i == 0)
                {
                    System.Windows.Forms.SendKeys.SendWait("{UP 35}");
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 12}");
                }


                System.Windows.Forms.SendKeys.SendWait("{TAB}");
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                while (true)
                {
                    

                    AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                    if (Testcommpleted != null)
                    {
                        Invoke(Testcommpleted);
                        break;
                    }

                }

            }




        }

        private void DPR100_Test_14()
        {


            int count = Int32.Parse(textBox2_Iteration.Text);
            for (int i = 0; i < count; i++)
            {

                Network_Check(); // Network Check before sending data 

                // Data send to server

                string client_data = "800x600@60MDS8BPC";
                Client.Class1 Client1 = new Client.Class1();
                Client1.Client(textBox1.Text, client_data);

                //// Data reciveve 

                string data_rece;
                SERVER.Class1 server1 = new SERVER.Class1();
                data_rece = server1.Server();





                System.Threading.Thread.Sleep(5000);
                AutomationElement Link_layer = SelectElementNameControlType("Link Layer Tests", ControlType.TabItem);
                SelectionItem(Link_layer);
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                System.Windows.Forms.SendKeys.SendWait("{TAB}");

                if (i == 0)
                {
                    System.Windows.Forms.SendKeys.SendWait("{UP 35}");
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 13}");
                }


                System.Windows.Forms.SendKeys.SendWait("{TAB}");
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                while (true)
                {
                    

                    AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                    if (Testcommpleted != null)
                    {
                        Invoke(Testcommpleted);
                        break;
                    }

                }

            }




        }

        private void DPR100_Test_15()
        {


            int count = Int32.Parse(textBox2_Iteration.Text);
            for (int i = 0; i < count; i++)
            {

                Network_Check(); // Network Check before sending data 

                // Data send to server

                string client_data = "800x600@60MDS8BPC";
                Client.Class1 Client1 = new Client.Class1();
                Client1.Client(textBox1.Text, client_data);

                //// Data reciveve 

                string data_rece;
                SERVER.Class1 server1 = new SERVER.Class1();
                data_rece = server1.Server();





                System.Threading.Thread.Sleep(5000);
                AutomationElement Link_layer = SelectElementNameControlType("Link Layer Tests", ControlType.TabItem);
                SelectionItem(Link_layer);
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                System.Windows.Forms.SendKeys.SendWait("{TAB}");

                if (i == 0)
                {
                    System.Windows.Forms.SendKeys.SendWait("{UP 35}");
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 14}");
                }


                System.Windows.Forms.SendKeys.SendWait("{TAB}");
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                while (true)
                {
                    

                    AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                    if (Testcommpleted != null)
                    {
                        Invoke(Testcommpleted);
                        break;
                    }

                }

            }




        }

        private void DPR100_Test_16()
        {


            int count = Int32.Parse(textBox2_Iteration.Text);
            for (int i = 0; i < count; i++)
            {

                Network_Check(); // Network Check before sending data 

                // Data send to server

                string client_data = "800x600@60MDS8BPC";
                Client.Class1 Client1 = new Client.Class1();
                Client1.Client(textBox1.Text, client_data);

                //// Data reciveve 

                string data_rece;
                SERVER.Class1 server1 = new SERVER.Class1();
                data_rece = server1.Server();





                System.Threading.Thread.Sleep(5000);
                AutomationElement Link_layer = SelectElementNameControlType("Link Layer Tests", ControlType.TabItem);
                SelectionItem(Link_layer);
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                System.Windows.Forms.SendKeys.SendWait("{TAB}");

                if (i == 0)
                {
                    System.Windows.Forms.SendKeys.SendWait("{UP 35}");
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 15}");
                }


                System.Windows.Forms.SendKeys.SendWait("{TAB}");
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                while (true)
                {
                    

                    AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                    if (Testcommpleted != null)
                    {
                        Invoke(Testcommpleted);
                        break;
                    }

                }

            }




        }

        private void DPR100_Test_17()
        {


            int count = Int32.Parse(textBox2_Iteration.Text);
            for (int i = 0; i < count; i++)
            {

                Network_Check(); // Network Check before sending data 

                // Data send to server

                string client_data = "800x600@60MDS8BPC";
                Client.Class1 Client1 = new Client.Class1();
                Client1.Client(textBox1.Text, client_data);

                //// Data reciveve 

                string data_rece;
                SERVER.Class1 server1 = new SERVER.Class1();
                data_rece = server1.Server();





                System.Threading.Thread.Sleep(5000);
                AutomationElement Link_layer = SelectElementNameControlType("Link Layer Tests", ControlType.TabItem);
                SelectionItem(Link_layer);
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                System.Windows.Forms.SendKeys.SendWait("{TAB}");

                if (i == 0)
                {
                    System.Windows.Forms.SendKeys.SendWait("{UP 35}");
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 16}");
                }


                System.Windows.Forms.SendKeys.SendWait("{TAB}");
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                while (true)
                {
                    

                    AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                    if (Testcommpleted != null)
                    {
                        Invoke(Testcommpleted);
                        break;
                    }

                }

            }




        }

        private void DPR100_Test_18()
        {


            int count = Int32.Parse(textBox2_Iteration.Text);
            for (int i = 0; i < count; i++)
            {

                Network_Check(); // Network Check before sending data 

                // Data send to server

                string client_data = "800x600@60MDS8BPC";
                Client.Class1 Client1 = new Client.Class1();
                Client1.Client(textBox1.Text, client_data);

                //// Data reciveve 

                string data_rece;
                SERVER.Class1 server1 = new SERVER.Class1();
                data_rece = server1.Server();





                System.Threading.Thread.Sleep(5000);
                AutomationElement Link_layer = SelectElementNameControlType("Link Layer Tests", ControlType.TabItem);
                SelectionItem(Link_layer);
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                System.Windows.Forms.SendKeys.SendWait("{TAB}");

                if (i == 0)
                {
                    System.Windows.Forms.SendKeys.SendWait("{UP 35}");
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 17}");
                }


                System.Windows.Forms.SendKeys.SendWait("{TAB}");
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                while (true)
                {
                    

                    AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                    if (Testcommpleted != null)
                    {
                        Invoke(Testcommpleted);
                        break;
                    }

                }

            }




        }

        private void DPR100_Test_19()
        {


            int count = Int32.Parse(textBox2_Iteration.Text);
            for (int i = 0; i < count; i++)
            {

                Network_Check(); // Network Check before sending data 

                // Data send to server

                string client_data = "800x600@60MDS8BPC";
                Client.Class1 Client1 = new Client.Class1();
                Client1.Client(textBox1.Text, client_data);

                //// Data reciveve 

                string data_rece;
                SERVER.Class1 server1 = new SERVER.Class1();
                data_rece = server1.Server();





                System.Threading.Thread.Sleep(5000);
                AutomationElement Link_layer = SelectElementNameControlType("Link Layer Tests", ControlType.TabItem);
                SelectionItem(Link_layer);
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                System.Windows.Forms.SendKeys.SendWait("{TAB}");

                if (i == 0)
                {
                    System.Windows.Forms.SendKeys.SendWait("{UP 35}");
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 18}");
                }


                System.Windows.Forms.SendKeys.SendWait("{TAB}");
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                while (true)
                {
                    

                    AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                    if (Testcommpleted != null)
                    {
                        Invoke(Testcommpleted);
                        break;
                    }

                }

            }




        }

        private void DPR100_Test_20()
        {


            int count = Int32.Parse(textBox2_Iteration.Text);
            for (int i = 0; i < count; i++)
            {

                Network_Check(); // Network Check before sending data 

                // Data send to server

                string client_data = "800x600@60MDS8BPC";
                Client.Class1 Client1 = new Client.Class1();
                Client1.Client(textBox1.Text, client_data);

                //// Data reciveve 

                string data_rece;
                SERVER.Class1 server1 = new SERVER.Class1();
                data_rece = server1.Server();





                System.Threading.Thread.Sleep(5000);
                AutomationElement Link_layer = SelectElementNameControlType("Link Layer Tests", ControlType.TabItem);
                SelectionItem(Link_layer);
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                System.Windows.Forms.SendKeys.SendWait("{TAB}");

                if (i == 0)
                {
                    System.Windows.Forms.SendKeys.SendWait("{UP 35}");
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 19}");
                }


                System.Windows.Forms.SendKeys.SendWait("{TAB}");
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                while (true)
                {
                    

                    AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                    if (Testcommpleted != null)
                    {
                        Invoke(Testcommpleted);
                        break;
                    }

                }

            }




        }

        private void DPR100_Test_21()
        {


            int count = Int32.Parse(textBox2_Iteration.Text);
            for (int i = 0; i < count; i++)
            {

                Network_Check(); // Network Check before sending data 

                // Data send to server

                string client_data = "800x600@60MDS8BPC";
                Client.Class1 Client1 = new Client.Class1();
                Client1.Client(textBox1.Text, client_data);

                //// Data reciveve 

                string data_rece;
                SERVER.Class1 server1 = new SERVER.Class1();
                data_rece = server1.Server();





                System.Threading.Thread.Sleep(5000);
                AutomationElement Link_layer = SelectElementNameControlType("Link Layer Tests", ControlType.TabItem);
                SelectionItem(Link_layer);
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                System.Windows.Forms.SendKeys.SendWait("{TAB}");

                if (i == 0)
                {
                    System.Windows.Forms.SendKeys.SendWait("{UP 35}");
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 20}");
                }


                System.Windows.Forms.SendKeys.SendWait("{TAB}");
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                while (true)
                {
                    

                    AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                    if (Testcommpleted != null)
                    {
                        Invoke(Testcommpleted);
                        break;
                    }

                }

            }




        }

        private void DPR100_Test_22()
        {


            int count = Int32.Parse(textBox2_Iteration.Text);
            for (int i = 0; i < count; i++)
            {

                Network_Check(); // Network Check before sending data 

                // Data send to server

                string client_data = "800x600@60MDS8BPC";
                Client.Class1 Client1 = new Client.Class1();
                Client1.Client(textBox1.Text, client_data);

                //// Data reciveve 

                string data_rece;
                SERVER.Class1 server1 = new SERVER.Class1();
                data_rece = server1.Server();





                System.Threading.Thread.Sleep(5000);
                AutomationElement Link_layer = SelectElementNameControlType("Link Layer Tests", ControlType.TabItem);
                SelectionItem(Link_layer);
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                System.Windows.Forms.SendKeys.SendWait("{TAB}");

                if (i == 0)
                {
                    System.Windows.Forms.SendKeys.SendWait("{UP 35}");
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 21}");
                }


                System.Windows.Forms.SendKeys.SendWait("{TAB}");
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                while (true)
                {
                    

                    AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                    if (Testcommpleted != null)
                    {
                        Invoke(Testcommpleted);
                        break;
                    }

                }

            }




        }

        private void DPR100_Test_23()
        {


            int count = Int32.Parse(textBox2_Iteration.Text);
            for (int i = 0; i < count; i++)
            {

                Network_Check(); // Network Check before sending data 

                // Data send to server

                string client_data = "800x600@60MDS8BPC";
                Client.Class1 Client1 = new Client.Class1();
                Client1.Client(textBox1.Text, client_data);

                //// Data reciveve 

                string data_rece;
                SERVER.Class1 server1 = new SERVER.Class1();
                data_rece = server1.Server();





                System.Threading.Thread.Sleep(5000);
                AutomationElement Link_layer = SelectElementNameControlType("Link Layer Tests", ControlType.TabItem);
                SelectionItem(Link_layer);
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                System.Windows.Forms.SendKeys.SendWait("{TAB}");

                if (i == 0)
                {
                    System.Windows.Forms.SendKeys.SendWait("{UP 35}");
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 22}");
                }


                System.Windows.Forms.SendKeys.SendWait("{TAB}");
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                while (true)
                {
                   

                    AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                    if (Testcommpleted != null)
                    {
                        Invoke(Testcommpleted);
                        break;
                    }

                }

            }




        }

        private void DPR100_Test_24()
        {


            int count = Int32.Parse(textBox2_Iteration.Text);
            for (int i = 0; i < count; i++)
            {

                Network_Check(); // Network Check before sending data 

                // Data send to server

                string client_data = "800x600@60MDS8BPC";
                Client.Class1 Client1 = new Client.Class1();
                Client1.Client(textBox1.Text, client_data);

                //// Data reciveve 

                string data_rece;
                SERVER.Class1 server1 = new SERVER.Class1();
                data_rece = server1.Server();





                System.Threading.Thread.Sleep(5000);
                AutomationElement Link_layer = SelectElementNameControlType("Link Layer Tests", ControlType.TabItem);
                SelectionItem(Link_layer);
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                System.Windows.Forms.SendKeys.SendWait("{TAB}");

                if (i == 0)
                {
                    System.Windows.Forms.SendKeys.SendWait("{UP 35}");
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 23}");
                }


                System.Windows.Forms.SendKeys.SendWait("{TAB}");
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                while (true)
                {
                    

                    AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                    if (Testcommpleted != null)
                    {
                        Invoke(Testcommpleted);
                        break;
                    }

                }

            }




        }

        private void DPR100_Test_25()
        {


            int count = Int32.Parse(textBox2_Iteration.Text);
            for (int i = 0; i < count; i++)
            {

                Network_Check(); // Network Check before sending data 

                // Data send to server

                string client_data = "800x600@60MDS8BPC";
                Client.Class1 Client1 = new Client.Class1();
                Client1.Client(textBox1.Text, client_data);

                //// Data reciveve 

                string data_rece;
                SERVER.Class1 server1 = new SERVER.Class1();
                data_rece = server1.Server();





                System.Threading.Thread.Sleep(5000);
                AutomationElement Link_layer = SelectElementNameControlType("Link Layer Tests", ControlType.TabItem);
                SelectionItem(Link_layer);
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                System.Windows.Forms.SendKeys.SendWait("{TAB}");

                if (i == 0)
                {
                    System.Windows.Forms.SendKeys.SendWait("{UP 35}");
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 24}");
                }


                System.Windows.Forms.SendKeys.SendWait("{TAB}");
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                while (true)
                {
                    

                    AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                    if (Testcommpleted != null)
                    {
                        Invoke(Testcommpleted);
                        break;
                    }

                }

            }




        }

        private void DPR100_Test_26()
        {


            int count = Int32.Parse(textBox2_Iteration.Text);
            for (int i = 0; i < count; i++)
            {

                Network_Check(); // Network Check before sending data 

                // Data send to server

                string client_data = "800x600@60MDS8BPC";
                Client.Class1 Client1 = new Client.Class1();
                Client1.Client(textBox1.Text, client_data);

                //// Data reciveve 

                string data_rece;
                SERVER.Class1 server1 = new SERVER.Class1();
                data_rece = server1.Server();





                System.Threading.Thread.Sleep(5000);
                AutomationElement Link_layer = SelectElementNameControlType("Link Layer Tests", ControlType.TabItem);
                SelectionItem(Link_layer);
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                System.Windows.Forms.SendKeys.SendWait("{TAB}");

                if (i == 0)
                {
                    System.Windows.Forms.SendKeys.SendWait("{UP 35}");
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 25}");
                }


                System.Windows.Forms.SendKeys.SendWait("{TAB}");
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                while (true)
                {
                    

                    AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                    if (Testcommpleted != null)
                    {
                        Invoke(Testcommpleted);
                        break;
                    }

                }

            }




        }

        private void DPR100_Test_27()
        {


            int count = Int32.Parse(textBox2_Iteration.Text);
            for (int i = 0; i < count; i++)
            {

                Network_Check(); // Network Check before sending data 

                // Data send to server

                string client_data = "800x600@60MDS8BPC";
                Client.Class1 Client1 = new Client.Class1();
                Client1.Client(textBox1.Text, client_data);

                //// Data reciveve 

                string data_rece;
                SERVER.Class1 server1 = new SERVER.Class1();
                data_rece = server1.Server();





                System.Threading.Thread.Sleep(5000);
                AutomationElement Link_layer = SelectElementNameControlType("Link Layer Tests", ControlType.TabItem);
                SelectionItem(Link_layer);
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                System.Windows.Forms.SendKeys.SendWait("{TAB}");

                if (i == 0)
                {
                    System.Windows.Forms.SendKeys.SendWait("{UP 35}");
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 26}");
                }


                System.Windows.Forms.SendKeys.SendWait("{TAB}");
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                while (true)
                {
                    

                    AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                    if (Testcommpleted != null)
                    {
                        Invoke(Testcommpleted);
                        break;
                    }

                }

            }




        }
        


//DPR100 Applet Test "28 "  4.3.3.1 Video Time Stamp genaration 

        private void DPR100_Applet_4_3_3_1()

        {
            int count = Int32.Parse(textBox2_Iteration.Text);
            for (int i = 0; i < count; i++)
            {


                


                System.Threading.Thread.Sleep(3000);
                AutomationElement Link_layer = SelectElementNameControlType("Link Layer Tests", ControlType.TabItem);
                SelectionItem(Link_layer);
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                System.Windows.Forms.SendKeys.SendWait("{TAB}");

                if (i == 0)
                {
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 1}");
                    System.Windows.Forms.SendKeys.SendWait("{UP 50}");
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 27}");
                }

                System.Windows.Forms.SendKeys.SendWait("{TAB}");
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                int Patter_no = 0;
                while (true)
                {
                    System.Threading.Thread.Sleep(1000);

                    AutomationElement PatternApply_Proceed = SelectElementNameControlType("Proceed", ControlType.Button);

                    

                    if (PatternApply_Proceed != null)
                    {


                        if (Patter_no == 0 || Patter_no == 2)
                        {
                            Network_Check(); // Network Check before sending data 

                            // Data send to server
                          
                            string client_data = "-dDPB -n640x480@6";
                            Client.Class1 Client1 = new Client.Class1();
                            Client1.Client(textBox1.Text, client_data);
                            string str = Convert.ToString(Patter_no);


                            ////// Data reciveve 

                            string data_rece;
                            SERVER.Class1 server1 = new SERVER.Class1();
                            data_rece = server1.Server();
                            Invoke(PatternApply_Proceed);
                            System.Threading.Thread.Sleep(10000);

                            Patter_no++;

                        }

                        if (Patter_no == 1)
                        {
                            Network_Check(); // Network Check before sending data 
                            // Data send to server

                             string client_data = "-dDPB -n1920x1080@8";
                            Client.Class1 Client1 = new Client.Class1();
                            Client1.Client(textBox1.Text, client_data);
                            string str = Convert.ToString(Patter_no);


                            ////// Data reciveve 

                            string data_rece;
                            SERVER.Class1 server1 = new SERVER.Class1();
                            data_rece = server1.Server();
                            
                            Invoke(PatternApply_Proceed);
                            System.Threading.Thread.Sleep(10000);
                            Patter_no++;

                        }
                        if (Patter_no == 3)
                        {
                            Network_Check(); // Network Check before sending data 
                            // Data send to server

                            string client_data = "-dDPB -n1920x1440@8";
                            Client.Class1 Client1 = new Client.Class1();
                            Client1.Client(textBox1.Text, client_data);
                            string str = Convert.ToString(Patter_no);


                            ////// Data reciveve 

                            string data_rece;
                            SERVER.Class1 server1 = new SERVER.Class1();
                            data_rece = server1.Server();
                            
                            Invoke(PatternApply_Proceed);
                            System.Threading.Thread.Sleep(10000);
                            Patter_no++;

                        }

                    }



                    AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                    if (Testcommpleted != null)
                    {
                        Invoke(Testcommpleted);
                        break;
                    }



                }


            }
        
        
        }

//DPR100 Applet Test " 29 "  4.4.1.1  Pixel Data Packing and Steering

        private void DPR100_Applet_4_4_1_1()
        {

            int count = Int32.Parse(textBox2_Iteration.Text);
            for (int i = 0; i < count; i++)
            {


                


                System.Threading.Thread.Sleep(3000);
                AutomationElement Link_layer = SelectElementNameControlType("Link Layer Tests", ControlType.TabItem);
                SelectionItem(Link_layer);
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                System.Windows.Forms.SendKeys.SendWait("{TAB}");

                if (i == 0)
                {
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 1}");
                    System.Windows.Forms.SendKeys.SendWait("{UP 50}");
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 28}");
                }

                System.Windows.Forms.SendKeys.SendWait("{TAB}");
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                int Patter_no = 0;
                while (true)
                {
                    System.Threading.Thread.Sleep(1000);

                    AutomationElement PatternApply_Proceed = SelectElementNameControlType("Proceed", ControlType.Button);



                    if (PatternApply_Proceed != null)
                    {


                        if (Patter_no == 0 || Patter_no == 2 || Patter_no == 4 || Patter_no == 6)
                        {

                            Network_Check(); // Network Check before sending data 
                            // Data send to server
                            
                            string client_data = "-dDPB -n640x480@6";
                            Client.Class1 Client1 = new Client.Class1();
                            Client1.Client(textBox1.Text, client_data);
                            string str = Convert.ToString(Patter_no);
                            

                            ////// Data reciveve 

                            string data_rece;
                            SERVER.Class1 server1 = new SERVER.Class1();
                            data_rece = server1.Server();
                            
                            Invoke(PatternApply_Proceed);
                            System.Threading.Thread.Sleep(10000);

                            Patter_no++;

                        }

                        if (Patter_no == 1 || Patter_no == 3 || Patter_no == 5 || Patter_no == 7)
                        {

                            Network_Check(); // Network Check before sending data 
                            // Data send to server

                            
                            string client_data = "-dDPB -n640x480@8";
                            Client.Class1 Client1 = new Client.Class1();
                            Client1.Client(textBox1.Text, client_data);
                            string str = Convert.ToString(Patter_no);
                            

                            ////// Data reciveve 

                            string data_rece;
                            SERVER.Class1 server1 = new SERVER.Class1();
                            data_rece = server1.Server();
                            
                            Invoke(PatternApply_Proceed);
                            System.Threading.Thread.Sleep(10000);
                            Patter_no++;

                        }
                    }

                    AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                    if (Testcommpleted != null)
                    {
                        Invoke(Testcommpleted);
                        break;
                    }



                }


            }

        
        
        
        }


 //DPR100 Applet Test " 30 "  4.4.1.2  Main Stream Data Packing and Stuffing - Least Packed TC

        private void DPR100_Applet_4_4_1_2()
        { 
        
            


                       int count = Int32.Parse(textBox2_Iteration.Text);
                        for (int i = 0; i < count; i++)
                        {


                            


                            System.Threading.Thread.Sleep(3000);
                            AutomationElement Link_layer = SelectElementNameControlType("Link Layer Tests", ControlType.TabItem);
                            SelectionItem(Link_layer);
                            System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                            System.Windows.Forms.SendKeys.SendWait("{TAB}");

                            if (i == 0)
                            {
                                System.Windows.Forms.SendKeys.SendWait("{DOWN 1}");
                                System.Windows.Forms.SendKeys.SendWait("{UP 50}");
                                System.Windows.Forms.SendKeys.SendWait("{DOWN 29}");
                            }

                            System.Windows.Forms.SendKeys.SendWait("{TAB}");
                            System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                            int Patter_no = 0;
                            while (true)
                            {
                                System.Threading.Thread.Sleep(1000);

                                AutomationElement PatternApply_Proceed = SelectElementNameControlType("Proceed", ControlType.Button);



                                if (PatternApply_Proceed != null)
                                {


                                    if (Patter_no == 0 )
                                    {
                                        Network_Check(); // Network Check before sending data 
                                        // Data send to server
                                        string client_data = "-dDPB -n640x480@6";
                                        Client.Class1 Client1 = new Client.Class1();
                                        Client1.Client(textBox1.Text, client_data);
                                        string str = Convert.ToString(Patter_no);
                        

                                        ////// Data reciveve 

                                        string data_rece;
                                        SERVER.Class1 server1 = new SERVER.Class1();
                                        data_rece = server1.Server();
                                        Invoke(PatternApply_Proceed);
                                        System.Threading.Thread.Sleep(10000);

                                        Patter_no++;

                                    }

                                }

                                AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                                if (Testcommpleted != null)
                                {
                                    Invoke(Testcommpleted);
                                    break;
                                }



                            }


                        }

            



        
        }


 //DPR100 Applet Test " 31 "  4.4.1.3  Main Stream Data Packing and Stuffing - Most Packed TC


        private void DPR100_Applet_4_4_1_3()
        {

            

            int count = Int32.Parse(textBox2_Iteration.Text);
            for (int i = 0; i < count; i++)
            {


                


                System.Threading.Thread.Sleep(3000);
                AutomationElement Link_layer = SelectElementNameControlType("Link Layer Tests", ControlType.TabItem);
                SelectionItem(Link_layer);
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                System.Windows.Forms.SendKeys.SendWait("{TAB}");

                if (i == 0)
                {
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 1}");
                    System.Windows.Forms.SendKeys.SendWait("{UP 50}");
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 30}");
                }

                System.Windows.Forms.SendKeys.SendWait("{TAB}");
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                int Patter_no = 0;
                while (true)
                {
                    System.Threading.Thread.Sleep(1000);

                    AutomationElement PatternApply_Proceed = SelectElementNameControlType("Proceed", ControlType.Button);



                    if (PatternApply_Proceed != null)
                    {


                        if (Patter_no == 0)
                        {

                            Network_Check(); // Network Check before sending data 
                            // Data send to server
                            string client_data = "-dDPB -n1024x768@6";
                            Client.Class1 Client1 = new Client.Class1();
                            Client1.Client(textBox1.Text, client_data);
                            string str = Convert.ToString(Patter_no);

                            ////// Data reciveve 

                            string data_rece;
                            SERVER.Class1 server1 = new SERVER.Class1();
                            data_rece = server1.Server();
                            
                            Invoke(PatternApply_Proceed);
                            System.Threading.Thread.Sleep(10000);

                            Patter_no++;

                        }

                        if (Patter_no == 1)
                        {
                            Network_Check(); // Network Check before sending data 
                            // Data send to server

                            string client_data = "-l2 -s0 -dDPB -n1280x1024@8";
                            Client.Class1 Client1 = new Client.Class1();
                            Client1.Client(textBox1.Text, client_data);
                            string str = Convert.ToString(Patter_no);


                            ////// Data reciveve 

                            string data_rece;
                            SERVER.Class1 server1 = new SERVER.Class1();
                            data_rece = server1.Server();
                            Invoke(PatternApply_Proceed);
                            System.Threading.Thread.Sleep(10000);
                            Patter_no++;

                        } if (Patter_no == 2)
                        {
                            Network_Check(); // Network Check before sending data 
                            // Data send to server

                            string client_data = "-dDPB -n1792x1344@8";
                            Client.Class1 Client1 = new Client.Class1();
                            Client1.Client(textBox1.Text, client_data);
                            string str = Convert.ToString(Patter_no);


                            ////// Data reciveve 

                            string data_rece;
                            SERVER.Class1 server1 = new SERVER.Class1();
                            data_rece = server1.Server();
                            Invoke(PatternApply_Proceed);
                            System.Threading.Thread.Sleep(10000);
                            Patter_no++;

                        }



                    }

                    AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                    if (Testcommpleted != null)
                    {
                        Invoke(Testcommpleted);
                        break;
                    }



                }


            }

        
        }


//DPR100 Applet Test " 32 "  4.4.2  Not supported by Intel Platform 

//DPR100 Applet Test " 33 "  4.4.3  Power Managment 

        private void DPR100_Applet_4_4_3()
        {


            
            int count = Int32.Parse(textBox2_Iteration.Text);
            for (int i = 0; i < count; i++)
            {


                


                System.Threading.Thread.Sleep(3000);
                AutomationElement Tabitem_RUN_Tests = SelectElementNameControlType("Link Layer Tests", ControlType.TabItem);
                SelectionItem(Tabitem_RUN_Tests);
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                System.Windows.Forms.SendKeys.SendWait("{TAB}");

                if (i == 0)
                {
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 1}");
                    System.Windows.Forms.SendKeys.SendWait("{UP 50}");
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 32}");
                }
                System.Threading.Thread.Sleep(10000);
                System.Windows.Forms.SendKeys.SendWait("{TAB}");
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                int Patter_no = 0;
                while (true)
                {
                    System.Threading.Thread.Sleep(20000);

                    AutomationElement PatternApply_Proceed = SelectElementNameControlType("Proceed", ControlType.Button);



                    if (PatternApply_Proceed != null)
                    {

                        Network_Check(); // Network Check before sending data 
                        // Data send to server
                        string client_data = "-mOFF";
                        Client.Class1 Client1 = new Client.Class1();
                        Client1.Client(textBox1.Text, client_data);
                        string str = Convert.ToString(Patter_no);

                        System.Threading.Thread.Sleep(10000);
                        Invoke(PatternApply_Proceed);
                        System.Threading.Thread.Sleep(50000);
                        
                         
                        Invoke(PatternApply_Proceed);
                       
                       
                        
                    }
                    

                    AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                    if (Testcommpleted != null)
                    {
                        Invoke(Testcommpleted);
                        break;
                    }



                }


            }
        
        }
          
//DPR100 Test "34 and 35"  7.1.1.1 and 7.1.1.2 Additional DPCD Handining Test 1 and Test 2

        private void DPR100_7_1_1_1()

        { 
        
       
                int count = Int32.Parse(textBox2_Iteration.Text);
                for (int i = 0; i < count; i++)
                {

                    Network_Check(); // Network Check before sending data 
                    // Data send to server

                   





                    System.Threading.Thread.Sleep(3000);
                    AutomationElement Link_layer = SelectElementNameControlType("Link Layer Tests", ControlType.TabItem);
                    SelectionItem(Link_layer);
                    System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                    System.Windows.Forms.SendKeys.SendWait("{TAB}");

                    if (i == 0)
                    {
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 1}");
                    System.Windows.Forms.SendKeys.SendWait("{UP 50}");
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 33}");
                    }


                    System.Windows.Forms.SendKeys.SendWait("{TAB}");
                    System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                    while (true)
                    {
                        

                        AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                        if (Testcommpleted != null)
                        {
                            Invoke(Testcommpleted);
                            break;
                        }

                    }

                }
            


        
        }

        private void DPR100_7_1_1_2()
        {


            int count = Int32.Parse(textBox2_Iteration.Text);
            for (int i = 0; i < count; i++)
            {

                Network_Check(); // Network Check before sending data 
                // Data send to server

                





                System.Threading.Thread.Sleep(3000);
                AutomationElement Link_layer = SelectElementNameControlType("Link Layer Tests", ControlType.TabItem);
                SelectionItem(Link_layer);
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                System.Windows.Forms.SendKeys.SendWait("{TAB}");

                if (i == 0)
                {
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 1}");
                    System.Windows.Forms.SendKeys.SendWait("{UP 50}");
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 34}");
                }


                System.Windows.Forms.SendKeys.SendWait("{TAB}");
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                while (true)
                {
                    

                    AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                    if (Testcommpleted != null)
                    {
                        Invoke(Testcommpleted);
                        break;
                    }

                }

            }




        }

    
// DPR100 Audio Test " 1 "   4.4.4.2  Intel Platform is not supported this test 


// DPR100 Audio Test " 2 " 4.4.4.3   Audio Time Stamp Genaration 

        private void DPR100_Audio_Test_4_4_4_3()
        {

            int count = Int32.Parse(textBox2_Iteration.Text);
            for (int i = 0; i < count; i++)
            {


                // Data send to server

                



                System.Threading.Thread.Sleep(4000);

                AutomationElement Audio_Tests = SelectElementNameControlType("Audio Tests", ControlType.TabItem);
                SelectionItem(Audio_Tests);
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                System.Windows.Forms.SendKeys.SendWait("{TAB}");

                if (i == 0)
                {
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 2}");
                }


                System.Windows.Forms.SendKeys.SendWait("{TAB}");
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                int Patter_no = 0;
                while (true)
                {
                    System.Threading.Thread.Sleep(1000);


                    AutomationElement PatternApply_Proceed = SelectElementNameControlType("Proceed", ControlType.Button);



                    if (PatternApply_Proceed != null)
                    {


                        if (Patter_no == 0 || Patter_no == 2 || Patter_no == 4 || Patter_no == 6 || Patter_no == 8 || Patter_no == 10)
                        {
                            
                            Network_Check(); // Network Check before sending data 
                            System.Threading.Thread.Sleep(5000);
                            // Data send to server
                            string client_data = "2_Channel_48000Hz_24bits_20s.wav";
                            Client.Class1 Client1 = new Client.Class1();
                          
                            Client1.Client(textBox1.Text, client_data);
                            string str = Convert.ToString(Patter_no);

                            ////// Data reciveve 

                            string data_rece;
                            SERVER.Class1 server1 = new SERVER.Class1();
                            data_rece = server1.Server();
                            
                            Invoke(PatternApply_Proceed);
                            System.Threading.Thread.Sleep(10000);

                            Patter_no++;

                        } if (Patter_no == 1 || Patter_no == 3 || Patter_no == 5 || Patter_no == 7 || Patter_no == 9 || Patter_no == 11)
                        {
                            Network_Check(); // Network Check before sending data 
                            System.Threading.Thread.Sleep(5000);
                            // Data send to server
                            string client_data = "2_Channel_192000Hz_16bits_20s.wav";
                            Client.Class1 Client1 = new Client.Class1();
                            Client1.Client(textBox1.Text, client_data);
                            string str = Convert.ToString(Patter_no);

                            ////// Data reciveve 

                            string data_rece;
                            SERVER.Class1 server1 = new SERVER.Class1();
                            data_rece = server1.Server();
                            
                            Invoke(PatternApply_Proceed);
                            System.Threading.Thread.Sleep(10000);

                            Patter_no++;


                        }





                        AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                        if (Testcommpleted != null)
                        {
                            Invoke(Testcommpleted);
                            break;
                        }

                    }


                }






            }



        
        }

        private void SKL_DPR100_Audio_Test_4_4_4_3()
        {

            int count = Int32.Parse(textBox2_Iteration.Text);
            for (int i = 0; i < count; i++)
            {

                System.Threading.Thread.Sleep(4000);

                AutomationElement Audio_Tests = SelectElementNameControlType("Audio Tests", ControlType.TabItem);
                SelectionItem(Audio_Tests);
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                System.Windows.Forms.SendKeys.SendWait("{TAB}");

                if (i == 0)
                {
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 2}");
                }


                System.Windows.Forms.SendKeys.SendWait("{TAB}");
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                int Patter_no = 0;
                while (true)
                {
                    System.Threading.Thread.Sleep(1000);


                    AutomationElement PatternApply_Proceed = SelectElementNameControlType("Proceed", ControlType.Button);



                    if (PatternApply_Proceed != null)
                    {


                        if (Patter_no == 0 || Patter_no == 2 || Patter_no == 4 || Patter_no == 6 || Patter_no == 8 || Patter_no == 10)
                        {
                            Network_Check(); // Network Check before sending data 
                            System.Threading.Thread.Sleep(20000);
                            // Data send to server
                            string client_data = "2_Channel_48000Hz_24bits_20s.wav";
                            Client.Class1 Client1 = new Client.Class1();
                            Client1.Client(textBox1.Text, client_data);
                            string str = Convert.ToString(Patter_no);
                            
                            ////// Data reciveve 

                            string data_rece1;
                            SERVER.Class1 server1 = new SERVER.Class1();
                            data_rece1 = server1.Server();
                           
                            System.Threading.Thread.Sleep(2000);
                            Invoke(PatternApply_Proceed);
                            System.Threading.Thread.Sleep(10000);

                            Patter_no++;

                        } if (Patter_no == 1 || Patter_no == 3 || Patter_no == 5 || Patter_no == 7 || Patter_no == 9 || Patter_no == 11)
                        {
                            Network_Check(); // Network Check before sending data
                            System.Threading.Thread.Sleep(20000);
                            // Data send to server
                            string client_data = "2_Channel_192000Hz_16bits_20s.wav";
                            Client.Class1 Client1 = new Client.Class1();
                            Client1.Client(textBox1.Text, client_data);
                            string str = Convert.ToString(Patter_no);
                            
                            ////// Data reciveve 

                            string data_rece2;
                            SERVER.Class1 server1 = new SERVER.Class1();
                            data_rece2 = server1.Server();
                            
                            
                            Invoke(PatternApply_Proceed);
                            System.Threading.Thread.Sleep(10000);

                            Patter_no++;


                        }





                        AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                        if (Testcommpleted != null)
                        {
                            Invoke(Testcommpleted);
                            break;
                        }

                    }


                }






            }




        }

// DPR100 Audio Test  "3 " 4.4.4.4 Audio InforFrame Packet

        private void DPR100_Audio_Test_4_4_4_4()
        {

            int count1 = Int32.Parse(textBox2_Iteration.Text);
            for (int i = 0; i < count1; i++)
            {


                // Data send to server

                





                AutomationElement Audio_Tests = SelectElementNameControlType("Audio Tests", ControlType.TabItem);
                SelectionItem(Audio_Tests);
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                System.Windows.Forms.SendKeys.SendWait("{TAB}");

                if (i == 0)
                {
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 1}");
                    System.Windows.Forms.SendKeys.SendWait("{UP 10}");
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 2}");
                }


                System.Windows.Forms.SendKeys.SendWait("{TAB}");
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                int Patter_no = 0;
                while (true)
                {
                    System.Threading.Thread.Sleep(1000);


                    AutomationElement PatternApply_Proceed = SelectElementNameControlType("Proceed", ControlType.Button);



                    if (PatternApply_Proceed != null)
                    {


                        if (Patter_no == 0 || Patter_no == 1 || Patter_no == 2 || Patter_no == 3)
                        {
                            Network_Check(); // Network Check before sending data 
                            System.Threading.Thread.Sleep(20000);
                            // Data send to server
                            string client_data = "2_Channel_48000Hz_24bits_20s.wav";
                            Client.Class1 Client1 = new Client.Class1();
                            Client1.Client(textBox1.Text, client_data);
                            string str = Convert.ToString(Patter_no);

                            ////// Data reciveve 

                            string data_rece;
                            SERVER.Class1 server1 = new SERVER.Class1();
                            data_rece = server1.Server();
                            
                            Invoke(PatternApply_Proceed);
                            System.Threading.Thread.Sleep(20000);

                            Patter_no++;

                        }
                        





                        AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                        if (Testcommpleted != null)
                        {
                            Invoke(Testcommpleted);
                            break;
                        }

                    }


                }






            }
        
        
        
        }


 // DPR100 Audio Test " 4" 4.4.4.5 Audio Steam Transmission 

        private void DPR100_Audio_Test_4_4_4_5()
        {

            int count2 = Int32.Parse(textBox2_Iteration.Text);
            for (int i = 0; i < count2; i++)
            {


                





                AutomationElement Audio_Tests = SelectElementNameControlType("Audio Tests", ControlType.TabItem);
                SelectionItem(Audio_Tests);
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                System.Windows.Forms.SendKeys.SendWait("{TAB}");

                if (i == 0)
                {
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 1}");
                    System.Windows.Forms.SendKeys.SendWait("{UP 10}");
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 3}");
                }


                System.Windows.Forms.SendKeys.SendWait("{TAB}");
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                int Patter_no = 0;
                while (true)
                {
                    System.Threading.Thread.Sleep(1000);


                    AutomationElement PatternApply_Proceed = SelectElementNameControlType("Proceed", ControlType.Button);



                    if (PatternApply_Proceed != null)
                    {


                        if (Patter_no == 0 || Patter_no == 2 || Patter_no == 4 || Patter_no == 6 || Patter_no == 8 || Patter_no == 10)
                        {
                            Network_Check(); // Network Check before sending data 
                            System.Threading.Thread.Sleep(4000);
                            // Data send to server
                            string client_data = "2_Channel_48000Hz_24bits_20s.wav";
                            Client.Class1 Client1 = new Client.Class1();
                            Client1.Client(textBox1.Text, client_data);
                            string str = Convert.ToString(Patter_no);

                            ////// Data reciveve 

                            string data_rece;
                            SERVER.Class1 server1 = new SERVER.Class1();
                            data_rece = server1.Server();
                            
                            Invoke(PatternApply_Proceed);
                            System.Threading.Thread.Sleep(10000);
                            AutomationElement Two_Channel_Select = SelectElementNameControlType("Channels 1 & 2", ControlType.RadioButton);
                            SelectionItem(Two_Channel_Select);
                            AutomationElement Two_Channel_Pass = SelectElementNameControlType("Pass", ControlType.Button);
                            Invoke(Two_Channel_Pass);
                            System.Threading.Thread.Sleep(15000);
                            AutomationElement TE_Pass = SelectElementNameControlType("Pass", ControlType.Button);
                            Invoke(TE_Pass);
                            System.Threading.Thread.Sleep(10000);
                            Patter_no++;

                        } if (Patter_no == 1 || Patter_no == 3 || Patter_no == 5 || Patter_no == 7 || Patter_no == 9 || Patter_no == 11)
                        {
                            Network_Check(); // Network Check before sending data 
                            System.Threading.Thread.Sleep(4000);
                            // Data send to server
                            string client_data = "8_Channel_192000Hz_16bits_20s.wav";
                            Client.Class1 Client1 = new Client.Class1();
                            Client1.Client(textBox1.Text, client_data);
                            string str = Convert.ToString(Patter_no);

                            ////// Data reciveve 

                            string data_rece;
                            SERVER.Class1 server1 = new SERVER.Class1();
                            data_rece = server1.Server();
                            
                            Invoke(PatternApply_Proceed);
                            System.Threading.Thread.Sleep(10000);

                            AutomationElement Eight_Channel_Select = SelectElementNameControlType("Channels 7 & 8", ControlType.RadioButton);
                            SelectionItem(Eight_Channel_Select);
                            AutomationElement Eight_Channel_Pass = SelectElementNameControlType("Pass", ControlType.Button);
                            Invoke(Eight_Channel_Pass);
                            System.Threading.Thread.Sleep(15000);
                            AutomationElement TE1_Pass = SelectElementNameControlType("Pass", ControlType.Button);
                            Invoke(TE1_Pass);
                            System.Threading.Thread.Sleep(10000);
                            Patter_no++;


                        }





                        AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                        if (Testcommpleted != null)
                        {
                            Invoke(Testcommpleted);
                            break;
                        }

                    }


                }






            }

        
        }

        private void SKL_DPR100_Audio_Test_4_4_4_5()
        {

            int count2 = Int32.Parse(textBox2_Iteration.Text);
            for (int i = 0; i < count2; i++)
            {

                AutomationElement Audio_Tests = SelectElementNameControlType("Audio Tests", ControlType.TabItem);
                SelectionItem(Audio_Tests);
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                System.Windows.Forms.SendKeys.SendWait("{TAB}");

                if (i == 0)
                {
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 1}");
                    System.Windows.Forms.SendKeys.SendWait("{UP 10}");
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 3}");
                }


                System.Windows.Forms.SendKeys.SendWait("{TAB}");
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                int Patter_no = 0;
                while (true)
                {
                    System.Threading.Thread.Sleep(1000);


                    AutomationElement PatternApply_Proceed = SelectElementNameControlType("Proceed", ControlType.Button);



                    if (PatternApply_Proceed != null)
                    {


                        if (Patter_no == 0 || Patter_no == 2 || Patter_no == 4 || Patter_no == 6 || Patter_no == 8 || Patter_no == 10)
                        {
                            Network_Check(); // Network Check before sending data 
                            System.Threading.Thread.Sleep(20000);
                            // Data send to server
                            string client_data = "2_Channel_48000Hz_24bits_20s.wav";
                            Client.Class1 Client1 = new Client.Class1();
                            Client1.Client(textBox1.Text, client_data);
                            string str = Convert.ToString(Patter_no);

                            ////// Data reciveve 

                            string data_rece;
                            SERVER.Class1 server1 = new SERVER.Class1();
                            data_rece = server1.Server();
                            
                            Invoke(PatternApply_Proceed);
                            System.Threading.Thread.Sleep(10000);
                            AutomationElement Two_Channel_Select = SelectElementNameControlType("Channels 1 & 2", ControlType.RadioButton);
                            SelectionItem(Two_Channel_Select);
                            AutomationElement Two_Channel_Pass = SelectElementNameControlType("Pass", ControlType.Button);
                            Invoke(Two_Channel_Pass);
                            System.Threading.Thread.Sleep(15000);
                            AutomationElement TE_Pass = SelectElementNameControlType("Pass", ControlType.Button);
                            Invoke(TE_Pass);
                            System.Threading.Thread.Sleep(10000);
                            Patter_no++;

                        } if (Patter_no == 1 || Patter_no == 3 || Patter_no == 5 || Patter_no == 7 || Patter_no == 9 || Patter_no == 11)
                        {
                            Network_Check(); // Network Check before sending data
                            System.Threading.Thread.Sleep(20000);
                            // Data send to server
                            string client_data = "8_Channel_192000Hz_16bits_20s.wav";
                            Client.Class1 Client1 = new Client.Class1();
                            Client1.Client(textBox1.Text, client_data);
                            string str = Convert.ToString(Patter_no);

                            ////// Data reciveve 

                            string data_rece;
                            SERVER.Class1 server1 = new SERVER.Class1();
                            data_rece = server1.Server();
                            
                            Invoke(PatternApply_Proceed);
                            System.Threading.Thread.Sleep(10000);

                            AutomationElement Eight_Channel_Select = SelectElementNameControlType("Channels 7 & 8", ControlType.RadioButton);
                            SelectionItem(Eight_Channel_Select);
                            AutomationElement Eight_Channel_Pass = SelectElementNameControlType("Pass", ControlType.Button);
                            Invoke(Eight_Channel_Pass);
                            System.Threading.Thread.Sleep(15000);
                            AutomationElement TE1_Pass = SelectElementNameControlType("Pass", ControlType.Button);
                            Invoke(TE1_Pass);
                            System.Threading.Thread.Sleep(10000);
                            Patter_no++;


                        }





                        AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                        if (Testcommpleted != null)
                        {
                            Invoke(Testcommpleted);
                            break;
                        }

                    }


                }






            }


        }

// DPR100 Audio Test " 5 " 4.4.4.6 Audio Start Sequence 

        private void DPR100_Audio_Test_4_4_4_6()

        {

            int count1 = Int32.Parse(textBox2_Iteration.Text);
            for (int i = 0; i < count1; i++)
            {


                





                AutomationElement Audio_Tests = SelectElementNameControlType("Audio Tests", ControlType.TabItem);
                SelectionItem(Audio_Tests);
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                System.Windows.Forms.SendKeys.SendWait("{TAB}");

                if (i == 0)
                {
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 1}");
                    System.Windows.Forms.SendKeys.SendWait("{UP 10}");
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 4}");
                }


                System.Windows.Forms.SendKeys.SendWait("{TAB}");
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                int Patter_no = 0;
                while (true)
                {
                    System.Threading.Thread.Sleep(1000);


                    AutomationElement PatternApply_Proceed = SelectElementNameControlType("Proceed", ControlType.Button);



                    if (PatternApply_Proceed != null)
                    {


                        if (Patter_no == 0)
                        {
                            Network_Check(); // Network Check before sending data 
                            System.Threading.Thread.Sleep(1000);
                            // Data send to server
                            string client_data = "2_Channel_48000Hz_24bits_20s.wav";
                            Client.Class1 Client1 = new Client.Class1();
                            Client1.Client(textBox1.Text, client_data);
                            string str = Convert.ToString(Patter_no);
                            

                           ////// Data reciveve 

                            string data_rece;
                            SERVER.Class1 server1 = new SERVER.Class1();
                            data_rece = server1.Server();
                            
                            Invoke(PatternApply_Proceed);
                            System.Threading.Thread.Sleep(10000);
                            AutomationElement Two_Channel_Select = SelectElementNameControlType("Channels 1 & 2", ControlType.RadioButton);
                            SelectionItem(Two_Channel_Select);
                            AutomationElement Two_Channel_Pass = SelectElementNameControlType("Pass", ControlType.Button);
                            Invoke(Two_Channel_Pass);
                            System.Threading.Thread.Sleep(10000);
                            Patter_no++;

                        } if (Patter_no == 1 )
                        {

                            Network_Check(); // Network Check before sending data 
                            System.Threading.Thread.Sleep(1000);
                            // Data send to server
                            string client_data = "8_Channel_192000Hz_16bits_20s.wav";
                            Client.Class1 Client1 = new Client.Class1();
                            Client1.Client(textBox1.Text, client_data);
                            string str = Convert.ToString(Patter_no);


                            ////// Data reciveve 

                            string data_rece;
                            SERVER.Class1 server1 = new SERVER.Class1();
                            data_rece = server1.Server();
                            
                            Invoke(PatternApply_Proceed);
                            System.Threading.Thread.Sleep(10000);
                            AutomationElement Eight_Channel_Select = SelectElementNameControlType("Channels 7 & 8", ControlType.RadioButton);
                            SelectionItem(Eight_Channel_Select);
                            AutomationElement Eight_Channel_Pass = SelectElementNameControlType("Pass", ControlType.Button);
                            Invoke(Eight_Channel_Pass);
                            System.Threading.Thread.Sleep(10000);
                            Patter_no++;


                        }





                        AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                        if (Testcommpleted != null)
                        {
                            Invoke(Testcommpleted);
                            break;
                        }

                    }


                }






            }
        
        }


        private void SKL_DPR100_Audio_Test_4_4_4_6()
        {

            int count1 = Int32.Parse(textBox2_Iteration.Text);
            for (int i = 0; i < count1; i++)
            {
                AutomationElement Audio_Tests = SelectElementNameControlType("Audio Tests", ControlType.TabItem);
                SelectionItem(Audio_Tests);
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                System.Windows.Forms.SendKeys.SendWait("{TAB}");

                if (i == 0)
                {
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 1}");
                    System.Windows.Forms.SendKeys.SendWait("{UP 10}");
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 4}");
                }


                System.Windows.Forms.SendKeys.SendWait("{TAB}");
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                int Patter_no = 0;
                while (true)
                {
                    System.Threading.Thread.Sleep(1000);


                    AutomationElement PatternApply_Proceed = SelectElementNameControlType("Proceed", ControlType.Button);



                    if (PatternApply_Proceed != null)
                    {


                        if (Patter_no == 0)
                        {
                            Network_Check(); // Network Check before sending data 
                            System.Threading.Thread.Sleep(20000);
                            // Data send to server
                            string client_data = "2_Channel_48000Hz_24bits_20s.wav";
                            Client.Class1 Client1 = new Client.Class1();
                            Client1.Client(textBox1.Text, client_data);
                            string str = Convert.ToString(Patter_no);


                            ////// Data reciveve 

                            string data_rece;
                            SERVER.Class1 server1 = new SERVER.Class1();
                            data_rece = server1.Server();
                            
                            Invoke(PatternApply_Proceed);
                            System.Threading.Thread.Sleep(10000);
                            AutomationElement Two_Channel_Select = SelectElementNameControlType("Channels 1 & 2", ControlType.RadioButton);
                            SelectionItem(Two_Channel_Select);
                            AutomationElement Two_Channel_Pass = SelectElementNameControlType("Pass", ControlType.Button);
                            Invoke(Two_Channel_Pass);
                            System.Threading.Thread.Sleep(10000);
                            Patter_no++;

                        } if (Patter_no == 1)
                        {

                            Network_Check(); // Network Check before sending data 
                            System.Threading.Thread.Sleep(20000);
                            // Data send to server
                            string client_data = "8_Channel_192000Hz_16bits_20s.wav";
                            Client.Class1 Client1 = new Client.Class1();
                            Client1.Client(textBox1.Text, client_data);
                            string str = Convert.ToString(Patter_no);


                            ////// Data reciveve 

                            string data_rece;
                            SERVER.Class1 server1 = new SERVER.Class1();
                            data_rece = server1.Server();
                            
                            Invoke(PatternApply_Proceed);
                            System.Threading.Thread.Sleep(10000);
                            AutomationElement Eight_Channel_Select = SelectElementNameControlType("Channels 7 & 8", ControlType.RadioButton);
                            SelectionItem(Eight_Channel_Select);
                            AutomationElement Eight_Channel_Pass = SelectElementNameControlType("Pass", ControlType.Button);
                            Invoke(Eight_Channel_Pass);
                            System.Threading.Thread.Sleep(10000);
                            Patter_no++;


                        }





                        AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                        if (Testcommpleted != null)
                        {
                            Invoke(Testcommpleted);
                            break;
                        }

                    }


                }






            }

        }

// DPR100 Log Save Function 

        private void DPR100_LogSave()
        {
            
           
            
            AutomationElement MenuElement_FILE = SelectElementNameControlType("File", ControlType.MenuItem);
            ExpandCollapse(MenuElement_FILE);

            AutomationElement Save_Report = SelectElementNameControlType("Save Report ...", ControlType.MenuItem);
            Invoke(Save_Report);
            System.Windows.Forms.SendKeys.SendWait("{TAB 10}");
            System.Windows.Forms.SendKeys.SendWait("{ENTER}");
            System.Threading.Thread.Sleep(1000);
            System.Windows.Forms.SendKeys.SendWait("C:\\100logs\\" + Platform.Text + "_" + Driver_Version.Text + "_" + DateTime.Now.ToString("dd.MM.yyyy.hh.mm.ss") + ".html");
            System.Threading.Thread.Sleep(5000);
            
            AutomationElement Save1 = SelectElementNameControlType("Save", ControlType.Button);
            Invoke(Save1);
            System.Threading.Thread.Sleep(5000);

            AutomationElement Save = SelectElementNameControlType("Save Report", ControlType.Button);
            Invoke(Save);
            System.Threading.Thread.Sleep(5000);
        }

//DPR100 APP Close 

        private void DPR100_APP_Close()
        {
           

           
            Process myProcess = new Process();
            foreach (var process in Process.GetProcessesByName("DP_RefSink_CTS"))
            {
                process.Kill();

            }
        
        }


// DPR100 DP HDCP Tests 

        private void DPR100_HDCP_1A_01()
        {

            int count = Int32.Parse(textBox2_Iteration.Text);
            for (int i = 0; i < count; i++)
            {

                Network_Check(); // Network Check before sending data 
                // Data send to server

                string client_data1 = "800x600@60MDS8BPC";
                Client.Class1 Client2 = new Client.Class1();
                Client2.Client(textBox1.Text, client_data1);

                // Data reciveve 

                
                SERVER.Class1 server2 = new SERVER.Class1();
                string data_rece1 = server2.Server();
                





                Network_Check(); // Network Check before sending data 
                // Data send to server

                string client_data = "ENABLE_HDCP";
                Client.Class1 Client1 = new Client.Class1();
                Client1.Client(textBox1.Text, client_data);

                //// Data reciveve 

               
                SERVER.Class1 server1 = new SERVER.Class1();
                string data_rece3 = server1.Server();
                


                System.Threading.Thread.Sleep(3000);
                AutomationElement HDCP_Transmitters = SelectElementNameControlType("HDCP Tests (for Transmitters)", ControlType.TabItem);
                SelectionItem(HDCP_Transmitters);
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                System.Windows.Forms.SendKeys.SendWait("{TAB 6}");

                if (i == 0)
                {
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 1}");
                    
                }

                System.Windows.Forms.SendKeys.SendWait("{TAB}");
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                
                while (true)
                {
                    System.Threading.Thread.Sleep(1000);

                 
                    AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                    if (Testcommpleted != null)
                    {
                        Invoke(Testcommpleted);
                        break;
                    }



                }


            }

          
        
        
        }
    
        private void DPR100_HDCP_1A_02()
        {

            int count = Int32.Parse(textBox2_Iteration.Text);
            for (int i = 0; i < count; i++)
            {

                Network_Check(); // Network Check before sending data 
                // Data send to server

                string client_data1 = "800x600@60MDS8BPC";
                Client.Class1 Client2 = new Client.Class1();
                Client2.Client(textBox1.Text, client_data1);

                // Data reciveve 

                
                SERVER.Class1 server2 = new SERVER.Class1();
                string data_rece1 = server2.Server();
               



                Network_Check(); // Network Check before sending data 
                // Data send to server

                string client_data = "ENABLE_HDCP";
                Client.Class1 Client1 = new Client.Class1();
                Client1.Client(textBox1.Text, client_data);

                //// Data reciveve 

                
                SERVER.Class1 server1 = new SERVER.Class1();
                string data_rece3 = server1.Server();
                




                System.Threading.Thread.Sleep(3000);
                AutomationElement HDCP_Transmitters = SelectElementNameControlType("HDCP Tests (for Transmitters)", ControlType.TabItem);
                SelectionItem(HDCP_Transmitters);
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                System.Windows.Forms.SendKeys.SendWait("{TAB 6}");

                if (i == 0)
                {
                    System.Windows.Forms.SendKeys.SendWait("{UP 20}");
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 1}");

                }

                System.Windows.Forms.SendKeys.SendWait("{TAB}");
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");

                while (true)
                {
                    System.Threading.Thread.Sleep(1000);


                    AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                    if (Testcommpleted != null)
                    {
                        Invoke(Testcommpleted);
                        break;
                    }



                }


            }




        }

        private void DPR100_HDCP_1A_03()
        {

            int count = Int32.Parse(textBox2_Iteration.Text);
            for (int i = 0; i < count; i++)
            {
                Network_Check(); // Network Check before sending data 
                // Data send to server

                string client_data1 = "800x600@60MDS8BPC";
                Client.Class1 Client2 = new Client.Class1();
                Client2.Client(textBox1.Text, client_data1);

                // Data reciveve 

                
                SERVER.Class1 server2 = new SERVER.Class1();
                string data_rece1 = server2.Server();
                




                Network_Check(); // Network Check before sending data 
                // Data send to server

                string client_data = "ENABLE_HDCP";
                Client.Class1 Client1 = new Client.Class1();
                Client1.Client(textBox1.Text, client_data);

                //// Data reciveve 

                
                SERVER.Class1 server1 = new SERVER.Class1();
                string data_rece3 = server1.Server();
                


                System.Threading.Thread.Sleep(3000);
                AutomationElement HDCP_Transmitters = SelectElementNameControlType("HDCP Tests (for Transmitters)", ControlType.TabItem);
                SelectionItem(HDCP_Transmitters);
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                System.Windows.Forms.SendKeys.SendWait("{TAB 6}");

                if (i == 0)
                {
                    System.Windows.Forms.SendKeys.SendWait("{UP 20}");
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 2}");

                }

                System.Windows.Forms.SendKeys.SendWait("{TAB}");
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");

                while (true)
                {
                    System.Threading.Thread.Sleep(1000);


                    AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                    if (Testcommpleted != null)
                    {
                        Invoke(Testcommpleted);
                        break;
                    }



                }


            }




        }

        private void DPR100_HDCP_1A_04()
        {

            int count = Int32.Parse(textBox2_Iteration.Text);
            for (int i = 0; i < count; i++)
            {

                Network_Check(); // Network Check before sending data 
                // Data send to server

                string client_data1 = "800x600@60MDS8BPC";
                Client.Class1 Client2 = new Client.Class1();
                Client2.Client(textBox1.Text, client_data1);

                // Data reciveve 

                
                SERVER.Class1 server2 = new SERVER.Class1();
                string data_rece1 = server2.Server();
                




                Network_Check(); // Network Check before sending data 
                // Data send to server

                string client_data = "ENABLE_HDCP";
                Client.Class1 Client1 = new Client.Class1();
                Client1.Client(textBox1.Text, client_data);

                //// Data reciveve 

                
                SERVER.Class1 server1 = new SERVER.Class1();
                string data_rece3 = server1.Server();
                
                System.Threading.Thread.Sleep(3000);
                AutomationElement HDCP_Transmitters = SelectElementNameControlType("HDCP Tests (for Transmitters)", ControlType.TabItem);
                SelectionItem(HDCP_Transmitters);
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                System.Windows.Forms.SendKeys.SendWait("{TAB 6}");

                if (i == 0)
                {
                    System.Windows.Forms.SendKeys.SendWait("{UP 20}");
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 3}");

                }

                System.Windows.Forms.SendKeys.SendWait("{TAB}");
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");

                while (true)
                {
                    System.Threading.Thread.Sleep(1000);


                    AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                    if (Testcommpleted != null)
                    {
                        Invoke(Testcommpleted);
                        break;
                    }



                }


            }




        }

        private void DPR100_HDCP_1A_05()
        {

            int count = Int32.Parse(textBox2_Iteration.Text);
            for (int i = 0; i < count; i++)
            {

                Network_Check(); // Network Check before sending data 
                // Data send to server

                string client_data1 = "800x600@60MDS8BPC";
                Client.Class1 Client2 = new Client.Class1();
                Client2.Client(textBox1.Text, client_data1);

                // Data reciveve 

                
                SERVER.Class1 server2 = new SERVER.Class1();
                string data_rece1 = server2.Server();
                




                Network_Check(); // Network Check before sending data 
                // Data send to server

                string client_data = "ENABLE_HDCP";
                Client.Class1 Client1 = new Client.Class1();
                Client1.Client(textBox1.Text, client_data);

                //// Data reciveve 

                
                SERVER.Class1 server1 = new SERVER.Class1();
                string data_rece3 = server1.Server();
                


                System.Threading.Thread.Sleep(3000);
                AutomationElement HDCP_Transmitters = SelectElementNameControlType("HDCP Tests (for Transmitters)", ControlType.TabItem);
                SelectionItem(HDCP_Transmitters);
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                System.Windows.Forms.SendKeys.SendWait("{TAB 6}");

                if (i == 0)
                {
                    System.Windows.Forms.SendKeys.SendWait("{UP 20}");
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 4}");

                }

                System.Windows.Forms.SendKeys.SendWait("{TAB}");
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");

                while (true)
                {
                    System.Threading.Thread.Sleep(1000);


                    AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                    if (Testcommpleted != null)
                    {
                        Invoke(Testcommpleted);
                        break;
                    }



                }


            }




        }

        private void DPR100_HDCP_1A_06()
        {

            int count = Int32.Parse(textBox2_Iteration.Text);
            for (int i = 0; i < count; i++)
            {

                Network_Check(); // Network Check before sending data 
                // Data send to server

                string client_data1 = "800x600@60MDS8BPC";
                Client.Class1 Client2 = new Client.Class1();
                Client2.Client(textBox1.Text, client_data1);

                // Data reciveve 

                
                SERVER.Class1 server2 = new SERVER.Class1();
                string data_rece1 = server2.Server();
                





                // Data send to server

                string client_data = "ENABLE_HDCP";
                Client.Class1 Client1 = new Client.Class1();
                Client1.Client(textBox1.Text, client_data);

                //// Data reciveve 

                
                SERVER.Class1 server1 = new SERVER.Class1();
                string data_rece3 = server1.Server();
                


                System.Threading.Thread.Sleep(3000);
                AutomationElement HDCP_Transmitters = SelectElementNameControlType("HDCP Tests (for Transmitters)", ControlType.TabItem);
                SelectionItem(HDCP_Transmitters);
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                System.Windows.Forms.SendKeys.SendWait("{TAB 6}");

                if (i == 0)
                {
                    System.Windows.Forms.SendKeys.SendWait("{UP 20}");
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 5}");

                }

                System.Windows.Forms.SendKeys.SendWait("{TAB}");
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");

                while (true)
                {
                    System.Threading.Thread.Sleep(1000);


                    AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                    if (Testcommpleted != null)
                    {
                        Invoke(Testcommpleted);
                        break;
                    }



                }


            }




        }

        private void DPR100_HDCP_1A_07()
        {

            int count = Int32.Parse(textBox2_Iteration.Text);
            for (int i = 0; i < count; i++)
            {
                Network_Check(); // Network Check before sending data 
                // Data send to server

                string client_data1 = "800x600@60MDS8BPC";
                Client.Class1 Client2 = new Client.Class1();
                Client2.Client(textBox1.Text, client_data1);

                // Data reciveve 

                
                SERVER.Class1 server2 = new SERVER.Class1();
                string data_rece1 = server2.Server();
                



                Network_Check(); // Network Check before sending data 

                // Data send to server

                string client_data = "ENABLE_HDCP";
                Client.Class1 Client1 = new Client.Class1();
                Client1.Client(textBox1.Text, client_data);

                //// Data reciveve 

                
                SERVER.Class1 server1 = new SERVER.Class1();
                string data_rece3 = server1.Server();
                


                System.Threading.Thread.Sleep(3000);
                AutomationElement HDCP_Transmitters = SelectElementNameControlType("HDCP Tests (for Transmitters)", ControlType.TabItem);
                SelectionItem(HDCP_Transmitters);
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                System.Windows.Forms.SendKeys.SendWait("{TAB 6}");

                if (i == 0)
                {
                    System.Windows.Forms.SendKeys.SendWait("{UP 20}");
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 6}");

                }

                System.Windows.Forms.SendKeys.SendWait("{TAB}");
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");

                while (true)
                {
                    System.Threading.Thread.Sleep(1000);


                    AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                    if (Testcommpleted != null)
                    {
                        Invoke(Testcommpleted);
                        break;
                    }



                }


            }




        }

        private void DPR100_HDCP_1B_01()
        {

            int count = Int32.Parse(textBox2_Iteration.Text);
            for (int i = 0; i < count; i++)
            {

                Network_Check(); // Network Check before sending data 
                // Data send to server

                string client_data1 = "800x600@60MDS8BPC";
                Client.Class1 Client2 = new Client.Class1();
                Client2.Client(textBox1.Text, client_data1);

                // Data reciveve 

                
                SERVER.Class1 server2 = new SERVER.Class1();
                string data_rece1 = server2.Server();
                


                Network_Check(); // Network Check before sending data 

                // Data send to server

                string client_data = "ENABLE_HDCP";
                Client.Class1 Client1 = new Client.Class1();
                Client1.Client(textBox1.Text, client_data);

                //// Data reciveve 

                
                SERVER.Class1 server1 = new SERVER.Class1();
                string data_rece3 = server1.Server();
                


                System.Threading.Thread.Sleep(3000);
                AutomationElement HDCP_Transmitters = SelectElementNameControlType("HDCP Tests (for Transmitters)", ControlType.TabItem);
                SelectionItem(HDCP_Transmitters);
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                System.Windows.Forms.SendKeys.SendWait("{TAB 6}");

                if (i == 0)
                {
                    System.Windows.Forms.SendKeys.SendWait("{UP 20}");
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 9}");

                }

                System.Windows.Forms.SendKeys.SendWait("{TAB}");
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");

                while (true)
                {
                    System.Threading.Thread.Sleep(1000);


                    AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                    if (Testcommpleted != null)
                    {
                        Invoke(Testcommpleted);
                        break;
                    }



                }


            }




        }

        private void DPR100_HDCP_1B_02()
        {

            int count = Int32.Parse(textBox2_Iteration.Text);
            for (int i = 0; i < count; i++)
            {

                Network_Check(); // Network Check before sending data 
                // Data send to server

                string client_data1 = "800x600@60MDS8BPC";
                Client.Class1 Client2 = new Client.Class1();
                Client2.Client(textBox1.Text, client_data1);

                // Data reciveve 

                
                SERVER.Class1 server2 = new SERVER.Class1();
                string data_rece1 = server2.Server();
                




                Network_Check(); // Network Check before sending data 
                // Data send to server

                string client_data = "ENABLE_HDCP";
                Client.Class1 Client1 = new Client.Class1();
                Client1.Client(textBox1.Text, client_data);

                //// Data reciveve 

                
                SERVER.Class1 server1 = new SERVER.Class1();
                string data_rece3 = server1.Server();
                

                System.Threading.Thread.Sleep(3000);
                AutomationElement HDCP_Transmitters = SelectElementNameControlType("HDCP Tests (for Transmitters)", ControlType.TabItem);
                SelectionItem(HDCP_Transmitters);
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                System.Windows.Forms.SendKeys.SendWait("{TAB 6}");

                if (i == 0)
                {
                    System.Windows.Forms.SendKeys.SendWait("{UP 20}");
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 10}");

                }

                System.Windows.Forms.SendKeys.SendWait("{TAB}");
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");

                while (true)
                {
                    System.Threading.Thread.Sleep(1000);


                    AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                    if (Testcommpleted != null)
                    {
                        Invoke(Testcommpleted);
                        break;
                    }



                }


            }




        }

        private void DPR100_HDCP_1B_03()
        {

            int count = Int32.Parse(textBox2_Iteration.Text);
            for (int i = 0; i < count; i++)
            {

                Network_Check(); // Network Check before sending data 
                // Data send to server

                string client_data1 = "800x600@60MDS8BPC";
                Client.Class1 Client2 = new Client.Class1();
                Client2.Client(textBox1.Text, client_data1);

                // Data reciveve 

                
                SERVER.Class1 server2 = new SERVER.Class1();
                string data_rece1 = server2.Server();
                




                Network_Check(); // Network Check before sending data 
                // Data send to server

                string client_data = "ENABLE_HDCP";
                Client.Class1 Client1 = new Client.Class1();
                Client1.Client(textBox1.Text, client_data);

                //// Data reciveve 

                
                SERVER.Class1 server1 = new SERVER.Class1();
                string data_rece3 = server1.Server();
                

                System.Threading.Thread.Sleep(3000);
                AutomationElement HDCP_Transmitters = SelectElementNameControlType("HDCP Tests (for Transmitters)", ControlType.TabItem);
                SelectionItem(HDCP_Transmitters);
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                System.Windows.Forms.SendKeys.SendWait("{TAB 6}");

                if (i == 0)
                {
                    System.Windows.Forms.SendKeys.SendWait("{UP 20}");
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 11}");

                }

                System.Windows.Forms.SendKeys.SendWait("{TAB}");
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");

                while (true)
                {
                    System.Threading.Thread.Sleep(1000);


                    AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                    if (Testcommpleted != null)
                    {
                        Invoke(Testcommpleted);
                        break;
                    }



                }


            }




        }

        private void DPR100_HDCP_1B_04()
        {

            int count = Int32.Parse(textBox2_Iteration.Text);
            for (int i = 0; i < count; i++)
            {

                Network_Check(); // Network Check before sending data 
                // Data send to server

                string client_data1 = "800x600@60MDS8BPC";
                Client.Class1 Client2 = new Client.Class1();
                Client2.Client(textBox1.Text, client_data1);

                // Data reciveve 

               
                SERVER.Class1 server2 = new SERVER.Class1();
                string data_rece1 = server2.Server();
                




                Network_Check(); // Network Check before sending data 
                // Data send to server

                string client_data = "ENABLE_HDCP";
                Client.Class1 Client1 = new Client.Class1();
                Client1.Client(textBox1.Text, client_data);

                //// Data reciveve 

                
                SERVER.Class1 server1 = new SERVER.Class1();
                string data_rece3 = server1.Server();
                


                System.Threading.Thread.Sleep(3000);
                AutomationElement HDCP_Transmitters = SelectElementNameControlType("HDCP Tests (for Transmitters)", ControlType.TabItem);
                SelectionItem(HDCP_Transmitters);
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                System.Windows.Forms.SendKeys.SendWait("{TAB 6}");

                if (i == 0)
                {
                    System.Windows.Forms.SendKeys.SendWait("{UP 20}");
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 12}");

                }

                System.Windows.Forms.SendKeys.SendWait("{TAB}");
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");

                while (true)
                {
                    System.Threading.Thread.Sleep(1000);


                    AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                    if (Testcommpleted != null)
                    {
                        Invoke(Testcommpleted);
                        break;
                    }



                }


            }




        }

        private void DPR100_HDCP_1B_05()
        {

            int count = Int32.Parse(textBox2_Iteration.Text);
            for (int i = 0; i < count; i++)
            {

                Network_Check(); // Network Check before sending data 
                // Data send to server

                string client_data1 = "800x600@60MDS8BPC";
                Client.Class1 Client2 = new Client.Class1();
                Client2.Client(textBox1.Text, client_data1);

                // Data reciveve 

                
                SERVER.Class1 server2 = new SERVER.Class1();
                string data_rece1 = server2.Server();
                




                Network_Check(); // Network Check before sending data 
                // Data send to server

                string client_data = "ENABLE_HDCP";
                Client.Class1 Client1 = new Client.Class1();
                Client1.Client(textBox1.Text, client_data);

                //// Data reciveve 

               
                SERVER.Class1 server1 = new SERVER.Class1();
                string data_rece3 = server1.Server();
                

                System.Threading.Thread.Sleep(3000);
                AutomationElement HDCP_Transmitters = SelectElementNameControlType("HDCP Tests (for Transmitters)", ControlType.TabItem);
                SelectionItem(HDCP_Transmitters);
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                System.Windows.Forms.SendKeys.SendWait("{TAB 6}");

                if (i == 0)
                {
                    System.Windows.Forms.SendKeys.SendWait("{UP 20}");
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 13}");

                }

                System.Windows.Forms.SendKeys.SendWait("{TAB}");
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");

                while (true)
                {
                    System.Threading.Thread.Sleep(1000);


                    AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                    if (Testcommpleted != null)
                    {
                        Invoke(Testcommpleted);
                        break;
                    }



                }


            }




        }

        private void DPR100_HDCP_1B_06()
        {

            int count = Int32.Parse(textBox2_Iteration.Text);
            for (int i = 0; i < count; i++)
            {

                Network_Check(); // Network Check before sending data 
                // Data send to server

                string client_data1 = "800x600@60MDS8BPC";
                Client.Class1 Client2 = new Client.Class1();
                Client2.Client(textBox1.Text, client_data1);

                // Data reciveve 

                
                SERVER.Class1 server2 = new SERVER.Class1();
                string data_rece1 = server2.Server();
                




                Network_Check(); // Network Check before sending data 
                // Data send to server

                string client_data = "ENABLE_HDCP";
                Client.Class1 Client1 = new Client.Class1();
                Client1.Client(textBox1.Text, client_data);

                //// Data reciveve 

                
                SERVER.Class1 server1 = new SERVER.Class1();
                string data_rece3 = server1.Server();
                


                System.Threading.Thread.Sleep(3000);
                AutomationElement HDCP_Transmitters = SelectElementNameControlType("HDCP Tests (for Transmitters)", ControlType.TabItem);
                SelectionItem(HDCP_Transmitters);
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                System.Windows.Forms.SendKeys.SendWait("{TAB 6}");

                if (i == 0)
                {
                    System.Windows.Forms.SendKeys.SendWait("{UP 20}");
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 14}");

                }

                System.Windows.Forms.SendKeys.SendWait("{TAB}");
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");

                while (true)
                {
                    System.Threading.Thread.Sleep(1000);


                    AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                    if (Testcommpleted != null)
                    {
                        Invoke(Testcommpleted);
                        break;
                    }



                }


            }




        }

        private void DPR100_HDCP_1B_07()
        {

            int count = Int32.Parse(textBox2_Iteration.Text);
            for (int i = 0; i < count; i++)
            {

                Network_Check(); // Network Check before sending data 
                // Data send to server

                string client_data1 = "800x600@60MDS8BPC";
                Client.Class1 Client2 = new Client.Class1();
                Client2.Client(textBox1.Text, client_data1);

                // Data reciveve 

                
                SERVER.Class1 server2 = new SERVER.Class1();
                string data_rece1 = server2.Server();
                




                Network_Check(); // Network Check before sending data 
                // Data send to server

                string client_data = "ENABLE_HDCP";
                Client.Class1 Client1 = new Client.Class1();
                Client1.Client(textBox1.Text, client_data);

                //// Data reciveve 

                
                SERVER.Class1 server1 = new SERVER.Class1();
                string data_rece3 = server1.Server();
                


                System.Threading.Thread.Sleep(3000);
                AutomationElement HDCP_Transmitters = SelectElementNameControlType("HDCP Tests (for Transmitters)", ControlType.TabItem);
                SelectionItem(HDCP_Transmitters);
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                System.Windows.Forms.SendKeys.SendWait("{TAB 6}");

                if (i == 0)
                {
                    System.Windows.Forms.SendKeys.SendWait("{UP 20}");
                    System.Windows.Forms.SendKeys.SendWait("{DOWN 15}");

                }

                System.Windows.Forms.SendKeys.SendWait("{TAB}");
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");

                while (true)
                {
                    System.Threading.Thread.Sleep(1000);


                    AutomationElement Testcommpleted = SelectElementNameControlType("OK", ControlType.Button);
                    if (Testcommpleted != null)
                    {
                        Invoke(Testcommpleted);
                        break;
                    }



                }


            }




        }



// Inovoke Functions for Buttons 



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
                InvokePattern  pattern = element.GetCurrentPattern(InvokePattern.Pattern) as InvokePattern;
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

        private void DPR100_HDCP_CheckedChanged(object sender, EventArgs e)
        {
            MessageBox.Show(" HDCP");
        }

        private void AUDIO_Click(object sender, EventArgs e)
        {

        }

        private void HDCP_Click(object sender, EventArgs e)
        {
           
        }



        private void DPR120_LINK_CheckedChanged(object sender, EventArgs e)
        {

            if (DPR120_LINK.Checked == true)
            {

                
                    DPR100_LINK.Checked = false;
                    DPR100_AUDIO.Checked = false;
                    DPR100_HDCP.Checked = false;
                    DPR120_Applet.Checked = false;
                    DPR100_Applet.Checked = false;
                    START.Enabled = true;


            }
            else START.Enabled = false;

            }

        private void DPR100_LINK_CheckedChanged(object sender, EventArgs e)
        {
            if(DPR100_LINK.Checked == true)
            {
            DPR120_LINK.Checked= false;
            DPR120_Applet.Checked = false;

            START.Enabled = true;
            
            }

            if (DPR100_LINK.Checked == false)
            {
                if (DPR100_AUDIO.Checked == true || DPR100_HDCP.Checked == true)
                {
                    START.Enabled = true;
                }
                else START.Enabled = false;

            }

            
        }

        private void DPR100_AUDIO_CheckedChanged(object sender, EventArgs e)
        {
            if(DPR100_AUDIO.Checked == true)
            {
            DPR120_LINK.Checked= false;
            DPR120_Applet.Checked = false;
            START.Enabled = true;
            }
            if (DPR100_AUDIO.Checked == false)
            {
                if (DPR100_HDCP.Checked == true || DPR100_LINK.Checked == true)
                {
                    START.Enabled = true;
                }
                else START.Enabled = false;

            }

            
        }

        private void DPR100_HDCP_CheckedChanged_1(object sender, EventArgs e)
        {
        
            if(DPR100_HDCP.Checked == true)
            {
            DPR120_LINK.Checked= false;
            DPR120_Applet.Checked = false;
            DPR100_Applet.Checked = false;
            START.Enabled = true;


            }
            if (DPR100_HDCP.Checked == false)
            {
                if (DPR100_AUDIO.Checked == true || DPR100_LINK.Checked == true)
                {
                    START.Enabled = true;
                }
                else START.Enabled = false;
            
            }

           
            
        }

        private void DPR100_Applet_CheckedChanged(object sender, EventArgs e)
        {
            if (DPR100_Applet.Checked == true)
            {
                DPR120_LINK.Checked = false;
                DPR100_LINK.Checked = false;
                DPR100_AUDIO.Checked = false;
                DPR100_HDCP.Checked = false;
                DPR120_Applet.Checked = false;
                START.Enabled = true;
            }
            else START.Enabled = false;

        }

        private void DPR120_Applet_CheckedChanged(object sender, EventArgs e)
        {
            if (DPR120_Applet.Checked == true)
            {
                DPR120_LINK.Checked = false;
                DPR100_LINK.Checked = false;
                DPR100_AUDIO.Checked = false;
                DPR100_HDCP.Checked = false;
                DPR100_Applet.Checked = false;
                START.Enabled = true;
            }

            else START.Enabled = false;
        }



        public void Network_Check()
        {

            int Waittime = 0;
            while (Waittime <=10)
            {
                Ping ping = new Ping();
                PingReply pingresults = ping.Send(textBox1.Text);
                if (pingresults.Status.ToString() == "Success")
                {
                    //MessageBox.Show("Success");
                    break; // Come out of While Loop

                }
                else
                {
                    if (Waittime == 10)
                    {

                        MessageBox.Show(" Network failure or System is Crash ..!!! ,please Check and Click OK once System is up");
                    }
                    System.Threading.Thread.Sleep(10000);
                    Waittime++;
                }

            }
        
        
        }

        private void BDW_CheckedChanged(object sender, EventArgs e)
        {
            if(BDW.Checked == true)
            {
                SKL.Checked = false;
            }

          
        }
        
        private void SKL_CheckedChanged(object sender, EventArgs e)
        {
            if(SKL.Checked == true)
            {
                BDW.Checked = false;

            }
        }

        private void checkBox2_CheckedChanged(object sender, EventArgs e)
        {
            DP_PORT_B.Checked = false;
            DP_PORT_D.Checked = false;
            START.Enabled = true;
        }

        private void checkBox3_CheckedChanged(object sender, EventArgs e)
        {
            DP_PORT_C.Checked = false;
            DP_PORT_B.Checked = false;
            START.Enabled = true;
        }

        private void DP_PORT_B_CheckedChanged(object sender, EventArgs e)
        {
            DP_PORT_C.Checked = false;
            DP_PORT_D.Checked = false;
            START.Enabled = true;
        }

      

       

    }
}
