namespace AudioEndpointVerification
{
    using Microsoft.Win32;
    using System;
    using System.Collections.Generic;
    using System.Diagnostics;
    using System.Linq;
    using System.Text;
    using System.Threading.Tasks;
    class EDIDData
    {
        List<string> monitorDetails;
        RegistryKey Key;
        public List<string> MonitorDetails
        {
            get { return monitorDetails; }
        }
        private string[] DisplaySerialNo;
        public EDIDData()
        {
            monitorDetails = GetMonitorDetails();
        }
        private List<string> GetMonitorDetails()
        {
            List<string> MonitorIDs = new List<string>();
            Process monitorID_process = CommonExtension.StartProcess("devcon.exe", "find = port *monitor*");
            while (!monitorID_process.StandardOutput.EndOfStream)
            {
                string line = monitorID_process.StandardOutput.ReadLine().ToLower().Trim();
                if (line.ToLower().Contains("display"))
                {
                    string[] Info = line.Split(':');
                    MonitorIDs.Add(Info.First().Trim());
                }
            }
            return MonitorIDs;
        }
        public object GetEDIDDetails(object windowsMonID)
        {
            foreach (string eachMonDetails in monitorDetails)
            {
                if (eachMonDetails.Contains(Convert.ToString(windowsMonID)))
                {
                    Console.WriteLine("Fetching Monitor Details for {0} ", eachMonDetails);
                    if (Verify(eachMonDetails, true))
                        return GetEDIDRawData(eachMonDetails);
                    else
                    {
                        GetDisplayModels();
                        string[] monIDData = eachMonDetails.Split('\\');
                        foreach (string temp in DisplaySerialNo)
                        {
                            monIDData[1] = temp;
                            if (Verify(string.Join("\\", monIDData), true))
                                return GetEDIDRawData(string.Join("\\", monIDData));
                        }
                    }
                }
            }
            return null;
        }
        private object GetEDIDRawData(string MonDetails)
        {
            string Path = @"SYSTEM\CurrentControlSet\Enum\" + MonDetails + @"\Device Parameters";
            Key = Registry.LocalMachine.OpenSubKey(Path);
            byte[] edidData = Key.GetValue("EDID") as byte[];
            byte[] nullData = new byte[256 - edidData.Length];
            byte[] newData = edidData.Concat(nullData).ToArray();
            return newData;
        }

        private void GetDisplayModels()
        {
            string Path = @"SYSTEM\CurrentControlSet\Enum\Display";
            Key = Registry.LocalMachine.OpenSubKey(Path);
            DisplaySerialNo = Key.GetSubKeyNames();
        }

        private bool Verify(string MonDetails, bool getEDID = false)
        {
            Key = Registry.LocalMachine.OpenSubKey(@"SYSTEM\CurrentControlSet\Enum\" + MonDetails + @"\Device Parameters");
            if (Key == null)
                return false;
            else
            {
                if (getEDID)
                {
                    byte[] edidData = Key.GetValue("EDID") as byte[];
                    if (edidData != null)
                        return true;
                    else
                        return false;
                }
            }
            return true;
        }
    }
}
