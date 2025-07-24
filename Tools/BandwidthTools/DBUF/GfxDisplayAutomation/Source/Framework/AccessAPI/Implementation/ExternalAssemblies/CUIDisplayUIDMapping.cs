namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.IO;
    using System.Linq;
    internal class CUIDisplayUIDMapping : FunctionalBase, IGetAll
    {
        public CUIDisplayUIDMapping() { }
        public void DisplayUIDMapping(ref List<DisplayUIDMapper> actualmonIDList)
        {
            int DigitalDisplayCount = 0;
            foreach (DisplayUIDMapper eachMonID in actualmonIDList)
            {
                switch (eachMonID.WindowsID >> ((eachMonID.WindowsID.ToString().Length) == 8 ? 24 : 16))
                {
                    case 1: // VGA
                        eachMonID.CuiID = 1;
                        break;
                    case 2: // TV
                    case 3: // DFP
                        eachMonID.CuiID = (uint)Math.Pow(2, 8 + DigitalDisplayCount++);
                        break;
                    case 4: // LFP
                        eachMonID.CuiID = 4096; 
                        break;
                    default:
                        Log.Alert("Cannot find CUI UID for display " + eachMonID);
                        eachMonID.CuiID = 0;
                        break;
                }
            }
        }

        public void dummy(Type type)
        {
           //object obj = Activator.CreateInstance(type);
           //base.CopyOver(obj);
        }

        private void ModifyMonListforActiveDongle(ref List<DisplayUIDMapper> monIDList)
        {
            SdkExtensions sdkExtn = base.CreateInstance<SdkExtensions>( new SdkExtensions());
            UInt32 numPathArrayElements = 0, numModeInfoArrayElements = 0;
            int returnVal = Interop.GetDisplayConfigBufferSizes((uint)QDCFlags.QDC_ALL_PATHS, ref numPathArrayElements, ref numModeInfoArrayElements);
            DISPLAYCONFIG_PATH_INFO[] pathInfo = new DISPLAYCONFIG_PATH_INFO[numPathArrayElements];
            DISPLAYCONFIG_MODE_INFO[] modeInfo = new DISPLAYCONFIG_MODE_INFO[numModeInfoArrayElements];
            DISPLAYCONFIG_TOPOLOGY_ID topologyId = DISPLAYCONFIG_TOPOLOGY_ID.DISPLAYCONFIG_TOPOLOGY_NULL;
            returnVal = Interop.QueryDisplayConfig((UInt32)QDCFlags.QDC_ALL_PATHS, ref numPathArrayElements, pathInfo,
                ref numModeInfoArrayElements, modeInfo, topologyId);
            if (!Convert.ToBoolean(returnVal))
            {
                foreach (DISPLAYCONFIG_PATH_INFO eachPath in pathInfo)
                {
                    uint tempWinMonID = CommonExtensions.GetMaskedWindowsId(base.MachineInfo.OS.Type, eachPath.targetInfo.id); //workaround for Threshold OS issue for Windows ID.
                    if (!tempWinMonID.Equals(0) && monIDList.Any(UID => UID.WindowsID == tempWinMonID)
                                && (eachPath.targetInfo.targetAvailable))
                    {
                        DisplayType windowsType = DisplayEnumeration.GetWindowsDisplayType(eachPath);
                        ISDK sdk = sdkExtn.GetSDKHandle(SDKServices.DisplayType);
                        DisplayType sdkDisplayType = (DisplayType)sdk.Get(monIDList.Find(DT => DT.WindowsID == tempWinMonID));
                        if (windowsType != sdkDisplayType)
                        {
                            DisplayUIDMapper tempDisplayList = monIDList.Where(DT => DT.WindowsID == tempWinMonID).First();
                            monIDList.Remove(monIDList.Where(DT => DT.WindowsID == tempWinMonID).First());
                            monIDList.Add(tempDisplayList);
                            break; ;
                        }
                    }
                }
            }
        }

        public object GetAll
        {
            get 
            {
                List<DisplayUIDMapper> monIDList = new List<DisplayUIDMapper>();
                List<DisplayUIDMapper> actualmonIDList = new List<DisplayUIDMapper>();
                UInt32 numPathArrayElements = 0, numModeInfoArrayElements = 0;
                int returnVal = Interop.GetDisplayConfigBufferSizes((uint)QDCFlags.QDC_ALL_PATHS, ref numPathArrayElements, ref numModeInfoArrayElements);
                DISPLAYCONFIG_PATH_INFO[] pathInfo = new DISPLAYCONFIG_PATH_INFO[numPathArrayElements];
                DISPLAYCONFIG_MODE_INFO[] modeInfo = new DISPLAYCONFIG_MODE_INFO[numModeInfoArrayElements];
                DISPLAYCONFIG_TOPOLOGY_ID topologyId = DISPLAYCONFIG_TOPOLOGY_ID.DISPLAYCONFIG_TOPOLOGY_NULL;
                returnVal = Interop.QueryDisplayConfig((UInt32)QDCFlags.QDC_ALL_PATHS, ref numPathArrayElements, pathInfo,
                ref numModeInfoArrayElements, modeInfo, topologyId);
                Log.Verbose("Return value from QDC call {0}", returnVal);
                if (!Convert.ToBoolean(returnVal))
                {
                    foreach (DISPLAYCONFIG_PATH_INFO eachPath in pathInfo)
                    {
                        uint tempWinMonID = CommonExtensions.GetMaskedWindowsId(base.MachineInfo.OS.Type, eachPath.targetInfo.id); //workaround for Threshold OS issue for Windows ID.

                        if (!tempWinMonID.Equals(0) &&
                            (eachPath.targetInfo.targetAvailable) &&
                            !monIDList.Any(UID => UID.WindowsID.Equals(tempWinMonID)) &&
                            !actualmonIDList.Any(UID => UID.WindowsID.Equals(tempWinMonID)))
                        {
                            DisplayUIDMapper mapper = new DisplayUIDMapper();
                            DriverEscape escapeData = new DriverEscape();
                            DriverEscapeData<uint, PORT> PortData = new DriverEscapeData<uint, PORT>() { input = tempWinMonID };
                            escapeData.ParsePortName(PortData);
                            mapper.PortType = PortData.output;
                            mapper.WindowsID = tempWinMonID;

                            switch (DisplayEnumeration.GetWindowsDisplayType(eachPath))
                            {
                                case DisplayType.DP:
                                    actualmonIDList.Add(mapper);
                                    actualmonIDList.Sort((x, y) => x.PortType.CompareTo(y.PortType));
                                    break;
                                default:
                                    monIDList.Add(mapper);
                                    monIDList.Sort((x, y) => x.PortType.CompareTo(y.PortType));
                                    break;
                            }
                        }
                    }
                    actualmonIDList.AddRange(monIDList);
                    DisplayUIDMapping(ref actualmonIDList);
                    ModifyMonListforActiveDongle(ref actualmonIDList);
                    return actualmonIDList;
                }
                else
                  Log.Abort("QDC called failed, exiting the test");
                return null;
            }
        }
    }
}
