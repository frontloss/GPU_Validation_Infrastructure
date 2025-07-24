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



namespace HDMI_Compliance_QD980_new
{
    public partial class Form1 : Form
    {
         static int count_value = 0;
         static int error_count = 0;

        public Form1()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {

            QD_App_close();
            QD_App_close();

            START_Button.Enabled = false;
            Version.Enabled = false;

            SERVER_ADDRESS.Text = GetLocalIP();

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

        // To START the Automation Tool

        private void START_Button_Click_1(object sender, EventArgs e)
        {
            if (checkBox1.Checked == true || checkBox2.Checked == true)
            {
                if (checkBox7.Checked == true)//OLD QD APP
                {
                    try
                    {
                        Process myProcess = new Process();
                        myProcess.StartInfo.WorkingDirectory = @"C:\Program Files (x86)\Quantum Data\980 Manager 4.16.39\980mgr";
                        myProcess.StartInfo.FileName = "980mgr.exe";
                        myProcess.StartInfo.Verb = "runas";
                        myProcess.Start();
                    }
                    catch
                    {
                        MessageBox.Show("Please Install the QD 980b Version Correctly");
                        Close();

                        Process myProcess = new Process();
                        foreach (var process in Process.GetProcessesByName("HDMI Compliance_QD980_new"))
                        {
                            process.Kill();

                        }
                    }
                    System.Threading.Thread.Sleep(8000);
                }

                else if (checkBox8.Checked == true)//New QD APP
                {
                    Process myProcess = new Process();
                    myProcess.StartInfo.WorkingDirectory = @"C:\Program Files (x86)\Quantum Data\980 Manager " + Version.Text + "\\980mgr";
                    myProcess.StartInfo.FileName = "980mgr.exe";
                    myProcess.StartInfo.Verb = "runas";
                    myProcess.Start();
                    System.Threading.Thread.Sleep(8000);
                }

                //Adding IP Address for connection
                AutomationElement menu_instrument_item = SelectElementNameControlType("Instrument", ControlType.MenuItem); ;
                ExpandCollapse(menu_instrument_item);
                AutomationElement add_click = SelectElementNameControlType("Add", ControlType.MenuItem);
                Invoke(add_click);
                System.Threading.Thread.Sleep(3000);
                System.Windows.Forms.SendKeys.SendWait("QD 980");
                System.Threading.Thread.Sleep(2000);
                System.Windows.Forms.SendKeys.SendWait("{TAB}");
                System.Threading.Thread.Sleep(1000);
                System.Windows.Forms.SendKeys.SendWait(IP_ADDRESS.Text);
                System.Threading.Thread.Sleep(2000);
                AutomationElement add_button = SelectElementNameControlType("Add", ControlType.Button);
                Invoke(add_button);
                System.Threading.Thread.Sleep(4000);

                ////Checking for Communication Failure
                AutomationElement comfail = SelectElementNameControlType("Communication Failure\r\nconnect timed out", ControlType.Text);
                if (comfail != null)
                {
                    if (comfail.Current.IsOffscreen == false)
                    {
                        foreach (var process in Process.GetProcessesByName("980mgr"))
                        {
                            process.Kill();
                            MessageBox.Show("NETWORK CONNECTION PROBLEM: PLEASE CHECK THE CONNECTION BETWEEN CONTROL SYSTEM AND HDMI ANALYZER");
                        }
                    }
                }
                else
                {
                    AutomationElement ae_Tab_Compliance = SelectElementNameControlType("Compliance", ControlType.TabItem);
                    SelectionItem(ae_Tab_Compliance);
                    System.Threading.Thread.Sleep(1000);

                    //For HDMI 1.4b 5 frames 

                    AutomationElement ae_Source = SelectElementNameControlType("HDMI 1.4b Source", ControlType.TreeItem);
                    ExpandCollapse(ae_Source);

                    System.Threading.Thread.Sleep(3000);
                    AutomationElement cdf_Source = SelectElementNameControlType("CDF", ControlType.TreeItem);
                    ExpandCollapse(cdf_Source);
                    System.Threading.Thread.Sleep(1000);

                    if (checkBox1.Checked == true)
                    {
                        //Load Hdmi 1.4 5f cdf
                        AutomationElement hdmi_1_4b_5f_source_treeitem = SelectElementNameControlType("HDMI_1.4_5F", ControlType.TreeItem);
                        SelectionItem(hdmi_1_4b_5f_source_treeitem);
                        System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                        System.Threading.Thread.Sleep(3000);
                        //Load Hdmi 1.4 5f tests
                        AutomationElement tab_firstElem1 = SelectElementNameControlType("Test Selection", ControlType.TabItem); ;
                        SelectionItem(tab_firstElem1);
                        System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                        System.Threading.Thread.Sleep(3000);
                        System.Windows.Forms.SendKeys.SendWait("{TAB}");
                        System.Threading.Thread.Sleep(1000);
                        System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                        System.Threading.Thread.Sleep(2000);
                        //Select Tests xml files through keyboard Event
                        System.Windows.Forms.SendKeys.SendWait("{DOWN}");
                        System.Threading.Thread.Sleep(1000);
                        System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                        System.Threading.Thread.Sleep(1000);

                    }

                    else if (checkBox2.Checked == true)
                    {
                        //Load Hdmi 1.4 120f cdf
                        AutomationElement hdmi_1_4b_120f_source_treeitem = SelectElementNameControlType("HDMI_1.4_120F", ControlType.TreeItem);
                        SelectionItem(hdmi_1_4b_120f_source_treeitem);
                        System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                        System.Threading.Thread.Sleep(3000);
                        //Load Hdmi 1.4 120f tests
                        AutomationElement tab_firstElem1 = SelectElementNameControlType("Test Selection", ControlType.TabItem); ;
                        SelectionItem(tab_firstElem1);
                        System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                        System.Threading.Thread.Sleep(3000);
                        System.Windows.Forms.SendKeys.SendWait("{TAB}");
                        System.Threading.Thread.Sleep(1000);
                        System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                        System.Threading.Thread.Sleep(1000);
                        //Select test.xml file through keyboard event
                        System.Windows.Forms.SendKeys.SendWait("{DOWN}");
                        System.Threading.Thread.Sleep(1000);
                        System.Windows.Forms.SendKeys.SendWait("{UP}");
                        System.Threading.Thread.Sleep(1000);
                        System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                        System.Threading.Thread.Sleep(1000);
                    }

                    AutomationElement tab_thirdElem = SelectElementNameControlType("Test Options / Preview", ControlType.TabItem); ;
                    SelectionItem(tab_thirdElem);
                    System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                    System.Threading.Thread.Sleep(1000);

                    //Selecting 5 frames or 120 frames through keyboard event
                    AutomationElement all_button = SelectElementNameControlType("All", ControlType.Button);
                    Invoke(all_button);
                    System.Threading.Thread.Sleep(1000);
                    AutomationElement Duration_button = SelectElementNameControlType("Duration", ControlType.Button);
                    Invoke(Duration_button);
                    System.Threading.Thread.Sleep(2000);
                    System.Windows.Forms.SendKeys.SendWait("{TAB}");
                    System.Threading.Thread.Sleep(1000);
                    System.Windows.Forms.SendKeys.SendWait("{DOWN}");
                    System.Threading.Thread.Sleep(1000);
                    System.Windows.Forms.SendKeys.SendWait("{TAB}");
                    System.Threading.Thread.Sleep(1000);
                    System.Windows.Forms.SendKeys.SendWait("{DOWN}");
                    System.Threading.Thread.Sleep(1000);
                    System.Threading.Thread.Sleep(1000);

                    if (checkBox1.Checked == true)
                    {//Select 5 frames
                        System.Windows.Forms.SendKeys.SendWait("5");
                        System.Threading.Thread.Sleep(1000);
                        AutomationElement ok_button = SelectElementNameControlType("OK", ControlType.Button);
                        Invoke(ok_button);

                        System.Threading.Thread.Sleep(3000);

                        int i;

                        for (i = 0; i < 90; i++)
                        {
                            AutomationElement scroll_down_button = SelectElementNameControlType("Forward by small amount", ControlType.Button);
                            if (scroll_down_button != null)
                            {
                                Invoke(scroll_down_button);
                            }
                        }

                        AutomationElement test_7_32_120f = SelectElementNameControlType("7-29: ACR", ControlType.TreeItem);

                        if (test_7_32_120f != null)
                        {
                            test_7_32_120f.SetFocus();

                            System.Threading.Thread.Sleep(1000);
                            Duration_button = SelectElementNameControlType("Duration", ControlType.Button);
                            Invoke(Duration_button);

                            System.Threading.Thread.Sleep(1000);
                            System.Windows.Forms.SendKeys.SendWait("120");
                            System.Threading.Thread.Sleep(1000);
                            System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                            System.Threading.Thread.Sleep(1000);
                        }
                        ok_button = SelectElementNameControlType("OK", ControlType.Button);
                        if (ok_button != null)
                        {
                            Invoke(ok_button);
                        }


                    }

                    if (checkBox2.Checked == true)
                    {//Select 120 Frame
                        System.Windows.Forms.SendKeys.SendWait("120");
                        System.Threading.Thread.Sleep(1000);

                        AutomationElement ok_button = SelectElementNameControlType("OK", ControlType.Button);
                        Invoke(ok_button);
                    }



                    System.Threading.Thread.Sleep(4000);
                    //Old QD and New Qd Control Type little bit different
                    if (checkBox7.Checked == true)
                    {//For Old QD
                        AutomationElement execute_test_button = SelectElementNameControlType("Execute Tests", ControlType.Button);
                        Invoke(execute_test_button);
                    }

                    if (checkBox8.Checked == true)
                    {//For New QD
                        AutomationElement execute_test_button = SelectElementNameControlType("Execute Tests     ", ControlType.Button);
                        Invoke(execute_test_button);
                    }
                    System.Threading.Thread.Sleep(8000);
                    //Give name for the log files
                    System.Windows.Forms.SendKeys.SendWait(Platform.Text + "_" + DriverVersion.Text + "_" + DateTime.Now.ToString("dd.MM.yyyy.hh.mm.ss"));
                    System.Threading.Thread.Sleep(4000);
                    System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                    System.Threading.Thread.Sleep(8000);
                    //Press Continue Button
                    AutomationElement continue_test_button = SelectElementNameControlType("Continue   ", ControlType.Button);
                    Invoke(continue_test_button);
                    System.Threading.Thread.Sleep(20000);

                    //Logic: Search for close_test button to appear on the screen, if it appears means tests are completed.
                    //Until that, handle all pop ups that will come
                    AutomationElement close_test = SelectElementNameControlType("Close Window", ControlType.Button);
                    while (close_test == null)
                    {
                        System.Threading.Thread.Sleep(2000);

                        req_dut_config_handler();//required DUT Config pop up where all tests are handled

                        dut_config_err_handler();//If there is any error in dut configuration, this pop up will appear and this is handled in this function.

                        test_error_handler();//If there is any error in dut configuration, this pop up will appear some times and this is handled in this function.

                        manual_pass_fail_handler();//This pop up will appear asking to manually pass or fail the test cases such as 7-23,7-24,7-39

                        audio_handler();//This pop up handler will handle a pop up asking for selecting 2 channel or 8 channel audio.

                        close_test = SelectElementNameControlType("Close Window", ControlType.Button);//Continuosly Check close test butto will appear.
                    }
                    //If close test button appears close the application
                    if (close_test != null)
                    {
                        if (close_test.Current.IsOffscreen == false)
                        {
                            close_test_handler();
                        }
                    }
                }
            }

            /// Start HDMI 2.0
            else if (checkBox3.Checked == true || checkBox4.Checked == true)
            {
                if (checkBox8.Checked == true)//New QD APP
                {
                    Process myProcess = new Process();
                    myProcess.StartInfo.WorkingDirectory = @"C:\Program Files (x86)\Quantum Data\980 Manager " + Version.Text + "\\980mgr";
                    myProcess.StartInfo.FileName = "980mgr.exe";
                    myProcess.StartInfo.Verb = "runas";
                    myProcess.Start();
                    System.Threading.Thread.Sleep(8000);
                }

                //Adding IP Address for connection
                AutomationElement menu_instrument_item = SelectElementNameControlType("Instrument", ControlType.MenuItem); ;
                ExpandCollapse(menu_instrument_item);
                AutomationElement add_click = SelectElementNameControlType("Add", ControlType.MenuItem);
                Invoke(add_click);
                System.Threading.Thread.Sleep(3000);
                System.Windows.Forms.SendKeys.SendWait("QD 980");
                System.Threading.Thread.Sleep(2000);
                System.Windows.Forms.SendKeys.SendWait("{TAB}");
                System.Threading.Thread.Sleep(1000);
                System.Windows.Forms.SendKeys.SendWait(IP_ADDRESS.Text);
                System.Threading.Thread.Sleep(2000);
                AutomationElement add_button = SelectElementNameControlType("Add", ControlType.Button);
                Invoke(add_button);
                System.Threading.Thread.Sleep(4000);

                ////Checking for Communication Failure
                AutomationElement comfail = SelectElementNameControlType("Communication Failure\r\nconnect timed out", ControlType.Text);
                if (comfail != null)
                {
                    if (comfail.Current.IsOffscreen == false)
                    {
                        foreach (var process in Process.GetProcessesByName("980mgr"))
                        {
                            process.Kill();
                            MessageBox.Show("NETWORK CONNECTION PROBLEM: PLEASE CHECK THE CONNECTION BETWEEN CONTROL SYSTEM AND HDMI ANALYZER");
                        }
                    }
                }
                else
                {
                    AutomationElement ae_Tab_Compliance = SelectElementNameControlType("Compliance", ControlType.TabItem);
                    SelectionItem(ae_Tab_Compliance);
                    System.Threading.Thread.Sleep(1000);

                    AutomationElement ae_Source2 = SelectElementNameControlType("HDMI 2.0 Source", ControlType.TreeItem);
                    ExpandCollapse(ae_Source2);

                    System.Threading.Thread.Sleep(3000);
                    AutomationElement cdf_Source = SelectElementNameControlType("CDF", ControlType.TreeItem);
                    ExpandCollapse(cdf_Source);
                    System.Threading.Thread.Sleep(1000);

                    if (checkBox3.Checked == true)
                    {
                        //Load Hdmi 2.0 5f cdf
                        AutomationElement hdmi_2_0_5f_source_treeitem = SelectElementNameControlType("HDMI_2.0_5F", ControlType.TreeItem);
                        SelectionItem(hdmi_2_0_5f_source_treeitem);
                        System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                        System.Threading.Thread.Sleep(3000);
                        //Load Hdmi 1.4 5f tests
                        AutomationElement tab_firstElem1 = SelectElementNameControlType("Test Selection", ControlType.TabItem); ;
                        SelectionItem(tab_firstElem1);
                        System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                        System.Threading.Thread.Sleep(3000);
                        System.Windows.Forms.SendKeys.SendWait("{TAB}");
                        System.Threading.Thread.Sleep(1000);
                        System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                        System.Threading.Thread.Sleep(2000);
                        //Select Tests xml files through keyboard Event
                        System.Windows.Forms.SendKeys.SendWait("{DOWN}");
                        System.Threading.Thread.Sleep(1000);
                        System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                        System.Threading.Thread.Sleep(1000);
                    }

                    if(checkBox4.Checked == true)
                    {
                        ///////Load Hdmi 2.0  120f cdf
                        AutomationElement hdmi_2_0_120f_source_treeitem = SelectElementNameControlType("HDMI_2.0_120F", ControlType.TreeItem);
                        SelectionItem(hdmi_2_0_120f_source_treeitem);
                        System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                        System.Threading.Thread.Sleep(3000);
                        //Load Hdmi 1.4 120f tests
                        AutomationElement tab_firstElem1 = SelectElementNameControlType("Test Selection", ControlType.TabItem); ;
                        SelectionItem(tab_firstElem1);
                        System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                        System.Threading.Thread.Sleep(3000);
                        System.Windows.Forms.SendKeys.SendWait("{TAB}");
                        System.Threading.Thread.Sleep(1000);
                        System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                        System.Threading.Thread.Sleep(1000);
                        //Select test.xml file through keyboard event
                        System.Windows.Forms.SendKeys.SendWait("{DOWN}");
                        System.Threading.Thread.Sleep(1000);
                        System.Windows.Forms.SendKeys.SendWait("{UP}");
                        System.Threading.Thread.Sleep(1000);
                        System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                        System.Threading.Thread.Sleep(1000);

                    }

                    AutomationElement tab_thirdElem = SelectElementNameControlType("Test Options / Preview", ControlType.TabItem); ;
                    SelectionItem(tab_thirdElem);
                    System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                    System.Threading.Thread.Sleep(1000);

                    //Selecting 5 frames or 120 frames through keyboard event
                    AutomationElement all_button = SelectElementNameControlType("All", ControlType.Button);
                    Invoke(all_button);
                    System.Threading.Thread.Sleep(1000);
                    AutomationElement Duration_button = SelectElementNameControlType("Duration", ControlType.Button);
                    Invoke(Duration_button);
                    System.Threading.Thread.Sleep(2000);
                    System.Windows.Forms.SendKeys.SendWait("{TAB}");
                    System.Threading.Thread.Sleep(1000);
                    System.Windows.Forms.SendKeys.SendWait("{DOWN}");
                    System.Threading.Thread.Sleep(1000);
                    System.Windows.Forms.SendKeys.SendWait("{TAB}");
                    System.Threading.Thread.Sleep(1000);
                    System.Windows.Forms.SendKeys.SendWait("{DOWN}");
                    System.Threading.Thread.Sleep(1000);
                    System.Threading.Thread.Sleep(1000);

                    if (checkBox3.Checked == true)
                    {//Select 5 frames
                        System.Windows.Forms.SendKeys.SendWait("15");
                        System.Threading.Thread.Sleep(1000);
                        AutomationElement ok_button = SelectElementNameControlType("OK", ControlType.Button);
                        Invoke(ok_button);
                    }

                    if (checkBox4.Checked == true)
                    {//Select 120 Frame
                        System.Windows.Forms.SendKeys.SendWait("120");
                        System.Threading.Thread.Sleep(1000);

                        AutomationElement ok_button = SelectElementNameControlType("OK", ControlType.Button);
                        Invoke(ok_button);
                    }

                    AutomationElement execute_test_button = SelectElementNameControlType("Execute Tests     ", ControlType.Button);
                    Invoke(execute_test_button);
                    System.Threading.Thread.Sleep(8000);
                    //Give name for the log files
                    System.Windows.Forms.SendKeys.SendWait(Platform.Text + "_" + DriverVersion.Text + "_" + DateTime.Now.ToString("dd.MM.yyyy.hh.mm.ss"));
                    System.Threading.Thread.Sleep(4000);
                    System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                    System.Threading.Thread.Sleep(8000);
                    //Press Continue Button
                    AutomationElement continue_test_button = SelectElementNameControlType("Continue   ", ControlType.Button);
                    Invoke(continue_test_button);
                    System.Threading.Thread.Sleep(20000);

                    //Logic: Search for close_test button to appear on the screen, if it appears means tests are completed.
                    //Until that, handle all pop ups that will come
                    AutomationElement close_test = SelectElementNameControlType("Close Window", ControlType.Button);

                    while (close_test == null)
                    {
                        System.Threading.Thread.Sleep(1000);

                        required_dut_configuration_handler();

                        dut_config_err_handler();//If there is any error in dut configuration, this pop up will appear and this is handled in this function.

                        test_error_handler();//If there is any error in dut configuration, this pop up will appear some times and this is handled in this function.

                        pass_fail_handler();// Manually press pass button

                        System.Threading.Thread.Sleep(2000);

                        close_test = SelectElementNameControlType("Close Window", ControlType.Button);

                    }
                    //If close test button appears close the application
                    if (close_test != null)
                    {
                        if (close_test.Current.IsOffscreen == false)
                        {
                            close_test_handler();
                        }
                    }

                }
            }

        }

        void required_dut_configuration_handler()
        {
            AutomationElement dut_config = SelectElementNameControlType("DUT Configuration", ControlType.TitleBar);
            System.Threading.Thread.Sleep(1000);
            if (dut_config != null)
            {
                read_test();

                //After reading, press continue button
                AutomationElement continue_button = SelectElementNameControlType("Continue", ControlType.Button);

                if (continue_button != null)
                {
                    Invoke(continue_button);
                    System.Threading.Thread.Sleep(1000);
                    return;
                }

            }

        }

        private void read_test()
        {
            AutomationElement hf1_10_1 = SelectElementNameControlType("Test HF1-10, Iter-01\r\nConfirm that the Source changes the TMDS Bit Clock Ratio correctly according to the output signal.", ControlType.Text);
            if (hf1_10_1 != null)
            {
                send_resolution_to_clent("1024x768@60MDSCLONE");
                System.Threading.Thread.Sleep(2000);
                send_resolution_to_clent("4096x2160@60MDS8BPC");
                System.Threading.Thread.Sleep(4000);
                return;
            }

            AutomationElement hf1_10_2 = SelectElementNameControlType("Test HF1-10, Iter-02\r\nConfirm that the Source changes the TMDS Bit Clock Ratio correctly according to the output signal.", ControlType.Text);
            if (hf1_10_2 != null)
            {
                send_resolution_to_clent("1024x768@60MDSCLONE");
                System.Threading.Thread.Sleep(2000);
                send_resolution_to_clent("720x480@60MDS8BPC");
                System.Threading.Thread.Sleep(4000);
                return;

            }

            AutomationElement hf1_11_1 = SelectElementNameControlType("Test HF1-11, Iter-01\r\nConfirm that the Source only outputs legal 10-bit codes.", ControlType.Text);
            if (hf1_11_1 != null)
            {
                send_resolution_to_clent("1024x768@60MDSCLONE");
                System.Threading.Thread.Sleep(2000);
                send_resolution_to_clent("3840x2160@50MDS8BPC");
                System.Threading.Thread.Sleep(4000);
                return;
            }

            AutomationElement hf1_12_1 = SelectElementNameControlType("Test HF1-12, Iter-01\r\nConfirm that the Source only outputs code sequences for Control Periods, Data Island Periods\r\nand Video Data Periods corresponding to basic HDMI protocol rules.", ControlType.Text);
            if (hf1_12_1 != null)
            {
                send_resolution_to_clent("1024x768@60MDSCLONE");
                System.Threading.Thread.Sleep(2000);
                send_resolution_to_clent("3840x2160@50MDS8BPC");
                System.Threading.Thread.Sleep(4000);
                return;
            }


            AutomationElement hf1_14_1 = SelectElementNameControlType("Test HF1-14, Iter-01\r\nConfirm that the Source, whenever transmitting any 24-bit color depth 2160p Video Format with\r\na TMDS Character Rate greater than 340Mcsc, complies with all of the required Pixel and line counts.", ControlType.Text);
            if (hf1_14_1 != null)
            {
                send_resolution_to_clent("1024x768@60MDSCLONE");
                System.Threading.Thread.Sleep(2000);
                send_resolution_to_clent("3840x2160@50MDS8BPC");
                System.Threading.Thread.Sleep(4000);
                return;
            }

            AutomationElement hf1_14_2 = SelectElementNameControlType("Test HF1-14, Iter-02\r\nConfirm that the Source, whenever transmitting any 24-bit color depth 2160p Video Format with\r\na TMDS Character Rate greater than 340Mcsc, complies with all of the required Pixel and line counts.", ControlType.Text);
            if (hf1_14_2 != null)
            {
                send_resolution_to_clent("1024x768@60MDSCLONE");
                System.Threading.Thread.Sleep(2000);
                send_resolution_to_clent("3840x2160@60MDS8BPC");
                System.Threading.Thread.Sleep(4000);
                return;
            }

            AutomationElement hf1_14_3 = SelectElementNameControlType("Test HF1-14, Iter-03\r\nConfirm that the Source, whenever transmitting any 24-bit color depth 2160p Video Format with\r\na TMDS Character Rate greater than 340Mcsc, complies with all of the required Pixel and line counts.", ControlType.Text);
            if (hf1_14_3 != null)
            {
                send_resolution_to_clent("1024x768@60MDSCLONE");
                System.Threading.Thread.Sleep(2000);
                send_resolution_to_clent("4096x2160@50MDS8BPC");
                System.Threading.Thread.Sleep(4000);
                return;
            }

            AutomationElement hf1_14_4 = SelectElementNameControlType("Test HF1-14, Iter-04\r\nConfirm that the Source, whenever transmitting any 24-bit color depth 2160p Video Format with\r\na TMDS Character Rate greater than 340Mcsc, complies with all of the required Pixel and line counts.", ControlType.Text);
            if (hf1_14_4 != null)
            {
                send_resolution_to_clent("1024x768@60MDSCLONE");
                System.Threading.Thread.Sleep(2000);
                send_resolution_to_clent("4096x2160@60MDS8BPC");
                System.Threading.Thread.Sleep(4000);
                return;
            }

            AutomationElement hf1_18_1 = SelectElementNameControlType("Test HF1-18, Iter-01\r\nConfirm that the Source, whenever transmitting any Video Format with a TMDS Character Rate greater\r\nthan 340Mcsc, transmits an accurate AVI InfoFrame at least once per every two video fields.", ControlType.Text);
            if (hf1_18_1 != null)
            {
                send_resolution_to_clent("1024x768@60MDSCLONE");
                System.Threading.Thread.Sleep(2000);
                send_resolution_to_clent("3840x2160@50MDS8BPC");
                System.Threading.Thread.Sleep(4000);
                return;
            }

            AutomationElement hf1_18_2 = SelectElementNameControlType("Test HF1-18, Iter-02\r\nConfirm that the Source, whenever transmitting any Video Format with a TMDS Character Rate greater\r\nthan 340Mcsc, transmits an accurate AVI InfoFrame at least once per every two video fields.", ControlType.Text);
            if (hf1_18_2 != null)
            {
                send_resolution_to_clent("1024x768@60MDSCLONE");
                System.Threading.Thread.Sleep(2000);
                send_resolution_to_clent("3840x2160@60MDS8BPC");
                System.Threading.Thread.Sleep(4000);
                return;
            }

            AutomationElement hf1_18_3 = SelectElementNameControlType("Test HF1-18, Iter-03\r\nConfirm that the Source, whenever transmitting any Video Format with a TMDS Character Rate greater\r\nthan 340Mcsc, transmits an accurate AVI InfoFrame at least once per every two video fields.", ControlType.Text);
            if (hf1_18_3 != null)
            {
                send_resolution_to_clent("1024x768@60MDSCLONE");
                System.Threading.Thread.Sleep(2000);
                send_resolution_to_clent("4096x2160@50MDS8BPC");
                System.Threading.Thread.Sleep(4000);
                return;
            }

            AutomationElement hf1_18_4 = SelectElementNameControlType("Test HF1-18, Iter-04\r\nConfirm that the Source, whenever transmitting any Video Format with a TMDS Character Rate greater\r\nthan 340Mcsc, transmits an accurate AVI InfoFrame at least once per every two video fields.", ControlType.Text);
            if (hf1_18_4 != null)
            {
                send_resolution_to_clent("1024x768@60MDSCLONE");
                System.Threading.Thread.Sleep(2000);
                send_resolution_to_clent("4096x2160@60MDS8BPC");
                System.Threading.Thread.Sleep(4000);
                return;
            }

            AutomationElement hf1_31_1 = SelectElementNameControlType("Test HF1-31, Iter-01\r\nConfirm that a YCBCR 4:2:0 Pixel encoding-capable Source DUT outputs correct YCBCR 4:2:0 Pixel\r\ne...xels and the order of the color-component data of the test\r\nPixels with fully saturated (extreme-value) color components.", ControlType.Text);
            if (hf1_31_1 != null)
            {
                send_resolution_to_clent("1024x768@60MDSCLONE");
                System.Threading.Thread.Sleep(2000);
                send_resolution_to_clent("3840x2160@50MDS8BPC");
                ///ycbcr encoding
                System.Threading.Thread.Sleep(4000);
                return;
            }

            AutomationElement hf1_31_2 = SelectElementNameControlType("Test HF1-31, Iter-02\r\nConfirm that a YCBCR 4:2:0 Pixel encoding-capable Source DUT outputs correct YCBCR 4:2:0 Pixel\r\ne...xels and the order of the color-component data of the test\r\nPixels with fully saturated (extreme-value) color components.", ControlType.Text);
            if (hf1_31_2 != null)
            {
                send_resolution_to_clent("1024x768@60MDSCLONE");
                System.Threading.Thread.Sleep(2000);
                send_resolution_to_clent("3840x2160@60MDS8BPC");
                ///ycbcr encoding
                System.Threading.Thread.Sleep(4000);
                return;
            }


            AutomationElement hf1_31_3 = SelectElementNameControlType("Test HF1-31, Iter-03\r\nConfirm that a YCBCR 4:2:0 Pixel encoding-capable Source DUT outputs correct YCBCR 4:2:0 Pixel\r\ne...xels and the order of the color-component data of the test\r\nPixels with fully saturated (extreme-value) color components.", ControlType.Text);
            if (hf1_31_3 != null)
            {
                send_resolution_to_clent("1024x768@60MDSCLONE");
                System.Threading.Thread.Sleep(2000);
                send_resolution_to_clent("4096x2160@50MDS8BPC");
                ///ycbcr encoding
                System.Threading.Thread.Sleep(4000);
                return;
            }

            AutomationElement hf1_31_4 = SelectElementNameControlType("Test HF1-31, Iter-04\r\nConfirm that a YCBCR 4:2:0 Pixel encoding-capable Source DUT outputs correct YCBCR 4:2:0 Pixel\r\ne...xels and the order of the color-component data of the test\r\nPixels with fully saturated (extreme-value) color components.", ControlType.Text);
            if (hf1_31_4 != null)
            {
                send_resolution_to_clent("1024x768@60MDSCLONE");
                System.Threading.Thread.Sleep(2000);
                send_resolution_to_clent("4096x2160@60MDS8BPC");
                ///ycbcr encoding
                System.Threading.Thread.Sleep(4000);
                return;
            }

            AutomationElement hf1_31_5 = SelectElementNameControlType("Test HF1-31, Iter-05\r\nConfirm that a YCBCR 4:2:0 Pixel encoding-capable Source DUT outputs correct YCBCR 4:2:0 Pixel\r\ne...xels and the order of the color-component data of the test\r\nPixels with fully saturated (extreme-value) color components.", ControlType.Text);
            if (hf1_31_5 != null)
            {
                send_resolution_to_clent("1024x768@60MDSCLONE");
                System.Threading.Thread.Sleep(2000);
                /////Any Resolution
                send_resolution_to_clent("1280x720@60MDS8BPC");
                ///ycbcr encoding
                System.Threading.Thread.Sleep(4000);
                return;
            }

            AutomationElement hf1_33_1 = SelectElementNameControlType("Test HF1-33, Iter-01\r\nConfirm that the Source outputs the correct timing for YCBCR 4:2:0 timings.", ControlType.Text);
            if (hf1_33_1 != null)
            {
                send_resolution_to_clent("1024x768@60MDSCLONE");
                System.Threading.Thread.Sleep(2000);
                send_resolution_to_clent("3840x2160@50MDS8BPC");
                ////ycbcr encoding
                System.Threading.Thread.Sleep(4000);
                return;
            }

            AutomationElement hf1_33_2 = SelectElementNameControlType("Test HF1-33, Iter-02\r\nConfirm that the Source outputs the correct timing for YCBCR 4:2:0 timings.", ControlType.Text);
            if (hf1_33_2 != null)
            {
                send_resolution_to_clent("1024x768@60MDSCLONE");
                System.Threading.Thread.Sleep(2000);
                send_resolution_to_clent("3840x2160@60MDS8BPC");
                ////ycbcr encoding
                System.Threading.Thread.Sleep(4000);
                return;
            }

            AutomationElement hf1_33_3 = SelectElementNameControlType("Test HF1-33, Iter-03\r\nConfirm that the Source outputs the correct timing for YCBCR 4:2:0 timings.", ControlType.Text);
            if (hf1_33_3 != null)
            {
                send_resolution_to_clent("1024x768@60MDSCLONE");
                System.Threading.Thread.Sleep(2000);
                send_resolution_to_clent("4096x2160@50MDS8BPC");
                ////ycbcr encoding
                System.Threading.Thread.Sleep(4000);
                return;
            }

            AutomationElement hf1_33_4 = SelectElementNameControlType("Test HF1-33, Iter-04\r\nConfirm that the Source outputs the correct timing for YCBCR 4:2:0 timings.", ControlType.Text);
            if (hf1_33_4 != null)
            {
                send_resolution_to_clent("1024x768@60MDSCLONE");
                System.Threading.Thread.Sleep(2000);
                send_resolution_to_clent("4096x2160@60MDS8BPC");
                ////ycbcr encoding
                System.Threading.Thread.Sleep(4000);
                return;
            }

            AutomationElement hf1_51_1 = SelectElementNameControlType("Test HF1-51, Iter-01\r\nConfirm that the YCBCR 4:2:0 signaling information in the AVI InfoFrame is correct.", ControlType.Text);
            if (hf1_51_1 != null)
            {
                send_resolution_to_clent("1024x768@60MDSCLONE");
                System.Threading.Thread.Sleep(2000);
                send_resolution_to_clent("3840x2160@50MDS8BPC");
                ////ycbcr encoding
                System.Threading.Thread.Sleep(4000);
                return;
            }


            AutomationElement hf1_51_2 = SelectElementNameControlType("Test HF1-51, Iter-02\r\nConfirm that the YCBCR 4:2:0 signaling information in the AVI InfoFrame is correct.", ControlType.Text);
            if (hf1_51_2 != null)
            {
                send_resolution_to_clent("1024x768@60MDSCLONE");
                System.Threading.Thread.Sleep(2000);
                send_resolution_to_clent("3840x2160@50MDS8BPC");
                ////ycbcr encoding
                System.Threading.Thread.Sleep(4000);
                return;
            }


            AutomationElement hf1_51_3 = SelectElementNameControlType("Test HF1-51, Iter-03\r\nConfirm that the YCBCR 4:2:0 signaling information in the AVI InfoFrame is correct.", ControlType.Text);
            if (hf1_51_3 != null)
            {
                send_resolution_to_clent("1024x768@60MDSCLONE");
                System.Threading.Thread.Sleep(2000);
                send_resolution_to_clent("3840x2160@50MDS8BPC");
                ////ycbcr encoding
                System.Threading.Thread.Sleep(4000);
                return;
            }


            AutomationElement hf1_51_4 = SelectElementNameControlType("Test HF1-51, Iter-04\r\nConfirm that the YCBCR 4:2:0 signaling information in the AVI InfoFrame is correct.", ControlType.Text);
            if (hf1_51_4 != null)
            {
                send_resolution_to_clent("1024x768@60MDSCLONE");
                System.Threading.Thread.Sleep(2000);
                send_resolution_to_clent("3840x2160@30MDS8BPC");
                ////ycbcr encoding
                System.Threading.Thread.Sleep(4000);
                return;
            }


            AutomationElement hf1_51_5 = SelectElementNameControlType("Test HF1-51, Iter-05\r\nConfirm that the YCBCR 4:2:0 signaling information in the AVI InfoFrame is correct.", ControlType.Text);
            if (hf1_51_5 != null)
            {
                send_resolution_to_clent("1024x768@60MDSCLONE");
                System.Threading.Thread.Sleep(2000);
                send_resolution_to_clent("3840x2160@60MDS8BPC");
                ////ycbcr encoding
                System.Threading.Thread.Sleep(4000);
                return;
            }

            AutomationElement hf1_51_6 = SelectElementNameControlType("Test HF1-51, Iter-06\r\nConfirm that the YCBCR 4:2:0 signaling information in the AVI InfoFrame is correct.", ControlType.Text);
            if (hf1_51_6 != null)
            {
                send_resolution_to_clent("1024x768@60MDSCLONE");
                System.Threading.Thread.Sleep(2000);
                send_resolution_to_clent("3840x2160@60MDS8BPC");
                ////ycbcr encoding
                System.Threading.Thread.Sleep(4000);
                return;
            }

            AutomationElement hf1_51_7 = SelectElementNameControlType("Test HF1-51, Iter-07\r\nConfirm that the YCBCR 4:2:0 signaling information in the AVI InfoFrame is correct.", ControlType.Text);
            if (hf1_51_7 != null)
            {
                send_resolution_to_clent("1024x768@60MDSCLONE");
                System.Threading.Thread.Sleep(2000);
                send_resolution_to_clent("3840x2160@60MDS8BPC");
                ////ycbcr encoding
                System.Threading.Thread.Sleep(4000);
                return;
            }

            AutomationElement hf1_51_8 = SelectElementNameControlType("Test HF1-51, Iter-08\r\nConfirm that the YCBCR 4:2:0 signaling information in the AVI InfoFrame is correct.", ControlType.Text);
            if (hf1_51_8 != null)
            {
                send_resolution_to_clent("1024x768@60MDSCLONE");
                System.Threading.Thread.Sleep(2000);
                send_resolution_to_clent("3840x2160@30MDS8BPC");
                ////ycbcr encoding
                System.Threading.Thread.Sleep(4000);
                return;
            }

            AutomationElement hf1_51_9 = SelectElementNameControlType("Test HF1-51, Iter-09\r\nConfirm that the YCBCR 4:2:0 signaling information in the AVI InfoFrame is correct.", ControlType.Text);
            if (hf1_51_9 != null)
            {
                send_resolution_to_clent("1024x768@60MDSCLONE");
                System.Threading.Thread.Sleep(2000);
                send_resolution_to_clent("4096x2160@50MDS8BPC");
                ////ycbcr encoding
                System.Threading.Thread.Sleep(4000);
                return;
            }

            AutomationElement hf1_51_10 = SelectElementNameControlType("Test HF1-51, Iter-10\r\nConfirm that the YCBCR 4:2:0 signaling information in the AVI InfoFrame is correct.", ControlType.Text);
            if (hf1_51_10 != null)
            {
                send_resolution_to_clent("1024x768@60MDSCLONE");
                System.Threading.Thread.Sleep(2000);
                send_resolution_to_clent("4096x2160@50MDS8BPC");
                ////ycbcr encoding
                System.Threading.Thread.Sleep(4000);
                return;
            }

            AutomationElement hf1_51_11 = SelectElementNameControlType("Test HF1-51, Iter-11\r\nConfirm that the YCBCR 4:2:0 signaling information in the AVI InfoFrame is correct.", ControlType.Text);
            if (hf1_51_11 != null)
            {
                send_resolution_to_clent("1024x768@60MDSCLONE");
                System.Threading.Thread.Sleep(2000);
                send_resolution_to_clent("4096x2160@50MDS8BPC");
                ////ycbcr encoding
                System.Threading.Thread.Sleep(4000);
                return;
            }

            AutomationElement hf1_51_12 = SelectElementNameControlType("Test HF1-51, Iter-12\r\nConfirm that the YCBCR 4:2:0 signaling information in the AVI InfoFrame is correct.", ControlType.Text);
            if (hf1_51_12 != null)
            {
                send_resolution_to_clent("1024x768@60MDSCLONE");
                System.Threading.Thread.Sleep(2000);
                send_resolution_to_clent("3840x2160@30MDS8BPC");
                ////ycbcr encoding
                System.Threading.Thread.Sleep(4000);
                return;
            }


            AutomationElement hf1_51_13 = SelectElementNameControlType("Test HF1-51, Iter-13\r\nConfirm that the YCBCR 4:2:0 signaling information in the AVI InfoFrame is correct.", ControlType.Text);
            if (hf1_51_13 != null)
            {
                send_resolution_to_clent("1024x768@60MDSCLONE");
                System.Threading.Thread.Sleep(2000);
                send_resolution_to_clent("4096x2160@60MDS8BPC");
                ////ycbcr encoding
                System.Threading.Thread.Sleep(4000);
                return;
            }

            AutomationElement hf1_51_14 = SelectElementNameControlType("Test HF1-51, Iter-14\r\nConfirm that the YCBCR 4:2:0 signaling information in the AVI InfoFrame is correct.", ControlType.Text);
            if (hf1_51_14 != null)
            {
                send_resolution_to_clent("1024x768@60MDSCLONE");
                System.Threading.Thread.Sleep(2000);
                send_resolution_to_clent("4096x2160@60MDS8BPC");
                ////ycbcr encoding
                System.Threading.Thread.Sleep(4000);
                return;
            }

            AutomationElement hf1_51_15 = SelectElementNameControlType("Test HF1-51, Iter-15\r\nConfirm that the YCBCR 4:2:0 signaling information in the AVI InfoFrame is correct.", ControlType.Text);
            if (hf1_51_15 != null)
            {
                send_resolution_to_clent("1024x768@60MDSCLONE");
                System.Threading.Thread.Sleep(2000);
                send_resolution_to_clent("4096x2160@60MDS8BPC");
                ////ycbcr encoding
                System.Threading.Thread.Sleep(4000);
                return;
            }

            AutomationElement hf1_51_16 = SelectElementNameControlType("Test HF1-51, Iter-16\r\nConfirm that the YCBCR 4:2:0 signaling information in the AVI InfoFrame is correct.", ControlType.Text);
            if (hf1_51_16 != null)
            {
                send_resolution_to_clent("1024x768@60MDSCLONE");
                System.Threading.Thread.Sleep(2000);
                send_resolution_to_clent("3840x2160@30MDS8BPC");
                ////ycbcr encoding
                System.Threading.Thread.Sleep(4000);
                return;
            }

  /*          string screenWidth = Screen.PrimaryScreen.Bounds.Width.ToString();

            string screenHeight = Screen.PrimaryScreen.Bounds.Height.ToString();

            string Resolution_to_check = screenWidth + "x" + screenHeight;


            if(Resolution_to_check == "1280x720")
            {
                send_resolution_to_clent("3840x2160@50MDS8BPC");
                System.Threading.Thread.Sleep(4000);
            }

    */

        }



        private void pass_fail_handler()
        {
            AutomationElement image_validation_title = SelectElementNameControlType("Image Validation", ControlType.TitleBar);
            System.Threading.Thread.Sleep(1000);

            AutomationElement ycbcrCheck = SelectElementNameControlType("YCbCr 4:2:0 Check", ControlType.TitleBar);
            System.Threading.Thread.Sleep(1000);


            if (image_validation_title != null || ycbcrCheck != null)
            {

                    AutomationElement mpass_button = SelectElementNameControlType("PASS     ", ControlType.Button);
                    if (mpass_button != null)
                    {
                        Invoke(mpass_button);
                        System.Threading.Thread.Sleep(2000);
                        return;
                    }
           }
            
        }





        //Checks the network connection
        public void Network_Check()
        {
            int Waittime = 0;
            while (Waittime <= 10)
            {
                Ping ping = new Ping();
                PingReply pingresults = ping.Send(CLIENT_ADDRESS.Text);
                if (pingresults.Status.ToString() == "Success")
                {
                    
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

        //Handle required DUT configuration pop up
        private void req_dut_config_handler()
        {
            AutomationElement dut_config = SelectElementNameControlType("DUT Configuration", ControlType.TitleBar);
            System.Threading.Thread.Sleep(1000);
            if (dut_config != null)
            {
                if (dut_config.Current.IsOffscreen == false)
                {
                    read_test_name_for_playing_audio();//Read test name and iteration for playin audio and enabling deep color

                    test_7_32_function();//Separate test handler for 7_32 test because to close hbr app after running iteration 2

                    ycbcr_tests();//handle ycbcr test cases

                    System.Threading.Thread.Sleep(2000);
                    //After all these, press continue button
                    AutomationElement continue_button = SelectElementNameControlType("Continue", ControlType.Button);

                    if (continue_button != null)
                    {
                        Invoke(continue_button);
                        System.Threading.Thread.Sleep(1000);
                        return;
                    }
                }
            }

        }

        //DUT configuration error pop up
        private void dut_config_err_handler()
        {

            AutomationElement dut_config_err = SelectElementNameControlType("DUT Configuration Error", ControlType.Text);
            System.Threading.Thread.Sleep(1000);

            if (dut_config_err != null)
            {
                if (dut_config_err.Current.IsOffscreen == false)
                {
                    if (count_value >= 3)
                    {
                        AutomationElement fail_this_iteration = SelectElementNameControlType("FAIL this Iteration", ControlType.Button);
                        if (fail_this_iteration != null)
                        { 
                            Invoke(fail_this_iteration);
                        }
                        System.Threading.Thread.Sleep(1000);
                        count_value = 0;
                    }
                    else
                    {
                        AutomationElement retry_dut_config = SelectElementNameControlType("Retry DUT Configuration", ControlType.Button);
                        if (retry_dut_config != null)
                        {
                            Invoke(retry_dut_config);
                        }

                        System.Threading.Thread.Sleep(1000);
                        count_value++;
                        if(count_value == 3)
                        {
                            count_value = 0;
                        }
                        return;
                    }
                }
            }
        }

        //Manual pass fail pop up handler
        private void manual_pass_fail_handler()
        {
            AutomationElement image_validation_title = SelectElementNameControlType("Image Validation", ControlType.TitleBar);
            System.Threading.Thread.Sleep(1000);

            if (image_validation_title != null)
            {
                if (image_validation_title.Current.IsOffscreen == false)
                {
                    Network_Check();
                    System.Threading.Thread.Sleep(5000);
                    //Close HBR App
                    string client_data = "CloseHBR";
                    uint count=0;
                exc1: try
                    {
                        count++;
                        Client.Class1 Client1 = new Client.Class1();
                        Client1.Client(CLIENT_ADDRESS.Text, client_data);
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

                            else if (result1 == DialogResult.Cancel)
                            {

                            }
                        }
                    }
                    System.Threading.Thread.Sleep(1000);

                    ////// Data reciveve 

                    string data_rece;
                    SERVER.Class1 server1 = new SERVER.Class1();
                    data_rece = server1.Server();

                    System.Threading.Thread.Sleep(1000);

                    AutomationElement mpass_button = SelectElementNameControlType("PASS     ", ControlType.Button);
                    //Use 7-24 iteration 10 to disable ycbcr feature after completing 10 iterations
                    AutomationElement test_7_24_10 = SelectElementNameControlType("Test 7-24, Iter-10\r\nVerify that the Source DUT always outputs pixel encoding that correlates with AVI fields\r\nY0 and Y1 when presented with a YCbCr-capable Sink and that the DUT is capable of\r\nsupporting YCbCr pixel encoding when required.", ControlType.Text);

                    if (test_7_24_10 != null)
                    {
                        if (test_7_24_10.Current.IsOffscreen == false)
                        {
                            string test_name = test_7_24_10.Current.Name;
                            string test_no = test_name.Substring(5, 13);

                            if (test_no == "7-24, Iter-10")
                            {
                                disable_Ycbcr();
                                System.Threading.Thread.Sleep(1000);
                                enable_Ycbcr();

                                if (mpass_button != null)
                                {
                                    Invoke(mpass_button);
                                    System.Threading.Thread.Sleep(20000);
                                    disable_Ycbcr();//Disable ycbcr after 10 th iteration
                                    return;
                                }
                            }
                        }
                    }
                    mpass_button = SelectElementNameControlType("PASS     ", ControlType.Button);
                    if (mpass_button != null)
                    {
                        Invoke(mpass_button);
                        System.Threading.Thread.Sleep(2000);
                        return;
                    }
                }
            }
        }



        //Audio Channel Selection handler
        private void audio_handler()
        {
            string test_name;
            string test_no;

            AutomationElement audio_config = SelectElementNameControlType("Audio Configuration", ControlType.TitleBar);

            if (audio_config != null)
            {
                if (audio_config.Current.IsOffscreen == false)
                {//Select particular channel for particular iteration
                    AutomationElement test_30_6 = SelectElementNameControlType("Test 7-30, Iter-06\r\nVerify that the Source audio packet jitter is within the limits specified.", ControlType.Text);

                    if (test_30_6 != null)
                    {
                        if (test_30_6.Current.IsOffscreen == false)
                        {
                            test_name = test_30_6.Current.Name;
                            test_no = test_name.Substring(5, 13);
                            audio_channel_select_handler(test_no);
                        }
                    }

                    AutomationElement test_30_3 = SelectElementNameControlType("Test 7-30, Iter-03\r\nVerify that the Source audio packet jitter is within the limits specified.", ControlType.Text);

                    if (test_30_3 != null)
                    {
                        if (test_30_3.Current.IsOffscreen == false)
                        {
                            test_name = test_30_3.Current.Name;
                            test_no = test_name.Substring(5, 13);
                            audio_channel_select_handler(test_no);
                        }
                    }

                    AutomationElement test_30_4 = SelectElementNameControlType("Test 7-30, Iter-04\r\nVerify that the Source audio packet jitter is within the limits specified.", ControlType.Text);

                    if (test_30_4 != null)
                    {
                        if (test_30_4.Current.IsOffscreen == false)
                        {
                            test_name = test_30_4.Current.Name;
                            test_no = test_name.Substring(5, 13);
                            audio_channel_select_handler(test_no);
                        }
                    }

                    AutomationElement test_30_5 = SelectElementNameControlType("Test 7-30, Iter-05\r\nVerify that the Source audio packet jitter is within the limits specified.", ControlType.Text);

                    if (test_30_5 != null)
                    {
                        if (test_30_5.Current.IsOffscreen == false)
                        {
                            test_name = test_30_5.Current.Name;
                            test_no = test_name.Substring(5, 13);
                            audio_channel_select_handler(test_no);
                        }
                    }

                    AutomationElement test_30_7 = SelectElementNameControlType("Test 7-30, Iter-07\r\nVerify that the Source audio packet jitter is within the limits specified.", ControlType.Text);

                    if (test_30_7 != null)
                    {
                        if (test_30_7.Current.IsOffscreen == false)
                        {
                            test_name = test_30_7.Current.Name;
                            test_no = test_name.Substring(5, 13);
                            audio_channel_select_handler(test_no);
                        }
                    }

                    AutomationElement test_30_8 = SelectElementNameControlType("Test 7-30, Iter-08\r\nVerify that the Source audio packet jitter is within the limits specified.", ControlType.Text);

                    if (test_30_8 != null)
                    {
                        if (test_30_8.Current.IsOffscreen == false)
                        {
                            test_name = test_30_8.Current.Name;
                            test_no = test_name.Substring(5, 13);
                            audio_channel_select_handler(test_no);
                        }
                    }

                    AutomationElement test_30_9 = SelectElementNameControlType("Test 7-30, Iter-09\r\nVerify that the Source audio packet jitter is within the limits specified.", ControlType.Text);

                    if (test_30_9 != null)
                    {
                        if (test_30_9.Current.IsOffscreen == false)
                        {
                            test_name = test_30_9.Current.Name;
                            test_no = test_name.Substring(5, 13);
                            audio_channel_select_handler(test_no);
                        }
                    }

                    AutomationElement test_30_10 = SelectElementNameControlType("Test 7-30, Iter-10\r\nVerify that the Source audio packet jitter is within the limits specified.", ControlType.Text);

                    if (test_30_10 != null)
                    {
                        if (test_30_10.Current.IsOffscreen == false)
                        {
                            test_name = test_30_10.Current.Name;
                            test_no = test_name.Substring(5, 13);
                            audio_channel_select_handler(test_no);
                        }
                    }


                }
            }

        }
//Reading test name and iteration
        private void read_test_name_for_playing_audio()
        {
            string test_name, test_no;

            AutomationElement test_7_16_1 = SelectElementNameControlType("Test 7-16, Iter-01\r\nVerify that the source outputs legal 10-bit codes.", ControlType.Text);

            if (test_7_16_1 != null)
            {
                if (test_7_16_1.Current.IsOffscreen == false)
                {
                    test_name = test_7_16_1.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-16")
                    {
                        channel_2_48khz_24_bit_hbr_player();
                        return;
                    }
                }
            }

            AutomationElement test_7_16_2 = SelectElementNameControlType("Test 7-16, Iter-02\r\nVerify that the source outputs legal 10-bit codes.", ControlType.Text);

            if (test_7_16_2 != null)
            {
                if (test_7_16_2.Current.IsOffscreen == false)
                {
                    test_name = test_7_16_2.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-16")
                    {
                        channel_2_48khz_24_bit_hbr_player();
                        return;
                    }
                }
            }

            AutomationElement test_7_16_3 = SelectElementNameControlType("Test 7-16, Iter-03\r\nVerify that the source outputs legal 10-bit codes.", ControlType.Text);

            if (test_7_16_3 != null)
            {
                if (test_7_16_3.Current.IsOffscreen == false)
                {
                    test_name = test_7_16_3.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-16")
                    {
                        channel_2_48khz_24_bit_hbr_player();
                        return;
                    }
                }
            }

            AutomationElement test_7_17_1 = SelectElementNameControlType("Test 7-17, Iter-01\r\nVerify that the Source only outputs code sequences for Control Periods, Data Island Periods and\r\nVideo Data Periods corresponding to basic HDMI protocol rules.", ControlType.Text);

            if (test_7_17_1 != null)
            {
                if (test_7_17_1.Current.IsOffscreen == false)
                {
                    test_name = test_7_17_1.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-17")
                    {
                        channel_2_48khz_24_bit_hbr_player();
                        return;
                    }
                }
            }


            AutomationElement test_7_17_2 = SelectElementNameControlType("Test 7-17, Iter-02\r\nVerify that the Source only outputs code sequences for Control Periods, Data Island Periods and\r\nVideo Data Periods corresponding to basic HDMI protocol rules.", ControlType.Text);

            if (test_7_17_2 != null)
            {
                if (test_7_17_2.Current.IsOffscreen == false)
                {
                    test_name = test_7_17_2.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-17")
                    {
                        channel_2_48khz_24_bit_hbr_player();
                        return;
                    }
                }
            }

            AutomationElement test_7_17_3 = SelectElementNameControlType("Test 7-17, Iter-03\r\nVerify that the Source only outputs code sequences for Control Periods, Data Island Periods and\r\nVideo Data Periods corresponding to basic HDMI protocol rules.", ControlType.Text);

            if (test_7_17_3 != null)
            {
                if (test_7_17_3.Current.IsOffscreen == false)
                {
                    test_name = test_7_17_3.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-17")
                    {
                        channel_2_48khz_24_bit_hbr_player();
                        return;
                    }
                }
            }


            AutomationElement test_7_18_1 = SelectElementNameControlType("Test 7-18, Iter-01\r\nVerify that Source outputs an Extended Control Period within the required period.", ControlType.Text);

            if (test_7_18_1 != null)
            {
                if (test_7_18_1.Current.IsOffscreen == false)
                {
                    test_name = test_7_18_1.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-18")
                    {
                        channel_2_48khz_24_bit_hbr_player();
                        return;
                    }
                }
            }

            AutomationElement test_7_18_2 = SelectElementNameControlType("Test 7-18, Iter-02\r\nVerify that Source outputs an Extended Control Period within the required period.", ControlType.Text);

            if (test_7_18_2 != null)
            {
                if (test_7_18_2.Current.IsOffscreen == false)
                {
                    test_name = test_7_18_2.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-18")
                    {
                        channel_2_48khz_24_bit_hbr_player();
                        return;
                    }
                }
            }

            AutomationElement test_7_18_3 = SelectElementNameControlType("Test 7-18, Iter-03\r\nVerify that Source outputs an Extended Control Period within the required period.", ControlType.Text);

            if (test_7_18_3 != null)
            {
                if (test_7_18_3.Current.IsOffscreen == false)
                {
                    test_name = test_7_18_3.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-18")
                    {
                        channel_2_48khz_24_bit_hbr_player();
                        return;
                    }
                }
            }

            AutomationElement test_7_19_1 = SelectElementNameControlType("Test 7-19, Iter-01\r\nVerify that Source only transmits permitted Packet Types and reserved fields are zero.", ControlType.Text);

            if (test_7_19_1 != null)
            {
                if (test_7_19_1.Current.IsOffscreen == false)
                {
                    test_name = test_7_19_1.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-19")
                    {
                        channel_2_48khz_24_bit_hbr_player();
                        return;
                    }
                }
            }

            AutomationElement test_7_19_2 = SelectElementNameControlType("Test 7-19, Iter-02\r\nVerify that Source only transmits permitted Packet Types and reserved fields are zero.", ControlType.Text);

            if (test_7_19_1 != null)
            {
                if (test_7_19_1.Current.IsOffscreen == false)
                {
                    test_name = test_7_19_1.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-19")
                    {
                        channel_2_48khz_24_bit_hbr_player();
                        return;
                    }
                }
            }

            AutomationElement test_7_19_3 = SelectElementNameControlType("Test 7-19, Iter-03\r\nVerify that Source only transmits permitted Packet Types and reserved fields are zero.", ControlType.Text);

            if (test_7_19_1 != null)
            {
                if (test_7_19_1.Current.IsOffscreen == false)
                {
                    test_name = test_7_19_1.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-19")
                    {
                        channel_2_48khz_24_bit_hbr_player();
                        return;
                    }
                }
            }

            AutomationElement test_7_19_4 = SelectElementNameControlType("Test 7-19, Iter-04\r\nVerify that Source only transmits permitted Packet Types and reserved fields are zero.", ControlType.Text);

            if (test_7_19_4 != null)
            {
                if (test_7_19_4.Current.IsOffscreen == false)
                {
                    test_name = test_7_19_4.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-19")
                    {
                        channel_2_48khz_24_bit_hbr_player();
                        return;
                    }
                }
            }

            AutomationElement test_7_19_5 = SelectElementNameControlType("Test 7-19, Iter-05\r\nVerify that Source only transmits permitted Packet Types and reserved fields are zero.", ControlType.Text);

            if (test_7_19_5 != null)
            {
                if (test_7_19_5.Current.IsOffscreen == false)
                {
                    test_name = test_7_19_5.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-19")
                    {
                        channel_2_48khz_24_bit_hbr_player();
                        return;
                    }
                }
            }

            AutomationElement test_7_19_6 = SelectElementNameControlType("Test 7-19, Iter-06\r\nVerify that Source only transmits permitted Packet Types and reserved fields are zero.", ControlType.Text);

            if (test_7_19_6 != null)
            {
                if (test_7_19_6.Current.IsOffscreen == false)
                {
                    test_name = test_7_19_6.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-19")
                    {
                        channel_2_48khz_24_bit_hbr_player();
                        return;
                    }
                }
            }

            AutomationElement test_7_23_1 = SelectElementNameControlType("Test 7-23, Iter-01\r\nVerify that the Source DUT always outputs required pixel encoding (RGB), which also\r\ncorrelates with AVI fields Y0 and Y1 when connected to an RGB-only Sink.", ControlType.Text);

            if (test_7_23_1 != null)
            {
                if (test_7_23_1.Current.IsOffscreen == false)
                {
                    test_name = test_7_23_1.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-23")
                    {
                        return;
                    }
                }
            }

            AutomationElement test_7_23_2 = SelectElementNameControlType("Test 7-23, Iter-02\r\nVerify that the Source DUT always outputs required pixel encoding (RGB), which also\r\ncorrelates with AVI fields Y0 and Y1 when connected to an RGB-only Sink.", ControlType.Text);

            if (test_7_23_2 != null)
            {
                if (test_7_23_2.Current.IsOffscreen == false)
                {
                    test_name = test_7_23_2.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-23")
                    {
                        return;
                    }
                }
            }

            AutomationElement test_7_23_3 = SelectElementNameControlType("Test 7-23, Iter-03\r\nVerify that the Source DUT always outputs required pixel encoding (RGB), which also\r\ncorrelates with AVI fields Y0 and Y1 when connected to an RGB-only Sink.", ControlType.Text);

            if (test_7_23_3 != null)
            {
                if (test_7_23_3.Current.IsOffscreen == false)
                {
                    test_name = test_7_23_3.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-23")
                    {
                        return;
                    }
                }
            }

            AutomationElement test_7_23_4 = SelectElementNameControlType("Test 7-23, Iter-04\r\nVerify that the Source DUT always outputs required pixel encoding (RGB), which also\r\ncorrelates with AVI fields Y0 and Y1 when connected to an RGB-only Sink.", ControlType.Text);

            if (test_7_23_4 != null)
            {
                if (test_7_23_4.Current.IsOffscreen == false)
                {
                    test_name = test_7_23_4.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-23")
                    {
                        return;
                    }
                }
            }

            AutomationElement test_7_23_5 = SelectElementNameControlType("Test 7-23, Iter-05\r\nVerify that the Source DUT always outputs required pixel encoding (RGB), which also\r\ncorrelates with AVI fields Y0 and Y1 when connected to an RGB-only Sink.", ControlType.Text);

            if (test_7_23_5 != null)
            {
                if (test_7_23_5.Current.IsOffscreen == false)
                {
                    test_name = test_7_23_5.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-23")
                    {
                        return;
                    }
                }
            }

            AutomationElement test_7_23_6 = SelectElementNameControlType("Test 7-23, Iter-06\r\nVerify that the Source DUT always outputs required pixel encoding (RGB), which also\r\ncorrelates with AVI fields Y0 and Y1 when connected to an RGB-only Sink.", ControlType.Text);

            if (test_7_23_6 != null)
            {
                if (test_7_23_6.Current.IsOffscreen == false)
                {
                    test_name = test_7_23_6.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-23")
                    {
                        return;
                    }
                }
            }

            AutomationElement test_7_23_7 = SelectElementNameControlType("Test 7-23, Iter-07\r\nVerify that the Source DUT always outputs required pixel encoding (RGB), which also\r\ncorrelates with AVI fields Y0 and Y1 when connected to an RGB-only Sink.", ControlType.Text);

            if (test_7_23_7 != null)
            {
                if (test_7_23_7.Current.IsOffscreen == false)
                {
                    test_name = test_7_23_7.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-23")
                    {
                        return;
                    }
                }
            }

            AutomationElement test_7_23_8 = SelectElementNameControlType("Test 7-23, Iter-08\r\nVerify that the Source DUT always outputs required pixel encoding (RGB), which also\r\ncorrelates with AVI fields Y0 and Y1 when connected to an RGB-only Sink.", ControlType.Text);

            if (test_7_23_8 != null)
            {
                if (test_7_23_8.Current.IsOffscreen == false)
                {
                    test_name = test_7_23_8.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-23")
                    {
                        return;
                    }
                }
            }

            AutomationElement test_7_23_9 = SelectElementNameControlType("Test 7-23, Iter-09\r\nVerify that the Source DUT always outputs required pixel encoding (RGB), which also\r\ncorrelates with AVI fields Y0 and Y1 when connected to an RGB-only Sink.", ControlType.Text);

            if (test_7_23_9 != null)
            {
                if (test_7_23_9.Current.IsOffscreen == false)
                {
                    test_name = test_7_23_9.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-23")
                    {
                        return;
                    }
                }
            }

            AutomationElement test_7_23_10 = SelectElementNameControlType("Test 7-23, Iter-10\r\nVerify that the Source DUT always outputs required pixel encoding (RGB), which also\r\ncorrelates with AVI fields Y0 and Y1 when connected to an RGB-only Sink.", ControlType.Text);

            if (test_7_23_10 != null)
            {
                if (test_7_23_10.Current.IsOffscreen == false)
                {
                    test_name = test_7_23_10.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-23")
                    {
                        return;
                    }
                }
            }

            AutomationElement test_7_23_11 = SelectElementNameControlType("Test 7-23, Iter-11\r\nVerify that the Source DUT always outputs required pixel encoding (RGB), which also\r\ncorrelates with AVI fields Y0 and Y1 when connected to an RGB-only Sink.", ControlType.Text);

            if (test_7_23_11 != null)
            {
                if (test_7_23_11.Current.IsOffscreen == false)
                {
                    test_name = test_7_23_11.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-23")
                    {
                        return;
                    }
                }
            }

            AutomationElement test_7_23_12 = SelectElementNameControlType("Test 7-23, Iter-12\r\nVerify that the Source DUT always outputs required pixel encoding (RGB), which also\r\ncorrelates with AVI fields Y0 and Y1 when connected to an RGB-only Sink.", ControlType.Text);

            if (test_7_23_12 != null)
            {
                if (test_7_23_12.Current.IsOffscreen == false)
                {
                    test_name = test_7_23_12.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-23")
                    {
                        return;
                    }
                }
            }

            AutomationElement test_7_25_1 = SelectElementNameControlType("Test 7-25, Iter-01\r\nVerify that Source DUT, whenever transmitting any CEA video format, complies with all\r\nrequired pixel and line counts and pixel clock frequency range.", ControlType.Text);

            if (test_7_25_1 != null)
            {
                if (test_7_25_1.Current.IsOffscreen == false)
                {
                    test_name = test_7_25_1.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-25")
                    {
                        return;
                    }
                }
            }

            AutomationElement test_7_25_2 = SelectElementNameControlType("Test 7-25, Iter-02\r\nVerify that Source DUT, whenever transmitting any CEA video format, complies with all\r\nrequired pixel and line counts and pixel clock frequency range.", ControlType.Text);

            if (test_7_25_2 != null)
            {
                if (test_7_25_2.Current.IsOffscreen == false)
                {
                    test_name = test_7_25_2.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-25")
                    {
                        return;
                    }
                }
            }

            AutomationElement test_7_25_3 = SelectElementNameControlType("Test 7-25, Iter-03\r\nVerify that Source DUT, whenever transmitting any CEA video format, complies with all\r\nrequired pixel and line counts and pixel clock frequency range.", ControlType.Text);

            if (test_7_25_3 != null)
            {
                if (test_7_25_3.Current.IsOffscreen == false)
                {
                    test_name = test_7_25_3.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-25")
                    {
                        return;
                    }
                }
            }

            AutomationElement test_7_25_4 = SelectElementNameControlType("Test 7-25, Iter-04\r\nVerify that Source DUT, whenever transmitting any CEA video format, complies with all\r\nrequired pixel and line counts and pixel clock frequency range.", ControlType.Text);

            if (test_7_25_4 != null)
            {
                if (test_7_25_4.Current.IsOffscreen == false)
                {
                    test_name = test_7_25_4.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-25")
                    {
                        return;
                    }
                }
            }

            AutomationElement test_7_25_5 = SelectElementNameControlType("Test 7-25, Iter-05\r\nVerify that Source DUT, whenever transmitting any CEA video format, complies with all\r\nrequired pixel and line counts and pixel clock frequency range.", ControlType.Text);

            if (test_7_25_5 != null)
            {
                if (test_7_25_5.Current.IsOffscreen == false)
                {
                    test_name = test_7_25_5.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-25")
                    {
                        return;
                    }
                }
            }

            AutomationElement test_7_25_6 = SelectElementNameControlType("Test 7-25, Iter-06\r\nVerify that Source DUT, whenever transmitting any CEA video format, complies with all\r\nrequired pixel and line counts and pixel clock frequency range.", ControlType.Text);

            if (test_7_25_6 != null)
            {
                if (test_7_25_6.Current.IsOffscreen == false)
                {
                    test_name = test_7_25_6.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-25")
                    {
                        return;
                    }
                }
            }

            AutomationElement test_7_25_7 = SelectElementNameControlType("Test 7-25, Iter-07\r\nVerify that Source DUT, whenever transmitting any CEA video format, complies with all\r\nrequired pixel and line counts and pixel clock frequency range.", ControlType.Text);

            if (test_7_25_7 != null)
            {
                if (test_7_25_7.Current.IsOffscreen == false)
                {
                    test_name = test_7_25_7.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-25")
                    {
                        return;
                    }
                }
            }

            AutomationElement test_7_25_8 = SelectElementNameControlType("Test 7-25, Iter-08\r\nVerify that Source DUT, whenever transmitting any CEA video format, complies with all\r\nrequired pixel and line counts and pixel clock frequency range.", ControlType.Text);

            if (test_7_25_8 != null)
            {
                if (test_7_25_8.Current.IsOffscreen == false)
                {
                    test_name = test_7_25_8.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-25")
                    {
                        return;
                    }
                }
            }

            AutomationElement test_7_25_9 = SelectElementNameControlType("Test 7-25, Iter-09\r\nVerify that Source DUT, whenever transmitting any CEA video format, complies with all\r\nrequired pixel and line counts and pixel clock frequency range.", ControlType.Text);

            if (test_7_25_9 != null)
            {
                if (test_7_25_9.Current.IsOffscreen == false)
                {
                    test_name = test_7_25_9.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-25")
                    {
                        return;
                    }
                }
            }

            AutomationElement test_7_25_10 = SelectElementNameControlType("Test 7-25, Iter-10\r\nVerify that Source DUT, whenever transmitting any CEA video format, complies with all\r\nrequired pixel and line counts and pixel clock frequency range.", ControlType.Text);

            if (test_7_25_10 != null)
            {
                if (test_7_25_10.Current.IsOffscreen == false)
                {
                    test_name = test_7_25_10.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-25")
                    {
                        return;
                    }
                }
            }

            AutomationElement test_7_25_11 = SelectElementNameControlType("Test 7-25, Iter-11\r\nVerify that Source DUT, whenever transmitting any CEA video format, complies with all\r\nrequired pixel and line counts and pixel clock frequency range.", ControlType.Text);

            if (test_7_25_11 != null)
            {
                if (test_7_25_11.Current.IsOffscreen == false)
                {
                    test_name = test_7_25_11.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-25")
                    {
                        return;
                    }
                }
            }

            AutomationElement test_7_25_12 = SelectElementNameControlType("Test 7-25, Iter-12\r\nVerify that Source DUT, whenever transmitting any CEA video format, complies with all\r\nrequired pixel and line counts and pixel clock frequency range.", ControlType.Text);

            if (test_7_25_12 != null)
            {
                if (test_7_25_12.Current.IsOffscreen == false)
                {
                    test_name = test_7_25_12.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-25")
                    {
                        return;
                    }
                }
            }

            AutomationElement test_7_26_1 = SelectElementNameControlType("Test 7-26, Iter-01\r\nVerify that Source DUT indicates Pixel Repetition values in the AVI as required and\r\nthat the pixels are actually repeated the indicated number of times.", ControlType.Text);

            if (test_7_26_1 != null)
            {
                if (test_7_26_1.Current.IsOffscreen == false)
                {
                    test_name = test_7_26_1.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-26")
                    {
                        return;
                    }
                }
            }

            AutomationElement test_7_26_2 = SelectElementNameControlType("Test 7-26, Iter-02\r\nVerify that Source DUT indicates Pixel Repetition values in the AVI as required and\r\nthat the pixels are actually repeated the indicated number of times.", ControlType.Text);

            if (test_7_26_2 != null)
            {
                if (test_7_26_2.Current.IsOffscreen == false)
                {
                    test_name = test_7_26_2.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-26")
                    {
                        return;
                    }
                }
            }

            AutomationElement test_7_26_3 = SelectElementNameControlType("Test 7-26, Iter-03\r\nVerify that Source DUT indicates Pixel Repetition values in the AVI as required and\r\nthat the pixels are actually repeated the indicated number of times.", ControlType.Text);

            if (test_7_26_3 != null)
            {
                if (test_7_26_3.Current.IsOffscreen == false)
                {
                    test_name = test_7_26_3.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-26")
                    {
                        return;
                    }
                }
            }

            AutomationElement test_7_26_4 = SelectElementNameControlType("Test 7-26, Iter-04\r\nVerify that Source DUT indicates Pixel Repetition values in the AVI as required and\r\nthat the pixels are actually repeated the indicated number of times.", ControlType.Text);

            if (test_7_26_4 != null)
            {
                if (test_7_26_4.Current.IsOffscreen == false)
                {
                    test_name = test_7_26_4.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-26")
                    {
                        return;
                    }
                }
            }

            AutomationElement test_7_26_5 = SelectElementNameControlType("Test 7-26, Iter-05\r\nVerify that Source DUT indicates Pixel Repetition values in the AVI as required and\r\nthat the pixels are actually repeated the indicated number of times.", ControlType.Text);

            if (test_7_26_5 != null)
            {
                if (test_7_26_5.Current.IsOffscreen == false)
                {
                    test_name = test_7_26_5.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-26")
                    {
                        return;
                    }
                }
            }

            AutomationElement test_7_26_6 = SelectElementNameControlType("Test 7-26, Iter-06\r\nVerify that Source DUT indicates Pixel Repetition values in the AVI as required and\r\nthat the pixels are actually repeated the indicated number of times.", ControlType.Text);

            if (test_7_26_6 != null)
            {
                if (test_7_26_6.Current.IsOffscreen == false)
                {
                    test_name = test_7_26_6.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-26")
                    {
                        return;
                    }
                }
            }

            AutomationElement test_7_26_7 = SelectElementNameControlType("Test 7-26, Iter-07\r\nVerify that Source DUT indicates Pixel Repetition values in the AVI as required and\r\nthat the pixels are actually repeated the indicated number of times.", ControlType.Text);

            if (test_7_26_7 != null)
            {
                if (test_7_26_7.Current.IsOffscreen == false)
                {
                    test_name = test_7_26_7.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-26")
                    {
                        return;
                    }
                }
            }

            AutomationElement test_7_26_8 = SelectElementNameControlType("Test 7-26, Iter-08\r\nVerify that Source DUT indicates Pixel Repetition values in the AVI as required and\r\nthat the pixels are actually repeated the indicated number of times.", ControlType.Text);

            if (test_7_26_8 != null)
            {
                if (test_7_26_8.Current.IsOffscreen == false)
                {
                    test_name = test_7_26_8.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-26")
                    {
                        return;
                    }
                }
            }

            AutomationElement test_7_26_9 = SelectElementNameControlType("Test 7-26, Iter-09\r\nVerify that Source DUT indicates Pixel Repetition values in the AVI as required and\r\nthat the pixels are actually repeated the indicated number of times.", ControlType.Text);

            if (test_7_26_9 != null)
            {
                if (test_7_26_9.Current.IsOffscreen == false)
                {
                    test_name = test_7_26_9.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-26")
                    {
                        return;
                    }
                }
            }

            AutomationElement test_7_26_10 = SelectElementNameControlType("Test 7-26, Iter-10\r\nVerify that Source DUT indicates Pixel Repetition values in the AVI as required and\r\nthat the pixels are actually repeated the indicated number of times.", ControlType.Text);

            if (test_7_26_10 != null)
            {
                if (test_7_26_10.Current.IsOffscreen == false)
                {
                    test_name = test_7_26_10.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-26")
                    {
                        return;
                    }
                }
            }

            AutomationElement test_7_26_11 = SelectElementNameControlType("Test 7-26, Iter-11\r\nVerify that Source DUT indicates Pixel Repetition values in the AVI as required and\r\nthat the pixels are actually repeated the indicated number of times.", ControlType.Text);

            if (test_7_26_11 != null)
            {
                if (test_7_26_11.Current.IsOffscreen == false)
                {
                    test_name = test_7_26_11.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-26")
                    {
                        return;
                    }
                }
            }

            AutomationElement test_7_26_12 = SelectElementNameControlType("Test 7-26, Iter-12\r\nVerify that Source DUT indicates Pixel Repetition values in the AVI as required and\r\nthat the pixels are actually repeated the indicated number of times.", ControlType.Text);

            if (test_7_26_12 != null)
            {
                if (test_7_26_12.Current.IsOffscreen == false)
                {
                    test_name = test_7_26_12.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-26")
                    {
                        return;
                    }
                }
            }

            AutomationElement test_7_27_1 = SelectElementNameControlType("Test 7-27, Iter-01\r\nVerify that at least one AVI InfoFrame is transmitted for every two video fields when\r\nrequired and that any AVI InfoFrame is accurate.", ControlType.Text);

            if (test_7_27_1 != null)
            {
                if (test_7_27_1.Current.IsOffscreen == false)
                {
                    test_name = test_7_27_1.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-27")
                    {
                        return;
                    }
                }
            }

            AutomationElement test_7_27_2 = SelectElementNameControlType("Test 7-27, Iter-02\r\nVerify that at least one AVI InfoFrame is transmitted for every two video fields when\r\nrequired and that any AVI InfoFrame is accurate.", ControlType.Text);

            if (test_7_27_2 != null)
            {
                if (test_7_27_2.Current.IsOffscreen == false)
                {
                    test_name = test_7_27_2.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-27")
                    {
                        return;
                    }
                }
            }

            AutomationElement test_7_27_3 = SelectElementNameControlType("Test 7-27, Iter-03\r\nVerify that at least one AVI InfoFrame is transmitted for every two video fields when\r\nrequired and that any AVI InfoFrame is accurate.", ControlType.Text);

            if (test_7_27_3 != null)
            {
                if (test_7_27_3.Current.IsOffscreen == false)
                {
                    test_name = test_7_27_3.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-27")
                    {
                        return;
                    }
                }
            }

            AutomationElement test_7_27_4 = SelectElementNameControlType("Test 7-27, Iter-04\r\nVerify that at least one AVI InfoFrame is transmitted for every two video fields when\r\nrequired and that any AVI InfoFrame is accurate.", ControlType.Text);

            if (test_7_27_4 != null)
            {
                if (test_7_27_4.Current.IsOffscreen == false)
                {
                    test_name = test_7_27_4.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-27")
                    {
                        return;
                    }
                }
            }

            AutomationElement test_7_27_5 = SelectElementNameControlType("Test 7-27, Iter-05\r\nVerify that at least one AVI InfoFrame is transmitted for every two video fields when\r\nrequired and that any AVI InfoFrame is accurate.", ControlType.Text);

            if (test_7_27_5 != null)
            {
                if (test_7_27_5.Current.IsOffscreen == false)
                {
                    test_name = test_7_27_5.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-27")
                    {
                        return;
                    }
                }
            }

            AutomationElement test_7_27_6 = SelectElementNameControlType("Test 7-27, Iter-06\r\nVerify that at least one AVI InfoFrame is transmitted for every two video fields when\r\nrequired and that any AVI InfoFrame is accurate.", ControlType.Text);

            if (test_7_27_6 != null)
            {
                if (test_7_27_6.Current.IsOffscreen == false)
                {
                    test_name = test_7_27_6.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-27")
                    {
                        return;
                    }
                }
            }

            AutomationElement test_7_27_7 = SelectElementNameControlType("Test 7-27, Iter-07\r\nVerify that at least one AVI InfoFrame is transmitted for every two video fields when\r\nrequired and that any AVI InfoFrame is accurate.", ControlType.Text);

            if (test_7_27_7 != null)
            {
                if (test_7_27_7.Current.IsOffscreen == false)
                {
                    test_name = test_7_27_7.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-27")
                    {
                        return;
                    }
                }
            }

            AutomationElement test_7_27_8 = SelectElementNameControlType("Test 7-27, Iter-08\r\nVerify that at least one AVI InfoFrame is transmitted for every two video fields when\r\nrequired and that any AVI InfoFrame is accurate.", ControlType.Text);

            if (test_7_27_8 != null)
            {
                if (test_7_27_8.Current.IsOffscreen == false)
                {
                    test_name = test_7_27_8.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-27")
                    {
                        return;
                    }
                }
            }

            AutomationElement test_7_27_9 = SelectElementNameControlType("Test 7-27, Iter-09\r\nVerify that at least one AVI InfoFrame is transmitted for every two video fields when\r\nrequired and that any AVI InfoFrame is accurate.", ControlType.Text);

            if (test_7_27_9 != null)
            {
                if (test_7_27_9.Current.IsOffscreen == false)
                {
                    test_name = test_7_27_9.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-27")
                    {
                        return;
                    }
                }
            }

            AutomationElement test_7_27_10 = SelectElementNameControlType("Test 7-27, Iter-10\r\nVerify that at least one AVI InfoFrame is transmitted for every two video fields when\r\nrequired and that any AVI InfoFrame is accurate.", ControlType.Text);

            if (test_7_27_10 != null)
            {
                if (test_7_27_10.Current.IsOffscreen == false)
                {
                    test_name = test_7_27_10.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-27")
                    {
                        return;
                    }
                }
            }

            AutomationElement test_7_27_11 = SelectElementNameControlType("Test 7-27, Iter-11\r\nVerify that at least one AVI InfoFrame is transmitted for every two video fields when\r\nrequired and that any AVI InfoFrame is accurate.", ControlType.Text);

            if (test_7_27_11 != null)
            {
                if (test_7_27_11.Current.IsOffscreen == false)
                {
                    test_name = test_7_27_11.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-27")
                    {
                        return;
                    }
                }
            }

            AutomationElement test_7_27_12 = SelectElementNameControlType("Test 7-27, Iter-12\r\nVerify that at least one AVI InfoFrame is transmitted for every two video fields when\r\nrequired and that any AVI InfoFrame is accurate.", ControlType.Text);

            if (test_7_27_12 != null)
            {
                if (test_7_27_12.Current.IsOffscreen == false)
                {
                    test_name = test_7_27_12.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-27")
                    {
                        return;
                    }
                }
            }

            AutomationElement test_7_27_13 = SelectElementNameControlType("Test 7-27, Iter-13\r\nVerify that at least one AVI InfoFrame is transmitted for every two video fields when\r\nrequired and that any AVI InfoFrame is accurate.", ControlType.Text);

            if (test_7_27_13 != null)
            {
                if (test_7_27_13.Current.IsOffscreen == false)
                {
                    test_name = test_7_27_13.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-27")
                    {
                        return;
                    }
                }
            }

            AutomationElement test_7_27_14 = SelectElementNameControlType("Test 7-27, Iter-14\r\nVerify that at least one AVI InfoFrame is transmitted for every two video fields when\r\nrequired and that any AVI InfoFrame is accurate.", ControlType.Text);

            if (test_7_27_14 != null)
            {
                if (test_7_27_14.Current.IsOffscreen == false)
                {
                    test_name = test_7_27_14.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-27")
                    {
                        return;
                    }
                }
            }

            AutomationElement test_7_27_15 = SelectElementNameControlType("Test 7-27, Iter-15\r\nVerify that at least one AVI InfoFrame is transmitted for every two video fields when\r\nrequired and that any AVI InfoFrame is accurate.", ControlType.Text);

            if (test_7_27_15 != null)
            {
                if (test_7_27_15.Current.IsOffscreen == false)
                {
                    test_name = test_7_27_15.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-27")
                    {
                        return;
                    }
                }
            }

            AutomationElement test_7_27_16 = SelectElementNameControlType("Test 7-27, Iter-16\r\nVerify that at least one AVI InfoFrame is transmitted for every two video fields when\r\nrequired and that any AVI InfoFrame is accurate.", ControlType.Text);

            if (test_7_27_16 != null)
            {
                if (test_7_27_16.Current.IsOffscreen == false)
                {
                    test_name = test_7_27_16.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-27")
                    {
                        return;
                    }
                }
            }



            AutomationElement test_7_28_1 = SelectElementNameControlType("Test 7-28, Iter-01\r\nVerify that the behavior of all fields within the Audio Sample or High Bitrate Audio\r\nStream Subpackets follow the corresponding rules specified in the IEC 60958 or\r\nIEC 61937 specifications.", ControlType.Text);

            if (test_7_28_1 != null)
            {
                if (test_7_28_1.Current.IsOffscreen == false)
                {
                    test_name = test_7_28_1.Current.Name;
                    test_no = test_name.Substring(5, 13);

                    if (test_no == "7-28, Iter-01")
                    {
                        channel_2_48khz_24_bit_hbr_player();
                        return;
                    }
                }
            }

            AutomationElement test_7_28_2 = SelectElementNameControlType("Test 7-28, Iter-02\r\nVerify that the behavior of all fields within the Audio Sample or High Bitrate Audio\r\nStream Subpackets follow the corresponding rules specified in the IEC 60958 or\r\nIEC 61937 specifications.", ControlType.Text);

            if (test_7_28_2 != null)
            {
                if (test_7_28_2.Current.IsOffscreen == false)
                {
                    test_name = test_7_28_2.Current.Name;
                    test_no = test_name.Substring(5, 13);

                    if (test_no == "7-28, Iter-02")
                    {
                        send_resolution_to_clent("1920x1080@60MDS8BPC");
                        System.Threading.Thread.Sleep(1000);

                        channel_8_192khz_16_bit_hbr_player();
                        return;
                    }
                }
            }


            AutomationElement test_7_28_3 = SelectElementNameControlType("Test 7-28, Iter-03\r\nVerify that the behavior of all fields within the Audio Sample or High Bitrate Audio\r\nStream Subpackets follow the corresponding rules specified in the IEC 60958 or\r\nIEC 61937 specifications.", ControlType.Text);

            if (test_7_28_3 != null)
            {
                if (test_7_28_3.Current.IsOffscreen == false)
                {
                    test_name = test_7_28_3.Current.Name;
                    test_no = test_name.Substring(5, 13);

                    if (test_no == "7-28, Iter-03")
                    {
                        send_resolution_to_clent("1920x1080@60MDS8BPC");
                        System.Threading.Thread.Sleep(1000);

                        dts_hd_hbr_player();
                        return;
                    }
                }
            }

            AutomationElement test_7_28_4 = SelectElementNameControlType("Test 7-28, Iter-04\r\nVerify that the behavior of all fields within the Audio Sample or High Bitrate Audio\r\nStream Subpackets follow the corresponding rules specified in the IEC 60958 or\r\nIEC 61937 specifications.", ControlType.Text);

            if (test_7_28_4 != null)
            {
                if (test_7_28_4.Current.IsOffscreen == false)
                {
                    test_name = test_7_28_4.Current.Name;
                    test_no = test_name.Substring(5, 13);

                    if (test_no == "7-28, Iter-04")
                    {
                        channel_2_48khz_24_bit_hbr_player();
                        return;
                    }
                }
            }

            AutomationElement test_7_29_1 = SelectElementNameControlType("Test 7-29, Iter-01\r\nVerify that the relationship between the parameters (N, CTS, audio sample rate) is\r\ncorrect with respect to the Audio Clock Regeneration mechanism.", ControlType.Text);

            if (test_7_29_1 != null)
            {
                if (test_7_29_1.Current.IsOffscreen == false)
                {
                    test_name = test_7_29_1.Current.Name;
                    test_no = test_name.Substring(5, 13);

                    if (test_no == "7-29, Iter-01")
                    {
                        channel_2_48khz_24_bit_hbr_player();
                        return;
                    }
                }
            }

            AutomationElement test_7_29_2 = SelectElementNameControlType("Test 7-29, Iter-02\r\nVerify that the relationship between the parameters (N, CTS, audio sample rate) is\r\ncorrect with respect to the Audio Clock Regeneration mechanism.", ControlType.Text);
            if (test_7_29_2 != null)
            {
                if (test_7_29_2.Current.IsOffscreen == false)
                {
                    test_name = test_7_29_2.Current.Name;
                    test_no = test_name.Substring(5, 13);

                    if (test_no == "7-29, Iter-02")
                    {

                        enable_deep_color();
                        System.Threading.Thread.Sleep(1000);
                        send_resolution_to_clent("720x480@59MDS8BPC");
                        System.Threading.Thread.Sleep(1000);
                        send_resolution_to_clent("720x480@60MDS8BPC");
                        channel_2_48khz_24_bit_hbr_player();
                        return;
                    }
                }
            }

            AutomationElement test_7_29_3 = SelectElementNameControlType("Test 7-29, Iter-03\r\nVerify that the relationship between the parameters (N, CTS, audio sample rate) is\r\ncorrect with respect to the Audio Clock Regeneration mechanism.", ControlType.Text);

            if (test_7_29_3 != null)
            {
                if (test_7_29_3.Current.IsOffscreen == false)
                {
                    test_name = test_7_29_3.Current.Name;
                    test_no = test_name.Substring(5, 13);

                    if (test_no == "7-29, Iter-03")
                    {
                        channel_2_48khz_24_bit_hbr_player();
                        return;
                    }
                }
            }
            //Send 1920x1080p Resolution for test cases asking any resolution
            AutomationElement test_7_29_4 = SelectElementNameControlType("Test 7-29, Iter-04\r\nVerify that the relationship between the parameters (N, CTS, audio sample rate) is\r\ncorrect with respect to the Audio Clock Regeneration mechanism.", ControlType.Text);
            if (test_7_29_4 != null)
            {
                if (test_7_29_4.Current.IsOffscreen == false)
                {
                    test_name = test_7_29_4.Current.Name;
                    test_no = test_name.Substring(5, 13);

                    if (test_no == "7-29, Iter-04")
                    {
                        enable_deep_color();
                        System.Threading.Thread.Sleep(1000);
                        send_resolution_to_clent("1920x1080@59MDS8BPC");
                        System.Threading.Thread.Sleep(1000);
                        send_resolution_to_clent("1920x1080@60MDS8BPC");
                        channel_2_48khz_24_bit_hbr_player();
                        return;
                    }
                }
            }

            AutomationElement test_7_30_1 = SelectElementNameControlType("Test 7-30, Iter-01\r\nVerify that the Source audio packet jitter is within the limits specified.", ControlType.Text);
            if (test_7_30_1 != null)
            {
                if (test_7_30_1.Current.IsOffscreen == false)
                {
                    test_name = test_7_30_1.Current.Name;
                    test_no = test_name.Substring(5, 13);

                    if (test_no == "7-30, Iter-01")
                    {
                        channel_8_192khz_16_bit_hbr_player();
                        return;
                    }
                }
            }


            AutomationElement test_7_30_2 = SelectElementNameControlType("Test 7-30, Iter-02\r\nVerify that the Source audio packet jitter is within the limits specified.", ControlType.Text);
            if (test_7_30_2 != null)
            {
                if (test_7_30_2.Current.IsOffscreen == false)
                {
                    test_name = test_7_30_2.Current.Name;
                    test_no = test_name.Substring(5, 13);

                    if (test_no == "7-30, Iter-02")
                    {
                        channel_2_48khz_24_bit_hbr_player();
                        return;
                    }
                }
            }

            AutomationElement test_7_30_3 = SelectElementNameControlType("Test 7-30, Iter-03\r\nVerify that the Source audio packet jitter is within the limits specified.", ControlType.Text);
            if (test_7_30_3 != null)
            {
                if (test_7_30_3.Current.IsOffscreen == false)
                {
                    test_name = test_7_30_3.Current.Name;
                    test_no = test_name.Substring(5, 13);

                    if (test_no == "7-30, Iter-03")
                    {
                        channel_2_48khz_24_bit_hbr_player();
                        return;
                    }
                }
            }

            AutomationElement test_7_30_4 = SelectElementNameControlType("Test 7-30, Iter-04\r\nVerify that the Source audio packet jitter is within the limits specified.", ControlType.Text);
            if (test_7_30_4 != null)
            {
                if (test_7_30_4.Current.IsOffscreen == false)
                {
                    test_name = test_7_30_4.Current.Name;
                    test_no = test_name.Substring(5, 13);

                    if (test_no == "7-30, Iter-04")
                    {
                        channel_8_192khz_16_bit_hbr_player();
                        return;
                    }
                }
            }

            AutomationElement test_7_30_5 = SelectElementNameControlType("Test 7-30, Iter-05\r\nVerify that the Source audio packet jitter is within the limits specified.", ControlType.Text);
            if (test_7_30_5 != null)
            {
                if (test_7_30_5.Current.IsOffscreen == false)
                {
                    test_name = test_7_30_1.Current.Name;
                    test_no = test_name.Substring(5, 13);

                    if (test_no == "7-30, Iter-05")
                    {
                        channel_2_48khz_24_bit_hbr_player();
                        return;
                    }
                }
            }

            AutomationElement test_7_30_8 = SelectElementNameControlType("Test 7-30, Iter-08\r\nVerify that the Source audio packet jitter is within the limits specified.", ControlType.Text);
            if (test_7_30_8 != null)
            {
                if (test_7_30_8.Current.IsOffscreen == false)
                {
                    test_name = test_7_30_8.Current.Name;
                    test_no = test_name.Substring(5, 13);

                    if (test_no == "7-30, Iter-08")
                    {
                        channel_8_192khz_16_bit_hbr_player();
                        return;
                    }
                }
            }

            AutomationElement test_7_30_9 = SelectElementNameControlType("Test 7-30, Iter-09\r\nVerify that the Source audio packet jitter is within the limits specified.", ControlType.Text);
            if (test_7_30_9 != null)
            {
                if (test_7_30_9.Current.IsOffscreen == false)
                {
                    test_name = test_7_30_9.Current.Name;
                    test_no = test_name.Substring(5, 13);

                    if (test_no == "7-30, Iter-09")
                    {
                        channel_8_192khz_16_bit_hbr_player();
                        return;
                    }
                }
            }

            AutomationElement test_7_31_1 = SelectElementNameControlType("Test 7-31, Iter-01\r\nVerify that the Source transmits an Audio InfoFrame whenever required and that the\r\ncontents are valid.", ControlType.Text);
            if (test_7_31_1 != null)
            {
                if (test_7_31_1.Current.IsOffscreen == false)
                {
                    test_name = test_7_31_1.Current.Name;
                    test_no = test_name.Substring(5, 13);

                    if (test_no == "7-31, Iter-01")
                    {
                        channel_2_48khz_24_bit_hbr_player();
                        return;
                    }
                }
            }

            //Send 1920x1080p Resolution for test cases asking any resolution
            AutomationElement test_7_31_2 = SelectElementNameControlType("Test 7-31, Iter-02\r\nVerify that the Source transmits an Audio InfoFrame whenever required and that the\r\ncontents are valid.", ControlType.Text);

            if (test_7_31_2 != null)
            {
                if (test_7_31_2.Current.IsOffscreen == false)
                {
                    test_name = test_7_31_2.Current.Name;
                    test_no = test_name.Substring(5, 13);

                    if (test_no == "7-31, Iter-02")
                    {
                        send_resolution_to_clent("1920x1080@60MDS8BPC");
                        System.Threading.Thread.Sleep(1000);

                        channel_8_192khz_16_bit_hbr_player();
                        return;
                    }
                }
            }

            AutomationElement test_7_31_3 = SelectElementNameControlType("Test 7-31, Iter-03\r\nVerify that the Source transmits an Audio InfoFrame whenever required and that the\r\ncontents are valid.", ControlType.Text);

            if (test_7_31_3 != null)
            {
                if (test_7_31_3.Current.IsOffscreen == false)
                {
                    test_name = test_7_31_3.Current.Name;
                    test_no = test_name.Substring(5, 13);

                    if (test_no == "7-31, Iter-03")
                    {
                        channel_2_48khz_24_bit_hbr_player();
                        return;
                    }
                }
            }

            //Deep Color Tests and changing resolution so as to apply deep color feature
            AutomationElement test_7_34_1 = SelectElementNameControlType("Test 7-34, Iter-01\r\nVerify that a Deep Color capable Source DUT outputs correct Deep Color packing and signaling.", ControlType.Text);
            if (test_7_34_1 != null)
            {
                if (test_7_34_1.Current.IsOffscreen == false)
                {
                    test_name = test_7_34_1.Current.Name;
                    test_no = test_name.Substring(5, 13);

                    if (test_no == "7-34, Iter-01")
                    {
                        enable_deep_color();
                        System.Threading.Thread.Sleep(1000);
                        send_resolution_to_clent("640x480@59MDS8BPC");
                        System.Threading.Thread.Sleep(1000);
                        send_resolution_to_clent("640x480@60MDS8BPC");
                        return;
                    }
                }
            }

            AutomationElement test_7_34_2 = SelectElementNameControlType("Test 7-34, Iter-02\r\nVerify that a Deep Color capable Source DUT outputs correct Deep Color packing and signaling.", ControlType.Text);

            if (test_7_34_2 != null)
            {
                if (test_7_34_2.Current.IsOffscreen == false)
                {
                    test_name = test_7_34_2.Current.Name;
                    test_no = test_name.Substring(5, 13);

                    if (test_no == "7-34, Iter-02")
                    {
                        enable_deep_color();
                        System.Threading.Thread.Sleep(1000);
                        send_resolution_to_clent("720x480@59MDS8BPC");
                        System.Threading.Thread.Sleep(1000);
                        send_resolution_to_clent("720x480@60MDS8BPC");
                        return;
                    }
                }
            }

            AutomationElement test_7_34_3 = SelectElementNameControlType("Test 7-34, Iter-03\r\nVerify that a Deep Color capable Source DUT outputs correct Deep Color packing and signaling.", ControlType.Text);
            if (test_7_34_3 != null)
            {
                if (test_7_34_3.Current.IsOffscreen == false)
                {
                    test_name = test_7_34_3.Current.Name;
                    test_no = test_name.Substring(5, 13);

                    if (test_no == "7-34, Iter-03")
                    {
                        enable_deep_color();
                        System.Threading.Thread.Sleep(1000);
                        send_resolution_to_clent("1280x720@59MDS8BPC");
                        System.Threading.Thread.Sleep(1000);
                        send_resolution_to_clent("1280x720@60MDS8BPC");
                        return;
                    }
                }
            }

            AutomationElement test_7_34_4 = SelectElementNameControlType("Test 7-34, Iter-04\r\nVerify that a Deep Color capable Source DUT outputs correct Deep Color packing and signaling.", ControlType.Text);
            if (test_7_34_4 != null)
            {
                if (test_7_34_4.Current.IsOffscreen == false)
                {
                    test_name = test_7_34_4.Current.Name;
                    test_no = test_name.Substring(5, 13);

                    if (test_no == "7-34, Iter-04")
                    {
                        enable_deep_color();
                        System.Threading.Thread.Sleep(1000);
                        send_resolution_to_clent("1920x1080@i59MDS8BPC");
                        System.Threading.Thread.Sleep(1000);
                        send_resolution_to_clent("1920x1080@i60MDS8BPC");
                        return;
                    }
                }
            }

            AutomationElement test_7_34_5 = SelectElementNameControlType("Test 7-34, Iter-05\r\nVerify that a Deep Color capable Source DUT outputs correct Deep Color packing and signaling.", ControlType.Text);
            if (test_7_34_5 != null)
            {
                if (test_7_34_5.Current.IsOffscreen == false)
                {
                    test_name = test_7_34_5.Current.Name;
                    test_no = test_name.Substring(5, 13);

                    if (test_no == "7-34, Iter-05")
                    {
                        enable_deep_color();
                        System.Threading.Thread.Sleep(1000);
                        send_resolution_to_clent("1920x1080@59MDS8BPC");

                        System.Threading.Thread.Sleep(1000);

                        send_resolution_to_clent("1920x1080@60MDS8BPC");

                        return;
                    }
                }
            }

            AutomationElement test_7_34_6 = SelectElementNameControlType("Test 7-34, Iter-06\r\nVerify that a Deep Color capable Source DUT outputs correct Deep Color packing and signaling.", ControlType.Text);

            if (test_7_34_6 != null)
            {
                if (test_7_34_6.Current.IsOffscreen == false)
                {
                    test_name = test_7_34_6.Current.Name;
                    test_no = test_name.Substring(5, 13);

                    if (test_no == "7-34, Iter-06")
                    {
                        enable_deep_color();
                        System.Threading.Thread.Sleep(1000);
                        send_resolution_to_clent("720x576@49MDS8BPC");
                        System.Threading.Thread.Sleep(1000);
                        send_resolution_to_clent("720x576@50MDS8BPC");
                        return;
                    }
                }
            }

            AutomationElement test_7_34_7 = SelectElementNameControlType("Test 7-34, Iter-07\r\nVerify that a Deep Color capable Source DUT outputs correct Deep Color packing and signaling.", ControlType.Text);
            if (test_7_34_7 != null)
            {
                if (test_7_34_7.Current.IsOffscreen == false)
                {
                    test_name = test_7_34_7.Current.Name;
                    test_no = test_name.Substring(5, 13);

                    if (test_no == "7-34, Iter-07")
                    {
                        enable_deep_color();
                        System.Threading.Thread.Sleep(1000);
                        send_resolution_to_clent("1280x720@49MDS8BPC");
                        System.Threading.Thread.Sleep(1000);
                        send_resolution_to_clent("1280x720@50MDS8BPC");
                        return;
                    }
                }
            }

            AutomationElement test_7_34_8 = SelectElementNameControlType("Test 7-34, Iter-08\r\nVerify that a Deep Color capable Source DUT outputs correct Deep Color packing and signaling.", ControlType.Text);
            if (test_7_34_8 != null)
            {
                if (test_7_34_8.Current.IsOffscreen == false)
                {
                    test_name = test_7_34_8.Current.Name;
                    test_no = test_name.Substring(5, 13);

                    if (test_no == "7-34, Iter-08")
                    {
                        enable_deep_color();
                        System.Threading.Thread.Sleep(1000);
                        send_resolution_to_clent("1920x1080@49MDS8BPC");
                        System.Threading.Thread.Sleep(1000);
                        send_resolution_to_clent("1920x1080@50MDS8BPC");

                        return;
                    }
                }
            }

            AutomationElement test_7_34_9 = SelectElementNameControlType("Test 7-34, Iter-09\r\nVerify that a Deep Color capable Source DUT outputs correct Deep Color packing and signaling.", ControlType.Text);
            if (test_7_34_9 != null)
            {
                if (test_7_34_9.Current.IsOffscreen == false)
                {
                    test_name = test_7_34_9.Current.Name;
                    test_no = test_name.Substring(5, 13);

                    if (test_no == "7-34, Iter-09")
                    {
                        enable_deep_color();
                        System.Threading.Thread.Sleep(1000);
                        send_resolution_to_clent("1920x1080@i49MDS8BPC");
                        System.Threading.Thread.Sleep(1000);
                        send_resolution_to_clent("1920x1080@i50MDS8BPC");
                        return;
                    }
                }
            }

            AutomationElement test_7_34_10 = SelectElementNameControlType("Test 7-34, Iter-10\r\nVerify that a Deep Color capable Source DUT outputs correct Deep Color packing and signaling.", ControlType.Text);
            if (test_7_34_10 != null)
            {
                if (test_7_34_10.Current.IsOffscreen == false)
                {
                    test_name = test_7_34_10.Current.Name;
                    test_no = test_name.Substring(5, 13);

                    if (test_no == "7-34, Iter-10")
                    {
                        enable_deep_color();
                        System.Threading.Thread.Sleep(1000);
                        send_resolution_to_clent("720x576@i49MDS8BPC");
                        System.Threading.Thread.Sleep(1000);
                        send_resolution_to_clent("720x576@i50MDS8BPC");
                        return;
                    }
                }
            }
            ///xvYCC Tests
            AutomationElement test_7_35_1 = SelectElementNameControlType("Test 7-35, Iter-01\r\nVerify that an xvYCC capable Source outputs valid Gamut Metadata Packets.", ControlType.Text);

            if (test_7_35_1 != null)
            {
                if (test_7_35_1.Current.IsOffscreen == false)
                {
                    test_name = test_7_35_1.Current.Name;
                    test_no = test_name.Substring(5, 13);

                    if (test_no == "7-35, Iter-01")
                    {
                        disable_xvYCC();
                        enable_xvYCC();
                        return;
                    }
                }
            }
            //High Bit rate Audio
            AutomationElement test_7_36_1 = SelectElementNameControlType("Test 7-36, Iter-01\r\nVerify that a High Bitrate Audio capable source is able to transmit High Bitrate Audio\r\nStream Packets with packet jitter limited to compliant values.", ControlType.Text);

            if (test_7_36_1 != null)
            {
                if (test_7_36_1.Current.IsOffscreen == false)
                {

                    test_name = test_7_36_1.Current.Name;
                    test_no = test_name.Substring(5, 13);

                    if (test_no == "7-36, Iter-01")
                    {
                        send_resolution_to_clent("2880x480@60MDS8BPC");
                        dts_hd_hbr_player();
                        return;
                    }
                }
            }

            AutomationElement test_7_39_1 = SelectElementNameControlType("Test 7-39, Iter-01\r\nVerify that Source DUT, whenever transmitting any 4K x 2K video format, complies with\r\nall required pixel and line counts and pixel clock frequency range.\r\n(Requires 4Kx2K capable test equipment)", ControlType.Text);

            if (test_7_39_1 != null)
            {
                if (test_7_39_1.Current.IsOffscreen == false)
                {

                    test_name = test_7_39_1.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-39")
                    {
                        send_resolution_to_clent("3840x2160@30MDS8BPC");
                        return;
                    }
                }
            }

            AutomationElement test_7_39_2 = SelectElementNameControlType("Test 7-39, Iter-02\r\nVerify that Source DUT, whenever transmitting any 4K x 2K video format, complies with\r\nall required pixel and line counts and pixel clock frequency range.\r\n(Requires 4Kx2K capable test equipment)", ControlType.Text);

            if (test_7_39_2 != null)
            {
                if (test_7_39_2.Current.IsOffscreen == false)
                {

                    test_name = test_7_39_2.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-39")
                    {
                        send_resolution_to_clent("3840x2160@25MDS8BPC");
                        return;
                    }
                }
            }

            AutomationElement test_7_39_3 = SelectElementNameControlType("Test 7-39, Iter-03\r\nVerify that Source DUT, whenever transmitting any 4K x 2K video format, complies with\r\nall required pixel and line counts and pixel clock frequency range.\r\n(Requires 4Kx2K capable test equipment)", ControlType.Text);

            if (test_7_39_3 != null)
            {
                if (test_7_39_3.Current.IsOffscreen == false)
                {

                    test_name = test_7_39_3.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-39")
                    {
                        send_resolution_to_clent("3840x2160@24MDS8BPC");
                        return;
                    }
                }
            }

            AutomationElement test_7_39_4 = SelectElementNameControlType("Test 7-39, Iter-04\r\nVerify that Source DUT, whenever transmitting any 4K x 2K video format, complies with\r\nall required pixel and line counts and pixel clock frequency range.\r\n(Requires 4Kx2K capable test equipment)", ControlType.Text);

            if (test_7_39_4 != null)
            {
                if (test_7_39_4.Current.IsOffscreen == false)
                {

                    test_name = test_7_39_4.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-39")
                    {
                        send_resolution_to_clent("3840x2160@24MDS8BPC");
                        return;
                    }
                }
            }

        }

        //7-32 function once completed close hbr app
        private void test_7_32_function()
        {
            string test_name, test_no;

            AutomationElement test_7_32_1 = SelectElementNameControlType("Test 7-32, Iter-01\r\nVerify that the Source transmits audio using permitted layout type.", ControlType.Text);

            if (test_7_32_1 != null)
            {
                if (test_7_32_1.Current.IsOffscreen == false)
                {
                    test_name = test_7_32_1.Current.Name;
                    test_no = test_name.Substring(5, 13);

                    if (test_no == "7-32, Iter-01")
                    {
                        send_resolution_to_clent("1920x1080@60MDS8BPC");
                        System.Threading.Thread.Sleep(1000);

                        channel_2_48khz_24_bit_hbr_player();
                        return;
                    }
                }
            }

            AutomationElement test_7_32_2 = SelectElementNameControlType("Test 7-32, Iter-02\r\nVerify that the Source transmits audio using permitted layout type.", ControlType.Text);
            if (test_7_32_2 != null)
            {
                if (test_7_32_2.Current.IsOffscreen == false)
                {
                    test_name = test_7_32_2.Current.Name;
                    test_no = test_name.Substring(5, 13);

                    if (test_no == "7-32, Iter-02")
                    {
                        send_resolution_to_clent("1920x1080@60MDS8BPC");
                        System.Threading.Thread.Sleep(1000);
                        channel_8_192khz_16_bit_hbr_player();

                        AutomationElement continue_button = SelectElementNameControlType("Continue", ControlType.Button);

                        if (continue_button != null)
                        {
                            Invoke(continue_button);
                            System.Threading.Thread.Sleep(30000);
                            Network_Check();
                            System.Threading.Thread.Sleep(5000);

                            string client_data = "CloseHBR";
                            uint count = 0;
                        exc2: try
                            {
                                count++;
                            
                                Client.Class1 Client1 = new Client.Class1();
                                Client1.Client(CLIENT_ADDRESS.Text, client_data);
                            }

                            catch
                            {
                                if (count <= 4)//Wait until count is greater than 3 times so that manual pop up will appear.
                                {
                                    System.Threading.Thread.Sleep(1000);//Wait for 1 sec
                                    goto exc2;//execute try block once again automatically
                                }

                                else
                                {
                                    //If the client fails 3 times, ask manually
                                    DialogResult result1 = MessageBox.Show("Do you want to retry or cancel?", "Important Note", MessageBoxButtons.RetryCancel);

                                    //If Retry button is pressed, again execute try block 3 times
                                    if (result1 == DialogResult.Retry)
                                    {
                                        count = 0;
                                        goto exc2;
                                    }

                                    else if (result1 == DialogResult.Cancel)
                                    {

                                    }
                                }
                            }
                            System.Threading.Thread.Sleep(1000);

                            ////// Data reciveve 

                            string data_rece;
                            SERVER.Class1 server1 = new SERVER.Class1();
                            data_rece = server1.Server();
                            System.Threading.Thread.Sleep(1000);
                            return;
                        }
                    }
                }
            }
        }
//Test error pop up
        private void test_error_handler()
        {
            AutomationElement test_err = SelectElementNameControlType("Test Error", ControlType.TitleBar);
            System.Threading.Thread.Sleep(1000);
            if (test_err != null)
            {
                if (test_err.Current.IsOffscreen == false)
                {
                    if (error_count >= 3)
                    {
                        AutomationElement fail_and_continue = SelectElementNameControlType("FAIL and Continue", ControlType.Button);
                        Invoke(fail_and_continue);
                        System.Threading.Thread.Sleep(1000);
                        error_count = 0;
                    }

                    else
                    {
                        AutomationElement retry_button = SelectElementNameControlType("Retry    ", ControlType.Button);
                        Invoke(retry_button);
                        System.Threading.Thread.Sleep(1000);
                        error_count++;
                        if (error_count == 3)
                        { 
                            error_count = 0; 
                        }
                        return;
                    }
                }
            }
        }

        //Apply Resolution in the client
        private void send_resolution_to_clent(string res)
        {
            Network_Check(); // Network Check before sending data 
            System.Threading.Thread.Sleep(3000);
            // Data send to server

            string client_data = res;
            uint count = 0;
        exc3: try
            {
                count++;
                Client.Class1 Client1 = new Client.Class1();
                Client1.Client(CLIENT_ADDRESS.Text, client_data);
            }

            catch
            {
                if (count <= 4)//Wait until count is greater than 3 times so that manual pop up will appear.
                {
                    System.Threading.Thread.Sleep(1000);//Wait for 1 sec
                    goto exc3;//execute try block once again automatically
                }

                else
                {
                    //If the client fails 3 times, ask manually
                    DialogResult result1 = MessageBox.Show("Do you want to retry or cancel?", "Important Note", MessageBoxButtons.RetryCancel);

                    //If Retry button is pressed, again execute try block 3 times
                    if (result1 == DialogResult.Retry)
                    {
                        count = 0;
                        goto exc3;
                    }

                    else if (result1 == DialogResult.Cancel)
                    {

                    }
                }
            }

            System.Threading.Thread.Sleep(1000);
            ////// Data reciveve 

            string data_rece;
            SERVER.Class1 server1 = new SERVER.Class1();
            data_rece = server1.Server();
            System.Threading.Thread.Sleep(3000);
        }

        //ycbcr tests
        private void ycbcr_tests()
        {
            AutomationElement dut_config = SelectElementNameControlType("DUT Configuration", ControlType.TitleBar);
            System.Threading.Thread.Sleep(1000);
            if (dut_config != null)
            {
                if (dut_config.Current.IsOffscreen == false)
                {
                    read_test_name_for_enabling_ycbcr();
                    System.Threading.Thread.Sleep(2000);
                    AutomationElement continue_button = SelectElementNameControlType("Continue", ControlType.Button);
                    Invoke(continue_button);
                    System.Threading.Thread.Sleep(1000);
                }
            }
        }

        //Reading test name for enabling ycbcr
        private void read_test_name_for_enabling_ycbcr()
        {
            string test_name, test_no;

            AutomationElement test_7_24_1 = SelectElementNameControlType("Test 7-24, Iter-01\r\nVerify that the Source DUT always outputs pixel encoding that correlates with AVI fields\r\nY0 and Y1 when presented with a YCbCr-capable Sink and that the DUT is capable of\r\nsupporting YCbCr pixel encoding when required.", ControlType.Text);

            if (test_7_24_1 != null)
            {
                if (test_7_24_1.Current.IsOffscreen == false)
                {
                    test_name = test_7_24_1.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-24")
                    {
                        disable_Ycbcr();
                        System.Threading.Thread.Sleep(1000);
                        enable_Ycbcr();
                        return;
                    }
                }
            }

            AutomationElement test_7_24_2 = SelectElementNameControlType("Test 7-24, Iter-02\r\nVerify that the Source DUT always outputs pixel encoding that correlates with AVI fields\r\nY0 and Y1 when presented with a YCbCr-capable Sink and that the DUT is capable of\r\nsupporting YCbCr pixel encoding when required.", ControlType.Text);

            if (test_7_24_2 != null)
            {
                if (test_7_24_2.Current.IsOffscreen == false)
                {
                    test_name = test_7_24_2.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-24")
                    {
                        disable_Ycbcr();
                        System.Threading.Thread.Sleep(1000);
                        enable_Ycbcr();
                        return;
                    }
                }
            }

            AutomationElement test_7_24_3 = SelectElementNameControlType("Test 7-24, Iter-03\r\nVerify that the Source DUT always outputs pixel encoding that correlates with AVI fields\r\nY0 and Y1 when presented with a YCbCr-capable Sink and that the DUT is capable of\r\nsupporting YCbCr pixel encoding when required.", ControlType.Text);

            if (test_7_24_3 != null)
            {
                if (test_7_24_3.Current.IsOffscreen == false)
                {
                    test_name = test_7_24_3.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-24")
                    {
                        disable_Ycbcr();
                        System.Threading.Thread.Sleep(1000);
                        enable_Ycbcr();
                        return;
                    }
                }
            }

            AutomationElement test_7_24_4 = SelectElementNameControlType("Test 7-24, Iter-04\r\nVerify that the Source DUT always outputs pixel encoding that correlates with AVI fields\r\nY0 and Y1 when presented with a YCbCr-capable Sink and that the DUT is capable of\r\nsupporting YCbCr pixel encoding when required.", ControlType.Text);

            if (test_7_24_4 != null)
            {
                if (test_7_24_4.Current.IsOffscreen == false)
                {
                    test_name = test_7_24_4.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-24")
                    {
                        disable_Ycbcr();
                        System.Threading.Thread.Sleep(1000);
                        enable_Ycbcr();
                        return;
                    }
                }
            }

            AutomationElement test_7_24_5 = SelectElementNameControlType("Test 7-24, Iter-05\r\nVerify that the Source DUT always outputs pixel encoding that correlates with AVI fields\r\nY0 and Y1 when presented with a YCbCr-capable Sink and that the DUT is capable of\r\nsupporting YCbCr pixel encoding when required.", ControlType.Text);

            if (test_7_24_5 != null)
            {
                if (test_7_24_5.Current.IsOffscreen == false)
                {
                    test_name = test_7_24_5.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-24")
                    {
                        disable_Ycbcr();
                        System.Threading.Thread.Sleep(1000);
                        enable_Ycbcr();
                        return;
                    }
                }
            }

            AutomationElement test_7_24_6 = SelectElementNameControlType("Test 7-24, Iter-06\r\nVerify that the Source DUT always outputs pixel encoding that correlates with AVI fields\r\nY0 and Y1 when presented with a YCbCr-capable Sink and that the DUT is capable of\r\nsupporting YCbCr pixel encoding when required.", ControlType.Text);

            if (test_7_24_6 != null)
            {
                if (test_7_24_6.Current.IsOffscreen == false)
                {
                    test_name = test_7_24_6.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-24")
                    {
                        disable_Ycbcr();
                        System.Threading.Thread.Sleep(1000);
                        enable_Ycbcr();
                        return;
                    }
                }
            }

            AutomationElement test_7_24_7 = SelectElementNameControlType("Test 7-24, Iter-07\r\nVerify that the Source DUT always outputs pixel encoding that correlates with AVI fields\r\nY0 and Y1 when presented with a YCbCr-capable Sink and that the DUT is capable of\r\nsupporting YCbCr pixel encoding when required.", ControlType.Text);

            if (test_7_24_7 != null)
            {
                if (test_7_24_7.Current.IsOffscreen == false)
                {
                    test_name = test_7_24_7.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-24")
                    {
                        disable_Ycbcr();
                        System.Threading.Thread.Sleep(1000);
                        enable_Ycbcr();
                        return;
                    }
                }
            }


            AutomationElement test_7_24_8 = SelectElementNameControlType("Test 7-24, Iter-08\r\nVerify that the Source DUT always outputs pixel encoding that correlates with AVI fields\r\nY0 and Y1 when presented with a YCbCr-capable Sink and that the DUT is capable of\r\nsupporting YCbCr pixel encoding when required.", ControlType.Text);

            if (test_7_24_8 != null)
            {
                if (test_7_24_8.Current.IsOffscreen == false)
                {
                    test_name = test_7_24_8.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-24")
                    {
                        disable_Ycbcr();
                        System.Threading.Thread.Sleep(1000);
                        enable_Ycbcr();
                        return;
                    }
                }
            }


            AutomationElement test_7_24_9 = SelectElementNameControlType("Test 7-24, Iter-09\r\nVerify that the Source DUT always outputs pixel encoding that correlates with AVI fields\r\nY0 and Y1 when presented with a YCbCr-capable Sink and that the DUT is capable of\r\nsupporting YCbCr pixel encoding when required.", ControlType.Text);

            if (test_7_24_9 != null)
            {
                if (test_7_24_9.Current.IsOffscreen == false)
                {
                    test_name = test_7_24_9.Current.Name;
                    test_no = test_name.Substring(5, 4);

                    if (test_no == "7-24")
                    {
                        disable_Ycbcr();
                        System.Threading.Thread.Sleep(1000);
                        enable_Ycbcr();
                        return;
                    }
                }
            }
        }
        //Enabling ycbcr in client
        private void enable_Ycbcr()
        {
            Network_Check();
            System.Threading.Thread.Sleep(5000);

            string client_data = "Enable_YCbCr";
            uint count = 0;
        exc4: try
            {
                count++;
                Client.Class1 Client1 = new Client.Class1();
                Client1.Client(CLIENT_ADDRESS.Text, client_data);
            }

            catch
            {
                if (count <= 4)//Wait until count is greater than 3 times so that manual pop up will appear.
                {
                    System.Threading.Thread.Sleep(1000);//Wait for 1 sec
                    goto exc4;//execute try block once again automatically
                }

                else
                {
                    //If the client fails 3 times, ask manually
                    DialogResult result1 = MessageBox.Show("Do you want to retry or cancel?", "Important Note", MessageBoxButtons.RetryCancel);

                    //If Retry button is pressed, again execute try block 3 times
                    if (result1 == DialogResult.Retry)
                    {
                        count = 0;
                        goto exc4;
                    }

                    else if (result1 == DialogResult.Cancel)
                    {

                    }
                }
            }
            System.Threading.Thread.Sleep(1000);

            ////// Data reciveve 

            string data_rece;
            SERVER.Class1 server1 = new SERVER.Class1();
            data_rece = server1.Server();

            System.Threading.Thread.Sleep(1000);
        }

        private void disable_xvYCC()
        {
            Network_Check();
            System.Threading.Thread.Sleep(5000);

            string client_data = "CloseHBR";
            uint count = 0;
        exc5: try
            {
                count++;
                Client.Class1 Client1 = new Client.Class1();
                Client1.Client(CLIENT_ADDRESS.Text, client_data);
            }

            catch
            {
                if (count <= 4)//Wait until count is greater than 3 times so that manual pop up will appear.
                {
                    System.Threading.Thread.Sleep(1000);//Wait for 1 sec
                    goto exc5;//execute try block once again automatically
                }

                else
                {
                    //If the client fails 3 times, ask manually
                    DialogResult result1 = MessageBox.Show("Do you want to retry or cancel?", "Important Note", MessageBoxButtons.RetryCancel);

                    //If Retry button is pressed, again execute try block 3 times
                    if (result1 == DialogResult.Retry)
                    {
                        count = 0;
                        goto exc5;
                    }

                    else if (result1 == DialogResult.Cancel)
                    {

                    }
                }
            }

            System.Threading.Thread.Sleep(1000);

            ////// Data reciveve 

            string data_rece;
            SERVER.Class1 server1 = new SERVER.Class1();
            data_rece = server1.Server();

            System.Threading.Thread.Sleep(1000);

            Network_Check();
            System.Threading.Thread.Sleep(5000);

            client_data = "Disable_xvYcc";
            count = 0;
        exc6: try
            {
                count++;
                Client.Class1 Client1 = new Client.Class1();
                Client1.Client(CLIENT_ADDRESS.Text, client_data);
            }

            catch
            {
                if (count <= 4)//Wait until count is greater than 3 times so that manual pop up will appear.
                {
                    System.Threading.Thread.Sleep(1000);//Wait for 1 sec
                    goto exc6;//execute try block once again automatically
                }

                else
                {
                    //If the client fails 3 times, ask manually
                    DialogResult result1 = MessageBox.Show("Do you want to retry or cancel?", "Important Note", MessageBoxButtons.RetryCancel);

                    //If Retry button is pressed, again execute try block 3 times
                    if (result1 == DialogResult.Retry)
                    {
                        count = 0;
                        goto exc6;
                    }

                    else if (result1 == DialogResult.Cancel)
                    {

                    }
                }
            }
            System.Threading.Thread.Sleep(1000);

            ////// Data reciveve 

            server1 = new SERVER.Class1();
            data_rece = server1.Server();

            System.Threading.Thread.Sleep(1000);
        }

        //disable ycbcr
        private void disable_Ycbcr()
        {
            Network_Check();
            System.Threading.Thread.Sleep(5000);

            string client_data = "Disable_YCbCr";
            uint count = 0;
        exc7: try
            {
                count++;
                Client.Class1 Client1 = new Client.Class1();
                Client1.Client(CLIENT_ADDRESS.Text, client_data);
            }

            catch
            {
                if (count <= 4)//Wait until count is greater than 3 times so that manual pop up will appear.
                {
                    System.Threading.Thread.Sleep(1000);//Wait for 1 sec
                    goto exc7;//execute try block once again automatically
                }

                else
                {
                    //If the client fails 3 times, ask manually
                    DialogResult result1 = MessageBox.Show("Do you want to retry or cancel?", "Important Note", MessageBoxButtons.RetryCancel);

                    //If Retry button is pressed, again execute try block 3 times
                    if (result1 == DialogResult.Retry)
                    {
                        count = 0;
                        goto exc7;
                    }

                    else if (result1 == DialogResult.Cancel)
                    {

                    }
                }
            }
            System.Threading.Thread.Sleep(1000);

            ////// Data reciveve 

            string data_rece;
            SERVER.Class1 server1 = new SERVER.Class1();
            data_rece = server1.Server();

            System.Threading.Thread.Sleep(1000);
        }

        //enable xvycc
        private void enable_xvYCC()
        {
            Network_Check();
            System.Threading.Thread.Sleep(5000);

            string client_data = "Enable_xvYcc";
            uint count = 0;
        exc8: try
            {
                count++;
                Client.Class1 Client1 = new Client.Class1();
                Client1.Client(CLIENT_ADDRESS.Text, client_data);
            }

            catch
            {
                if (count <= 4)//Wait until count is greater than 3 times so that manual pop up will appear.
                {
                    System.Threading.Thread.Sleep(1000);//Wait for 1 sec
                    goto exc8;//execute try block once again automatically
                }

                else
                {
                    //If the client fails 3 times, ask manually
                    DialogResult result1 = MessageBox.Show("Do you want to retry or cancel?", "Important Note", MessageBoxButtons.RetryCancel);

                    //If Retry button is pressed, again execute try block 3 times
                    if (result1 == DialogResult.Retry)
                    {
                        count = 0;
                        goto exc8;
                    }

                    else if (result1 == DialogResult.Cancel)
                    {

                    }
                }
            }

            System.Threading.Thread.Sleep(1000);

            ////// Data reciveve 

            string data_rece;
            SERVER.Class1 server1 = new SERVER.Class1();
            data_rece = server1.Server();

            System.Threading.Thread.Sleep(1000);

        }

        //enable deep color
        private void enable_deep_color()
        {
            Network_Check();
            System.Threading.Thread.Sleep(5000);

            string client_data = "CloseHBR";
            uint count = 0;
        exc9: try
            {
                count++;
                Client.Class1 Client1 = new Client.Class1();
                Client1.Client(CLIENT_ADDRESS.Text, client_data);
            }

            catch
            {
                if (count <= 4)//Wait until count is greater than 3 times so that manual pop up will appear.
                {
                    System.Threading.Thread.Sleep(1000);//Wait for 1 sec
                    goto exc9;//execute try block once again automatically
                }

                else
                {
                    //If the client fails 3 times, ask manually
                    DialogResult result1 = MessageBox.Show("Do you want to retry or cancel?", "Important Note", MessageBoxButtons.RetryCancel);

                    //If Retry button is pressed, again execute try block 3 times
                    if (result1 == DialogResult.Retry)
                    {
                        count = 0;
                        goto exc9;
                    }

                    else if (result1 == DialogResult.Cancel)
                    {

                    }
                }
            }

            System.Threading.Thread.Sleep(1000);

            ////// Data reciveve 

            string data_rece;
            SERVER.Class1 server1 = new SERVER.Class1();
            data_rece = server1.Server();

            System.Threading.Thread.Sleep(1000);

            Network_Check();
            System.Threading.Thread.Sleep(5000);

            client_data = "DeepColor";
            count = 0;
        exc10: try
            {
                count++;
                Client.Class1 Client1 = new Client.Class1();
                Client1.Client(CLIENT_ADDRESS.Text, client_data);
            }

            catch
            {
                if (count <= 4)//Wait until count is greater than 3 times so that manual pop up will appear.
                {
                    System.Threading.Thread.Sleep(1000);//Wait for 1 sec
                    goto exc10;//execute try block once again automatically
                }

                else
                {
                    //If the client fails 3 times, ask manually
                    DialogResult result1 = MessageBox.Show("Do you want to retry or cancel?", "Important Note", MessageBoxButtons.RetryCancel);

                    //If Retry button is pressed, again execute try block 3 times
                    if (result1 == DialogResult.Retry)
                    {
                        count = 0;
                        goto exc10;
                    }

                    else if (result1 == DialogResult.Cancel)
                    {

                    }
                }
            }

            System.Threading.Thread.Sleep(1000);

            ////// Data reciveve 

            server1 = new SERVER.Class1();
            data_rece = server1.Server();

            System.Threading.Thread.Sleep(1000);
        }

        //2 channel 48khz audio
        private void channel_2_48khz_24_bit_hbr_player()
        {
            Network_Check();
            System.Threading.Thread.Sleep(5000);

            string client_data = "2_Channel_48000Hz_24bits_20s.wav";
            uint count = 0;
        exc11: try
            {
                count++;
                Client.Class1 Client1 = new Client.Class1();
                Client1.Client(CLIENT_ADDRESS.Text, client_data);
            }

            catch
            {
                if (count <= 4)//Wait until count is greater than 3 times so that manual pop up will appear.
                {
                    System.Threading.Thread.Sleep(1000);//Wait for 1 sec
                    goto exc11;//execute try block once again automatically
                }

                else
                {
                    //If the client fails 3 times, ask manually
                    DialogResult result1 = MessageBox.Show("Do you want to retry or cancel?", "Important Note", MessageBoxButtons.RetryCancel);

                    //If Retry button is pressed, again execute try block 3 times
                    if (result1 == DialogResult.Retry)
                    {
                        count = 0;
                        goto exc11;
                    }

                    else if (result1 == DialogResult.Cancel)
                    {

                    }
                }
            }
            System.Threading.Thread.Sleep(1000);

            ////// Data reciveve 

            string data_rece;
            SERVER.Class1 server1 = new SERVER.Class1();
            data_rece = server1.Server();

            System.Threading.Thread.Sleep(1000);

        }
        //8 channel 192 khz audio
        private void channel_8_192khz_16_bit_hbr_player()
        {
            Network_Check();
            System.Threading.Thread.Sleep(5000);

            string client_data = "Sine_SevenPointOneSurround_192000Hz_16bits_20s.wav";
            uint count = 0;
        exc12: try
            {
                count++;
                Client.Class1 Client1 = new Client.Class1();
                Client1.Client(CLIENT_ADDRESS.Text, client_data);
            }

            catch
            {
                if (count <= 4)//Wait until count is greater than 3 times so that manual pop up will appear.
                {
                    System.Threading.Thread.Sleep(1000);//Wait for 1 sec
                    goto exc12;//execute try block once again automatically
                }

                else
                {
                    //If the client fails 3 times, ask manually
                    DialogResult result1 = MessageBox.Show("Do you want to retry or cancel?", "Important Note", MessageBoxButtons.RetryCancel);

                    //If Retry button is pressed, again execute try block 3 times
                    if (result1 == DialogResult.Retry)
                    {
                        count = 0;
                        goto exc12;
                    }

                    else if (result1 == DialogResult.Cancel)
                    {

                    }
                }
            }
            System.Threading.Thread.Sleep(1000);

            ////// Data reciveve 

            string data_rece;
            SERVER.Class1 server1 = new SERVER.Class1();
            data_rece = server1.Server();
            System.Threading.Thread.Sleep(1000);

        }
//8 channel 48khz audio
        private void channel_8_48khz_16_bit_hbr_player()
        {
            Network_Check();
            System.Threading.Thread.Sleep(5000);

            string client_data = "Sine_SevenPointOneSurround_48000Hz_16bits_20s.wav";
            uint count = 0;
        exc13: try
            {
                count++;
                Client.Class1 Client1 = new Client.Class1();
                Client1.Client(CLIENT_ADDRESS.Text, client_data);
            }

            catch
            {
                if (count <= 4)//Wait until count is greater than 3 times so that manual pop up will appear.
                {
                    System.Threading.Thread.Sleep(1000);//Wait for 1 sec
                    goto exc13;//execute try block once again automatically
                }

                else
                {
                    //If the client fails 3 times, ask manually
                    DialogResult result1 = MessageBox.Show("Do you want to retry or cancel?", "Important Note", MessageBoxButtons.RetryCancel);

                    //If Retry button is pressed, again execute try block 3 times
                    if (result1 == DialogResult.Retry)
                    {
                        count = 0;
                        goto exc13;
                    }

                    else if (result1 == DialogResult.Cancel)
                    {

                    }
                }
            }

            System.Threading.Thread.Sleep(1000);

            ////// Data reciveve 

            string data_rece;
            SERVER.Class1 server1 = new SERVER.Class1();
            data_rece = server1.Server();

            System.Threading.Thread.Sleep(1000);

        }

        //dts-hd-hbr-player
        private void dts_hd_hbr_player()
        {
            Network_Check();
            System.Threading.Thread.Sleep(5000);

            string client_data = "Tone_71_BDMA.dtshd";
            uint count = 0;
        exc14: try
            {
                count++;
                Client.Class1 Client1 = new Client.Class1();
                Client1.Client(CLIENT_ADDRESS.Text, client_data);
            }

            catch
            {
                if (count <= 4)//Wait until count is greater than 3 times so that manual pop up will appear.
                {
                    System.Threading.Thread.Sleep(1000);//Wait for 1 sec
                    goto exc14;//execute try block once again automatically
                }

                else
                {
                    //If the client fails 3 times, ask manually
                    DialogResult result1 = MessageBox.Show("Do you want to retry or cancel?", "Important Note", MessageBoxButtons.RetryCancel);

                    //If Retry button is pressed, again execute try block 3 times
                    if (result1 == DialogResult.Retry)
                    {
                        count = 0;
                        goto exc14;
                    }

                    else if (result1 == DialogResult.Cancel)
                    {

                    }
                }
            }

            System.Threading.Thread.Sleep(1000);

            ////// Data reciveve 

            string data_rece;
            SERVER.Class1 server1 = new SERVER.Class1();
            data_rece = server1.Server();

            System.Threading.Thread.Sleep(1000);

        }

        private void QD_App_close()//Close QD Application not working
        {
            Process myProcess = new Process();
            foreach (var process in Process.GetProcessesByName("980mgr"))
            {
                process.Kill();

            }
        }

        private void audio_channel_select_handler(String test)
        {
            /////////////8 channel
            if (test == "7-30, Iter-04" || test == "7-30, Iter-08" || test == "7-30, Iter-09")
            {
                System.Windows.Forms.SendKeys.SendWait("{TAB}");
                System.Threading.Thread.Sleep(1000);

                System.Windows.Forms.SendKeys.SendWait("{DOWN}");
                System.Threading.Thread.Sleep(1000);

                System.Windows.Forms.SendKeys.SendWait("{TAB}");
                System.Threading.Thread.Sleep(1000);

                System.Windows.Forms.SendKeys.SendWait("{DOWN 4}");
                System.Threading.Thread.Sleep(1000);

                channel_8_192khz_16_bit_hbr_player();
                System.Threading.Thread.Sleep(1000);


                AutomationElement man_cont_button = SelectElementNameControlType("Continue   ", ControlType.Button);
                Invoke(man_cont_button);
            }
            ///////////// 2 channel
            else if (test == "7-30, Iter-03" || test == "7-30, Iter-06" || test == "7-30, Iter-07" || test == "7-30, Iter-10" || test == "7-30, Iter-05")
            {
                System.Windows.Forms.SendKeys.SendWait("{TAB}");
                System.Threading.Thread.Sleep(1000);


                channel_2_48khz_24_bit_hbr_player();

                AutomationElement man_cont_button = SelectElementNameControlType("Continue   ", ControlType.Button);
                Invoke(man_cont_button);
            }

        }

        private void close_test_handler()
        {
            AutomationElement close_test = SelectElementNameControlType("Close Window", ControlType.Button);


            System.Threading.Thread.Sleep(1000);
       //     close_test.SetFocus();
            System.Threading.Thread.Sleep(1000);
            Invoke(close_test);

            System.Threading.Thread.Sleep(5000);

            AutomationElement Result_HTML = SelectElementNameControlType("HTML Report", ControlType.Button);
            //Result_HTML.SetFocus();

            Invoke(Result_HTML);
            System.Threading.Thread.Sleep(1000);

            System.Windows.Forms.SendKeys.SendWait("{ENTER}");



            Network_Check();
            System.Threading.Thread.Sleep(4000);

            string client_data = "CloseAllApps";
            uint count = 0;
        exc15: try
            {
                count++;
                Client.Class1 Client1 = new Client.Class1();
                Client1.Client(CLIENT_ADDRESS.Text, client_data);
            }

            catch
            {
                if (count <= 4)//Wait until count is greater than 3 times so that manual pop up will appear.
                {
                    System.Threading.Thread.Sleep(1000);//Wait for 1 sec
                    goto exc15;//execute try block once again automatically
                }

                else
                {
                    //If the client fails 3 times, ask manually
                    DialogResult result1 = MessageBox.Show("Do you want to retry or cancel?", "Important Note", MessageBoxButtons.RetryCancel);

                    //If Retry button is pressed, again execute try block 3 times
                    if (result1 == DialogResult.Retry)
                    {
                        count = 0;
                        goto exc15;
                    }

                    else if (result1 == DialogResult.Cancel)
                    {

                    }
                }
            }
            System.Threading.Thread.Sleep(1000);
            ////// Data reciveve 

            string data_rece;
            SERVER.Class1 server1 = new SERVER.Class1();
            data_rece = server1.Server();

            System.Threading.Thread.Sleep(1000);




        }


        private void groupBox1_Enter(object sender, EventArgs e)
        {
           
        }

/// <summary>
/// //////////Invoke Functions
/// </summary>
/// <param name="element"></param>
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


        /// <summary>
        /// ////////
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void checkBox1_CheckedChanged(object sender, EventArgs e)
        {
            if (checkBox1.Checked == true)
            {
                checkBox2.Checked = false;
                checkBox3.Checked = false;
                checkBox4.Checked = false;
                checkBox5.Checked = false;
                
                if(checkBox7.Checked == true || checkBox8.Checked == true)
                {
                    START_Button.Enabled = true;
                }

                else
                {
                    START_Button.Enabled = false;
                }
            }

            else
            {
                Version.Enabled = false;

                if ((checkBox7.Checked == false && checkBox8.Checked == false) || (checkBox1.Checked == false && checkBox2.Checked == false && checkBox3.Checked == false && checkBox4.Checked == false && checkBox5.Checked == false ))
                {
                    START_Button.Enabled = false;
                }
            }
        }

   
        private void checkBox2_CheckedChanged(object sender, EventArgs e)
        {
            if(checkBox2.Checked == true)
            {
                checkBox1.Checked = false;
                checkBox3.Checked = false;
                checkBox4.Checked = false;
                checkBox5.Checked = false;
                
                if (checkBox7.Checked == true || checkBox8.Checked == true)
                {
                    START_Button.Enabled = true;
                }

                else
                {
                    START_Button.Enabled = false;
                }
            }

            else
            {
                Version.Enabled = false;

                if ((checkBox7.Checked == false && checkBox8.Checked == false) || (checkBox1.Checked == false && checkBox2.Checked == false && checkBox3.Checked == false && checkBox4.Checked == false && checkBox5.Checked == false ))
                {
                    START_Button.Enabled = false;
                }
            }

        }

        private void checkBox3_CheckedChanged(object sender, EventArgs e)
        {
            if(checkBox3.Checked == true)
            {
                checkBox1.Checked = false;
                checkBox2.Checked = false;
                checkBox4.Checked = false;
                checkBox5.Checked = false;
                

                if (checkBox7.Checked == true || checkBox8.Checked == true)
                {
                    START_Button.Enabled = true;
                }

                else
                {
                    START_Button.Enabled = false;
                }
            }

            else
            {
                Version.Enabled = false;

                if ((checkBox7.Checked == false && checkBox8.Checked == false) || (checkBox1.Checked == false && checkBox2.Checked == false && checkBox3.Checked == false && checkBox4.Checked == false && checkBox5.Checked == false ))
                {
                    START_Button.Enabled = false;
                }
            }
        }

        private void checkBox4_CheckedChanged(object sender, EventArgs e)
        {
            if(checkBox4.Checked == true)
            {
                checkBox1.Checked = false;
                checkBox2.Checked = false;
                checkBox3.Checked = false;
                checkBox5.Checked = false;
               

                if (checkBox7.Checked == true || checkBox8.Checked == true)
                {
                    START_Button.Enabled = true;
                }

                else
                {
                    START_Button.Enabled = false;
                }

            }

            else
            {
                Version.Enabled = false;

                if ((checkBox7.Checked == false && checkBox8.Checked == false) || (checkBox1.Checked == false && checkBox2.Checked == false && checkBox3.Checked == false && checkBox4.Checked == false && checkBox5.Checked == false ))
                {
                    START_Button.Enabled = false;
                }
            }
        }

        private void checkBox5_CheckedChanged(object sender, EventArgs e)
        {
            if(checkBox5.Checked == true)
            {
                checkBox1.Checked = false;
                checkBox2.Checked = false;
                checkBox3.Checked = false;
                checkBox4.Checked = false;
                

                if (checkBox7.Checked == true || checkBox8.Checked == true)
                {
                    START_Button.Enabled = true;
                }

                else
                {
                    START_Button.Enabled = false;
                }
            }
            else
            {
                Version.Enabled = false;

                if ((checkBox7.Checked == false && checkBox8.Checked == false) || (checkBox1.Checked == false && checkBox2.Checked == false && checkBox3.Checked == false && checkBox4.Checked == false && checkBox5.Checked == false ))
                {
                    START_Button.Enabled = false;
                }
            }
        }

        private void label1_Click(object sender, EventArgs e)
        {

        }

        private void IP_ADDRESS_TextChanged(object sender, EventArgs e)
        {

        }

        private void label2_Click(object sender, EventArgs e)
        {

        }

        
        private void initialize_ed()
        {

            Network_Check();
            System.Threading.Thread.Sleep(5000);

            string client_data = "1920x1080@60MDS8BPC";
            Client.Class1 Client1 = new Client.Class1();

            Client1.Client(CLIENT_ADDRESS.Text, client_data);


            System.Threading.Thread.Sleep(1000);
            ////// Data reciveve 

            string data_rece;
            SERVER.Class1 server1 = new SERVER.Class1();
            data_rece = server1.Server();

            System.Threading.Thread.Sleep(1000);

        }

        private void textBox1_TextChanged(object sender, EventArgs e)
        {

        }

        private void textBox2_TextChanged(object sender, EventArgs e)
        {

        }

       
        private void checkBox8_CheckedChanged(object sender, EventArgs e)
        {

            if(checkBox8.Checked == true)
            {
                checkBox7.Checked = false;
                Version.Enabled = true;

                if(checkBox1.Checked == true || checkBox2.Checked == true || checkBox3.Checked == true || checkBox4.Checked == true || checkBox5.Checked == true )
                {           
                    START_Button.Enabled = true;
                }

                else
                {
                    START_Button.Enabled = false;
                }
            }

            else
            {
                Version.Enabled = false;

                if ((checkBox1.Checked == false && checkBox2.Checked == false && checkBox3.Checked == false && checkBox4.Checked == false && checkBox5.Checked == false ) || (checkBox7.Checked == false && checkBox8.Checked == false))
                {
                    START_Button.Enabled = false;
                }
            }
        }

        private void groupBox3_Enter(object sender, EventArgs e)
        {
           
        }

        private void checkBox7_CheckedChanged(object sender, EventArgs e)
        {
            if(checkBox7.Checked == true)
            {
                checkBox8.Checked = false;
                Version.Enabled = false;

                if (checkBox1.Checked == true || checkBox2.Checked == true || checkBox3.Checked == true || checkBox4.Checked == true || checkBox5.Checked == true )
                {
                    START_Button.Enabled = true;
                }

                else
                {
                    START_Button.Enabled = false;
                }

            }

            else
            {
                Version.Enabled = false;

                if ((checkBox1.Checked == false && checkBox2.Checked == false && checkBox3.Checked == false && checkBox4.Checked == false && checkBox5.Checked == false ) || (checkBox7.Checked == false && checkBox8.Checked == false))
                {
                    START_Button.Enabled = false;
                }
            }

        }


    }

}
        