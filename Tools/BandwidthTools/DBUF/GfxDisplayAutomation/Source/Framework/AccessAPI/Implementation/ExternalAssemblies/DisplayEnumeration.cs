namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Linq;
    using System.Collections.Generic;
    using System.Diagnostics;
    internal class DisplayEnumeration : FunctionalBase, IGetAll, IGetMethod, ISetMethod
    {
        
        public object GetAll
        {
            get
            {
                CUIDisplayUIDMapping mapper = base.CreateInstance<CUIDisplayUIDMapping>(new CUIDisplayUIDMapping());
                return EnumerationAllDisplays(mapper.GetAll as List<DisplayUIDMapper>);
            }
        }
        public bool SetMethod(object argMessage)
        {
            List<DisplayInfo> enumeratedDisplay = argMessage as List<DisplayInfo>;
            return UpdateDvmuPortInfo(enumeratedDisplay);
        }

        public object GetMethod(object argMessage)
        {
            List<DisplayInfo> enmeratedDisplay = argMessage as List<DisplayInfo>;
            PrintEnumeratedDisplay(enmeratedDisplay);
            return true;
        }
        private List<DisplayInfo> EnumerationAllDisplays(List<DisplayUIDMapper> monitorIDList)
        {
            List<DisplayInfo> enumeratedDisplays = new List<DisplayInfo>();
            List<DisplayType> winDisplayTypeList = new List<DisplayType>();
            List<DisplayType> sdkDisplayTypeList = new List<DisplayType>();
            SdkExtensions sdkExtn = base.CreateInstance<SdkExtensions>(new SdkExtensions());

            if (null != monitorIDList && !monitorIDList.Count.Equals(0))
            {
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
                    foreach (DisplayUIDMapper eachUID in monitorIDList)
                    {
                        foreach (DISPLAYCONFIG_PATH_INFO eachPath in pathInfo)
                        {
                            uint tempWinMonID = CommonExtensions.GetMaskedWindowsId(base.MachineInfo.OS.Type, eachPath.targetInfo.id); //workaround for Threshold OS issue for Windows ID.

                            if (!tempWinMonID.Equals(0) && !enumeratedDisplays.Any(UID => UID.WindowsMonitorID == tempWinMonID)
                                && (eachPath.targetInfo.targetAvailable) && tempWinMonID == eachUID.WindowsID)
                            {
                                DisplayInfo displayInfo = new DisplayInfo();
                                displayInfo.WindowsMonitorID = tempWinMonID;
                                displayInfo.CUIMonitorID = monitorIDList.Find(UID => UID.WindowsID == displayInfo.WindowsMonitorID).CuiID;
                                displayInfo.Port = monitorIDList.Find(UID => UID.WindowsID == displayInfo.WindowsMonitorID).PortType;
                                displayInfo.DvmuPort = DVMU_PORT.None;
                                enumeratedDisplays.Add(displayInfo);

                                DisplayType windowsType = GetWindowsDisplayType(eachPath);
                                ISDK sdkDispType = sdkExtn.GetSDKHandle(SDKServices.DisplayType);
                                DisplayType sdkDisplayType = (DisplayType)sdkDispType.Get(eachUID);

                                if (sdkDisplayType == DisplayType.None)
                                {
                                    Log.Fail(" CUI SDK display type is {0}", sdkDisplayType.ToString());
                                    CommonExtensions.Exit(0);
                                }

                                ISDK sdkEdid = sdkExtn.GetSDKHandle(SDKServices.EDID);
                                byte[] edidData = (byte[]) sdkEdid.Get(eachUID);
                                if (edidData == null)
                                {
                                    Log.Verbose("Reading EDID data using Windows API");
                                    EDIDData edidInfo = new EDIDData();
                                    edidData = edidInfo.GetEDIDDetails(displayInfo.WindowsMonitorID) as byte[];
                                }

                                //Ignore RAR display interface.
                                if ((edidData != null && edidData.Length >= 128) && (edidData[8] == 0x48 && edidData[9] == 0x32))
                                {
                                    enumeratedDisplays.Remove(displayInfo);
                                    continue;
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
                                    Log.Abort("EDID for {0}-{1}-{2} returned null!", displayInfo.DisplayType, displayInfo.CUIMonitorID, displayInfo.WindowsMonitorID);

                                #region MIPI Display Type
                                if (displayInfo.DisplayType == DisplayType.EDP)
                                {
                                    DriverEscape escapeData = new DriverEscape();
                                    DriverEscapeData<uint, DisplayType> PortType = new DriverEscapeData<uint, DisplayType>() { input = displayInfo.WindowsMonitorID };
                                    escapeData.ParseConnectorType(PortType);
                                    if (PortType.output == DisplayType.MIPI)
                                        displayInfo.DisplayType = DisplayType.MIPI;
                                }
                                #endregion

                                #region Fill Internal Or External Display Information
                                if (displayInfo.DisplayType == DisplayType.EDP || displayInfo.DisplayType == DisplayType.MIPI)
                                {
                                    displayInfo.displayExtnInformation = DisplayExtensionInfo.Internal;
                                }
                                else
                                {
                                    displayInfo.displayExtnInformation = DisplayExtensionInfo.External;
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
                                        displayInfo.ConnectorType = DisplayInfoCollection.Collection.Where(DI => DI.DisplayType == DisplayType.CRT).First().ConnectorType;
                                    }
                                    else if (sdkDisplayType == DisplayType.WIDI && windowsType == DisplayType.HDMI)
                                    {
                                        displayInfo.DisplayType = DisplayType.WIDI;
                                    }
                                    else if (sdkDisplayType == DisplayType.DVI) // CUISDK detecting WiGig display as DVI
                                    {
                                        if (VerifyRegister("WDE_Transcoder_CTL0_Register", PIPE.NONE, PLANE.NONE, PORT.NONE))
                                        {
                                             //Set displayInfo.DisplayType to WIGIG_DP only if DVI is detected as WiGig Display.
                                             //Otherwise, let displayInfo.DisplayType be default DVI.
                                            displayInfo.DisplayType = DisplayType.WIGIG_DP;
                                        }
                                            //Check for second WiGig Path
                                        else if (VerifyRegister("WDE_Transcoder_CTL1_Register", PIPE.NONE, PLANE.NONE, PORT.NONE))   
                                         {
                                                displayInfo.DisplayType = DisplayType.WIGIG_DP2;
                                         }
                                    }
                                    DongleExtensions dongleExtn = base.CreateInstance<DongleExtensions>(new DongleExtensions());
                                    dongleExtn.GetDongleData(enumeratedDisplays.Where(DUID => DUID.CUIMonitorID == displayInfo.CUIMonitorID).First());
                                }
                            }
                        }
                    }
                }
            }
            if (null != base.ParamInfo && base.ParamInfo.ContainsKey(ArgumentType.Enumeration) && null != base.ParamInfo[ArgumentType.Enumeration])
            {
                (base.ParamInfo[ArgumentType.Enumeration] as List<DisplayInfo>).Clear();
                base.ParamInfo[ArgumentType.Enumeration] = enumeratedDisplays;
            }
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
                case DISPLAYCONFIG_VIDEO_OUTPUT_TECHNOLOGY.DISPLAYCONFIG_OUTPUT_TECHNOLOGY_DVI:
                    Log.Message("Assuming it to be HDMI");
                    return DisplayType.HDMI;
                default:
                    Log.Message("No match found, returning display type as NONE");
                    return DisplayType.None;
            }
        }

        protected bool UpdateDvmuPortInfo(List<DisplayInfo> enumeratedDisplays)
        {
            string dvmuHWID = "usb*vid_8087*pid_f021*";
            Process nodesProcess = CommonExtensions.StartProcess("devcon.exe", string.Concat("status ", dvmuHWID));
            string processName = nodesProcess.StandardOutput.ReadLine().ToLower();
            if (processName.Contains("usb") && processName.Contains("vid_8087") && processName.Contains("pid_f021"))
            {
                List<DVMU_PORT> dvmuPortList = new List<DVMU_PORT>() { DVMU_PORT.PORTA, DVMU_PORT.PORTB };
                List<DisplayInfo> hdmiWithoutDVMUPort = enumeratedDisplays.Where(dI => dI.DisplayType.ToString().Contains("HDMI") && dI.DvmuPort == DVMU_PORT.None).ToList();

                foreach (DisplayInfo curHDMI in hdmiWithoutDVMUPort)
                {
                    List<DVMU_PORT> enumeratedPortList = enumeratedDisplays.Select(dI => dI.DvmuPort).ToList();
                    List<DVMU_PORT> freeDvmuPort = dvmuPortList.Except(enumeratedPortList).ToList();
                    if (freeDvmuPort.Count() > 0)
                    {
                        curHDMI.DvmuPort = freeDvmuPort.First();
                    }
                    else
                        return false;
                }
            }
            return true;
        }
        public void PrintEnumeratedDisplay(List<DisplayInfo> enumeratedDisplays)
        {
            Log.Verbose("************** List Of Enumerated Display supported by System ***************");
            foreach (DisplayInfo eachEnumDisplay in enumeratedDisplays)
            {
                Log.Verbose("{0}: {1} - Windows ID: 0x{2}, CUI SDK ID: {3}", eachEnumDisplay.DisplayType, eachEnumDisplay.CompleteDisplayName, eachEnumDisplay.WindowsMonitorID.ToString("X"), eachEnumDisplay.CUIMonitorID);
                Log.Verbose("System port: {0}, DVMU port: {1} Audio capable: {2}", eachEnumDisplay.Port, eachEnumDisplay.DvmuPort, eachEnumDisplay.isAudioCapable);
                Log.Verbose("Serial No: {0}, Optmal Resolution is {1}x{2}x{3}{4}Hz", eachEnumDisplay.SerialNum, eachEnumDisplay.DisplayMode.HzRes, eachEnumDisplay.DisplayMode.VtRes, eachEnumDisplay.DisplayMode.RR, eachEnumDisplay.DisplayMode.InterlacedFlag.Equals(0) ? "p" : "i");
                Log.Verbose("Color support: XvYcc: {0}, YcBcr: {1}, MaxBPC: {2}", eachEnumDisplay.ColorInfo.IsXvYcc, eachEnumDisplay.ColorInfo.IsYcBcr, eachEnumDisplay.ColorInfo.MaxDeepColorValue);
                Log.Verbose("------------------------------------------------------------------------------");
            }
            Log.Verbose("*************** List Of Enumerated Display End ***************");
        }

        private bool VerifyRegister(string registerEvent, PIPE pipe, PLANE plane, PORT port)
        {
            EventInfo eventInfo = new EventInfo();
            EventRegisterInfo eventRegisterInfo = base.CreateInstance<EventRegisterInfo>(new EventRegisterInfo());
            Log.Verbose("Fetching Registers for event:{0} with factors:{1},{2},{3}", registerEvent, pipe, plane, port);
            eventInfo.pipe = pipe;
            eventInfo.plane = plane;
            eventInfo.port = port;
            eventInfo.eventName = registerEvent;
            eventRegisterInfo.MachineInfo = base.MachineInfo;
            EventInfo returnEventInfo = (EventInfo)eventRegisterInfo.GetMethod(eventInfo);
            return returnEventInfo.RegistersMatched;
        }
    }
}
