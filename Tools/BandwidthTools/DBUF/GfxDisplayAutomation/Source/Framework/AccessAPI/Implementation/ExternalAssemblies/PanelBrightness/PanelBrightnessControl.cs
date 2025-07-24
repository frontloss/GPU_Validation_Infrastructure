using System;
using System.Collections.Generic;
using System.Linq;
using System.Management;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    class PanelBrightnessControl : FunctionalBase, IGetMethod, ISetMethod
    {
        SetBrightnessParam PanelSetParam;
        GetBrightnessParam PanelGetParam;
        public object GetMethod(object argMessage)
        {
            PanelGetParam = (GetBrightnessParam)argMessage;
            if (PanelGetParam == null)
            {
                Log.Alert("Invalid Panel Get Param");
                return false;
            }
            switch (PanelGetParam.ServiceType)
            {
                case PanelGetService.GetCurrentBrightness:
                    return GetCurrentBrightness();
                default:
                    Log.Fail("Invalide Input Parameter");
                    break;
            }

            return false;
        }

        public bool SetMethod(object argMessage)
        {
            PanelSetParam = (SetBrightnessParam)argMessage;
            if (PanelSetParam == null)
            {
                Log.Alert("Invalid Panel Set Param");
                return false;
            }
            switch (PanelSetParam.ServiceType)
            {
                case PanelSetService.SerBrightness:
                    return SetPanelBrightness();
                default:
                    Log.Fail("Invalide Input Parameter");
                    break;
            }
            return false;
        }

        private bool SetPanelBrightness()
        {
            ManagementClass mclass = new ManagementClass("WmiMonitorBrightnessMethods");
            mclass.Scope = new ManagementScope(@"\\.\root\wmi");
            ManagementObjectCollection instances = mclass.GetInstances();
            foreach (ManagementObject instance in instances)
            {
                ulong timeout = PanelSetParam.Timeout;
                ushort brightness = PanelSetParam.Brightness;
                object[] args = new object[] { timeout, brightness };
                instance.InvokeMethod("WmiSetBrightness", args);
            }
            return true;
        }

        private ushort GetCurrentBrightness()
        {
            ushort currentBrightness = 0;
            ManagementScope scope = new ManagementScope("root\\WMI");
            SelectQuery query = new SelectQuery("SELECT * FROM WmiMonitorBrightness");
            using (ManagementObjectSearcher searcher = new ManagementObjectSearcher(scope, query))
            {
                using (ManagementObjectCollection objectCollection = searcher.Get())
                {
                    foreach (ManagementObject mObj in objectCollection)
                    {
                        foreach (var item in mObj.Properties)
                        {
                            Console.WriteLine(item.Name + " " + item.Value.ToString());
                            if (item.Name == "CurrentBrightness")
                            {
                                currentBrightness = Convert.ToUInt16(item.Value);
                                break;
                            }
                        }
                    }
                }
            }
            return currentBrightness;
        }
    }
}
