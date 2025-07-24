namespace AudioEndpointVerification
{
    using System;
    using System.Linq;
    using System.Collections.Generic;
    using System.Diagnostics;
    internal class DisplayEnumeration
    {
        public List<DisplayInfo> GetAll
        {
            get
            {
                CUIDisplayUIDMapping mapper = new CUIDisplayUIDMapping();
                return EnumerationAllDisplays(mapper.GetAll as List<DisplayUIDMapper>);
            }
        }
        private List<DisplayInfo> EnumerationAllDisplays(List<DisplayUIDMapper> monitorIDList)
        {
            List<DisplayInfo> enumeratedDisplays = new List<DisplayInfo>();
            List<DisplayType> winDisplayTypeList = new List<DisplayType>();
            List<DisplayType> sdkDisplayTypeList = new List<DisplayType>();
            if (null != monitorIDList && !monitorIDList.Count.Equals(0))
            {
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
                    foreach (DisplayUIDMapper eachUID in monitorIDList)
                    {
                        foreach (DISPLAYCONFIG_PATH_INFO eachPath in pathInfo)
                        {
                            if (!eachPath.targetInfo.id.Equals(0) && !enumeratedDisplays.Any(UID => UID.WindowsMonitorID == eachPath.targetInfo.id)
                                && (eachPath.targetInfo.targetAvailable) && eachPath.targetInfo.id.Equals(eachUID.WinDowsMonID))
                            {
                                DisplayInfo displayInfo = new DisplayInfo();
                                SDKDisplayEnumeration sdk = new SDKDisplayEnumeration();
                                displayInfo.CUIMonitorID = monitorIDList.Find(UID => UID.WinDowsMonID == eachPath.targetInfo.id).CuiMonID;
                                displayInfo.WindowsMonitorID = eachPath.targetInfo.id;
                                displayInfo.Port = monitorIDList.Find(UID => UID.WinDowsMonID == eachPath.targetInfo.id).PortType;
                                enumeratedDisplays.Add(displayInfo);

                                DisplayType windowsType = GetWindowsDisplayType(eachPath);
                                DisplayType sdkDisplayType = sdk.CUISDKDisplayType(displayInfo.CUIMonitorID);
                                if (sdkDisplayType == DisplayType.None)
                                {
                                    
                                    Console.WriteLine(" CUI SDK display type is {0}", sdkDisplayType.ToString());
                                }

                                byte[] edidData = sdk.GetEDID(displayInfo.CUIMonitorID);
                                if (edidData == null)
                                {
                                    Console.WriteLine("Reading EDID data using Windows API");
                                    EDIDData edidInfo = new EDIDData();
                                    edidData = edidInfo.GetEDIDDetails(displayInfo.WindowsMonitorID) as byte[];
                                }

                                List<DisplayType> tempList = sdkDisplayTypeList.Where(DT => DT.ToString().ToLower().StartsWith(sdkDisplayType.ToString().ToLower())).ToList();
                                if (tempList.Count == 0)
                                    sdkDisplayTypeList.Add(sdkDisplayType);
                                else
                                    sdkDisplayTypeList.Add(tempList.Last() + 1);
                                displayInfo.DisplayType = sdkDisplayTypeList.Last();

                                if (null != edidData)
                                    APIExtensions.SetMonitorNameNOptimalMode(enumeratedDisplays, displayInfo.DisplayType, edidData);
                                else
                                    Console.WriteLine("EDID for {0}-{1}-{2} returned null!", displayInfo.DisplayType, displayInfo.CUIMonitorID, displayInfo.WindowsMonitorID);

                                #region MIPI Display Type
                                if (displayInfo.DisplayType == DisplayType.EDP)
                                {
                                    DriverEscape escapeData = new DriverEscape();
                                    DriverEscapeData<uint, DisplayType> PortType = new DriverEscapeData<uint, DisplayType>() { input = eachPath.targetInfo.id };
                                    escapeData.ParseConnectorType(PortType);
                                    if (PortType.output == DisplayType.MIPI)
                                        displayInfo.DisplayType = DisplayType.MIPI;
                                }
                                #endregion

                                if (sdkDisplayType != windowsType)
                                {

                                    tempList = winDisplayTypeList.Where(DT => DT.ToString().ToLower().StartsWith(windowsType.ToString().ToLower())).ToList();
                                    foreach (DisplayInfo eachDisplayInfo in enumeratedDisplays.Where(DT => DT.DisplayType.ToString().ToLower().StartsWith(windowsType.ToString().ToLower())).ToList())
                                    {
                                        if (tempList.Count == 0)
                                            tempList.Add(windowsType);
                                        else
                                            tempList.Add(tempList.Last() + 1);
                                    }
                                    if (tempList.Count == 0)
                                        winDisplayTypeList.Add(windowsType);
                                    else
                                        winDisplayTypeList.Add(tempList.Last() + 1);
                                    displayInfo.DisplayType = winDisplayTypeList.Last();

                                    if (sdkDisplayType == DisplayType.WIDI && windowsType == DisplayType.CRT)
                                    {
                                        displayInfo.DisplayType = DisplayType.WIDI;
            
                                    }
                                    else if (sdkDisplayType == DisplayType.WIDI && windowsType == DisplayType.HDMI)
                                    {
                                        displayInfo.DisplayType = DisplayType.WIDI;
                                    }
                                }
                            }
                        }
                    }
                }
            }
            //PrintEnumeratedDisplay(enumeratedDisplays);
            return enumeratedDisplays;
        }

        internal static DisplayType GetWindowsDisplayType(DISPLAYCONFIG_PATH_INFO eachPath)
        {
            switch (eachPath.targetInfo.outputTechnology)
            {
                case DISPLAYCONFIG_VIDEO_OUTPUT_TECHNOLOGY.DISPLAYCONFIG_OUTPUT_TECHNOLOGY_HD15:
                    return DisplayType.CRT;
                case DISPLAYCONFIG_VIDEO_OUTPUT_TECHNOLOGY.DISPLAYCONFIG_OUTPUT_TECHNOLOGY_INTERNAL:
                    return DisplayType.EDP;
                case DISPLAYCONFIG_VIDEO_OUTPUT_TECHNOLOGY.DISPLAYCONFIG_OUTPUT_TECHNOLOGY_HDMI:
                    return DisplayType.HDMI;
                case DISPLAYCONFIG_VIDEO_OUTPUT_TECHNOLOGY.DISPLAYCONFIG_OUTPUT_TECHNOLOGY_DISPLAYPORT_EXTERNAL:
                    return DisplayType.DP;
                default:
                    return DisplayType.None;
            }
        }

        public void PrintEnumeratedDisplay(List<DisplayInfo> enumeratedDisplays)
        {
            Console.WriteLine("************** List Of Enumerated Display supported by System ***************");
            foreach (DisplayInfo eachEnumDisplay in enumeratedDisplays)
            {
                Console.WriteLine("Enumerated {0}: {1} - Windows monitor ID: {2}, CUI SDK ID {3}", eachEnumDisplay.DisplayType, eachEnumDisplay.CompleteDisplayName, eachEnumDisplay.WindowsMonitorID, eachEnumDisplay.CUIMonitorID);
                Console.WriteLine("Port information for display {0}: System port is {1}", eachEnumDisplay.DisplayType, eachEnumDisplay.Port);
                Console.WriteLine("------------------------------------------------------------------------------");
            }
            Console.WriteLine("*************** List Of Enumerated Display End ***************");
        }


    }
}
