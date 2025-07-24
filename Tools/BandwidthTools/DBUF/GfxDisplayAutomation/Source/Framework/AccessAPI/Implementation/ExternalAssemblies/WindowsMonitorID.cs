namespace Intel.VPG.Display.Automation
{
    using System.Diagnostics;
    using System.Collections.Generic;
    using System.Text.RegularExpressions;
    internal class WindowsMonitorID : FunctionalBase, IGetAll
    {
        public object GetAll
        {
            get
            {
                List<uint> monIDList = new List<uint>();
                Process monitorID_process = CommonExtensions.StartProcess("devcon.exe", "find = port *monitor*");
                Regex rOption = new Regex("uid");
                uint result = 0;
                while (!monitorID_process.StandardOutput.EndOfStream)
                {
                    string line = monitorID_process.StandardOutput.ReadLine().ToLower();
                    if (line.Contains("uid"))
                    {
                        string[] Info = line.Split(':');
                        if (!string.IsNullOrEmpty(Info[0]))
                        {
                            string[] ID = rOption.Split(Info[0]);
                            if (ID != null && uint.TryParse(ID[1], out result))
                                if (!result.Equals(0))
                                    monIDList.Add(CommonExtensions.GetMaskedWindowsId(base.MachineInfo.OS.Type, result)); //workaround for Threshold OS issue for Windows ID.
                        }
                    }
                }
                return monIDList;
            }
        }
    }
}
