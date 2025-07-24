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
    using System.Windows.Forms;
    using System.Net.NetworkInformation;


    internal static class AddWirelessDisplay
    {
        private static string hostReceverID = null;
        public static bool ScanNAddWirelessDisplayDevice(int enumDisplay)
        {
            GetReceverID();
            if (ScanNValidateDevice(enumDisplay))
                Log.Message("Wireless device with recever id {0} already added in {0}", hostReceverID, Environment.MachineName);
            else
            {
                AddWirelessDevice();
                if (ScanNValidateDevice(enumDisplay))
                {
                    Log.Message("Successfully added wireless display with revever ID {0} into host {1}", hostReceverID, Environment.MachineName);
                    return true;
                }
                else
                    Log.Abort("Unable to add wireless display with revever ID {0} into host {1}", hostReceverID, Environment.MachineName);
            }
            return false;
        }
        private static bool ScanNValidateDevice(int enumDisplayCount)
        {
            string[] splitChar = hostReceverID.Split(new char[] { ' ', '-' });
            if (enumDisplayCount > 1)
            {
                LaunchProjector projector = new LaunchProjector();
                projector.LaunchDispProjector();
                projector.PressTab(4);
                projector.Enter();
            }
            else if(enumDisplayCount == 1)
            {
                LaunchProjector projector = new LaunchProjector();
                projector.LaunchDispProjector();
                Thread.Sleep(2000);
            }
            Process deviceVerifyProcess = CommonExtensions.StartProcess("devcon.exe", " find *miracast*", 5);
            while (!deviceVerifyProcess.StandardOutput.EndOfStream)
            {
                if (deviceVerifyProcess.StandardOutput.ReadLine().ToUpper().Contains(splitChar[1].ToString().Trim().ToUpper()))
                {
                    Log.Verbose("Found miracast device in device manager");
                    return true;
                }
            }
            Log.Verbose("Could not find miracast device in device manager");
            return false;
        }
        private static void GetReceverID()
        {
            string MAC_ID = string.Empty;
            NetworkInterface[] nic = NetworkInterface.GetAllNetworkInterfaces();
            foreach (NetworkInterface adapter in nic)
            {
                if (adapter.Description.ToString().ToLower().Contains("intel") &&
                    NetworkInterfaceType.Wireless80211 == adapter.NetworkInterfaceType)
                {
                    MAC_ID = adapter.GetPhysicalAddress().ToString().Trim();
                    break;
                }
            }
            if (string.IsNullOrEmpty(MAC_ID))
                Log.Abort("Could not find MAC ID for host {0}", Environment.MachineName);
            else
                Log.Message("Host System MAC ID is {0}", MAC_ID);

            XmlDocument widiDeviceData = new XmlDocument();
            widiDeviceData.Load(@"Mapper\WiDiData.map");
            XmlElement root = widiDeviceData.DocumentElement;
            foreach (XmlNode fieldName in root.ChildNodes)
            {
                foreach (XmlNode attribute in fieldName.Attributes)
                {
                    if (MAC_ID.Trim().ToUpper() == attribute.Value.ToUpper())
                        hostReceverID = fieldName.InnerText.ToUpper();
                }
            }

            if (string.IsNullOrEmpty(hostReceverID))
                Log.Abort("could not find recever for host {0} with MAC ID {1}, please modify widiData.map file", Environment.MachineName, MAC_ID);
        }
        private static void AddWirelessDevice()
        {
            int keyDownCount = 20;
            int scrolDownCount = 10;
            int clickCount = 0;
            Log.Verbose("Running add device program");
            CommonExtensions.StartProcess("DevicePairingWizard", string.Empty, 15);
            AutomationElement DeviceControlItem = UIABaseHandler.SelectElementNameControlType("Add a device", ControlType.Window);
            Log.Verbose("Add device is selected");
            Thread.Sleep(2000);
            while (keyDownCount != 0)
            {
                Thread.Sleep(500);
                AutomationElement ele = UIABaseHandler.SelectElementNameControlType(hostReceverID, ControlType.Button);
                if (ele.Current.IsOffscreen == false && ele.Current.IsEnabled == true)
                {
                    Log.Verbose("Found receiver {0} in add device wizard", hostReceverID);
                    UIABaseHandler.InvokeElement(ele);
                    UIABaseHandler.InvokeElement(UIABaseHandler.SelectElementNameControlType("Next", ControlType.Button));
                    break;
                }
                while (clickCount != scrolDownCount)
                {
                    UIABaseHandler.InvokeElement(UIABaseHandler.SelectElementNameControlType("Line down", ControlType.Button));
                    clickCount++;
                }
                clickCount = 0;
                keyDownCount--;
            }
            Thread.Sleep(30000);
        }
    }
}
