namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.Threading.Tasks;

    internal class PlugUnPlugEnumeration : FunctionalBase, ISetMethod
    {
        private Dictionary<uint, DVMU_PORT> dvmuPortInfo = new Dictionary<uint, DVMU_PORT>();
        public bool SetMethod(object argMessage)
        {
            HotPlugUnplug HotPlugUnplugContext = argMessage as HotPlugUnplug;
            if (HotPlugUnplugContext == null)
            {
                Log.Abort("Plug/Unplug Enumerate object is null, aborting test execution");
            }
            if (HotPlugUnplugContext.FunctionName == FunctionName.PLUG ||
                HotPlugUnplugContext.FunctionName == FunctionName.PlugEnumerate)
                EnumerateAfterPlug(HotPlugUnplugContext.Port);
            else if (HotPlugUnplugContext.FunctionName == FunctionName.UNPLUG ||
                HotPlugUnplugContext.FunctionName == FunctionName.UnplugEnumerate)
                EnumerateAfterUnplug();
            return true;
        }

        private void EnumerateAfterPlug(DVMU_PORT port)
        {
            List<DisplayInfo> currentDisplayEnum = base.EnumeratedDisplays;

            List<DisplayInfo> displayInfoCollection = currentDisplayEnum.Where(DT => DT.DvmuPort != DVMU_PORT.None).ToList();
            if (displayInfoCollection.Count != 0)
            {
                foreach (DisplayInfo info in displayInfoCollection)
                {
                    dvmuPortInfo.Add(info.WindowsMonitorID, info.DvmuPort);
                }
            }
            List<uint> previousMonitorList = new List<uint>();
            foreach (DisplayInfo temp in base.EnumeratedDisplays)
            {
                previousMonitorList.Add(temp.WindowsMonitorID);
            }
            DisplayEnumeration enumDisplay = base.CreateInstance<DisplayEnumeration>(new DisplayEnumeration());
            List<DisplayInfo> enumeratedDisplay = enumDisplay.GetAll as List<DisplayInfo>;
            if (dvmuPortInfo.Count != 0)
            {
                foreach (DisplayInfo info in displayInfoCollection)
                {
                    DisplayInfo DIT = enumeratedDisplay.Where(DI => DI.WindowsMonitorID == dvmuPortInfo.Keys.First()).First();
                    DIT.DvmuPort = dvmuPortInfo.Values.First();
                }
            }
            List<uint> currentWinMonIDList = base.EnumeratedDisplays.Where(dI => !dI.WindowsMonitorID.Equals(0)).Select(dI => dI.WindowsMonitorID).ToList();
            List<uint> diffMonitorIdList = currentWinMonIDList.Except(previousMonitorList).ToList();
            if (diffMonitorIdList.Count == 1)
            {
                DisplayInfo DIT = enumeratedDisplay.Where(DI => DI.WindowsMonitorID == diffMonitorIdList.First()).First();
                DIT.DvmuPort = port;
                Log.Success("{0} is plugged successfully", DIT.DisplayType.ToString());
                enumDisplay.PrintEnumeratedDisplay(enumeratedDisplay);
            }
        }
        private void EnumerateAfterUnplug()
        {
            List<DisplayInfo> displayInfoCollection = base.EnumeratedDisplays.Where(DT => DT.DvmuPort != DVMU_PORT.None).ToList();
            if (displayInfoCollection.Count != 0)
            {
                foreach (DisplayInfo info in displayInfoCollection)
                {
                    dvmuPortInfo.Add(info.WindowsMonitorID, info.DvmuPort);
                }
            }
            DisplayEnumeration enumDisplay = base.CreateInstance<DisplayEnumeration>(new DisplayEnumeration());
            List<DisplayInfo> enumeratedDisplay = enumDisplay.GetAll as List<DisplayInfo>;
            if (dvmuPortInfo.Count != 0)
            {
                foreach (DisplayInfo info in enumeratedDisplay)
                {
                    foreach (uint winID in dvmuPortInfo.Keys)
                    {
                        if (info.WindowsMonitorID == winID)
                        {
                            DisplayInfo DIT = enumeratedDisplay.Find(DT => DT.WindowsMonitorID == winID);
                            DIT.DvmuPort = dvmuPortInfo.Values.First();
                        }
                    }
                }
            }
            enumDisplay.PrintEnumeratedDisplay(enumeratedDisplay);
        }
    }
}
