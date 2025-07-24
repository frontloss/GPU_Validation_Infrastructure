namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.Diagnostics;
    using System.Threading;
    using System.Windows.Automation;
    using System.Xml;

    internal static class AddWirelessDisplay
    {
        private static string hostReceverID = null;
        public static bool ScanNAddWirelessDisplayDevice()
        {
            GetReceverID();
            if (string.IsNullOrEmpty(hostReceverID))
            {
                Log.Verbose("could not find recever for host {0}, please modify widiData.map file", Environment.MachineName);
                return false;
            }
            if (!ScanNValidateDevice())
                Log.Message("Wireless device with recever id {0} already added in {0}", hostReceverID, Environment.MachineName);
            else
            {
                AddWirelessDevice();
                if (ScanMiracastdevice())
                {
                    Log.Message("Successfully added wireless display with revever ID {0} into host {1}", hostReceverID, Environment.MachineName);
                    return true;
                }
                else
                    Log.Verbose("Unable to add wireless display with revever ID {0} into host {1}", hostReceverID, Environment.MachineName);
            }
            return false;
        }
        private static bool ScanNValidateDevice()
        {
            Log.Verbose("Running add device program");
            CommonExtensions.StartProcess("DevicePairingWizard", string.Empty, 15);
            AutomationElement element = UIABaseHandler.SelectElementAutomationIdControlType(AutomationElement.RootElement, "eDeviceList", ControlType.List);
            if (element != null)
            {
                Condition condition = new PropertyCondition(AutomationElement.ControlTypeProperty, ControlType.Button);
                AutomationElementCollection elementColn = element.FindAll(TreeScope.Descendants, condition);
                foreach (AutomationElement ele in elementColn)
                {
                    if (ele.Current.Name == hostReceverID)
                        return true;
                }

            }
            UIABaseHandler.InvokeElement(UIABaseHandler.SelectElementNameControlType("Cancel", ControlType.Button));
            return false;
        }
        private static bool ScanMiracastdevice()
        {
            Process deviceVerifyProcess = CommonExtensions.StartProcess("devcon.exe", " find *miracast*", 5);
            while (!deviceVerifyProcess.StandardOutput.EndOfStream)
            {
                if (deviceVerifyProcess.StandardOutput.ReadLine().ToUpper().Contains(hostReceverID))
                    return true;
            }
            return false;
        }

        private static void GetReceverID()
        {
            XmlDocument widiDeviceData = new XmlDocument();
            widiDeviceData.Load(@"Mapper\WiDiData.map");
            XmlElement root = widiDeviceData.DocumentElement;
            foreach (XmlNode fieldName in root.ChildNodes)
            {
                foreach (XmlNode attribute in fieldName.Attributes)
                {
                    if (Environment.MachineName.ToUpper() == attribute.Value.ToUpper())
                        hostReceverID = fieldName.InnerText.ToUpper();
                }
            }
        }
        private static void AddWirelessDevice()
        {
            Log.Verbose("Running add device program");
            CommonExtensions.StartProcess("DevicePairingWizard", string.Empty, 15);
            UIABaseHandler.InvokeElement(UIABaseHandler.SelectElementNameControlType(hostReceverID, ControlType.Button));
            UIABaseHandler.InvokeElement(UIABaseHandler.SelectElementNameControlType("Next", ControlType.Button));
          //  UIABaseHandler.I(UIABaseHandler.SelectElementNameControlType("Next", ControlType.Button));
            Thread.Sleep(30000);
        }
    }
}
