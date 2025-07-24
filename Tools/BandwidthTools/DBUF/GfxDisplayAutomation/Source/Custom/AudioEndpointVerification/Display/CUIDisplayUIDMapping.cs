namespace AudioEndpointVerification
{
    using System;
    using System.Collections.Generic;
    using System.IO;
    using System.Linq;
    internal class CUIDisplayUIDMapping
    {
        public CUIDisplayUIDMapping() { }
        public void DisplayUIDMapping(ref List<DisplayUIDMapper> actualmonIDList)
        {
            int DigitalDisplayCount = 0;
            foreach (DisplayUIDMapper eachMonID in actualmonIDList)
            {
                uint tempWinID = eachMonID.WinDowsMonID & 0x0FFFFFFF;
                switch (tempWinID >> ((tempWinID.ToString().Length) == 8 ? 24 : 16))
                {
                    case 1: // VGA
                        eachMonID.CuiMonID = 1;
                        break;
                    case 2: // TV
                    case 3: // DFP
                        eachMonID.CuiMonID = (uint)Math.Pow(2, 8 + DigitalDisplayCount++);
                        break;
                    case 4: // LFP
                        eachMonID.CuiMonID = 4096; 
                        break;
                    default:
                        Console.WriteLine("Cannot find CUI UID for display " + eachMonID);
                        eachMonID.CuiMonID = 0;
                        break;
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
                //Console.WriteLine("Return value from QDC call {0}", returnVal);
                if (!Convert.ToBoolean(returnVal))
                {
                    foreach (DISPLAYCONFIG_PATH_INFO eachPath in pathInfo)
                    {
                        if (!eachPath.targetInfo.id.Equals(0) &&
                            (eachPath.targetInfo.targetAvailable) &&
                            !monIDList.Any(UID => UID.WinDowsMonID.Equals(eachPath.targetInfo.id)) &&
                            !actualmonIDList.Any(UID => UID.WinDowsMonID.Equals(eachPath.targetInfo.id)))
                        {
                            DisplayUIDMapper mapper = new DisplayUIDMapper();
                            DriverEscape escapeData = new DriverEscape();
                            DriverEscapeData<uint, PORT> PortData = new DriverEscapeData<uint, PORT>() { input = eachPath.targetInfo.id };
                            escapeData.ParsePortName(PortData);
                            mapper.PortType = PortData.output;
                            mapper.WinDowsMonID = eachPath.targetInfo.id;

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
                    return actualmonIDList;
                }
                else
                  Console.WriteLine("QDC called failed, exiting the test");
                return null;
            }
        }
    }
}
