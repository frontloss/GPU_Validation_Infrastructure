namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Linq;
    using System.Xml;
    using System.Text.RegularExpressions;
    public class AudioEnumeration : FunctionalBase, IGetAll, IGet, ISetMethod
    {
        public object GetAll
        {
            get
            {
                AudioDataProvider audioEndpointDataProvider = new AudioDataProvider();
                Config cfg = base.CreateInstance<Config>(new Config());

                DisplayConfig currentCfg = cfg.Get as DisplayConfig;
                Log.Verbose("Current display config is {0}", currentCfg.GetCurrentConfigStr());
                PipePlane pipeplaneInfo = base.CreateInstance<PipePlane>(new PipePlane());

                DriverEscape driverEscape = base.CreateInstance<DriverEscape>(new DriverEscape());
                EventRegisterInfo regCheck = base.CreateInstance<EventRegisterInfo>(new EventRegisterInfo());

                GetMaxSupportedEndpoint(audioEndpointDataProvider);
                foreach (DisplayType display in currentCfg.CustomDisplayList)
                {
                    AudioDisplayInfo audioDataInfo = new AudioDisplayInfo();
                    EventInfo eventInfo = new EventInfo();
                    PipePlaneParams pipePlaneObject = new PipePlaneParams(display);
                    if (DisplayExtensions.EnableMonitorTurnOff == false)
                    {
                        pipePlaneObject = pipeplaneInfo.GetMethod(pipePlaneObject) as PipePlaneParams;
                        DisplayExtensions.pipePlaneInfo.Add(pipePlaneObject);
                    }
                    else
                    {
                        if (DisplayExtensions.pipePlaneInfo.Count > 0)
                            pipePlaneObject = DisplayExtensions.pipePlaneInfo.Where(DT => DT.DisplayType == display).FirstOrDefault();
                        else
                            Log.Abort("Unable to find pipe plane Information from stored information");
                    }

                    DisplayInfo dispInfo = base.EnumeratedDisplays.Where(DT => DT.DisplayType == pipePlaneObject.DisplayType).First();
                    if (dispInfo.DisplayType != DisplayType.EDP)
                        audioDataInfo.displayFriendlyName = dispInfo.CompleteDisplayName.Replace(dispInfo.DisplayName, "").Trim();
                    else
                        audioDataInfo.displayFriendlyName = dispInfo.CompleteDisplayName;
                    audioDataInfo.planeInfo = pipePlaneObject.Plane;
                    audioDataInfo.isAudioCapablePannel = dispInfo.isAudioCapable;
                    audioDataInfo.dispType = dispInfo.DisplayType;
                    eventInfo.plane = pipePlaneObject.Plane;
                    Log.Verbose("Display {0} is attached to {1}", dispInfo.DisplayType, eventInfo.plane);
                    if (dispInfo.isAudioCapable)
                    {
                        Log.Message("Display {0} is audio capable pannel", dispInfo.DisplayType);
                        if (DisplayExtensions.EnableMonitorTurnOff && DisplayExtensions.AudioWTVideoEnable)
                        {
                            eventInfo.eventName = "AUDIO_REG_LP";
                        }
                        else
                            eventInfo.eventName = "AUDIO_ENABLE";
                        audioEndpointDataProvider.ActiveAudioEndpointDevice++;
                    }
                    else
                    {
                        Log.Message("Display {0} is not audio capable pannel", dispInfo.DisplayType);
                        eventInfo.eventName = "AUDIO_DISABLE";
                    }
                    EventInfo returnEventInfo = regCheck.GetMethod(eventInfo) as EventInfo;
                    foreach (RegisterInf reginfo in returnEventInfo.listRegisters)
                    {
                        Log.Message("Offset being checked = {0} Bitmap being checked {1}  Value to be got = {2}", reginfo.Offset, reginfo.Bitmap, reginfo.Value);
                        DriverEscapeData<uint, uint> driverData = new DriverEscapeData<uint, uint>();
                        driverData.input = Convert.ToUInt32(reginfo.Offset, 16);
                        DriverEscapeParams driverParams = new DriverEscapeParams(DriverEscapeType.Register, driverData);

                        if (!driverEscape.SetMethod(driverParams))
                            Log.Abort("Failed to read Register with offset as {0}", driverData.input);
                        else
                        {
                            if (CompareRegisters(driverData.output, reginfo, audioDataInfo))
                                audioDataInfo.isValidRegisterEntry = true;
                            else
                                audioDataInfo.isValidRegisterEntry = false;
                        }
                    }

                    audioEndpointDataProvider.ListAudioDisplayInfo.Add(audioDataInfo);
                }
                MMDeviceEnumerator DevEnum = new MMDeviceEnumerator();
                MMDeviceCollection enumAudioDisplayCollection = DevEnum.EnumerateAudioEndPoints(EDataFlow.eRender, EDeviceState.DEVICE_STATE_ACTIVE);
                for (int eachAudioEndPoint = 0; eachAudioEndPoint < enumAudioDisplayCollection.Count; eachAudioEndPoint++)
                {
                    string modelName = string.Empty;
                    Regex reg = new Regex("[^a-zA-Z-0-9]");
                    MMDevice endPointDevice = enumAudioDisplayCollection[eachAudioEndPoint];
                    modelName = reg.Replace(endPointDevice.FriendlyName, "");
                    if (audioEndpointDataProvider.ListAudioDisplayInfo.Any(CDN => CDN.displayFriendlyName.Replace(" ", "").Equals(modelName.Trim())))
                        audioEndpointDataProvider.ListAudioEndpointDevice.Add(endPointDevice.FriendlyName);
                }
                return audioEndpointDataProvider;
            }
        }

        private void GetMaxSupportedEndpoint(AudioDataProvider audioEndpointDataProvider)
        {
            XmlDocument benchmarkValue = new XmlDocument();
            benchmarkValue.Load("Mapper\\AudioEndpointData.map");
            XmlNode eventBenchmarkRoot = benchmarkValue.SelectSingleNode("/Data/NumAudioEndPoint");
            foreach (XmlNode eventNode in eventBenchmarkRoot.ChildNodes)
            {
                if (base.MachineInfo.PlatformDetails.Platform.ToString().Contains(Convert.ToString(eventNode.Attributes["id"].Value)))
                {
                    audioEndpointDataProvider.MaxSupportedAudioEndpoint = Convert.ToInt32(eventNode.Attributes["MaxSupportedEndpoints"].Value);
                    break;
                }
            }
        }

        public object Get
        {
            get
            {
                AudioMMDeviceData mmDeviceData = new AudioMMDeviceData();
                MMDeviceEnumerator DevEnum = new MMDeviceEnumerator();
                MMDevice device = DevEnum.GetDefaultAudioEndpoint(EDataFlow.eRender, ERole.eMultimedia);
                mmDeviceData.FriendlyName = device.FriendlyName;
                mmDeviceData.ID = device.ID;
                mmDeviceData.State = device.State;
                return mmDeviceData;
            }
        }

        public bool SetMethod(object argMessage)
        {
            SetAudioParam param = argMessage as SetAudioParam;
            bool status = false;
            if (param.setAudioInfo == SetAudioSource.SetAudioEndpoint)
            {
                PolicyConfigVista polConfig = new PolicyConfigVista();
                if (polConfig.SetAudioEndpoint(param.ID, ERole.eConsole) == 0)
                    status = true;
            }
            else
            {
                SdkExtensions sdkExtn = base.CreateInstance<SdkExtensions>(new SdkExtensions());
                ISDK sdkAudio = sdkExtn.GetSDKHandle(SDKServices.Audio);
                status = (bool)sdkAudio.Set(argMessage);
            }
            return status;
        }

        protected bool CompareRegisters(uint argDriverData, RegisterInf argRegInfo, AudioDisplayInfo argaudioDataInfo)
        {
            uint bit = Convert.ToUInt32(argRegInfo.Bitmap, 16);
            string binary = argDriverData.ToString("X");
            argaudioDataInfo.AUD_PIN_ELD_Reg_Value = BitMerge(Convert.ToString(argDriverData, 2));
            uint hex = Convert.ToUInt32(String.Format("{0:X}", argDriverData), 16);
            string valu = String.Format("{0:X}", hex & bit);
            Log.Verbose("after bitmap = {0}", valu);
            argaudioDataInfo.PlaneRegValue = valu;
            argaudioDataInfo.expectedRegValue = argRegInfo.Value;
            if (argaudioDataInfo.isAudioCapablePannel == false)
            {
                if ((Convert.ToInt32(valu) & 01) == 1)
                    return false;
                else
                    return true;
            }

            else if (String.Equals(valu, argRegInfo.Value))
                return true;
            return false;
        }
        private string BitMerge(string argData)
        {
            char[] dataBit = new char[14];
            for (int count = 0; count < dataBit.Length; count++)
            {
                if (count == 4 || count == 9)
                {
                    dataBit[4] = '-';
                    dataBit[9] = '-';
                }
                else
                    dataBit[count] = '0';
            }
            int index = dataBit.Length;
            for (int i = argData.Length - 1; i >= 0; i--)
            {
                if (dataBit[--index] == '-')
                {
                    i++;
                    continue;
                }
                dataBit[index] = argData[i];
            }
            string text = new string(dataBit);
            if (!string.IsNullOrEmpty(argData))
                return text;
            return string.Empty;
        }


    }
}
