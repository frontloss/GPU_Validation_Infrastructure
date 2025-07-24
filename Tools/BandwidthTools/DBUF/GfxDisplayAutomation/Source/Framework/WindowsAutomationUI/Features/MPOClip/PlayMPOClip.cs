namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.Windows.Automation;
    using System.Threading;
    using System.IO;
    using System.Timers;
    using System.Runtime.InteropServices;
    using System.Windows.Forms;
    using System.Diagnostics;

    public class PlayMPOClip : FunctionalBase, ISetMethod
    {
        [DllImport("user32.dll", SetLastError = true, CallingConvention = CallingConvention.StdCall)]
        private static extern bool SetForegroundWindow(IntPtr hWnd);
        [DllImport("user32.dll", SetLastError = true, CallingConvention = CallingConvention.StdCall)]
        static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);

        private static List<ControlParams> _elementSequence; 
        private List<KeyCode> listKeyCode = new List<KeyCode>();
        KeyPress keyPress = new KeyPress();
        const int FORCE_MINIMIZE = 11;
        const int SW_RESTORE = 9;
        public bool SetMethod(object argMessage)
        {
            _elementSequence  = new List<ControlParams>();
            UIABaseHandler uiaBaseHandler = new UIABaseHandler();
            string clipName = argMessage as string;
            clipName = GetFileNameAsInWindow(clipName);
            Log.Verbose("Playing Clip {0}", clipName);

            _elementSequence.Add(new ControlParams() { ControlType = ControlType.ListItem, Name = clipName, ClickStatus = false });
            _elementSequence.Add(new ControlParams() { ControlType = ControlType.MenuItem, Name = "Open with", ClickStatus = false });

            if (base.MachineInfo.OS.Type == OSType.WINTHRESHOLD)
            {
                _elementSequence.Add(new ControlParams() { ControlType = ControlType.MenuItem, Name = "Movies & TV", ClickStatus = false });
                _elementSequence.Add(new ControlParams() { ControlType = ControlType.Button, Name = "Full Screen", ClickStatus = false });
            }
            else if (base.MachineInfo.OS.Type == OSType.WIN7)
            {
                _elementSequence.Add(new ControlParams() { ControlType = ControlType.MenuItem, Name = "Windows Media Player", ClickStatus = false });
                _elementSequence.Add(new ControlParams() { ControlType = ControlType.RadioButton, Name = "Recommended settings", ClickStatus = false });
                _elementSequence.Add(new ControlParams() { ControlType = ControlType.Button, Name = "Finish", ClickStatus = false });
            }
            else
            {
                _elementSequence.Add(new ControlParams() { ControlType = ControlType.MenuItem, Name = "Video", ClickStatus = false });
            }
            AutomationElement rootElement = AutomationElement.RootElement;
            Condition regCondition = null;
            AutomationElement appElement = null;

            foreach (ControlParams cP in _elementSequence)
            {
                regCondition = new PropertyCondition(AutomationElement.NameProperty, cP.Name);
                appElement = rootElement.FindFirst(TreeScope.Descendants, regCondition);
                if (appElement != null && ((bool)appElement.GetCurrentPropertyValue(AutomationElement.IsEnabledProperty, true)))
                {
                    if (appElement.Current.ControlType.Equals(ControlType.ListItem))
                    {
                        Log.Verbose("Selecting {0} ", appElement.Current.Name);
                        SelectionItemPattern rpa = appElement.GetCurrentPattern(SelectionItemPattern.Pattern) as SelectionItemPattern;
                        if (rpa == null)
                            Log.Verbose("Unable to get handle for the ListItem:{0}", appElement.Current.Name);
                        rpa.Select();
                        Thread.Sleep(3000);
                        if (cP.Name.Equals(clipName))
                        {
                            SendKeys.SendWait("+{F10}");
                            Thread.Sleep(3000);
                            cP.ClickStatus = true;
                        }
                    }

                    if (appElement.Current.ControlType.Equals(ControlType.MenuItem))
                    {
                        AutomationElement element = UIABaseHandler.SelectElementNameControlType(cP.Name, ControlType.MenuItem);
                        if (element != null)
                        {
                            Log.Verbose("element name is {0}", element.Current.Name);
                            uiaBaseHandler.SendKey(element);
                            Thread.Sleep(2000);
                            cP.ClickStatus = true;                           
                        }
                    }

                    if (appElement.Current.ControlType.Equals(ControlType.RadioButton) && base.MachineInfo.OS.Type == OSType.WIN7)
                    {
                        AutomationElement element = UIABaseHandler.SelectElementNameControlType(cP.Name, ControlType.RadioButton);
                        if (element != null)
                        {
                            Log.Verbose("element name is {0}", element.Current.Name);
                            uiaBaseHandler.SendKey(element);
                            Thread.Sleep(2000);
                            cP.ClickStatus = true;
                        }
                    }
                    if ((appElement.Current.ControlType.Equals(ControlType.Button)) && (base.MachineInfo.OS.Type == OSType.WINTHRESHOLD || base.MachineInfo.OS.Type == OSType.WIN7))
                    {
                        AutomationElement element = UIABaseHandler.SelectElementNameControlType(cP.Name, ControlType.Button);
                        if (element != null)
                        {
                            Log.Verbose("element name is {0}", element.Current.Name);
                            uiaBaseHandler.Invoke(element);
                            cP.ClickStatus = true;
                        }
                    }
                }               
            }            
            foreach (ControlParams cP in _elementSequence)
            {
                if (cP.ClickStatus == false)
                    return false;
            }

            return true;
        }
        private string GetFileNameAsInWindow(string fileName)
        {
            string returnFileName;
            ControlParams cp = new ControlParams() { ControlType = ControlType.ListItem, Name = fileName, ClickStatus = false };
            AutomationElement rootElement = AutomationElement.RootElement;
            Condition regCondition = null;
            AutomationElement appElement = null;
            
            var process = System.Diagnostics.Process.GetProcessesByName("explorer").FirstOrDefault();
            if ((process != null) && (process.MainWindowHandle != IntPtr.Zero))
                ForceForegroundWindow(process.MainWindowHandle);
           
            regCondition = new PropertyCondition(AutomationElement.NameProperty, cp.Name);
            appElement = rootElement.FindFirst(TreeScope.Descendants, regCondition);

            if (appElement != null && ((bool)appElement.GetCurrentPropertyValue(AutomationElement.IsEnabledProperty, true)))
                returnFileName = fileName;
            else
                returnFileName = Path.GetFileNameWithoutExtension(fileName);
            return returnFileName;
        }
        private static void ForceForegroundWindow(IntPtr hWnd)
        {            
            List<Process> RunningProcesses = Process.GetProcesses().Where(p => p.ProcessName.Equals("cmd")).ToList();
            RunningProcesses.ForEach(p => ShowWindow(p.MainWindowHandle, FORCE_MINIMIZE));

            SetForegroundWindow(hWnd);

            RunningProcesses.ForEach(p =>
            {
                if (p.HasExited != true)
                    ShowWindow(p.MainWindowHandle, SW_RESTORE);
            });
        }
        
    }
}
