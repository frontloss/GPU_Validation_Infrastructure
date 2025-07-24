using System;
using System.Collections.Generic;
using System.Linq;
using System.Management;
using System.Net.NetworkInformation;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    public static class NetworkExtensions
    {
        static NetworkAdapter _backUp;
        public static bool SetNetworkConnection(NetParam networkParam)
        {
            SelectQuery query = new SelectQuery("Win32_NetworkAdapter", "NetConnectionStatus=2");
            ManagementObjectSearcher search = new ManagementObjectSearcher(query);
            if (networkParam.adapter != Adapter.LAN)
            {
                Log.Abort("Invalid adapter argument");
                return false;
            }
            switch (networkParam.netWorkState)
            {
                case NetworkState.Disable:
                    if (GetLANUPStatus())
                        return DisableLAN(search);
                    else
                    {
                        Log.Message("LAN already Disabled");
                        return true;
                    }
                case NetworkState.Enable:
                    if (!GetLANUPStatus() && _backUp != null)
                        return EnableLAN(_backUp);
                    else
                    {
                        Log.Message("LAN already Enabled");
                        return true;
                    }
                default:
                    Log.Abort("Wrong network State");
                    break;
            }
            return false;
        }

        public static bool GetLANUPStatus()
        {
            Thread.Sleep(2000);
            bool status = false;
            NetworkInterface[] nic = NetworkInterface.GetAllNetworkInterfaces();
            foreach (NetworkInterface adapter in nic)
            {
                if (NetworkInterfaceType.Ethernet == adapter.NetworkInterfaceType
                    && adapter.OperationalStatus == OperationalStatus.Up)
                {
                    status = true;
                    break;
                }
            }
            return status;
        }

        private static bool DisableLAN(ManagementObjectSearcher search)
        {
            foreach (ManagementObject result in search.Get())
            {
                NetworkAdapter adapter = new NetworkAdapter(result);
                if (adapter.AdapterType.Equals("Ethernet 802.3"))
                {
                    if (System.Diagnostics.Debugger.IsAttached)
                    {
                        Log.Alert("Debugger is attached, Skipping Disabling LAN Connection");
                        return true;
                    }
                    _backUp = adapter;
                    Log.Verbose("Disabling LAN Connection ...");
                    adapter.Disable();
                    Thread.Sleep(20000);
                    if (!GetLANUPStatus())
                    {
                        if (!TestPostProcessing.RegisterCleanupRequest.ContainsKey(TestCleanUpType.LANConnection))
                        {
                            TestPostProcessing.RegisterCleanupRequest.Add(TestCleanUpType.LANConnection, null);
                        }
                        return true;
                    }
                    else
                        Log.Abort("Failed to disable LAN !!!");
                }
            }
            return false;
        }

        private static bool EnableLAN(NetworkAdapter backUp)
        {
            backUp.Enable();
            Thread.Sleep(45000);
            Log.Verbose("Enabling LAN Connection ...");
            if (GetLANUPStatus())
            {
                Log.Verbose("LAN Successfully Enabled..");
                return true;
            }
            else
            {
                Log.Abort("Failed to Enable LAN !!!");
            }
            return false;
        }

        public static bool GetWLANStatus()
        {
            Thread.Sleep(2000);
            bool status = false;
            NetworkInterface[] nic = NetworkInterface.GetAllNetworkInterfaces();
            foreach (NetworkInterface adapter in nic)
            {
                if (NetworkInterfaceType.Wireless80211 == adapter.NetworkInterfaceType
                    && adapter.Name.Trim().ToUpper() == "WI-FI")
                {
                    Log.Verbose("WLAN Enabled");
                    status = true;
                    break;
                }
            }
            return status;
        }
    }
}
