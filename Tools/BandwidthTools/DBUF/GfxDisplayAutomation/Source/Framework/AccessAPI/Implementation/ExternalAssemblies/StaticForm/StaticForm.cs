namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Text;
    using System.Linq;
    using System.Threading;
    using System.Diagnostics;
    using System.Xml.Serialization;
    using System.IO;
    using System.Collections.Generic;
    using System.Runtime.InteropServices;
    using Microsoft.Win32;
    using System.Windows.Automation;
    using System.Windows.Forms;
    using System.Drawing;

    internal class StaticForm : FunctionalBase, ISetMethod, IParse
    {
        private const int SW_HIDE = 0;
        private const int SW_SHOW = 1;
         private const int SM_CXSCREEN = 0;
	    private const int SM_CYSCREEN = 1;
        private const int WM_CLOSE = 0x0010;

         [DllImport("user32.dll", EntryPoint = "GetSystemMetrics")]
        public static extern int GetSystemMetrics(int which);

         [DllImport("user32.dll", SetLastError = true, CallingConvention = CallingConvention.Cdecl)]
         public static extern void SwitchToThisWindow(IntPtr handle, bool keys);

         public bool SetMethod(object argMessage)
         {
             bool status = true;
             StaticFormArgs desktopArgs = argMessage as StaticFormArgs;
             Log.Message(true, "Setting desktop to {0}", desktopArgs.ShowForm);

             if (desktopArgs.ShowForm == true)
             {
                 Size size = new Size();
                 int formPosition = 0;
                 Screen[] screens = Screen.AllScreens;
                 //Initialize Size object for form
                 size.Width = screens[0].Bounds.Width;
                 size.Height = screens[0].Bounds.Height;

                 if (desktopArgs.currentConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Extended)
                 {
                     int displayHierarchy = (int)desktopArgs.currentConfig.GetDispHierarchy(desktopArgs.displayType);

                     for (int i = 0; i < displayHierarchy; i++)
                         formPosition += screens[i].Bounds.Width;

                     size.Width = screens[displayHierarchy].Bounds.Width;
                     size.Height = screens[displayHierarchy].Bounds.Height;
                 }
                 
                 //Launch Image through windows form
                 Form1 f1 = new Form1();

                 //Update the form's size and location for computing CRC
                 f1.MonitorSize = size;
                 f1.FormLocation = new Point(formPosition + 1, 0);

                 f1.PrintMonitorSize();

                 f1.SetLostFocus(false);

                 /* This is done to avoid the form window to hang.
           This code snippet will execute all the queued events in the process*/
                 for (int i = 1; i <= 10000; i++)
                 {
                     System.Windows.Forms.Application.DoEvents();
                 }

                 Thread.Sleep(1000);
                 f1.Show();

                 //Bring form to top
                 f1.Focus();
                 SwitchToThisWindow(f1.Handle, false);
             }
             else if (desktopArgs.ShowForm == false)
             {
                 IntPtr sf = Interop.FindWindow(null, "StaticForm");
                 if (sf != IntPtr.Zero)
                 {
                     Interop.SendMessage(sf, WM_CLOSE, IntPtr.Zero, IntPtr.Zero);
                 }
                 else
                 {
                     status = false;
                 }
             }
             return status;
         }
            
        public void Parse(string[] args)
        {
            StaticFormArgs staticFormArgs = new StaticFormArgs(true);

            if (args.Length == 2 && args[0].ToLower().Contains("set"))
            {
                staticFormArgs.ShowForm = Convert.ToBoolean(args[1]);
                
                SetMethod(staticFormArgs);

                staticFormArgs.ShowForm = false;
                SetMethod(staticFormArgs);
            }
            else
                this.HelpText();
        }

        private void HelpText()
        {
            StringBuilder sb = new StringBuilder();
            sb.Append("..\\>Problem with Commandline Parameters. \n Please type : Execute.exe StaticForm set true").Append(Environment.NewLine);
            sb.Append("For example : Execute.exe StaticForm set true");
            Log.Message(sb.ToString());
        }
    }
}