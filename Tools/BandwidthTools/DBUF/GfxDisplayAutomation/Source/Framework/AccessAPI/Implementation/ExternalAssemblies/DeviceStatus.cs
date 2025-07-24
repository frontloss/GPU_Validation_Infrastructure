namespace Intel.VPG.Display.Automation
{
    using System;
    using System.IO;
    using System.Linq;
    using System.Threading;
    using System.Diagnostics;
    using System.Collections.Generic;
    using System.Runtime.InteropServices;
    using System.Text;

    internal class DeviceStatus : FunctionalBase, IGetMethod
    {
        public object GetMethod(object argMessage)
        {
            string HardwareID = argMessage as string;
            bool status = false;

            string result = string.Empty;
            Process nodesProcess = CommonExtensions.StartProcess("devcon.exe", string.Concat("status ", HardwareID));
            Log.Verbose("Getting device status for {0}", HardwareID);

            while (!nodesProcess.StandardOutput.EndOfStream)
            {
                result = nodesProcess.StandardOutput.ReadLine();
                Log.Verbose("{0}", result);
                if (result.ToLower().Contains("running"))
                    status = true;
            }
            return status;
        }

    }
}
